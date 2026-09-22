#!/usr/bin/env python3
"""Post-hoc matched system metrics for all four saved methods (planning task E1).

Reads saved v2 reference rankings and saved primary element-pair rankings, checks
every input against its bundle inventory, and reports composition hits, system
coverage, concentration and cutoff ties on identical held-out sets. Nothing is
refit, re-ranked, re-split or relabelled. Specification:
docs/paper-planning/09-e0-system-metrics-spec.md.
"""
import argparse
import json
import math
import shutil
import tomllib
from collections import Counter
from pathlib import Path
from statistics import mean, median

from analyze_pu_pilot import require, rows, sha, write_rows
from analyze_system_holdout import system, DESIGNS, POLICIES

METHODS = ("random", "popularity", "similarity", "element_pair")
REFERENCE = "popularity"
BUDGETS = (20, 50, 100, 200)
SEEDS = tuple(range(20))
V2_CONFIG_SHA = "c55cc2cf29f75b74abda3dc66194043339b564cf1614d925434adcb581932565"
PAIR_CONFIG_SHA = "f7b4d6268ed29ed10e60d53c6d31a49673cf9b218af3c369f21e885cf8d94525"
FLOAT_TOLERANCE = 1e-12
REPOSITORY = Path(__file__).resolve().parent.parent
KERNEL_SOURCES = ("compositions.jl", "benchmark.jl", "ranking_evaluation.jl")
SUMMARY_FIELDS = ("hits", "selected_system_count", "relevant_system_count", "hit_system_count",
                  "system_recall", "effective_hit_systems", "largest_hit_system_fraction",
                  "random_expected_hits", "random_expected_hit_systems")
DIFFERENCE_FIELDS = ("hits", "hit_system_count", "system_recall", "effective_hit_systems")
JULIA_INTEGER_FIELDS = ("hits", "candidate_count", "relevant_count", "selected_system_count",
                        "relevant_system_count", "hit_system_count", "cutoff_tie_size", "cutoff_tie_selected")
JULIA_FLOAT_FIELDS = ("system_recall", "effective_hit_systems", "largest_hit_system_fraction", "cutoff_score")


class Inventory:
    """Hash-checked reader for one result bundle."""

    def __init__(self, run, expected_sha):
        require(sha(run/"config.toml") == expected_sha, f"unexpected config identity: {run}")
        self.run = run
        self.config = tomllib.loads((run/"config.toml").read_text())
        self.hashes = self.config["deterministic_file_hashes"]
        self.files_read = 0

    def digest(self, name):
        require(name in self.hashes, f"{name} absent from {self.run} inventory")
        return self.hashes[name]

    def read(self, name):
        require(sha(self.run/name) == self.digest(name), f"hash mismatch: {self.run/name}")
        self.files_read += 1
        return rows(self.run/name)


def split_path(design, policy, seed):
    return f"{design}/{policy}/split-{seed:02}"


def load_membership(v2, pair, design, policy, seed):
    folder = split_path(design, policy, seed)
    for name in ("inputs/training.tsv", "inputs/candidates.tsv", "evaluation/heldout.tsv", "evaluation/labels.tsv"):
        require(pair.digest(f"baseline/{folder}/{name}") == v2.digest(f"{folder}/{name}"),
                f"pair and v2 memberships differ: {folder}/{name}")
    candidates = [r["composition"] for r in v2.read(f"{folder}/inputs/candidates.tsv")]
    labels = {r["composition"]: r["label"] for r in v2.read(f"{folder}/evaluation/labels.tsv")}
    heldout = [r["composition"] for r in v2.read(f"{folder}/evaluation/heldout.tsv")]
    require(len(set(candidates)) == len(candidates) and set(labels) == set(candidates), f"label/candidate mismatch: {folder}")
    require(set(labels.values()) <= {"positive", "unlabelled"}, f"unexpected label: {folder}")
    require(len(set(heldout)) == len(heldout) and set(heldout) == {c for c, l in labels.items() if l == "positive"},
            f"held-out set is not the positive candidates: {folder}")
    return set(candidates), labels, set(heldout)


def load_ranking(v2, pair, design, policy, seed, method, candidates, labels):
    folder = split_path(design, policy, seed)
    ranked = pair.read(f"{folder}/ranking.tsv") if method == "element_pair" else v2.read(f"{folder}/{method}.tsv")
    require([int(r["rank"]) for r in ranked] == list(range(1, len(ranked)+1)), f"ranks not 1..N: {folder} {method}")
    formulas = [r["composition"] for r in ranked]
    require(len(formulas) == len(candidates) and set(formulas) == candidates, f"ranking is not a candidate permutation: {folder} {method}")
    require(all(r["observed_label"] == labels[r["composition"]] for r in ranked), f"ranking label mismatch: {folder} {method}")
    if method == "random":
        require(all(r["score"] == "" for r in ranked), "random ranking unexpectedly has scores")
        return formulas, None
    scores = [float(r["score"]) for r in ranked]
    require(all(math.isfinite(s) for s in scores) and all(a >= b for a, b in zip(scores, scores[1:])),
            f"scores not finite and descending: {folder} {method}")
    return formulas, scores


def random_expected_hit_systems(relevant_by_system, candidate_count, budget):
    """Exact expectation of hit systems for a uniform random K-subset."""
    total = 0.0
    for _, size in sorted(relevant_by_system.items()):  # fixed float summation order
        miss = 1.0
        for i in range(size):
            miss *= max(candidate_count - budget - i, 0) / (candidate_count - i)
        total += 1.0 - miss
    return total


def tie_fields(formulas, scores, heldout, budget, hits):
    if scores is None:
        return dict(cutoff_score="NA", cutoff_tie_size="NA", cutoff_tie_selected="NA", cutoff_tie_crosses="NA",
                    hits_tie_min="NA", hits_tie_max="NA", hits_tie_expected="NA")
    cutoff = scores[budget-1]
    block = [i for i, s in enumerate(scores) if s == cutoff]
    require(block == list(range(block[0], block[-1]+1)), "tie block not contiguous")
    size, selected = len(block), sum(i < budget for i in block)
    positives = sum(formulas[i] in heldout for i in block)
    strict = hits - sum(formulas[i] in heldout for i in block if i < budget)
    return dict(cutoff_score=repr(cutoff), cutoff_tie_size=size, cutoff_tie_selected=selected,
                cutoff_tie_crosses=str(selected < size).lower(),
                hits_tie_min=strict + max(0, selected - (size - positives)),
                hits_tie_max=strict + min(selected, positives),
                hits_tie_expected=strict + selected*positives/size)


def ranking_rows(design, policy, seed, method, formulas, scores, heldout):
    relevant_by_system = Counter(system(f) for f in heldout)
    candidate_count, relevant_count = len(formulas), len(heldout)
    result = []
    for budget in BUDGETS:
        top = formulas[:budget]
        hit_systems = Counter(system(f) for f in top if f in heldout)
        hits = sum(hit_systems.values())
        result.append(dict(
            design=design, policy=policy, split_seed=seed, method=method, budget=budget,
            hits=hits, candidate_count=candidate_count, relevant_count=relevant_count,
            selected_system_count=len({system(f) for f in top}),
            relevant_system_count=len(relevant_by_system),
            hit_system_count=len(hit_systems),
            system_recall=len(hit_systems)/len(relevant_by_system),
            effective_hit_systems=hits*hits/sum(n*n for n in hit_systems.values()) if hits else 0.0,
            largest_hit_system_fraction=max(hit_systems.values())/hits if hits else 0.0,
            random_expected_hits=budget*relevant_count/candidate_count,
            random_expected_hit_systems=random_expected_hit_systems(relevant_by_system, candidate_count, budget),
            **tie_fields(formulas, scores, heldout, budget, hits)))
    return result


def saved_metrics(v2, pair):
    saved = {}
    for inventory in (v2, pair):
        for r in inventory.read("metrics.tsv"):
            key = (r["design"], r["policy"], int(r["split_seed"]), r["method"], int(r["budget"]))
            require(key not in saved, f"duplicate saved metric row: {key}")
            saved[key] = (int(r["hits"]), int(r["candidate_count"]), int(r["heldout_count"]))
    return saved


def summarize(detail):
    summary = []
    for design in DESIGNS:
        for policy in POLICIES:
            for method in METHODS:
                for budget in BUDGETS:
                    rs = [r for r in detail if (r["design"], r["policy"], r["method"], r["budget"]) == (design, policy, method, budget)]
                    require(len(rs) == len(SEEDS), "incomplete summary group")
                    row = dict(design=design, policy=policy, method=method, budget=budget, splits=len(rs))
                    row.update({f"{field}_mean": mean(r[field] for r in rs) for field in SUMMARY_FIELDS})
                    row["cutoff_tie_crossing_splits"] = "NA" if method == "random" else sum(r["cutoff_tie_crosses"] == "true" for r in rs)
                    for field in ("hits_tie_min", "hits_tie_max"):
                        row[f"{field}_mean"] = "NA" if method == "random" else mean(r[field] for r in rs)
                    summary.append(row)
    return summary


def paired_differences(detail):
    index = {(r["design"], r["policy"], r["split_seed"], r["method"], r["budget"]): r for r in detail}
    result = []
    for design in DESIGNS:
        for policy in POLICIES:
            for method in METHODS:
                if method == REFERENCE:
                    continue
                for budget in BUDGETS:
                    for field in DIFFERENCE_FIELDS:
                        diffs = [index[design, policy, s, method, budget][field] - index[design, policy, s, REFERENCE, budget][field] for s in SEEDS]
                        result.append(dict(design=design, policy=policy, contrast=f"{method}-{REFERENCE}", budget=budget,
                                           field=field, splits=len(diffs), mean=mean(diffs), median=median(diffs),
                                           min=min(diffs), max=max(diffs), positive=sum(d > 0 for d in diffs),
                                           zero=sum(d == 0 for d in diffs), negative=sum(d < 0 for d in diffs)))
    return result


def tie_sensitivity(detail):
    """Paired Hits@K contrasts versus popularity when only crossing tie blocks are reordered."""
    index = {(r["design"], r["policy"], r["split_seed"], r["method"], r["budget"]): r for r in detail}
    result = []
    for design in DESIGNS:
        for policy in POLICIES:
            for method in ("similarity", "element_pair"):
                for budget in BUDGETS:
                    pairs = [(index[design, policy, s, method, budget], index[design, policy, s, REFERENCE, budget]) for s in SEEDS]
                    least = [m["hits_tie_min"] - r["hits_tie_max"] for m, r in pairs]
                    most = [m["hits_tie_max"] - r["hits_tie_min"] for m, r in pairs]
                    result.append(dict(design=design, policy=policy, contrast=f"{method}-{REFERENCE}", budget=budget, splits=len(pairs),
                                       saved_mean=mean(m["hits"] - r["hits"] for m, r in pairs),
                                       random_tie_expected_mean=mean(m["hits_tie_expected"] - r["hits_tie_expected"] for m, r in pairs),
                                       least_favourable_mean=mean(least), least_favourable_positive=sum(d > 0 for d in least),
                                       least_favourable_negative=sum(d < 0 for d in least), most_favourable_mean=mean(most)))
    return result


def primary_contrast(differences):
    policies = {}
    for r in differences:
        if (r["design"], r["contrast"], r["budget"], r["field"]) == ("system", "element_pair-popularity", 100, "hit_system_count"):
            policies[r["policy"]] = dict(mean=r["mean"], median=r["median"], min=r["min"], max=r["max"],
                                         positive=r["positive"], zero=r["zero"], negative=r["negative"],
                                         favours_pair=r["mean"] > 0 and r["positive"] > r["negative"])
    require(set(policies) == set(POLICIES), "primary contrast incomplete")
    count = sum(p["favours_pair"] for p in policies.values())
    reading = "extends" if count == len(POLICIES) else "mixed" if count else "does_not_extend"
    return dict(design="system", budget=100, contrast="element_pair-popularity", field="hit_system_count",
                policies=policies, policies_favouring_pair=count, reading=reading)


def compare_julia(detail, path):
    julia = {(r["design"], r["policy"], int(r["split_seed"]), r["method"], int(r["budget"])): r for r in rows(path)}
    require(len(julia) == len(detail), f"Julia row count {len(julia)} != {len(detail)}")
    worst = 0.0
    for r in detail:
        j = julia[(r["design"], r["policy"], r["split_seed"], r["method"], r["budget"])]
        for field in JULIA_INTEGER_FIELDS:
            require(str(r[field]) == j[field], f"Julia {field} mismatch: {r['design']} {r['policy']} {r['split_seed']} {r['method']} {r['budget']}")
        for field in JULIA_FLOAT_FIELDS:
            if r[field] == "NA" or j[field] == "NA":
                require(r[field] == j[field], f"Julia NA mismatch: {field}")
                continue
            gap = abs(float(r[field]) - float(j[field]))
            require(gap <= FLOAT_TOLERANCE, f"Julia {field} differs by {gap}")
            worst = max(worst, gap)
        require(r["cutoff_tie_crosses"] == j["cutoff_tie_crosses"], "Julia tie crossing mismatch")
    return dict(rows=len(julia), integer_fields=list(JULIA_INTEGER_FIELDS), float_fields=list(JULIA_FLOAT_FIELDS),
                max_abs_float_difference=worst, tolerance=FLOAT_TOLERANCE, status="passed")


def compare_prior_concentration(detail, analysis):
    """Agreement with the v0.1.1 pair-model concentration diagnostic (C7)."""
    manifest = json.loads((analysis/"SHA256SUMS.json").read_text())["files"]
    name = "system-concentration-by-split.tsv"
    require(sha(analysis/name) == manifest[name], "prior concentration file hash mismatch")
    index = {(r["policy"], r["split_seed"]): r for r in detail
             if (r["design"], r["method"], r["budget"]) == ("system", "element_pair", 100)}
    prior = rows(analysis/name)
    require(len(prior) == len(index), "prior concentration row count mismatch")
    for p in prior:
        r = index[p["policy"], int(p["split_seed"])]
        require(int(p["top100_hits"]) == r["hits"] and int(p["distinct_systems"]) == r["selected_system_count"]
                and int(p["positive_hit_systems"]) == r["hit_system_count"]
                and abs(float(p["effective_hit_systems"]) - r["effective_hit_systems"]) <= FLOAT_TOLERANCE
                and abs(float(p["largest_hit_system_fraction"]) - r["largest_hit_system_fraction"]) <= FLOAT_TOLERANCE,
                f"prior concentration mismatch: {p['policy']} {p['split_seed']}")
    return dict(rows=len(prior), file_sha256=manifest[name], status="passed")


def report(summary, differences, primary, validation):
    lookup = {(r["design"], r["policy"], r["method"], r["budget"]): r for r in summary}
    diff = {(r["design"], r["policy"], r["contrast"], r["budget"], r["field"]): r for r in differences}
    lines = ["# Matched system metrics (E1, post hoc)", "",
             "Saved rankings only; no refit. Means are macro-averages over 20 overlapping holdouts; "
             "systems are element sets, not validated chemical diversity. Random reference = exact uniform-random expectation.", "",
             f"**Primary contrast** (system design, K=100, element_pair − popularity, hit systems): reading = `{primary['reading']}` "
             f"({primary['policies_favouring_pair']}/3 policies meet the pre-stated rule).", "",
             "| Policy | Mean Δ hit systems | Median | Range | +/0/− splits |", "| --- | ---: | ---: | ---: | ---: |"]
    for policy in POLICIES:
        p = primary["policies"][policy]
        lines.append(f"| {policy} | {p['mean']:+.2f} | {p['median']:+.1f} | {p['min']:+d} to {p['max']:+d} | {p['positive']}/{p['zero']}/{p['negative']} |")
    for budget in BUDGETS:
        lines += ["", f"## K = {budget}", "",
                  "| Design | Policy | Method | Hits | Hit systems | Relevant systems | System recall | Random exp. hit systems | Effective hit systems | Largest hit share | Selected systems | Tie-crossing splits |",
                  "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
        for design in DESIGNS:
            for policy in POLICIES:
                for method in METHODS:
                    r = lookup[design, policy, method, budget]
                    lines.append(f"| {design} | {policy} | {method} | {r['hits_mean']:.2f} | {r['hit_system_count_mean']:.2f} | "
                                 f"{r['relevant_system_count_mean']:.2f} | {100*r['system_recall_mean']:.2f}% | {r['random_expected_hit_systems_mean']:.2f} | "
                                 f"{r['effective_hit_systems_mean']:.2f} | {100*r['largest_hit_system_fraction_mean']:.1f}% | "
                                 f"{r['selected_system_count_mean']:.2f} | {r['cutoff_tie_crossing_splits']} |")
        lines += ["", "Paired within-split differences versus popularity (mean; +/0/− splits):", "",
                  "| Design | Policy | Contrast | Δ hits | Δ hit systems | Δ effective hit systems |", "| --- | --- | --- | ---: | ---: | ---: |"]
        for design in DESIGNS:
            for policy in POLICIES:
                for method in ("random", "similarity", "element_pair"):
                    c = f"{method}-{REFERENCE}"
                    cells = [diff[design, policy, c, budget, f] for f in ("hits", "hit_system_count", "effective_hit_systems")]
                    lines.append(f"| {design} | {policy} | {c} | " + " | ".join(
                        f"{d['mean']:+.2f} ({d['positive']}/{d['zero']}/{d['negative']})" for d in cells) + " |")
    lines += ["", "## Validation", "", "```json", json.dumps(validation, indent=2, sort_keys=True), "```", ""]
    return "\n".join(lines)


def manifest(output):
    files = {p.relative_to(output).as_posix(): sha(p) for p in sorted(output.rglob("*")) if p.is_file() and p.name != "SHA256SUMS.json"}
    (output/"SHA256SUMS.json").write_text(json.dumps(dict(schema_version=1, files=files), indent=2, sort_keys=True)+"\n")


def analyze(v2_run, pair_run, output, julia_path, prior_analysis, spec):
    require(not output.exists(), "refusing to overwrite matched system analysis")
    v2, pair = Inventory(v2_run, V2_CONFIG_SHA), Inventory(pair_run, PAIR_CONFIG_SHA)
    require(pair.config["baseline_config_sha256"] == V2_CONFIG_SHA, "pair run does not bind the v2 baseline")
    for inventory in (v2, pair):
        require(tuple(inventory.config["budgets"]) == BUDGETS and tuple(inventory.config["split_seeds"]) == SEEDS, "unexpected grid")
    saved = saved_metrics(v2, pair)
    detail = []
    for design in DESIGNS:
        for policy in POLICIES:
            for seed in SEEDS:
                candidates, labels, heldout = load_membership(v2, pair, design, policy, seed)
                for method in METHODS:
                    formulas, scores = load_ranking(v2, pair, design, policy, seed, method, candidates, labels)
                    detail.extend(ranking_rows(design, policy, seed, method, formulas, scores, heldout))
    expected = len(DESIGNS)*len(POLICIES)*len(SEEDS)*len(METHODS)*len(BUDGETS)
    require(len(detail) == expected == len(saved), f"expected {expected} rows, saved {len(saved)}, computed {len(detail)}")
    for r in detail:
        key = (r["design"], r["policy"], r["split_seed"], r["method"], r["budget"])
        require(saved[key] == (r["hits"], r["candidate_count"], r["relevant_count"]), f"saved metric mismatch: {key}")
    summary, differences = summarize(detail), paired_differences(detail)
    primary = primary_contrast(differences)
    validation = dict(status="passed", analysis_mode="posthoc_matched_system_metrics", rows=len(detail),
                      saved_metric_rows_matched=len(saved), v2_config_sha256=V2_CONFIG_SHA, pair_config_sha256=PAIR_CONFIG_SHA,
                      input_files_hash_checked=v2.files_read + pair.files_read,
                      specification=spec.as_posix(), specification_sha256=sha(spec),
                      julia_crosscheck=dict(compare_julia(detail, julia_path), file_sha256=sha(julia_path),
                                            kernel_sources={f"src/{name}": sha(REPOSITORY/"src"/name) for name in KERNEL_SOURCES}),
                      prior_pair_concentration=compare_prior_concentration(detail, prior_analysis))
    output.mkdir()
    write_rows(output/"system-metrics-by-split.tsv", detail)
    write_rows(output/"system-metrics-summary.tsv", summary)
    write_rows(output/"paired-differences.tsv", differences)
    write_rows(output/"tie-sensitivity.tsv", tie_sensitivity(detail))
    shutil.copyfile(julia_path, output/"julia-system-metrics-by-split.tsv")
    (output/"primary-contrast.json").write_text(json.dumps(primary, indent=2, sort_keys=True)+"\n")
    (output/"validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True)+"\n")
    (output/"report.md").write_text(report(summary, differences, primary, validation))
    manifest(output)
    return dict(primary=primary, validation=validation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("v2_results", type=Path)
    parser.add_argument("pair_results", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--julia", type=Path, required=True, help="TSV written by scripts/matched_system_metrics.jl")
    parser.add_argument("--prior-concentration", type=Path, required=True, help="v0.1.1 diagnostics analysis directory")
    parser.add_argument("--spec", type=Path, default=Path("docs/paper-planning/09-e0-system-metrics-spec.md"))
    args = parser.parse_args()
    print(json.dumps(analyze(args.v2_results, args.pair_results, args.output, args.julia, args.prior_concentration, args.spec),
                     indent=2, sort_keys=True))

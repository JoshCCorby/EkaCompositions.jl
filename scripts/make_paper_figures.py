#!/usr/bin/env python3
"""Paper tables T1/T2 and figures F1, F2, S1, F3 from retained, hash-checked results.

Aggregate-only outputs for the evaluation paper (planning tasks E2, E3, E4, F2, F3).
Every input is checked against its bundle inventory, and every plotted quantity is
checked against the independently produced analysis tables before drawing. Nothing
is refit, re-ranked or relabelled. Needs matplotlib (for example `.venv-mp`).
"""
import argparse
import csv
import hashlib
import json
import tomllib
from collections import Counter
from pathlib import Path
from statistics import mean, median

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

LOCAL = Path("reports/local")
V2 = LOCAL/"mp-system-holdout-v2-2026-08-31"
PAIR = LOCAL/"element-pair-evaluation-2026-08-31"
LABEL = LOCAL/"mp-label-sensitivity-v1-2026-08-31"
DIAG = LOCAL/"element-pair-diagnostics-stability-2026-09-07"
E1 = LOCAL/"matched-system-metrics-2026-09-22"

DESIGNS = ("composition", "system")
POLICIES = ("original", "exclude_mixed", "unlabel_mixed")
POLICY_LABEL = {"original": "Original", "exclude_mixed": "Exclude mixed", "unlabel_mixed": "Unlabel mixed"}
DESIGN_LABEL = {"composition": "Composition holdout", "system": "System holdout"}
METHODS = ("random", "popularity", "similarity", "element_pair")
METHOD_LABEL = {"random": "Random", "popularity": "Popularity", "similarity": "Max similarity", "element_pair": "Pair model"}
BUDGETS = (20, 50, 100, 200)
SEEDS = tuple(range(20))
TOL = 1e-9

# Validated with the dataviz skill's validate_palette.js (light, all pairs): the three
# categorical slots pass; aqua is below 3:1 contrast, so every chart carries a legend
# and marker shapes as secondary encoding. Random is a neutral reference, not a series.
INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
COLOR = {"random": MUTED, "popularity": "#2a78d6", "similarity": "#eb6834", "element_pair": "#1baf7a"}
MARKER = {"random": "o", "popularity": "s", "similarity": "^", "element_pair": "D"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


class Checked:
    """Reads files only after matching them to the bundle's own hash inventory."""

    def __init__(self):
        self.read = {}

    def file(self, path, expected):
        digest = sha(path)
        require(digest == expected, f"hash mismatch: {path}")
        self.read[path.as_posix()] = digest
        return path

    def from_config(self, results, name):
        inventory = tomllib.loads((results/"config.toml").read_text())["deterministic_file_hashes"]
        return rows(self.file(results/name, inventory[name]))

    def from_sums(self, bundle, name, sums="SHA256SUMS.json"):
        inventory = json.loads((bundle/sums).read_text())
        return self.file(bundle/name, inventory.get("files", inventory)[name])


def style():
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
        "legend.fontsize": 7, "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
        "axes.edgecolor": AXIS, "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "xtick.major.size": 2.5, "ytick.major.size": 2.5, "axes.grid": True, "grid.color": GRID,
        "grid.linewidth": 0.5, "grid.linestyle": "-", "axes.axisbelow": True, "axes.spines.top": False,
        "axes.spines.right": False, "figure.dpi": 150, "savefig.dpi": 300, "pdf.fonttype": 42,
        "axes.titlelocation": "left", "axes.titleweight": "bold", "legend.frameon": False,
    })


def save(fig, output, stem):
    fig.savefig(output/f"{stem}.pdf", metadata={"CreationDate": None, "ModDate": None, "Producer": None, "Creator": None})
    fig.savefig(output/f"{stem}.png", metadata={"Software": None})
    plt.close(fig)


def write_tsv(path, data):
    with path.open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(data[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)


def spread(values):
    if min(values) == max(values):
        return f"{min(values):,.0f}"
    return f"{mean(values):,.2f} [{min(values):,.0f}–{max(values):,.0f}]"


def signs(values):
    return f"{sum(v > 0 for v in values)}/{sum(v == 0 for v in values)}/{sum(v < 0 for v in values)}"


def zero_line(ax):
    ax.axhline(0, color=AXIS, linewidth=0.9, zorder=1)


# ---------------------------------------------------------------- data

def load(check):
    metrics = {}
    for results in (V2/"results", PAIR/"results"):
        for r in check.from_config(results, "metrics.tsv"):
            key = (r["design"], r["policy"], int(r["split_seed"]), r["method"], int(r["budget"]))
            require(key not in metrics, f"duplicate metric row {key}")
            metrics[key] = r
    require(len(metrics) == 1920, "expected 1,920 metric rows")
    audit = check.from_config(V2/"results", "source/audit/compositions.tsv")
    populations = rows(check.from_sums(V2, "analysis/populations.tsv"))
    v2_summary = rows(check.from_sums(V2, "analysis/summary.tsv"))
    v2_methods = rows(check.from_sums(V2, "analysis/method-summary.tsv"))
    pair_summary = rows(check.from_sums(PAIR, "analysis/summary.tsv"))
    pair_methods = rows(check.from_sums(PAIR, "analysis/method-summary.tsv"))
    label_summary = rows(check.from_sums(LABEL, "analysis/summary.tsv"))
    diag = DIAG/"analysis"
    stability = rows(check.from_sums(diag, "stability-by-fit.tsv"))
    stability_summary = json.loads(check.from_sums(diag, "stability-summary.json").read_text())
    subgroup = rows(check.from_sums(diag, "subgroup-summary.tsv"))
    e1 = rows(check.from_sums(E1, "system-metrics-by-split.tsv"))
    e1_summary = rows(check.from_sums(E1, "system-metrics-summary.tsv"))
    return dict(metrics=metrics, audit=audit, populations=populations, v2_summary=v2_summary, v2_methods=v2_methods,
                pair_summary=pair_summary, pair_methods=pair_methods, label_summary=label_summary,
                stability=stability, stability_summary=stability_summary, subgroup=subgroup, e1=e1, e1_summary=e1_summary)


def hits(d, design, policy, seed, method, budget=100):
    return int(d["metrics"][design, policy, seed, method, budget]["hits"])


def difference(d, design, policy, method, budget=100):
    return [hits(d, design, policy, s, method, budget) - hits(d, design, policy, s, "popularity", budget) for s in SEEDS]


def cross_check_differences(d):
    """Paired differences must reproduce both bundles' own analysis summaries."""
    v2 = {(r["design"], r["policy"], int(r["budget"])): r for r in d["v2_summary"]}
    pair = {(r["design"], r["policy"], int(r["budget"])): r for r in d["pair_summary"]}
    for design in DESIGNS:
        for policy in POLICIES:
            for budget in BUDGETS:
                sim = difference(d, design, policy, "similarity", budget)
                pm = difference(d, design, policy, "element_pair", budget)
                s, p = v2[design, policy, budget], pair[design, policy, budget]
                require(abs(mean(sim) - float(s["difference_mean"])) < TOL and signs(sim) == f"{s['positive']}/{s['zero']}/{s['negative']}",
                        f"similarity difference mismatch {design} {policy} {budget}")
                require(abs(mean(pm) - float(p["mean_difference"])) < TOL and signs(pm) == f"{p['positive']}/{p['zero']}/{p['negative']}",
                        f"pair difference mismatch {design} {policy} {budget}")
    for table in (d["v2_methods"], d["pair_methods"]):
        for r in table:
            values = [hits(d, r["design"], r["policy"], s, r["method"], int(r["budget"])) for s in SEEDS]
            require(abs(mean(values) - float(r["hits_mean"])) < TOL, f"method mean mismatch {r['design']} {r['policy']} {r['method']}")


# ---------------------------------------------------------------- tables

def population_counts(audit):
    positives = [r for r in audit if r["label"] == "positive"]
    mixed = [r for r in positives if int(r["theoretical_records"]) > 0]
    unlabelled = [r for r in audit if r["label"] == "unlabelled"]
    counts = dict(groups=len(audit), positive=len(positives), unlabelled=len(unlabelled), mixed=len(mixed),
                  systems=len({r["chemical_system"] for r in audit}))
    require(counts == dict(groups=12506, positive=5359, unlabelled=7147, mixed=1343, systems=2630), f"audit counts changed: {counts}")
    eligible = {"original": (counts["positive"], counts["unlabelled"]),
                "exclude_mixed": (counts["positive"] - counts["mixed"], counts["unlabelled"]),
                "unlabel_mixed": (counts["positive"] - counts["mixed"], counts["unlabelled"] + counts["mixed"])}
    return counts, eligible


def table_t1(d, output):
    counts, eligible = population_counts(d["audit"])
    handling = {"original": "positive if any record is experimental",
                "exclude_mixed": f"{counts['mixed']:,} mixed groups removed",
                "unlabel_mixed": f"{counts['mixed']:,} mixed groups unlabelled"}
    data = []
    for design in DESIGNS:
        for policy in POLICIES:
            rs = [r for r in d["populations"] if (r["design"], r["policy"]) == (design, policy)]
            require(sorted(int(r["split_seed"]) for r in rs) == list(SEEDS), "population seeds incomplete")
            get = lambda field: [float(r[field]) for r in rs]
            n, h = get("candidate_count"), get("heldout_count")
            prevalence = [a/b for a, b in zip(h, n)]
            require(all(abs(a - float(r["prevalence"])) < TOL for a, r in zip(prevalence, rs)), "prevalence mismatch")
            if design == "composition":
                require(all(t + x == eligible[policy][0] for t, x in zip(get("training_count"), h)), "composition P mismatch")
            data.append(dict(
                design=design, policy=policy, eligible_positive=eligible[policy][0], eligible_unlabelled=eligible[policy][1],
                mixed_handling=handling[policy], training=spread(get("training_count")), candidates_N=spread(n),
                heldout_h=spread(h), heldout_systems=spread(get("heldout_system_count")),
                selected_systems=f"{int(get('selected_system_count')[0])} of {int(get('universe_system_count')[0])}" if design == "system" else "—",
                prevalence_mean_of_ratios=f"{mean(prevalence):.4f}", prevalence_ratio_of_means=f"{mean(h)/mean(n):.4f}",
                random_expected_hits100=f"{mean(100*a/b for a, b in zip(h, n)):.2f}"))
    write_tsv(output/"t1-populations.tsv", data)
    lines = ["| Design | Policy | Eligible P / U | Mixed-group handling | Training positives | Candidates N | Held-out positives h | Held-out systems | Selected systems | Prevalence h/N (mean of splits) | Random expected Hits@100 |",
             "| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in data:
        lines.append(f"| {DESIGN_LABEL[r['design']]} | {POLICY_LABEL[r['policy']]} | {r['eligible_positive']:,} / {r['eligible_unlabelled']:,} | {r['mixed_handling']} | "
                     f"{r['training']} | {r['candidates_N']} | {r['heldout_h']} | {r['heldout_systems']} | {r['selected_systems']} | {r['prevalence_mean_of_ratios']} | {r['random_expected_hits100']} |")
    lines += ["", f"Source population: {counts['groups']:,} canonical compositions ({counts['positive']:,} positive, {counts['unlabelled']:,} unlabelled, "
              f"{counts['mixed']:,} mixed positives) in {counts['systems']:,} chemical systems. Cells are mean [min–max] over 20 splits; composition-holdout counts are constant.",
              "Prevalence is the mean of per-split h/N; the ratio of means is in the TSV and differs slightly for system holdout.", ""]
    (output/"t1-populations.md").write_text("\n".join(lines))
    return data


def table_t2(d, output):
    data = []
    for design in DESIGNS:
        for policy in POLICIES:
            row = dict(design=design, policy=policy)
            ms = [d["metrics"][design, policy, s, "random", 100] for s in SEEDS]
            row["random_expected"] = mean(float(r["random_expected_hits"]) for r in ms)
            for method in METHODS:
                row[f"{method}_hits100"] = mean(hits(d, design, policy, s, method) for s in SEEDS)
            sim, pm = difference(d, design, policy, "similarity"), difference(d, design, policy, "element_pair")
            row.update(similarity_minus_popularity=mean(sim), similarity_signs=signs(sim),
                       pair_minus_popularity=mean(pm), pair_signs=signs(pm),
                       pair_enrichment_mean=mean(float(d["metrics"][design, policy, s, "element_pair", 100]["observed_label_enrichment"]) for s in SEEDS))
            data.append(row)
    write_tsv(output/"t2-main-outcomes.tsv", data)
    lines = ["| Design | Policy | Random expected | Random | Popularity | Max similarity | Pair model | Similarity − popularity (+/0/−) | Pair − popularity (+/0/−) | Pair mean enrichment |",
             "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in data:
        lines.append(f"| {DESIGN_LABEL[r['design']]} | {POLICY_LABEL[r['policy']]} | {r['random_expected']:.2f} | {r['random_hits100']:.2f} | {r['popularity_hits100']:.2f} | "
                     f"{r['similarity_hits100']:.2f} | {r['element_pair_hits100']:.2f} | {r['similarity_minus_popularity']:+.2f} ({r['similarity_signs']}) | "
                     f"{r['pair_minus_popularity']:+.2f} ({r['pair_signs']}) | {r['pair_enrichment_mean']:.3f} |")
    lines += ["", "Hits@100 means over 20 overlapping splits on identical within-branch pools. Enrichment is the mean of per-split values.", ""]
    (output/"t2-main-outcomes.md").write_text("\n".join(lines))
    return data


def table_label_modes(d, output):
    data = [r for r in d["label_summary"] if int(r["budget"]) in BUDGETS]
    require(len(data) == 2*len(POLICIES)*len(BUDGETS), "label-mode summary incomplete")
    lines = ["| Mode | Policy | K=20 | K=50 | K=100 | K=200 |", "| --- | --- | ---: | ---: | ---: | ---: |"]
    for mode in ("evaluation_only", "full_pipeline"):
        for policy in POLICIES:
            cells = []
            for budget in BUDGETS:
                (r,) = [x for x in data if (x["mode"], x["policy"], int(x["budget"])) == (mode, policy, budget)]
                cells.append(f"{float(r['difference_mean']):+.2f} ({r['positive']}/{r['zero']}/{r['negative']})")
            lines.append(f"| {mode.replace('_', '-')} | {POLICY_LABEL[policy]} | " + " | ".join(cells) + " |")
    lines += ["", "Composition holdout, similarity − popularity Hits@K, mean (+/0/− splits). Evaluation-only relabels fixed original-policy rankings; full-pipeline rebuilds training, candidates and labels.", ""]
    (output/"s1-label-modes.md").write_text("\n".join(lines))


# ---------------------------------------------------------------- figures

def figure_f1(d, output):
    fig, axes = plt.subplots(2, 3, figsize=(7.0, 4.6), sharey="row")
    t1 = {(r["design"], r["policy"]): (mean(float(x["candidate_count"]) for x in d["populations"] if (x["design"], x["policy"]) == (r["design"], r["policy"])),
                                       mean(float(x["heldout_count"]) for x in d["populations"] if (x["design"], x["policy"]) == (r["design"], r["policy"])))
          for r in d["t1"]}
    plotted = []
    for i, design in enumerate(DESIGNS):
        for j, policy in enumerate(POLICIES):
            ax = axes[i, j]
            zero_line(ax)
            for x, method in enumerate(("similarity", "element_pair")):
                values = difference(d, design, policy, method)
                offsets = [(-0.18 + 0.36*k/19) for k in range(20)]
                ax.scatter([x + o for o in offsets], values, s=14, marker=MARKER[method], color=COLOR[method],
                           edgecolors="white", linewidths=0.5, zorder=3)
                ax.hlines(median(values), x - 0.28, x + 0.28, color=INK, linewidth=1.0, zorder=4)
                ax.scatter([x + 0.34], [mean(values)], s=22, marker="D", facecolors="white", edgecolors=INK, linewidths=0.9, zorder=4)
                plotted += [dict(design=design, policy=policy, contrast=f"{method}-popularity", split_seed=s, difference=v) for s, v in zip(SEEDS, values)]
            n, h = t1[design, policy]
            ax.set_title(f"{DESIGN_LABEL[design]} · {POLICY_LABEL[policy]}", fontsize=7.5, pad=12)
            ax.text(0.0, 1.015, f"mean N = {n:,.0f}, h = {h:,.0f}", transform=ax.transAxes, fontsize=6.5, color=MUTED, va="bottom", ha="left")
            ax.set_xticks([0, 1], ["Similarity\n− popularity", "Pair model\n− popularity"])
            ax.set_xlim(-0.5, 1.6)
            ax.grid(axis="x", visible=False)
        axes[i, 0].set_ylabel("Δ Hits@100 vs popularity\n(within split)")
    require(len(plotted) == 240, "F1 must plot 240 paired differences")
    handles = [Line2D([], [], marker=MARKER[m], color=COLOR[m], linestyle="", markersize=4.5, label=f"{METHOD_LABEL[m]} − popularity (one split)") for m in ("similarity", "element_pair")]
    handles += [Line2D([], [], color=INK, linewidth=1.0, label="Median"),
                Line2D([], [], marker="D", markerfacecolor="white", markeredgecolor=INK, linestyle="", markersize=4.5, label="Mean")]
    fig.legend(handles=handles, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, output, "f1-paired-differences")
    write_tsv(output/"f1-data.tsv", plotted)


def figure_f2(d, output):
    e1 = [r for r in d["e1"] if r["budget"] == "100"]
    expected = {(r["design"], r["policy"]): float(r["random_expected_hit_systems_mean"]) for r in d["e1_summary"]
                if r["budget"] == "100" and r["method"] == "random"}
    fig, axes = plt.subplots(2, 3, figsize=(7.0, 4.8), sharey="row", sharex="row")
    for i, design in enumerate(("system", "composition")):
        for j, policy in enumerate(POLICIES):
            ax = axes[i, j]
            for method in METHODS:
                rs = [r for r in e1 if (r["design"], r["policy"], r["method"]) == (design, policy, method)]
                require(len(rs) == 20, "F2 facet incomplete")
                ax.scatter([int(r["hits"]) for r in rs], [int(r["hit_system_count"]) for r in rs], s=13, marker=MARKER[method],
                           color=COLOR[method], edgecolors="white", linewidths=0.5, zorder=3, alpha=0.95)
            ax.axhline(expected[design, policy], color=MUTED, linewidth=0.8, zorder=2)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_title(f"{DESIGN_LABEL[design]} · {POLICY_LABEL[policy]}", fontsize=7.5)
            ax.set_xlabel("Hits@100 (observed positives)")
        axes[i, 0].set_ylabel("Positive systems hit\nin top 100")
    handles = [Line2D([], [], marker=MARKER[m], color=COLOR[m], linestyle="", markersize=4.5, label=METHOD_LABEL[m]) for m in METHODS]
    handles.append(Line2D([], [], color=MUTED, linewidth=0.8, label="Exact random expectation (mean)"))
    fig.legend(handles=handles, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, output, "f2-system-coverage")


def figure_s1(d, output):
    fig, axes = plt.subplots(2, 3, figsize=(7.0, 4.6), sharey="row")
    plotted = []
    for i, design in enumerate(DESIGNS):
        for j, policy in enumerate(POLICIES):
            ax = axes[i, j]
            zero_line(ax)
            for k, method in enumerate(("similarity", "element_pair")):
                xs = [b + (-0.12 if k == 0 else 0.12) for b in range(len(BUDGETS))]
                series = [difference(d, design, policy, method, budget) for budget in BUDGETS]
                ax.vlines(xs, [min(v) for v in series], [max(v) for v in series], color=COLOR[method], linewidth=0.8, alpha=0.6, zorder=2)
                ax.plot(xs, [mean(v) for v in series], color=COLOR[method], linewidth=1.2, marker=MARKER[method], markersize=4,
                        markeredgecolor="white", markeredgewidth=0.5, zorder=3)
                plotted += [dict(design=design, policy=policy, contrast=f"{method}-popularity", budget=b, mean=mean(v), min=min(v), max=max(v), signs=signs(v))
                            for b, v in zip(BUDGETS, series)]
            ax.set_xticks(range(len(BUDGETS)), [str(b) for b in BUDGETS])
            ax.set_title(f"{DESIGN_LABEL[design]} · {POLICY_LABEL[policy]}", fontsize=7.5)
            ax.set_xlabel("Budget K")
            ax.grid(axis="x", visible=False)
        axes[i, 0].set_ylabel("Δ Hits@K vs popularity\n(mean; bar = split range)")
    handles = [Line2D([], [], marker=MARKER[m], color=COLOR[m], markersize=4, linewidth=1.2, label=f"{METHOD_LABEL[m]} − popularity") for m in ("similarity", "element_pair")]
    fig.legend(handles=handles, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, output, "s1-all-budgets")
    write_tsv(output/"s1-data.tsv", plotted)
    return plotted


def figure_f3(d, output):
    fits = d["stability"]
    require(len(fits) == 120, "F3 must account for all 120 fits")
    summary = d["stability_summary"]
    capped = [r for r in fits if r["primary_termination"] == "iteration_limit"]
    converged = [r for r in fits if r["primary_termination"] == "projected_gradient"]
    require(len(capped) == summary["previously_capped_fits"] and len(converged) == summary["previously_converged_fits"], "F3 status counts differ")
    require(sum(r["top100_changed"] == "True" for r in capped) == summary["previously_capped_top100_changed"], "F3 changed count differs")
    require(max(int(r["top100_replacements"]) for r in fits) == summary["top100_replacements_max"], "F3 max replacements differs")
    require(not any(r["top100_changed"] == "True" for r in converged), "a converged fit changed")
    fig, axes = plt.subplots(2, 3, figsize=(7.0, 4.4), sharex=True, sharey=True)
    accounted = 0
    for i, design in enumerate(DESIGNS):
        for j, policy in enumerate(POLICIES):
            ax = axes[i, j]
            zero_line(ax)
            rs = [r for r in fits if (r["design"], r["policy"]) == (design, policy)]
            changed = Counter((int(r["top100_replacements"]), int(r["hit_delta"])) for r in rs if r["top100_changed"] == "True")
            for (x, y), n in changed.items():
                ax.scatter([x], [y], s=16, marker="o", color=COLOR["element_pair"], edgecolors="white", linewidths=0.5, zorder=3)
                if n > 1:
                    ax.annotate(f"×{n}", (x, y), xytext=(3, 3), textcoords="offset points", fontsize=5.5, color=INK2)
            same = [r for r in rs if r["top100_changed"] == "False"]
            n_conv = sum(r["primary_termination"] == "projected_gradient" for r in same)
            ax.text(0.98, 0.96, f"Top 100 unchanged: {len(same)} fits\n({n_conv} converged, {len(same) - n_conv} capped)",
                    transform=ax.transAxes, ha="right", va="top", fontsize=6.2, color=INK2)
            accounted += sum(changed.values()) + len(same)
            ax.set_title(f"{DESIGN_LABEL[design]} · {POLICY_LABEL[policy]}", fontsize=7.5)
        axes[i, 0].set_ylabel("Δ Hits@100 (20k − 2k iterations)")
    require(accounted == 120, "F3 does not account for all 120 fits")
    for ax in axes[1]:
        ax.set_xlabel("Top-100 replacements")
    handles = [Line2D([], [], marker="o", color=COLOR["element_pair"], markeredgecolor="white", linestyle="", markersize=4.5,
                      label="Fit whose top 100 changed (all had stopped at the 2,000-iteration cap)")]
    fig.legend(handles=handles, loc="lower center", ncol=1, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, output, "f3-optimization-stability")


def captions(d, output):
    s = d["stability_summary"]
    (output/"captions.md").write_text(f"""# Draft captions (check every number against the TSVs before submission)

Attribution for every figure and table: derived from Materials Project data (database version 2026.04.13, retrieved 31 August 2026; CC BY 4.0).
Records were grouped by canonical composition and labelled by the stated provenance policy; only aggregate counts are shown.
Confirm the exact notice against docs/publication-permissions.md.

**Table 1.** Population definitions for one Materials Project snapshot of oxygen-containing ternaries. Cells are mean [min–max] over 20 overlapping holdouts. Random expectations use each split's actual h/N.

**Table 2.** Primary top-100 recovery on identical within-branch candidate pools. Entries are means across 20 overlapping holdouts; sign counts refer to paired differences from popularity. Scores and metrics measure withheld provenance labels, not synthesis.

**Figure 1.** Within-split differences in observed-positive Hits@100 relative to training-element popularity, for two holdout procedures and three provenance-label policies. Dots are the 20 predeclared, overlapping holdouts; the bar marks the median and the open diamond the mean. Comparisons within a panel share candidates and labels; different holdout designs do not, and their y-scales differ. Spread is descriptive split sensitivity, not a confidence interval.

**Figure 2 (post hoc).** Composition hits versus positive chemical systems reached in the top 100, for all four methods on identical pools. Each point is one split. The grey line is the exact expectation of positive systems hit by a uniform random top 100. Systems are unordered element sets, not measures of chemical diversity. Methods leading on composition hits in system holdout reach the fewest positive systems. This mirrors "first found" chemotype accounting in virtual screening (Mackey & Melville 2009).

**Figure 3 (post hoc).** Sensitivity to raising only the iteration cap from 2,000 to 20,000. Points are the fits whose top 100 changed (×n marks repeated points); each panel states how many fits were unchanged, so all 120 are accounted for. Of {s['previously_capped_fits']} previously capped fits, {s['previously_capped_top100_changed']} top-100 sets changed, with up to {s['top100_replacements_max']} replacements; none of the {s['previously_converged_fits']} previously converged sets changed. Hit changes averaged {s['hit_delta_mean']:+.2f} (range {s['hit_delta_min']:+d} to {s['hit_delta_max']:+d}). All longer-run fits reached the projected-gradient criterion. The 2,000-iteration evaluations remain primary; stationarity does not imply a global optimum. Alternative-policy fits share training within each design and split, so they are not independent.

**Figure S1.** Paired differences from popularity at every frozen budget. Lines join means across the same 20 overlapping splits; vertical bars show the split range. Budget dependence is part of the result: no K defines a universal ordering.

**Table S1.** Label-sensitivity modes (composition holdout, similarity − popularity). Evaluation-only relabelling keeps original training information and is not a newly trained alternative-policy experiment.
""")


def manifest(output, check):
    files = {p.name: sha(p) for p in sorted(output.iterdir()) if p.name != "SHA256SUMS.json"}
    (output/"SHA256SUMS.json").write_text(json.dumps(dict(schema_version=1, inputs=check.read, files=files), indent=2, sort_keys=True) + "\n")


def main(output):
    require(not output.exists(), f"refusing to overwrite {output}")
    check = Checked()
    d = load(check)
    cross_check_differences(d)
    style()
    output.mkdir(parents=True)
    d["t1"] = table_t1(d, output)
    table_t2(d, output)
    table_label_modes(d, output)
    figure_f1(d, output)
    figure_f2(d, output)
    figure_s1(d, output)
    figure_f3(d, output)
    captions(d, output)
    manifest(output, check)
    print(f"Wrote tables, figures and captions to {output}; {len(check.read)} inputs hash-checked")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, nargs="?", default=LOCAL/"paper-figures-2026-09-22")
    main(parser.parse_args().output)

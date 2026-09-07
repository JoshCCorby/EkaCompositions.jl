#!/usr/bin/env python3
"""Reproduce subgroup, system-concentration and 20k-fit stability diagnostics."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean

from analyze_pu_pilot import require,rows,sha,write_rows
from analyze_system_holdout import system,POLICIES
import analyze_element_pair as primary_analysis

STABILITY_SETTINGS=dict(primary_analysis.SETTINGS,max_iterations=20000)


def ranking(run,design,policy,seed):
    return rows(run/design/policy/f'split-{seed:02}'/'ranking.tsv')


def memberships(run,design,policy,seed):
    base=run/'baseline'/design/policy/f'split-{seed:02}'
    training={r['composition'] for r in rows(base/'inputs/training.tsv')}
    candidates={r['composition'] for r in rows(base/'inputs/candidates.tsv')}
    heldout={r['composition'] for r in rows(base/'evaluation/heldout.tsv')}
    return training,candidates,heldout


def subgroup_rows(run,seeds):
    detail=[]
    for policy in POLICIES:
        for seed in seeds:
            training,candidates,heldout=memberships(run,'composition',policy,seed)
            training_systems={system(f) for f in training}
            novel={f for f in heldout if system(f) not in training_systems}
            top={r['composition'] for r in ranking(run,'composition',policy,seed)[:100]}
            detail.append(dict(policy=policy,split_seed=seed,heldout_count=len(heldout),
                system_disjoint_count=len(novel),system_disjoint_fraction=len(novel)/len(heldout),
                top100_system_disjoint_hits=len(top&novel),
                random_expected_top100_system_disjoint_hits=100*len(novel)/len(candidates)))
    summary=[]
    for policy in POLICIES:
        rs=[r for r in detail if r['policy']==policy]
        summary.append(dict(policy=policy,splits=len(rs),heldout_total=sum(r['heldout_count'] for r in rs),
            system_disjoint_total=sum(r['system_disjoint_count'] for r in rs),
            system_disjoint_fraction=sum(r['system_disjoint_count'] for r in rs)/sum(r['heldout_count'] for r in rs),
            top100_system_disjoint_hits=sum(r['top100_system_disjoint_hits'] for r in rs),
            random_expected_top100_system_disjoint_hits=sum(r['random_expected_top100_system_disjoint_hits'] for r in rs)))
    return detail,summary


def concentration_rows(run,seeds):
    detail=[]
    for policy in POLICIES:
        for seed in seeds:
            top=ranking(run,'system',policy,seed)[:100]
            all_systems=Counter(system(r['composition']) for r in top)
            hit_systems=Counter(system(r['composition']) for r in top if r['observed_label']=='positive')
            hits=sum(hit_systems.values())
            effective=hits*hits/sum(n*n for n in hit_systems.values()) if hits else 0.0
            detail.append(dict(policy=policy,split_seed=seed,top100_hits=hits,
                distinct_systems=len(all_systems),positive_hit_systems=len(hit_systems),
                effective_hit_systems=effective,
                largest_hit_system_fraction=max(hit_systems.values())/hits if hits else 0.0,
                largest_system_rows=max(all_systems.values())))
    summary=[]
    for policy in POLICIES:
        rs=[r for r in detail if r['policy']==policy]
        summary.append(dict(policy=policy,splits=len(rs),
            **{f'{field}_mean':mean(r[field] for r in rs) for field in
               ('top100_hits','distinct_systems','positive_hit_systems','effective_hit_systems','largest_hit_system_fraction','largest_system_rows')},
            largest_system_rows_max=max(r['largest_system_rows'] for r in rs)))
    return detail,summary


def stability_rows(primary,stability,seeds):
    before_diagnostics={(r['design'],r['policy'],int(r['split_seed'])):r for r in rows(primary/'fit-diagnostics.tsv')}
    after_diagnostics={(r['design'],r['policy'],int(r['split_seed'])):r for r in rows(stability/'fit-diagnostics.tsv')}
    detail=[]
    for design in ('composition','system'):
        for policy in POLICIES:
            for seed in seeds:
                before=ranking(primary,design,policy,seed);after=ranking(stability,design,policy,seed)
                require({r['composition'] for r in before}=={r['composition'] for r in after},'stability candidate membership mismatch')
                btop={r['composition'] for r in before[:100]};atop={r['composition'] for r in after[:100]}
                bhits=sum(r['observed_label']=='positive' for r in before[:100]);ahits=sum(r['observed_label']=='positive' for r in after[:100])
                bdiag=before_diagnostics[design,policy,seed];adiag=after_diagnostics[design,policy,seed]
                detail.append(dict(design=design,policy=policy,split_seed=seed,
                    primary_termination=bdiag['termination'],primary_iterations=int(bdiag['iterations']),
                    stability_termination=adiag['termination'],stability_iterations=int(adiag['iterations']),
                    top100_changed=btop!=atop,top100_replacements=len(btop-atop),
                    primary_hits=bhits,stability_hits=ahits,hit_delta=ahits-bhits))
    return detail


def manifest(output):
    files={p.relative_to(output).as_posix():sha(p) for p in sorted(output.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'}
    digest=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    (output/'SHA256SUMS.json').write_text(json.dumps(dict(schema_version=1,files=files,manifest_sha256=digest),indent=2,sort_keys=True)+'\n')


def analyze(primary,stability,output):
    require(not output.exists(),'refusing to overwrite stability analysis')
    pcfg,_,_,_=primary_analysis.validate(primary)
    scfg,_,_,_=primary_analysis.validate(stability,STABILITY_SETTINGS,'posthoc_stability_20000')
    require(not pcfg['is_synthetic'] == False or pcfg['split_seeds']==list(range(20)),'unexpected real primary seeds')
    require(pcfg['is_synthetic']==scfg['is_synthetic'],'primary/stability mode mismatch')
    require(pcfg['input_hashes']==scfg['input_hashes'] and pcfg['baseline_config_sha256']==scfg['baseline_config_sha256'],'primary/stability source mismatch')
    output.mkdir()
    seeds=pcfg['split_seeds']
    subdetail,subsummary=subgroup_rows(primary,seeds)
    stable_subdetail,stable_subsummary=subgroup_rows(stability,seeds)
    cdetail,csummary=concentration_rows(primary,seeds)
    stable=stability_rows(primary,stability,seeds)
    write_rows(output/'subgroup-by-split.tsv',subdetail);write_rows(output/'subgroup-summary.tsv',subsummary)
    write_rows(output/'stability-subgroup-by-split.tsv',stable_subdetail);write_rows(output/'stability-subgroup-summary.tsv',stable_subsummary)
    write_rows(output/'system-concentration-by-split.tsv',cdetail);write_rows(output/'system-concentration-summary.tsv',csummary)
    write_rows(output/'stability-by-fit.tsv',stable)
    previously_converged=[r for r in stable if r['primary_termination']=='projected_gradient']
    previously_capped=[r for r in stable if r['primary_termination']=='iteration_limit']
    summary=dict(schema_version=1,primary_config_sha256=sha(primary/'config.toml'),stability_config_sha256=sha(stability/'config.toml'),
        fits=len(stable),stability_converged=sum(r['stability_termination']=='projected_gradient' for r in stable),
        stability_iteration_max=max(r['stability_iterations'] for r in stable),
        previously_converged_fits=len(previously_converged),previously_converged_top100_changed=sum(r['top100_changed'] for r in previously_converged),
        previously_capped_fits=len(previously_capped),previously_capped_top100_changed=sum(r['top100_changed'] for r in previously_capped),
        top100_replacements_max=max(r['top100_replacements'] for r in stable),hit_delta_mean=mean(r['hit_delta'] for r in stable),
        hit_delta_min=min(r['hit_delta'] for r in stable),hit_delta_max=max(r['hit_delta'] for r in stable))
    summary['stability_system_disjoint_hits']={r['policy']:r['top100_system_disjoint_hits'] for r in stable_subsummary}
    (output/'stability-summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    lines=['# Element-pair diagnostic and stability analysis','',
        'The 2,000-iteration result remains primary. The 20,000-iteration run changes only the declared iteration cap and is post-hoc stability evidence, not model selection.','',
        '## System-disjoint composition holdout','',
        '| Policy | Disjoint share | Hits@100 across splits | Random expectation |','| --- | ---: | ---: | ---: |']
    for r in subsummary:lines.append(f"| {r['policy']} | {100*r['system_disjoint_fraction']:.2f}% | {r['top100_system_disjoint_hits']} | {r['random_expected_top100_system_disjoint_hits']:.2f} |")
    lines+=['','## System-holdout concentration','',
        '| Policy | Mean systems | Mean hit systems | Effective hit systems | Largest hit share | Max rows from one system |','| --- | ---: | ---: | ---: | ---: | ---: |']
    for r in csummary:lines.append(f"| {r['policy']} | {r['distinct_systems_mean']:.2f} | {r['positive_hit_systems_mean']:.2f} | {r['effective_hit_systems_mean']:.2f} | {100*r['largest_hit_system_fraction_mean']:.1f}% | {r['largest_system_rows_max']} |")
    lines+=['','## 20,000-iteration stability','',
        f"All {summary['fits']} fits converged by iteration {summary['stability_iteration_max']}. None of the {summary['previously_converged_fits']} previously converged top-100 sets changed; {summary['previously_capped_top100_changed']} of {summary['previously_capped_fits']} previously capped sets changed. The largest replacement count was {summary['top100_replacements_max']}; hit deltas averaged {summary['hit_delta_mean']:+.2f} and ranged from {summary['hit_delta_min']:+d} to {summary['hit_delta_max']:+d}.",
        'The converged composition-holdout system-disjoint Hits@100 totals are '+', '.join(f"{r['policy']}={r['top100_system_disjoint_hits']}" for r in stable_subsummary)+'.','']
    (output/'report.md').write_text('\n'.join(lines))
    (output/'validation.json').write_text(json.dumps(dict(status='passed',primary_synthetic=pcfg['is_synthetic'],fits=len(stable)),indent=2,sort_keys=True)+'\n')
    manifest(output)
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('primary_run',type=Path);parser.add_argument('stability_run',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();print(json.dumps(analyze(args.primary_run,args.stability_run,args.output),indent=2,sort_keys=True))

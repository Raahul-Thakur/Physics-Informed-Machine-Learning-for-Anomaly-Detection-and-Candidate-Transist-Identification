# Larger-experiment output audit

## Correction follow-up (2026-09-13)

The two implementation issues below have now been fixed and the derived outputs regenerated from the same cached observations. The original audit below is historical; its pre-fix numbers are preserved for comparison. Original outputs are retained in `experiments/default/audit_snapshots/before_boundary_order_fix_20260913_182142/`.

- All 1,353 target-sector rows from 982 targets were retained; no feature-stage failures occurred.
- Every saved BLS trial and winning period respects both configured bounds and the individual baseline cap. Exactly seven winning periods changed.
- Every all-feature refit score exactly reproduces its primary score (maximum absolute difference zero), and every all-feature ablation metric exactly matches its primary metric. Evaluation uses round-trip float parsing to preserve score ties after CSV serialization.
- Corrected top-99 recovery is BLS 44/297, Isolation Forest 21/297, LOF 22/297, ensemble 24/297, hybrid 26/297. The primary and all-feature hybrid results are now both 26, rather than the pre-fix 25 versus 26.
- The interpretation limits remain: 71/297 representative host periods are outside the configured interval, usable sector coverage differs by group, and all five top hybrid candidates are unlabelled backgrounds. No independent generalisation or workload reduction is established. The corrected hybrid still does not outperform BLS in this comparison.
- All 24 tests pass. Source, tests and scripts pass Ruff. The smaller 110-target experiment was also regenerated and passed exact score/metric and strict period-bound checks. Repository-wide Ruff additionally reports existing notebook formatting issues, outside these changes.

Machine-readable post-fix verification: `experiments/default/outputs/tables/correction_verification.json`. Updated results: `experiments/default/outputs/research_summary.md`. Reproduce the checks using `python scripts/verify_output_corrections.py --config config/default.yaml`.

## Original pre-fix audit

Audited 2026-09-13 against `docs/abstract.md`, the saved configuration and artifacts in `experiments/default/`. This audit inspected existing results and refitted models in memory for verification. It did not change the scientific outputs, model settings or primary rankings. Machine-readable checks are in `output_audit.json`.

## Verdict

The outputs support the revised abstract's **descriptive, unsupervised candidate-ranking framework**. They do not establish improved planet recovery, reduced inspection workload or independent generalisation. The main ranking results are numerically reproducible. Two implementation inconsistencies should be corrected before treating all tables as final paper results: ablation fitting order and strict BLS upper-period enforcement.

## Verified data and model integrity

The configuration requests 300 planet/candidate hosts, 300 false positives and 500 backgrounds. The eligible catalogue/observing pool contained only 196 false positives; this shortage was explicitly logged. Consequently the actual selected sample contains 996 targets, not 1,100.

| Population | Selected | Analysed unique targets |
|---|---:|---:|
| Planet/candidate | 300 | 297 |
| False positive | 196 | 193 |
| Background/unlabelled | 500 | 492 |
| Total | 996 | 982 |

There are 1,353 target-sector feature rows, with no duplicate TIC-sector keys. The 14 targets absent from the final feature table are all accounted for by download failures. There are 25 failed download records for 25 distinct targets: 11 of those targets still supplied another usable sector. Preprocessing, BLS and feature-stage failure tables are empty. A completed pipeline run therefore does not mean every requested download succeeded.

Checks confirmed:

- Feature and score tables have identical TIC-sector keys, and labels match the selected catalogue sample.
- All 1,353 processed curves have aligned arrays, increasing unique times, finite detrended flux, positive trends and valid positive flux errors. Configured quality bits are filtered, and detrended flux equals normalized flux divided by the trend.
- No infinite numeric feature values were found. The transformed ML matrix is finite and matches its saved row order.
- The model uses 41 explicitly selected features. TIC, TOI, sector, labels, disposition and catalogue period are absent from the model feature list. Stellar-catalogue-dependent radius and duration-consistency proxies are excluded as configured.
- Every BLS search used measured errors. Saved IF scores match negative `score_samples`; saved LOF scores match negative fit-time outlier factors. The saved LOF reference matrix matches transformed training features.
- Equal-weight percentile ensemble and hybrid formulas reproduce the saved scores.
- Unique-target scores reproduce the documented per-method maximum across sectors.
- Every saved main-model top-K count, precision, recall, positive-rank summary, ROC-AUC and average precision was independently recomputed from the target rankings and agreed.
- Refitting on the original feature-table row order reproduces the saved primary model scores.
- All four ablation families, PCA coordinates for 1,353 rows, 250 feature-score correlation rows and 21 PNG/PDF figure pairs are present. One top-candidate diagnostic was visually inspected; this is not exhaustive astrophysical vetting of every target.

## Main scientific results

At the top 99 of 982 targets (approximately 10%):

| Method | Catalogue-positive hosts recovered | Recall | ROC-AUC | Average precision |
|---|---:|---:|---:|---:|
| BLS depth SNR | 44/297 | 14.81% | 0.6434 | 0.5991 |
| Isolation Forest | 21/297 | 7.07% | 0.5382 | 0.4774 |
| LOF | 22/297 | 7.41% | 0.4226 | 0.4385 |
| Anomaly ensemble | 24/297 | 8.08% | 0.4843 | 0.4615 |
| Hybrid | 25/297 | 8.42% | 0.5663 | 0.5174 |

Recovery uses all 297 catalogue-positive hosts. The binary AUC/AP comparison uses a different subset: 169 hosts with a CP/KP disposition versus 193 FP/FA hosts (362 total). The 128 PC-only hosts and 492 unlabelled backgrounds are excluded from binary AUC/AP. These denominators must remain distinct in the paper.

BLS depth SNR and the ensemble have target-level Spearman rho = 0.330048. The scores therefore differ, but this correlation does not show that anomaly scores add useful independent discrimination. At the stated inspection budget, the ensemble and hybrid recover fewer catalogue-positive hosts than BLS. Maximum BLS power and depth SNR are identical in this SNR-objective experiment; they are not two independent baseline methods.

## Corrections needed before final paper tables

### 1. All-feature ablation does not reproduce the primary model

Training reads the original feature table. Evaluation instead refits ablations from the score table, which has been sorted by ensemble score. With a fixed random seed, Isolation Forest's sampled row indices refer to different objects after reordering. This changes the fitted finite ensemble and consequently some IF, ensemble and hybrid rankings.

The cause was verified in both directions: original-order refitting reproduces the primary scores; sorted-score-order refitting reproduces the saved all-feature ablation metrics. Nine method/cutoff combinations have different recovered counts. For example, at K=99 the primary IF recovers 21 while its all-feature ablation recovers 22; primary hybrid recovers 25 while the all-feature ablation recovers 26.

The main metrics remain valid. However, feature-family comparisons currently include a change in fitting order as well as representation. Use the same original target-sector order for every family, and verify that the all-feature ablation exactly reproduces the primary result. Prefer reusing the primary all-feature scores for that control. Regenerate ablation tables and the research report after correction. Do not claim a physics-feature benefit from the current ablation alone.

### 2. Seven winning BLS periods slightly exceed the intended cap

Astropy's automatically sampled grid can place its last period just beyond the supplied upper endpoint. The code uses the resulting power array without explicitly removing out-of-range trials. Seven winning periods exceed `min(12 days, baseline/2)` by approximately 0.0116–0.0225 days. This is a small discretisation issue, not an array-alignment or flux-quality failure, but the output does not strictly satisfy the stated search cap.

Affected TIC-sector pairs: 42054565–3, 451599528–12, 148273382–7, 183537481–2, 159707889–11, 192559318–9 and 255400005–12. Exact values are in `output_audit.json`.

Explicitly constrain the trial-period array before selecting peaks and harmonics, add a boundary regression check, and regenerate dependent results. The effect of this correction on rankings has not been measured in this audit.

## Interpretation limits relevant to the abstract

- The experiment fits and ranks the same unlabelled sample. Reference labels support retrospective evaluation, not semi-supervised learning or independent predictive validation.
- Physics-informed means feature engineering. No physical equations are enforced during training. The stellar duration-consistency feature is entirely missing here; the default physics family is chiefly morphology plus the depth-derived radius ratio.
- 71 of the 297 hosts' representative catalogue periods fall outside the nominal 0.5–12-day grid. A host label also does not guarantee that a transit occurred in the selected sector. Known-host recovery is not a measured planet-detection completeness rate.
- Repeated sectors are correctly aggregated for target-level metrics, but observing opportunities differ: two sectors are available for 132/297 planet hosts, 93/193 false positives and 146/492 backgrounds. Both maximum-score selection and fitting multiple rows per target can introduce observing-selection effects.
- The feature-score correlation table operates on target-sector rows. Its p-values should not be treated as independent-target inference because sectors from a common TIC can be correlated; target-level aggregation or clustered uncertainty estimates are needed for inferential use. Exploratory multiple-testing caveats also apply.
- All five top hybrid-ranked objects are unlabelled backgrounds, with fitted depths approximately 5–31%. The inspected leading target has deep repeated dips, a second dip away from phase 0.5, and visible detrending ripples. These observations warrant manual vetting; they do not justify calling these objects planet candidates. A secondary-eclipse proxy fixed at phase 0.5 can miss the second dip visible in this example.
- Correlations, PCA, ablations and diagnostic plots describe associations. They do not provide causation, formal per-object model attribution or calibrated anomaly significance. No study of actual human inspection time or independent generalisation has been performed.

## Supported paper wording

“In a descriptive analysis of 1,353 TESS light curves from 982 targets, BLS depth-SNR ranking recovered 44 of 297 catalogue-positive hosts within the top 99 targets, compared with 24 for the anomaly ensemble and 25 for the hybrid. At this inspection budget, the tested anomaly-based rankings did not improve known-host recovery over BLS. The framework provides interpretable diagnostics for investigating high-scoring light curves; independent evaluation is required to assess generalisation and inspection-workload reduction.”

These numbers describe the currently saved outputs. Final publication values should be regenerated after the two implementation corrections above.

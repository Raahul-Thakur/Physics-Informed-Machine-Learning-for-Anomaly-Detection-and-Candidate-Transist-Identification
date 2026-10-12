# Completed V3 evidence and abstract-claim assessment

Reporting revision: 11 October 2026. Computations completed on 6 October 2026.
The submitted title and abstract remain unchanged. This report describes what the experiments
actually support. No model or ranking formula was changed after inspecting V3 outcomes.

## Sample and integrity

All 1,032 selected targets produced features: 1,364 light curves in sectors 27–39, with no
remaining acquisition or feature-processing failures. One interrupted FITS download was
retained under an `.interrupted-20261003` suffix and successfully downloaded again; its
initial failure log is retained separately. There are no target overlaps with the 1,988 excluded
previously inspected targets and no recovered periods outside the configured search limits.

The evaluation includes 300 catalogue-positive targets, 232 labelled false positives and
500 unlabelled backgrounds. The positive group comprises 124 targets with CP/KP dispositions
and 176 PC-only targets. Backgrounds are not verified negatives. The historical V2 positive
group similarly contained 151 CP/KP and 149 PC-only targets: its preserved 28/300 versus
33/300 result is catalogue-positive recovery, not confirmed-planet recovery.

## Frozen independent ranking results

At K=100, using each method's maximum score across sectors:

| Method | Catalogue-positive recovery /300 | CP/KP recovery /124 | Period-and-epoch matches in top 100 |
| --- | ---: | ---: | ---: |
| BLS | 32 | 26 | 20 |
| Unsupervised anomaly | 14 | 4 | 2 |
| Unsupervised hybrid | 21 | 10 | 6 |
| Semi-supervised reference-class affinity | 37 | 21 | 17 |
| Semi-supervised anomaly | 18 | 9 | 5 |
| **Predefined primary semi-supervised hybrid** | **24** | **13** | **9** |

The primary hybrid–BLS difference is −8 catalogue-positive targets, with a paired target-level
bootstrap 95% interval of [−19,+2], conditional on the fitted models and calibration. Under
coverage-selected one-sector evaluation, the primary hybrid recovers 22 versus BLS's 31,
difference −9, interval [−20,+1]. These results do not demonstrate superiority.

For the predefined 10% catalogue-positive recovery target (30 of 300), the primary hybrid
requires 112 inspections versus 87 for BLS; the one-sector budgets are 116 versus 88.
The primary method therefore does not reduce this inspection budget. Human review time
was not measured.

The secondary affinity-only method recovers 37 versus 32 at K=100, but its paired difference
interval is [−6,+16]. Its 10% recovery budget is 86 versus 87. These observations do not
justify replacing the primary method after inspection or claiming a proven workload benefit.
On CP/KP versus FP/FA references, affinity-only ROC-AUC is 0.602 and AP is 0.440, compared
with BLS's 0.498 and 0.365. These are supplementary descriptive point estimates, not
calibrated significance tests, planetary probabilities or real-survey purity estimates.

The 80-BLS-plus-20-additional-semi-hybrid list recovers 30 versus 32 for BLS alone, gaining
four positive targets but losing six. The one-sector comparison is 32 versus 31, gaining
four and losing three. Both outcomes are retained; a favourable secondary comparison is
not substituted for the primary result.

Of 300 positive targets, 219 have a representative catalogue period inside the realised
search grid. BLS and the primary hybrid recover 31 and 21 of these at K=100. The full
300-target denominator remains the headline outcome. Grid eligibility does not guarantee
sampled transit visibility or completeness for multi-planet systems.

## Transit-signal agreement

A metadata-screened NASA literature selection retained 91 ephemerides across 79 targets,
requiring explicit BJD-TDB, finite uncertainties, no limit flags and no flagged TTV. Period
and epoch are kept from one literature solution. The frozen matcher rejects overly uncertain
propagated epochs; it assumes zero period–epoch covariance. There are 76 positive targets
with testable selected-sector ephemerides. The top-100 signal-match counts above concern
the sector selected by each ranking. Unavailable ephemerides are untestable, not failed
planet confirmations. Agreement does not establish a new planet or the physical source of a dip.

## Statistical significance

The separate cohort was locked before reading scores: 480 unlabelled reference targets and
20 test targets. All were scored. Conservative upper-tail rank p-values from the fixed raw
Isolation Forest statistic were adjusted by Holm over the full family at alpha=0.05.
There were **zero rejections**. The smallest unadjusted p-value was 0.004158; the smallest
adjusted p-value was 0.08316.

This test concerns exchangeability with the selected unlabelled SPOC reference population.
It is not a test of planetary origin or a universal definition of dominant stellar variability.
The experiment supplies a statistical procedure but no statistically significant objects under
that procedure. Failure to reject does not establish that all objects are ordinary.

## Development injections and controlled interventions

All 14,400 method-trials on 30 distinct real development stars completed. Savitzky–Golay
retrieved the injected period in 3,924/7,200 trials (54.5%), versus 3,703/7,200 (51.4%) for
rolling median. A 5,000-repeat paired whole-star bootstrap gives a difference of +3.07
percentage points, 95% interval [+1.58,+4.71]. Median paired depth biases are −5.27% and
−1.83%, respectively. The 768 out-of-grid trials remain in the headline denominator;
36 trials lack finite template-depth estimates, so depth medians condition on available values.
All 30 original raw-file hashes remain unchanged. This measures synthetic-signal sensitivity
and attenuation, not real-planet purity or calibrated false-alarm performance.

All 54 controlled raw-light-curve intervention cases completed on three development stars.
Changing depth, period or duration changes the output, with direction and magnitude depending
on the star and parameter. These are controlled effects on software, not astrophysical causes
of the original variability. Existing per-feature replacement diagnostics also describe score
behaviour, but correlated-feature replacements need not be physically realistic.

## Predefined visual diagnostic review

The ten plots were inspected. Selection used two examples per group, by semi-hybrid rank
except for BLS-only cases, which used BLS rank. These are descriptive illustrations, not
prevalence estimates or human timing measurements.

| Group and TIC | Observed morphology and measured evidence | Interpretation limit |
| --- | --- | --- |
| Both: 371443216 | Repeated coherent dips; folded rounded-bottom transit; period 2.82442 d; signal agreement | Shows a recovered reference signal, not new validation |
| Both: 441420236 | Large positive excursions, irregular local variability; 6.33016 d BLS period differs from representative 8.45368 d; event-dominance proxy 0.972 | Host recovery is not demonstrated transit recovery; epoch untestable |
| BLS-only: 160708862 | Repeated, coherent 3.34518 d dips; signal agreement; anomaly percentile 0.596 | Clear reference transit need not be highly anomalous |
| BLS-only: 290131778 | Repeated 3.30618 d dips; signal agreement; anomaly percentile 0.551 | Hybrid ranking can demote coherent transits |
| Hybrid-only: 263075864 | Repeated dips amid scatter; period 4.81301 d near catalogue 4.81032 d; PC disposition | Epoch untestable; candidate recovery is not confirmed-planet recovery |
| Hybrid-only: 201248411 | Short, repeated 0.98085 d dips; signal agreement; high anomaly percentile | Example of complementarity, not a net population benefit |
| False positive: 127793615 | Deep dips with surrounding positive excursions; BLS depth 0.0690 | Strong BLS/anomaly scores also select labelled false positives |
| False positive: 270841724 | Dominant boundary excursion, isolated extremes, asymmetric folded profile; event-dominance proxy 0.984 | Folded morphology can reflect sparse or boundary-driven structure |
| Background: 146520491 | Large continuous periodic modulation; BLS depth 0.1263; top hybrid score | Unlabelled high variability is not a validated transit candidate |
| Background: 452734608 | Deep repeating dips and changing out-of-dip levels; BLS depth 0.3587 | Eclipse-like morphology warrants investigation, not a planetary claim |

## Which abstract claims are supported?

| Claim | Current evidence status |
| --- | --- |
| Public TESS preprocessing, segmentation and conventional period search | Implemented and executed; complete acquisition/feature manifests |
| Astrophysically motivated features | Implemented; physics-informed must retain the feature-engineering definition |
| Unsupervised and semi-supervised analysis | Both fitted on development data and scored on unseen targets |
| Additional discriminatory information | Evaluated, with mixed secondary findings and a negative primary comparison |
| Significantly unusual observations | **Not demonstrated:** 0/20 after the predefined correction |
| Properties that cause anomalous classification | Controlled software-input responses measured; astrophysical causation **not established** |
| Candidate identification and interpretability | Candidate measurements, reference comparisons, ephemeris agreement and diagnostics provided; no planet validation |
| Reduced inspection workload | **Not demonstrated** by the primary experiment; no human timing study |

The project supports a research poster about an interpretable, evaluated framework with
limitations and unsuccessful comparisons. It does not substantiate every literal outcome
claim in the submitted abstract. This evaluated population is now inspected; any changes
motivated by these results need a new untouched sample for independent confirmation.

## Artifacts

- `experiments/independent_v3/evaluation`: frozen rankings, candidates, curves, budgets, paired uncertainty, explanations and ephemerides.
- `experiments/abstract_evidence/final_summary`: reference-group tables, discrimination, injection tables and PNG/PDF figures.
- `experiments/abstract_evidence/significance`: full test family, reference scores and outcome.
- `experiments/abstract_evidence/diagnostic_review`: ten PNG/PDF plots, measured features and selection rule.
- `docs/abstract_evidence_plan.md`: cohort protocol, assumptions, provenance and reproduction commands.

The last code check passed 56 tests. Frozen-model and evidence manifests and all 371 protected
historical files were reverified. The local artifacts have not been publicly deposited or assigned a DOI.

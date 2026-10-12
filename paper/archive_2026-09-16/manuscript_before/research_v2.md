# Frozen research extension

This extension preserves `experiments/default/outputs` as the descriptive baseline. Its outputs live under `experiments/research_v2/`. It implements new experiments; it does not assert that recovery improves.

## Frozen development and independent evaluation

`config/research_v2.yaml` specifies a compact primary representation, five comparison representations, a 20% calibration fraction, a 0.95 redundancy threshold for the new representations, and an 80% BLS / 20% additional-anomaly allocation at budget 100. The compact hypothesis was motivated by earlier labelled development results. This is label-informed experiment selection; IF/LOF fitting, calibration, and redundancy removal do not use labels.

Targets are split deterministically into training and calibration groups; sectors from a target never cross the split. All usable training sectors fit median imputation, robust scaling, Isolation Forest and novelty-enabled LOF. Calibration uses one coverage-selected curve per calibration target. It fixes empirical score distributions for IF, LOF, BLS depth SNR and the ensemble. Unseen scores use midpoint empirical CDF values against those saved calibration arrays. Equal-weight IF/LOF percentiles form the ensemble; the hybrid averages the fixed BLS and ensemble percentiles. Evaluation batches never refit transforms or recompute percentile distributions. This calibration differs from the original transductive, within-batch rank normalization and must be described as a new experiment.

The frozen directory includes models, selected features and redundancy decisions, source snapshot, package versions, UTC freeze time, original configuration, protocol, training/calibration IDs, and all excluded development IDs. The original 996 targets are development data. Targets from earlier small and cached-probe samples are also excluded, even when absent from the current 996. Their inclusion in the exclusion list does not add them to model fitting. Model checksums, source fingerprints and scientific dependency versions are checked on loading. Existing frozen directories cannot be overwritten.

Development calibration diagnostics are produced, but these targets were already part of the inspected development population and were used to calibrate scores. **These diagnostics are not independent evaluation.** The new evaluation sampling plan uses sectors 14–26, seed 2027, requested counts 300 planet/candidate hosts, 300 false positives and 500 backgrounds, subject to actual availability. This changes the observing population; target disjointness does not remove selection bias or sector-dependent distribution shifts. Sampling is catalogue-stratified, while model fitting is label-free.

The initial `development_calibration` report uses the one-sector calibration rows. To test exposure on all available sectors of those same calibration targets without changing the fitted models or calibration arrays, run:

```powershell
..\.venv\Scripts\python.exe scripts/development_exposure.py --frozen experiments/research_v2/frozen --output experiments/research_v2/development_exposure
```

This additional comparison remains development evidence. Training-target scores are not substituted for unseen LOF scores.

### First freeze of a new version

From the repository directory in PowerShell:

```powershell
..\.venv\Scripts\python.exe scripts/research_experiment.py freeze --config config/default.yaml --protocol config/research_v2.yaml --output experiments/research_v2/frozen
```

Do not repeat this command for an existing frozen version. Changes to the scientific source require a new version or restoring the saved source snapshot and recorded dependencies. Keep new versions distinct, and do not call a population independent after inspecting it for model selection.

### Prepare a new target-disjoint evaluation sample

```powershell
..\.venv\Scripts\python.exe scripts/research_experiment.py prepare-evaluation --frozen experiments/research_v2/frozen --workspace experiments/independent_v2 --config-output config/independent_v2.yaml
```

This only creates the locked acquisition configuration and references the frozen exclusion list. It does not download observations or produce independent evidence. It refuses an existing evaluation workspace/config. If the configuration has already been prepared, continue with acquisition:

```powershell
..\.venv\Scripts\python.exe scripts/run_pipeline.py --config config/independent_v2.yaml --stage download --resume
..\.venv\Scripts\python.exe scripts/run_pipeline.py --config config/independent_v2.yaml --stage features --resume
..\.venv\Scripts\python.exe scripts/research_experiment.py evaluate --frozen experiments/research_v2/frozen --evaluation-workspace experiments/independent_v2 --output experiments/independent_v2/frozen_evaluation
```

Use only download and features stages for these new observations. The ordinary `all` command would fit models on the evaluation population and would not be this independent experiment. The features stage performs preprocessing and BLS as needed. Frozen evaluation checks the sampling plan, preprocessing and BLS configuration, and rejects any development-target overlap. It reports requested, analysed and missing targets. Download shortages are not filled with fabricated observations.

## Coherence and compact representations

The baseline feature families are preserved. New `compact` and `extended` representations add:

| Feature | Definition and limitations |
|---|---|
| Event-depth relative MAD | Local out-of-transit median minus each event median; MAD divided by absolute median depth, with at least three measurable events |
| Event-duration relative MAD | Scatter of sampled half-depth widths divided by median width, with at least three measurable events; a proxy, not a fitted physical duration |
| Single-event power fraction | Maximum positive depth-squared × in-transit count / local MAD-squared contribution divided by the event total; a dominance proxy, not exact BLS power attribution |
| Local noise beta | Scatter of duration/2-bin mean flux divided by expected white-noise scatter; bins stay within photometric segments and use local out-of-transit points |
| Edge-to-centre depth ratio | Median-based outer-transit depth divided by centre depth; approximate flat-bottomed versus V-shaped morphology |
| Ingress/egress difference | Median flux difference between the two outer transit regions |
| Secondary scan depth and ratio | Strongest median dip on an 80-position orbital-phase grid outside the primary region, and its ratio to the primary depth |

The secondary scan is a coarse feature measurement, not an exhaustive secondary-transit search. Narrow secondary events can fall between trial centres. Maximizing over phases introduces selection effects; the feature is not calibrated significance. Event widths and noise beta can be affected by sampling, spots, variability, and remaining systematics. Missing measurements remain NaN and use the training-only feature contract. No proxy establishes planetary origin or causation.

Compact features omit the repeated generic variance/amplitude family. New compact/extended transforms further remove features with absolute pairwise Spearman correlation at least 0.95, using at least 20 jointly observed training rows and deterministic whitelist order. The report records which retained feature made each removed feature redundant. This feature-selection rule does not examine calibration/evaluation labels or scores. Legacy families retain their existing feature-selection behavior for comparison.

## Exposure and search coverage

Every representation has an all-sector comparison and a coverage-selected single-sector comparison. Selection uses most valid cadences, then longest baseline, then smallest sector number. The selection rule never reads scores or labels. Both comparisons apply the same frozen model; this tests score aggregation exposure, not a model refitted to one-sector training data.

`metrics.csv` retains full-population recall and adds eligible-positive recall at the same inspection budgets. The eligible-positive denominator includes hosts whose representative catalogue period lies within the configured minimum and at least one selected sector's baseline-limited maximum. The ranking pool is unchanged: out-of-grid and missing-period hosts are not silently removed or recast as false positives. The eligibility table distinguishes missing periods. This is grid eligibility, not proof that transits occurred in the observed windows or completeness over all planets in a system.

## Complementarity and uncertainty

Inspect the first 80 BLS-ranked targets, then the highest 20 ensemble-ranked targets not already selected, at an effective budget of 100. Smaller populations use floor(0.8 × effective budget) BLS slots. TIC order resolves ties. Export actual selected IDs, gains, losses, and net catalogue-host recovery against the same-budget BLS list.

The paired target bootstrap resamples per-target differences between the two fixed inspection lists, with 1,000 replicates and percentile 95% intervals. These are conditional descriptive intervals: the lists are fixed, models are not refitted, and selection/training uncertainty is not included. Counts reflect catalogue-positive hosts, not validated planet purity. Additional recovery does not establish reduced human review time. The allocation is frozen before new evaluation; changing it based on development results must be disclosed and tested on untouched data.

## Real-light-curve injection validation

```powershell
..\.venv\Scripts\python.exe scripts/real_injection_recovery.py --config config/default.yaml --settings config/real_injections.yaml --output experiments/research_v2/injections
```

The default experiment uses six deterministically selected real targets, one sector each, three periods, three depths, two durations, and one randomized phase per case. Each of the 108 signals is processed with Savitzky–Golay and rolling-median detrending, giving 216 paired trials. Signals are trapezoids injected multiplicatively into copies of the raw photometry before preprocessing. Raw-file hashes are verified, and observation files are never modified. The existing rolling median is a robust comparator; this implementation does not add Wōtan as a dependency.

The noise and original uncertainties are retained, not resimulated. The signal family approximates morphology without limb darkening or a physical orbital fit. Original light curves can contain real variability and transits. Uninjected controls are therefore not guaranteed null examples or false alarms.

Outputs separate blind direct-period and harmonic retrieval, sampled event counts, grid eligibility, and paired depth attenuation at the known injected ephemeris. Depth attenuation regresses the injected/control detrended flux ratio against the injection template. This isolates preprocessing response more directly than comparing a possibly unrelated winning BLS depth to the injected depth. Trial failures are explicit; summary recovery rates condition on successful processing. The small default experiment is a validation pilot, not a survey-completeness estimate. Its output never enters real-candidate rankings.

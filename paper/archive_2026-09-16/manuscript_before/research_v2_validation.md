# Research extension implementation validation

Implemented and exercised on 2026-09-13. The original larger-run scientific outputs remain under `experiments/default/outputs`; this extension writes separate artifacts.

- Test suite: 31 passed. Ruff passes for source, tests and scripts.
- Frozen model fitting: 796 targets. Separate development calibration: 200 targets, one curve per target for calibration distributions.
- Additional exposure diagnostics: all 269 available curves of those 200 calibration targets versus 200 coverage-selected curves.
- Independent exclusion list: 1,064 unique previously inspected targets, including the current 996 and additional targets from earlier experiments.
- Six representation families fitted. Compact retains 15 features after one redundant feature is removed; extended retains 33 after 16 redundant features are removed. The original all-feature family retains 41.
- Frozen-model serialization, disjoint-target rejection, label-free scoring, score-batch invariance, training-only redundancy selection, unchanged transform statistics, source-version rejection, deterministic exposure selection, complementary-list deduplication and raw-file preservation are covered by tests.
- The frozen model/package/source checks pass on the saved real-data bundle.
- The independent acquisition configuration is prepared at `config/independent_v2.yaml`. No new evaluation observations have been downloaded by this implementation run, and no independent performance result is claimed.

## Development exposure diagnostics

These results involve previously inspected calibration targets, not an independent sample. At K=100, among 63 catalogue-positive targets:

| Exposure | BLS recovered | Compact hybrid recovered | 80/20 complementary list recovered |
|---|---:|---:|---:|
| All available sectors | 39 | 37 | 37 |
| Coverage-selected single sector | 37 | 35 | 36 |

The compact complementary list gains two hosts and loses four relative to BLS with all sectors, a net difference of −2. Its conditional paired-bootstrap 95% interval is [−7, 3]. For one sector, it gains two and loses three, net −1 with interval [−5, 3]. These intervals condition on fixed inspection lists and do not include model-fitting uncertainty. Neither comparison demonstrates improvement over BLS. Forty-five of the 63 positive reference targets meet representative-period grid eligibility under these comparisons; full-sample metrics retain all 63.

## Injection pilot

All 216 trials succeeded, with 12 successful uninjected controls and 216 finite paired template-depth estimates. Each detrending method processes the same 108 signals in six real target light curves.

| Detrender | Direct period retrieval | Median paired depth bias |
|---|---:|---:|
| Savitzky–Golay | 60/108 (55.6%) | −7.3% |
| Rolling median | 55/108 (50.9%) | −1.6% |

The pilot suggests a depth-preservation/retrieval tradeoff, not a universal winner. Savitzky–Golay remains the frozen default; no independent outcomes were used to select it. Synthetic signal retrieval is not real-planet validation, detection at a calibrated false-alarm rate, or a survey-wide completeness estimate.

## Artifact locations

- `experiments/research_v2/frozen/protocol.json`: fixed settings, IDs, hashes, source/dependency versions and selection history.
- `experiments/research_v2/frozen/feature_selection_*.csv`: selected, missing, disabled and redundant features.
- `experiments/research_v2/development_exposure/`: scores, metrics, eligibility, selected sectors, complementary lists and report.
- `experiments/research_v2/injections/`: every trial, uninjected controls, method summaries, selected source curves and injection protocol.
- `experiments/research_v2/implementation_validation.json`: implementation-run status.

Commands and detailed definitions are in [research_v2.md](research_v2.md).

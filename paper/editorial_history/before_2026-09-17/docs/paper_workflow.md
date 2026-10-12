# Preserved final paper workflow

The inspected independent result is archived in `paper/archive_2026-09-16`. The evaluated compact hybrid recovered 28/300 catalogue-positive hosts at K=100, versus BLS's 33/300. This result must not become untouched validation again after model choices are motivated by it.

The final reporting package is `paper/final`. Start with `manuscript.md`, `diagnostic_review.md`, `figure_captions.md` and `REPRODUCE.md`. It includes machine-readable tables, eight summary figures and ten diagnostic figures in both PNG/PDF, and copies of selected diagnostic photometry. The prior abstract and methods remain in the archive; the current `docs/abstract.md` is updated to the independent result.

From the repository directory in the recorded environment, reproduce all numerical reporting and figures with:

```powershell
python scripts/paper_report.py --reproduce --archive paper/archive_2026-09-16 --output paper/reproduction
```

The destination must not already exist. The command verifies the input archive and referenced photometry checksums, performs paired target bootstrap resampling with reranking, and regenerates the paper tables, figures and manuscript template. It never fits a new model or changes the original evaluated rankings. Recorded visual-review notes and captions are editorial supplements, not algorithmic discoveries; preserve them alongside regenerated outputs.

The archive contains frozen models, source snapshot, reporting scripts, tests, requirements, package versions, acquisition configurations, target IDs, original result tables and hashes. The full raw/processed photometry is referenced in the experiment workspace by checksum, rather than duplicated into the archive. A clean-machine reproduction therefore requires restoring those files and the recorded scientific environment. Selected diagnostic data are copied into the final report for convenient inspection.

The paired 95% interval for the primary difference is [−13, +3] hosts, with an observed difference of −5. It reflects resampling of evaluation targets and reranking while models remain fixed. It does not include uncertainty from fitting a different model, changing calibration samples, label errors or population-selection bias. It supports no claim of improved recovery or reduced human inspection time.

The software and result reporting are ready for author review. Journal formatting, author/affiliation details, a completed literature review and any required data-release arrangements remain manuscript submission tasks. Visual morphology review is not independent astrophysical validation.

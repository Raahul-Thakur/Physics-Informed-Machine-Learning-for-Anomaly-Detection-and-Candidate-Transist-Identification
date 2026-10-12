# Reproduce the preserved paper analysis

From the repository directory, using the recorded Python environment:

```powershell
python scripts/paper_report.py --reproduce --archive paper/archive_2026-09-16 --output paper/reproduction
```

The command verifies archive and referenced photometry hashes, resamples paired targets with the saved seed and regenerates tables, figures and manuscript into a new directory. It never refits models or overwrites the independent evaluation. Copies of scripts, tests, frozen source, package versions and requirements-lock.txt are retained in the archive. Restore the frozen source and recorded environment if the working scientific code changes. Human visual review notes are a separate supplement and are not regenerated as if produced by an algorithm.

Run `python -m pytest -q` for checks. Exact numerical table equality is expected under the recorded environment; PDF timestamps can differ, so figure file hashes need not match. The independent sample is now inspected: do not reuse it as untouched validation after tuning.

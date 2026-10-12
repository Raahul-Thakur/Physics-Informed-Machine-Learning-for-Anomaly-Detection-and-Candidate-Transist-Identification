"""Select explicit BJD-TDB, non-TTV literature ephemerides without consulting scores."""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import research_v3 as v3


def select(snapshot, ids):
    f = snapshot.copy()
    f["tic_id"] = pd.to_numeric(
        f.tic_id.astype(str).str.extract(r"^TIC\s+(\d+)$")[0], errors="coerce"
    )
    f = f[f.tic_id.isin(ids)].copy()
    f["time_verified"] = f.pl_tsystemref.isin(["BJD-TDB", "BJD/TDB"])
    numeric = [
        "pl_orbper",
        "pl_orbpererr1",
        "pl_orbpererr2",
        "pl_tranmid",
        "pl_tranmiderr1",
        "pl_tranmiderr2",
    ]
    finite = np.isfinite(f[numeric]).all(axis=1)
    f["eligible"] = (
        f.time_verified
        & finite
        & (f.pl_orbper > 0)
        & (f.pl_tranmid > 2400000)
        & f.ttv_flag.eq(0)
        & f.pl_orbperlim.eq(0)
        & f.pl_tranmidlim.eq(0)
        & (f.pl_orbpererr1 > 0)
        & (f.pl_orbpererr2 < 0)
        & (f.pl_tranmiderr1 > 0)
        & (f.pl_tranmiderr2 < 0)
        & f.pl_refname.notna()
    )
    # Prefer the archive default among eligible coherent literature rows; otherwise newest.
    chosen = (
        f[f.eligible]
        .sort_values(
            ["tic_id", "pl_name", "default_flag", "pl_pubdate", "rowupdate", "pl_refname"],
            ascending=[True, True, False, False, False, True],
            kind="stable",
        )
        .drop_duplicates(["tic_id", "pl_name"])
    )
    out = pd.DataFrame(
        dict(
            tic_id=chosen.tic_id.astype("int64"),
            catalogue_id=chosen.pl_name,
            period_days=chosen.pl_orbper,
            epoch_bjd_tdb=chosen.pl_tranmid,
            period_error_days=chosen[["pl_orbpererr1", "pl_orbpererr2"]].abs().max(axis=1),
            epoch_error_days=chosen[["pl_tranmiderr1", "pl_tranmiderr2"]].abs().max(axis=1),
            reliable=True,
            reference=chosen.pl_refname,
            publication_date=chosen.pl_pubdate,
            time_system=chosen.pl_tsystemref,
        )
    )
    return out, f


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--snapshot", type=Path, required=True)
    p.add_argument("--sample", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        raise ValueError("Do not overwrite ephemeris selection")
    result, audit = select(pd.read_csv(args.snapshot), pd.read_csv(args.sample).tic_id)
    args.output.mkdir(parents=True)
    result.to_csv(args.output / "ephemerides.csv", index=False)
    audit.to_csv(args.output / "selection_audit.csv", index=False)
    v3.write_json(
        args.output / "provenance.json",
        dict(
            snapshot_sha256=v3.sha(args.snapshot),
            sample_sha256=v3.sha(args.sample),
            script_sha256=v3.sha(__file__),
            rule="Explicit BJD-TDB; finite positive uncertainties; no limits or flagged TTV; "
            "period and epoch from same literature row. Prefer eligible archive default, then newest publication.",
            caveat="Catalogue metadata reliability screen, not individual paper reanalysis. "
            "Frozen matcher assumes zero period-epoch covariance and rejects propagated uncertainty "
            "larger than half the measured duration. Unflagged TTV and stale solutions remain possible.",
            selected_planets=len(result),
            selected_targets=result.tic_id.nunique(),
        ),
    )
    v3.seal(args.output)


if __name__ == "__main__":
    main()

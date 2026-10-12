"""Additional evidence experiments without altering the frozen V3 ranking model.

Statistical tests concern a sampled stellar reference population, not planetary origin.
Interventions concern the deterministic software pipeline, not natural stellar causation.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import research_v3 as v3
import yaml

from tess_anomaly.bls import search_bls
from tess_anomaly.coherence import coherence_features
from tess_anomaly.features import extract_features
from tess_anomaly.preprocessing import preprocess
from tess_anomaly.real_injections import inject
from tess_anomaly.research import one_sector

ROOT = Path(__file__).resolve().parents[1]


def conformal_pvalues(reference, scores):
    """Upper-tail ranks with finite-sample correction and conservative ties.

    Marginal super-uniformity requires a fixed score independent of this reference
    set and exchangeability of reference/null test observations. No clean-inlier
    or planet-negative interpretation is assigned to unlabelled backgrounds.
    """
    reference, scores = np.asarray(reference, float), np.asarray(scores, float)
    if reference.ndim != 1 or scores.ndim != 1 or not len(reference):
        raise ValueError("Require nonempty one-dimensional reference and test vectors")
    if not np.isfinite(reference).all() or not np.isfinite(scores).all():
        raise ValueError("Nonfinite statistical scores")
    ordered = np.sort(reference)
    return (1 + len(reference) - np.searchsorted(ordered, scores, side="left")) / (
        len(reference) + 1
    )


def holm(pvalues):
    """Holm adjusted p-values; family-wise error control for valid marginal p-values."""
    values = np.asarray(pvalues, float)
    if values.ndim != 1 or not len(values) or not np.isfinite(values).all():
        raise ValueError("Require a nonempty finite p-value vector")
    if np.any((values < 0) | (values > 1)):
        raise ValueError("P-values outside [0,1]")
    order = np.argsort(values, kind="stable")
    corrected = np.minimum(1, np.maximum.accumulate(values[order] * np.arange(len(values), 0, -1)))
    result = np.empty_like(values)
    result[order] = corrected
    return result


def lock_cohort(sample, bundle, output, seed=20261003, test_count=20):
    """Lock roles using only selected catalogue IDs and group, before reading scores."""
    if output.exists():
        raise ValueError("Cohort lock already exists")
    if sample.tic_id.duplicated().any() or sample.tic_id.isna().any():
        raise ValueError("Cohort must contain unique, nonmissing target IDs")
    if set(sample.tic_id) & set(bundle["excluded_ids"]):
        raise ValueError("Previously inspected targets cannot be significance references/tests")
    ids = np.sort(sample.loc[sample.label.eq("background"), "tic_id"].to_numpy(dtype="int64"))
    if test_count < 1 or len(ids) <= test_count:
        raise ValueError("Insufficient unlabelled targets for reference/test split")
    test_ids = set(np.random.default_rng(seed).choice(ids, test_count, replace=False))
    roles = pd.DataFrame(
        {"tic_id": ids, "role": ["test" if i in test_ids else "reference" for i in ids]}
    )
    output.mkdir(parents=True)
    roles.to_csv(output / "roles.csv", index=False)
    sample.to_csv(output / "selected_sample.csv", index=False)
    v3.write_json(
        output / "plan.json",
        dict(
            seed=seed,
            alpha=0.05,
            method="raw_isolation_forest",
            correction="Holm; one family over every prespecified test target",
            test_count=test_count,
            reference_count=len(ids) - test_count,
            script_sha256=v3.sha(__file__),
            null="Target drawn from the same selected unlabelled SPOC stellar population as reference targets",
            assumptions="Fixed model; target exchangeability; identical selection/preprocessing/coverage rules. "
            "Missingness must not depend on randomly assigned role. Unlabelled references are not verified inliers.",
            interpretation="Statistically extreme relative to this reference population, not planet significance "
            "or proof of deviation from every dominant stellar variability class.",
        ),
    )
    v3.seal(output)


def significance(frame, bundle, cohort, output):
    if output.exists():
        raise ValueError("Refusing to overwrite statistical results")
    v3.verify(cohort)
    plan = json.loads((cohort / "plan.json").read_text())
    if plan["script_sha256"] != v3.sha(__file__):
        raise ValueError("Evidence implementation changed since cohort lock")
    v3.check_frame(frame)
    if set(frame.tic_id) & set(bundle["excluded_ids"]):
        raise ValueError("Statistical data overlap inspected/training targets")
    if not set(frame.sector) <= set(bundle["protocol"]["evaluation_sectors"]):
        raise ValueError("Statistical data outside predefined observing sectors")
    roles = pd.read_csv(cohort / "roles.csv")
    chosen = one_sector(frame[frame.tic_id.isin(roles.tic_id)])
    # Raw IF avoids saturation of empirical-CDF anomaly scores; fixed in advance.
    x = bundle["transform"].transform(chosen)
    scores = pd.DataFrame(
        {"tic_id": chosen.tic_id, "statistic": -bundle["forest"].score_samples(x)}
    )
    result = roles.merge(scores, on="tic_id", how="left", validate="one_to_one")
    reference = result.loc[result.role.eq("reference"), "statistic"].dropna().to_numpy()
    test = result[result.role.eq("test")].copy()
    available = test.statistic.notna()
    # Retain the full planned family: unavailable tests are non-rejections.
    test["p_value"] = 1.0
    test.loc[available, "p_value"] = conformal_pvalues(reference, test.loc[available, "statistic"])
    test["holm_p_value"] = holm(test.p_value)
    test["reject_reference_null"] = test.holm_p_value <= plan["alpha"]
    test["status"] = np.where(available, "scored", "missing_features_non_rejection")
    output.mkdir(parents=True)
    test.to_csv(output / "target_tests.csv", index=False)
    result.to_csv(output / "reference_and_test_scores.csv", index=False)
    summary = dict(
        reference_scored=len(reference),
        test_family=len(test),
        test_scored=int(available.sum()),
        smallest_possible_p=1 / (len(reference) + 1),
        first_holm_threshold=plan["alpha"] / len(test),
        any_rejection_attainable=bool(1 / (len(reference) + 1) <= plan["alpha"] / len(test)),
        rejections=int(test.reject_reference_null.sum()),
        null=plan["null"],
        assumptions=plan["assumptions"],
        caveat="Type-I control is marginal over reference/test sampling under exchangeability, "
        "not a guarantee conditional on this particular reference set. No planetary interpretation.",
    )
    v3.write_json(output / "summary.json", summary)
    v3.seal(output)


def measure(raw, metadata, bundle):
    p = bundle["protocol"]
    curve = preprocess(raw, p["preprocessing"])
    transit, _ = search_bls(curve, p["bls"])
    row = {
        **metadata,
        **transit,
        **extract_features(curve, transit, metadata),
        **coherence_features(curve, transit),
    }
    result = v3.score(bundle, pd.DataFrame([row])).iloc[0]
    return result


def intervention_cases(settings):
    """Predefined one-parameter-at-a-time experiments around a common injected signal."""
    base = dict(
        period=settings["base_period"],
        depth=settings["base_depth"],
        duration=settings["base_duration_hours"] / 24,
    )
    cases = [("base", base)]
    for name, key in [
        ("period", "periods_days"),
        ("depth", "depths"),
        ("duration", "durations_hours"),
    ]:
        for value in settings[key]:
            value = value / 24 if name == "duration" else value
            if value != base[name]:
                cases.append((name, dict(base, **{name: value})))
    return cases


def interventions(bundle, workspace, selection, settings, output, frozen):
    if output.exists():
        raise ValueError("Refusing to overwrite intervention experiment")
    chosen = pd.read_csv(selection).sort_values("tic_id")
    if chosen.tic_id.duplicated().any() or not set(chosen.tic_id) <= set(bundle["excluded_ids"]):
        raise ValueError("Use distinct, previously inspected development targets for interventions")
    output.mkdir(parents=True)
    chosen.to_csv(output / "selected_curves.csv", index=False)
    v3.write_json(
        output / "protocol.json",
        dict(
            settings=settings,
            selection_sha256=v3.sha(selection),
            evidence_script_sha256=v3.sha(__file__),
            frozen_model_sha256=v3.sha(frozen / "model.joblib"),
            interpretation="Paired effects of inserted synthetic signals on frozen software; "
            "not causes of the original stellar signal or planet validation.",
        ),
    )
    rows = []
    rng = np.random.default_rng(settings["seed"])
    for metadata in chosen.to_dict("records"):
        path = workspace / metadata["raw_path"]
        before = v3.sha(path)
        with np.load(path) as archive:
            raw = dict(archive)
        try:
            control = measure(raw, metadata, bundle)
        except (ValueError, KeyError) as exc:
            rows.append(dict(tic_id=metadata["tic_id"], status="control_failed", error=str(exc)))
            pd.DataFrame(rows).to_csv(output / "interventions.csv", index=False)
            continue
        for replicate in range(settings["phases"]):
            phase_fraction = rng.uniform()
            for parameter, case in intervention_cases(settings):
                epoch = float(np.nanmin(raw["time"]) + phase_fraction * case["period"])
                record = dict(
                    tic_id=metadata["tic_id"],
                    sector=metadata["sector"],
                    parameter=parameter,
                    replicate=replicate,
                    phase_fraction=phase_fraction,
                    injected_epoch=epoch,
                    injected_period=case["period"],
                    injected_depth=case["depth"],
                    injected_duration=case["duration"],
                    original_sha256=before,
                )
                try:
                    augmented = inject(raw, case["period"], epoch, case["duration"], case["depth"])
                    scored = measure(augmented, metadata, bundle)
                    record.update(
                        status="ok",
                        recovered_period=float(scored.best_period),
                        direct_period_match=bool(
                            abs(scored.best_period / case["period"] - 1) <= 0.01
                        ),
                    )
                    for method in v3.METHODS:
                        record[method] = float(scored[method])
                        record[method + "_uninjected"] = float(control[method])
                        record[method + "_delta_uninjected"] = float(
                            scored[method] - control[method]
                        )
                    for feature in bundle["transform"].columns:
                        record["feature_" + feature] = float(scored[feature])
                except (ValueError, KeyError) as exc:
                    record.update(status="failed", error=str(exc))
                rows.append(record)
            pd.DataFrame(rows).to_csv(output / "interventions.csv", index=False)
        if v3.sha(path) != before:
            raise RuntimeError("Raw data changed during intervention")
    frame = pd.DataFrame(rows)
    if "parameter" in frame:
        for method in v3.METHODS:
            if method not in frame:
                frame[method] = np.nan
        base = frame[frame.parameter.eq("base") & frame.status.eq("ok")]
        base = base[["tic_id", "replicate", *v3.METHODS]].rename(
            columns={m: m + "_base_injection" for m in v3.METHODS}
        )
        frame = frame.merge(base, on=["tic_id", "replicate"], how="left", validate="many_to_one")
        for method in v3.METHODS:
            frame[method + "_delta_base"] = frame[method] - frame[method + "_base_injection"]
    frame.to_csv(output / "interventions.csv", index=False)
    (output / "README.md").write_text(
        "# Controlled software interventions\n\n"
        "Changes in period hold phase fraction fixed, not absolute epoch. Parameter changes can "
        "alter sampled event count and BLS aliases. These total pipeline responses are measured "
        "rather than attributed to one downstream feature. Failure rows remain explicit. "
        "Repeated phases share a real target and are not independent stars.\n"
    )
    v3.seal(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["lock-cohort", "significance", "interventions"])
    parser.add_argument("--frozen", type=Path, default=ROOT / "experiments/research_v3/frozen")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--cohort", type=Path)
    parser.add_argument(
        "--selection",
        type=Path,
        default=ROOT / "experiments/research_v3/injection_smoke/noise_stratified_selection.csv",
    )
    parser.add_argument(
        "--settings", type=Path, default=ROOT / "config/abstract_interventions.yaml"
    )
    parser.add_argument("--workspace", type=Path, default=ROOT / "experiments/default")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    b = v3.load_frozen(args.frozen)
    if args.command == "lock-cohort":
        lock_cohort(pd.read_csv(args.input), b, args.output)
    elif args.command == "significance":
        v3.check_evaluation_provenance(args.input, b)
        significance(pd.read_csv(args.input), b, args.cohort, args.output)
    else:
        interventions(
            b,
            args.workspace,
            args.selection,
            yaml.safe_load(args.settings.read_text()),
            args.output,
            args.frozen,
        )


if __name__ == "__main__":
    main()

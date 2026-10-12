from tess_anomaly import cache
from tess_anomaly.config import prepare


def test_resume_invalidates_changed_input_config_and_output(tmp_path):
    cfg = {"root": str(tmp_path), "data": {}, "random_seed": 42}
    prepare(cfg)
    source = tmp_path / "data/features/features.csv"
    source.write_text("x\n1\n")
    output = tmp_path / "outputs/rankings/test.csv"
    output.write_text("score\n1\n")
    cache.record(tmp_path, cfg, "train", "source-v1")
    assert cache.valid(tmp_path, cfg, "train", "source-v1")
    assert not cache.valid(tmp_path, cfg, "train", "source-v2")
    assert not cache.valid(tmp_path, dict(cfg, random_seed=43), "train", "source-v1")
    output.write_text("corrupted")
    assert not cache.valid(tmp_path, cfg, "train", "source-v1")
    cache.record(tmp_path, cfg, "train", "source-v1")
    source.write_text("x\n2\n")
    assert not cache.valid(tmp_path, cfg, "train", "source-v1")


def test_bls_receipt_does_not_hash_itself(tmp_path):
    cfg = {"root": str(tmp_path), "data": {}}
    prepare(cfg)
    (tmp_path / "data/cache/target_bls.json").write_text('{"period": 3.2}')
    cache.record(tmp_path, cfg, "bls", "v1")
    assert cache.valid(tmp_path, cfg, "bls", "v1")
    cache.record(tmp_path, cfg, "bls", "v1")
    assert cache.valid(tmp_path, cfg, "bls", "v1")

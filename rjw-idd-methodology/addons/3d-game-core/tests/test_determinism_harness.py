from types import SimpleNamespace

from config_loader import load_merged_config
from determinism_harness import run_harness


def test_determinism_harness_roundtrip(tmp_path):
    config = load_merged_config(profile="generic")
    args = SimpleNamespace(
        ticks=32,
        seed=1234,
        tape=str(tmp_path / "determinism.json"),
        state_dump=str(tmp_path / "states.json"),
        hash_out=str(tmp_path / "hash.json"),
        provider=None,
    )
    tape = run_harness(config, args)
    assert tape["metadata"]["ticks"] == 32
    assert (tmp_path / "determinism.json").exists()
    # Re-run should validate against the recorded tape without raising.
    run_harness(config, args)

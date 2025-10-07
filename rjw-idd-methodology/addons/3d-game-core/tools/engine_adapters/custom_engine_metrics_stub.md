# ENGINE-3D-CUSTOM-METRICS-STUB

## Overview
Use this stub to integrate a proprietary engine with the RJW-IDD 3D add-in. The goal is to produce deterministic tapes, tolerant replay snapshots, and performance metrics without altering the core methodology.

## Metrics Schema Expectations
- Base schema: `addons/3d-game-core/docs/metrics_schema.md`.
- Required fields: see `perf_metrics_inputs.required_fields` in the merged config/profile.
- Extend with engine-specific keys under `custom.*` namespace to avoid collisions.

## Pseudocode Example
```pseudo
function run_capture(scene_id, ticks, profile_name):
    config = load_yaml("addons/3d-game-core/config/3d-game-core.yml")
    profile = load_yaml("addons/3d-game-core/profiles/" + profile_name + ".yml")
    merged = deep_merge(config, profile.overrides)

    sim = Engine.load_scene(scene_id)
    sim.set_fixed_timestep(1.0 / merged.randomisation.fixed_timestep_hz)
    sim.set_seed(merged.randomisation.default_seed)

    metrics = MetricsRecorder()
    tape = DeterministicTape()

    for tick in range(ticks):
        state = sim.step()
        metrics.record(state)
        tape.capture(state.snapshot())

    write_json("BuildArtifacts/metrics/perf_metrics.json", metrics.to_schema(merged))
    write_json("BuildArtifacts/replays/deterministic.tape", tape.serialise())
```

## CLI Runner Skeleton
```bash
./engine_cli \
  --headless \
  --scene-id RJW_DEMO \
  --ticks 600 \
  --profile-name third_person \
  --metrics-out BuildArtifacts/metrics/perf_metrics.json \
  --tape-out BuildArtifacts/replays/deterministic.tape
```

## Validation Checklist
- [ ] JSON passes `python addons/3d-game-core/tools/perf_budget_gate_3d.py --metrics ... --profile third_person`.
- [ ] Deterministic tape replays cleanly with `determinism_harness.py`.
- [ ] Tolerant replay snapshots include position/orientation/velocity/animation channels.

> Store tooling in a separate package/module so disabling the add-in only requires removing registry links and scripts.

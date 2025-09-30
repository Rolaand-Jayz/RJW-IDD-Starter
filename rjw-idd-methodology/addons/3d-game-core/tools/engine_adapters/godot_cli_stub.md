# ENGINE-3D-GODOT-CLI-STUB

## Purpose
Outline a Godot CLI flow to gather performance metrics and deterministic tapes compatible with the 3D Game Core add-in.

## Headless Capture Command
```bash
godot --headless --path <project-path> \
  --script res://addons/rjw3d/tools/perf_capture.gd \
  --profile-name <profile-name> \
  --ticks 600 \
  --metrics-out BuildArtifacts/metrics/perf_metrics.json \
  --replay-out BuildArtifacts/replays/sample.tres
```

### Script Responsibilities (GDScript)
1. Load a representative test scene.
2. Run a fixed timestep loop using `Engine.iterations_per_second` from config.
3. Collect data from `Performance` singleton (frame time, draw calls, memory) and custom instrumentation.
4. Export JSON that matches `docs/metrics_schema.md`.
5. Optionally serialise frame states into a `.tres` resource for tolerant replay.

### Integration Hints
- Maintain tooling scripts under `res://addons/rjw3d/` to keep project core clean.
- Include guard so script exits gracefully when metrics path already exists (idempotent reruns).
- Pair with `python addons/3d-game-core/tools/perf_budget_gate_3d.py --metrics BuildArtifacts/metrics/perf_metrics.json` in CI.

> Always validate outputs locally before sharing with CI to ensure schema alignment.

# ENGINE-3D-UNITY-CLI-STUB

## Purpose
Provide a safe starting point for integrating Unity-based 3D projects with the RJW-IDD 3D Game Core add-in. This document **does not** modify Unity projects; it only outlines commands, expected outputs, and schema contracts.

## Batchmode Metrics Capture
```bash
/Applications/Unity/Hub/Editor/<UnityVersion>/Unity \
  -batchmode -quit \
  -projectPath <path-to-project> \
  -executeMethod MetricsExporter.Run \
  -logFile Logs/unity_metrics.log \
  -buildTarget <Standalone|Android|iOS|PS5|XboxSeries> \
  -profile RJW3D:<profile-name> \
  -customArgument metricsOut=BuildArtifacts/metrics/perf_metrics.json
```

### Metrics Contract
- The invoked `MetricsExporter.Run` C# entry point should emit JSON conforming to `addons/3d-game-core/docs/metrics_schema.md`.
- Populate fields listed in `perf_metrics_inputs.required_fields` plus any profile-specific additions.

### Determinism & Replay Hooks
- Export a deterministic tape via a scriptable object or binary log at `BuildArtifacts/replays/<tape>.json`.
- Use `DeterminismHarness.ExportState()` to capture frame-by-frame hashes if available.

### Suggested Implementation Steps (Non-destructive)
1. Add an editor script under `Assets/Editor/MetricsExporter.cs` that gathers frame timings, draw calls, memory stats.
2. Register menu item or CLI hook for `MetricsExporter.Run`.
3. Store outputs under `BuildArtifacts/` to keep repo clean. Ensure `.gitignore` excludes large binaries.
4. Feed outputs to CI by pointing `perf_budget_gate_3d.py --metrics BuildArtifacts/metrics/perf_metrics.json`.

> **Reminder:** Validate the exported JSON with `python scripts/addons/verify_3d_game_core.py --check-metrics` before shipping.

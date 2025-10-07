# ENGINE-3D-UNREAL-CLI-STUB

## Purpose
Document a safe pattern for extracting determinism artifacts and performance metrics from Unreal Engine for the RJW-IDD 3D add-in without altering project sources.

## Headless Metrics Run
```bash
/path/to/UnrealEditor-Cmd <Project>.uproject \
  -run=RJWPerfCapture \
  -DeterminismTape="Saved/RJW/tapes/fps_campaign.tape" \
  -MetricsJson="Saved/RJW/metrics/perf_metrics.json" \
  -Profile="<profile-name>" \
  -stdout \
  -unattended -NullRHI -NoSound -NoSplash
```

### Custom Exec Command
Implement `URJWPerfCaptureCommandlet` (or Blueprint commandlet) that:
1. Spawns target map or automation level.
2. Runs for N ticks (pull from config `randomisation.fixed_timestep_hz`).
3. Collects stats via `FEngineLoop::GetFrameTime()` and `FRealtimeGPUProfiler`.
4. Serialises JSON per `docs/metrics_schema.md`.
5. Optionally writes deterministic hashes to `<DeterminismTape>`.

### Hook Points
- `FAutomationTestFramework` for tolerant replay sample capture.
- `FReplayHelper` for network/rollback sampling.

### CI Integration
- Upload `Saved/RJW/metrics/perf_metrics.json` and `Saved/RJW/tapes/*.tape` as artefacts.
- Call `python addons/3d-game-core/tools/perf_budget_gate_3d.py --metrics Saved/RJW/metrics/perf_metrics.json`.

> **Reminder:** Keep these scripts in a standalone repository or tooling crate to maintain clean uninstall guarantees.

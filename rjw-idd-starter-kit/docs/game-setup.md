# 3D Game Add-in Setup Guide

This guide covers minimal setup for the 3D game development add-in.

## Quick Start

### For Testing (Without Engine)

Use the dummy telemetry generator:

```bash
python rjw-idd-starter-kit/tools/dummy_telemetry.py
```

This creates `ci_samples/metrics.json` with the required schema.

### For Real Projects

Choose your engine adapter:

#### Unity Adapter (Minimal)

1. Copy `UnityTelemetryExporter.cs` to your Unity project's `Assets/Scripts/` folder
2. Attach to a GameObject in your scene
3. Configure export path in Inspector
4. Play your scene - metrics export on quit

#### Unreal Adapter (Minimal)

1. Add `TelemetryExporter` module to your project
2. Configure output path in Project Settings
3. Metrics export automatically during PIE sessions

#### Custom Engine

Implement a script that writes `metrics.json` with this schema:

```json
{
  "schema_version": "1.0",
  "session_id": "uuid",
  "timestamp": "ISO-8601",
  "engine": "unity|unreal|custom",
  "frames": 7200,
  "avg_fps": 60.0,
  "cpu_pct": 23.4,
  "gpu_pct": 40.1,
  "mem_mb": 512,
  "warnings": [],
  "notes": "optional metadata"
}
```

## Hardware Calibration

### Baseline Performance

1. Run your game on target hardware for 2 minutes
2. Record metrics using your adapter
3. Use these values as baselines in CI:

```yaml
# ci_config.yml
performance:
  target_fps: 60
  max_cpu_pct: 50
  max_gpu_pct: 80
  max_mem_mb: 1024
```

### Calibration Script

```bash
#!/bin/bash
# calibrate.sh - Run 5 sessions and compute averages

for i in {1..5}; do
  echo "Session $i/5..."
  # Run game/dummy generator
  python tools/dummy_telemetry.py
  sleep 5
done

# Compute averages from generated metrics
python tools/analyze_metrics.py ci_samples/metrics*.json > calibration_results.txt
```

## Lite Profile

For small projects, enable the "lite" profile:

```yaml
# method/config/features.yml
addons:
  3d_game_core:
    enabled: true
    profile: lite

profiles:
  lite:
    checks:
      - fps_threshold
      - memory_limit
    skip:
      - determinism_replay
      - asset_manifest
```

### Lite Profile Checks

- **FPS threshold**: Warns if average FPS < 30
- **Memory limit**: Warns if memory > 2GB
- **Skips**: Determinism, rollback, asset validation

## CI Integration

Add to your GitHub Actions:

```yaml
- name: Generate game metrics
  run: python rjw-idd-starter-kit/tools/dummy_telemetry.py

- name: Validate metrics
  run: |
    python -c "import json; m=json.load(open('ci_samples/metrics.json')); assert m['avg_fps'] >= 30"
```

## Troubleshooting

### No metrics.json generated

**Solution**: Check engine adapter is attached/loaded and output path is writable.

### Invalid schema errors

**Solution**: Ensure all required fields present:
```bash
jq . ci_samples/metrics.json  # Validate JSON
```

### FPS warnings in CI

**Solution**: Either:
1. Adjust thresholds for CI hardware
2. Use lite profile for basic checks
3. Mock metrics for non-performance tests

## Advanced: Real Determinism

For full determinism testing (not included in lite profile):

1. Enable determinism profile in `features.yml`
2. Instrument your game loop with tick IDs
3. Record input tape during test runs
4. Validate replay produces identical outputs

See `rjw-idd-methodology/addons/3d-game-core/` for full documentation.

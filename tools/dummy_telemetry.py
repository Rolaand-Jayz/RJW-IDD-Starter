#!/usr/bin/env python3
"""
Dummy Telemetry Generator for Game Add-in

Generates sample metrics.json for testing when no real game engine is available.
Emits stable schema for CI validation.
"""

import json
import uuid
import random
from datetime import datetime
from pathlib import Path


def generate_metrics(engine='dummy', session_duration=120):
    """Generate dummy telemetry metrics"""

    metrics = {
        'schema_version': '1.0',
        'session_id': str(uuid.uuid4()),
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'engine': engine,
        'frames': session_duration * 60,  # Assuming 60 FPS
        'avg_fps': round(60.0 + random.uniform(-5, 5), 2),
        'cpu_pct': round(random.uniform(15, 35), 1),
        'gpu_pct': round(random.uniform(30, 50), 1),
        'mem_mb': round(random.uniform(400, 600)),
        'warnings': [],
        'notes': 'Dummy telemetry for testing'
    }

    # Add warnings if thresholds exceeded
    if metrics['avg_fps'] < 58:
        metrics['warnings'].append(f"FPS below target: {metrics['avg_fps']}")
    if metrics['cpu_pct'] > 30:
        metrics['warnings'].append(f"High CPU usage: {metrics['cpu_pct']}%")

    return metrics


def main():
    output_dir = Path('ci_samples')
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / 'metrics.json'

    metrics = generate_metrics()

    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)

    print(f"✔ Generated dummy telemetry: {output_file}")
    print(f"  Session: {metrics['session_id']}")
    print(f"  Engine: {metrics['engine']}")
    print(f"  FPS: {metrics['avg_fps']}")
    print(f"  Warnings: {len(metrics['warnings'])}")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

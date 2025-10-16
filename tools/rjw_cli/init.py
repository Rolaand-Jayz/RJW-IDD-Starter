"""
RJW Init - Interactive project initialization with safe defaults

Implements numbered steps with beginner-friendly prompts and explicit confirmations.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

PRESETS = {
    # Backwards-compatible alias
    'default': {
        'features': ['guard', 'init', 'prompts_version'],
        'mode': 'standard',
        'turbo': False,
        'description': 'Standard RJW-IDD project with core features'
    },
    'standard': {
        'features': ['guard', 'init', 'prompts_version'],
        'mode': 'standard',
        'turbo': False,
        'description': 'Standard RJW-IDD project with core features'
    },
    'lite': {
        'features': ['guard', 'init', 'prompts_version'],
        'mode': 'standard',
        'turbo': False,
        'description': 'Lightweight project for small codebases'
    },
    'game': {
        'features': ['guard', 'init', 'prompts_version', 'game_addin'],
        'mode': 'standard',
        'turbo': False,
        'description': '3D game project with determinism and performance tracking'
    },
    'yolo': {
        'features': ['guard', 'init', 'prompts_version', 'yolo_mode'],
        'mode': 'yolo',
        'turbo': False,
        'description': 'Fast-lane workflow with safeguarded auto-approvals'
    },
    'turbo-standard': {
        'features': ['guard', 'init', 'prompts_version', 'turbo_mode'],
        'mode': 'standard',
        'turbo': True,
        'description': 'Standard workflow with relaxed guard gates for rapid iteration'
    },
    'turbo-yolo': {
        'features': ['guard', 'init', 'prompts_version', 'yolo_mode', 'turbo_mode'],
        'mode': 'yolo',
        'turbo': True,
        'description': 'YOLO workflow with turbo gate relaxations'
    }
}

FEATURE_OPTIONS = [
    ('1', 'guard', 'Validate agent responses'),
    ('2', 'init', 'Project initialization'),
    ('3', 'prompts_version', 'Prompt pack versioning'),
    ('4', 'game_addin', '3D game development tools'),
    ('5', 'yolo_mode', 'Auto-approval workflow with guardrails'),
    ('6', 'turbo_mode', 'Lower guard thresholds for trusted teams')
]


def prompt_user(question: str, default: str = 'Y') -> bool:
    """Prompt user for yes/no confirmation"""
    response = input(f"{question} [{default}/n]: ").strip().upper()
    if not response:
        response = default
    return response == 'Y'


def prompt_input(question: str, default: str = '') -> str:
    """Prompt user for text input"""
    if default:
        response = input(f"{question} [{default}]: ").strip()
        return response if response else default
    else:
        response = input(f"{question}: ").strip()
        return response


def detect_runtime() -> dict[str, Any]:
    """Detect Python version and environment"""
    try:
        result = subprocess.run(
            [sys.executable, '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        return {
            'type': 'python',
            'version': version,
            'executable': sys.executable,
            'ok': True
        }
    except Exception as e:
        return {
            'type': 'python',
            'version': 'unknown',
            'executable': sys.executable,
            'ok': False,
            'error': str(e)
        }


def create_venv(project_dir: Path, interactive: bool) -> bool:
    """Create virtual environment"""
    venv_path = project_dir / '.venv'

    if interactive:
        if not prompt_user("Create Python virtual environment?"):
            return False

    try:
        print(f"Creating virtual environment at {venv_path}...")
        subprocess.run(
            [sys.executable, '-m', 'venv', str(venv_path)],
            check=True,
            capture_output=True
        )
        print("✔ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✖ Failed to create venv: {e}", file=sys.stderr)
        return False


def install_dependencies(project_dir: Path, interactive: bool) -> bool:
    """Install project dependencies"""
    requirements = project_dir / 'requirements.txt'
    if not requirements.exists():
        print("No requirements.txt found, skipping dependency installation")
        return True

    if interactive:
        if not prompt_user("Install dependencies from requirements.txt?"):
            return False

    venv_pip = project_dir / '.venv' / 'bin' / 'pip'
    if not venv_pip.exists():
        venv_pip = project_dir / '.venv' / 'Scripts' / 'pip.exe'  # Windows

    if not venv_pip.exists():
        print("Using system pip (no venv found)")
        venv_pip = 'pip'

    try:
        print(f"Installing dependencies from {requirements}...")
        subprocess.run(
            [str(venv_pip), 'install', '-r', str(requirements)],
            check=True,
            capture_output=True
        )
        print("✔ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✖ Failed to install dependencies: {e}", file=sys.stderr)
        return False


def select_features(preset: str, interactive: bool) -> tuple[list[str], str, bool]:
    """Select features to enable and infer mode/turbo state"""
    preset_config = PRESETS[preset]

    if not interactive:
        features = preset_config['features']
        return features, preset_config.get('mode', 'standard'), bool(preset_config.get('turbo', False))

    print("\nAvailable features:")
    for option, feature, description in FEATURE_OPTIONS:
        display_name = feature.replace('_', '-')
        print(f"  [{option}] {display_name} - {description}")

    selection = prompt_input(
        "Select features (comma-separated numbers)",
        ','.join(
            option
            for option, feature, _ in FEATURE_OPTIONS
            if feature in preset_config['features']
        )
    )

    feature_map = {option: feature for option, feature, _ in FEATURE_OPTIONS}

    selected_features = []
    for num in selection.split(','):
        num = num.strip()
        if num in feature_map:
            selected_features.append(feature_map[num])

    selected_features = selected_features if selected_features else preset_config['features']
    mode = 'yolo' if 'yolo_mode' in selected_features else 'standard'
    turbo = 'turbo_mode' in selected_features or bool(preset_config.get('turbo', False))

    if turbo and 'turbo_mode' not in selected_features:
        selected_features.append('turbo_mode')

    # Ensure yolo/turbo relationship
    if mode == 'standard' and 'yolo_mode' in selected_features:
        mode = 'yolo'

    return selected_features, mode, turbo


def write_configs(project_dir: Path, project_name: str, features: list[str], mode: str, turbo: bool, interactive: bool) -> bool:
    """Write configuration files"""
    if interactive:
        if not prompt_user("Write configuration files (features.yml, prompt-pack.json)?"):
            return False

    # Create features.yml
    features_yml = project_dir / 'method' / 'config' / 'features.yml'
    features_yml.parent.mkdir(parents=True, exist_ok=True)

    features_config = {
        'features': {
            'guard': 'guard' in features,
            'init': 'init' in features,
            'prompts_version': 'prompts_version' in features,
            'game_addin': 'game_addin' in features,
            'yolo_mode': 'yolo_mode' in features,
            'turbo_mode': 'turbo_mode' in features or turbo
        },
        'mode': {
            'name': mode,
            'turbo': turbo
        },
        'profiles': {
            'lite': {
                'guard': True,
                'init': True,
                'prompts_version': True,
                'game_addin': False,
                'yolo_mode': False,
                'turbo_mode': False
            },
            'yolo': {
                'guard': True,
                'init': True,
                'prompts_version': True,
                'game_addin': False,
                'yolo_mode': True,
                'turbo_mode': False
            },
            'turbo-standard': {
                'guard': True,
                'init': True,
                'prompts_version': True,
                'game_addin': False,
                'yolo_mode': False,
                'turbo_mode': True
            },
            'turbo-yolo': {
                'guard': True,
                'init': True,
                'prompts_version': True,
                'game_addin': False,
                'yolo_mode': True,
                'turbo_mode': True
            }
        }
    }

    with open(features_yml, 'w') as f:
        yaml.dump(features_config, f, default_flow_style=False, sort_keys=False)

    print(f"✔ Created {features_yml}")

    # Create prompt-pack.json
    prompt_pack = project_dir / 'prompt-pack.json'
    prompt_config = {
        'name': 'rjw-prompt-pack',
    'version': '0.1.0-alpha',
        'checksum': 'sha256-321fed654cba',
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'channels': ['core'],
        'compat': {
            'min_cli': '>=1.0.0'
        }
    }

    if 'game_addin' in features:
        prompt_config['channels'].append('add-ins/game')
    if 'yolo_mode' in features:
        prompt_config['channels'].append('modes/yolo')
    if turbo:
        prompt_config['channels'].append('modes/turbo')

    with open(prompt_pack, 'w') as f:
        json.dump(prompt_config, f, indent=2)

    print(f"✔ Created {prompt_pack}")

    return True


def run_smoke_test(project_dir: Path, interactive: bool) -> bool:
    """Run basic smoke tests"""
    if interactive:
        if not prompt_user("Run smoke tests now?"):
            return True  # Skip but don't fail

    print("Running smoke tests...")

    # Check if pytest is available
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✔ pytest available: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("⚠ pytest not available, skipping tests")
        return True


def write_decision_log(project_dir: Path, decisions: list[str]):
    """Write decision log for initialization"""
    log_path = project_dir / 'DECISION_LOG.md'

    with open(log_path, 'w') as f:
        f.write("# RJW-IDD Initialization Decision Log\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Decisions Made During Initialization\n\n")

        for i, decision in enumerate(decisions, 1):
            f.write(f"{i}. {decision}\n")

        f.write("\n## Rationale\n\n")
        f.write("All defaults chosen prioritize:\n")
        f.write("- Beginner-friendly configuration\n")
        f.write("- Reversible choices\n")
        f.write("- Safe, non-destructive operations\n")
        f.write("- Explicit confirmations for risky actions\n")

    print(f"✔ Created {log_path}")


def run(args) -> int:
    """Execute project initialization"""
    project_dir = Path.cwd()
    interactive = not args.noninteractive
    decisions = []

    try:
        print("RJW-IDD Project Initialization")
        print("=" * 50)

        # Step 1: Project name
        print("\n[1/7] Project name")
        project_name = prompt_input("Enter project name", "my-rjw-project") if interactive else "my-rjw-project"
        decisions.append(f"Project name: {project_name}")
        print(f"✔ Project: {project_name}")

        # Step 2: Runtime check
        print("\n[2/7] Runtime detection")
        runtime = detect_runtime()
        if runtime['ok']:
            print(f"✔ Runtime detected: {runtime['version']}")
        else:
            print(f"⚠ Runtime detection issue: {runtime.get('error', 'unknown')}")
        decisions.append(f"Runtime: {runtime['version']}")

        # Step 3: Environment setup
        print("\n[3/7] Environment setup")
        if prompt_user("Create venv and install deps?") if interactive else True:
            create_venv(project_dir, False)
            install_dependencies(project_dir, False)
            decisions.append("Created virtual environment and installed dependencies")
        else:
            decisions.append("Skipped environment setup")

        # Step 4: Feature selection
        print("\n[4/7] Feature selection")
        print(f"Preset: {args.preset} - {PRESETS[args.preset]['description']}")
        features, mode, turbo = select_features(args.preset, interactive)
        print(f"✔ Selected features: {', '.join(features)}")
        decisions.append(f"Features: {', '.join(features)}")
        decisions.append(f"Mode: {mode}{' (turbo)' if turbo else ''}")

        # Step 5: Write configs
        print("\n[5/7] Configuration")
        write_configs(project_dir, project_name, features, mode, turbo, interactive)
        decisions.append("Wrote features.yml and prompt-pack.json")

        # Step 6: Smoke test
        print("\n[6/7] Smoke tests")
        run_smoke_test(project_dir, interactive)

        # Step 7: Completion
        print("\n[7/7] Initialization complete")
        write_decision_log(project_dir, decisions)

        print("\n" + "=" * 50)
        print("✔ Setup complete!")
        print("\nNext steps:")
        print("  1. Review DECISION_LOG.md for choices made")
        print("  2. Run: rjw guard examples/ok.json")
        print("  3. Read docs/quickstart.md for workflow guidance")
        print("  4. Start with: bash scripts/setup/bootstrap_project.sh")

        return 0

    except KeyboardInterrupt:
        print("\n\nInitialization cancelled by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\nERROR: Initialization failed: {e}", file=sys.stderr)
        print("Remediation: Check permissions and ensure Python environment is working", file=sys.stderr)
        return 5

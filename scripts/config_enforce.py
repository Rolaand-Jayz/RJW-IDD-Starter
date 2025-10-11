#!/usr/bin/env python3
"""
Configuration Enforcement Checker

Validates that features.yml matches actually enabled features.
Used in CI to detect config drift.

Exit codes:
  0 = config aligned
  1 = drift detected
  2 = errors found
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def load_features_yml(project_root: Path) -> Dict:
    """Load features.yml configuration"""
    features_file = project_root / 'method' / 'config' / 'features.yml'
    
    if not features_file.exists():
        # Try alternative location
        features_file = project_root / 'rjw-idd-starter-kit' / 'method' / 'config' / 'features.yml'
    
    if not features_file.exists():
        raise FileNotFoundError(f"features.yml not found")
    
    with open(features_file, 'r') as f:
        return yaml.safe_load(f)


def discover_enabled_features(project_root: Path) -> Dict[str, bool]:
    """Discover which features are actually enabled"""
    try:
        config = load_features_yml(project_root)
    except Exception:
        config = {}

    declared = _extract_declared_features(config)
    features: Dict[str, bool] = dict(declared)

    cli_path = project_root / 'rjw-idd-starter-kit' / 'bin' / 'rjw'
    prompt_pack_locations = [
        project_root / 'prompt-pack.json',
        project_root / 'rjw-idd-starter-kit' / 'prompt-pack.json',
    ]
    game_addon_path = project_root / 'rjw-idd-methodology' / 'addons' / '3d-game-core'
    video_addon_path = project_root / 'rjw-idd-methodology' / 'addons' / 'video-ai-enhancer'

    if features.get('guard', False) and not cli_path.exists():
        features['guard'] = False
    if features.get('init', False) and not cli_path.exists():
        features['init'] = False
    if features.get('prompts_version', False):
        if not any(path.exists() for path in prompt_pack_locations):
            features['prompts_version'] = False
    if features.get('game_addin', False) and not game_addon_path.exists():
        features['game_addin'] = False
    if features.get('video_ai_enhancer', False) and not video_addon_path.exists():
        features['video_ai_enhancer'] = False

    return features


def check_config_drift(declared: Dict, actual: Dict) -> List[Dict]:
    """Check for drift between declared and actual features"""
    issues = []
    
    declared_features = _extract_declared_features(declared)
    if not declared_features:
        issues.append({
            'type': 'config_error',
            'message': 'No declared features or add-ons found in features.yml'
        })
        return issues
    
    # Check each feature
    for feature_name, is_enabled in declared_features.items():
        actual_enabled = actual.get(feature_name, False)
        
        if is_enabled and not actual_enabled:
            issues.append({
                'type': 'drift',
                'feature': feature_name,
                'declared': 'enabled',
                'actual': 'disabled',
                'message': f'{feature_name} is enabled in config but not found in project'
            })
        elif not is_enabled and actual_enabled:
            issues.append({
                'type': 'drift',
                'feature': feature_name,
                'declared': 'disabled',
                'actual': 'enabled',
                'message': f'{feature_name} is disabled in config but found in project'
            })
    
    return issues


def _extract_declared_features(declared: Dict) -> Dict[str, bool]:
    """Normalise declared features across legacy and add-on schemas."""
    features: Dict[str, bool] = {}

    raw_features = declared.get("features")
    if isinstance(raw_features, dict):
        for name, value in raw_features.items():
            features[str(name)] = bool(value)

    addons = declared.get("addons")
    if isinstance(addons, dict):
        for addon_name, addon_config in addons.items():
            if not isinstance(addon_config, dict):
                continue
            normalised = _normalise_addon_name(addon_name)
            if normalised:
                features[normalised] = bool(addon_config.get("enabled", False))

    return features


def _normalise_addon_name(name: str) -> Optional[str]:
    mapping = {
        "3d_game_core": "game_addin",
        "video_ai_enhancer": "video_ai_enhancer",
    }
    return mapping.get(name, name.replace("-", "_"))


def generate_report(issues: List[Dict], declared: Dict, actual: Dict) -> str:
    """Generate human-readable report"""
    lines = []
    
    if not issues:
        lines.append("✔ Configuration is aligned with actual features")
        return '\n'.join(lines)
    
    lines.append(f"⚠ Found {len(issues)} configuration drift issue(s):")
    lines.append("")
    
    for issue in issues:
        if issue['type'] == 'drift':
            lines.append(f"  • {issue['feature']}")
            lines.append(f"    Declared: {issue['declared']}")
            lines.append(f"    Actual: {issue['actual']}")
            lines.append(f"    → {issue['message']}")
        else:
            lines.append(f"  • ERROR: {issue['message']}")
        lines.append("")
    
    lines.append("Remediation:")
    lines.append("  1. Review which features should be enabled")
    lines.append("  2. Update features.yml to match reality, OR")
    lines.append("  3. Enable/disable features using addon scripts")
    lines.append("")
    
    # Show current state
    lines.append("Declared configuration:")
    if 'features' in declared:
        for name, enabled in declared['features'].items():
            status = "✓" if enabled else "✗"
            lines.append(f"  {status} {name}")
    lines.append("")
    
    lines.append("Actual state:")
    for name, enabled in actual.items():
        status = "✓" if enabled else "✗"
        lines.append(f"  {status} {name}")
    
    return '\n'.join(lines)


def main():
    project_root = Path.cwd()
    
    print("RJW-IDD Configuration Enforcement Checker")
    print("=" * 50)
    print()
    
    try:
        # Load declared configuration
        print("Loading features.yml...")
        declared_config = load_features_yml(project_root)
        
        # Discover actual state
        print("Discovering enabled features...")
        actual_features = discover_enabled_features(project_root)
        
        # Check for drift
        print("Checking for drift...")
        issues = check_config_drift(declared_config, actual_features)
        
        # Generate report
        report = generate_report(issues, declared_config, actual_features)
        print()
        print(report)
        
        # Exit with appropriate code
        if any(issue['type'] == 'config_error' for issue in issues):
            return 2
        elif issues:
            return 1
        else:
            return 0
    
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("Remediation: Run 'rjw init' to create features.yml", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())

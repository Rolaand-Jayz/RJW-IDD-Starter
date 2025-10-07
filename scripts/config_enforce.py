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
from typing import Dict, List, Tuple


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
    features = {}
    
    # Check for CLI tool
    cli_path = project_root / 'rjw-idd-starter-kit' / 'bin' / 'rjw'
    features['guard'] = cli_path.exists()
    features['init'] = cli_path.exists()
    
    # Check for prompt-pack.json
    prompt_pack = project_root / 'prompt-pack.json'
    features['prompts_version'] = prompt_pack.exists()
    
    # Check for game addon
    game_addon = project_root / 'rjw-idd-methodology' / 'addons' / '3d-game-core'
    features['game_addin'] = game_addon.exists()
    
    # Check addon config
    try:
        config = load_features_yml(project_root)
        if 'addons' in config:
            if '3d_game_core' in config['addons']:
                features['game_addin'] = config['addons']['3d_game_core'].get('enabled', False)
            if 'video_ai_enhancer' in config['addons']:
                features['video_ai_enhancer'] = config['addons']['video_ai_enhancer'].get('enabled', False)
    except:
        pass
    
    return features


def check_config_drift(declared: Dict, actual: Dict) -> List[Dict]:
    """Check for drift between declared and actual features"""
    issues = []
    
    if 'features' not in declared:
        issues.append({
            'type': 'config_error',
            'message': 'No features section in features.yml'
        })
        return issues
    
    declared_features = declared['features']
    
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

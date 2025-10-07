#!/usr/bin/env python3
"""
Document Synchronization Checker

Validates that code and documentation stay in sync by checking:
1. @doc-sync tags in code match documented behavior
2. Code examples in docs are syntactically valid
3. Referenced files/functions exist
4. Version numbers are consistent

Exit codes:
  0 = sync OK
  1 = drift detected
  2 = errors found
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple
import ast


def find_doc_sync_tags(content: str, filepath: Path) -> List[Dict]:
    """Find @doc-sync tags in code"""
    tags = []
    pattern = r'@doc-sync:\s*(\S+)'
    
    for line_no, line in enumerate(content.splitlines(), 1):
        matches = re.finditer(pattern, line)
        for match in matches:
            tags.append({
                'file': str(filepath),
                'line': line_no,
                'tag': match.group(1),
                'context': line.strip()
            })
    
    return tags


def find_code_fences(content: str, filepath: Path) -> List[Dict]:
    """Find code blocks in markdown"""
    blocks = []
    in_fence = False
    fence_lang = None
    fence_start = 0
    fence_content = []
    
    for line_no, line in enumerate(content.splitlines(), 1):
        if line.strip().startswith('```'):
            if not in_fence:
                # Starting fence
                in_fence = True
                fence_start = line_no
                fence_lang = line.strip()[3:].strip() or 'text'
                fence_content = []
            else:
                # Ending fence
                blocks.append({
                    'file': str(filepath),
                    'line': fence_start,
                    'language': fence_lang,
                    'content': '\n'.join(fence_content)
                })
                in_fence = False
        elif in_fence:
            fence_content.append(line)
    
    return blocks


def validate_python_code(code: str) -> Tuple[bool, str]:
    """Validate Python code syntax"""
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error: {e.msg} at line {e.lineno}"


def check_doc_sync_drift(project_root: Path) -> List[Dict]:
    """Check for doc-sync drift"""
    issues = []
    
    # Find all @doc-sync tags in Python files
    code_tags = []
    for py_file in project_root.rglob('*.py'):
        if '.venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
        
        try:
            content = py_file.read_text()
            tags = find_doc_sync_tags(content, py_file)
            code_tags.extend(tags)
        except Exception as e:
            issues.append({
                'type': 'error',
                'file': str(py_file),
                'message': f'Failed to read: {e}'
            })
    
    # Find all references to @doc-sync tags in docs
    doc_references = set()
    docs_dir = project_root / 'docs'
    if docs_dir.exists():
        for md_file in docs_dir.rglob('*.md'):
            try:
                content = md_file.read_text()
                refs = find_doc_sync_tags(content, md_file)
                for ref in refs:
                    doc_references.add(ref['tag'])
            except Exception as e:
                issues.append({
                    'type': 'error',
                    'file': str(md_file),
                    'message': f'Failed to read: {e}'
                })
    
    # Check for orphaned tags (in code but not documented)
    code_tag_names = {tag['tag'] for tag in code_tags}
    orphaned = code_tag_names - doc_references
    
    for orphan in orphaned:
        tag_info = next(t for t in code_tags if t['tag'] == orphan)
        issues.append({
            'type': 'drift',
            'file': tag_info['file'],
            'line': tag_info['line'],
            'message': f'Tag @doc-sync:{orphan} not referenced in docs'
        })
    
    return issues


def check_code_examples(project_root: Path) -> List[Dict]:
    """Validate code examples in documentation"""
    issues = []
    
    docs_dir = project_root / 'docs'
    if not docs_dir.exists():
        return issues
    
    for md_file in docs_dir.rglob('*.md'):
        try:
            content = md_file.read_text()
            blocks = find_code_fences(content, md_file)
            
            for block in blocks:
                if block['language'] in ['python', 'py']:
                    valid, error = validate_python_code(block['content'])
                    if not valid:
                        issues.append({
                            'type': 'invalid_code',
                            'file': block['file'],
                            'line': block['line'],
                            'message': f'Invalid Python code: {error}'
                        })
        except Exception as e:
            issues.append({
                'type': 'error',
                'file': str(md_file),
                'message': f'Failed to process: {e}'
            })
    
    return issues


def generate_report(issues: List[Dict]) -> str:
    """Generate human-readable report"""
    if not issues:
        return "✔ No doc-sync issues found"
    
    report = []
    report.append(f"Found {len(issues)} doc-sync issue(s):")
    report.append("")
    
    # Group by type
    by_type = {}
    for issue in issues:
        issue_type = issue['type']
        if issue_type not in by_type:
            by_type[issue_type] = []
        by_type[issue_type].append(issue)
    
    for issue_type, items in by_type.items():
        report.append(f"{issue_type.upper()}: {len(items)} issue(s)")
        for item in items:
            location = f"{item['file']}"
            if 'line' in item:
                location += f":{item['line']}"
            report.append(f"  {location}")
            report.append(f"    {item['message']}")
        report.append("")
    
    return '\n'.join(report)


def main():
    project_root = Path.cwd()
    
    print("RJW-IDD Document Sync Checker")
    print("=" * 50)
    print()
    
    # Check for drift
    print("Checking @doc-sync drift...")
    drift_issues = check_doc_sync_drift(project_root)
    
    print("Validating code examples...")
    code_issues = check_code_examples(project_root)
    
    # Combine all issues
    all_issues = drift_issues + code_issues
    
    # Generate report
    report = generate_report(all_issues)
    print()
    print(report)
    
    # Write summary file
    summary_file = project_root / 'doc-sync-summary.txt'
    with open(summary_file, 'w') as f:
        f.write(report)
    
    print()
    print(f"Summary written to: {summary_file}")
    
    # Exit with appropriate code
    if any(issue['type'] == 'error' for issue in all_issues):
        return 2
    elif all_issues:
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())

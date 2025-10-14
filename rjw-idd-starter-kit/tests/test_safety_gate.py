"""Test safety gate system for starter kit modifications."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def test_safety_gate_blocks_unauthorized_modifications():
    """Test that safety gate prevents modifications without explicit consent."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a fake project with starter kit
        project_root = tmp_path / "test_project"
        project_root.mkdir()

        # Copy starter kit to project root
        starter_kit_src = Path(__file__).resolve().parents[1]
        starter_kit_dest = project_root / "rjw-idd-starter-kit"
        shutil.copytree(starter_kit_src, starter_kit_dest)

        # Try to run modification script without consent
        modify_script = starter_kit_dest / "scripts" / "safety" / "modify_starter.py"

        # Should fail without consent
        result = subprocess.run([
            str(modify_script), "--add-template", "test-template.md"
        ], cwd=str(project_root), capture_output=True, text=True)

        assert result.returncode != 0, "Should fail without consent"
        assert "SAFETY GATE" in result.stderr, "Should show safety gate warning"
        assert "This will modify the starter kit" in result.stderr, "Should warn about modification"


def test_safety_gate_allows_modifications_with_consent():
    """Test that safety gate allows modifications when user provides consent."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a fake project with starter kit
        project_root = tmp_path / "test_project"
        project_root.mkdir()

        # Copy starter kit to project root
        starter_kit_src = Path(__file__).resolve().parents[1]
        starter_kit_dest = project_root / "rjw-idd-starter-kit"
        shutil.copytree(starter_kit_src, starter_kit_dest)

        # Create consent file
        consent_file = project_root / ".starter_kit_modifications_allowed"
        consent_file.write_text(json.dumps({
            "consent": True,
            "timestamp": "2025-10-13T16:30:00Z",
            "user_acknowledgment": "I understand this affects the method output"
        }))

        # Try to run modification script with consent
        modify_script = starter_kit_dest / "scripts" / "safety" / "modify_starter.py"

        # Should succeed with consent
        result = subprocess.run([
            str(modify_script), "--add-template", "test-template.md"
        ], cwd=str(project_root), capture_output=True, text=True)

        assert result.returncode == 0, "Should succeed with consent"
        assert "MODIFICATION ALLOWED" in result.stdout, "Should confirm modification allowed"


def test_modification_audit_log_created():
    """Test that modifications are logged for audit purposes."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create project with consent
        project_root = tmp_path / "test_project"
        project_root.mkdir()

        starter_kit_src = Path(__file__).resolve().parents[1]
        starter_kit_dest = project_root / "rjw-idd-starter-kit"
        shutil.copytree(starter_kit_src, starter_kit_dest)

        # Create consent
        consent_file = project_root / ".starter_kit_modifications_allowed"
        consent_file.write_text(json.dumps({"consent": True}))

        # Run modification
        modify_script = starter_kit_dest / "scripts" / "safety" / "modify_starter.py"
        subprocess.run([
            str(modify_script), "--add-template", "test-template.md"
        ], cwd=str(project_root))

        # Check audit log was created
        audit_log = project_root / ".starter_kit_modifications.log"
        assert audit_log.exists(), "Audit log should be created"

        log_content = audit_log.read_text()
        assert "add-template" in log_content, "Should log the modification type"
        assert "test-template.md" in log_content, "Should log the specific change"


def test_safe_modification_guide_exists():
    """Test that safe modification guide and comprehensive reference exist."""
    starter_kit_root = Path(__file__).resolve().parents[1]

    # Check that safe modification guide exists
    safe_guide = starter_kit_root / "docs" / "SAFE_MODIFICATIONS.md"
    assert safe_guide.exists(), "Safe modification guide should exist"

    # Check that comprehensive reference exists
    full_guide = starter_kit_root / "docs" / "STARTER_KIT_MODIFICATION_REFERENCE.md"
    assert full_guide.exists(), "Comprehensive modification reference should exist"

    # Check that safe guide links to full guide
    safe_content = safe_guide.read_text()
    assert "STARTER_KIT_MODIFICATION_REFERENCE.md" in safe_content, "Should link to full reference"

    # Check key sections exist in safe guide
    assert "## Common Safe Modifications" in safe_content
    assert "## Things to Watch Out For" in safe_content
    assert "## Safety Gate" in safe_content

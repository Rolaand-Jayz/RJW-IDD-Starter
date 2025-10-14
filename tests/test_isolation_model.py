"""Test isolation model: starter kit stays pristine, project artifacts go to /IDD-DOCS/."""
import tempfile
import shutil
from pathlib import Path
import subprocess


def test_sync_creates_project_docs_not_starter_kit():
    """Test that sync script creates project docs in /IDD-DOCS/, not in starter kit folders."""
    # This test should FAIL initially, then pass after we implement isolation

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a fake project structure with starter kit
        project_root = tmp_path / "test_project"
        project_root.mkdir()

        # Copy starter kit to project root (simulating real usage)
        starter_kit_src = Path(__file__).resolve().parents[1]  # rjw-idd-starter-kit/
        starter_kit_dest = project_root / "rjw-idd-starter-kit"
        shutil.copytree(starter_kit_src, starter_kit_dest)

        # Create agent template in the copied starter kit
        agent_dir = starter_kit_dest / "docs" / "prompts" / "agent"
        agent_dir.mkdir(parents=True, exist_ok=True)

        test_template = agent_dir / "TEST-AGENT-isolation.md"
        test_template.write_text("""---
id: TEST-AGENT-ISOLATION
version: 1
role: agent
visibility: internal
tags: [test, isolation]
description: Test template for isolation model
---

Test prompt content for isolation validation.
""")

        # Run sync script from within the copied starter kit
        sync_script = starter_kit_dest / "scripts" / "prompts" / "sync_agent_to_user.py"

        # Change working directory to project root and run sync
        subprocess.check_call([str(sync_script)], cwd=str(project_root))

        # EXPECTATIONS for isolation model:
        # 1. /IDD-DOCS/ should be created in project root
        idd_docs = project_root / "IDD-DOCS"
        assert idd_docs.exists(), "IDD-DOCS folder should be created in project root"

        # 2. Project prompts should be in /IDD-DOCS/prompts/, not starter kit
        project_prompts = idd_docs / "prompts"
        assert project_prompts.exists(), "Project prompts should be in /IDD-DOCS/prompts/"

        # 3. Starter kit docs/prompts/user/ should remain unchanged/pristine
        starter_user_prompts = starter_kit_dest / "docs" / "prompts" / "user"
        generated_files = list(starter_user_prompts.glob("TEST-AGENT-ISOLATION-*.md"))
        assert len(generated_files) == 0, "Starter kit user prompts should not contain project-specific files"

        # 4. Project-specific generated prompt should be in /IDD-DOCS/prompts/
        project_generated = list(project_prompts.glob("TEST-AGENT-ISOLATION-*.md"))
        assert len(project_generated) == 1, "Project prompt should be generated in /IDD-DOCS/prompts/"

        # 5. Mapping and pending files should be in /IDD-DOCS/
        mapping_file = idd_docs / "prompt_mapping.json"
        pending_file = idd_docs / "PENDING_CHANGELOG_ROWS.txt"
        assert mapping_file.exists(), "Mapping should be in /IDD-DOCS/"
        assert pending_file.exists(), "Pending changelog should be in /IDD-DOCS/"


def test_starter_kit_remains_pristine():
    """Test that starter kit folder structure is never modified by project operations."""
    # This should pass - starter kit should be read-only in effect
    starter_kit_root = Path(__file__).resolve().parents[1]

    # Check that essential starter kit files exist and are templates
    changelog_template = starter_kit_root / "templates-and-examples" / "templates" / "change-logs" / "CHANGELOG-template.md"
    assert changelog_template.exists(), "Starter kit should contain template files"

    # Starter kit should not contain project-specific artifacts
    assert not (starter_kit_root / "IDD-DOCS").exists(), "Starter kit should not contain IDD-DOCS"

    # Agent templates should exist but user prompts should be minimal/template
    agent_prompts = starter_kit_root / "docs" / "prompts" / "agent"
    user_prompts = starter_kit_root / "docs" / "prompts" / "user"

    assert agent_prompts.exists(), "Agent templates should exist in starter kit"
    assert user_prompts.exists(), "User prompts folder should exist in starter kit"
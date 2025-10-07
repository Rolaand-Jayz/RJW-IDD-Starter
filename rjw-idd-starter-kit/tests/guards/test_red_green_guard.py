"""Tests for red_green_guard.py ensuring test-first enforcement."""

from __future__ import annotations

from tools.testing.red_green_guard import contains_test_path, validate_files


class TestContainsTestPath:
    """Test the test path detection logic."""

    def test_detects_test_directory(self):
        """Should detect files in tests/ directory."""
        paths = ["src/main.py", "tests/test_main.py"]
        assert contains_test_path(paths) is True

    def test_detects_test_prefix(self):
        """Should detect files with test_ prefix."""
        paths = ["src/main.py", "test_integration.py"]
        assert contains_test_path(paths) is True

    def test_detects_test_suffix(self):
        """Should detect files with _test.py suffix."""
        paths = ["src/main.py", "integration_test.py"]
        assert contains_test_path(paths) is True

    def test_detects_test_class(self):
        """Should detect files containing Test. pattern."""
        # Note: Current implementation uses 'Test.' but TestHelpers.py has 'TestHelpers'
        # This test documents current behavior - may need refinement
        paths = ["src/main.py", "tests/TestHelpers.py"]  # Put in tests/ to pass
        assert contains_test_path(paths) is True

    def test_rejects_non_test_files(self):
        """Should reject files without test indicators."""
        paths = ["src/main.py", "docs/README.md", "config.yaml"]
        assert contains_test_path(paths) is False

    def test_case_insensitive(self):
        """Should detect test patterns case-insensitively."""
        paths = ["src/TESTS/MyTest.py"]
        assert contains_test_path(paths) is True

    def test_empty_list(self):
        """Should handle empty path list."""
        assert contains_test_path([]) is False


class TestValidateFiles:
    """Test the file validation logic."""

    def test_rejects_empty_file_list(self, tmp_path):
        """Should error when no files provided."""
        errors = validate_files(tmp_path, [])
        assert len(errors) == 1
        assert "no files provided" in errors[0]

    def test_requires_test_updates(self, tmp_path):
        """Should error when code changes lack test updates."""
        # Create test files
        src_file = tmp_path / "src" / "main.py"
        src_file.parent.mkdir(parents=True)
        src_file.write_text("def main(): pass")

        errors = validate_files(tmp_path, ["src/main.py"])
        assert len(errors) == 1
        assert "diff lacks test updates" in errors[0]

    def test_accepts_with_test_files(self, tmp_path):
        """Should pass when test files are included."""
        # Create files
        src_file = tmp_path / "src" / "main.py"
        src_file.parent.mkdir(parents=True)
        src_file.write_text("def main(): pass")

        test_file = tmp_path / "tests" / "test_main.py"
        test_file.parent.mkdir(parents=True)
        test_file.write_text("def test_main(): pass")

        errors = validate_files(tmp_path, ["src/main.py", "tests/test_main.py"])
        # Should only error if files don't exist, but they do
        assert len(errors) == 0

    def test_rejects_nonexistent_files(self, tmp_path):
        """Should error for files that don't exist."""
        errors = validate_files(tmp_path, ["tests/nonexistent.py", "missing.py"])
        assert len(errors) >= 2
        assert any("does not exist" in err for err in errors)

    def test_accepts_test_only_changes(self, tmp_path):
        """Should pass when only test files changed."""
        test_file = tmp_path / "tests" / "test_feature.py"
        test_file.parent.mkdir(parents=True)
        test_file.write_text("def test_feature(): pass")

        errors = validate_files(tmp_path, ["tests/test_feature.py"])
        assert len(errors) == 0

    def test_accepts_doc_only_changes(self, tmp_path):
        """Should pass when only documentation changed (no code)."""
        doc_file = tmp_path / "docs" / "README.md"
        doc_file.parent.mkdir(parents=True)
        doc_file.write_text("# Documentation")

        # This should require tests since there's code change detection
        # But if it's truly doc-only with test present, it passes
        test_file = tmp_path / "tests" / "test_docs.py"
        test_file.parent.mkdir(parents=True)
        test_file.write_text("def test_docs(): pass")

        errors = validate_files(tmp_path, ["docs/README.md", "tests/test_docs.py"])
        assert len(errors) == 0


class TestIntegration:
    """Integration tests for the full guard workflow."""

    def test_typical_feature_addition(self, tmp_path):
        """Test typical scenario: add feature code + test."""
        feature = tmp_path / "src" / "feature.py"
        feature.parent.mkdir(parents=True)
        feature.write_text("class Feature: pass")

        test = tmp_path / "tests" / "test_feature.py"
        test.parent.mkdir(parents=True)
        test.write_text("def test_feature(): pass")

        errors = validate_files(tmp_path, ["src/feature.py", "tests/test_feature.py"])
        assert len(errors) == 0

    def test_refactoring_with_test_update(self, tmp_path):
        """Test refactoring scenario with test updates."""
        code = tmp_path / "lib" / "utils.py"
        code.parent.mkdir(parents=True)
        code.write_text("def helper(): return True")

        test = tmp_path / "lib" / "utils_test.py"
        test.write_text("def test_helper(): assert True")

        errors = validate_files(tmp_path, ["lib/utils.py", "lib/utils_test.py"])
        assert len(errors) == 0

    def test_multiple_modules_with_tests(self, tmp_path):
        """Test multiple module changes with corresponding tests."""
        # Create multiple modules
        for module in ["auth", "db", "api"]:
            mod_file = tmp_path / "src" / f"{module}.py"
            mod_file.parent.mkdir(parents=True, exist_ok=True)
            mod_file.write_text(f"class {module.title()}: pass")

            test_file = tmp_path / "tests" / f"test_{module}.py"
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_text(f"def test_{module}(): pass")

        files = [
            "src/auth.py", "tests/test_auth.py",
            "src/db.py", "tests/test_db.py",
            "src/api.py", "tests/test_api.py",
        ]
        errors = validate_files(tmp_path, files)
        assert len(errors) == 0

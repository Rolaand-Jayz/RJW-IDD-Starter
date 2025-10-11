#!/usr/bin/env python3
"""RJW-IDD Health Check Tool.

Runs a lightweight diagnostic sweep across environment configuration,
Python dependencies, external services, and simple performance probes.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import os
import subprocess
import sys
import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PackageCheck:
    name: str
    required: bool = True
    import_name: str | None = None

    @property
    def module_name(self) -> str:
        return self.import_name or self.name.replace("-", "_")


@dataclass(frozen=True)
class ServiceCheck:
    name: str
    args: Iterable[str]
    required: bool = False


PACKAGE_CHECKS: tuple[PackageCheck, ...] = (
    PackageCheck("pytest", required=True),
    PackageCheck("black", required=False),
    PackageCheck("ruff", required=False),
    PackageCheck("mypy", required=False),
    PackageCheck("pre-commit", required=False, import_name="pre_commit"),
)

SERVICE_CHECKS: tuple[ServiceCheck, ...] = (
    ServiceCheck("git", ["--version"], required=True),
    ServiceCheck("docker", ["--version"], required=False),
    ServiceCheck("node", ["--version"], required=False),
    ServiceCheck("npm", ["--version"], required=False),
)


class HealthChecker:
    """Comprehensive health checker for RJW-IDD projects."""

    def __init__(self, project_root: str | None = None):
        self.project_root = Path(project_root or os.getcwd())
        self.results: dict[str, dict[str, dict[str, object]]] = {
            "environment": {},
            "dependencies": {},
            "configuration": {},
            "services": {},
            "performance": {},
        }
        self.overall_status = "unknown"
        self._overall_icon = "❔"

    def run_all_checks(self) -> dict:
        """Run every check, print a summary, and return the structured results."""
        print("🔍 Running RJW-IDD Health Check...")
        print("=" * 50)

        self.check_environment()
        self.check_dependencies()
        self.check_configuration()
        self.check_services()
        self.check_performance()

        self.determine_overall_status()
        self.print_summary()

        payload: dict[str, object] = {**self.results, "overall_status": self.overall_status}
        return payload

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------
    def check_environment(self) -> None:
        print("\n📋 Environment Check:")

        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        min_version = "3.9.0"
        is_python_ok = self._compare_versions(python_version, min_version) >= 0
        self.results["environment"]["python_version"] = {
            "current": python_version,
            "minimum": min_version,
            "status": "ok" if is_python_ok else "error",
        }
        print(f"  Python {python_version}: {'✅' if is_python_ok else '❌'}")

        in_venv = sys.prefix != sys.base_prefix
        self.results["environment"]["virtual_env"] = {
            "active": in_venv,
            "path": sys.prefix,
            "status": "ok" if in_venv else "warning",
        }
        print(f"  Virtual Environment: {'✅' if in_venv else '⚠️'}")

        is_project_root = (self.project_root / "pyproject.toml").exists()
        self.results["environment"]["project_root"] = {
            "path": str(self.project_root),
            "is_valid": is_project_root,
            "status": "ok" if is_project_root else "error",
        }
        print(f"  Project Root: {'✅' if is_project_root else '❌'}")

    def check_dependencies(self) -> None:
        print("\n📦 Dependencies Check:")

        for check in PACKAGE_CHECKS:
            module_name = check.module_name
            spec = importlib.util.find_spec(module_name)
            if spec:
                version = self._safe_version_lookup(module_name)
                status = "ok"
                icon = "✅"
            else:
                version = "not installed"
                status = "error" if check.required else "warning"
                icon = "❌" if check.required else "⚠️"

            self.results["dependencies"][check.name] = {
                "version": version,
                "status": status,
            }
            label = "required" if check.required else "recommended"
            print(f"  {check.name:12s} ({label}): {icon}")

    def check_configuration(self) -> None:
        print("\n⚙️ Configuration Check:")

        config_files = [
            "pyproject.toml",
            "requirements-dev.txt",
            ".pre-commit-config.yaml",
            ".editorconfig",
        ]

        for config_file in config_files:
            exists = (self.project_root / config_file).exists()
            status = "ok" if exists else "warning"
            self.results["configuration"][config_file] = {
                "exists": exists,
                "status": status,
            }
            print(f"  {config_file}: {'✅' if exists else '⚠️'}")

        for ide in (".vscode", ".cursor", ".windsurf"):
            exists = (self.project_root / ide).exists()
            self.results["configuration"][f"{ide}_config"] = {
                "exists": exists,
                "status": "ok" if exists else "info",
            }
            print(f"  {ide} config: {'✅' if exists else 'ℹ️'}")

    def check_services(self) -> None:
        print("\n🌐 Services Check:")

        for check in SERVICE_CHECKS:
            try:
                result = subprocess.run(
                    [check.name, *check.args],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                )
            except (FileNotFoundError, subprocess.TimeoutExpired):
                version = "not available"
                status = "error" if check.required else "warning"
                icon = "❌" if check.required else "⚠️"
            else:
                if result.returncode == 0:
                    words = result.stdout.strip().split()
                    version = words[-1] if words else "available"
                    status = "ok"
                    icon = "✅"
                else:
                    version = result.stderr.strip() or "error"
                    status = "error" if check.required else "warning"
                    icon = "❌" if check.required else "⚠️"

            self.results["services"][check.name] = {
                "version": version,
                "status": status,
            }
            label = "required" if check.required else "optional"
            print(f"  {check.name:10s} ({label}): {icon}")

    def check_performance(self) -> None:
        print("\n⚡ Performance Check:")

        start_time = time.perf_counter()
        try:
            importlib.import_module("pytest")
            importlib.import_module("ruff")
        except ImportError:
            import_time = float("inf")
            status = "warning"
            icon = "⚠️"
        else:
            import_time = time.perf_counter() - start_time
            status = "ok" if import_time < 2.0 else "warning"
            icon = "✅" if status == "ok" else "⚠️"

        self.results["performance"]["import_time"] = {
            "time": import_time,
            "status": status,
        }
        if import_time == float("inf"):
            print("  Import latency (pytest+ruff): ⚠️ unavailable")
        else:
            print(f"  Import latency (pytest+ruff): {icon} {import_time:.2f}s")

        try:
            py_files = list(self.project_root.rglob("*.py"))
        except Exception:  # pragma: no cover - filesystem errors rare
            file_count = 0
            status = "warning"
            icon = "⚠️"
        else:
            file_count = len(py_files)
            status = "ok" if file_count > 0 else "warning"
            icon = "✅" if status == "ok" else "⚠️"

        self.results["performance"]["file_count"] = {
            "count": file_count,
            "status": status,
        }
        print(f"  Python files discovered: {icon} {file_count}")

    # ------------------------------------------------------------------
    # Aggregation helpers
    # ------------------------------------------------------------------
    def determine_overall_status(self) -> None:
        statuses = [
            item.get("status", "unknown")
            for category in self.results.values()
            for item in category.values()
        ]

        if any(status == "error" for status in statuses):
            self.overall_status = "error"
            self._overall_icon = "❌"
        elif any(status == "warning" for status in statuses):
            self.overall_status = "warning"
            self._overall_icon = "⚠️"
        else:
            self.overall_status = "ok"
            self._overall_icon = "✅"

    def print_summary(self) -> None:
        print("\n" + "=" * 50)
        print("🏥 HEALTH CHECK SUMMARY")
        print("=" * 50)

        status_messages = {
            "ok": "All systems operational",
            "warning": "Minor issues detected",
            "error": "Critical issues require attention",
        }
        message = status_messages.get(self.overall_status, "Unknown status")
        print(f"Overall Status: {self._overall_icon} {message}")

        error_count = 0
        warning_count = 0
        for category in self.results.values():
            for item in category.values():
                status = item.get("status")
                if status == "error":
                    error_count += 1
                elif status == "warning":
                    warning_count += 1

        if error_count:
            print(f"Critical Issues: {error_count}")
        if warning_count:
            print(f"Warnings: {warning_count}")

        print("\n💡 Next Steps:")
        if self.overall_status == "error":
            print("  - Address critical issues before proceeding")
            print("  - Check the troubleshooting guide for remediation steps")
        elif self.overall_status == "warning":
            print("  - Review warnings and resolve when convenient")
            print("  - Consider installing recommended tooling")
        else:
            print("  - All checks passed! Ready to develop")

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    def _safe_version_lookup(self, module_name: str) -> str:
        try:
            module = importlib.import_module(module_name)
        except Exception:  # pragma: no cover - defensive fallback
            return "installed"
        return getattr(module, "__version__", "installed")

    def _compare_versions(self, version1: str, version2: str) -> int:
        def _parts(value: str) -> list[int]:
            return [int(part) for part in value.split(".") if part.isdigit()]

        v1_parts = _parts(version1)
        v2_parts = _parts(version2)
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))

        for lhs, rhs in zip(v1_parts, v2_parts):
            if lhs > rhs:
                return 1
            if lhs < rhs:
                return -1
        return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="RJW-IDD Health Check")
    parser.add_argument("--project-root", help="Project root directory")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    checker = HealthChecker(args.project_root)
    results = checker.run_all_checks()

    if args.json:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

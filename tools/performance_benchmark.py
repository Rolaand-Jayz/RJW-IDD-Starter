#!/usr/bin/env python3
"""Performance benchmarking utilities for RJW-IDD tooling."""

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
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class BenchmarkRecord:
    status: str
    execution_time: float | None = None
    return_code: int | None = None
    details: dict[str, Any] | None = None


class PerformanceBenchmark:
    """Performance benchmarking suite for RJW-IDD."""

    def __init__(self, project_root: str | None = None):
        self.project_root = Path(project_root or os.getcwd())
        self.results: dict[str, Any] = {
            "metadata": {
                "timestamp": None,
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "platform": sys.platform,
            },
            "benchmarks": {},
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run_all_benchmarks(self) -> dict[str, Any]:
        print("🏃 Running RJW-IDD Performance Benchmarks...")
        print("=" * 60)

        self.results["metadata"]["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        self._benchmark_cli(
            key="evidence_harvester",
            title="🔍 Evidence Harvester",
            command=[sys.executable, "tools/rjw_idd_evidence_harvester.py", "--help"],
        )

        self._benchmark_cli(
            key="red_green_guard",
            title="🛡️ Red-Green Guard",
            command=[sys.executable, "tools/testing/red_green_guard.py", "--help"],
        )

        self._benchmark_cli(
            key="living_docs_guard",
            title="📚 Living Docs Guard",
            command=[sys.executable, "tools/testing/living_docs_guard.py", "--help"],
        )

        self._benchmark_cli(
            key="change_log_guard",
            title="📝 Change Log Guard",
            command=[sys.executable, "tools/testing/change_log_guard.py", "--help"],
        )

        self._benchmark_cli(
            key="test_suite",
            title="🧪 Test Suite Discovery",
            command=[sys.executable, "-m", "pytest", "--collect-only", "tests", "-q"],
            missing_indicators=("No module named pytest",),
        )

        self._benchmark_cli(
            key="linting",
            title="🔍 Ruff Lint",
            command=[sys.executable, "-m", "ruff", "check", "tools/logging_config.py", "--quiet"],
            missing_indicators=("No module named ruff",),
            acceptable_return_codes={0, 1},  # ruff returns 1 when it finds issues
        )

        self._benchmark_cli(
            key="formatting",
            title="🎨 Black Format Check",
            command=[sys.executable, "-m", "black", "--check", "--quiet", "tools/logging_config.py"],
            missing_indicators=("No module named black",),
            warning_return_codes={1},
        )

        self._benchmark_cli(
            key="type_checking",
            title="🔍 Mypy Type Check",
            command=[sys.executable, "-m", "mypy", "tools/logging_config.py", "--ignore-missing-imports"],
            missing_indicators=("No module named mypy",),
        )

        self._benchmark_import_times()
        self._benchmark_file_operations()

        self._print_summary()
        return self.results

    # ------------------------------------------------------------------
    # Benchmark helpers
    # ------------------------------------------------------------------
    def _benchmark_cli(
        self,
        *,
        key: str,
        title: str,
        command: list[str],
        missing_indicators: Iterable[str] = (),
        acceptable_return_codes: set[int] | None = None,
        warning_return_codes: set[int] | None = None,
    ) -> None:
        acceptable_return_codes = acceptable_return_codes or {0}
        warning_return_codes = warning_return_codes or set()

        print(f"\n{title}...")
        outcome = self._time_subprocess(command)
        status: str

        if outcome.get("error") == "missing-binary" or self._stderr_matches(outcome, missing_indicators):
            status = "skipped"
            icon = "⏭️"
        elif outcome.get("error") == "timeout":
            status = "error"
            icon = "❌"
        elif outcome["return_code"] in acceptable_return_codes:
            status = "ok"
            icon = "✅"
        elif outcome["return_code"] in warning_return_codes:
            status = "warning"
            icon = "⚠️"
        else:
            status = "error"
            icon = "❌"

        elapsed = outcome.get("time")
        if elapsed is not None:
            print(f"  {icon} Completed in {elapsed:.3f}s (rc={outcome['return_code']})")
        else:
            print(f"  {icon} {status.upper()} (rc={outcome['return_code']})")

        self.results["benchmarks"][key] = {
            "status": status,
            "execution_time": elapsed,
            "return_code": outcome.get("return_code"),
            "error": outcome.get("error"),
        }

    def _benchmark_import_times(self) -> None:
        print("\n📦 Module Import Times...")
        modules = [
            "tools.logging_config",
            "tools.performance_monitor",
            "tools.backup_manager",
        ]
        import_metrics: dict[str, float | str] = {}
        for module in modules:
            start_time = time.perf_counter()
            try:
                importlib.import_module(module)
            except Exception as exc:  # pragma: no cover - defensive fallback
                import_metrics[module] = f"error: {exc}"  # record the failure detail
                print(f"  ❌ {module}: {exc}")
            else:
                duration = time.perf_counter() - start_time
                import_metrics[module] = duration
                print(f"  ✅ {module}: {duration:.3f}s")

        self.results["benchmarks"]["import_times"] = {
            "status": "ok",
            "modules": import_metrics,
        }

    def _benchmark_file_operations(self) -> None:
        print("\n📁 File Operations...")
        start = time.perf_counter()
        py_files = list(self.project_root.rglob("*.py"))
        count_time = time.perf_counter() - start

        start = time.perf_counter()
        total_size = sum(f.stat().st_size for f in py_files if f.exists())
        size_time = time.perf_counter() - start

        print(
            f"  ✅ Counted {len(py_files)} Python files in {count_time:.3f}s; "
            f"total size {total_size:,} bytes (computed in {size_time:.3f}s)"
        )

        self.results["benchmarks"]["file_operations"] = {
            "status": "ok",
            "file_count": len(py_files),
            "total_size_bytes": total_size,
            "count_time": count_time,
            "size_time": size_time,
        }

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    def _time_subprocess(self, command: list[str]) -> dict[str, Any]:
        start = time.perf_counter()
        try:
            completed = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60,
            )
        except FileNotFoundError:
            return {
                "time": None,
                "return_code": -1,
                "stdout": "",
                "stderr": "",
                "error": "missing-binary",
            }
        except subprocess.TimeoutExpired:
            return {
                "time": 60.0,
                "return_code": -1,
                "stdout": "",
                "stderr": "",
                "error": "timeout",
            }
        else:
            elapsed = time.perf_counter() - start
            return {
                "time": elapsed,
                "return_code": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "error": None,
            }

    def _stderr_matches(self, outcome: dict[str, Any], indicators: Iterable[str]) -> bool:
        stderr = outcome.get("stderr") or ""
        return any(indicator in stderr for indicator in indicators)

    def _print_summary(self) -> None:
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE BENCHMARK SUMMARY")
        print("=" * 60)

        benchmarks = self.results["benchmarks"]
        total = len(benchmarks)
        success = sum(1 for record in benchmarks.values() if record["status"] == "ok")
        warnings = sum(1 for record in benchmarks.values() if record["status"] == "warning")
        errors = sum(1 for record in benchmarks.values() if record["status"] == "error")
        skipped = sum(1 for record in benchmarks.values() if record["status"] == "skipped")

        cumulative_time = sum(
            (record.get("execution_time") or 0.0)
            for record in benchmarks.values()
            if record["status"] == "ok"
        )

        print(f"Total Benchmarks: {total}")
        print(f"Successful: {success}")
        print(f"Warnings: {warnings}")
        print(f"Errors: {errors}")
        print(f"Skipped: {skipped}")
        print(f"Cumulative execution time: {cumulative_time:.3f}s")

        if errors:
            rating = "❌ Needs Attention"
        elif warnings:
            rating = "⚠️ Mixed"
        elif skipped:
            rating = "ℹ️ Partial"
        else:
            rating = "🚀 Excellent"
        print(f"Performance Rating: {rating}")

    # ------------------------------------------------------------------
    # Optional profiling helpers (retained for backwards compatibility)
    # ------------------------------------------------------------------
    @contextmanager
    def profile_code(self, name: str):  # pragma: no cover - retained for manual use
        import cProfile
        import pstats
        from io import StringIO

        profiler = cProfile.Profile()
        profiler.enable()
        start = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start
            profiler.disable()
            stream = StringIO()
            stats = pstats.Stats(profiler, stream=stream).sort_stats("cumulative")
            stats.print_stats(10)
            self.results.setdefault("benchmarks", {})[f"profile_{name}"] = {
                "status": "ok",
                "execution_time": duration,
                "profile_stats": stream.getvalue(),
            }


def main() -> None:
    parser = argparse.ArgumentParser(description="RJW-IDD Performance Benchmarks")
    parser.add_argument("--project-root", help="Project root directory")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    benchmark = PerformanceBenchmark(args.project_root)
    results = benchmark.run_all_benchmarks()

    if args.json:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

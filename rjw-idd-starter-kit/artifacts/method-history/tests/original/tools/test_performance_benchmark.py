from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

import tools.performance_benchmark as performance_benchmark_module  # type: ignore[import-not-found]


@pytest.fixture
def benchmark(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> performance_benchmark_module.PerformanceBenchmark:
    (tmp_path / "module_under_test.py").write_text("print('ok')\n", encoding="utf-8")

    def fake_time_subprocess(self: Any, command: list[str]) -> dict[str, Any]:
        joined = " ".join(command)
        if "ruff" in joined:
            return {
                "time": None,
                "return_code": 1,
                "stdout": "",
                "stderr": "No module named ruff",
                "error": None,
            }
        return {
            "time": 0.05,
            "return_code": 0,
            "stdout": "",
            "stderr": "",
            "error": None,
        }

    def fake_import_module(name: str) -> object:
        class DummyModule:
            __slots__ = ()

        return DummyModule()

    monkeypatch.setattr(performance_benchmark_module.PerformanceBenchmark, "_time_subprocess", fake_time_subprocess)
    monkeypatch.setattr(performance_benchmark_module.importlib, "import_module", fake_import_module)

    return performance_benchmark_module.PerformanceBenchmark(str(tmp_path))


def test_performance_benchmark_records_statuses(
    benchmark: performance_benchmark_module.PerformanceBenchmark,
) -> None:
    results = benchmark.run_all_benchmarks()

    assert results["benchmarks"]["evidence_harvester"]["status"] == "ok"
    assert results["benchmarks"]["linting"]["status"] == "skipped"
    assert "file_operations" in results["benchmarks"]
    assert results["benchmarks"]["file_operations"]["status"] == "ok"

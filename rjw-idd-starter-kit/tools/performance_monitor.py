#!/usr/bin/env python3
"""Performance monitoring and profiling tools for RJW-IDD."""

from __future__ import annotations

import cProfile
import functools
import logging
import pstats
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

from tools.logging_config import get_logger

logger = get_logger(__name__)

F = TypeVar('F', bound=Callable[..., Any])


@dataclass
class PerformanceMetrics:
    """Container for performance measurement results."""

    operation: str
    start_time: float
    end_time: float
    duration: float = field(init=False)
    memory_usage: Optional[int] = None
    cpu_usage: Optional[float] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.duration = self.end_time - self.start_time


class PerformanceMonitor:
    """Monitor and profile code performance."""

    def __init__(self, log_level: str = "INFO"):
        self.logger = logging.getLogger(f"{__name__}.monitor")
        self.logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        self.metrics: list[PerformanceMetrics] = []

    @contextmanager
    def measure(self, operation: str, **metadata: Any):
        """Context manager to measure operation performance."""
        start_time = time.perf_counter()

        try:
            yield
        finally:
            end_time = time.perf_counter()

            metrics = PerformanceMetrics(
                operation=operation,
                start_time=start_time,
                end_time=end_time,
                metadata=metadata
            )

            self.metrics.append(metrics)
            self.logger.info(
                f"Performance: {operation} took {metrics.duration:.4f}s"
            )

    def profile_function(
        self,
        output_file: Optional[Path] = None,
        sort_by: str = 'cumulative'
    ) -> Callable[[F], F]:
        """Decorator to profile function performance."""
        def decorator(func: F) -> F:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                profiler = cProfile.Profile()
                profiler.enable()

                try:
                    return func(*args, **kwargs)
                finally:
                    profiler.disable()

                    if output_file:
                        profiler.dump_stats(str(output_file))
                        self.logger.info(f"Profile saved to {output_file}")
                    else:
                        # Print stats to console
                        stats = pstats.Stats(profiler)
                        stats.sort_stats(sort_by)
                        stats.print_stats(20)  # Top 20 functions

            return wrapper  # type: ignore
        return decorator

    def get_summary_stats(self) -> dict[str, Any]:
        """Get summary statistics of all measurements."""
        if not self.metrics:
            return {}

        durations = [m.duration for m in self.metrics]
        operations = list(set(m.operation for m in self.metrics))

        return {
            "total_measurements": len(self.metrics),
            "unique_operations": len(operations),
            "total_time": sum(durations),
            "average_time": sum(durations) / len(durations),
            "min_time": min(durations),
            "max_time": max(durations),
            "operations": operations,
            "measurements": [
                {
                    "operation": m.operation,
                    "duration": m.duration,
                    "metadata": m.metadata
                }
                for m in self.metrics
            ]
        }

    def save_report(self, output_path: Path) -> None:
        """Save performance report to file."""
        import json

        stats = self.get_summary_stats()
        stats["timestamp"] = time.time()

        with output_path.open('w') as f:
            json.dump(stats, f, indent=2, default=str)

        self.logger.info(f"Performance report saved to {output_path}")


# Global monitor instance
monitor = PerformanceMonitor()


def measure_performance(operation: str, **metadata: Any) -> Callable[[F], F]:
    """Decorator to measure function performance."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with monitor.measure(operation, **metadata):
                return func(*args, **kwargs)
        return wrapper  # type: ignore
    return decorator


@contextmanager
def benchmark(operation: str, **metadata: Any):
    """Context manager for benchmarking code blocks."""
    with monitor.measure(operation, **metadata):
        yield


def run_performance_test(
    func: Callable[[], Any],
    iterations: int = 100,
    warmup_iterations: int = 10
) -> dict[str, Any]:
    """Run performance test with multiple iterations."""
    # Warmup
    for _ in range(warmup_iterations):
        func()

    # Actual test
    monitor.metrics.clear()
    start_time = time.perf_counter()

    for i in range(iterations):
        with monitor.measure(f"iteration_{i}"):
            func()

    end_time = time.perf_counter()
    total_time = end_time - start_time

    return {
        "iterations": iterations,
        "total_time": total_time,
        "average_time": total_time / iterations,
        "operations_per_second": iterations / total_time,
        "summary": monitor.get_summary_stats()
    }


if __name__ == "__main__":
    # Example usage
    @measure_performance("example_function")
    def example_function():
        time.sleep(0.1)
        return "done"

    # Run example
    result = example_function()
    print(f"Result: {result}")

    # Print summary
    print("Performance Summary:")
    print(monitor.get_summary_stats())
"""Utility functions for measuring runtime and peak RAM usage."""

from __future__ import annotations

import os
import threading
import time
from typing import Any, Callable

import psutil


def measure_time_and_peak_ram(
    func: Callable[..., Any],
    *args,
    sample_interval: float = 0.001,
    **kwargs,
) -> dict[str, Any]:
    """
    Measure elapsed time and peak process RAM while a function runs.

    Returns a dictionary containing:
    - result
    - elapsed_seconds
    - ram_before_mb
    - ram_after_mb
    - peak_ram_mb
    """
    process = psutil.Process(os.getpid())

    ram_before_bytes = process.memory_info().rss
    peak_ram_bytes = ram_before_bytes
    running = True

    def sampler() -> None:
        nonlocal peak_ram_bytes, running
        while running:
            current_bytes = process.memory_info().rss
            if current_bytes > peak_ram_bytes:
                peak_ram_bytes = current_bytes
            time.sleep(sample_interval)

    sampler_thread = threading.Thread(target=sampler, daemon=True)
    sampler_thread.start()

    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()

    running = False
    sampler_thread.join(timeout=0.1)

    ram_after_bytes = process.memory_info().rss

    return {
        "result": result,
        "elapsed_seconds": end - start,
        "ram_before_mb": ram_before_bytes / (1024 * 1024),
        "ram_after_mb": ram_after_bytes / (1024 * 1024),
        "peak_ram_mb": peak_ram_bytes / (1024 * 1024),
    }
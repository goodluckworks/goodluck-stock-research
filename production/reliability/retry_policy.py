#!/usr/bin/env python3
"""Bounded retry policy."""

from __future__ import annotations


def retry_schedule(max_attempts: int = 3, base_delay_seconds: float = 0.2) -> list[float]:
    if not 1 <= max_attempts <= 3:
        raise ValueError("max_attempts must be between 1 and 3.")
    return [base_delay_seconds * attempt for attempt in range(max_attempts)]

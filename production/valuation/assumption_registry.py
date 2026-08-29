#!/usr/bin/env python3
"""Assumption registry for valuation scenarios."""

from __future__ import annotations


DEFAULT_ASSUMPTIONS = {
    "bear": {"revenue_multiple": 4.0, "fcf_margin": 0.15},
    "base": {"revenue_multiple": 6.0, "fcf_margin": 0.20},
    "bull": {"revenue_multiple": 8.0, "fcf_margin": 0.25},
}


def get_assumptions() -> dict[str, dict[str, float]]:
    return DEFAULT_ASSUMPTIONS

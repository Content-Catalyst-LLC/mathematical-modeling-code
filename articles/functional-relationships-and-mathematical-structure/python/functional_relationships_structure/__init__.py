"""Companion workflow for functional relationships and mathematical structure."""

from .core import (
    RelationshipRecord,
    StructureScenario,
    load_relationships,
    load_scenarios,
    simulate_structure,
    summarize_structure,
    structure_risk_score,
    build_structural_diagnostics_card,
)

__all__ = [
    "RelationshipRecord",
    "StructureScenario",
    "load_relationships",
    "load_scenarios",
    "simulate_structure",
    "summarize_structure",
    "structure_risk_score",
    "build_structural_diagnostics_card",
]

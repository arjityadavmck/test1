"""Core package exports for agents.

This package re-exports the minimal APIs agents need so agent code can use
`from src.core import chat, pick_requirement` without deep imports.

Keep this file small: its purpose is purely convenience for teaching and
to keep example agent files short and readable.
"""

from .llm_client import chat
from .utils import pick_requirement, parse_json_safely, to_rows, write_csv, write_json
from .quality_scorer import score_test_cases, TestCaseQualityScorer
from .requirement_enhancer import enhance_requirement, enhance_requirement_file, RequirementEnhancementAgent

__all__ = [
    "chat",
    "pick_requirement",
    "parse_json_safely",
    "to_rows",
    "write_csv",
    "write_json",
    "score_test_cases",
    "TestCaseQualityScorer",
    "enhance_requirement",
    "enhance_requirement_file",
    "RequirementEnhancementAgent",
]
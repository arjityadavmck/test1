"""
Enhanced Test Case Generator Graph with Rich UI
"""

import logging
import time
from langgraph.graph import StateGraph, END

from .state import TestCaseState
from .enhanced_nodes import (
    display_banner,
    enhanced_read_requirements,
    enhanced_generate_tests_with_llm,
    enhanced_approval_checkpoint,
    enhanced_push_to_testrail,
    display_final_summary
)

# Logger
logging.basicConfig(level=logging.INFO, format="🔹 %(message)s")
logger = logging.getLogger(__name__)


def _route_after_approval(state: TestCaseState) -> str:
    """Router for conditional edges after approval node."""
    return "approved" if state.get("approval_decision") == "approved" else "rejected"


def build_enhanced_graph():
    """Build and return the enhanced Test Case Generator pipeline with Rich UI."""
    
    # Display banner at build time
    display_banner()
    
    workflow = StateGraph(TestCaseState)

    # Add enhanced nodes
    workflow.add_node("read_requirements", enhanced_read_requirements)
    workflow.add_node("generate_tests_with_llm", enhanced_generate_tests_with_llm)
    workflow.add_node("approval_checkpoint", enhanced_approval_checkpoint)
    workflow.add_node("push_to_testrail", enhanced_push_to_testrail)

    # Edges
    workflow.set_entry_point("read_requirements")
    workflow.add_edge("read_requirements", "generate_tests_with_llm")
    workflow.add_edge("generate_tests_with_llm", "approval_checkpoint")

    # Conditional routing based on approval decision
    workflow.add_conditional_edges(
        "approval_checkpoint",
        _route_after_approval,
        {
            "approved": "push_to_testrail",
            "rejected": END,
        },
    )

    # Push goes to END
    workflow.add_edge("push_to_testrail", END)

    app = workflow.compile()
    
    logger.info("✅ Enhanced Test Case Generator pipeline built successfully")
    return app
"""
Test Case Quality Scoring Module
===============================

This module provides AI-powered quality assessment for generated test cases.
It evaluates various quality metrics and provides actionable insights.
"""

import logging
from typing import List, Dict, Any, Tuple
from pathlib import Path
import re
import json

from .llm_client import chat
from .utils import write_json

logger = logging.getLogger(__name__)

# Quality scoring prompts
QUALITY_SYSTEM_PROMPT = """You are an expert QA quality assessor. Evaluate test cases based on industry best practices and provide detailed scoring with actionable feedback.

Return your assessment as JSON with this exact structure:
{
  "overall_score": 8.5,
  "individual_scores": [
    {
      "test_id": "TC-001",
      "scores": {
        "clarity": 9.0,
        "completeness": 8.5,
        "specificity": 8.0,
        "testability": 9.0,
        "coverage": 7.5
      },
      "total_score": 8.4,
      "strengths": ["Clear step descriptions", "Specific expected results"],
      "weaknesses": ["Missing error handling", "No boundary value tests"],
      "suggestions": ["Add negative test scenarios", "Include edge cases for input validation"]
    }
  ],
  "quality_insights": {
    "coverage_gaps": ["Error handling scenarios", "Performance edge cases"],
    "missing_categories": ["Security tests", "Integration tests"],
    "recommendations": ["Add boundary value analysis", "Include negative test scenarios"],
    "strengths": ["Good happy path coverage", "Clear test descriptions"],
    "overall_feedback": "Test suite covers basic functionality well but needs more comprehensive error handling and edge case coverage."
  }
}

Quality Criteria:
- Clarity (1-10): How clear and understandable are the test steps?
- Completeness (1-10): Does the test cover all aspects of the requirement?
- Specificity (1-10): Are expected results specific and measurable?
- Testability (1-10): Can the test be executed reliably?
- Coverage (1-10): How well does it cover different scenarios?
"""

QUALITY_USER_TEMPLATE = """Assess the quality of these test cases against the given requirement:

REQUIREMENT:
{requirement_text}

TEST CASES:
{test_cases_json}

Provide detailed quality scoring and actionable improvement suggestions."""


class TestCaseQualityScorer:
    """Evaluates test case quality using AI-powered analysis."""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("outputs/quality_reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def score_test_cases(self, test_cases: List[Dict], requirement_text: str) -> Dict[str, Any]:
        """
        Score test cases for quality and provide improvement suggestions.
        
        Args:
            test_cases: List of test case dictionaries
            requirement_text: Original requirement text
            
        Returns:
            Quality assessment dictionary with scores and suggestions
        """
        logger.info("🔍 Starting test case quality assessment...")
        
        try:
            # Prepare input for LLM
            user_prompt = QUALITY_USER_TEMPLATE.format(
                requirement_text=requirement_text,
                test_cases_json=json.dumps(test_cases, indent=2)
            )
            
            messages = [
                {"role": "system", "content": QUALITY_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
            
            # Get quality assessment from LLM
            logger.info("📡 Calling LLM for quality assessment...")
            raw_response = chat(messages)
            
            # Parse the quality assessment
            quality_report = self._parse_quality_response(raw_response)
            
            # Add metadata
            quality_report["metadata"] = {
                "total_test_cases": len(test_cases),
                "requirement_length": len(requirement_text),
                "assessment_timestamp": "2025-10-12T10:30:00Z"
            }
            
            # Save detailed report
            report_file = self.output_dir / "quality_assessment.json"
            write_json(quality_report, report_file)
            logger.info(f"📊 Quality report saved to {report_file}")
            
            # Log summary
            overall_score = quality_report.get("overall_score", 0)
            logger.info(f"✅ Quality assessment complete. Overall score: {overall_score}/10")
            
            return quality_report
            
        except Exception as e:
            logger.error(f"❌ Quality assessment failed: {e}")
            return self._get_fallback_quality_report(test_cases)
    
    def _parse_quality_response(self, raw_response: str) -> Dict[str, Any]:
        """Parse LLM response into structured quality report."""
        try:
            # Try direct JSON parsing
            return json.loads(raw_response.strip())
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # If all parsing fails, create a basic structure
            logger.warning("⚠️ Could not parse quality response, using fallback")
            return self._get_fallback_quality_report([])
    
    def _get_fallback_quality_report(self, test_cases: List[Dict]) -> Dict[str, Any]:
        """Generate a basic quality report when LLM assessment fails."""
        individual_scores = []
        
        for i, test_case in enumerate(test_cases):
            test_id = test_case.get("id", f"TC-{i+1:03d}")
            
            # Simple heuristic scoring
            clarity_score = self._score_clarity(test_case)
            completeness_score = self._score_completeness(test_case)
            specificity_score = self._score_specificity(test_case)
            testability_score = self._score_testability(test_case)
            coverage_score = 7.0  # Default coverage score
            
            total_score = (clarity_score + completeness_score + specificity_score + 
                          testability_score + coverage_score) / 5
            
            individual_scores.append({
                "test_id": test_id,
                "scores": {
                    "clarity": clarity_score,
                    "completeness": completeness_score,
                    "specificity": specificity_score,
                    "testability": testability_score,
                    "coverage": coverage_score
                },
                "total_score": round(total_score, 1),
                "strengths": ["Basic test structure present"],
                "weaknesses": ["Limited assessment available"],
                "suggestions": ["Review test completeness", "Add more specific assertions"]
            })
        
        overall_score = sum(score["total_score"] for score in individual_scores) / len(individual_scores) if individual_scores else 6.0
        
        return {
            "overall_score": round(overall_score, 1),
            "individual_scores": individual_scores,
            "quality_insights": {
                "coverage_gaps": ["Detailed analysis not available"],
                "missing_categories": ["Assessment limited"],
                "recommendations": ["Run full quality assessment", "Review test coverage"],
                "strengths": ["Basic test structure"],
                "overall_feedback": "Basic quality assessment completed. For detailed analysis, ensure LLM service is available."
            }
        }
    
    def _score_clarity(self, test_case: Dict) -> float:
        """Score test case clarity based on step descriptions."""
        steps = test_case.get("steps", [])
        if not steps:
            return 3.0
        
        total_length = sum(len(str(step)) for step in steps)
        avg_length = total_length / len(steps)
        
        # Longer, more descriptive steps generally indicate better clarity
        if avg_length > 50:
            return 8.5
        elif avg_length > 30:
            return 7.0
        elif avg_length > 15:
            return 6.0
        else:
            return 4.0
    
    def _score_completeness(self, test_case: Dict) -> float:
        """Score test case completeness based on required fields."""
        required_fields = ["title", "steps", "expected"]
        present_fields = sum(1 for field in required_fields if test_case.get(field))
        
        base_score = (present_fields / len(required_fields)) * 10
        
        # Bonus for additional fields
        if test_case.get("priority"):
            base_score += 0.5
        if test_case.get("preconditions"):
            base_score += 0.5
        
        return min(base_score, 10.0)
    
    def _score_specificity(self, test_case: Dict) -> float:
        """Score test case specificity based on expected results."""
        expected = test_case.get("expected", "")
        if not expected:
            return 2.0
        
        # Look for specific assertions
        specific_indicators = [
            "should display", "should show", "should redirect",
            "error message", "success message", "specific value",
            "status code", "response contains"
        ]
        
        specificity_count = sum(1 for indicator in specific_indicators 
                               if indicator.lower() in expected.lower())
        
        base_score = min(specificity_count * 2 + 5, 10.0)
        return base_score
    
    def _score_testability(self, test_case: Dict) -> float:
        """Score how easily the test can be executed."""
        steps = test_case.get("steps", [])
        if not steps:
            return 3.0
        
        # Look for actionable verbs
        actionable_verbs = [
            "click", "enter", "select", "navigate", "verify",
            "check", "validate", "confirm", "submit", "open"
        ]
        
        actionable_count = 0
        for step in steps:
            step_str = str(step).lower()
            actionable_count += sum(1 for verb in actionable_verbs if verb in step_str)
        
        # Higher ratio of actionable steps = better testability
        testability_ratio = actionable_count / len(steps) if steps else 0
        return min(testability_ratio * 10 + 5, 10.0)
    
    def get_quality_summary(self, quality_report: Dict[str, Any]) -> str:
        """Generate a human-readable quality summary."""
        overall_score = quality_report.get("overall_score", 0)
        individual_scores = quality_report.get("individual_scores", [])
        insights = quality_report.get("quality_insights", {})
        
        summary_lines = [
            f"📊 Overall Quality Score: {overall_score}/10",
            f"📝 Total Test Cases: {len(individual_scores)}",
            ""
        ]
        
        # Score distribution
        if individual_scores:
            high_quality = sum(1 for score in individual_scores if score["total_score"] >= 8.0)
            medium_quality = sum(1 for score in individual_scores if 6.0 <= score["total_score"] < 8.0)
            low_quality = sum(1 for score in individual_scores if score["total_score"] < 6.0)
            
            summary_lines.extend([
                "🎯 Quality Distribution:",
                f"  🟢 High Quality (8.0+): {high_quality} tests",
                f"  🟡 Medium Quality (6.0-7.9): {medium_quality} tests", 
                f"  🔴 Low Quality (<6.0): {low_quality} tests",
                ""
            ])
        
        # Key insights
        recommendations = insights.get("recommendations", [])
        if recommendations:
            summary_lines.extend([
                "💡 Key Recommendations:",
                *[f"  • {rec}" for rec in recommendations[:3]],
                ""
            ])
        
        # Coverage gaps
        coverage_gaps = insights.get("coverage_gaps", [])
        if coverage_gaps:
            summary_lines.extend([
                "⚠️ Coverage Gaps:",
                *[f"  • {gap}" for gap in coverage_gaps[:3]],
                ""
            ])
        
        return "\n".join(summary_lines)


def score_test_cases(test_cases: List[Dict], requirement_text: str, 
                    output_dir: Path = None) -> Dict[str, Any]:
    """
    Convenience function to score test cases.
    
    Args:
        test_cases: List of test case dictionaries
        requirement_text: Original requirement text
        output_dir: Directory to save quality reports
        
    Returns:
        Quality assessment dictionary
    """
    scorer = TestCaseQualityScorer(output_dir)
    return scorer.score_test_cases(test_cases, requirement_text)
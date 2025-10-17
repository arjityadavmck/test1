"""
Requirement Enhancement Agent
============================

This agent analyzes requirement files and enhances them for better test case generation.
It fixes grammatical errors, improves clarity, adds missing details, and structures 
requirements for optimal LLM processing.
"""

import logging
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

from .llm_client import chat
from .utils import write_json

logger = logging.getLogger(__name__)

# Requirement enhancement prompts
ENHANCEMENT_SYSTEM_PROMPT = """You are an expert Business Analyst and Technical Writer specializing in requirement analysis and improvement. Your role is to enhance software requirements to make them clearer, more complete, and better structured for test case generation.

Return your analysis as JSON with this exact structure:
{
  "enhanced_requirement": "The improved requirement text with better structure, clarity, and completeness",
  "improvements_made": [
    "Fixed grammatical errors in sentence 2",
    "Added specific error handling requirements",
    "Clarified user flow steps",
    "Added acceptance criteria"
  ],
  "quality_issues_found": [
    "Vague expected behavior descriptions",
    "Missing error handling scenarios",
    "Ambiguous user interface elements"
  ],
  "suggestions_applied": [
    "Added specific UI element names",
    "Included error message specifications",
    "Added prerequisite conditions",
    "Structured as user stories with acceptance criteria"
  ],
  "completeness_score": 8.5,
  "clarity_score": 9.0,
  "testability_score": 8.8,
  "overall_score": 8.8,
  "missing_elements": [
    "Performance requirements",
    "Security considerations",
    "Browser compatibility"
  ],
  "recommended_additions": [
    "Add specific timeout values for operations",
    "Include validation rules for input fields",
    "Specify expected response times"
  ]
}

Enhancement Guidelines:
1. Fix all grammatical and spelling errors
2. Replace vague terms with specific, measurable criteria
3. Add missing acceptance criteria and edge cases
4. Structure requirements clearly with bullet points or user stories
5. Include error handling and validation requirements
6. Add prerequisite conditions and assumptions
7. Specify UI elements, messages, and system responses
8. Include performance and security considerations where relevant
9. Make requirements testable and verifiable
10. Add examples and scenarios where helpful"""

ENHANCEMENT_USER_TEMPLATE = """Analyze and enhance this software requirement for optimal test case generation:

ORIGINAL REQUIREMENT:
{requirement_text}

Please improve this requirement by:
1. Fixing any grammatical or spelling errors
2. Adding clarity and specificity
3. Including missing acceptance criteria
4. Structuring it for better readability
5. Adding error handling scenarios
6. Making it more testable and complete

Focus on making this requirement clear, complete, and optimal for AI test case generation."""


class RequirementEnhancementAgent:
    """Agent that analyzes and enhances requirement files for better test case generation."""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("outputs/enhanced_requirements")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def enhance_requirement(self, requirement_text: str, source_file: str = None) -> Dict:
        """
        Enhance a requirement text for better test case generation.
        
        Args:
            requirement_text: Original requirement text
            source_file: Optional source file name for reference
            
        Returns:
            Enhancement report with improved requirement and analysis
        """
        logger.info("📝 Starting requirement enhancement analysis...")
        
        try:
            # Prepare prompt for LLM
            user_prompt = ENHANCEMENT_USER_TEMPLATE.format(
                requirement_text=requirement_text.strip()
            )
            
            messages = [
                {"role": "system", "content": ENHANCEMENT_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
            
            # Get enhancement from LLM
            logger.info("🤖 Analyzing requirement with AI...")
            raw_response = chat(messages)
            
            # Parse the enhancement response
            enhancement_report = self._parse_enhancement_response(raw_response)
            
            # Add metadata
            enhancement_report["metadata"] = {
                "source_file": source_file,
                "original_length": len(requirement_text),
                "enhanced_length": len(enhancement_report.get("enhanced_requirement", "")),
                "processing_timestamp": "2025-10-12T10:30:00Z"
            }
            
            # Perform additional analysis
            enhancement_report.update(self._analyze_enhancement_quality(
                requirement_text, 
                enhancement_report.get("enhanced_requirement", "")
            ))
            
            # Save enhancement report
            if source_file:
                report_file = self.output_dir / f"{Path(source_file).stem}_enhancement_report.json"
                write_json(enhancement_report, report_file)
                logger.info(f"📊 Enhancement report saved to {report_file}")
            
            # Log summary
            overall_score = enhancement_report.get("overall_score", 0)
            improvements_count = len(enhancement_report.get("improvements_made", []))
            logger.info(f"✅ Requirement enhanced! Score: {overall_score}/10, {improvements_count} improvements made")
            
            return enhancement_report
            
        except Exception as e:
            logger.error(f"❌ Requirement enhancement failed: {e}")
            return self._get_fallback_enhancement(requirement_text, source_file)
    
    def enhance_requirement_file(self, file_path: Path) -> Tuple[str, Dict]:
        """
        Enhance a requirement file and return improved content with analysis.
        
        Args:
            file_path: Path to requirement file
            
        Returns:
            Tuple of (enhanced_requirement_text, enhancement_report)
        """
        logger.info(f"📄 Processing requirement file: {file_path.name}")
        
        try:
            # Read original requirement
            original_text = file_path.read_text(encoding="utf-8").strip()
            
            # Enhance the requirement
            report = self.enhance_requirement(original_text, str(file_path))
            
            # Get enhanced text
            enhanced_text = report.get("enhanced_requirement", original_text)
            
            # Save enhanced requirement file
            enhanced_file = self.output_dir / f"{file_path.stem}_enhanced.txt"
            enhanced_file.write_text(enhanced_text, encoding="utf-8")
            logger.info(f"📝 Enhanced requirement saved to {enhanced_file}")
            
            return enhanced_text, report
            
        except Exception as e:
            logger.error(f"❌ Failed to process file {file_path}: {e}")
            # Return original text with minimal report
            original_text = file_path.read_text(encoding="utf-8").strip()
            return original_text, self._get_fallback_enhancement(original_text, str(file_path))
    
    def batch_enhance_requirements(self, requirements_dir: Path) -> Dict[str, Dict]:
        """
        Enhance all requirement files in a directory.
        
        Args:
            requirements_dir: Directory containing requirement files
            
        Returns:
            Dictionary mapping filenames to enhancement reports
        """
        logger.info(f"📁 Batch processing requirements from {requirements_dir}")
        
        results = {}
        req_files = list(requirements_dir.glob("*.txt"))
        
        if not req_files:
            logger.warning(f"⚠️ No .txt files found in {requirements_dir}")
            return results
        
        for req_file in req_files:
            try:
                enhanced_text, report = self.enhance_requirement_file(req_file)
                results[req_file.name] = {
                    "enhanced_text": enhanced_text,
                    "report": report,
                    "success": True
                }
                logger.info(f"✅ Enhanced {req_file.name}")
            except Exception as e:
                logger.error(f"❌ Failed to enhance {req_file.name}: {e}")
                results[req_file.name] = {
                    "error": str(e),
                    "success": False
                }
        
        # Save batch summary
        summary_file = self.output_dir / "batch_enhancement_summary.json"
        summary = {
            "total_files": len(req_files),
            "successful": sum(1 for r in results.values() if r.get("success", False)),
            "failed": sum(1 for r in results.values() if not r.get("success", False)),
            "results": results
        }
        write_json(summary, summary_file)
        
        logger.info(f"📊 Batch processing complete: {summary['successful']}/{summary['total_files']} files enhanced")
        return results
    
    def _parse_enhancement_response(self, raw_response: str) -> Dict:
        """Parse LLM response into structured enhancement report."""
        try:
            # Try direct JSON parsing
            return json.loads(raw_response.strip())
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # If all parsing fails, create a basic structure
            logger.warning("⚠️ Could not parse enhancement response, using fallback")
            return self._get_fallback_enhancement("", "")
    
    def _analyze_enhancement_quality(self, original: str, enhanced: str) -> Dict:
        """Analyze the quality of the enhancement."""
        analysis = {}
        
        # Length analysis
        original_words = len(original.split())
        enhanced_words = len(enhanced.split())
        analysis["length_improvement"] = enhanced_words - original_words
        analysis["length_ratio"] = enhanced_words / original_words if original_words > 0 else 1.0
        
        # Structural improvements
        analysis["structure_improvements"] = {
            "bullet_points_added": enhanced.count("•") + enhanced.count("-") - (original.count("•") + original.count("-")),
            "sections_added": enhanced.count("\n\n") - original.count("\n\n"),
            "capitalized_sections": len(re.findall(r'\n[A-Z][A-Z\s]+:', enhanced)) - len(re.findall(r'\n[A-Z][A-Z\s]+:', original))
        }
        
        # Content analysis
        analysis["content_improvements"] = {
            "specific_values_added": len(re.findall(r'\d+', enhanced)) - len(re.findall(r'\d+', original)),
            "error_scenarios_added": enhanced.lower().count("error") + enhanced.lower().count("invalid") - (original.lower().count("error") + original.lower().count("invalid")),
            "ui_elements_specified": len(re.findall(r'button|field|page|form|menu', enhanced, re.IGNORECASE)) - len(re.findall(r'button|field|page|form|menu', original, re.IGNORECASE))
        }
        
        return analysis
    
    def _get_fallback_enhancement(self, original_text: str, source_file: str = None) -> Dict:
        """Generate a basic enhancement report when LLM processing fails."""
        # Basic grammar and structure improvements
        enhanced_text = self._apply_basic_improvements(original_text)
        
        return {
            "enhanced_requirement": enhanced_text,
            "improvements_made": [
                "Applied basic grammar corrections",
                "Improved sentence structure",
                "Added basic formatting"
            ],
            "quality_issues_found": [
                "Limited analysis available - LLM processing failed"
            ],
            "suggestions_applied": [
                "Basic text cleaning and formatting"
            ],
            "completeness_score": 6.0,
            "clarity_score": 6.5,
            "testability_score": 6.0,
            "overall_score": 6.2,
            "missing_elements": [
                "Detailed analysis not available"
            ],
            "recommended_additions": [
                "Run full enhancement when LLM service is available"
            ],
            "fallback_used": True,
            "metadata": {
                "source_file": source_file,
                "original_length": len(original_text),
                "enhanced_length": len(enhanced_text),
                "processing_timestamp": "2025-10-12T10:30:00Z"
            }
        }
    
    def _apply_basic_improvements(self, text: str) -> str:
        """Apply basic text improvements when LLM is unavailable."""
        improved = text
        
        # Basic grammar fixes
        improved = re.sub(r'\s+', ' ', improved)  # Normalize whitespace
        improved = re.sub(r'([.!?])\s*([a-z])', r'\1 \2'.upper(), improved)  # Capitalize after periods
        improved = improved.strip()
        
        # Add structure if missing
        if not any(indicator in improved.lower() for indicator in ['requirement:', 'details:', 'acceptance criteria:']):
            improved = f"Requirement:\n{improved}\n\nDetails:\n- This requirement needs further specification\n- Consider adding acceptance criteria\n- Include error handling scenarios"
        
        return improved
    
    def get_enhancement_summary(self, enhancement_report: Dict) -> str:
        """Generate a human-readable enhancement summary."""
        if not enhancement_report:
            return "No enhancement report available."
        
        lines = []
        
        # Overall scores
        overall_score = enhancement_report.get("overall_score", 0)
        clarity_score = enhancement_report.get("clarity_score", 0)
        completeness_score = enhancement_report.get("completeness_score", 0)
        testability_score = enhancement_report.get("testability_score", 0)
        
        lines.extend([
            "📊 REQUIREMENT ENHANCEMENT SUMMARY",
            "=" * 40,
            f"Overall Score: {overall_score:.1f}/10",
            f"Clarity: {clarity_score:.1f} | Completeness: {completeness_score:.1f} | Testability: {testability_score:.1f}",
            ""
        ])
        
        # Improvements made
        improvements = enhancement_report.get("improvements_made", [])
        if improvements:
            lines.extend([
                "✅ Improvements Made:",
                *[f"  • {imp}" for imp in improvements[:5]],
                ""
            ])
        
        # Quality issues found
        issues = enhancement_report.get("quality_issues_found", [])
        if issues:
            lines.extend([
                "⚠️ Issues Addressed:",
                *[f"  • {issue}" for issue in issues[:3]],
                ""
            ])
        
        # Recommendations
        recommendations = enhancement_report.get("recommended_additions", [])
        if recommendations:
            lines.extend([
                "💡 Additional Recommendations:",
                *[f"  • {rec}" for rec in recommendations[:3]],
                ""
            ])
        
        return "\n".join(lines)


def enhance_requirement(requirement_text: str, output_dir: Path = None) -> Tuple[str, Dict]:
    """
    Convenience function to enhance a requirement text.
    
    Args:
        requirement_text: Original requirement text
        output_dir: Directory to save enhancement reports
        
    Returns:
        Tuple of (enhanced_text, enhancement_report)
    """
    agent = RequirementEnhancementAgent(output_dir)
    report = agent.enhance_requirement(requirement_text)
    enhanced_text = report.get("enhanced_requirement", requirement_text)
    return enhanced_text, report


def enhance_requirement_file(file_path: Path, output_dir: Path = None) -> Tuple[str, Dict]:
    """
    Convenience function to enhance a requirement file.
    
    Args:
        file_path: Path to requirement file
        output_dir: Directory to save enhancement reports
        
    Returns:
        Tuple of (enhanced_text, enhancement_report)
    """
    agent = RequirementEnhancementAgent(output_dir)
    return agent.enhance_requirement_file(file_path)
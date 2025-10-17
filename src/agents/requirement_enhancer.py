#!/usr/bin/env python3
"""
Requirement Enhancement Agent - CLI Tool
========================================

A command-line tool that analyzes and enhances requirement files
to improve them for better test case generation.

Usage:
    python -m src.agents.requirement_enhancer --input data/requirements/login.txt
    python -m src.agents.requirement_enhancer --batch data/requirements/
    python -m src.agents.requirement_enhancer --interactive
"""

import argparse
import logging
from pathlib import Path
import sys

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.core import enhance_requirement_file, RequirementEnhancementAgent


def setup_logging():
    """Configure logging for the CLI tool."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )


def enhance_single_file(file_path: Path, output_dir: Path = None):
    """Enhance a single requirement file."""
    logger = logging.getLogger(__name__)
    
    if not file_path.exists():
        logger.error(f"❌ File not found: {file_path}")
        return False
    
    try:
        logger.info(f"🚀 Enhancing requirement file: {file_path.name}")
        enhanced_text, report = enhance_requirement_file(file_path, output_dir)
        
        # Display summary
        agent = RequirementEnhancementAgent(output_dir)
        summary = agent.get_enhancement_summary(report)
        print("\n" + summary)
        
        # Show before/after comparison
        print("📄 BEFORE & AFTER COMPARISON:")
        print("=" * 50)
        original_text = file_path.read_text(encoding="utf-8").strip()
        
        print("🔴 ORIGINAL:")
        print("-" * 20)
        print(original_text[:300] + "..." if len(original_text) > 300 else original_text)
        
        print("\n🟢 ENHANCED:")
        print("-" * 20)
        print(enhanced_text[:300] + "..." if len(enhanced_text) > 300 else enhanced_text)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Enhancement failed: {e}")
        return False


def enhance_batch(requirements_dir: Path, output_dir: Path = None):
    """Enhance all requirement files in a directory."""
    logger = logging.getLogger(__name__)
    
    if not requirements_dir.exists():
        logger.error(f"❌ Directory not found: {requirements_dir}")
        return False
    
    try:
        logger.info(f"📁 Batch enhancing requirements from: {requirements_dir}")
        agent = RequirementEnhancementAgent(output_dir)
        results = agent.batch_enhance_requirements(requirements_dir)
        
        # Display batch summary
        successful = sum(1 for r in results.values() if r.get("success", False))
        total = len(results)
        
        print(f"\n📊 BATCH ENHANCEMENT SUMMARY")
        print("=" * 40)
        print(f"Total Files: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {total - successful}")
        print(f"Success Rate: {(successful/total*100):.1f}%")
        
        # Show individual results
        print("\n📋 Individual Results:")
        for filename, result in results.items():
            if result.get("success", False):
                report = result.get("report", {})
                score = report.get("overall_score", 0)
                improvements = len(report.get("improvements_made", []))
                print(f"  ✅ {filename} - Score: {score:.1f}/10, {improvements} improvements")
            else:
                error = result.get("error", "Unknown error")
                print(f"  ❌ {filename} - Error: {error}")
        
        return successful > 0
        
    except Exception as e:
        logger.error(f"❌ Batch enhancement failed: {e}")
        return False


def interactive_mode():
    """Interactive mode for requirement enhancement."""
    logger = logging.getLogger(__name__)
    
    print("🎯 INTERACTIVE REQUIREMENT ENHANCEMENT")
    print("=" * 40)
    print("Enter your requirement text (press Ctrl+D or Ctrl+Z when finished):")
    print("-" * 40)
    
    try:
        # Read multi-line input
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        
        requirement_text = "\n".join(lines).strip()
        
        if not requirement_text:
            print("❌ No requirement text provided.")
            return False
        
        print("\n🤖 Processing your requirement...")
        
        # Enhance the requirement
        agent = RequirementEnhancementAgent()
        report = agent.enhance_requirement(requirement_text)
        enhanced_text = report.get("enhanced_requirement", requirement_text)
        
        # Display results
        summary = agent.get_enhancement_summary(report)
        print("\n" + summary)
        
        print("\n📄 ENHANCED REQUIREMENT:")
        print("=" * 50)
        print(enhanced_text)
        
        # Ask if user wants to save
        save_choice = input("\n💾 Save enhanced requirement to file? (y/n): ").lower().strip()
        if save_choice in ['y', 'yes']:
            output_file = Path("outputs/enhanced_requirements/interactive_enhanced.txt")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(enhanced_text, encoding="utf-8")
            print(f"✅ Saved to: {output_file}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n❌ Enhancement cancelled by user.")
        return False
    except Exception as e:
        logger.error(f"❌ Interactive enhancement failed: {e}")
        return False


def main():
    """Main entry point for the CLI tool."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    parser = argparse.ArgumentParser(
        description="Enhance requirement files for better test case generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Enhance a single file
  python -m src.agents.requirement_enhancer --input data/requirements/login.txt
  
  # Batch enhance all files in directory
  python -m src.agents.requirement_enhancer --batch data/requirements/
  
  # Interactive mode
  python -m src.agents.requirement_enhancer --interactive
  
  # Specify custom output directory
  python -m src.agents.requirement_enhancer --input login.txt --output enhanced_reqs/
        """
    )
    
    parser.add_argument(
        "--input", "-i",
        type=Path,
        help="Path to a single requirement file to enhance"
    )
    
    parser.add_argument(
        "--batch", "-b",
        type=Path,
        help="Path to directory containing requirement files to batch enhance"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode - enter requirement text directly"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output directory for enhanced requirements (default: outputs/enhanced_requirements/)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not any([args.input, args.batch, args.interactive]):
        parser.error("Must specify one of: --input, --batch, or --interactive")
    
    if sum(bool(x) for x in [args.input, args.batch, args.interactive]) > 1:
        parser.error("Cannot specify multiple modes simultaneously")
    
    # Set output directory
    output_dir = args.output or Path("outputs/enhanced_requirements")
    
    # Execute based on mode
    success = False
    
    try:
        if args.input:
            success = enhance_single_file(args.input, output_dir)
        elif args.batch:
            success = enhance_batch(args.batch, output_dir)
        elif args.interactive:
            success = interactive_mode()
        
        if success:
            logger.info("🎉 Requirement enhancement completed successfully!")
            print(f"\n📁 Enhanced requirements and reports saved to: {output_dir}")
        else:
            logger.error("❌ Requirement enhancement failed.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("❌ Enhancement cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
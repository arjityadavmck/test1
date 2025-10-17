import logging
import argparse
import time
from datetime import datetime

from src.graph.test_case_generator.enhanced_graph import build_enhanced_graph
from src.graph.test_case_generator.enhanced_nodes import display_final_summary
from src.graph.test_case_generator.state import TestCaseState

# Configure logger
logging.basicConfig(level=logging.INFO, format="� %(message)s")
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="🚀 Enhanced Test Case Generator with Rich UI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.graph.drivers.run_test_case_pipeline_enhanced --input data/requirements/login.txt
  python -m src.graph.drivers.run_test_case_pipeline_enhanced
        """
    )
    parser.add_argument(
        "--input",
        help="Path to a requirement .txt file (default: first in data/requirements/)",
        default=None,
    )
    args = parser.parse_args()

    start_time = time.time()
    
    try:
        logger.info("🚀 Starting Enhanced Test Case Generator pipeline...")
        
        # Build the enhanced graph
        app = build_enhanced_graph()
        
        # Prepare initial state
        init_state: TestCaseState = {}
        if args.input:
            init_state["requirement_path"] = args.input
        
        # Execute the pipeline
        final_state = app.invoke(
            init_state,
            config={"configurable": {"thread_id": "testcase-enhanced-run-1"}}
        )
        
        # Collect final stats
        stats = {
            'tests_generated': len(final_state.get("tests", [])),
            'testrail_cases': len(final_state.get("testrail_case_ids", [])),
            'processing_time': time.time() - start_time
        }
        
        # Display final summary
        display_final_summary(stats)
        
        logger.info(f"✅ Finished: {stats['tests_generated']} tests generated, {stats['testrail_cases']} cases pushed to TestRail.")
        
    except KeyboardInterrupt:
        logger.info("\n❌ Operation cancelled by user")
    except Exception as e:
        logger.error(f"🚨 Error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    main()
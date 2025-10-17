#!/usr/bin/env python3
"""
Test Script for Requirement Enhancement Agent
============================================

Test the new requirement enhancement functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_requirement_enhancement():
    """Test the requirement enhancement module."""
    print("🧪 Testing Requirement Enhancement Agent...")
    print("=" * 50)
    
    try:
        # Test imports
        from src.core import enhance_requirement, RequirementEnhancementAgent
        print("✅ Requirement enhancement import successful")
        
        # Sample poor quality requirement
        poor_requirement = """
        login functionality
        
        user can login. if password wrong show error. forgot password should work.
        """
        
        print("📝 Testing requirement enhancement...")
        print("Original requirement:")
        print("-" * 30)
        print(poor_requirement.strip())
        
        # Test enhancement
        enhanced_text, report = enhance_requirement(poor_requirement)
        
        print("\n✅ Enhancement completed!")
        print(f"📊 Overall Score: {report.get('overall_score', 'N/A')}/10")
        print(f"📈 Improvements Made: {len(report.get('improvements_made', []))}")
        
        print("\n🟢 Enhanced requirement:")
        print("-" * 30)
        print(enhanced_text[:500] + "..." if len(enhanced_text) > 500 else enhanced_text)
        
        # Test specific improvements
        improvements = report.get("improvements_made", [])
        if improvements:
            print("\n💡 Key improvements:")
            for improvement in improvements[:3]:
                print(f"  • {improvement}")
        
        print("\n🎉 Requirement enhancement test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_cli_agent():
    """Test CLI agent functionality."""
    print("\n🖥️ Testing CLI Agent...")
    print("=" * 30)
    
    try:
        # Test CLI agent import
        from src.agents.requirement_enhancer import main
        print("✅ CLI agent import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ CLI import error: {e}")
        return False
    except Exception as e:
        print(f"❌ CLI test error: {e}")
        return False

def test_file_enhancement():
    """Test file-based enhancement."""
    print("\n📄 Testing File Enhancement...")
    print("=" * 35)
    
    try:
        from src.core import enhance_requirement_file
        
        # Test with existing requirement file
        req_files = list(Path("data/requirements").glob("*.txt"))
        if req_files:
            test_file = req_files[0]
            print(f"📁 Testing with file: {test_file.name}")
            
            enhanced_text, report = enhance_requirement_file(test_file)
            
            print("✅ File enhancement successful!")
            print(f"📊 Enhancement Score: {report.get('overall_score', 'N/A')}/10")
            
            original_length = len(test_file.read_text())
            enhanced_length = len(enhanced_text)
            print(f"📏 Length: {original_length} → {enhanced_length} chars ({enhanced_length/original_length:.1f}x)")
            
        else:
            print("⚠️ No requirement files found for testing")
        
        return True
        
    except Exception as e:
        print(f"❌ File enhancement test error: {e}")
        return False

def test_ui_integration():
    """Test UI integration readiness."""
    print("\n🖼️ Testing UI Integration...")
    print("=" * 30)
    
    try:
        # Test UI integration
        from ui_app.main import TestCaseGeneratorApp
        print("✅ UI integration ready")
        
        return True
        
    except ImportError as e:
        print(f"❌ UI integration error: {e}")
        return False

def show_demo():
    """Show a demo of the enhancement capabilities."""
    print("\n🎬 ENHANCEMENT DEMO")
    print("=" * 25)
    
    demo_requirement = """
    User login
    
    Users login with email password. Show error if wrong. Reset password link.
    """
    
    print("📝 Demo Input:")
    print("-" * 15)
    print(demo_requirement.strip())
    
    try:
        from src.core import enhance_requirement
        enhanced_text, report = enhance_requirement(demo_requirement)
        
        print("\n🎯 Demo Output:")
        print("-" * 16)
        print(enhanced_text[:400] + "..." if len(enhanced_text) > 400 else enhanced_text)
        
        print(f"\n📊 Quality Improvement: {report.get('overall_score', 0):.1f}/10")
        
        improvements = report.get("improvements_made", [])[:3]
        if improvements:
            print("\n✨ Key Enhancements:")
            for imp in improvements:
                print(f"  • {imp}")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")

def main():
    """Run all tests."""
    print("🚀 Requirement Enhancement Agent - Test Suite")
    print("=" * 55)
    
    tests = [
        test_requirement_enhancement,
        test_cli_agent,
        test_file_enhancement,
        test_ui_integration
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {e}")
    
    # Show demo regardless of test results
    show_demo()
    
    print("\n" + "=" * 55)
    print(f"🏆 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("✅ All tests passed! Requirement Enhancement Agent is ready!")
        print("\n🚀 Usage Options:")
        print("   1. CLI Single File:  python -m src.agents.requirement_enhancer --input data/requirements/login.txt")
        print("   2. CLI Batch Mode:   python -m src.agents.requirement_enhancer --batch data/requirements/")
        print("   3. CLI Interactive:  python -m src.agents.requirement_enhancer --interactive")
        print("   4. Enhanced UI:      python3 launch_ui.py")
    else:
        print("❌ Some tests failed. Please fix issues before using the agent.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
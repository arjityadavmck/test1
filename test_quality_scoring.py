#!/usr/bin/env python3
"""
Test Script for Quality Scoring Enhancement
==========================================

Test the new quality scoring functionality independently.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_quality_scoring():
    """Test the quality scoring module."""
    print("🧪 Testing Quality Scoring Module...")
    print("=" * 40)
    
    try:
        # Test imports
        from src.core import score_test_cases
        print("✅ Quality scoring import successful")
        
        # Sample test cases
        sample_cases = [
            {
                "id": "TC-001",
                "title": "Login with Valid Credentials",
                "steps": [
                    "Navigate to login page",
                    "Enter valid email address",
                    "Enter correct password",
                    "Click Login button"
                ],
                "expected": "User should be redirected to dashboard and see welcome message",
                "priority": "High"
            },
            {
                "id": "TC-002", 
                "title": "Login with Invalid Password",
                "steps": [
                    "Go to login",
                    "Enter email",
                    "Enter wrong password",
                    "Click login"
                ],
                "expected": "Error message",
                "priority": "High"
            }
        ]
        
        sample_requirement = """
        Requirement: The system shall allow users to log in using their registered email and password.
        
        Details:
        - If the password is entered incorrectly 3 times, the account should be locked for 10 minutes.
        - Users should have an option to reset their password via the "Forgot Password" link.
        - Successful login should redirect the user to their dashboard.
        - Error messages must be displayed for invalid credentials.
        """
        
        print("📊 Running quality assessment...")
        
        # Test quality scoring
        quality_report = score_test_cases(sample_cases, sample_requirement)
        
        print("✅ Quality assessment completed!")
        print(f"📊 Overall Score: {quality_report.get('overall_score', 'N/A')}/10")
        print(f"📝 Individual Scores: {len(quality_report.get('individual_scores', []))}")
        
        # Print individual scores
        individual_scores = quality_report.get("individual_scores", [])
        for score_info in individual_scores:
            test_id = score_info.get("test_id", "")
            total_score = score_info.get("total_score", 0)
            print(f"  {test_id}: {total_score:.1f}/10")
        
        # Print insights
        insights = quality_report.get("quality_insights", {})
        recommendations = insights.get("recommendations", [])
        if recommendations:
            print("\n💡 Recommendations:")
            for rec in recommendations[:3]:
                print(f"  • {rec}")
        
        print("\n🎉 Quality scoring test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_ui_integration():
    """Test UI integration readiness."""
    print("\n🖼️ Testing UI Integration Readiness...")
    print("=" * 40)
    
    try:
        # Test tkinter imports
        import tkinter as tk
        from tkinter import ttk
        print("✅ Tkinter imports successful")
        
        # Test UI app import
        from ui_app.main import TestCaseGeneratorApp
        print("✅ UI app import successful")
        
        print("✅ UI integration ready!")
        return True
        
    except ImportError as e:
        print(f"❌ UI import error: {e}")
        return False
    except Exception as e:
        print(f"❌ UI test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Quality Scoring Enhancement - Test Suite")
    print("=" * 50)
    
    tests = [
        test_quality_scoring,
        test_ui_integration
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {e}")
    
    print("\n" + "=" * 50)
    print(f"🏆 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("✅ All tests passed! Quality scoring enhancement is ready!")
        print("\n🚀 To test the enhanced UI, run:")
        print("   python3 launch_ui.py")
    else:
        print("❌ Some tests failed. Please fix the issues before using the enhancement.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
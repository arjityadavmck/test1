#!/usr/bin/env python3
"""
Test script to demonstrate the new features:
1. Double-click to view detailed test case
2. Expand/collapse view for better readability
"""

import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent))

from ui_app.main import TestCaseGeneratorApp

def main():
    """Run the TestCase Generator with sample data to test new features."""
    root = tk.Tk()
    app = TestCaseGeneratorApp(root)
    
    # Add some sample test cases to demonstrate the features
    sample_cases = [
        {
            "id": "TC001",
            "title": "User Login with Valid Credentials",
            "steps": ["Navigate to login page", "Enter valid email address", "Enter correct password", "Click Login button", "Verify user is redirected to dashboard"],
            "expected": "User successfully logs in and is redirected to the main dashboard with welcome message displayed",
            "priority": "High"
        },
        {
            "id": "TC002", 
            "title": "Password Reset Functionality",
            "steps": ["Click 'Forgot Password' link", "Enter registered email", "Check email for reset link", "Click reset link", "Enter new password", "Confirm new password", "Submit form"],
            "expected": "Password is successfully reset and user receives confirmation email. User can login with new password.",
            "priority": "Medium"
        },
        {
            "id": "TC003",
            "title": "Invalid Login Attempt with Wrong Credentials",
            "steps": ["Navigate to login page", "Enter invalid email or username", "Enter incorrect password", "Click Login button", "Observe error message"],
            "expected": "System displays appropriate error message 'Invalid credentials' and does not allow login. Account lockout after 3 failed attempts.",
            "priority": "High"
        }
    ]
    
    # Sample quality report
    sample_quality = {
        "overall_score": 8.5,
        "individual_scores": [
            {"test_id": "TC001", "total_score": 9.2},
            {"test_id": "TC002", "total_score": 8.1}, 
            {"test_id": "TC003", "total_score": 8.3}
        ]
    }
    
    # Simulate generated test cases
    app.generated_cases = sample_cases
    app.quality_report = sample_quality
    
    # Populate the UI
    app._update_ui_with_cases(sample_cases, sample_quality)
    
    print("🎉 TestCase Generator loaded with sample data!")
    print("💡 Try these new features:")
    print("   📊 Click 'Expand View' to see more details")
    print("   👆 Double-click any test case row for full details") 
    print("   📉 Toggle between expanded and collapsed views")
    
    root.mainloop()

if __name__ == "__main__":
    main()
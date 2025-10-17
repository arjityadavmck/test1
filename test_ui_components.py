#!/usr/bin/env python3
"""
TestCase Generator UI - Test Script
===================================

Test script to verify all components work without opening the GUI.
Useful for debugging and development.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test all imports work correctly."""
    print("🧪 Testing imports...")
    
    try:
        # Test core imports
        from src.core import chat, pick_requirement, parse_json_safely, to_rows, write_csv
        print("✅ Core imports successful")
        
        # Test integration imports  
        from src.integrations.testrail import map_case_to_testrail_payload, create_case, list_cases, add_result, get_stats
        print("✅ TestRail integration imports successful")
        
        # Test UI imports
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox, scrolledtext
        print("✅ Tkinter imports successful")
        
        # Test threading
        import threading
        print("✅ Threading import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_paths():
    """Test that all required paths exist."""
    print("\n🧪 Testing paths...")
    
    ROOT = Path(__file__).parent
    
    paths_to_check = [
        ROOT / "data" / "requirements",
        ROOT / "src" / "core" / "prompts",
        ROOT / "src" / "integrations",
        ROOT / "outputs" / "testcase_generated"
    ]
    
    all_exist = True
    for path in paths_to_check:
        if path.exists():
            print(f"✅ Path exists: {path.relative_to(ROOT)}")
        else:
            print(f"❌ Path missing: {path.relative_to(ROOT)}")
            all_exist = False
            # Create the directory if it's an output dir
            if "outputs" in str(path):
                path.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created directory: {path.relative_to(ROOT)}")
                all_exist = True  # We fixed it
    
    return all_exist

def test_prompts():
    """Test that prompt files can be loaded."""
    print("\n🧪 Testing prompt files...")
    
    ROOT = Path(__file__).parent
    PROMPTS_DIR = ROOT / "src" / "core" / "prompts"
    
    prompt_files = [
        "testcase_system.txt",
        "testcase_user.txt"
    ]
    
    all_loaded = True
    for prompt_file in prompt_files:
        prompt_path = PROMPTS_DIR / prompt_file
        if prompt_path.exists():
            try:
                content = prompt_path.read_text(encoding="utf-8")
                print(f"✅ Loaded prompt: {prompt_file} ({len(content)} chars)")
            except Exception as e:
                print(f"❌ Error loading {prompt_file}: {e}")
                all_loaded = False
        else:
            print(f"❌ Missing prompt file: {prompt_file}")
            all_loaded = False
    
    return all_loaded

def test_requirements():
    """Test that requirement files exist."""
    print("\n🧪 Testing requirement files...")
    
    ROOT = Path(__file__).parent
    REQ_DIR = ROOT / "data" / "requirements"
    
    if REQ_DIR.exists():
        req_files = list(REQ_DIR.glob("*.txt"))
        print(f"✅ Found {len(req_files)} requirement files:")
        for req_file in req_files[:3]:  # Show first 3
            print(f"   📄 {req_file.name}")
        if len(req_files) > 3:
            print(f"   ... and {len(req_files) - 3} more")
        return len(req_files) > 0
    else:
        print(f"❌ Requirements directory not found: {REQ_DIR}")
        return False

def main():
    """Run all tests."""
    print("🧪 TestCase Generator UI - Component Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_paths, 
        test_prompts,
        test_requirements
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
        print("✅ All tests passed! The UI application should work correctly.")
        print("\n🚀 To launch the UI application, run:")
        print("   python3 launch_ui.py")
    else:
        print("❌ Some tests failed. Please fix the issues before running the UI.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
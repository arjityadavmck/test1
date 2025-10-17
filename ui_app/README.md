# TestCase Generator - Desktop UI Application

A graphical user interface for the TestCase Generator that provides an intuitive way to generate and manage test cases with TestRail integration.

## Features

🎯 **Core Functionality**
- 📄 **File Selection**: Browse and select requirement files with a GUI file picker
- 📋 **Content Preview**: View requirement text before processing
- 🤖 **AI Generation**: Generate test cases using LLM with visual progress tracking
- 📝 **Test Preview**: Display generated test cases in a structured table
- ✅ **Human Approval**: Approve or reject test cases before pushing to TestRail
- 🔗 **TestRail Integration**: Seamlessly push approved test cases to TestRail
- 📊 **Activity Logs**: Real-time logging and status updates

## Screenshot Preview

```
┌─ TestCase Generator - Desktop App ──────────────────────────────┐
│  🤖 TestCase Generator                                           │
├──────────────────────────────────────────────────────────────────┤
│  📄 Requirement File                                            │
│  File: [data/requirements/login.txt        ] [Browse...]        │
├──────────────────────────────────────────────────────────────────┤
│  📋 Requirement Content                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Requirement: The system shall allow users to log in...    │ │
│  │ Details: - If password is incorrect 3 times...            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [🚀 Generate Test Cases] [████████████] Processing...          │
├──────────────────────────────────────────────────────────────────┤
│  📝 Generated Test Cases                                        │
│  ┌─ID──┬─Title──────────┬─Steps────────┬─Expected──┬─Priority─┐ │
│  │TC-01│Login valid creds│Enter user... │User login │High     │ │
│  │TC-02│Login invalid pw │Enter user... │Error shown│High     │ │
│  └─────┴────────────────┴──────────────┴───────────┴─────────┘ │
│                                                                  │
│  🔗 TestRail Integration                                        │
│  [✅ Approve & Push to TestRail] [❌ Reject]                   │
├──────────────────────────────────────────────────────────────────┤
│  📊 Activity Log                                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 2025-10-11 10:30:15 - INFO - 🤖 Starting generation...   │ │
│  │ 2025-10-11 10:30:16 - INFO - ✅ Generated 5 test cases!  │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Install Dependencies
```bash
# Make sure you have the base requirements installed
pip install -r requirements.txt

# Install UI-specific dependencies (optional)
pip install -r ui_app/requirements_ui.txt
```

### 2. Launch the Application
```bash
# Method 1: Using the launcher script
python launch_ui.py

# Method 2: Direct launch
python ui_app/main.py

# Method 3: As a module
python -m ui_app.main
```

### 3. Using the Application

1. **Select Requirement File**: 
   - Click "Browse..." to select a `.txt` requirement file
   - Or use the auto-loaded default from `data/requirements/`

2. **Review Content**: 
   - Check the requirement text in the preview area
   - Edit if needed (changes are temporary)

3. **Generate Test Cases**: 
   - Click "🚀 Generate Test Cases"
   - Watch the progress bar and activity log
   - Generated cases appear in the table

4. **Review & Approve**: 
   - Review the generated test cases in the table
   - Click "✅ Approve & Push to TestRail" to accept
   - Or click "❌ Reject" to discard and try again

5. **Monitor Results**: 
   - Activity log shows real-time status
   - Success messages display TestRail case IDs
   - CSV output saved to `outputs/testcase_generated/`

## Technical Architecture

### Integration with Existing Code
The UI app reuses your existing core functionality:

```python
# Reuses existing modules
from src.core import chat, parse_json_safely, to_rows, write_csv
from src.integrations.testrail import create_case, add_result, get_stats
```

### Threading Model
- **Main Thread**: UI updates and user interactions
- **Background Threads**: LLM calls and TestRail API operations
- **Thread-Safe Logging**: Custom log handler for UI display

### File Structure
```
ui_app/
├── main.py                 # Main application window and logic
├── requirements_ui.txt     # UI-specific dependencies
└── README.md              # This file

launch_ui.py               # Launcher script
```

## Customization Options

### Modify UI Layout
Edit `create_widgets()` method in `ui_app/main.py`:
```python
def create_widgets(self):
    # Add new widgets or modify existing ones
    # Example: Add custom buttons, change colors, etc.
```

### Add New Features
Common extensions:
- **Batch Processing**: Handle multiple requirement files
- **Custom Templates**: User-defined test case templates  
- **Export Options**: PDF, Word, or other formats
- **Settings Panel**: Configure LLM parameters, TestRail settings
- **Dark Mode**: Theme switching capability

### Styling
Modify the ttk.Style configuration:
```python
self.style = ttk.Style()
self.style.theme_use('clam')  # Try: 'vista', 'xpnative', 'winnative'
```

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Solution: Make sure you're in the right directory
cd /path/to/TestTribe_Agentic_AI_Workshop_May2025
python launch_ui.py
```

**2. TestRail Connection Issues**
- Check your TestRail configuration in `src/integrations/testrail.py`
- Verify API credentials and project settings

**3. LLM API Errors**
- Ensure your LLM client is properly configured
- Check API keys and rate limits

**4. UI Freezing**
- The app uses background threads to prevent freezing
- If it still freezes, check the activity log for errors

### Debug Mode
Enable detailed logging by modifying the logging level:
```python
logging.basicConfig(level=logging.DEBUG)  # Instead of INFO
```

## Building Executable (Optional)

To create a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name="TestCaseGenerator" launch_ui.py

# The executable will be in dist/TestCaseGenerator
```

## Comparison with CLI Version

| Feature | CLI Version | Desktop UI |
|---------|-------------|------------|
| File Selection | `--input` argument | GUI file picker |
| Progress Tracking | Console logs | Progress bar + logs |
| Test Case Review | Manual file inspection | Interactive table |
| Approval Process | Command-line prompt | GUI buttons |
| Error Handling | Console output | Dialog boxes |
| Multi-tasking | Blocks terminal | Background processing |
| User Experience | Technical users | All user levels |

The desktop UI provides the same core functionality with a much more user-friendly interface!

## Contributing

To extend the UI application:

1. **Add New Widgets**: Modify `create_widgets()` method
2. **Add Background Tasks**: Use the threading pattern shown
3. **Add Menu Bar**: Create `create_menu()` method
4. **Add Keyboard Shortcuts**: Use `root.bind()` for key bindings
5. **Add Status Bar**: Create bottom status bar with connection info

Remember to test both the functionality and UI responsiveness!
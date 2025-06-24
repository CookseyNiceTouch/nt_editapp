# DaVinci Resolve API Setup Guide

This guide will help you set up DaVinci Resolve API integration following the official [Blackmagic Design documentation](https://resolvedevdoc.readthedocs.io/en/latest/readme_resolveapi.html).

## ⚠️ Critical Requirements

### Python Version Compatibility
- **✅ Supported:** Python 3.6 - 3.11
- **❌ NOT Supported:** Python 3.12+ 
  
**Why?** DaVinci Resolve's API uses the `imp` module which was completely removed in Python 3.12. See [forum discussion](https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=194040) for details.

### Prerequisites
1. **DaVinci Resolve** installed and running
2. **External scripting enabled** (see setup below)
3. **Compatible Python version** (3.6-3.11)

## 🛠️ Setup Steps

### Step 1: Enable External Scripting in DaVinci Resolve

1. Open DaVinci Resolve
2. Go to **DaVinci Resolve** > **Preferences** > **General**
3. Find **"External scripting using"** option
4. Set it to **"Local"** (for same-machine access)
5. **Restart DaVinci Resolve** (important!)

### Step 2: Environment Variables (Handled Automatically)

The `test_basic_connection.py` script automatically sets up the required environment variables:

**Windows:**
```cmd
RESOLVE_SCRIPT_API="%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
RESOLVE_SCRIPT_LIB="C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
PYTHONPATH="%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\"
```

**macOS:**
```bash
RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

**Linux:**
```bash
RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting"
RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

### Step 3: Test Your Setup

Run the basic connection test:
```bash
cd backend/python_services/services/resolveautomation
uv run test_basic_connection.py
```

## 🔧 Troubleshooting

### Common Issues

#### "No module named 'DaVinciResolveScript'"
- **Cause:** Environment variables not set or DaVinci Resolve not installed
- **Solution:** Ensure DaVinci Resolve is installed and running

#### "No module named 'imp'" 
- **Cause:** Using Python 3.12+
- **Solution:** Downgrade to Python 3.6-3.11

#### "Could not connect to DaVinci Resolve instance"
- **Cause:** External scripting not enabled or DaVinci Resolve not running
- **Solution:** 
  1. Ensure DaVinci Resolve is running
  2. Enable external scripting in preferences
  3. Restart DaVinci Resolve

#### "fusionscript.dll not found"
- **Cause:** DaVinci Resolve installation incomplete
- **Solution:** Reinstall DaVinci Resolve or check installation path

### Testing Checklist

✅ Python version 3.6-3.11  
✅ DaVinci Resolve installed and running  
✅ External scripting enabled in preferences  
✅ DaVinci Resolve restarted after enabling scripting  
✅ No firewall blocking the connection  
✅ A project loaded in DaVinci Resolve (recommended)  

## 📁 File Structure

```
resolveautomation/
├── lib/
│   ├── DaVinciResolveScript.py    # API wrapper (modified for local DLL)
│   └── fusionscript.dll           # Local copy of DaVinci Resolve library
├── resolve_api.py                 # Main API class
├── test_resolve_api.py           # Interactive API tester
├── test_basic_connection.py      # Basic connection diagnostic
├── setup_resolve_env.bat         # Windows environment setup
└── SETUP_README.md               # This file
```

## 🚀 Next Steps

Once the connection test passes:

1. **Use `test_resolve_api.py`** for interactive API testing
2. **Use `resolve_api.py`** in your automation scripts
3. **Check the main documentation** for available API functions

## 📚 Official Documentation

- [DaVinci Resolve API Documentation](https://resolvedevdoc.readthedocs.io/en/latest/readme_resolveapi.html)
- [Forum Discussion on Python Compatibility](https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=194040)

## 🆘 Support

If you encounter issues:
1. Run `test_basic_connection.py` for diagnostic information
2. Check the troubleshooting section above
3. Verify all prerequisites are met
4. Check DaVinci Resolve is the Studio version (if using advanced features) 
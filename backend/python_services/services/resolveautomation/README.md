## DaVinci Resolve Scripting API Setup

To use the DaVinci Resolve Scripting API, you need to ensure that your Python environment is correctly configured to find the `DaVinciResolveScript` module. This module is provided by the DaVinci Resolve application and is not a standard Python package.

### Required Environment Variables

Set the following environment variables based on your operating system:

#### Windows

```
RESOLVE_SCRIPT_API="%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
RESOLVE_SCRIPT_LIB="C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
PYTHONPATH="%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\"
```

#### Mac OS X

```
RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

#### Linux

```
RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting"
RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

### Testing the Setup

After setting the environment variables, you can test the setup by running the `test_resolve_api.py` script:

```bash
python test_resolve_api.py
```

Ensure that DaVinci Resolve is running before executing the script.

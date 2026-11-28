# Building UniGame Launcher on Windows

The current application is a Python/Tkinter desktop app. Its runtime UI uses Python's standard library; PyInstaller is needed to package it as a standalone Windows executable.

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer available as `py`
- Internet access for the first PyInstaller installation

## Build

1. Open the repository folder in File Explorer.
2. Double-click `build_windows.bat`, or run it from Command Prompt.
3. Wait for PyInstaller to finish.
4. Find the generated setup executable at `dist\UniGameLauncher-Setup.exe`.

The script calls the existing `--build` entry point in `UniGameLauncher_v1_2.py`. It does not alter user game libraries or settings.

## Troubleshooting

- If `py` is not recognized, install Python and enable the Python Launcher option.
- If PyInstaller fails, read the first traceback above the final build-failed message.
- Remove the local `build` and `dist` folders before a clean rebuild if stale build artifacts are suspected.
- Keep the source file and any future icon assets in the same project folder.

## Stability notes

The current source already scans supported game libraries in a worker thread and renders game cards in small batches. Keep filesystem scanning, network requests, and expensive process inspection off the Tkinter UI thread. UI updates from workers must be scheduled with `root.after(...)`.

# UniGame Launcher

A small Windows game library made as a single Python source file. It can launch games using an executable path or a platform launch URI, including Steam, Epic Games, Roblox, itch.io, and standalone games. Your library is stored locally in `%APPDATA%\\UniGameLauncher\\games.json`.

## Build one portable executable

Install Python 3.10+ for Windows, then install the one build dependency:

```powershell
py -m pip install pyinstaller
```

Run the Python file from a terminal or double-click it:

```powershell
py launcher.py
```

The script builds a single-file, windowed executable at `dist\\UniGameLauncher.exe`. Copy that EXE to another Windows PC to use it; the game files and game launchers themselves are not bundled. The target PC may need the Microsoft Edge WebView2 Runtime only for the old Tauri version; the Python/Tkinter build does not use WebView2.

To run the app from Python without building:

```powershell
py launcher.py --run
```

## Add games

Choose **Add game**, provide a name and platform, and enter an `.exe` path or a launch URI. Steam accepts an app ID (for example `123456`) or `steam://rungameid/123456`. You can also use protocol links such as `roblox://...` or `com.epicgames.launcher://...` where supported by your installed launcher.

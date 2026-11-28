# UniGameLauncher

### One launcher. All your games.

UniGameLauncher is a Windows desktop application designed to bring your gaming library into one convenient place. Automatically discover supported installations, organize your collection, launch games, and track playtime through a clean desktop interface.

## Features

- Automatic game detection and scanning (currently Steam and Epic Games)
- Custom game library management
- Add and remove games
- Game statistics and playtime tracking
- Profiles and wishlists
- Optional cloud/social features
- Per-game launch priority presets
- Customizable settings and JSON backup/restore
- Windows desktop and Start Menu shortcuts through the installer

## Platform and status

- **Platform:** Windows 10 / Windows 11
- **Current source:** Python + Tkinter
- **Status:** In development

## Build on Windows

1. Install Python 3.10 or newer.
2. Run `build_windows.bat`.
3. Find `UniGameLauncher-Setup.exe` in the `dist` folder.

See [BUILD_WINDOWS.md](BUILD_WINDOWS.md) for details and troubleshooting.

## Stability direction

The game scanner runs in a background worker, and library cards are rendered in small batches. Keep disk scans and network calls away from the Tkinter UI thread. A small helper regression-test suite is in `tests/`.

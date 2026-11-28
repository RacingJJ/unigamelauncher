
from __future__ import annotations

import csv
import base64
import ctypes
from ctypes import wintypes
import io
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog


APP_NAME = "UniGame Launcher"
APP_VERSION = "1.3.0"
SUPABASE_URL = "https://lhpfzapygjwxdhggxgkm.supabase.co"
SUPABASE_KEY = "sb_publishable_vv7ItOqJe6I_KeZn0o70Tg_rYV7-X1H"

BG = "#101216"
SIDEBAR = "#171B22"
PANEL = "#202630"
CARD = "#252C36"
BORDER = "#343D49"
TEXT = "#F1F3F6"
MUTED = "#9AA4B2"
ACCENT = "#E65B49"
GREEN = "#55C98B"

# Compact embedded UniGame controller logo (GIF, 64x64).
LOGO_GIF_BASE64 = "R0lGODdhQABAAIYAAAQBAhQVFiYmJyoBDfr6+6mlpzQ2N9TW1uzn6lMFJUdISW4FMLG2tEgDG2dnZ/UTdM/GyrAHUFYpOVRWVpWXl8kGW4YKPB0eIBwiIYiIiXR2dvUEcFMVLcuZrdCmtsq0vG0WOLZHb5UHRNcIY9ISZBEiHT4+QIh7gJNldLB5jDUYJmMpPcMSXNK6w20oQ7aImI5YaLMSVj5BQWs0RpUSSu/a43uHgoJEWKdie7KXospIedzo5P8UgCIVG1Q3RHYaQHZEU5IoVY04VotKYLI6aLlkg9RaisiDnOYpdOe7zOTH0lpiX1xjYWFdX4MQPZZxe68hXrmRncE5b9o9gdNLh9Zul955ot/f4NHi3eQ6feaDq+jY3QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAQABAAEAI/wABCBxIsKDBgwgTKlzIsCHBBAscSlw44EWBAAMHaBRAoYDHjyBDivRoAIDGgQEoeGgwoOGADgpUKAAQIIABAgQyALhQE6MFBDgJONjZE4CAoARC0MQoAKMDBhOMBhBgQMBKhDMKAFBgwgDGgjUFhrVQgwBQnQUVmAWqtGhYsAZMzMwAg+AADwJ4DrTwoCXBtwIcdGQwM6EABgwKOCi51OCDCiibfmgw0MWBAAl8GNi8WQCAAjlOIhwQYcOGBQtGbIjg96BGFAdoct7sIwGAAzMm6t7Nu7fv370TsHgQw/bBBjEekDAO3G6CJF4VKKjas2ZTACI2VPihQoB3ARgwfP8HURqy0Qs8ewqQ3hQCiNYGB4D4sNXzQAEHCGhA6RMozqHVGYVUWxhVBcAEFMgAgAEY0BRVDkLAB8AKWm2G0VekPfBABMwtsIFGOhxwAAQjQmCiiAdgYUVEI4gwUAKlrcacbDNRcMNAHDBAEAsgVFeURwItIIKEFFlggUAaxOZjTRyQINZnK8Q3wAIg/LAAS0Q2J2UDVIKQgGhahinmmGSWaWaYCVTwwAiokcDDCDOemdEKQMCAAgpPcLBABBZkmdAAFkRwJQopoADDDTNw4CdFEAgwgAuK8mddCeJ9Z+ml4JUgQA9SZaSCCy1BsMKiGTWQhHcKMHUAAvupB4AFBSD/RhgAGNSUnqwMEEFrelPhdBkAJpgQQAvv/YmDTlHdhFRQrb7qn1BLhXVUUG0BAAFOOmGUn1BVMXFEli8pIMAEX12YAQUzBejEswA+OS1OBEoL1K8XTmcVZQXlIEMA9v4JQAQqvFrDDggUjACuBiNQlq4BsECqTeJaBV8KQ+2bkXIHhbUAZANI0cHHIHfggRGURRBBtAaJwENEYnk1wQt+cfDBW/+yABZTrH4lkAIZnODzzz5n0ERBE0BLs0AiPIDSZxwINEALDQIQgwSaWmoUAhIYlFoFcb4YAZvxbRHVpeLZTFML+Dr9wgFLlGsAA0pE6hBEEg3QgAcQkCtQCQ4c/xAFqXIGLvjghBdu+OGIJ6744gilqSGcjCck3GMzOr5c5AkkxxpDA9DwAAtf+gXmbwOgAEEBFGRggwY2tICCBLC7sALstNdO+wou0A7EBxSwfm4BEKQwukMoaOUCFVkgQUIFJ2spQgUjPIDEFEEAQAHMdQ9xmXWYYrQADSqUQCmm3mEgvgo0uDjVd52VgBEDwnM+QBEUHCjsktYFiVoCtqKHXgBTQo1AvFMUnpXEAFHRwLcoEgKtTMA+08qWrQBAA6QMpSkBuICAgqKDaBUoKBeKSgaKsCj50CdiB7iCfxCwqnb9JCgAKsq7kkKTAxHgAIwBgANuuJ7PRMg1d9mMCf+M4hEGAOV0s+oPDD24QXjVcIcIUBCSeIiBVH2gayY51oF0djX98MdZSwzQDOM1wHlxMVUOiF9BEjAzueTQIAF6IU6iUq4m0tBHW6FASb6ynpkwAAQGOcF+puOVvxRlASrwXg0M5sWBKCBhd+xBRPA4kM2k6mXwGcDMDDCdgyTgeRsAQAP6MgAj7ABFqzIYKneghYg8ICLQE9RBBNAVAHygaQOBgU7ERZAFaIhlBfEQiEiESlRWgTLM86SbXFTDHmogBRmByVQIQgKl3YyLTktAA7bJTZbA8WgCiUBfmkmVDvilATPTi0leeTNgkYgBFBAMAUbykYMJhgEjimFBBvCoAObU6pYCkRlBRgmftxxgKMAxAAI8U5SBkIBlGClAlADAgRa8iAT402FsvMYhzplsRqjzYE9iAEwGZM0kHdgPB6BQqe9oqy4IscAGIPeiCmyAmQeZwUIXZCkMBAGQDvCAXVIAgQFSxT4UaMHwjmNT7aTtTy/RkVG+IxAGYM8uAxiCB5RgIgi0IAXelJNGcIC3rnrgBkvdp0YAV6a1Ru6tcI2rXOdKuIAAADs="

SOURCES = [
    "Steam", "Epic Games", "Ubisoft Connect", "EA App",
    "Xbox", "GOG", "Roblox", "itch.io", "Standalone"
]

PERFORMANCE_MODES = ["Quiet", "Balanced", "Performance"]

APPDATA = Path(os.environ.get("APPDATA", Path.home())) / "UniGameLauncher"
INSTALL_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Programs" / "UniGameLauncher"
INSTALLED_EXE = INSTALL_DIR / "UniGameLauncher.exe"
DATA_FILE = APPDATA / "data.json"
SETTINGS_FILE = APPDATA / "settings.json"


def ensure_data_folder():
    APPDATA.mkdir(parents=True, exist_ok=True)


def format_time(seconds):
    seconds = max(0, int(seconds or 0))
    hours, remainder = divmod(seconds, 3600)
    minutes = remainder // 60
    return f"{hours}h {minutes}m" if hours else f"{minutes}m"


def default_profile(name="Player"):
    return {
        "name": name,
        "games": [],
        "wishlist": [],
        "created": datetime.now().isoformat(timespec="minutes")
    }


def default_data():
    return {
        "active_profile": "Player",
        "profiles": {"Player": default_profile()}
    }


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return default


def save_json(path, data):
    ensure_data_folder()
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    temporary.replace(path)


# ============================================================
# SUPABASE ONLINE SERVICES
# ============================================================

def protect_local_secret(value):
    """Encrypt a small local session blob with Windows DPAPI when available."""
    raw = json.dumps(value).encode("utf-8")
    if os.name != "nt":
        return "plain:" + base64.b64encode(raw).decode("ascii")
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]
    source_buffer = ctypes.create_string_buffer(raw)
    source = DATA_BLOB(len(raw), ctypes.cast(source_buffer, ctypes.POINTER(ctypes.c_byte)))
    output = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptProtectData(ctypes.byref(source), None, None, None, None, 0, ctypes.byref(output)):
        raise OSError("Windows could not protect the sign-in session.")
    try:
        encrypted = ctypes.string_at(output.pbData, output.cbData)
        return "dpapi:" + base64.b64encode(encrypted).decode("ascii")
    finally:
        ctypes.windll.kernel32.LocalFree(output.pbData)


def unprotect_local_secret(value):
    if not value:
        return {}
    mode, _, encoded = value.partition(":")
    encrypted = base64.b64decode(encoded)
    if mode == "plain":
        return json.loads(encrypted.decode("utf-8"))
    if mode != "dpapi" or os.name != "nt":
        raise ValueError("This saved sign-in session cannot be decrypted on this device.")
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]
    source_buffer = ctypes.create_string_buffer(encrypted)
    source = DATA_BLOB(len(encrypted), ctypes.cast(source_buffer, ctypes.POINTER(ctypes.c_byte)))
    output = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(source), None, None, None, None, 0, ctypes.byref(output)):
        raise OSError("Windows could not unlock the saved sign-in session.")
    try:
        raw = ctypes.string_at(output.pbData, output.cbData)
        return json.loads(raw.decode("utf-8"))
    finally:
        ctypes.windll.kernel32.LocalFree(output.pbData)


class SupabaseClient:
    """Small Supabase Auth + PostgREST client using only the standard library."""
    def __init__(self, settings):
        self.settings = settings
        try:
            self.session = unprotect_local_secret(settings.get("cloud_session_protected")) if settings.get("cloud_session_protected") else (settings.get("cloud_session") or {})
        except Exception:
            self.session = {}

    @property
    def user(self):
        return self.session.get("user") or {}

    @property
    def user_id(self):
        return self.user.get("id")

    @property
    def access_token(self):
        return self.session.get("access_token")

    @property
    def logged_in(self):
        return bool(self.access_token and self.user_id)

    def _request(self, path, method="GET", payload=None, token=None, prefer=None):
        url = SUPABASE_URL.rstrip("/") + path
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": "Bearer " + (token or self.access_token or SUPABASE_KEY),
            "Content-Type": "application/json",
        }
        if prefer:
            headers["Prefer"] = prefer
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(detail)
                detail = parsed.get("msg") or parsed.get("message") or parsed.get("error_description") or detail
            except ValueError:
                pass
            raise RuntimeError(f"Supabase returned {error.code}: {detail}") from None
        except (urllib.error.URLError, TimeoutError) as error:
            raise RuntimeError(f"Could not reach Supabase: {error}") from None

    def _save_session(self, session):
        self.session = session or {}
        self.settings["cloud_session_protected"] = protect_local_secret(self.session) if self.session else ""
        self.settings.pop("cloud_session", None)
        save_json(SETTINGS_FILE, self.settings)

    def signup(self, email, password):
        result = self._request("/auth/v1/signup", "POST", {"email": email, "password": password}, token=SUPABASE_KEY)
        if result and result.get("access_token"):
            self._save_session(result)
        return result

    def login(self, email, password):
        result = self._request("/auth/v1/token?grant_type=password", "POST", {"email": email, "password": password}, token=SUPABASE_KEY)
        self._save_session(result)
        return result

    def logout(self):
        try:
            if self.access_token:
                self._request("/auth/v1/logout", "POST", {}, token=self.access_token)
        finally:
            self._save_session({})

    def _refresh_session(self):
        refresh_token = self.session.get("refresh_token")
        if not refresh_token:
            raise RuntimeError("Your online session expired. Please sign in again.")
        refreshed = self._request("/auth/v1/token?grant_type=refresh_token", "POST", {"refresh_token": refresh_token}, token=SUPABASE_KEY)
        self._save_session(refreshed)

    def rest(self, table, query="", method="GET", payload=None, prefer=None):
        expires_at = self.session.get("expires_at")
        if self.access_token and expires_at:
            try:
                if float(expires_at) <= time.time() + 60:
                    self._refresh_session()
            except (TypeError, ValueError):
                pass
        return self._request(f"/rest/v1/{table}{query}", method, payload, prefer=prefer)

    def ensure_profile(self, username):
        payload = {"id": self.user_id, "username": username, "display_name": username}
        return self.rest("profiles", "?on_conflict=id", "POST", payload, "resolution=merge-duplicates,return=representation")


# ============================================================
# INSTALLER
# ============================================================

class Installer:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Install UniGame Launcher")
        self.root.geometry("640x500")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.install_location = tk.StringVar(value=str(INSTALL_DIR))
        self.desktop_shortcut = tk.BooleanVar(value=True)
        self.start_menu_shortcut = tk.BooleanVar(value=True)
        self.launch_after = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Ready to install")

        self.build_ui()

    def label(self, parent, text, size=10, color=TEXT, bold=False, **kwargs):
        return tk.Label(
            parent,
            text=text,
            bg=kwargs.pop("bg", BG),
            fg=color,
            font=("Segoe UI", size, "bold" if bold else "normal"),
            **kwargs
        )

    def button(self, parent, text, command, primary=False):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=ACCENT if primary else CARD,
            fg=TEXT,
            activebackground="#F06C59" if primary else "#333D4A",
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            padx=22 if primary else 18,
            pady=12 if primary else 10,
            cursor="hand2",
            font=("Segoe UI", 10 if primary else 9, "bold")
        )

    def build_ui(self):
        header = tk.Frame(self.root, bg=SIDEBAR, height=112)
        header.pack(fill="x")
        header.pack_propagate(False)

        self.label(
            header, "U", 27, "white", True, bg=ACCENT,
            width=2, pady=5
        ).pack(side="left", padx=(28, 14), pady=25)

        heading = tk.Frame(header, bg=SIDEBAR)
        heading.pack(side="left", pady=25)
        self.label(heading, "UniGame Launcher", 21, bold=True, bg=SIDEBAR).pack(anchor="w")
        self.label(heading, "Setup wizard", 9, MUTED, bg=SIDEBAR).pack(anchor="w")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=32, pady=24)

        self.label(body, "Install UniGame Launcher", 18, bold=True).pack(anchor="w")
        self.label(
            body,
            "Choose where the app should be installed. Your library and profiles will be kept in your user data folder.",
            9, MUTED, wraplength=560, justify="left"
        ).pack(anchor="w", pady=(6, 20))

        self.label(body, "INSTALL LOCATION", 8, MUTED, True).pack(anchor="w")
        location_row = tk.Frame(body, bg=BG)
        location_row.pack(fill="x", pady=(7, 20))

        tk.Entry(
            location_row,
            textvariable=self.install_location,
            bg=PANEL, fg=TEXT, insertbackground=TEXT,
            relief="flat", font=("Segoe UI", 10)
        ).pack(side="left", fill="x", expand=True, ipady=10)

        self.button(location_row, "Browse", self.browse).pack(side="left", padx=(9, 0))

        self.label(body, "SHORTCUTS", 8, MUTED, True).pack(anchor="w", pady=(0, 7))
        for caption, variable in (
            ("Create Desktop shortcut", self.desktop_shortcut),
            ("Create Start Menu shortcut", self.start_menu_shortcut),
            ("Launch UniGame Launcher after installation", self.launch_after),
        ):
            tk.Checkbutton(
                body, text=caption, variable=variable,
                bg=BG, fg=TEXT, selectcolor=PANEL,
                activebackground=BG, activeforeground=TEXT,
                font=("Segoe UI", 9), anchor="w"
            ).pack(anchor="w", pady=2)

        footer = tk.Frame(self.root, bg=SIDEBAR)
        footer.pack(side="bottom", fill="x")

        status_row = tk.Frame(footer, bg=SIDEBAR)
        status_row.pack(side="left", fill="x", expand=True, padx=20, pady=12)
        self.status_label = tk.Label(
            status_row, textvariable=self.status_var,
            bg=SIDEBAR, fg=MUTED, font=("Segoe UI", 8)
        )
        self.status_label.pack(anchor="w")
        self.progress = ttk.Progressbar(
            status_row, mode="indeterminate", length=180
        )
        self.progress.pack(anchor="w", pady=(5, 0))

        buttons = tk.Frame(footer, bg=SIDEBAR)
        buttons.pack(side="right", padx=20, pady=13)

        self.button(buttons, "Cancel", self.root.destroy).pack(side="right")
        self.install_button = self.button(
            buttons, "Install now", self.install, primary=True
        )
        self.install_button.pack(side="right", padx=(0, 9))

    def browse(self):
        folder = filedialog.askdirectory(
            title="Choose installation folder",
            initialdir=self.install_location.get()
        )
        if folder:
            self.install_location.set(folder)

    def create_shortcut(self, shortcut_path, target):
        shortcut_path.parent.mkdir(parents=True, exist_ok=True)

        escaped_target = str(target).replace("'", "''")
        escaped_link = str(shortcut_path).replace("'", "''")
        script = (
            "$w=New-Object -ComObject WScript.Shell;"
            f"$s=$w.CreateShortcut('{escaped_link}');"
            f"$s.TargetPath='{escaped_target}';"
            "$s.Arguments='--installed';"
            "$s.WorkingDirectory=Split-Path $s.TargetPath;"
            "$s.Description='UniGame Launcher';"
            "$s.Save()"
        )

        subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )

    def install(self):
        if not getattr(sys, "frozen", False):
            messagebox.showerror(
                "Installer build required",
                "Build the setup EXE first, then open UniGameLauncher-Setup.exe to install it."
            )
            return

        source = Path(sys.executable).resolve()
        destination_folder = Path(self.install_location.get().strip()).expanduser()

        if not destination_folder.is_absolute():
            messagebox.showerror(
                "Invalid location", "Choose an absolute installation path.",
                parent=self.root
            )
            return

        destination = destination_folder / "UniGameLauncher.exe"
        make_desktop = self.desktop_shortcut.get()
        make_start = self.start_menu_shortcut.get()
        launch_after = self.launch_after.get()

        self.install_button.configure(state="disabled", text="Installing...")
        self.status_var.set("Copying application files...")
        self.progress.start(10)

        def worker():
            try:
                destination_folder.mkdir(parents=True, exist_ok=True)
                if source != destination.resolve():
                    shutil.copy2(source, destination)

                ensure_data_folder()

                if make_desktop:
                    desktop = Path.home() / "Desktop"
                    self.create_shortcut(
                        desktop / "UniGame Launcher.lnk", destination
                    )

                if make_start:
                    programs = (
                        Path(os.environ.get("APPDATA", Path.home()))
                        / "Microsoft" / "Windows" / "Start Menu" / "Programs"
                    )
                    self.create_shortcut(
                        programs / "UniGame Launcher.lnk", destination
                    )

                self.root.after(
                    0, lambda: self.install_complete(destination, launch_after)
                )
            except Exception as error:
                self.root.after(0, lambda err=str(error): self.install_failed(err))

        threading.Thread(
            target=worker, daemon=True, name="UniGameInstaller"
        ).start()

    def install_complete(self, destination, launch_after):
        self.progress.stop()
        self.status_var.set("Installation complete")
        messagebox.showinfo(
            "Installation complete",
            f"UniGame Launcher was installed successfully at:\n{destination}",
            parent=self.root
        )
        if launch_after:
            try:
                subprocess.Popen([str(destination), "--installed"])
            except OSError as error:
                messagebox.showerror(
                    "Could not launch", str(error), parent=self.root
                )
                return
        self.root.destroy()

    def install_failed(self, error):
        self.progress.stop()
        self.status_var.set("Installation failed")
        self.install_button.configure(state="normal", text="Try again")
        messagebox.showerror(
            "Installation failed",
            f"UniGame could not finish installing:\n\n{error}",
            parent=self.root
        )

    def run(self):
        self.root.mainloop()


# ============================================================
# MAIN APPLICATION
# ============================================================

class Launcher:

    def __init__(self):
        global ACCENT
        ensure_data_folder()

        self.data = load_json(DATA_FILE, default_data())
        self.settings = load_json(SETTINGS_FILE, {
            "theme": "Dark",
            "accent": ACCENT,
            "auto_scan": True,
            "performance_mode": "Balanced",
            "confirm_remove": True,
            "boot_animation": "Pulse"
        })
        ACCENT = self.settings.get("accent", ACCENT)
        self.cloud = SupabaseClient(self.settings)
        self.cloud_profile = None
        self.cloud_friends = []
        self.cloud_requests = []
        self.cloud_busy = False

        if not isinstance(self.data, dict):
            self.data = default_data()

        if "profiles" not in self.data or not self.data["profiles"]:
            self.data = default_data()

        self.active_profile = self.data.get("active_profile", "Player")
        if self.active_profile not in self.data["profiles"]:
            self.active_profile = next(iter(self.data["profiles"]))

        self.profile = self.data["profiles"][self.active_profile]
        self.profile.setdefault("games", [])
        self.profile.setdefault("wishlist", [])

        self.games = self.profile["games"]
        self.wishlist = self.profile["wishlist"]

        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} {APP_VERSION}")
        self.root.geometry("1250x790")
        self.root.minsize(950, 620)
        self.root.configure(bg=BG)
        try:
            self.root.iconphoto(True, tk.PhotoImage(data=LOGO_GIF_BASE64))
        except tk.TclError:
            pass

        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.profile_var = tk.StringVar(value=self.active_profile)
        self.mode_var = tk.StringVar(
            value=self.settings.get("performance_mode", "Balanced")
        )

        self.current_page = "Library"
        self.selected_index = None
        self._closing = False
        self._scan_running = False
        self._playtime_running = False
        self._tracked_processes = {}
        self._last_playtime_save = 0.0
        self._search_after = None
        self._library_render_after = None
        self._library_render_token = 0
        self._library_canvas = None

        self.setup_style()
        self.build_layout()
        self.show_page("Library")
        if self.settings.get("boot_animation", "Pulse") != "Off":
            self.show_boot_animation()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        if self.settings.get("auto_scan", True):
            self.root.after(1800, self.scan_games)

        self.root.after(5000, self.update_playtime)
        if self.cloud.logged_in:
            self.root.after(60000, self.presence_heartbeat)

    # --------------------------------------------------------
    # PERSISTENCE
    # --------------------------------------------------------

    def save_all(self):
        self.profile["games"] = self.games
        self.profile["wishlist"] = self.wishlist
        self.data["active_profile"] = self.active_profile
        self.data["profiles"][self.active_profile] = self.profile

        save_json(DATA_FILE, self.data)
        save_json(SETTINGS_FILE, self.settings)

    def switch_profile(self, name):
        if name not in self.data["profiles"]:
            return

        self.save_all()
        self.active_profile = name
        self.profile = self.data["profiles"][name]
        self.games = self.profile.setdefault("games", [])
        self.wishlist = self.profile.setdefault("wishlist", [])
        self.data["active_profile"] = name
        self.selected_index = None
        self.profile_var.set(name)
        self.show_page("Library")

    def create_profile(self):
        name = simpledialog.askstring(
            "New profile", "Enter a profile name:", parent=self.root
        )
        if not name:
            return

        name = name.strip()
        if not name:
            return

        if name in self.data["profiles"]:
            messagebox.showwarning("Profile exists", "That profile already exists.")
            return

        self.save_all()
        self.data["profiles"][name] = default_profile(name)
        self.switch_profile(name)

    def rename_profile(self):
        name = simpledialog.askstring(
            "Rename profile",
            "New profile name:",
            initialvalue=self.active_profile,
            parent=self.root
        )
        if not name:
            return

        name = name.strip()
        if not name or name in self.data["profiles"]:
            messagebox.showwarning("Invalid name", "Choose a different profile name.")
            return

        self.save_all()
        self.data["profiles"][name] = self.data["profiles"].pop(self.active_profile)
        self.data["profiles"][name]["name"] = name
        self.active_profile = name
        self.profile = self.data["profiles"][name]
        self.profile_var.set(name)
        self.save_all()
        self.show_page("Profiles")

    def delete_profile(self):
        if len(self.data["profiles"]) <= 1:
            messagebox.showwarning("Cannot delete", "You must keep at least one profile.")
            return

        if not messagebox.askyesno(
            "Delete profile",
            f"Delete profile '{self.active_profile}' and its library?"
        ):
            return

        del self.data["profiles"][self.active_profile]
        self.active_profile = next(iter(self.data["profiles"]))
        self.profile = self.data["profiles"][self.active_profile]
        self.games = self.profile.setdefault("games", [])
        self.wishlist = self.profile.setdefault("wishlist", [])
        self.profile_var.set(self.active_profile)
        self.save_all()
        self.show_page("Profiles")

    # --------------------------------------------------------
    # STYLING AND LAYOUT
    # --------------------------------------------------------

    def setup_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground=PANEL,
            background=PANEL,
            foreground=TEXT,
            arrowcolor=TEXT
        )
        style.configure(
            "TNotebook",
            background=BG,
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            background=PANEL,
            foreground=TEXT,
            padding=(12, 7)
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", ACCENT)]
        )
        style.configure(
            "Vertical.TScrollbar",
            background=PANEL,
            troughcolor=BG,
            bordercolor=BG,
            arrowcolor=MUTED
        )

    def label(self, parent, text, size=10, color=TEXT, bold=False, bg=None, **kwargs):
        return tk.Label(
            parent,
            text=text,
            bg=bg or BG,
            fg=color,
            font=("Segoe UI", size, "bold" if bold else "normal"),
            **kwargs
        )

    def button(self, parent, text, command, primary=False):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=ACCENT if primary else CARD,
            fg=TEXT,
            activebackground="#F06C59" if primary else "#333D49",
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            padx=14,
            pady=9,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        )

    def build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=226)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=18, pady=(23, 30))
        mark = tk.Frame(brand, bg="#090A0D", width=46, height=46)
        mark.pack(side="left", padx=(0, 10))
        mark.pack_propagate(False)
        self.logo_image = tk.PhotoImage(data=LOGO_GIF_BASE64).subsample(2, 2)
        tk.Label(mark, image=self.logo_image, bg="#090A0D", bd=0).place(relx=.5, rely=.5, anchor="center")
        brand_text = tk.Frame(brand, bg=SIDEBAR)
        brand_text.pack(side="left")
        self.label(brand_text, "UniGame", 15, TEXT, True, bg=SIDEBAR).pack(anchor="w")
        self.label(brand_text, "GAME LIBRARY", 7, MUTED, True, bg=SIDEBAR).pack(anchor="w", pady=(1, 0))

        self.label(self.sidebar, "YOUR SPACE", 8, MUTED, True, bg=SIDEBAR).pack(anchor="w", padx=20, pady=(0, 9))
        self.nav = {}
        for name, symbol in [
            ("Library", "▦"), ("Wishlist", "♡"), ("Store", "⌕"),
            ("Statistics", "▥"), ("Profiles", "◉"), ("Social", "◎"),
            ("Performance", "ϟ"), ("Settings", "⚙")
        ]:
            self.add_nav(name, symbol)

        self.label(self.sidebar, "MANAGE", 8, MUTED, True, bg=SIDEBAR).pack(anchor="w", padx=20, pady=(24, 9))
        self.add_nav("Scan PC", "↻")
        self.add_nav("Add game", "+")

        bottom = tk.Frame(self.sidebar, bg=SIDEBAR)
        bottom.pack(side="bottom", fill="x", padx=15, pady=16)
        tk.Frame(bottom, bg=BORDER, height=1).pack(fill="x", pady=(0, 13))
        self.label(bottom, "CURRENT PROFILE", 7, MUTED, True, bg=SIDEBAR).pack(anchor="w", padx=3)
        self.profile_box = ttk.Combobox(
            bottom, textvariable=self.profile_var,
            values=list(self.data["profiles"]), state="readonly"
        )
        self.profile_box.pack(fill="x", pady=(7, 0), ipady=4)
        self.profile_box.bind("<<ComboboxSelected>>", lambda event: self.switch_profile(self.profile_var.get()))

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        top = tk.Frame(self.main, bg=BG, height=76)
        top.pack(fill="x", padx=30)
        top.pack_propagate(False)
        top_left = tk.Frame(top, bg=BG)
        top_left.pack(side="left", fill="y")
        self.label(top_left, "UNIGAME LAUNCHER  /  DESKTOP", 8, MUTED, True).pack(anchor="w", pady=(17, 2))
        self.label(top_left, "Your games, organized.", 12, TEXT, True).pack(anchor="w")

        search_wrap = tk.Frame(top, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        search_wrap.pack(side="right", pady=17)
        self.label(search_wrap, "⌕", 14, MUTED, True, bg=PANEL).pack(side="left", padx=(11, 5))
        self.search_entry = tk.Entry(
            search_wrap, textvariable=self.search_var, bg=PANEL, fg=TEXT,
            insertbackground=TEXT, relief="flat", width=27, font=("Segoe UI", 10),
            highlightthickness=0, bd=0
        )
        self.search_entry.pack(side="left", padx=(0, 12), ipady=9)
        self.search_entry.insert(0, "Search games...")
        self.search_entry.bind("<FocusIn>", self.search_focus)
        self.search_entry.bind("<FocusOut>", self.search_blur)
        self.search_entry.bind("<KeyRelease>", self.on_search_key)

        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=30, pady=(0, 12))
        self.root.bind_all("<MouseWheel>", self.on_mousewheel)

        footer = tk.Frame(self.main, bg=SIDEBAR, height=29)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)
        self.label(footer, APP_NAME + "  ·  " + APP_VERSION, 8, MUTED, bg=SIDEBAR).pack(side="left", padx=14)
        self.status_label = tk.Label(
            footer, textvariable=self.status_var, bg=SIDEBAR,
            fg=MUTED, font=("Segoe UI", 8)
        )
        self.status_label.pack(side="right", padx=14)

    def add_nav(self, name, symbol):
        button = tk.Button(
            self.sidebar, text=f"  {symbol}     {name}",
            command=lambda n=name: self.navigate(n), anchor="w",
            bg=SIDEBAR, fg=MUTED, activebackground=CARD,
            activeforeground=TEXT, relief="flat", bd=0,
            padx=14, pady=11, cursor="hand2",
            font=("Segoe UI", 9, "bold")
        )
        button.pack(fill="x", padx=10, pady=2)
        self.nav[name] = button

    def search_focus(self, _event):
        if self.search_entry.get().strip().lower() in ("search...", "search games..."):
            self.search_entry.delete(0, "end")
            self.search_entry.configure(fg=TEXT)

    def search_blur(self, _event):
        if not self.search_entry.get().strip():
            self.search_entry.insert(0, "Search games...")
            self.search_entry.configure(fg=MUTED)

    def search_query(self):
        value = self.search_var.get().strip().lower()
        return "" if value in ("search...", "search games...") else value

    def navigate(self, page):
        if page == "Add game":
            self.game_form()
            return
        if page == "Scan PC":
            self.scan_games()
            return
        self.show_page(page)

    def on_search_key(self, _event=None):
        if self._search_after is not None:
            try:
                self.root.after_cancel(self._search_after)
            except tk.TclError:
                pass
        self._search_after = self.root.after(220, self.refresh_current)

    def refresh_current(self):
        self._search_after = None
        self.show_page(self.current_page)

    def on_mousewheel(self, event):
        canvas = self._library_canvas
        if canvas is not None:
            try:
                canvas.yview_scroll(int(-event.delta / 120), "units")
            except tk.TclError:
                self._library_canvas = None

    def show_page(self, page):
        if self._library_render_after is not None:
            try:
                self.root.after_cancel(self._library_render_after)
            except tk.TclError:
                pass
            self._library_render_after = None
        self._library_render_token += 1
        self._library_canvas = None
        self.current_page = page

        for name, button in self.nav.items():
            button.configure(
                bg=CARD if name == page else SIDEBAR,
                fg=TEXT if name == page else MUTED
            )

        for widget in self.content.winfo_children():
            widget.destroy()

        pages = {
            "Library": self.page_library,
            "Wishlist": self.page_wishlist,
            "Store": self.page_store,
            "Statistics": self.page_statistics,
            "Profiles": self.page_profiles,
            "Social": self.page_social,
            "Performance": self.page_performance,
            "Settings": self.page_settings
        }

        pages.get(page, self.page_library)()

    def page_heading(self, eyebrow, title, description=""):
        self.label(self.content, eyebrow.upper(), 8, MUTED, True).pack(anchor="w", pady=(13, 4))
        self.label(self.content, title, 24, bold=True).pack(anchor="w")
        if description:
            self.label(self.content, description, 9, MUTED).pack(anchor="w", pady=(4, 15))

    def section_card(self, parent=None):
        return tk.Frame(
            parent or self.content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=17,
            pady=15
        )

    # --------------------------------------------------------
    # GAME LIBRARY
    # --------------------------------------------------------

    def page_library(self):
        total = len(self.games)
        total_seconds = sum(int(game.get("play_seconds", 0) or 0) for game in self.games)
        total_launches = sum(int(game.get("launches", 0) or 0) for game in self.games)

        heading = tk.Frame(self.content, bg=BG)
        heading.pack(fill="x", pady=(15, 16))
        heading_left = tk.Frame(heading, bg=BG)
        heading_left.pack(side="left")
        self.label(heading_left, "YOUR COLLECTION", 8, ACCENT, True).pack(anchor="w")
        self.label(heading_left, "Game library", 25, TEXT, True).pack(anchor="w", pady=(3, 0))
        self.label(heading_left, f"Everything you play, all in one place · {self.active_profile}", 9, MUTED).pack(anchor="w", pady=(4, 0))
        self.button(heading, "+ Add game", self.game_form, True).pack(side="right", padx=(8, 0), pady=13)
        self.button(heading, "↻ Scan PC", self.scan_games).pack(side="right", pady=13)

        hero = tk.Frame(self.content, bg="#202936", highlightbackground="#344151", highlightthickness=1)
        hero.pack(fill="x", pady=(0, 15))
        hero_left = tk.Frame(hero, bg="#202936")
        hero_left.pack(side="left", fill="both", expand=True, padx=21, pady=18)
        self.label(hero_left, "READY WHEN YOU ARE", 8, "#F18A79", True, bg="#202936").pack(anchor="w")
        self.label(hero_left, "Pick up where you left off.", 17, TEXT, True, bg="#202936").pack(anchor="w", pady=(5, 3))
        self.label(hero_left, "Launch a game or add something new to your collection.", 9, "#B3BDCA", bg="#202936").pack(anchor="w")
        hero_mark = tk.Frame(hero, bg="#090A0D", width=104, height=90)
        hero_mark.pack(side="right", padx=20, pady=12)
        hero_mark.pack_propagate(False)
        self.logo_large = tk.PhotoImage(data=LOGO_GIF_BASE64)
        tk.Label(hero_mark, image=self.logo_large, bg="#090A0D", bd=0).place(relx=.5, rely=.5, anchor="center")

        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill="x", pady=(0, 17))
        stat_values = [
            ("GAMES", str(total)),
            ("TOTAL PLAYTIME", format_time(total_seconds)),
            ("LAUNCHES", str(total_launches)),
            ("WISHLIST", str(len(self.wishlist)))
        ]
        for index, (caption, value) in enumerate(stat_values):
            tile = tk.Frame(stats, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, padx=14, pady=10)
            tile.pack(side="left", fill="x", expand=True, padx=(0 if index == 0 else 7, 7 if index < 3 else 0))
            self.label(tile, caption, 7, MUTED, True, bg=PANEL).pack(anchor="w")
            self.label(tile, value, 16, TEXT, True, bg=PANEL).pack(anchor="w", pady=(4, 0))

        toolbar = tk.Frame(self.content, bg=BG)
        toolbar.pack(fill="x", pady=(0, 9))
        self.label(toolbar, "ALL GAMES", 9, TEXT, True).pack(side="left")
        query = self.search_query()
        visible = [
            (i, game) for i, game in enumerate(self.games)
            if query in game.get("title", "").lower()
            or query in game.get("source", "").lower()
            or query in game.get("category", "").lower()
        ]
        self.label(toolbar, f"{len(visible)} shown", 8, MUTED).pack(side="right")

        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
        container = tk.Frame(canvas, bg=BG)
        container.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        window = canvas.create_window((0, 0), window=container, anchor="nw")
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window, width=event.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self._library_canvas = canvas

        if not visible:
            empty = tk.Frame(container, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, padx=25, pady=28)
            empty.pack(fill="x", pady=12)
            title = "No games match your search" if self.games else "Your library is ready for its first game"
            subtitle = "Try another title, or clear the search field." if self.games else "Add a game manually or scan your PC to find installed games."
            self.label(empty, title, 14, TEXT, True, bg=PANEL).pack()
            self.label(empty, subtitle, 9, MUTED, bg=PANEL).pack(pady=(7, 13))
            self.button(empty, "+ Add your first game", self.game_form, True).pack()
            return

        self.render_game_cards(container, visible, self._library_render_token, start=0)

    def render_game_cards(self, parent, visible, token, start=0):
        if self._closing or token != self._library_render_token:
            return

        # Add cards in small batches so large libraries do not freeze the UI.
        stop = min(start + 18, len(visible))
        for index, game in visible[start:stop]:
            self.game_card(parent, index, game)

        if stop < len(visible):
            self._library_render_after = self.root.after(
                1, lambda: self.render_game_cards(
                    parent, visible, token, start=stop
                )
            )
        else:
            self._library_render_after = None

    def game_card(self, parent, index, game):
        card = tk.Frame(
            parent, bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill="x", pady=4)

        icon = tk.Frame(card, bg="#374252", width=54, height=54)
        icon.pack(side="left", padx=13, pady=10)
        icon.pack_propagate(False)

        self.label(
            icon, game.get("title", "?")[:1].upper(),
            20, TEXT, True, bg="#374252"
        ).place(relx=.5, rely=.5, anchor="center")

        details = tk.Frame(card, bg=CARD)
        details.pack(side="left", fill="both", expand=True, pady=11)

        self.label(
            details, game.get("title", "Untitled"),
            10, TEXT, True, bg=CARD
        ).pack(anchor="w")

        self.label(
            details,
            f"{game.get('source', 'PC')}  ·  {game.get('category', 'Uncategorized')}",
            8, MUTED, bg=CARD
        ).pack(anchor="w", pady=(4, 0))

        self.label(
            card, format_time(game.get("play_seconds", 0)),
            9, MUTED, bg=CARD
        ).pack(side="right", padx=12)

        self.button(
            card, "Details",
            lambda i=index: self.game_details(i)
        ).pack(side="right", padx=6, pady=13)

        self.button(
            card, "Play",
            lambda i=index: self.play_game(i),
            True
        ).pack(side="right", padx=7, pady=13)

    def game_details(self, index):
        game = self.games[index]

        dialog = tk.Toplevel(self.root)
        dialog.title(game.get("title", "Game details"))
        dialog.geometry("470x490")
        dialog.configure(bg=BG)
        dialog.transient(self.root)

        self.label(
            dialog, game.get("title", "Game"),
            21, TEXT, True
        ).pack(anchor="w", padx=22, pady=(22, 4))

        self.label(
            dialog, game.get("source", "PC"),
            9, MUTED
        ).pack(anchor="w", padx=22)

        info = tk.Frame(dialog, bg=PANEL, padx=18, pady=16)
        info.pack(fill="x", padx=20, pady=20)

        for heading, value in [
            ("PLAYTIME", format_time(game.get("play_seconds", 0))),
            ("LAUNCHES", str(game.get("launches", 0))),
            ("LAST PLAYED", game.get("last_played", "Never")),
            ("CATEGORY", game.get("category", "Uncategorized")),
            ("PROCESS", game.get("process_name", "Not set")),
            ("PERFORMANCE", game.get("performance_mode", "Default"))
        ]:
            line = tk.Frame(info, bg=PANEL)
            line.pack(fill="x", pady=5)
            self.label(line, heading, 8, MUTED, True, bg=PANEL).pack(side="left")
            self.label(line, value, 9, TEXT, bg=PANEL).pack(side="right")

        buttons = tk.Frame(dialog, bg=BG)
        buttons.pack(fill="x", padx=20, pady=5)

        self.button(
            buttons, "Play", lambda: [dialog.destroy(), self.play_game(index)], True
        ).pack(side="left")

        self.button(
            buttons, "Edit", lambda: [dialog.destroy(), self.game_form(index)]
        ).pack(side="left", padx=7)

        self.button(
            buttons, "Remove", lambda: [dialog.destroy(), self.remove_game(index)]
        ).pack(side="right")

    # --------------------------------------------------------
    # ADD / EDIT / REMOVE GAMES
    # --------------------------------------------------------

    def game_form(self, index=None):
        editing = index is not None
        old = self.games[index] if editing else {}

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit game" if editing else "Add game")
        dialog.geometry("550x650")
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.grab_set()

        self.label(
            dialog, "Edit game" if editing else "Add a game",
            21, TEXT, True
        ).pack(anchor="w", padx=24, pady=(20, 15))

        form = tk.Frame(dialog, bg=BG)
        form.pack(fill="both", expand=True, padx=24)

        fields = {}

        def entry_field(title, key, value=""):
            self.label(form, title, 8, MUTED, True).pack(anchor="w", pady=(9, 4))
            entry = tk.Entry(
                form, bg=PANEL, fg=TEXT, insertbackground=TEXT,
                relief="flat", font=("Segoe UI", 10)
            )
            entry.pack(fill="x", ipady=9)
            entry.insert(0, str(value or ""))
            fields[key] = entry
            return entry

        entry_field("GAME NAME", "title", old.get("title", ""))

        self.label(form, "PLATFORM", 8, MUTED, True).pack(anchor="w", pady=(12, 4))
        source_var = tk.StringVar(value=old.get("source", "Standalone"))
        ttk.Combobox(
            form, textvariable=source_var,
            values=SOURCES, state="readonly"
        ).pack(fill="x", ipady=5)

        target = entry_field("EXECUTABLE PATH OR LAUNCH URI", "target", old.get("target", ""))

        def browse():
            path = filedialog.askopenfilename(
                title="Select game executable",
                filetypes=[("Applications", "*.exe"), ("All files", "*.*")]
            )
            if path:
                target.delete(0, "end")
                target.insert(0, path)
                if not fields["process_name"].get().strip():
                    fields["process_name"].insert(0, Path(path).name)

        self.button(form, "Browse for game", browse).pack(anchor="w", pady=7)

        entry_field("PROCESS NAME FOR PLAYTIME (e.g. game.exe)", "process_name", old.get("process_name", ""))
        entry_field("CATEGORY (e.g. Racing, FPS, Simulation)", "category", old.get("category", ""))
        entry_field("LAUNCH ARGUMENTS", "arguments", old.get("arguments", ""))

        self.label(form, "PER-GAME PERFORMANCE MODE", 8, MUTED, True).pack(anchor="w", pady=(12, 4))
        game_mode = tk.StringVar(value=old.get("performance_mode", "Default"))
        ttk.Combobox(
            form, textvariable=game_mode,
            values=["Default"] + PERFORMANCE_MODES,
            state="readonly"
        ).pack(fill="x", ipady=5)

        def save():
            title = fields["title"].get().strip()
            destination = fields["target"].get().strip()

            if not title or not destination:
                messagebox.showwarning(
                    "Missing information",
                    "A game name and launch target are required.",
                    parent=dialog
                )
                return

            record = {
                "title": title,
                "source": source_var.get(),
                "target": destination,
                "process_name": fields["process_name"].get().strip(),
                "category": fields["category"].get().strip() or "Uncategorized",
                "arguments": fields["arguments"].get().strip(),
                "performance_mode": game_mode.get(),
                "launches": int(old.get("launches", 0) or 0),
                "play_seconds": int(old.get("play_seconds", 0) or 0),
                "last_played": old.get("last_played", ""),
                "favorite": bool(old.get("favorite", False))
            }

            if editing:
                self.games[index] = record
            else:
                self.games.append(record)

            self.save_all()
            dialog.destroy()
            self.show_page("Library")

        footer = tk.Frame(dialog, bg=SIDEBAR)
        footer.pack(side="bottom", fill="x")

        self.button(footer, "Cancel", dialog.destroy).pack(side="right", padx=8, pady=12)
        self.button(footer, "Save game", save, True).pack(side="right", pady=12)

    def remove_game(self, index):
        game = self.games[index]
        if self.settings.get("confirm_remove", True):
            if not messagebox.askyesno(
                "Remove game",
                f"Remove {game.get('title')} from this profile?"
            ):
                return

        self.games.pop(index)
        self.save_all()
        self.show_page("Library")

    # --------------------------------------------------------
    # LAUNCHING GAMES
    # --------------------------------------------------------

    def play_game(self, index):
        game = self.games[index]
        target = str(game.get("target", "")).strip()
        arguments = str(game.get("arguments", "")).strip()

        try:
            if target.lower().startswith((
                "steam://", "com.epicgames.launcher://",
                "roblox://", "http://", "https://"
            )):
                webbrowser.open(target)
            else:
                path = Path(target).expanduser()
                if not path.exists():
                    raise FileNotFoundError(f"Game target not found:\n{path}")

                mode = game.get("performance_mode", "Default")
                if mode == "Default":
                    mode = self.settings.get("performance_mode", "Balanced")

                flags = 0
                if os.name == "nt":
                    if mode == "Performance":
                        flags = getattr(subprocess, "ABOVE_NORMAL_PRIORITY_CLASS", 0)
                    elif mode == "Quiet":
                        flags = getattr(subprocess, "BELOW_NORMAL_PRIORITY_CLASS", 0)

                command = [str(path)]
                if arguments:
                    import shlex
                    command.extend(shlex.split(arguments, posix=False))

                subprocess.Popen(
                    command,
                    cwd=str(path.parent),
                    creationflags=flags
                )

            game["launches"] = int(game.get("launches", 0) or 0) + 1
            game["last_played"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.save_all()
            self.status_var.set(f"Started {game['title']}")
            self.show_page("Library")

        except (OSError, ValueError) as error:
            messagebox.showerror("Launch failed", str(error))

    # --------------------------------------------------------
    # WISHLIST
    # --------------------------------------------------------

    def page_wishlist(self):
        self.page_heading(
            "Your next games",
            "Wishlist",
            "Keep track of games you want to play or buy."
        )

        actions = tk.Frame(self.content, bg=BG)
        actions.pack(fill="x", pady=(0, 12))
        self.button(actions, "+ Add to wishlist", self.add_wishlist, True).pack(side="left")

        query = self.search_query()
        items = [
            (i, item) for i, item in enumerate(self.wishlist)
            if query in item.get("title", "").lower()
        ]

        if not items:
            self.label(
                self.content, "Your wishlist is empty", 16, MUTED, True
            ).pack(pady=45)
            self.label(
                self.content, "Add games you want to keep an eye on.", 9, MUTED
            ).pack()
            return

        for index, item in items:
            card = self.section_card()
            card.pack(fill="x", pady=5)

            self.label(
                card, item.get("title", "Untitled"), 11, TEXT, True, bg=PANEL
            ).pack(anchor="w")

            self.label(
                card,
                f"{item.get('platform', 'Any platform')}  ·  Target price: {item.get('target_price') or 'Not set'}",
                8, MUTED, bg=PANEL
            ).pack(anchor="w", pady=(5, 9))

            row = tk.Frame(card, bg=PANEL)
            row.pack(fill="x")

            self.button(
                row, "Store page",
                lambda url=item.get("url", ""): webbrowser.open(url) if url else None
            ).pack(side="left")

            self.button(
                row, "Mark owned",
                lambda i=index: self.wishlist_to_library(i)
            ).pack(side="left", padx=7)

            self.button(
                row, "Remove",
                lambda i=index: self.remove_wishlist(i)
            ).pack(side="right")

    def add_wishlist(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add to wishlist")
        dialog.geometry("430x420")
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.grab_set()

        self.label(dialog, "Add a game to your wishlist", 17, TEXT, True).pack(
            anchor="w", padx=22, pady=(20, 14)
        )

        fields = {}

        def add_field(title, key):
            self.label(dialog, title, 8, MUTED, True).pack(anchor="w", padx=22, pady=(8, 4))
            entry = tk.Entry(
                dialog, bg=PANEL, fg=TEXT,
                insertbackground=TEXT, relief="flat"
            )
            entry.pack(fill="x", padx=22, ipady=8)
            fields[key] = entry

        add_field("GAME NAME", "title")
        add_field("TARGET PRICE (OPTIONAL)", "target_price")
        add_field("STORE URL (OPTIONAL)", "url")

        self.label(dialog, "PLATFORM", 8, MUTED, True).pack(anchor="w", padx=22, pady=(10, 4))
        platform = tk.StringVar(value="Steam")
        ttk.Combobox(
            dialog, textvariable=platform,
            values=SOURCES + ["Any platform"],
            state="readonly"
        ).pack(fill="x", padx=22, ipady=5)

        def save():
            title = fields["title"].get().strip()
            if not title:
                messagebox.showwarning("Missing name", "Enter a game name.", parent=dialog)
                return

            price = fields["target_price"].get().strip()
            if price:
                try:
                    float(price.replace("$", "").replace(",", ""))
                except ValueError:
                    messagebox.showwarning("Invalid price", "Enter a number for the target price.", parent=dialog)
                    return

            self.wishlist.append({
                "title": title,
                "platform": platform.get(),
                "target_price": price,
                "url": fields["url"].get().strip()
            })
            self.save_all()
            dialog.destroy()
            self.show_page("Wishlist")

        self.button(dialog, "Save to wishlist", save, True).pack(
            anchor="e", padx=22, pady=18
        )

    def remove_wishlist(self, index):
        self.wishlist.pop(index)
        self.save_all()
        self.show_page("Wishlist")

    def wishlist_to_library(self, index):
        item = self.wishlist.pop(index)
        self.games.append({
            "title": item["title"],
            "source": item.get("platform", "Standalone"),
            "target": item.get("url", ""),
            "process_name": "",
            "category": "Uncategorized",
            "arguments": "",
            "performance_mode": "Default",
            "launches": 0,
            "play_seconds": 0,
            "last_played": "",
            "favorite": False
        })
        self.save_all()
        messagebox.showinfo(
            "Added to library",
            "The game is now in your library. Edit it to add its executable or launch target."
        )
        self.show_page("Library")

    # --------------------------------------------------------
    # STORE LINKS
    # --------------------------------------------------------

    def page_store(self):
        self.page_heading(
            "Discover",
            "Game storefronts",
            "Open official storefronts to browse games."
        )

        stores = [
            ("Steam", "https://store.steampowered.com/"),
            ("Epic Games Store", "https://store.epicgames.com/"),
            ("GOG", "https://www.gog.com/"),
            ("itch.io", "https://itch.io/"),
            ("Xbox", "https://www.xbox.com/games"),
            ("Ubisoft Store", "https://store.ubisoft.com/"),
            ("EA Store", "https://www.ea.com/games")
        ]

        for name, url in stores:
            card = self.section_card()
            card.pack(fill="x", pady=5)

            self.label(card, name, 12, TEXT, True, bg=PANEL).pack(side="left")
            self.button(
                card, "Visit store",
                lambda link=url: webbrowser.open(link), True
            ).pack(side="right")

        self.label(
            self.content,
            "Prices and availability are shown by the storefronts. Wishlist target prices are notes you enter yourself.",
            8, MUTED
        ).pack(anchor="w", pady=12)

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    def page_statistics(self):
        self.page_heading("Your activity", "Gaming statistics")

        total_time = sum(int(g.get("play_seconds", 0) or 0) for g in self.games)
        total_launches = sum(int(g.get("launches", 0) or 0) for g in self.games)

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", pady=10)

        for value, title in [
            (str(len(self.games)), "Games"),
            (format_time(total_time), "Total playtime"),
            (str(total_launches), "Game launches")
        ]:
            card = self.section_card(cards)
            card.pack(side="left", fill="both", expand=True, padx=(0, 9))
            self.label(card, value, 23, TEXT, True, bg=PANEL).pack(anchor="w")
            self.label(card, title, 8, MUTED, bg=PANEL).pack(anchor="w", pady=(5, 0))

        self.label(
            self.content, "MOST PLAYED GAMES", 9, MUTED, True
        ).pack(anchor="w", pady=(25, 10))

        ordered = sorted(
            self.games,
            key=lambda g: int(g.get("play_seconds", 0) or 0),
            reverse=True
        )

        for game in ordered[:10]:
            card = tk.Frame(self.content, bg=CARD, padx=14, pady=11)
            card.pack(fill="x", pady=3)
            self.label(card, game.get("title", "Unknown"), 9, TEXT, True, bg=CARD).pack(side="left")
            self.label(
                card, format_time(game.get("play_seconds", 0)),
                9, MUTED, bg=CARD
            ).pack(side="right")

    # --------------------------------------------------------
    # ONLINE ACCOUNT + SOCIAL
    # --------------------------------------------------------

    def show_boot_animation(self):
        splash = tk.Toplevel(self.root)
        splash.overrideredirect(True)
        splash.configure(bg=BG)
        width, height = 430, 210
        x = self.root.winfo_screenwidth() // 2 - width // 2
        y = self.root.winfo_screenheight() // 2 - height // 2
        splash.geometry(f"{width}x{height}+{x}+{y}")
        frame = tk.Frame(splash, bg=SIDEBAR, highlightbackground=ACCENT, highlightthickness=2)
        frame.pack(fill="both", expand=True, padx=2, pady=2)
        tk.Label(frame, text="U", bg=ACCENT, fg="white", font=("Segoe UI", 28, "bold"), width=2).pack(pady=(28, 8))
        tk.Label(frame, text="UniGame Launcher", bg=SIDEBAR, fg=TEXT, font=("Segoe UI", 18, "bold")).pack()
        status = tk.Label(frame, text="Loading your gaming space...", bg=SIDEBAR, fg=MUTED, font=("Segoe UI", 9))
        status.pack(pady=(8, 0))
        if self.settings.get("boot_animation") == "Minimal":
            self.root.after(650, lambda: splash.destroy() if splash.winfo_exists() else None)
        else:
            bar = ttk.Progressbar(frame, mode="indeterminate", length=230)
            bar.pack(pady=15)
            bar.start(12)
            self.root.after(1150, lambda: (bar.stop(), splash.destroy() if splash.winfo_exists() else None))

    def cloud_task(self, work, on_success, title="Online", on_error=None):
        if self.cloud_busy:
            messagebox.showinfo(title, "An online request is already running.", parent=self.root)
            return
        self.cloud_busy = True
        self.status_var.set(f"{title}: connecting...")
        def worker():
            try:
                result = work()
                self.root.after(0, lambda: self._cloud_done(result, on_success, title))
            except Exception as error:
                self.root.after(0, lambda e=str(error): self._cloud_failed(e, title, on_error))
        threading.Thread(target=worker, daemon=True).start()

    def _cloud_done(self, result, callback, title):
        self.cloud_busy = False
        self.status_var.set(f"{title}: complete")
        callback(result)

    def _cloud_failed(self, error, title, callback=None):
        self.cloud_busy = False
        self.status_var.set("Ready")
        if callback:
            callback(error)
        else:
            messagebox.showerror(title, error, parent=self.root)

    def account_dialog(self):
        if self.cloud.logged_in:
            choice = messagebox.askyesnocancel(
                "Online account",
                f"Signed in as {self.cloud.user.get('email', 'your account')}.\n\nYes: sign out\nNo: manage online profile\nCancel: close",
                parent=self.root
            )
            if choice is True:
                self.cloud_task(self.cloud.logout, lambda _r: (setattr(self, "cloud_profile", None), self.show_page("Social")), "Sign out")
            elif choice is False:
                self.edit_online_profile()
            return
        choice = messagebox.askyesnocancel("UniGame account", "Yes: create an account\nNo: sign in\nCancel: close", parent=self.root)
        if choice is None:
            return
        email = simpledialog.askstring("Email", "Email address:", parent=self.root)
        if not email:
            return
        password = simpledialog.askstring("Password", "Password:", show="•", parent=self.root)
        if not password:
            return
        if choice:
            def signup_done(result):
                if self.cloud.logged_in:
                    self.finish_cloud_profile_setup()
                else:
                    messagebox.showinfo("Check your email", "Supabase accepted the sign-up. Check your email to verify the account, then sign in.", parent=self.root)
            self.cloud_task(lambda: self.cloud.signup(email.strip(), password), signup_done, "Create account")
        else:
            def login_done(_result):
                self.finish_cloud_profile_setup()
            self.cloud_task(lambda: self.cloud.login(email.strip(), password), login_done, "Sign in")

    def finish_cloud_profile_setup(self):
        def check_existing():
            rows = self.cloud.rest("profiles", "?id=eq." + urllib.parse.quote(self.cloud.user_id) + "&select=*")
            return rows[0] if rows else None
        def checked(profile):
            if profile:
                self.cloud_profile = profile
                self.load_social_data(lambda: self.show_page("Social"))
                return
            username = simpledialog.askstring("Choose username", "Your unique UniGame username:", parent=self.root)
            if not username:
                username = "player_" + str(self.cloud.user_id or "user")[:8]
            username = re.sub(r"[^A-Za-z0-9_]", "", username.strip())[:24]
            if len(username) < 3:
                messagebox.showwarning("Username", "Usernames must be at least 3 characters.", parent=self.root)
                return
            self.cloud_task(lambda: self.cloud.ensure_profile(username), lambda rows: (setattr(self, "cloud_profile", rows[0] if rows else {}), self.load_social_data(lambda: self.show_page("Social"))), "Set up profile")
        self.cloud_task(check_existing, checked, "Check online profile")

    def update_online_presence(self):
        if not self.cloud.logged_in:
            return
        payload = {"user_id": self.cloud.user_id, "is_online": True, "last_seen": datetime.utcnow().isoformat(timespec="seconds") + "Z"}
        self.cloud_task(lambda: self.cloud.rest("user_presence", "?on_conflict=user_id", "POST", payload, "resolution=merge-duplicates,return=minimal"), lambda _r: None, "Update presence")

    def presence_heartbeat(self):
        if self._closing:
            return
        if self.cloud.logged_in and not self.cloud_busy:
            payload = {"user_id": self.cloud.user_id, "is_online": True, "last_seen": datetime.utcnow().isoformat(timespec="seconds") + "Z"}
            self.cloud_task(lambda: self.cloud.rest("user_presence", "?on_conflict=user_id", "POST", payload, "resolution=merge-duplicates,return=minimal"), lambda _r: None, "Presence")
        self.root.after(60000, self.presence_heartbeat)

    def sync_online_stats(self):
        if not self.cloud.logged_in:
            return
        records = []
        for game in self.games:
            title = str(game.get("title", "")).strip()
            if not title:
                continue
            key = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:80] or "game"
            records.append({
                "user_id": self.cloud.user_id,
                "game_key": key,
                "game_title": title[:120],
                "platform": str(game.get("source", "PC"))[:40],
                "play_seconds": max(0, int(game.get("play_seconds", 0) or 0)),
                "launches": max(0, int(game.get("launches", 0) or 0)),
                "last_played": game.get("last_played") or None,
            })
        if not records:
            return
        self.cloud_task(lambda: self.cloud.rest("game_stats", "?on_conflict=user_id,game_key", "POST", records, "resolution=merge-duplicates,return=minimal"), lambda _r: None, "Sync game stats")

    def apply_profile_theme(self, theme_name):
        global ACCENT
        accents = {"Midnight": "#E65B49", "Crimson": "#F0445E", "Ocean": "#4C9DFF", "Violet": "#A78BFA", "Emerald": "#34D399"}
        ACCENT = accents.get(theme_name, accents["Midnight"])
        self.settings["accent"] = ACCENT
        self.setup_style()
        self.root.configure(bg=BG)

    def edit_online_profile(self):
        if not self.cloud.logged_in:
            self.account_dialog()
            return
        win = tk.Toplevel(self.root)
        win.title("Edit online profile")
        win.configure(bg=BG)
        win.geometry("470x490")
        profile = self.cloud_profile or {}
        fields = {}
        for label, key, default in [
            ("Username", "username", profile.get("username", "")),
            ("Display name", "display_name", profile.get("display_name", "")),
            ("Bio", "bio", profile.get("bio", "")),
            ("Avatar image URL", "avatar_url", profile.get("avatar_url", "")),
            ("Banner image URL", "banner_url", profile.get("banner_url", "")),
        ]:
            tk.Label(win, text=label, bg=BG, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
            entry = tk.Entry(win, bg=PANEL, fg=TEXT, insertbackground=TEXT, relief="flat", font=("Segoe UI", 10))
            entry.pack(fill="x", padx=20, ipady=7)
            entry.insert(0, str(default or ""))
            fields[key] = entry
        tk.Label(win, text="Profile theme", bg=BG, fg=TEXT).pack(anchor="w", padx=20, pady=(10, 2))
        theme = tk.StringVar(value=(profile.get("theme") or {}).get("name", "Midnight"))
        ttk.Combobox(win, textvariable=theme, values=["Midnight", "Crimson", "Ocean", "Violet", "Emerald"], state="readonly").pack(anchor="w", padx=20)
        tk.Label(win, text="Profile visibility", bg=BG, fg=TEXT).pack(anchor="w", padx=20, pady=(10, 2))
        visibility = tk.StringVar(value=profile.get("visibility", "public"))
        ttk.Combobox(win, textvariable=visibility, values=["public", "friends", "private"], state="readonly").pack(anchor="w", padx=20)
        def save_profile():
            username = fields["username"].get().strip()
            if len(username) < 3 or not re.fullmatch(r"[A-Za-z0-9_]+", username):
                messagebox.showwarning("Invalid username", "Use 3–24 letters, numbers or underscores.", parent=win)
                return
            payload = {key: entry.get().strip() for key, entry in fields.items()}
            payload["theme"] = {"name": theme.get()}
            payload["visibility"] = visibility.get()
            def saved(rows):
                self.cloud_profile = rows[0] if rows else payload
                self.apply_profile_theme(theme.get())
                self.save_all()
                win.destroy()
                self.show_page("Social")
            self.cloud_task(lambda: self.cloud.rest("profiles", "?id=eq." + urllib.parse.quote(self.cloud.user_id) + "&select=*", "PATCH", payload, "return=representation"), saved, "Save profile")
        self.button(win, "Save online profile", save_profile, True).pack(anchor="w", padx=20, pady=18)

    def load_social_data(self, callback):
        uid = self.cloud.user_id
        def work():
            profile = self.cloud.rest("profiles", "?id=eq." + uid + "&select=*")
            relations = self.cloud.rest("friendships", "?or=(requester_id.eq." + uid + ",addressee_id.eq." + uid + ")&select=*") or []
            accepted = [r for r in relations if r.get("status") == "accepted"]
            friend_ids = [r.get("addressee_id") if r.get("requester_id") == uid else r.get("requester_id") for r in accepted]
            request_ids = [r.get("requester_id") for r in relations if r.get("status") == "pending" and r.get("addressee_id") == uid]
            all_ids = list(dict.fromkeys(friend_ids + request_ids))
            other_profiles = []
            presence = []
            friend_stats = []
            if all_ids:
                id_filter = "(" + ",".join(all_ids) + ")"
                other_profiles = self.cloud.rest("profiles", "?id=in." + urllib.parse.quote(id_filter, safe="(),") + "&select=id,username,display_name,avatar_url") or []
                presence = self.cloud.rest("user_presence", "?user_id=in." + urllib.parse.quote(id_filter, safe="(),") + "&select=user_id,is_online,last_seen") or []
                friend_stats = self.cloud.rest("game_stats", "?user_id=in." + urllib.parse.quote(id_filter, safe="(),") + "&select=user_id,game_title,play_seconds,launches&order=play_seconds.desc") or []
            presence_payload = {"user_id": uid, "is_online": True, "last_seen": datetime.utcnow().isoformat(timespec="seconds") + "Z"}
            self.cloud.rest("user_presence", "?on_conflict=user_id", "POST", presence_payload, "resolution=merge-duplicates,return=minimal")
            stats_records = []
            for game in self.games:
                title = str(game.get("title", "")).strip()
                if not title:
                    continue
                game_key = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:80] or "game"
                stats_records.append({"user_id": uid, "game_key": game_key, "game_title": title[:120], "platform": str(game.get("source", "PC"))[:40], "play_seconds": max(0, int(game.get("play_seconds", 0) or 0)), "launches": max(0, int(game.get("launches", 0) or 0)), "last_played": game.get("last_played") or None})
            if stats_records:
                self.cloud.rest("game_stats", "?on_conflict=user_id,game_key", "POST", stats_records, "resolution=merge-duplicates,return=minimal")
            return (profile[0] if profile else {}, relations, other_profiles, presence, friend_stats)
        def done(result):
            self.cloud_profile, relations, self.cloud_friend_profiles, self.cloud_friend_presence, self.cloud_friend_stats = result
            self.cloud_friends = [r for r in relations if r.get("status") == "accepted"]
            self.cloud_requests = [r for r in relations if r.get("status") == "pending" and r.get("addressee_id") == uid]
            theme_name = (self.cloud_profile.get("theme") or {}).get("name", "Midnight") if isinstance(self.cloud_profile, dict) else "Midnight"
            self.apply_profile_theme(theme_name)
            callback()
        self.cloud_task(work, done, "Load social profile")

    def delete_online_account(self):
        if not self.cloud.logged_in:
            return
        if not messagebox.askyesno("Delete online account", "Permanently delete your UniGame online account, profile, friends and synced stats?\n\nYour local game library will remain on this PC. This cannot be undone.", parent=self.root):
            return
        def deleted(_result):
            self.cloud._save_session({})
            self.cloud_profile = None
            self.show_page("Social")
            messagebox.showinfo("Account deleted", "Your online account has been deleted. Your local launcher data remains on this PC.", parent=self.root)
        self.cloud_task(lambda: self.cloud._request("/rest/v1/rpc/delete_my_account", "POST", {}, token=self.cloud.access_token), deleted, "Delete account")

    def add_friend(self):
        if not self.cloud.logged_in:
            self.account_dialog()
            return
        username = simpledialog.askstring("Add friend", "Enter their exact username:", parent=self.root)
        if not username:
            return
        def work():
            matches = self.cloud.rest("profiles", "?username=ilike." + urllib.parse.quote(username.strip()) + "&select=id,username,display_name")
            if not matches:
                raise RuntimeError("No public profile found with that username.")
            target = matches[0]
            if target["id"] == self.cloud.user_id:
                raise RuntimeError("You cannot add yourself.")
            return self.cloud.rest("friendships", "", "POST", {"requester_id": self.cloud.user_id, "addressee_id": target["id"], "status": "pending"}, "return=representation")
        self.cloud_task(work, lambda _r: self.show_page("Social"), "Send friend request")

    def respond_friend_request(self, request_id, accept):
        status = "accepted" if accept else "rejected"
        self.cloud_task(lambda: self.cloud.rest("friendships", "?id=eq." + urllib.parse.quote(str(request_id)), "PATCH", {"status": status}, "return=representation"), lambda _r: self.load_social_data(lambda: self.show_page("Social")), "Friend request")

    def page_social(self):
        self.page_heading("Your online identity", "UniGame Social", "Profiles, friends and gaming stats that travel with your account.")
        if not self.cloud.logged_in:
            card = self.section_card()
            card.pack(fill="x", pady=8)
            self.label(card, "Connect your UniGame account", 16, TEXT, True, bg=PANEL).pack(anchor="w")
            self.label(card, "Sign in or create an account to publish your profile, find friends and sync your gaming identity.", 9, MUTED, bg=PANEL, wraplength=760).pack(anchor="w", pady=8)
            self.button(card, "Sign in / Create account", self.account_dialog, True).pack(anchor="w", pady=5)
            self.label(self.content, "Your local profiles and game library continue working without an online account.", 8, MUTED).pack(anchor="w", pady=8)
            return
        card = self.section_card()
        card.pack(fill="x", pady=5)
        profile = self.cloud_profile or {}
        username = profile.get("username") or self.cloud.user.get("email", "Player")
        self.label(card, "@" + str(username), 17, TEXT, True, bg=PANEL).pack(anchor="w")
        self.label(card, profile.get("display_name") or "Set a display name", 10, MUTED, bg=PANEL).pack(anchor="w", pady=3)
        self.label(card, profile.get("bio") or "Add a bio to tell friends what you play.", 9, MUTED, bg=PANEL, wraplength=760).pack(anchor="w", pady=4)
        total_seconds = sum(int(g.get("play_seconds", 0) or 0) for g in self.games)
        total_launches = sum(int(g.get("launches", 0) or 0) for g in self.games)
        self.label(card, f"{len(self.games)} games   ·   {format_time(total_seconds)} played   ·   {total_launches} launches", 9, GREEN, True, bg=PANEL).pack(anchor="w", pady=(5, 0))
        row = tk.Frame(card, bg=PANEL); row.pack(anchor="w", pady=8)
        self.button(row, "Edit profile & theme", self.edit_online_profile, True).pack(side="left", padx=(0, 6))
        self.button(row, "Refresh", lambda: self.load_social_data(lambda: self.show_page("Social"))).pack(side="left", padx=6)
        self.button(row, "Sign out", self.account_dialog).pack(side="left", padx=6)
        self.button(row, "Delete account", self.delete_online_account).pack(side="left", padx=6)
        actions = tk.Frame(self.content, bg=BG); actions.pack(fill="x", pady=8)
        self.button(actions, "+ Add friend", self.add_friend, True).pack(side="left")
        friends = self.section_card(); friends.pack(fill="x", pady=5)
        self.label(friends, f"Friends · {len(self.cloud_friends)}", 12, TEXT, True, bg=PANEL).pack(anchor="w")
        if not self.cloud_friends:
            self.label(friends, "No friends yet. Add someone by their exact username.", 9, MUTED, bg=PANEL).pack(anchor="w", pady=7)
        profile_by_id = {p.get("id"): p for p in getattr(self, "cloud_friend_profiles", [])}
        presence_by_id = {p.get("user_id"): p for p in getattr(self, "cloud_friend_presence", [])}
        for relation in self.cloud_friends:
            other = relation.get("addressee_id") if relation.get("requester_id") == self.cloud.user_id else relation.get("requester_id")
            friend = profile_by_id.get(other, {})
            presence = presence_by_id.get(other, {})
            display = friend.get("display_name") or friend.get("username") or (str(other)[:8] if other else "Friend")
            state = "Offline"
            if presence.get("is_online") and presence.get("last_seen"):
                try:
                    seen = datetime.fromisoformat(str(presence.get("last_seen")).replace("Z", "+00:00"))
                    if (datetime.now().astimezone() - seen).total_seconds() < 150:
                        state = "Online"
                except (ValueError, TypeError):
                    pass
            top_game = next((g for g in getattr(self, "cloud_friend_stats", []) if g.get("user_id") == other), None)
            suffix = f"  ·  Top game: {top_game.get('game_title')} ({format_time(top_game.get('play_seconds', 0))})" if top_game else ""
            self.label(friends, f"{display}  ·  {state}{suffix}", 9, GREEN if state == "Online" else MUTED, bg=PANEL).pack(anchor="w", pady=3)
        requests = self.section_card(); requests.pack(fill="x", pady=5)
        self.label(requests, f"Incoming requests · {len(self.cloud_requests)}", 12, TEXT, True, bg=PANEL).pack(anchor="w")
        request_profile_by_id = {p.get("id"): p for p in getattr(self, "cloud_friend_profiles", [])}
        for request in self.cloud_requests:
            line = tk.Frame(requests, bg=PANEL); line.pack(fill="x", pady=4)
            sender = request_profile_by_id.get(request.get("requester_id"), {})
            sender_name = sender.get("display_name") or sender.get("username") or str(request.get("requester_id", ""))[:8]
            self.label(line, "Request from " + sender_name, 9, MUTED, bg=PANEL).pack(side="left")
            self.button(line, "Accept", lambda rid=request.get("id"): self.respond_friend_request(rid, True), True).pack(side="right", padx=3)
            self.button(line, "Decline", lambda rid=request.get("id"): self.respond_friend_request(rid, False)).pack(side="right", padx=3)
        if self.cloud.logged_in and self.cloud_profile is None and not self.cloud_busy:
            self.load_social_data(lambda: self.show_page("Social"))

    # --------------------------------------------------------
    # PROFILES
    # --------------------------------------------------------

    def page_profiles(self):
        self.page_heading(
            "Personal spaces",
            "Profiles",
            "Each profile has its own games, wishlist and statistics."
        )

        row = tk.Frame(self.content, bg=BG)
        row.pack(fill="x", pady=(0, 12))

        self.button(row, "+ New profile", self.create_profile, True).pack(side="left")
        self.button(row, "Rename active", self.rename_profile).pack(side="left", padx=7)
        self.button(row, "Delete active", self.delete_profile).pack(side="left")

        for name, profile in self.data["profiles"].items():
            card = self.section_card()
            card.pack(fill="x", pady=5)

            self.label(
                card, name, 12, TEXT, True, bg=PANEL
            ).pack(anchor="w")

            self.label(
                card,
                f"{len(profile.get('games', []))} games  ·  {len(profile.get('wishlist', []))} wishlist items",
                8, MUTED, bg=PANEL
            ).pack(anchor="w", pady=(5, 8))

            if name == self.active_profile:
                self.label(
                    card, "CURRENT PROFILE", 8, GREEN, True, bg=PANEL
                ).pack(anchor="w")
            else:
                self.button(
                    card, "Switch to profile",
                    lambda n=name: self.switch_profile(n)
                ).pack(anchor="w")

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    def page_performance(self):
        self.page_heading(
            "Launch preferences",
            "Performance center",
            "Choose how UniGame launches supported games."
        )

        card = self.section_card()
        card.pack(fill="x", pady=7)

        self.label(card, "DEFAULT PERFORMANCE PRESET", 9, TEXT, True, bg=PANEL).pack(anchor="w")

        self.label(
            card,
            "Quiet uses below-normal process priority. Balanced uses normal priority. Performance requests above-normal process priority. Windows and the game may override these settings.",
            8, MUTED, bg=PANEL, wraplength=750, justify="left"
        ).pack(anchor="w", pady=(7, 12))

        mode = tk.StringVar(value=self.settings.get("performance_mode", "Balanced"))
        ttk.Combobox(
            card, textvariable=mode,
            values=PERFORMANCE_MODES,
            state="readonly"
        ).pack(anchor="w", fill="x", ipady=5)

        def save_mode():
            self.settings["performance_mode"] = mode.get()
            self.mode_var.set(mode.get())
            self.save_all()
            messagebox.showinfo("Saved", f"Default mode set to {mode.get()}.")

        self.button(card, "Save performance preset", save_mode, True).pack(anchor="w", pady=(12, 0))

        note = self.section_card()
        note.pack(fill="x", pady=12)

        self.label(note, "What these modes do", 11, TEXT, True, bg=PANEL).pack(anchor="w")
        for text in [
            "Quiet: requests below-normal process priority for launched executables.",
            "Balanced: uses the normal Windows process priority.",
            "Performance: requests above-normal process priority for launched executables.",
            "Per-game settings can override the default preset."
        ]:
            self.label(note, "• " + text, 8, MUTED, bg=PANEL).pack(anchor="w", pady=3)

        self.label(
            self.content,
            "These presets do not change clock speeds, voltage, fan curves, or hardware settings.",
            8, MUTED
        ).pack(anchor="w", pady=7)

    # --------------------------------------------------------
    # SETTINGS AND BACKUP
    # --------------------------------------------------------

    def page_settings(self):
        self.page_heading(
            "Preferences",
            "Settings",
            "Customize how UniGame works."
        )

        card = self.section_card()
        card.pack(fill="x", pady=6)

        auto_scan = tk.BooleanVar(value=self.settings.get("auto_scan", True))
        confirm_remove = tk.BooleanVar(value=self.settings.get("confirm_remove", True))
        boot_animation = tk.StringVar(value=self.settings.get("boot_animation", "Pulse"))

        tk.Checkbutton(
            card, text="Automatically scan for games on startup",
            variable=auto_scan, bg=PANEL, fg=TEXT,
            selectcolor=BG, activebackground=PANEL,
            activeforeground=TEXT, font=("Segoe UI", 9)
        ).pack(anchor="w", pady=4)

        tk.Checkbutton(
            card, text="Ask before removing games",
            variable=confirm_remove, bg=PANEL, fg=TEXT,
            selectcolor=BG, activebackground=PANEL,
            activeforeground=TEXT, font=("Segoe UI", 9)
        ).pack(anchor="w", pady=4)
        tk.Label(card, text="Startup animation", bg=PANEL, fg=TEXT, font=("Segoe UI", 9)).pack(anchor="w", pady=(10, 3))
        ttk.Combobox(card, textvariable=boot_animation, values=["Pulse", "Minimal", "Off"], state="readonly", width=18).pack(anchor="w")

        def save_settings():
            self.settings["auto_scan"] = auto_scan.get()
            self.settings["confirm_remove"] = confirm_remove.get()
            self.settings["boot_animation"] = boot_animation.get()
            self.save_all()
            messagebox.showinfo("Settings saved", "Your settings have been saved.")

        self.button(card, "Save settings", save_settings, True).pack(anchor="w", pady=(10, 0))

        backup = self.section_card()
        backup.pack(fill="x", pady=8)

        self.label(backup, "Backup and restore", 12, TEXT, True, bg=PANEL).pack(anchor="w")
        self.label(
            backup,
            "Export your profiles, libraries, wishlists and settings to a JSON backup.",
            8, MUTED, bg=PANEL
        ).pack(anchor="w", pady=(5, 12))

        row = tk.Frame(backup, bg=PANEL)
        row.pack(anchor="w")

        self.button(row, "Export backup", self.export_backup).pack(side="left")
        self.button(row, "Import backup", self.import_backup).pack(side="left", padx=7)

        info = self.section_card()
        info.pack(fill="x", pady=8)

        self.label(info, "Application information", 11, TEXT, True, bg=PANEL).pack(anchor="w")
        self.label(info, f"Version {APP_VERSION}", 8, MUTED, bg=PANEL).pack(anchor="w", pady=3)
        self.label(info, f"Data folder: {APPDATA}", 8, MUTED, bg=PANEL, wraplength=760).pack(anchor="w")

    def export_backup(self):
        path = filedialog.asksaveasfilename(
            title="Export UniGame backup",
            defaultextension=".json",
            filetypes=[("JSON backup", "*.json")]
        )
        if not path:
            return

        self.save_all()
        backup = {
            "data": self.data,
            "settings": self.settings,
            "version": APP_VERSION
        }
        Path(path).write_text(json.dumps(backup, indent=2), encoding="utf-8")
        messagebox.showinfo("Backup exported", "Your backup was saved.")

    def import_backup(self):
        path = filedialog.askopenfilename(
            title="Import UniGame backup",
            filetypes=[("JSON backup", "*.json")]
        )
        if not path:
            return

        try:
            backup = json.loads(Path(path).read_text(encoding="utf-8"))
            imported_data = backup["data"]
            imported_settings = backup.get("settings", self.settings)

            if not isinstance(imported_data.get("profiles"), dict):
                raise ValueError("The backup does not contain valid profiles.")

            if not messagebox.askyesno(
                "Restore backup",
                "This replaces the current profiles and settings. Continue?"
            ):
                return

            self.data = imported_data
            self.settings = imported_settings
            self.active_profile = self.data.get("active_profile", next(iter(self.data["profiles"])))
            self.profile = self.data["profiles"][self.active_profile]
            self.games = self.profile.setdefault("games", [])
            self.wishlist = self.profile.setdefault("wishlist", [])
            self.profile_box.configure(values=list(self.data["profiles"]))
            self.profile_var.set(self.active_profile)
            self.save_all()
            self.show_page("Library")
            messagebox.showinfo("Backup restored", "Your backup has been restored.")

        except (OSError, ValueError, KeyError, TypeError) as error:
            messagebox.showerror("Import failed", str(error))

    # --------------------------------------------------------
    # GAME SCANNER
    # --------------------------------------------------------

    def steam_roots(self):
        roots = []

        for base in [
            Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")),
            Path(os.environ.get("PROGRAMFILES", r"C:\Program Files"))
        ]:
            candidate = base / "Steam"
            if (candidate / "steamapps").is_dir():
                roots.append(candidate)

        try:
            import winreg
            for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
                for key_path in (
                    r"Software\Valve\Steam",
                    r"Software\WOW6432Node\Valve\Steam"
                ):
                    try:
                        with winreg.OpenKey(hive, key_path) as key:
                            value, _ = winreg.QueryValueEx(key, "SteamPath")
                            candidate = Path(value)
                            if (candidate / "steamapps").is_dir() and candidate not in roots:
                                roots.append(candidate)
                    except OSError:
                        pass
        except ImportError:
            pass

        return roots

    def find_exe(self, folder):
        if not folder.is_dir():
            return None

        ignored = ("uninstall", "crash", "setup", "redist", "update", "helper")
        candidates = []

        try:
            visited = 0
            for base, dirs, files in os.walk(folder):
                visited += 1
                if visited > 180:
                    break

                depth = len(Path(base).relative_to(folder).parts)
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                if depth >= 2:
                    dirs[:] = []

                for filename in files:
                    low = filename.lower()
                    if low.endswith(".exe") and not any(x in low for x in ignored):
                        path = Path(base) / filename
                        try:
                            size = path.stat().st_size
                            if size > 256 * 1024:
                                candidates.append((size, path))
                        except OSError:
                            pass
        except OSError:
            return None

        return max(candidates, default=(0, None), key=lambda item: item[0])[1]

    def scan_steam(self):
        found = []

        for root in self.steam_roots():
            libraries = [root / "steamapps"]
            vdf = root / "steamapps" / "libraryfolders.vdf"

            if vdf.exists():
                try:
                    content = vdf.read_text(encoding="utf-8", errors="ignore")
                    for path in re.findall(r'"path"\s+"([^"]+)"', content):
                        library = Path(path.replace("\\\\", "\\")) / "steamapps"
                        if library.is_dir() and library not in libraries:
                            libraries.append(library)
                except OSError:
                    pass

            for library in libraries:
                for manifest in library.glob("appmanifest_*.acf"):
                    try:
                        content = manifest.read_text(encoding="utf-8", errors="ignore")
                        name = re.search(r'"name"\s+"([^"]+)"', content)
                        appid = re.search(r'"appid"\s+"?(\d+)', content)
                        install = re.search(r'"installdir"\s+"([^"]+)"', content)

                        if not name or not appid:
                            continue

                        folder = library / "common" / (
                            install.group(1) if install else name.group(1)
                        )
                        # Steam's app URI is enough to launch the game.
                        # Avoid recursively walking every game's install folder
                        # during scans; it can cause long disk stalls.
                        found.append({
                            "title": name.group(1),
                            "source": "Steam",
                            "target": f"steam://rungameid/{appid.group(1)}",
                            "process_name": "",
                            "category": "Uncategorized",
                            "arguments": "",
                            "performance_mode": "Default",
                            "launches": 0,
                            "play_seconds": 0,
                            "last_played": "",
                            "favorite": False
                        })
                    except OSError:
                        continue

        return found

    def scan_epic(self):
        found = []
        folder = (
            Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData"))
            / "Epic" / "EpicGamesLauncher" / "Data" / "Manifests"
        )

        if not folder.is_dir():
            return found

        for manifest in folder.glob("*.item"):
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
                name = data.get("DisplayName") or data.get("AppName")
                location = Path(data.get("InstallLocation", ""))
                launch = data.get("LaunchExecutable", "")

                if not name or not location.is_dir():
                    continue

                target = location / launch if launch else self.find_exe(location)
                if target and Path(target).exists():
                    found.append({
                        "title": name,
                        "source": "Epic Games",
                        "target": str(target),
                        "process_name": Path(target).name,
                        "category": "Uncategorized",
                        "arguments": "",
                        "performance_mode": "Default",
                        "launches": 0,
                        "play_seconds": 0,
                        "last_played": "",
                        "favorite": False
                    })
            except (OSError, ValueError, TypeError):
                continue

        return found

    def scan_games(self):
        if self._scan_running or self._closing:
            return

        self._scan_running = True
        self.status_var.set("Scanning installed games...")

        def worker():
            found = []
            errors = []

            for scanner in (self.scan_steam, self.scan_epic):
                try:
                    found.extend(scanner())
                except Exception as error:
                    errors.append(str(error))

            if not self._closing:
                try:
                    self.root.after(0, lambda: self.finish_scan(found, errors))
                except tk.TclError:
                    pass

        threading.Thread(target=worker, daemon=True, name="UniGameScanner").start()

    def finish_scan(self, found, errors):
        if self._closing:
            return

        existing = {
            (g.get("title", "").lower(), g.get("source", "").lower())
            for g in self.games
        }
        existing_targets = {
            g.get("target", "").lower() for g in self.games
        }

        added = 0
        for game in found:
            key = (game["title"].lower(), game["source"].lower())
            target = game["target"].lower()

            if key in existing or target in existing_targets:
                continue

            self.games.append(game)
            existing.add(key)
            existing_targets.add(target)
            added += 1

        self._scan_running = False
        self.save_all()
        self.status_var.set(f"Scan complete · {added} new games")
        self.show_page("Library")

        message = f"Found {len(found)} supported installations.\nAdded {added} new games."
        if errors:
            message += "\n\nSome scanners reported errors:\n" + "\n".join(errors)

        messagebox.showinfo("Scan complete", message)

    # --------------------------------------------------------
    # PLAYTIME TRACKING
    # --------------------------------------------------------

    def read_running_processes(self):
        try:
            result = subprocess.run(
                ["tasklist.exe", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
            )
            return {
                row[0].lower()
                for row in csv.reader(io.StringIO(result.stdout))
                if row
            }
        except (OSError, subprocess.TimeoutExpired):
            return set()

    def update_playtime(self):
        if self._closing:
            return

        if self._playtime_running:
            self.root.after(5000, self.update_playtime)
        if self.cloud.logged_in:
            self.root.after(60000, self.presence_heartbeat)
            return

        self._playtime_running = True

        def worker():
            processes = self.read_running_processes()
            if not self._closing:
                try:
                    self.root.after(0, lambda: self.apply_playtime(processes))
                except tk.TclError:
                    pass

        threading.Thread(target=worker, daemon=True, name="UniGamePlaytime").start()

    def apply_playtime(self, processes):
        if self._closing:
            return

        now = time.monotonic()
        running = {}
        changed = False

        for game in self.games:
            process = str(game.get("process_name", "")).strip().lower()
            if not process or process not in processes:
                continue

            key = game.get("title", "")
            running[key] = now
            previous = self._tracked_processes.get(key)

            if previous is not None:
                elapsed = max(0, min(15, int(now - previous)))
                if elapsed:
                    game["play_seconds"] = int(game.get("play_seconds", 0) or 0) + elapsed
                    changed = True

        self._tracked_processes = running
        if changed and now - self._last_playtime_save >= 60:
            self.save_all()
            self._last_playtime_save = now

        self._playtime_running = False
        if not self._closing:
            self.root.after(5000, self.update_playtime)
        if self.cloud.logged_in:
            self.root.after(60000, self.presence_heartbeat)

    # --------------------------------------------------------
    # CLOSE
    # --------------------------------------------------------

    def close(self):
        self._closing = True
        try:
            self.save_all()
            if self.cloud.logged_in:
                payload = {"user_id": self.cloud.user_id, "is_online": False, "last_seen": datetime.utcnow().isoformat(timespec="seconds") + "Z"}
                threading.Thread(target=lambda: self.cloud.rest("user_presence", "?on_conflict=user_id", "POST", payload, "resolution=merge-duplicates,return=minimal"), daemon=True).start()
        except OSError as error:
            print("Could not save data:", error)
        self.root.destroy()

    def run(self):
        self.root.mainloop()


# ============================================================
# BUILD MODE
# ============================================================

def build_exe():
    root = Path(__file__).resolve().parent
    script = Path(__file__).resolve()
    icon = root / "UniGameLauncher.ico"
    try:
        from PIL import Image
        from io import BytesIO
        logo = Image.open(BytesIO(base64.b64decode(LOGO_GIF_BASE64))).convert("RGBA")
        logo.save(icon, format="ICO", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)])
    except ImportError:
        print("Pillow is needed to create the Windows EXE icon.")
        print("Install it with: python -m pip install pillow")
    except Exception as error:
        print("Could not generate the EXE icon:", error)

    command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        "--name", "UniGameLauncher-Setup",
        "--distpath", str(root / "dist"),
        "--workpath", str(root / "build"),
        "--specpath", str(root / "build")
    ]

    if icon.is_file():
        command.extend(["--icon", str(icon)])

    command.append(str(script))

    print("Building the standalone UniGame installer...")
    print("This may take a few minutes.")

    result = subprocess.run(command, cwd=root)

    if result.returncode == 0:
        print("\nBUILD SUCCESSFUL")
        print("Installer:", root / "dist" / "UniGameLauncher-Setup.exe")
    else:
        print("\nBUILD FAILED")

    return result.returncode


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    if "--build" in sys.argv:
        raise SystemExit(build_exe())

    frozen = getattr(sys, "frozen", False)
    installed_argument = "--installed" in sys.argv

    if frozen and not installed_argument:
        # If this EXE is already in the installation directory,
        # launch the application instead of showing the installer again.
        try:
            already_installed = Path(sys.executable).resolve() == INSTALLED_EXE.resolve()
        except OSError:
            already_installed = False

        if already_installed:
            Launcher().run()
        else:
            Installer().run()
    else:
        Launcher().run()

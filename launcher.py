"""UniGame Launcher - single-file Windows launcher and PyInstaller builder.

Run `python launcher.py` to build dist/UniGameLauncher.exe.
Run `python launcher.py --run` to launch the app directly from source.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

APP_NAME = "UniGame Launcher"
SOURCES = ("Steam", "Epic Games", "Roblox", "itch.io", "Standalone")
BG = "#111315"
PANEL = "#1a1d20"
CARD = "#202428"
TEXT = "#f2f3f5"
MUTED = "#9ba1a9"
ACCENT = "#f05a3e"


def data_file() -> Path:
    base = Path(os.environ.get("APPDATA", Path.home()))
    folder = base / "UniGameLauncher"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "games.json"


class Launcher:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry("1000x680")
        self.root.minsize(760, 520)
        self.root.configure(bg=BG)
        self.games: list[dict[str, str]] = []
        self.query = tk.StringVar()
        self._load()
        self._style()
        self._layout()
        self.render_games()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _style(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=TEXT,
                        rowheight=36, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=PANEL, foreground=MUTED,
                        borderwidth=0, font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", "#43302d")], foreground=[("selected", TEXT)])

    def _load(self) -> None:
        try:
            self.games = json.loads(data_file().read_text(encoding="utf-8"))
            if not isinstance(self.games, list):
                self.games = []
        except (OSError, json.JSONDecodeError):
            self.games = []

    def _save(self) -> None:
        data_file().write_text(json.dumps(self.games, indent=2), encoding="utf-8")

    def _layout(self) -> None:
        sidebar = tk.Frame(self.root, bg="#0d0f10", width=205, padx=16, pady=20)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        brand = tk.Frame(sidebar, bg="#0d0f10")
        brand.pack(fill="x", pady=(0, 34))
        tk.Label(brand, text="✦", bg=ACCENT, fg="white", font=("Segoe UI", 16, "bold"),
                 width=2, height=1, padx=3, pady=4).pack(side="left", padx=(0, 10))
        tk.Label(brand, text="UniGame", bg="#0d0f10", fg=TEXT,
                 font=("Segoe UI", 15, "bold")).pack(side="left")
        tk.Label(sidebar, text="YOUR LIBRARY", bg="#0d0f10", fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=8, pady=(0, 10))
        tk.Label(sidebar, text="▦   All games", bg="#24272b", fg=TEXT,
                 font=("Segoe UI", 10, "bold"), padx=12, pady=11, anchor="w").pack(fill="x")
        tk.Label(sidebar, text="One library for all your PC games.", bg="#0d0f10", fg=MUTED,
                 wraplength=165, justify="left", font=("Segoe UI", 9)).pack(side="bottom", anchor="w", pady=8)

        main = tk.Frame(self.root, bg=BG, padx=34, pady=24)
        main.pack(side="left", fill="both", expand=True)
        top = tk.Frame(main, bg=BG)
        top.pack(fill="x", pady=(0, 30))
        self.search = tk.Entry(top, textvariable=self.query, bg=PANEL, fg=TEXT, insertbackground=TEXT,
                               relief="flat", font=("Segoe UI", 10))
        self.search.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 12))
        self.search.insert(0, "Search games")
        self.search.configure(fg=MUTED)
        self.search.bind("<FocusIn>", self._clear_placeholder)
        self.search.bind("<KeyRelease>", lambda _event: self.render_games())
        self._button(top, "＋  Add game", self.add_game, primary=True).pack(side="right", ipady=7)

        tk.Label(main, text="MY COLLECTION", bg=BG, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        heading = tk.Frame(main, bg=BG)
        heading.pack(fill="x", pady=(2, 20))
        tk.Label(heading, text="Library", bg=BG, fg=TEXT,
                 font=("Segoe UI", 28, "bold")).pack(side="left")
        self.count_label = tk.Label(heading, text="", bg=BG, fg=MUTED,
                                    font=("Segoe UI", 10))
        self.count_label.pack(side="left", padx=12, pady=(12, 0))

        self.list_area = tk.Frame(main, bg=BG)
        self.list_area.pack(fill="both", expand=True)
        bottom = tk.Frame(main, bg=BG)
        bottom.pack(fill="x", pady=(18, 0))
        self._button(bottom, "▶  Play game", self.play_selected, primary=True).pack(side="left", ipady=6)
        self._button(bottom, "Remove selected", self.remove_selected).pack(side="right", ipady=6)

    def _clear_placeholder(self, _event: object) -> None:
        if self.search.get() == "Search games":
            self.search.delete(0, "end")
            self.search.configure(fg=TEXT)

    def _button(self, parent: tk.Widget, label: str, command: object, primary: bool = False) -> tk.Button:
        return tk.Button(parent, text=label, command=command, bg=ACCENT if primary else CARD,
                         fg="white" if primary else TEXT, activebackground="#d74b33" if primary else "#2b3035",
                         activeforeground="white", relief="flat", bd=0, padx=14, pady=8,
                         font=("Segoe UI", 9, "bold"), cursor="hand2")

    def render_games(self) -> None:
        for child in self.list_area.winfo_children():
            child.destroy()
        query = self.query.get().strip().lower()
        if query == "search games":
            query = ""
        visible = [(index, game) for index, game in enumerate(self.games)
                   if query in game.get("title", "").lower()]
        self.count_label.configure(text=f"{len(self.games)} games")
        if not visible:
            message = "No games added yet. Choose Add game to build your library." if not query else "No games match your search."
            tk.Label(self.list_area, text=message, bg=BG, fg=MUTED,
                     font=("Segoe UI", 11)).pack(anchor="w", pady=24)
            self.selected_index = None
            return
        self.selected_index = None
        self.rows: dict[int, tk.Frame] = {}
        for index, game in visible:
            row = tk.Frame(self.list_area, bg=CARD, padx=14, pady=11, cursor="hand2")
            row.pack(fill="x", pady=4)
            badge = tk.Label(row, text=game.get("source", "PC"), bg="#34383e", fg="#d9dce0",
                             padx=9, pady=5, font=("Segoe UI", 8, "bold"))
            badge.pack(side="left", padx=(0, 14))
            tk.Label(row, text=game.get("title", "Untitled"), bg=CARD, fg=TEXT,
                     font=("Segoe UI", 10, "bold")).pack(side="left")
            tk.Label(row, text="Click to select", bg=CARD, fg=MUTED,
                     font=("Segoe UI", 8)).pack(side="right")
            self.rows[index] = row
            for widget in (row, badge, *row.winfo_children()):
                widget.bind("<Button-1>", lambda _event, i=index: self.select(i))

    def select(self, index: int) -> None:
        self.selected_index = index
        for i, row in getattr(self, "rows", {}).items():
            color = "#43302d" if i == index else CARD
            row.configure(bg=color)
            for widget in row.winfo_children():
                widget.configure(bg=color if isinstance(widget, tk.Label) and widget.cget("text") == self.games[index].get("title") else
                                 ("#59413d" if i == index and widget.cget("text") == self.games[i].get("source") else
                                  ("#34383e" if widget.cget("text") == self.games[i].get("source") else color)))

    def add_game(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Add game")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("470x300")
        form = tk.Frame(dialog, bg=BG, padx=22, pady=20)
        form.pack(fill="both", expand=True)
        tk.Label(form, text="Add a game", bg=BG, fg=TEXT,
                 font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(0, 16))
        tk.Label(form, text="Game name", bg=BG, fg=MUTED).pack(anchor="w")
        title_entry = tk.Entry(form, bg=PANEL, fg=TEXT, insertbackground=TEXT, relief="flat")
        title_entry.pack(fill="x", ipady=8, pady=(4, 12))
        tk.Label(form, text="Platform", bg=BG, fg=MUTED).pack(anchor="w")
        source = tk.StringVar(value="Steam")
        ttk.Combobox(form, textvariable=source, values=SOURCES, state="readonly").pack(fill="x", ipady=3, pady=(4, 12))
        tk.Label(form, text="Executable path or launch URI (e.g. steam://rungameid/123)",
                 bg=BG, fg=MUTED).pack(anchor="w")
        target_row = tk.Frame(form, bg=BG)
        target_row.pack(fill="x", pady=(4, 15))
        target = tk.Entry(target_row, bg=PANEL, fg=TEXT, insertbackground=TEXT, relief="flat")
        target.pack(side="left", fill="x", expand=True, ipady=8)
        self._button(target_row, "Browse", lambda: self._browse(target)).pack(side="left", padx=(8, 0))

        def save() -> None:
            name, destination = title_entry.get().strip(), target.get().strip()
            if not name or not destination:
                messagebox.showwarning("Missing information", "Enter a game name and executable path or launch URI.", parent=dialog)
                return
            self.games.append({"title": name, "source": source.get(), "target": destination})
            self._save()
            self.render_games()
            dialog.destroy()

        self._button(form, "Add to library", save, primary=True).pack(anchor="e")
        title_entry.focus_set()

    @staticmethod
    def _browse(entry: tk.Entry) -> None:
        path = filedialog.askopenfilename(title="Select game executable",
                                          filetypes=[("Applications", "*.exe"), ("All files", "*.*")])
        if path:
            entry.delete(0, "end")
            entry.insert(0, path)

    def play_selected(self) -> None:
        index = getattr(self, "selected_index", None)
        if index is None:
            messagebox.showinfo("Select a game", "Select a game in your library first.", parent=self.root)
            return
        game = self.games[index]
        target = game.get("target", "").strip()
        if game.get("source") == "Steam" and target.isdigit():
            target = f"steam://rungameid/{target}"
        try:
            if target.lower().startswith(("steam://", "com.epicgames.launcher://", "roblox://", "itch://", "https://", "http://")):
                if hasattr(os, "startfile"):
                    os.startfile(target)  # type: ignore[attr-defined]
                else:
                    webbrowser.open(target)
            else:
                path = Path(target).expanduser()
                if not path.is_file():
                    raise FileNotFoundError(f"Could not find: {path}")
                os.startfile(str(path))  # type: ignore[attr-defined]
        except (OSError, FileNotFoundError) as error:
            messagebox.showerror("Couldn't launch game", str(error), parent=self.root)

    def remove_selected(self) -> None:
        index = getattr(self, "selected_index", None)
        if index is None:
            messagebox.showinfo("Select a game", "Select a game to remove first.", parent=self.root)
            return
        if messagebox.askyesno("Remove game", f"Remove {self.games[index].get('title')} from your library?", parent=self.root):
            self.games.pop(index)
            self._save()
            self.render_games()

    def close(self) -> None:
        self._save()
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def build_exe() -> int:
    root = Path(__file__).resolve().parent
    try:
        check = subprocess.run([sys.executable, "-m", "PyInstaller", "--version"],
                               capture_output=True, text=True, check=False)
    except OSError:
        check = None
    if check is None or check.returncode != 0:
        print("PyInstaller is required to build the Windows executable.")
        print(f'Install it with: "{sys.executable}" -m pip install pyinstaller')
        return 1
    command = [sys.executable, "-m", "PyInstaller", "--onefile", "--windowed", "--clean",
               "--noconfirm", "--name", "UniGameLauncher", "--distpath", str(root / "dist"),
               "--workpath", str(root / "build"), "--specpath", str(root / "build"), str(Path(__file__).resolve())]
    result = subprocess.run(command, cwd=root, check=False)
    if result.returncode == 0:
        print(f"\nBuild complete: {root / 'dist' / 'UniGameLauncher.exe'}")
    return result.returncode


if __name__ == "__main__":
    if "--run" in sys.argv:
        Launcher().run()
    else:
        raise SystemExit(build_exe())

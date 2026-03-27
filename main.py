import os
import yaml
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
from datetime import datetime

DEFAULT_PATH = os.path.expanduser("~/.config/espanso/match/base.yml")


class EspansoLite:
    def __init__(self, root):
        self.root = root
        self.root.title("Espanso GUI")
        self.root.geometry("900x650")

        self.file_path = tk.StringVar(value=DEFAULT_PATH)
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Status: unknown")

        self.matches = []
        self.filtered = []

        self.setup_style()
        self.build_ui()
        self.bind_shortcuts()
        self.load()
        self.detect_status()

    # ---------- STYLE ----------
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=24,
                        fieldbackground="white")

        style.configure("Treeview.Heading",
                        background="#e0e0e0")

    # ---------- UI ----------
    def build_ui(self):
        # ===== TOP =====
        top = tk.Frame(self.root)
        top.pack(fill="x")

        tk.Entry(top, textvariable=self.file_path).pack(side="left", fill="x", expand=True)
        tk.Button(top, text="Browse", command=self.browse).pack(side="left")
        tk.Button(top, text="Reload", command=self.load).pack(side="left")

        # ===== CONTROL =====
        ctrl = tk.Frame(self.root)
        ctrl.pack(fill="x", pady=5)

        self.btn_start = tk.Button(ctrl, text="Start", command=self.start_espanso)
        self.btn_start.pack(side="left")

        self.btn_stop = tk.Button(ctrl, text="Stop", command=self.stop_espanso)
        self.btn_stop.pack(side="left")

        self.btn_restart = tk.Button(ctrl, text="Restart", command=self.restart_espanso)
        self.btn_restart.pack(side="left")

        tk.Button(ctrl, text="Refresh", command=self.detect_status).pack(side="left")

        self.status_label = tk.Label(ctrl, textvariable=self.status_var, width=40)
        self.status_label.pack(side="right")

        tk.Frame(self.root, height=2, bg="gray").pack(fill="x", pady=5)

        # ===== SEARCH =====
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="x")

        tk.Label(search_frame, text="Search / Filter:").pack(anchor="w")
        tk.Entry(search_frame, textvariable=self.search_var).pack(fill="x")

        self.search_var.trace_add("write", lambda *_: self.apply_filter())

        # ===== FORM =====
        form = tk.Frame(self.root)
        form.pack(fill="x")

        tk.Label(form, text="Trigger").grid(row=0, column=0)
        tk.Label(form, text="Replace").grid(row=1, column=0)
        tk.Label(form, text="Vars (YAML)").grid(row=2, column=0)

        self.trigger = tk.Entry(form)
        self.replace = tk.Entry(form)
        self.vars = tk.Text(form, height=6)

        self.trigger.grid(row=0, column=1, sticky="ew")
        self.replace.grid(row=1, column=1, sticky="ew")
        self.vars.grid(row=2, column=1, sticky="ew")

        form.columnconfigure(1, weight=1)

        # ===== BUTTONS =====
        btns = tk.Frame(self.root)
        btns.pack(fill="x")

        tk.Button(btns, text="Add", command=self.add).pack(side="left")
        tk.Button(btns, text="Update", command=self.update).pack(side="left")
        tk.Button(btns, text="Delete", command=self.delete).pack(side="left")
        tk.Button(btns, text="Save", command=self.save).pack(side="right")

        # ===== MAIN CONTENT =====
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)
        main_frame.columnconfigure(0, weight=1)

        # ===== TABLE =====
        table_frame = tk.Frame(main_frame)
        table_frame.grid(row=0, column=0, sticky="nsew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("trigger", "replace"),
            show="headings"
        )

        v_scroll = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scroll = tk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        self.tree.heading("trigger", text="Trigger")
        self.tree.heading("replace", text="Replace")

        self.tree.column("trigger", width=300, anchor="w", stretch=False)
        self.tree.column("replace", width=1000, anchor="w", stretch=False)

        self.tree.tag_configure("even", background="#ffffff")
        self.tree.tag_configure("odd", background="#f2f2f2")

        self.tree.bind("<<TreeviewSelect>>", self.select)
        self.tree.bind("<Double-1>", self.select)

        # ===== LOG =====
        log_frame = tk.Frame(main_frame)
        log_frame.grid(row=1, column=0, sticky="ew")

        tk.Label(log_frame, text="Log").pack(anchor="w")

        log_container = tk.Frame(log_frame, height=150)
        log_container.pack(fill="x")
        log_container.pack_propagate(False)

        log_inner = tk.Frame(log_container)
        log_inner.pack(fill="both", expand=True)

        self.log = tk.Text(log_inner)
        log_scroll = tk.Scrollbar(log_inner, orient="vertical", command=self.log.yview)

        self.log.configure(yscrollcommand=log_scroll.set)

        self.log.pack(side="left", fill="both", expand=True)
        log_scroll.pack(side="right", fill="y")

        # 🔥 LOG COLOR TAGS
        self.log.tag_config("INFO", foreground="black")
        self.log.tag_config("ACTION", foreground="blue")
        self.log.tag_config("ERROR", foreground="red")

        tk.Button(log_frame, text="Clear Log", command=self.clear_log).pack(anchor="e")

    # ---------- Logging ----------
    def log_write(self, text, level="INFO"):
        now = datetime.now().strftime("%H:%M:%S")
        line = f"[{now}] [{level}] {text}\n"
        self.log.insert(tk.END, line, level)
        self.log.see(tk.END)

    def clear_log(self):
        self.log.delete("1.0", tk.END)

    # ---------- Command ----------
    def run_cmd(self, cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.stdout:
                self.log_write(result.stdout.strip(), "INFO")

            if result.stderr:
                self.log_write(result.stderr.strip(), "ERROR")

            return result.stdout.strip()
        except Exception as e:
            self.log_write(str(e), "ERROR")
            return ""

    # ---------- Espanso ----------
    def get_status(self):
        out = self.run_cmd(["espanso", "status"])
        if "is running" in out:
            return "running"
        return "stopped"

    def update_status_label(self, status):
        count = len(self.filtered)
        self.status_var.set(f"Status: {status} | {count} items")
        color = "green" if status == "running" else "red"
        self.status_label.config(fg=color)

    def update_buttons_by_status(self, status):
        if status == "running":
            self.btn_start.config(state="disabled")
            self.btn_stop.config(state="normal")
        else:
            self.btn_start.config(state="normal")
            self.btn_stop.config(state="disabled")

    def detect_status(self):
        status = self.get_status()
        self.update_status_label(status)
        self.update_buttons_by_status(status)

    def start_espanso(self):
        if self.get_status() == "running":
            self.log_write("Espanso already running.", "INFO")
            return
        self.log_write("Starting espanso (unmanaged)...", "ACTION")
        self.run_cmd(["espanso", "start", "--unmanaged"])
        self.detect_status()

    def stop_espanso(self):
        if self.get_status() == "stopped":
            self.log_write("Espanso already stopped.", "INFO")
            return
        self.log_write("Stopping espanso...", "ACTION")
        self.run_cmd(["espanso", "stop"])
        self.detect_status()

    def restart_espanso(self):
        self.log_write("Restarting espanso (unmanaged)...", "ACTION")
        self.run_cmd(["espanso", "stop"])
        self.run_cmd(["espanso", "start", "--unmanaged"])
        self.detect_status()

    # ---------- Shortcuts ----------
    def bind_shortcuts(self):
        self.root.bind("<Control-n>", lambda e: self.add())
        self.root.bind("<Control-s>", lambda e: self.save())
        self.root.bind("<Delete>", lambda e: self.delete())

    # ---------- YAML ----------
    def load(self):
        try:
            with open(self.file_path.get(), "r") as f:
                data = yaml.safe_load(f) or {}
                self.matches = data.get("matches", [])
            self.apply_filter()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save(self):
        try:
            with open(self.file_path.get(), "w") as f:
                yaml.dump({"matches": self.matches}, f, sort_keys=False)
            messagebox.showinfo("Saved", "Saved")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def apply_filter(self):
        q = self.search_var.get().lower()
        if not q:
            self.filtered = self.matches
        else:
            self.filtered = [
                m for m in self.matches
                if q in str(m.get("trigger", "")).lower()
                or q in str(m.get("replace", "")).lower()
            ]
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for i, m in enumerate(self.filtered):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", iid=i,
                             values=(m.get("trigger", ""), m.get("replace", "")),
                             tags=(tag,))

    def select(self, event):
        sel = self.tree.selection()
        if not sel:
            return

        m = self.filtered[int(sel[0])]

        self.trigger.delete(0, tk.END)
        self.replace.delete(0, tk.END)
        self.vars.delete("1.0", tk.END)

        self.trigger.insert(0, m.get("trigger", ""))
        self.replace.insert(0, m.get("replace", ""))

        if "vars" in m:
            self.vars.insert("1.0", yaml.dump(m["vars"], sort_keys=False))

    def build_entry(self):
        entry = {
            "trigger": self.trigger.get().strip(),
            "replace": self.replace.get().strip()
        }

        vars_text = self.vars.get("1.0", tk.END).strip()
        if vars_text:
            try:
                entry["vars"] = yaml.safe_load(vars_text)
            except Exception as e:
                raise ValueError(f"Invalid YAML in vars:\n{e}")

        return entry

    def add(self):
        self.matches.append(self.build_entry())
        self.apply_filter()

    def update(self):
        sel = self.tree.selection()
        if not sel:
            return
        original = self.filtered[int(sel[0])]
        idx = self.matches.index(original)
        self.matches[idx] = self.build_entry()
        self.apply_filter()

    def delete(self):
        sel = self.tree.selection()
        if not sel:
            return
        if not messagebox.askyesno("Confirm", "Delete selected entry?"):
            return
        original = self.filtered[int(sel[0])]
        self.matches.remove(original)
        self.apply_filter()

    def browse(self):
        path = filedialog.askopenfilename(filetypes=[("YAML", "*.yml *.yaml")])
        if path:
            self.file_path.set(path)


if __name__ == "__main__":
    root = tk.Tk()
    app = EspansoLite(root)
    root.mainloop()

## 🧩 Overview

**EspansoLite** is a lightweight graphical interface for managing Espanso configuration files.

It provides a simple and efficient way to edit YAML-based text expansion rules, while also allowing direct control over the Espanso process—all from a single desktop application.

Built with **Python + Tkinter**, it requires no additional GUI frameworks and runs cross-platform.

---

## 🚀 Key Features

### 🗂 YAML Match Management

* Load and edit Espanso `matches` from YAML files
* Full CRUD operations:

  * Add new entries
  * Update existing entries
  * Delete entries
* Inline editing for:

  * `trigger`
  * `replace`
  * `vars` (with YAML parsing & validation)

---

### 🔍 Live Search & Filtering

* Instant filtering while typing
* Matches both:

  * trigger text
  * replacement text
* Case-insensitive search

---

### 🖥 Process Control (Espanso)

* Start Espanso (`--unmanaged` mode)
* Stop Espanso
* Restart Espanso safely
* Real-time status detection:

  * Running / Stopped
* Smart button state management:

  * Prevents multiple spawn instances
  * Disables invalid actions automatically

---

### 📊 Structured Logging System

* Timestamped logs (`HH:MM:SS`)
* Log levels:

  * `INFO`
  * `ACTION`
  * `ERROR`
* Color-coded output:

  * Black → Info
  * Blue → Actions
  * Red → Errors
* Captures:

  * Command output (stdout)
  * Command errors (stderr)

---

### 📋 Table View (Improved UX)

* Scrollable table with:

  * Vertical scrollbar
  * Horizontal scrollbar
* Fixed column widths for better readability
* Alternating row colors (striped view)
* Handles large datasets efficiently

---

### 🧾 Log Panel (Fixed Layout)

* Dedicated log area with:

  * Fixed height (no layout collapse)
  * Vertical scrollbar
* Auto-scroll to latest entry
* Clear log button

---

### ⌨️ Keyboard Shortcuts

* `Ctrl + N` → Add entry
* `Ctrl + S` → Save YAML
* `Delete` → Remove selected entry

---

### 🛡 Data Validation

* YAML parsing for `vars` field
* Prevents invalid YAML from being saved
* Clear error feedback via dialog

---

## ⚙️ Technical Highlights

* Pure standard library + `PyYAML` (no heavy dependencies)
* Deterministic subprocess handling (no race conditions)
* State-driven UI (buttons reflect real system state)
* Modular structure:

  * UI layer
  * Command execution layer
  * Data handling layer

---

## 🎯 Design Goals

* Simplicity over complexity
* No external GUI frameworks
* Safe interaction with Espanso
* Fast editing workflow for power users

---

## ⚠️ Notes

* Designed for **Espanso unmanaged mode**
* Requires `espanso` binary available in system `PATH`
* Assumes YAML structure contains `matches` key

---
<p align="center">
  <img src="./screenshots/main-ui.png" width="800">
</p>

---

## ⚙️ Requirements

* Python 3.8+
* PyYAML>=6.0
* Espanso installed

Install Espanso:
[https://espanso.org/install/](https://espanso.org/install/)

---

## 📥 Installation

```
git clone https://github.com/YOUR_USERNAME/espanso-lite.git
cd espanso-lite

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python main.py
```
OR without activating:
```
~/scripts/espanso-lite-env/bin/python ~/scripts/espanso-lite/main.py
```

## 🧠 How It Works

* Loads Espanso config from:

```
~/.config/espanso/match/base.yml
```

* Displays `matches` in a table
* Allows CRUD operations on entries
* Saves directly back to YAML file

---

## 🧪 Example YAML

```
matches:
  - trigger: ":hello"
    replace: "Hello world!"

  - trigger: ":date"
    replace: "{{mydate}}"
    vars:
      - name: mydate
        type: date
```


## ⚠️ Notes

- Espanso should not be running as a service when using this app (uses --unmanaged mode). If you run Espanso as a service, use [mainservice.py](./mainservice.py) instead.
- Uses `espanso start --unmanaged` (see implementation in [main.py](./main.py))
- Requires the espanso binary to be available in PATH
- YAML errors in `vars` are validated (see handling in [main.py](./main.py))
---

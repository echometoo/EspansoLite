# EspansoLite

A lightweight GUI manager for Espanso (text expander) built with Python + Tkinter.

This tool allows you to:

* Manage Espanso YAML matches visually
* Start / Stop / Restart Espanso
* Search and edit triggers quickly
* View command logs

---

## 📦 Features

* GUI-based YAML editor for Espanso
* Live filtering/search
* Start/Stop/Restart Espanso from UI
* YAML validation for `vars`
* Built-in log panel

---

## 📁 Project Structure

```
espanso-lite/
│── main.py
│── requirements.txt
│── README.md
│── .gitignore
```

---

## ⚙️ Requirements

* Python 3.8+
* Espanso installed

Install Espanso:
[https://espanso.org/install/](https://espanso.org/install/)

---

## 📥 Installation

### 1. Clone repository

```
git clone https://github.com/YOUR_USERNAME/espanso-lite.git
cd espanso-lite
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the application:

```
python main.py
```

---

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

---

## 🛠 Controls

| Button  | Function        |
| ------- | --------------- |
| Start   | Start espanso   |
| Stop    | Stop espanso    |
| Restart | Restart espanso |
| Refresh | Update status   |

---

## ⌨️ Shortcuts

| Shortcut | Action          |
| -------- | --------------- |
| Ctrl + N | Add entry       |
| Ctrl + S | Save            |
| Delete   | Delete selected |

---

## ⚠️ Notes

* Uses `espanso start --unmanaged`
* Requires espanso binary in PATH
* YAML errors in `vars` will be validated

---

## 🐞 Known Issues

* No schema validation for full espanso config
* Assumes `matches` key exists

---


## 🧾 requirements.txt

```
PyYAML
```

## 📌 main.py

Place your provided Python script here unchanged.

---


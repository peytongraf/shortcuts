# Shortcuts App

A streamlined GTK-based application for managing and navigating text files through an intuitive tabbed interface.


## Features
- Effortlessly navigate between tabs using keyboard shortcuts, including Tab, h, or l for Vim-style motion.
- Fully customizable user interface via an editable style.css file.

## Requirements
- Python 3
- GTK 4
- `python-gi` (PyGObject)

## Installation
1. Clone the repository:
   ```bash
    mkdir -p ~/Development
    cd ~/Development
    git clone https://github.com/peytongraf/shortcuts-app.git
    cd shortcuts-app
2. Make the sciprt executable
    ```bash
    chmod +x shortcuts.py

## Hyprland integration
- To launch the Shortcuts App using a keybind in Hyprland, add the following line to your hyprland.conf file, replacing $mainMod and S with your desired modifier and key:
```bash
    bind = $mainMod, S, exec, ~/Development/shortcuts-app/shortcuts.py

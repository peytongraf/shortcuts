# Shortcuts

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
    cd ~/.local/share
    git clone https://github.com/peytongraf/shortcuts.git
    cd shortcuts

2. Make the script executable
    ```bash
    chmod +x shortcuts.py

3. (Optional) Create a symbolic link to run the app from anywhere: 
    ```bash
    ln -s ~/.local/share/shortcuts/shortcuts.py ~/.local/bin/shortcuts

## Update
- To update the Shortcuts App to the latest version:

1. Navigate to the app's directory:
    ```bash
    cd ~/.local/share/shortcuts
2. Pull the latest changes from the repository:
    ```bash
    git pull origin main

## Hyprland integration
- To launch the Shortcuts App using a keybind in Hyprland, add the following line to your hyprland.conf file, replacing $mainMod and S with your desired modifier and key:
```bash
    bind = $mainMod, S, exec, ~/.local/share/shortcuts/shortcuts.py

#!/usr/bin/env python3

import os
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk

# App Constants
APP_NAME = "shortcuts"
CONFIG_DIR = os.path.expanduser(f"~/.config/{APP_NAME}/")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.conf")
STYLE_FILE = os.path.join(CONFIG_DIR, "style.css")
KEYBINDS_DIR = os.path.join(CONFIG_DIR, "keybinds")
HYPRLAND_CONFIG_FILE = os.path.expanduser("~/.config/hypr/hyprland.conf")

# Ensure the config directory and default files exist
os.makedirs(CONFIG_DIR, exist_ok=True)

if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as f:
        f.write("font_size=16\n")  # Example setting

if not os.path.exists(STYLE_FILE):
    with open(STYLE_FILE, "w") as f:
        f.write("/* Add custom CSS here */\n")

# Create a default text file if none exists
if not os.listdir(KEYBINDS_DIR):
    default_file = os.path.join(KEYBINDS_DIR, "default")
    with open(default_file, "w") as f:
        f.write("Welcome to the shortcuts app!\n")


# Helper Functions
def load_settings():
    settings = {}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE) as f:
            for line in f:
                # Remove comments and strip whitespace
                line = line.split("#", 1)[0].strip()
                # Skip empty lines after stripping
                if not line:
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    settings[key.strip()] = value.strip()
    else:
        print(f"Settings file not found at {SETTINGS_FILE}")
    return settings


# Helper Functions
def load_keybinds(file_path):
    if os.path.exists(file_path):
        with open(file_path) as f:
            return f.read()
    else:
        print(f"File not found at {file_path}")
        return "No text available."


def load_hyprland_keybinds():
    keybinds = {}

    if os.path.exists(HYPRLAND_CONFIG_FILE):
        with open(HYPRLAND_CONFIG_FILE) as f:
            for line in f:
                # Skip comments and empty lines
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Look for keybind lines (e.g., "bind = <modifiers>, <key>, exec <command>")
                if line.startswith("bind"):
                    try:
                        # Extract the keybind definition after "bind ="
                        _, keybind_definition = line.split("=", 1)
                        keybind_definition = keybind_definition.strip()

                        # Split into modifiers, key, and command
                        parts = keybind_definition.split(",")
                        if len(parts) >= 3:
                            modifiers = parts[0].strip()
                            key = parts[1].strip()
                            command = ",".join(parts[2:]).strip()

                            # Store the key and its command as a key-value pair
                            keybinds[f"{modifiers} + {key}"] = command
                    except ValueError:
                        print(f"Could not parse line: {line}")
    else:
        print(f"Hyprland config file not found at {HYPRLAND_CONFIG_FILE}")

    return keybinds


# Main Application
class ShortcutsApp(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(application=app, title="Shortcuts App")

        settings = load_settings()

        window_width = settings.get("window_width", 1000)
        window_height = settings.get("window_height", 600)

        self.set_default_size(int(window_width), int(window_height))

        # Apply CSS
        self.apply_css()

        # Load all text files
        self.text_files = [
            os.path.join(KEYBINDS_DIR, f) for f in os.listdir(KEYBINDS_DIR)
        ]
        self.current_index = 0

        # Create the UI components
        self.create_ui()

        # Add a key press event controller
        controller = Gtk.EventControllerKey.new()
        controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(controller)

    def create_ui(self):
        """
        Create the main UI for the application, including the notebook for tabs
        and dynamically arranging key-value pairs into a grid with multiple columns.
        """
        settings = load_settings()
        vbox_spacing = int(settings.get("vbox_spacing", 10))
        columns = int(settings.get("columns", 3))  # Default to 3 columns
        print(f"vbox_spacing is set to {vbox_spacing}, columns set to {columns}")

        # Create a vertical box to hold the title and content
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=vbox_spacing)
        vbox.set_css_classes(
            ["main-container"]
        )  # Assign CSS class for the main container

        # Create and configure the title label
        title_label = Gtk.Label(label="Shortcuts")
        title_label.set_xalign(0.5)  # Center the label horizontally
        title_label.set_css_classes(
            ["title-label"]
        )  # Add a custom CSS class for styling
        vbox.append(title_label)

        # Create a notebook for tabs
        self.notebook = Gtk.Notebook()
        self.notebook.set_tab_pos(Gtk.PositionType.TOP)
        self.notebook.set_scrollable(True)
        # Apply CSS to the notebook container
        self.notebook.set_css_classes(["notebook-container"])

        # Create a tab for each text file
        for file_path in self.text_files:
            file_name = os.path.basename(file_path)
            print(f"Processing file: {file_name}")
            tab_label = Gtk.Label(label=file_name)

            # Parse the text file content into key-value pairs
            text_content = load_keybinds(file_path)
            key_value_pairs = []
            for line in text_content.splitlines():
                if "=" in line:
                    key, value = line.split("=", 1)
                    key_value_pairs.append((key.strip(), value.strip()))
                else:
                    print(f"Ignoring invalid line in {file_path}: {line}")

            print(f"Loaded key-value pairs from {file_path}: {key_value_pairs}")

            # Create a grid with the key-value pairs
            grid = self.create_row(key_value_pairs, columns)
            print(f"Created grid with {len(key_value_pairs)} pairs.")

            # Configure the scroll window
            scroll = Gtk.ScrolledWindow()
            scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            scroll.set_child(grid)
            scroll.set_has_frame(False)  # Remove the frame around the scrollable window

            # Add the scrollable grid to the notebook
            self.notebook.append_page(scroll, tab_label)

        # Add the Hyprland tab
        self.add_hyprland_tab()  # <--- Call the method here

        # Add the notebook to the vertical box
        vbox.append(self.notebook)

        # Set the vertical box as the main window content
        self.set_child(vbox)

    def add_hyprland_tab(self):
        """Add a tab for Hyprland keybinds."""
        print("Adding Hyprland keybinds tab.")  # Debug message
        tab_label = Gtk.Label(label="Hyprland Keybinds")

        # Load Hyprland keybinds
        keybinds = load_hyprland_keybinds()
        if not keybinds:
            print("No Hyprland keybinds found.")  # Debug message
            keybinds = {"No Keybinds": "No Commands"}

        key_value_pairs = list(keybinds.items())  # Convert dictionary to list of tuples
        print(f"Loaded Hyprland keybinds: {key_value_pairs}")  # Debug message

        # Get the number of columns from settings
        settings = load_settings()
        columns = int(settings.get("columns", 3))  # Default to 3 columns

        # Create a grid with the key-value pairs
        grid = self.create_row(key_value_pairs, columns)

        # Add the grid to a scrollable window
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_child(grid)

        # scroll.set_has_frame(False)

        # Add the scrollable grid to the notebook
        self.notebook.append_page(scroll, tab_label)

    def create_row(self, key_value_pairs, columns):
        """
        Create a Gtk.Grid with key-value pairs arranged in the specified number of columns.

        Args:
            key_value_pairs (list of tuples): A list of (key, value) pairs to display.
            columns (int): The number of columns to arrange the grid.
        """
        settings = load_settings()
        column_spacing = int(settings.get("column_spacing", 20))
        row_spacing = int(settings.get("row_spacing", 10))

        grid = Gtk.Grid()

        grid.set_column_spacing(column_spacing)  # Space between columns
        grid.set_row_spacing(row_spacing)  # Space between rows
        grid.set_css_classes(["columns-container"])

        grid.set_hexpand(True)
        grid.set_vexpand(True)

        row = 0
        col = 0
        for key, value in key_value_pairs:
            print(
                f"Adding key: {key}, value: {value} to grid at row {row}, column {col}"
            )

            # Create a horizontal box for the row
            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            row_box.set_css_classes(["row-box"])  # Assign the CSS class for styling

            # Key label (aligned left)
            key_label = Gtk.Label(label=key)
            key_label.set_xalign(0)  # Align text to the left
            key_label.set_hexpand(True)  # Allow it to expand and push the keybind
            key_label.set_css_classes(["shortcut-name"])
            row_box.append(key_label)

            # Value label (aligned right)
            value_label = Gtk.Label(label=value)
            value_label.set_xalign(1)  # Align text to the right
            value_label.set_halign(Gtk.Align.END)  # Align it to the end of the row
            value_label.set_hexpand(True)
            value_label.set_css_classes(["shortcut-key"])
            row_box.append(value_label)

            # Add the row box to the grid
            grid.attach(row_box, col, row, 1, 1)

            # Move to the next column, or wrap to the next row if needed
            col += 1
            if col >= columns:
                col = 0
                row += 1

        return grid

    def on_key_pressed(self, controller, keyval, keycode, state):
        key_name = Gdk.keyval_name(keyval)
        print(f"Key pressed: {key_name}")

        if key_name == "Escape":
            self.close()
        elif key_name in ["Right", "l"] or key_name == "Tab":
            self.switch_tab(1)  # Move to the next tab
        elif key_name in ["Left", "h"]:
            self.switch_tab(-1)  # Move to the previous tab

    def switch_tab(self, direction):
        """
        Switch between tabs in the notebook.

        Args:
            direction (int): +1 to move forward, -1 to move backward.
        """
        total_tabs = self.notebook.get_n_pages()  # Dynamically get total tab count
        if total_tabs > 0:
            # Get the current page and calculate the new page index
            current_page = self.notebook.get_current_page()
            new_page = (current_page + direction) % total_tabs
            print(f"Switching from tab {current_page} to tab {new_page}")
            self.notebook.set_current_page(new_page)

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        if os.path.exists(STYLE_FILE):
            print(f"Style.css file found at {STYLE_FILE}")
            with open(STYLE_FILE) as f:
                css_data = f.read()
                css_provider.load_from_data(css_data.encode("utf-8"))
                print("CSS loaded successfully.")
        else:
            print(f"Style.css file not found at {STYLE_FILE}")

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )


class ShortcutsAppMain(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        window = ShortcutsApp(self)
        window.present()


if __name__ == "__main__":
    app = ShortcutsAppMain()
    app.run()

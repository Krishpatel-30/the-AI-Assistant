import customtkinter as ctk
import json
import os

SETTINGS_FILE = "settings.json"


class SettingsWindow(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title("⚙ Settings")
        self.geometry("620x650")
        self.resizable(False, False)

        self.grab_set()
        self.focus()

        self.load_settings()

        title = ctk.CTkLabel(
            self,
            text="⚙ Settings",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(pady=25)

        # -----------------------------------
        # Appearance
        # -----------------------------------

        appearance_label = ctk.CTkLabel(
            self,
            text="Appearance",
            font=("Segoe UI", 16, "bold")
        )

        appearance_label.pack(anchor="w", padx=30)

        self.appearance = ctk.CTkOptionMenu(
            self,
            values=["Dark", "Light", "System"]
        )

        self.appearance.pack(
            fill="x",
            padx=30,
            pady=(8, 25)
        )

        self.appearance.set(
            self.settings["appearance"]
        )

        # -----------------------------------
        # AI Model
        # -----------------------------------

        model_label = ctk.CTkLabel(
            self,
            text="AI Model",
            font=("Segoe UI", 16, "bold")
        )

        model_label.pack(anchor="w", padx=30)

        self.model = ctk.CTkOptionMenu(
            self,
            values=[
                "Gemini 2.5 Flash",
                "Gemini 2.5 Pro"
            ]
        )

        self.model.pack(
            fill="x",
            padx=30,
            pady=(8, 25)
        )

        self.model.set(
            self.settings["model"]
        )

        # -----------------------------------
        # Temperature
        # -----------------------------------

        temp_label = ctk.CTkLabel(
            self,
            text="Temperature",
            font=("Segoe UI", 16, "bold")
        )

        temp_label.pack(anchor="w", padx=30)

        self.temperature = ctk.CTkSlider(
            self,
            from_=0,
            to=1,
            number_of_steps=10
        )

        self.temperature.pack(
            fill="x",
            padx=30,
            pady=(8, 25)
        )

        self.temperature.set(
            self.settings["temperature"]
        )

        # -----------------------------------
        # Font Size
        # -----------------------------------

        font_label = ctk.CTkLabel(
            self,
            text="Font Size",
            font=("Segoe UI", 16, "bold")
        )

        font_label.pack(anchor="w", padx=30)

        self.font = ctk.CTkOptionMenu(
            self,
            values=[
                "12",
                "13",
                "14",
                "15",
                "16",
                "18"
            ]
        )

        self.font.pack(
            fill="x",
            padx=30,
            pady=(8, 25)
        )

        self.font.set(
            str(self.settings["font"])
        )

        # -----------------------------------
        # Auto Save
        # -----------------------------------

        self.autosave = ctk.CTkCheckBox(
            self,
            text="Auto Save Chats"
        )

        self.autosave.pack(
            anchor="w",
            padx=30,
            pady=(0, 30)
        )

        if self.settings["autosave"]:
            self.autosave.select()

        # -----------------------------------
        # Save Button
        # -----------------------------------

        save = ctk.CTkButton(
            self,
            text="💾 Save Changes",
            command=self.save_settings,
            height=55,
            font=("Segoe UI", 16, "bold")
        )

        save.pack(
            fill="x",
            padx=30,
            pady=30
        )

    # -----------------------------------
    # Load Settings
    # -----------------------------------

    def load_settings(self):

        if os.path.exists(SETTINGS_FILE):

            with open(
                SETTINGS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                self.settings = json.load(f)

        else:

            self.settings = {

                "appearance": "Dark",
                "model": "Gemini 2.5 Flash",
                "temperature": 0.3,
                "font": 14,
                "autosave": True

            }

    # -----------------------------------
    # Save Settings
    # -----------------------------------

    def save_settings(self):

        self.settings = {

            "appearance": self.appearance.get(),
            "model": self.model.get(),
            "temperature": self.temperature.get(),
            "font": int(self.font.get()),
            "autosave": bool(self.autosave.get())

        }

        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.settings,
                f,
                indent=4
            )

        ctk.set_appearance_mode(
            self.settings["appearance"]
        )

        success = ctk.CTkLabel(
            self,
            text="✅ Settings Saved Successfully!",
            text_color=("green4", "lightgreen"),
            font=("Segoe UI", 13, "bold")
        )

        success.pack(pady=10)

        self.after(1200, self.destroy)
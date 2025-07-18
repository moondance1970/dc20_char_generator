import tkinter as tk
from tkinter import ttk, messagebox


class CharacterCreatorUI:
    def __init__(self, root, character_data, file_manager, pdf_generator):
        self.root = root
        self.character_data = character_data
        self.file_manager = file_manager
        self.pdf_generator = pdf_generator
        self.remaining_display = None
        self.spell_frame = None
        self.spell_listbox = None
        self.available_spells_listbox = None

        self.create_ui()

        # Initialize
        self.character_data.calculate_skills()
        self.character_data.update_remaining_skill_slots(self.remaining_display)
        self.populate_character_dropdown()

    def create_ui(self):
        """Create the main user interface"""
        # Title
        ttk.Label(self.root, text="DC20 Character Creator", font=("Helvetica", 16)).pack(pady=10)

        # Load Character Section
        self.create_load_section()

        # Character Info Section
        self.create_character_info_section()

        # Attributes Section
        self.create_attributes_section()

        # Skills Section
        self.create_skills_section()

        # Spells Section (initially hidden)
        self.create_spells_section()

        # Final Button
        self.create_final_button()

    def create_load_section(self):
        """Create the character loading section"""
        load_frame = ttk.Frame(self.root)
        load_frame.pack(pady=5)

        ttk.Label(load_frame, text="Load Existing Character:", font=("Helvetica", 12, "bold")).pack()
        char_load_frame = ttk.Frame(load_frame)
        char_load_frame.pack(pady=5)

        self.character_dropdown = ttk.Combobox(char_load_frame, textvariable=self.character_data.character_var,
                                               width=30, state="readonly")
        self.character_dropdown.pack(side="left", padx=5)

        ttk.Button(char_load_frame, text="Load", command=self.load_selected_character).pack(side="left", padx=5)
        ttk.Button(char_load_frame, text="Refresh", command=self.refresh_character_list).pack(side="left", padx=5)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)

    def create_character_info_section(self):
        """Create the character information section"""
        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=5)

        # Character Info in a grid layout
        info_grid = ttk.Frame(info_frame)
        info_grid.pack()

        ttk.Label(info_grid, text="Character Name").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Entry(info_grid, textvariable=self.character_data.name_var, width=20).grid(row=0, column=1, padx=5)

        ttk.Label(info_grid, text="Player Name").grid(row=0, column=2, sticky="w", padx=5)
        ttk.Entry(info_grid, textvariable=self.character_data.player_name_var, width=20).grid(row=0, column=3, padx=5)

        ttk.Label(info_grid, text="Ancestry").grid(row=1, column=0, sticky="w", padx=5)
        ttk.Combobox(info_grid, textvariable=self.character_data.ancestry_var, values=[
            "Human", "Elf", "Dwarf", "Orc", "Gnome", "Halfling"
        ], state="readonly", width=18).grid(row=1, column=1, padx=5)

        ttk.Label(info_grid, text="Background").grid(row=1, column=2, sticky="w", padx=5)
        ttk.Combobox(info_grid, textvariable=self.character_data.background_var, values=[
            "Soldier", "Scholar", "Outlander", "Criminal", "Acolyte", "Entertainer"
        ], width=18).grid(row=1, column=3, padx=5)

        ttk.Label(info_grid, text="Class").grid(row=2, column=0, sticky="w", padx=5)
        class_combo = ttk.Combobox(info_grid, textvariable=self.character_data.class_var,
                                   values=list(self.character_data.inventory_presets.keys()),
                                   state="readonly", width=18)
        class_combo.grid(row=2, column=1, padx=5)

        ttk.Label(info_grid, text="Subclass").grid(row=2, column=2, sticky="w", padx=5)
        ttk.Entry(info_grid, textvariable=self.character_data.subclass_var, width=20).grid(row=2, column=3, padx=5)

        ttk.Label(info_grid, text="Level").grid(row=3, column=0, sticky="w", padx=5)
        level_combo = ttk.Combobox(info_grid, textvariable=self.character_data.level_var,
                                   values=[str(i) for i in range(1, 11)], width=18, state="readonly")
        level_combo.grid(row=3, column=1, padx=5)

        def on_class_or_level_change(event):
            cls = self.character_data.class_var.get()
            self.character_data.inventory_var.set(self.character_data.inventory_presets.get(cls, ""))
            self.update_spell_section()

        class_combo.bind("<<ComboboxSelected>>", on_class_or_level_change)
        level_combo.bind("<<ComboboxSelected>>", on_class_or_level_change)

        # Inventory section
        ttk.Label(info_frame, text="Inventory").pack(pady=(10, 0))
        ttk.Entry(info_frame, textvariable=self.character_data.inventory_var, width=60).pack()

    def create_attributes_section(self):
        """Create the attributes section"""
        attr_frame = ttk.Frame(self.root)
        attr_frame.pack(pady=10)
        ttk.Label(attr_frame, text="Assign Attribute Points (Start at -2)",
                  font=("Helvetica", 12, "bold")).pack()
        points_frame = ttk.Frame(attr_frame)
        points_frame.pack()
        ttk.Label(points_frame, text="Points Remaining:").pack(side="left")
        ttk.Label(points_frame, textvariable=self.character_data.points_remaining,
                  foreground="blue", font=("Helvetica", 12, "bold")).pack(side="left")

        attr_grid = ttk.Frame(attr_frame)
        attr_grid.pack(pady=5)

        for i, name in enumerate(self.character_data.attributes):
            f = ttk.Frame(attr_grid)
            f.grid(row=0, column=i, padx=10)
            ttk.Label(f, text=name, font=("Helvetica", 10, "bold")).pack()
            control_frame = ttk.Frame(f)
            control_frame.pack()
            ttk.Button(control_frame, text="-",
                       command=lambda n=name: self.update_attributes_wrapper(n, -1), width=3).pack(side="left")
            ttk.Label(control_frame, textvariable=self.character_data.attributes[name],
                      width=3, font=("Helvetica", 12, "bold")).pack(side="left")
            ttk.Button(control_frame, text="+",
                       command=lambda n=name: self.update_attributes_wrapper(n, 1), width=3).pack(side="left")

    def create_skills_section(self):
        """Create the skills section"""
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)
        ttk.Label(self.root, text="Skills Training", font=("Helvetica", 12, "bold")).pack()
        ttk.Button(self.root, text="Reset All Skill Trainings",
                   command=self.reset_skill_trainings_wrapper).pack(pady=5)

        skills_by_attribute = {
            "Might": ["Athletics", "Intimidation"],
            "Agility": ["Acrobatics", "Stealth", "Trickery"],
            "Charisma": ["Animal", "Influence", "Insight"],
            "Intelligence": ["Investigation", "Medicine", "Survival"]
        }

        skills_frame = ttk.Frame(self.root)
        skills_frame.pack(pady=5)

        remaining_frame = ttk.Frame(self.root)
        remaining_frame.pack()
        ttk.Label(remaining_frame, text="Remaining Skill Slots:").pack(side="left")
        self.remaining_display = ttk.Label(remaining_frame, textvariable=self.character_data.remaining_skill_slots_var,
                                           foreground="blue", font=("Helvetica", 12, "bold"))
        self.remaining_display.pack(side="left")

        for col_idx, (attr, skills) in enumerate(skills_by_attribute.items()):
            col_frame = ttk.Frame(skills_frame)
            col_frame.grid(row=0, column=col_idx, padx=15, sticky="n")
            ttk.Label(col_frame, text=attr, font=("Helvetica", 10, "bold")).pack()

            for skill in skills:
                if skill not in self.character_data.skill_vars:
                    self.character_data.skill_vars[skill] = tk.StringVar(value="0")
                if skill not in self.character_data.skill_trainings:
                    self.character_data.skill_trainings[skill] = tk.StringVar(value="None")

                skill_frame = ttk.Frame(col_frame)
                skill_frame.pack(pady=2)

                skill_label = ttk.Label(skill_frame, text=skill, width=12)
                skill_label.pack()

                entry = ttk.Entry(skill_frame, textvariable=self.character_data.skill_vars[skill],
                                  width=5, state="readonly")
                entry.pack()

                def create_update_function(skill_name, entry_widget):
                    def update_entry_bg(*args):
                        level = self.character_data.skill_trainings[skill_name].get()
                        if level == "Expert":
                            entry_widget.configure(background="#d1e7dd")
                        elif level == "Trained":
                            entry_widget.configure(background="#fff3cd")
                        else:
                            entry_widget.configure(background="white")

                    return update_entry_bg

                update_func = create_update_function(skill, entry)
                self.character_data.skill_trainings[skill].trace_add("write", update_func)
                update_func()

                combo = ttk.Combobox(skill_frame, textvariable=self.character_data.skill_trainings[skill],
                                     values=list(self.character_data.training_bonus.keys()), width=8, state="readonly")
                combo.pack()
                combo.bind("<<ComboboxSelected>>", lambda e: self.calculate_skills_wrapper())

    def create_spells_section(self):
        """Create the spells section (initially hidden)"""
        self.spell_frame = ttk.Frame(self.root)
        # Don't pack initially - will be shown/hidden based on class

        ttk.Separator(self.spell_frame, orient="horizontal").pack(fill="x", pady=10)
        ttk.Label(self.spell_frame, text="Spell Selection", font=("Helvetica", 12, "bold")).pack()

        # Spell selection area
        spell_selection_frame = ttk.Frame(self.spell_frame)
        spell_selection_frame.pack(pady=10, fill="both", expand=True)

        # Available spells (left side)
        available_frame = ttk.Frame(spell_selection_frame)
        available_frame.pack(side="left", fill="both", expand=True, padx=5)

        ttk.Label(available_frame, text="Available Spells", font=("Helvetica", 10, "bold")).pack()

        # Scrollable listbox for available spells
        available_scroll_frame = ttk.Frame(available_frame)
        available_scroll_frame.pack(fill="both", expand=True)

        available_scrollbar = ttk.Scrollbar(available_scroll_frame)
        available_scrollbar.pack(side="right", fill="y")

        self.available_spells_listbox = tk.Listbox(available_scroll_frame, height=8, width=30,
                                                   yscrollcommand=available_scrollbar.set)
        self.available_spells_listbox.pack(side="left", fill="both", expand=True)
        available_scrollbar.config(command=self.available_spells_listbox.yview)

        # Buttons (center)
        button_frame = ttk.Frame(spell_selection_frame)
        button_frame.pack(side="left", padx=10)

        ttk.Button(button_frame, text="Add →", command=self.add_spell).pack(pady=5)
        ttk.Button(button_frame, text="← Remove", command=self.remove_spell).pack(pady=5)
        ttk.Button(button_frame, text="View Spell", command=self.view_spell).pack(pady=10)

        # Selected spells (right side)
        selected_frame = ttk.Frame(spell_selection_frame)
        selected_frame.pack(side="right", fill="both", expand=True, padx=5)

        ttk.Label(selected_frame, text="Known Spells", font=("Helvetica", 10, "bold")).pack()

        # Scrollable listbox for selected spells
        selected_scroll_frame = ttk.Frame(selected_frame)
        selected_scroll_frame.pack(fill="both", expand=True)

        selected_scrollbar = ttk.Scrollbar(selected_scroll_frame)
        selected_scrollbar.pack(side="right", fill="y")

        self.spell_listbox = tk.Listbox(selected_scroll_frame, height=8, width=30,
                                        yscrollcommand=selected_scrollbar.set)
        self.spell_listbox.pack(side="left", fill="both", expand=True)
        selected_scrollbar.config(command=self.spell_listbox.yview)

    def update_spell_section(self):
        """Show or hide spell section based on class"""
        class_name = self.character_data.class_var.get()
        level = int(self.character_data.level_var.get()) if self.character_data.level_var.get() else 1

        if self.character_data.is_spellcaster():
            self.spell_frame.pack(fill="both", expand=True)
            self.update_available_spells()
        else:
            self.spell_frame.pack_forget()

    def update_available_spells(self):
        """Update the available spells list"""
        if not self.available_spells_listbox:
            return

        class_name = self.character_data.class_var.get()
        level = int(self.character_data.level_var.get()) if self.character_data.level_var.get() else 1

        available_spells = self.character_data.get_spells_for_class(class_name, level)

        self.available_spells_listbox.delete(0, tk.END)
        for spell in available_spells:
            spell_data = self.character_data.spell_database[spell]
            display_text = f"{spell} (Lvl {spell_data['level']})"
            self.available_spells_listbox.insert(tk.END, display_text)

        self.update_selected_spells()

    def update_selected_spells(self):
        """Update the selected spells list"""
        if not self.spell_listbox:
            return

        self.spell_listbox.delete(0, tk.END)
        for spell in self.character_data.selected_spells:
            if spell in self.character_data.spell_database:
                spell_data = self.character_data.spell_database[spell]
                display_text = f"{spell} (Lvl {spell_data['level']})"
                self.spell_listbox.insert(tk.END, display_text)

    def add_spell(self):
        """Add selected spell to character's spell list"""
        selection = self.available_spells_listbox.curselection()
        if selection:
            spell_text = self.available_spells_listbox.get(selection[0])
            spell_name = spell_text.split(" (Lvl")[0]  # Extract spell name
            self.character_data.add_spell(spell_name)
            self.update_selected_spells()

    def remove_spell(self):
        """Remove selected spell from character's spell list"""
        selection = self.spell_listbox.curselection()
        if selection:
            spell_text = self.spell_listbox.get(selection[0])
            spell_name = spell_text.split(" (Lvl")[0]  # Extract spell name
            self.character_data.remove_spell(spell_name)
            self.update_selected_spells()

    def view_spell(self):
        """View spell details in a popup"""
        selection = self.available_spells_listbox.curselection()
        if not selection:
            selection = self.spell_listbox.curselection()
            if not selection:
                messagebox.showinfo("No Selection", "Please select a spell to view.")
                return
            spell_text = self.spell_listbox.get(selection[0])
        else:
            spell_text = self.available_spells_listbox.get(selection[0])

        spell_name = spell_text.split(" (Lvl")[0]  # Extract spell name

        if spell_name in self.character_data.spell_database:
            spell_data = self.character_data.spell_database[spell_name]

            # Create popup window
            popup = tk.Toplevel(self.root)
            popup.title(f"Spell: {spell_name}")
            popup.geometry("400x300")

            # Spell details
            details_frame = ttk.Frame(popup)
            details_frame.pack(fill="both", expand=True, padx=10, pady=10)

            ttk.Label(details_frame, text=spell_name, font=("Helvetica", 14, "bold")).pack()
            ttk.Label(details_frame, text=f"Level: {spell_data['level']} | School: {spell_data['school']}",
                      font=("Helvetica", 10)).pack(pady=5)
            ttk.Label(details_frame, text=f"Casting Time: {spell_data['casting_time']}",
                      font=("Helvetica", 10)).pack()
            ttk.Label(details_frame, text=f"Range: {spell_data['range']}",
                      font=("Helvetica", 10)).pack()
            ttk.Label(details_frame, text=f"Duration: {spell_data['duration']}",
                      font=("Helvetica", 10)).pack()

            ttk.Separator(details_frame, orient="horizontal").pack(fill="x", pady=10)

            # Description with text widget for scrolling
            ttk.Label(details_frame, text="Description:", font=("Helvetica", 10, "bold")).pack(anchor="w")

            desc_text = tk.Text(details_frame, height=8, width=45, wrap=tk.WORD)
            desc_text.pack(fill="both", expand=True)
            desc_text.insert(tk.END, spell_data['description'])
            desc_text.config(state=tk.DISABLED)

            ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

    def create_final_button(self):
        """Create the final submit button"""
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=10)
        create_button = ttk.Button(self.root, text="Create Character Sheet (PDF)",
                                   command=self.submit_character)
        create_button.pack(pady=15)

    def update_attributes_wrapper(self, attr_name, delta):
        """Wrapper for updating attributes"""
        self.character_data.update_attributes(attr_name, delta)
        self.character_data.update_remaining_skill_slots(self.remaining_display)

    def reset_skill_trainings_wrapper(self):
        """Wrapper for resetting skill trainings"""
        self.character_data.reset_skill_trainings()
        self.character_data.update_remaining_skill_slots(self.remaining_display)

    def calculate_skills_wrapper(self):
        """Wrapper for calculating skills"""
        self.character_data.calculate_skills()
        self.character_data.update_remaining_skill_slots(self.remaining_display)

    def populate_character_dropdown(self):
        """Update the character dropdown with available characters"""
        characters = self.file_manager.get_available_characters()
        character_names = [name for name, _ in characters]
        self.character_dropdown['values'] = character_names
        return dict(characters)

    def load_selected_character(self):
        """Load the selected character from dropdown"""
        selected_name = self.character_data.character_var.get()
        if not selected_name:
            return

        character_map = self.populate_character_dropdown()
        if selected_name not in character_map:
            messagebox.showerror("Error", "Character not found!")
            return

        json_file = character_map[selected_name]
        data = self.file_manager.load_character_data(json_file)

        if not data:
            messagebox.showerror("Error", "Failed to load character data!")
            return

        try:
            self.character_data.load_character_data(data)
            self.character_data.update_remaining_skill_slots(self.remaining_display)
            self.update_spell_section()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load character: {e}")

    def refresh_character_list(self):
        """Refresh the character dropdown list"""
        self.populate_character_dropdown()
        self.character_data.character_var.set("")

    def submit_character(self):
        """Submit character and create PDF"""
        try:
            data = self.character_data.get_character_data()
            self.pdf_generator.export_to_pdf(data, self.character_data)
            self.file_manager.save_character_data(data)
            messagebox.showinfo("Character Created",
                                f"Character PDF saved as {data.get('Name', 'Character')}.pdf")
        except ValueError:
            messagebox.showerror("Input Error", "Make sure all fields are filled out correctly.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
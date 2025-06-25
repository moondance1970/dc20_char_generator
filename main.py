import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

root = tk.Tk()
root.title("DC20 Character Creator")

# ======================= Character Info ============================
name_var = tk.StringVar()
ancestry_var = tk.StringVar()
background_var = tk.StringVar()
class_var = tk.StringVar()
level_var = tk.StringVar(value="1")
inventory_var = tk.StringVar()

# Attributes
ATTRIBUTE_BASE = -2
ATTRIBUTE_POOL = 12
attributes = {
    "Might": tk.IntVar(value=ATTRIBUTE_BASE),
    "Agility": tk.IntVar(value=ATTRIBUTE_BASE),
    "Charisma": tk.IntVar(value=ATTRIBUTE_BASE),
    "Intelligence": tk.IntVar(value=ATTRIBUTE_BASE)
}
points_remaining = tk.IntVar(value=ATTRIBUTE_POOL)
skill_slots_var = tk.StringVar(value="0")

# Skill setup
skill_names = [
    ("Acrobatics", "Agility"),
    ("Stealth", "Agility"),
    ("Trickery", "Agility"),
    ("Athletics", "Might"),
    ("Intimidation", "Might"),
    ("Animal", "Charisma"),
    ("Influence", "Charisma"),
    ("Insight", "Charisma"),
    ("Investigation", "Intelligence"),
    ("Medicine", "Intelligence"),
    ("Survival", "Intelligence")
]

training_bonus = {"None": 0, "Trained": 1, "Expert": 2}
skill_vars = {name: tk.StringVar(value="0") for name, _ in skill_names}
skill_trainings = {name: tk.StringVar(value="None") for name, _ in skill_names}
remaining_skill_slots_var = tk.StringVar(value="0")

inventory_presets = {
    "Fighter": "Longsword, Shield, Chain Mail, Backpack",
    "Rogue": "Dagger, Thieves’ Tools, Leather Armor, Cloak",
    "Wizard": "Spellbook, Wand, Robes, Arcane Focus",
    "Cleric": "Mace, Holy Symbol, Chain Shirt, Healing Kit",
    "Hunter": "Bow, Hunting Knife, Hide Armor, Traps",
    "Bard": "Lute, Leather Armor, Charm Kit, Entertainer’s Pack",
}


# ======================= Functions ============================
def update_attributes(attr_name, delta):
    current = attributes[attr_name].get()
    total_spent = sum(val.get() - ATTRIBUTE_BASE for val in attributes.values())
    if 0 <= (total_spent + delta) <= ATTRIBUTE_POOL:
        attributes[attr_name].set(current + delta)
        points_remaining.set(ATTRIBUTE_POOL - (total_spent + delta))
        update_skill_slots()
        update_remaining_skill_slots()


def update_skill_slots():
    intelligence = attributes["Intelligence"].get()
    skill_slots_var.set(str(intelligence + 2))


def update_remaining_skill_slots():
    max_slots = attributes["Intelligence"].get() + 2
    used_slots = sum(1 for v in skill_trainings.values() if v.get() == "Trained") + sum(
        2 for v in skill_trainings.values() if v.get() == "Expert")
    remaining = max_slots - used_slots
    remaining_skill_slots_var.set(str(max(0, remaining)))
    if remaining < 0:
        remaining_display.configure(foreground="red")
    else:
        remaining_display.configure(foreground="blue")


def calculate_skills():
    scores = {k: v.get() for k, v in attributes.items()}
    for name, attr in skill_names:
        base = scores[attr]
        bonus = training_bonus[skill_trainings[name].get()]
        skill_vars[name].set(str(base + bonus))


def calculate_armor_rating(cls, inventory_text):
    armor_values = {
        "robes": 10, "leather armor": 13, "hide armor": 14,
        "chain shirt": 15, "chain mail": 16, "plate armor": 18, "shield": 2
    }
    inventory = inventory_text.lower()
    base_armor = 0
    has_shield = "shield" in inventory
    for name, value in armor_values.items():
        if name in inventory and name != "shield":
            base_armor = max(base_armor, value)
    if base_armor == 0:
        class_defaults = {
            "Fighter": 16, "Cleric": 15, "Hunter": 14,
            "Rogue": 14, "Bard": 13, "Wizard": 10
        }
        base_armor = class_defaults.get(cls, 12)
    if has_shield:
        base_armor += armor_values["shield"]
    return base_armor


def calculate_combat_stats(cls, cm, might, agi, prime):
    melee_hit = cm + might
    ranged_hit = cm + agi
    spell_check = cm + prime
    armor_rating = calculate_armor_rating(cls, inventory_var.get())
    return melee_hit, ranged_hit, spell_check, armor_rating


def export_to_pdf(data):
    from reportlab.lib import colors
    file_name = data.get("Name", "Character")+".pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Draw decorative border
    margin = 36
    c.setStrokeColor(colors.black)
    c.setLineWidth(3)

    # Header blocks layout
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.darkblue)
    c.drawString(margin + 10, height - 40, "Character Name:")
    c.setFillColor(colors.black)
    c.drawString(margin + 125, height - 40, data.get("Name", ""))

    c.setFillColor(colors.darkblue)
    c.drawString(width / 2, height - 40, "Class & Subclass:")
    c.setFillColor(colors.black)
    c.drawString(width / 2 + 105, height - 40, data.get("Class", ""))

    c.setFillColor(colors.darkblue)
    c.drawString(margin + 10, height - 70, "Ancestry & Background:")
    c.setFillColor(colors.black)
    c.drawString(margin + 155, height - 70, f"{data.get('Ancestry', '')} / {data.get('Background', '')}")

    c.setFillColor(colors.darkblue)
    c.drawString(width - 150, height - 70, "Level:")
    c.setFillColor(colors.black)
    c.drawString(width - 85, height - 70, str(data.get("Level", 1)))

    width, height = letter

    # Draw decorative border
    margin = 36
    c.setStrokeColor(colors.black)
    c.setLineWidth(3)

    # Add HP, Stamina, Mana section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 120, "Resources")
    c.setFont("Helvetica", 10)
    c.drawString(55, height - 136, f"Stamina: {data.get('Grit Points', '')}")
    c.drawString(165, height - 136, f"Mana: 0")  # Placeholder
    hp = 10 + (int(data.get('Level', 1)) * int(data.get('Might', 0)))
    c.drawString(275, height - 136, f"HP: {hp}")  # Placeholder
    #
    # # Armor Diagram Boxes (placeholders)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(width - 200, height - 120, "Defense Zones")
    c.setFont("Helvetica", 10)
    armor_y = height - 140
    for part in ["PDR", "EDR", "MDR"]:
        c.drawString(width - 195, armor_y + 4, part)
        armor_y -= 20
    y = height - 200
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Attributes")
    y -= 15
    c.setFont("Helvetica", 10)
    for key in ["Might", "Agility", "Charisma", "Intelligence"]:
        box_x = 60
        c.drawString(box_x, y, f"{key[:3]}: {data[key]}")
        y -= 20

    # # Reset y for Skills block to right of attributes
    y = height - 200
    skill_x = 140
    c.setFont("Helvetica-Bold", 12)
    c.drawString(skill_x, y, "Skills")
    y -= 15
    c.setFont("Helvetica", 10)
    skill_entries = data["Skills"].split(', ')
    grouped = {"Might": [], "Agility": [], "Charisma": [], "Intelligence": []}
    for entry in skill_entries:
        for stat in grouped:
            if any(entry.startswith(s) for s, a in skill_names if a == stat):
                grouped[stat].append(entry)
                break

    col_offset = 0
    for stat, skills in grouped.items():
        col_x = skill_x + col_offset
        col_y = y
        c.setFont("Helvetica-Bold", 10)
        c.drawString(col_x, col_y, stat)
        c.setFont("Helvetica", 10)
        col_y -= 12
        for s in skills:
            c.drawString(col_x, col_y, s)
            col_y -= 12
        col_offset += 110

    # # Reset y for Combat block
    y = col_y - 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Combat Stats")
    y -= 15
    c.setFont("Helvetica", 10)
    for key in ["Combat Mastery", "Prime", "Save DC", "Grit Points", "Initiative", "To Hit (Melee)", "To Hit (Ranged)",
                "Spell Check", "Armor Rating"]:
        c.drawString(60, y, f"{key}: {data[key]}")
        y -= 12

    # # Inventory section
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Inventory")
    y -= 15
    c.setFont("Helvetica", 10)
    inv_lines = data["Inventory"].split(', ')
    for item in inv_lines:
        c.drawString(60, y, f"- {item}")
        y -= 12

    # Attack Slots Section
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Attacks")
    y -= 15
    c.setFont("Helvetica", 10)
    attack_headers = ["Name", "Damage", "Type"]
    col_widths = [100, 100, 100]
    col_start = 60
    for i, header in enumerate(attack_headers):
        c.drawString(col_start + sum(col_widths[:i]), y, header)

    y -= 12
    for _ in range(3):
        y -= 20

    # Draw line numbers for reference
    c.setFont("Helvetica", 6)
    for i in range(0, int(height), 10):
        c.drawString(5, i, str(i))

    c.save()


def reset_skill_trainings():
    for skill in skill_trainings:
        skill_trainings[skill].set("None")
    calculate_skills()
    update_remaining_skill_slots()


def submit_character():
    try:
        might = attributes["Might"].get()
        agility = attributes["Agility"].get()
        charisma = attributes["Charisma"].get()
        intelligence = attributes["Intelligence"].get()
        level = int(level_var.get())
        prime = max(might, agility, charisma, intelligence)
        combat_mastery = level // 2
        save_dc = 10 + combat_mastery + prime
        grit = charisma + 2
        initiative = combat_mastery + agility

        melee_hit, ranged_hit, spell_check, armor_rating = calculate_combat_stats(
            class_var.get(), combat_mastery, might, agility, prime
        )

        calculate_skills()

        data = {
            "Name": name_var.get(),
            "Ancestry": ancestry_var.get(),
            "Background": background_var.get(),
            "Class": class_var.get(),
            "Level": level,
            "Might": might,
            "Agility": agility,
            "Charisma": charisma,
            "Intelligence": intelligence,
            "Prime": prime,
            "Combat Mastery": combat_mastery,
            "Save DC": save_dc,
            "Grit Points": grit,
            "Initiative": initiative,
            "To Hit (Melee)": melee_hit,
            "To Hit (Ranged)": ranged_hit,
            "Spell Check": spell_check,
            "Armor Rating": armor_rating,
            "Skill Slots (INT + 2)": intelligence + 2,
            "Inventory": inventory_var.get() or inventory_presets.get(class_var.get(), ""),
            "Skills": ", ".join(f"{k}: {skill_vars[k].get()} ({skill_trainings[k].get()})" for k in skill_vars)
        }
        file_name = data.get("Name", "Character.pdf")
        messagebox.showinfo("Character Created", "Character PDF saved as " + file_name )
        export_to_pdf(data)

    except ValueError:
        messagebox.showerror("Input Error", "Make sure all fields are filled out correctly.")


# ======================= UI ============================
ttk.Label(root, text="DC20 Character Creator", font=("Helvetica", 16)).pack(pady=10)

info_frame = ttk.Frame(root)
info_frame.pack()

ttk.Label(info_frame, text="Name").pack()
ttk.Entry(info_frame, textvariable=name_var).pack()

ttk.Label(info_frame, text="Ancestry").pack()
ttk.Combobox(info_frame, textvariable=ancestry_var, values=[
    "Human", "Elf", "Dwarf", "Orc", "Gnome", "Halfling"
], state="readonly").pack()

ttk.Label(info_frame, text="Background").pack()
background_combobox = ttk.Combobox(info_frame, textvariable=background_var, values=[
    "Soldier", "Scholar", "Outlander", "Criminal", "Acolyte", "Entertainer"
])
background_combobox.pack()
background_combobox.configure(state="normal")

ttk.Label(info_frame, text="Class").pack()
ttk.Combobox(info_frame, textvariable=class_var, values=list(inventory_presets.keys()), state="readonly").pack()

inventory_entry = ttk.Entry(info_frame, textvariable=inventory_var, width=50)
ttk.Label(info_frame, text="Inventory").pack()
inventory_entry.pack()


def update_inventory(event):
    cls = class_var.get()
    inventory_var.set(inventory_presets.get(cls, ""))


def on_class_change(event):
    cls = class_var.get()
    inventory_var.set(inventory_presets.get(cls, ""))

class_dropdown = ttk.Combobox(info_frame, textvariable=class_var, values=list(inventory_presets.keys()), state="readonly")
class_dropdown.pack()
class_dropdown.bind("<<ComboboxSelected>>", on_class_change)


ttk.Label(info_frame, text="Level").pack()
ttk.Entry(info_frame, textvariable=level_var).pack()

# Attributes
attr_frame = ttk.Frame(root)
attr_frame.pack(pady=10)
ttk.Label(attr_frame, text="Assign Attribute Points (Start at -2)").pack()
ttk.Label(attr_frame, textvariable=points_remaining, foreground="blue").pack()
ttk.Label(attr_frame, text="Points Remaining").pack()

for name in attributes:
    f = ttk.Frame(attr_frame)
    f.pack()
    ttk.Label(f, text=name, width=10).pack(side="left")
    ttk.Button(f, text="-", command=lambda n=name: update_attributes(n, -1)).pack(side="left")
    ttk.Label(f, textvariable=attributes[name], width=3).pack(side="left")
    ttk.Button(f, text="+", command=lambda n=name: update_attributes(n, 1)).pack(side="left")

# Skill section
ttk.Button(root, text="Reset All Skill Trainings", command=reset_skill_trainings).pack(pady=(5, 5))
skills_by_attribute = {
    "Might": ["Athletics", "Intimidation"],
    "Agility": ["Acrobatics", "Stealth", "Trickery"],
    "Charisma": ["Animal", "Influence", "Insight"],
    "Intelligence": ["Investigation", "Medicine", "Survival"]
}

ttk.Label(root, text="Skills (auto-fill from attributes + training)").pack(pady=(10, 0))
skills_frame = ttk.Frame(root)
skills_frame.pack()
remaining_label = ttk.Label(root, text="Remaining Skill Slots")
remaining_label.pack()
remaining_display = ttk.Label(root, textvariable=remaining_skill_slots_var, foreground="blue")
remaining_display.pack()

for col_idx, (attr, skills) in enumerate(skills_by_attribute.items()):
    col_frame = ttk.Frame(skills_frame)
    col_frame.grid(row=0, column=col_idx, padx=10, sticky="n")
    ttk.Label(col_frame, text=attr, font=("Helvetica", 10, "bold")).pack()
    for skill in skills:
        ttk.Label(col_frame, text=skill).pack()
        entry = ttk.Entry(col_frame, textvariable=skill_vars[skill], width=5, state="readonly")
        entry.pack()


        def update_entry_bg(var=skill_trainings[skill], widget=entry):
            level = var.get()
            if level == "Expert":
                widget.configure(background="#d1e7dd")
            elif level == "Trained":
                widget.configure(background="#fff3cd")
            else:
                widget.configure(background="white")


        var = skill_trainings[skill]
        var.trace_add("write", lambda *args, v=var, w=entry: update_entry_bg(v, w))
        update_entry_bg()
        combo = ttk.Combobox(col_frame, textvariable=skill_trainings[skill], values=list(training_bonus.keys()),
                             width=7, state="readonly")
        combo.pack()
        combo.bind("<<ComboboxSelected>>", lambda e: (calculate_skills(), update_remaining_skill_slots()))

# Final Button
ttk.Button(root, text="Create Character Sheet (PDF)", command=submit_character).pack(pady=10)

calculate_skills()
update_remaining_skill_slots()
root.mainloop()

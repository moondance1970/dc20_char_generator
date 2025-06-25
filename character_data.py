import tkinter as tk

class CharacterData:
    def __init__(self):
        # Character Info
        self.name_var = tk.StringVar()
        self.player_name_var = tk.StringVar()
        self.ancestry_var = tk.StringVar()
        self.background_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.subclass_var = tk.StringVar()
        self.level_var = tk.StringVar(value="1")
        self.inventory_var = tk.StringVar()
        
        # Attributes
        self.ATTRIBUTE_BASE = -2
        self.ATTRIBUTE_POOL = 12
        self.attributes = {
            "Might": tk.IntVar(value=self.ATTRIBUTE_BASE),
            "Agility": tk.IntVar(value=self.ATTRIBUTE_BASE),
            "Charisma": tk.IntVar(value=self.ATTRIBUTE_BASE),
            "Intelligence": tk.IntVar(value=self.ATTRIBUTE_BASE)
        }
        self.points_remaining = tk.IntVar(value=self.ATTRIBUTE_POOL)
        self.skill_slots_var = tk.StringVar(value="0")
        
        # Skills
        self.skill_names = [
            ("Athletics", "Might"),
            ("Intimidation", "Might"),
            ("Acrobatics", "Agility"),
            ("Trickery", "Agility"),
            ("Stealth", "Agility"),
            ("Animal", "Charisma"),
            ("Influence", "Charisma"),
            ("Insight", "Charisma"),
            ("Investigation", "Intelligence"),
            ("Medicine", "Intelligence"),
            ("Survival", "Intelligence")
        ]
        
        self.training_bonus = {"None": 0, "Trained": 1, "Expert": 2}
        self.skill_vars = {name: tk.StringVar(value="0") for name, _ in self.skill_names}
        self.skill_trainings = {name: tk.StringVar(value="None") for name, _ in self.skill_names}
        self.remaining_skill_slots_var = tk.StringVar(value="0")
        
        # Inventory presets
        self.inventory_presets = {
            "Fighter": "Longsword, Shield, Chain Mail, Backpack",
            "Rogue": "Dagger, Thieves' Tools, Leather Armor, Cloak",
            "Wizard": "Spellbook, Wand, Robes, Arcane Focus",
            "Cleric": "Mace, Holy Symbol, Chain Shirt, Healing Kit",
            "Hunter": "Bow, Hunting Knife, Hide Armor, Traps",
            "Bard": "Lute, Leather Armor, Charm Kit, Entertainer's Pack",
        }
        
        # Character loading
        self.character_var = tk.StringVar()
    
    def update_attributes(self, attr_name, delta):
        current = self.attributes[attr_name].get()
        total_spent = sum(val.get() - self.ATTRIBUTE_BASE for val in self.attributes.values())
        if 0 <= (total_spent + delta) <= self.ATTRIBUTE_POOL:
            self.attributes[attr_name].set(current + delta)
            self.points_remaining.set(self.ATTRIBUTE_POOL - (total_spent + delta))
            self.update_skill_slots()
    
    def update_skill_slots(self):
        intelligence = self.attributes["Intelligence"].get()
        self.skill_slots_var.set(str(intelligence + 2))
    
    def update_remaining_skill_slots(self, remaining_display):
        max_slots = self.attributes["Intelligence"].get() + 2
        used_slots = sum(1 for v in self.skill_trainings.values() if v.get() == "Trained") + sum(
            2 for v in self.skill_trainings.values() if v.get() == "Expert")
        remaining = max_slots - used_slots
        self.remaining_skill_slots_var.set(str(max(0, remaining)))
        if remaining < 0:
            remaining_display.configure(foreground="red")
        else:
            remaining_display.configure(foreground="blue")
    
    def calculate_skills(self):
        scores = {k: v.get() for k, v in self.attributes.items()}
        for name, attr in self.skill_names:
            base = scores[attr]
            bonus = self.training_bonus[self.skill_trainings[name].get()]
            self.skill_vars[name].set(str(base + bonus))
    
    def calculate_armor_rating(self, cls, inventory_text):
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
    
    def calculate_combat_stats(self, cls, cm, might, agi, prime):
        melee_hit = cm + might
        ranged_hit = cm + agi
        spell_check = cm + prime
        armor_rating = self.calculate_armor_rating(cls, self.inventory_var.get())
        return melee_hit, ranged_hit, spell_check, armor_rating
    
    def parse_weapons_from_inventory(self, inventory_text, class_name, might, agility, combat_mastery):
        """Parse weapons from inventory and return attack data with DC20 mechanics"""
        weapons = []
        inventory_lower = inventory_text.lower()
        
        # In DC20, damage is typically based on stats, not weapon type
        # Base damage often uses Might for melee, Agility for ranged
        melee_damage = might
        ranged_damage = agility
        
        # Common weapons with their attack types and damage calculations
        weapon_list = [
            ("longsword", "Longsword", f"{melee_damage}", "Slashing", "melee"),
            ("dagger", "Dagger", f"{melee_damage}", "Piercing", "melee"),
            ("bow", "Bow", f"{ranged_damage}", "Piercing", "ranged"),
            ("crossbow", "Crossbow", f"{ranged_damage}", "Piercing", "ranged"),
            ("mace", "Mace", f"{melee_damage}", "Bludgeoning", "melee"),
            ("wand", "Wand", "Special", "Force", "spell"),
            ("staff", "Staff", f"{melee_damage}", "Bludgeoning", "melee"),
            ("hunting knife", "Hunting Knife", f"{melee_damage}", "Slashing", "melee"),
            ("lute", "Lute", f"{melee_damage}", "Bludgeoning", "melee"),
            ("sword", "Sword", f"{melee_damage}", "Slashing", "melee"),
            ("axe", "Axe", f"{melee_damage}", "Slashing", "melee"),
            ("spear", "Spear", f"{melee_damage}", "Piercing", "melee"),
            ("club", "Club", f"{melee_damage}", "Bludgeoning", "melee"),
            ("hammer", "Hammer", f"{melee_damage}", "Bludgeoning", "melee")
        ]
        
        # Find weapons in inventory
        for weapon_key, name, damage, weapon_type, attack_type in weapon_list:
            if weapon_key in inventory_lower:
                weapons.append((name, damage, weapon_type))
        
        # Add class-specific abilities if no weapons found or as additional options
        class_abilities = {
            "Fighter": ("Combat Strike", f"{melee_damage + combat_mastery}", "Physical"),
            "Rogue": ("Precision Strike", f"{agility + combat_mastery}", "Piercing"),
            "Wizard": ("Cantrip", "Special", "Magical"),
            "Cleric": ("Divine Strike", f"{might + combat_mastery}", "Radiant"),
            "Hunter": ("Aimed Shot", f"{ranged_damage + combat_mastery}", "Piercing"),
            "Bard": ("Inspiring Strike", f"{melee_damage}", "Physical")
        }
        
        if class_name in class_abilities and len(weapons) < 3:
            weapons.append(class_abilities[class_name])
        
        # Always add unarmed strike
        weapons.append(("Unarmed Strike", f"{melee_damage}", "Bludgeoning"))
        
        return weapons[:4]  # Limit to 4 attacks to fit the table
    
    def reset_skill_trainings(self):
        for skill in self.skill_trainings:
            self.skill_trainings[skill].set("None")
        self.calculate_skills()
    
    def get_character_data(self):
        """Get all character data as a dictionary"""
        might = self.attributes["Might"].get()
        agility = self.attributes["Agility"].get()
        charisma = self.attributes["Charisma"].get()
        intelligence = self.attributes["Intelligence"].get()
        level = int(self.level_var.get())
        prime = max(might, agility, charisma, intelligence)
        combat_mastery = level // 2
        save_dc = 10 + combat_mastery + prime
        grit = charisma + 2
        initiative = combat_mastery + agility

        melee_hit, ranged_hit, spell_check, armor_rating = self.calculate_combat_stats(
            self.class_var.get(), combat_mastery, might, agility, prime
        )

        self.calculate_skills()

        return {
            "Name": self.name_var.get(),
            "Player Name": self.player_name_var.get(),
            "Ancestry": self.ancestry_var.get(),
            "Background": self.background_var.get(),
            "Class": self.class_var.get(),
            "Subclass": self.subclass_var.get(),
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
            "Inventory": self.inventory_var.get() or self.inventory_presets.get(self.class_var.get(), ""),
            "Skills": ", ".join(f"{k}: {self.skill_vars[k].get()} ({self.skill_trainings[k].get()})" for k in self.skill_vars)
        }
    
    def load_character_data(self, data):
        """Load character data from dictionary"""
        self.name_var.set(data.get("Name", ""))
        self.player_name_var.set(data.get("Player Name", ""))
        self.ancestry_var.set(data.get("Ancestry", ""))
        self.background_var.set(data.get("Background", ""))
        self.class_var.set(data.get("Class", ""))
        self.subclass_var.set(data.get("Subclass", ""))
        self.level_var.set(str(data.get("Level", 1)))
        self.inventory_var.set(data.get("Inventory", ""))
        
        # Load attributes
        self.attributes["Might"].set(data.get("Might", self.ATTRIBUTE_BASE))
        self.attributes["Agility"].set(data.get("Agility", self.ATTRIBUTE_BASE))
        self.attributes["Charisma"].set(data.get("Charisma", self.ATTRIBUTE_BASE))
        self.attributes["Intelligence"].set(data.get("Intelligence", self.ATTRIBUTE_BASE))
        
        # Load skills training
        skills_data = data.get("Skills", "")
        if skills_data:
            # Parse skills string and set training levels
            skill_entries = skills_data.split(', ')
            for entry in skill_entries:
                if ':' in entry and '(' in entry:
                    skill_name = entry.split(':')[0]
                    training = entry.split('(')[1].replace(')', '')
                    if skill_name in self.skill_trainings:
                        self.skill_trainings[skill_name].set(training)
        
        # Update calculations
        self.update_skill_slots()
        self.calculate_skills()
        
        # Update points remaining calculation
        total_spent = sum(val.get() - self.ATTRIBUTE_BASE for val in self.attributes.values())
        self.points_remaining.set(self.ATTRIBUTE_POOL - total_spent)
import tkinter as tk
import math


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

        # Spell system
        self.spellcasting_classes = ["Wizard", "Cleric", "Bard"]
        self.selected_spells = []  # List of selected spell names
        self.spell_database = self.init_spell_database()

        # Character loading
        self.character_var = tk.StringVar()

    def init_spell_database(self):
        """Initialize the DC20 spell database"""
        return {
            # Cantrips (0th level)
            "Light": {"level": 0, "school": "Evocation", "casting_time": "1 Action", "range": "Touch",
                      "duration": "1 Hour",
                      "description": "Touch an object no larger than 10 feet. The object sheds bright light in a 20-foot radius and dim light for an additional 20 feet."},
            "Mage Hand": {"level": 0, "school": "Transmutation", "casting_time": "1 Action", "range": "30 feet",
                          "duration": "1 Minute",
                          "description": "Create a spectral floating hand that can manipulate objects up to 10 pounds within range."},
            "Minor Illusion": {"level": 0, "school": "Illusion", "casting_time": "1 Action", "range": "30 feet",
                               "duration": "1 Minute",
                               "description": "Create a sound or image of an object within range for the duration."},
            "Prestidigitation": {"level": 0, "school": "Transmutation", "casting_time": "1 Action", "range": "10 feet",
                                 "duration": "1 Hour",
                                 "description": "Perform a minor magical trick such as lighting a candle, cleaning an object, or creating a small sensory effect."},
            "Sacred Flame": {"level": 0, "school": "Evocation", "casting_time": "1 Action", "range": "60 feet",
                             "duration": "Instantaneous",
                             "description": "Flame-like radiance descends on a creature. Target makes a Dexterity save or takes 1d8 radiant damage."},
            "Guidance": {"level": 0, "school": "Divination", "casting_time": "1 Action", "range": "Touch",
                         "duration": "1 Minute",
                         "description": "Touch a willing creature. Once before the spell ends, the target can roll a d4 and add it to one ability check."},

            # 1st Level Spells
            "Magic Missile": {"level": 1, "school": "Evocation", "casting_time": "1 Action", "range": "120 feet",
                              "duration": "Instantaneous",
                              "description": "Create three glowing darts that automatically hit their targets for 1d4+1 force damage each."},
            "Shield": {"level": 1, "school": "Abjuration", "casting_time": "1 Reaction", "range": "Self",
                       "duration": "1 Round",
                       "description": "Gain +5 AC until the start of your next turn. Can be cast as a reaction to being hit."},
            "Healing Word": {"level": 1, "school": "Evocation", "casting_time": "1 Action", "range": "60 feet",
                             "duration": "Instantaneous",
                             "description": "Heal a creature for 1d4 + spellcasting modifier hit points."},
            "Cure Wounds": {"level": 1, "school": "Evocation", "casting_time": "1 Action", "range": "Touch",
                            "duration": "Instantaneous",
                            "description": "Touch a creature to heal them for 1d8 + spellcasting modifier hit points."},
            "Bless": {"level": 1, "school": "Enchantment", "casting_time": "1 Action", "range": "30 feet",
                      "duration": "1 Minute",
                      "description": "Up to three creatures gain a d4 bonus to attack rolls and saving throws."},
            "Burning Hands": {"level": 1, "school": "Evocation", "casting_time": "1 Action",
                              "range": "Self (15-foot cone)", "duration": "Instantaneous",
                              "description": "Each creature in a 15-foot cone makes a Dexterity save or takes 3d6 fire damage."},
            "Charm Person": {"level": 1, "school": "Enchantment", "casting_time": "1 Action", "range": "30 feet",
                             "duration": "1 Hour",
                             "description": "Target humanoid makes a Wisdom save or is charmed by you for the duration."},
            "Sleep": {"level": 1, "school": "Enchantment", "casting_time": "1 Action", "range": "90 feet",
                      "duration": "1 Minute",
                      "description": "Creatures in a 20-foot radius fall unconscious. Roll 5d8; creatures with hit points equal to or less than the total fall asleep."},

            # 2nd Level Spells
            "Misty Step": {"level": 2, "school": "Conjuration", "casting_time": "1 Action", "range": "Self",
                           "duration": "Instantaneous",
                           "description": "Teleport up to 30 feet to an unoccupied space you can see."},
            "Web": {"level": 2, "school": "Conjuration", "casting_time": "1 Action", "range": "60 feet",
                    "duration": "1 Hour",
                    "description": "Fill a 20-foot cube with sticky webbing. Creatures are restrained and must make Strength checks to escape."},
            "Hold Person": {"level": 2, "school": "Enchantment", "casting_time": "1 Action", "range": "60 feet",
                            "duration": "1 Minute",
                            "description": "Target humanoid makes a Wisdom save or is paralyzed for the duration."},
            "Spiritual Weapon": {"level": 2, "school": "Evocation", "casting_time": "1 Action", "range": "60 feet",
                                 "duration": "1 Minute",
                                 "description": "Create a floating spectral weapon that attacks as a bonus action for 1d8 + spellcasting modifier damage."},
            "Suggestion": {"level": 2, "school": "Enchantment", "casting_time": "1 Action", "range": "30 feet",
                           "duration": "8 Hours",
                           "description": "Suggest a course of activity to a creature. The target makes a Wisdom save or follows the suggestion."},

            # 3rd Level Spells
            "Fireball": {"level": 3, "school": "Evocation", "casting_time": "1 Action", "range": "150 feet",
                         "duration": "Instantaneous",
                         "description": "Explode a 20-foot radius sphere dealing 8d6 fire damage. Dexterity save for half damage."},
            "Lightning Bolt": {"level": 3, "school": "Evocation", "casting_time": "1 Action",
                               "range": "Self (100-foot line)", "duration": "Instantaneous",
                               "description": "A 100-foot long, 5-foot wide line of lightning. Dexterity save or take 8d6 lightning damage."},
            "Counterspell": {"level": 3, "school": "Abjuration", "casting_time": "1 Reaction", "range": "60 feet",
                             "duration": "Instantaneous",
                             "description": "Attempt to interrupt a creature casting a spell within range."},
            "Healing Spirit": {"level": 3, "school": "Conjuration", "casting_time": "1 Action", "range": "60 feet",
                               "duration": "1 Minute",
                               "description": "Create a spirit that heals creatures for 1d6 hit points when they start their turn in its space."}
        }

    def get_spells_for_class(self, class_name, level):
        """Get available spells for a class at a given level"""
        if class_name not in self.spellcasting_classes:
            return []

        max_spell_level = min(3, (level + 1) // 2)  # DC20 spell progression
        available_spells = []

        for spell_name, spell_data in self.spell_database.items():
            if spell_data["level"] <= max_spell_level:
                # Class-specific spell filtering
                if class_name == "Wizard" and spell_data["school"] in ["Evocation", "Transmutation", "Abjuration",
                                                                       "Conjuration", "Illusion"]:
                    available_spells.append(spell_name)
                elif class_name == "Cleric" and spell_data["school"] in ["Evocation", "Abjuration", "Divination",
                                                                         "Enchantment"]:
                    available_spells.append(spell_name)
                elif class_name == "Bard" and spell_data["school"] in ["Enchantment", "Illusion", "Divination",
                                                                       "Transmutation"]:
                    available_spells.append(spell_name)

        return sorted(available_spells)

    def get_spell_slots(self, class_name, level):
        """Calculate spell slots for a class at given level"""
        if class_name not in self.spellcasting_classes:
            return {}

        # DC20 spell slot progression (simplified)
        if level == 1:
            return {0: 3, 1: 2}  # 3 cantrips, 2 first level
        elif level == 2:
            return {0: 3, 1: 3}
        elif level == 3:
            return {0: 4, 1: 4, 2: 2}
        elif level == 4:
            return {0: 4, 1: 4, 2: 3}
        elif level == 5:
            return {0: 4, 1: 4, 2: 3, 3: 2}
        else:
            return {0: 4, 1: 4, 2: 3, 3: 3}

    def is_spellcaster(self):
        """Check if current class is a spellcaster"""
        return self.class_var.get() in self.spellcasting_classes

    def add_spell(self, spell_name):
        """Add a spell to the character's spell list"""
        if spell_name not in self.selected_spells:
            self.selected_spells.append(spell_name)

    def remove_spell(self, spell_name):
        """Remove a spell from the character's spell list"""
        if spell_name in self.selected_spells:
            self.selected_spells.remove(spell_name)

    def get_selected_spells_by_level(self):
        """Get selected spells organized by level"""
        spells_by_level = {}
        for spell_name in self.selected_spells:
            if spell_name in self.spell_database:
                level = self.spell_database[spell_name]["level"]
                if level not in spells_by_level:
                    spells_by_level[level] = []
                spells_by_level[level].append(spell_name)
        return spells_by_level

    # ... (rest of the existing methods remain the same)

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

        # In DC20, damage typically has a base weapon damage + ability modifier
        # Common weapons with their base damage and calculations
        weapon_list = [
            ("longsword", "Longsword", f"{2 + might}", "Slashing", "melee"),
            ("dagger", "Dagger", f"{1 + might}", "Piercing", "melee"),
            ("bow", "Bow", f"{2 + agility}", "Piercing", "ranged"),
            ("crossbow", "Crossbow", f"{2 + agility}", "Piercing", "ranged"),
            ("mace", "Mace", f"{2 + might}", "Bludgeoning", "melee"),
            ("wand", "Wand", "Special", "Force", "spell"),
            ("staff", "Staff", f"{1 + might}", "Bludgeoning", "melee"),
            ("hunting knife", "Hunting Knife", f"{1 + might}", "Slashing", "melee"),
            ("lute", "Lute", f"{1 + might}", "Bludgeoning", "melee"),
            ("sword", "Sword", f"{2 + might}", "Slashing", "melee"),
            ("axe", "Axe", f"{2 + might}", "Slashing", "melee"),
            ("spear", "Spear", f"{2 + might}", "Piercing", "melee"),
            ("club", "Club", f"{1 + might}", "Bludgeoning", "melee"),
            ("hammer", "Hammer", f"{2 + might}", "Bludgeoning", "melee")
        ]

        # Find weapons in inventory
        for weapon_key, name, damage, weapon_type, attack_type in weapon_list:
            if weapon_key in inventory_lower:
                weapons.append((name, damage, weapon_type))

        # Add class-specific abilities if no weapons found or as additional options
        class_abilities = {
            "Fighter": ("Combat Strike", f"{2 + might + combat_mastery}", "Physical"),
            "Rogue": ("Precision Strike", f"{1 + agility + combat_mastery}", "Piercing"),
            "Wizard": ("Cantrip", "1d4", "Magical"),
            "Cleric": ("Divine Strike", f"{1 + might + combat_mastery}", "Radiant"),
            "Hunter": ("Aimed Shot", f"{2 + agility + combat_mastery}", "Piercing"),
            "Bard": ("Inspiring Strike", f"{1 + might}", "Physical")
        }

        if class_name in class_abilities and len(weapons) < 3:
            weapons.append(class_abilities[class_name])

        # Always add unarmed strike with base damage
        weapons.append(("Unarmed Strike", f"{1 + might}", "Bludgeoning"))

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

        # Combat Mastery should be level / 2 rounded UP
        combat_mastery = math.ceil(level / 2)

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
            "Skills": ", ".join(
                f"{k}: {self.skill_vars[k].get()} ({self.skill_trainings[k].get()})" for k in self.skill_vars),
            "Selected Spells": self.selected_spells,
            "Spell Slots": self.get_spell_slots(self.class_var.get(), level) if self.is_spellcaster() else {}
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

        # Load spells
        self.selected_spells = data.get("Selected Spells", [])

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
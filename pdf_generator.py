from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class PDFGenerator:
    def __init__(self):
        pass

    def draw_hexagonal_border(self, c, x, y, width, height):
        """Draw hexagonal/angular border like DC20 style"""
        corner_cut = 8
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)

        # Draw angular border with cut corners
        path = [
            (x + corner_cut, y),
            (x + width - corner_cut, y),
            (x + width, y + corner_cut),
            (x + width, y + height - corner_cut),
            (x + width - corner_cut, y + height),
            (x + corner_cut, y + height),
            (x, y + height - corner_cut),
            (x, y + corner_cut),
            (x + corner_cut, y)
        ]

        for i in range(len(path) - 1):
            c.line(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1])

    def draw_attribute_hexagon(self, c, x, y, attr_name, attr_value, width=100, height=120):
        """Draw DC20-style attribute section with hexagonal styling"""
        # Main hexagonal border
        self.draw_hexagonal_border(c, x, y, width, height)

        # Fill background
        c.setFillColor(colors.white)
        c.rect(x + 2, y + 2, width - 4, height - 4, fill=1, stroke=0)

        # Attribute abbreviation mapping
        abbrev_map = {"Might": "MIG", "Agility": "AGI", "Charisma": "CHA", "Intelligence": "INT"}
        abbrev = abbrev_map.get(attr_name, attr_name[:3])

        # Top section with abbreviation
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        text_width = c.stringWidth(abbrev, "Helvetica-Bold", 12)
        c.drawString(x + width / 2 - text_width / 2, y + height - 20, abbrev)

        # Large attribute value in center
        c.setFont("Helvetica-Bold", 36)
        value_text = str(attr_value)
        value_width = c.stringWidth(value_text, "Helvetica-Bold", 36)
        c.drawString(x + width / 2 - value_width / 2, y + height / 2 - 8, value_text)

        # SAVE label and box at bottom
        c.setFont("Helvetica-Bold", 10)
        save_text = "SAVE"
        save_width = c.stringWidth(save_text, "Helvetica-Bold", 10)
        c.drawString(x + width / 2 - save_width / 2, y + 25, save_text)

        # Save modifier box
        save_box_width = 25
        save_box_height = 15
        save_x = x + width / 2 - save_box_width / 2
        save_y = y + 5
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.setFillColor(colors.white)
        c.rect(save_x, save_y, save_box_width, save_box_height, fill=1, stroke=1)

    def draw_expertise_boxes(self, c, x, y, training_level, box_count=5):
        """Draw expertise level boxes"""
        box_size = 8
        box_spacing = 2

        # Determine filled boxes
        filled_boxes = 0
        if training_level == "Trained":
            filled_boxes = 1
        elif training_level == "Expert":
            filled_boxes = 2
        elif training_level == "Master":
            filled_boxes = 3
        elif training_level == "Grandmaster":
            filled_boxes = 5

        for i in range(box_count):
            box_x = x + (i * (box_size + box_spacing))

            c.setStrokeColor(colors.black)
            c.setLineWidth(1)

            if i < filled_boxes:
                c.setFillColor(colors.black)
            else:
                c.setFillColor(colors.white)

            c.rect(box_x, y, box_size, box_size, fill=1, stroke=1)

    def draw_skill_column(self, c, x, y, attr_name, skills_data, column_width=110):
        """Draw a column of skills for an attribute"""
        current_y = y

        # Attribute header
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.black)
        header_text = attr_name.upper()
        c.drawString(x, current_y, header_text)
        current_y -= 20

        # Skills
        for skill_name, skill_value, training in skills_data:
            # Skill name
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.black)
            c.drawString(x, current_y, skill_name.upper())

            # Expertise boxes
            self.draw_expertise_boxes(c, x, current_y - 15, training)

            current_y -= 30

        # Add some empty slots with labels if needed
        skill_names_by_attr = {
            "MIGHT": ["ATHLETICS", "INTIMIDATION"],
            "AGILITY": ["ACROBATICS", "STEALTH", "TRICKERY"],
            "CHARISMA": ["ANIMAL", "INFLUENCE", "INSIGHT"],
            "INTELLIGENCE": ["INVESTIGATION", "MEDICINE", "SURVIVAL"]
        }

        # Show all possible skills for this attribute, even if not trained
        all_skills = skill_names_by_attr.get(attr_name.upper(), [])
        trained_skills = [skill[0] for skill in skills_data]

        for skill_name in all_skills:
            if skill_name not in [s.upper() for s in trained_skills]:
                c.setFont("Helvetica", 9)
                c.setFillColor(colors.black)
                c.drawString(x, current_y, skill_name)
                # Draw empty expertise boxes
                self.draw_expertise_boxes(c, x, current_y - 15, "None")
                current_y -= 30

    def draw_prime_hexagon(self, c, x, y):
        """Draw the large PRIME attribute hexagon"""
        width = 80
        height = 80

        # Large hexagonal border
        self.draw_hexagonal_border(c, x, y, width, height)
        c.setFillColor(colors.white)
        c.rect(x + 2, y + 2, width - 4, height - 4, fill=1, stroke=0)

        # PRIME label
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        prime_text = "PRIME"
        prime_width = c.stringWidth(prime_text, "Helvetica-Bold", 10)
        c.drawString(x + width / 2 - prime_width / 2, y + height - 15, prime_text)

        # Subtitle
        c.setFont("Helvetica", 7)
        subtitle = "= Highest Attribute"
        sub_width = c.stringWidth(subtitle, "Helvetica", 7)
        c.drawString(x + width / 2 - sub_width / 2, y + 8, subtitle)

    def draw_dc20_header(self, c, width, height, data):
        """Draw the DC20-style header with proper layout"""
        header_y = height - 80

        # Main header border
        header_width = width - 100
        header_height = 70
        self.draw_hexagonal_border(c, 50, header_y - 10, header_width, header_height)

        # Character info layout
        c.setFillColor(colors.black)

        # Left side - Player and Character name
        c.setFont("Helvetica", 8)
        c.drawString(60, header_y + 40, "PLAYER NAME")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, header_y + 28, data.get("Player Name", ""))

        c.setFont("Helvetica", 8)
        c.drawString(60, header_y + 15, "CHARACTER NAME")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, header_y + 2, data.get("Name", ""))

        # Center - Class and Ancestry
        center_x = 280
        c.setFont("Helvetica", 8)
        c.drawString(center_x, header_y + 40, "CLASS & SUBCLASS")
        c.setFont("Helvetica-Bold", 10)
        class_text = data.get("Class", "")
        if data.get("Subclass"):
            class_text += f" / {data.get('Subclass')}"
        c.drawString(center_x, header_y + 28, class_text)

        c.setFont("Helvetica", 8)
        c.drawString(center_x, header_y + 15, "ANCESTRY & BACKGROUND")
        c.setFont("Helvetica-Bold", 10)
        ancestry_bg = f"{data.get('Ancestry', '')} / {data.get('Background', '')}"
        c.drawString(center_x, header_y + 2, ancestry_bg)

        # Right side - Level
        level_x = width - 140
        level_size = 50
        self.draw_hexagonal_border(c, level_x, header_y + 10, level_size, level_size)

        c.setFont("Helvetica", 8)
        c.drawString(level_x + 15, header_y + 45, "LEVEL")
        c.setFont("Helvetica-Bold", 20)
        level_text = str(data.get("Level", 1))
        level_width = c.stringWidth(level_text, "Helvetica-Bold", 20)
        c.drawString(level_x + level_size / 2 - level_width / 2, header_y + 25, level_text)

        # Combat Mastery in a box
        cm_x = level_x - 70
        cm_size = 60
        self.draw_hexagonal_border(c, cm_x, header_y + 10, cm_size, 50)
        c.setFillColor(colors.white)
        c.rect(cm_x + 2, header_y + 12, cm_size - 4, 46, fill=1, stroke=0)

        c.setFillColor(colors.black)
        c.setFont("Helvetica", 8)
        # Split into two lines
        combat_width = c.stringWidth("COMBAT", "Helvetica", 8)
        mastery_width = c.stringWidth("MASTERY", "Helvetica", 8)
        c.drawString(cm_x + cm_size / 2 - combat_width / 2, header_y + 48, "COMBAT")
        c.drawString(cm_x + cm_size / 2 - mastery_width / 2, header_y + 40, "MASTERY")

        c.setFont("Helvetica-Bold", 16)
        cm_text = str(data.get("Combat Mastery", 0))
        cm_width = c.stringWidth(cm_text, "Helvetica-Bold", 16)
        c.drawString(cm_x + cm_size / 2 - cm_width / 2, header_y + 20, cm_text)

    def draw_resources_section(self, c, x, y, data):
        """Draw the health and resources section"""
        # Health Points
        hp_width = 120
        hp_height = 60
        self.draw_hexagonal_border(c, x, y, hp_width, hp_height)

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 10, y + hp_height - 15, "HEALTH POINTS")

        hp = 10 + (int(data.get('Level', 1)) * int(data.get('Might', 0)))
        c.setFont("Helvetica-Bold", 24)
        hp_text = str(hp)
        hp_width_text = c.stringWidth(hp_text, "Helvetica-Bold", 24)
        c.drawString(x + hp_width / 2 - hp_width_text / 2, y + 20, hp_text)

        # Resources section
        resources_x = x + 150
        resources_width = 200
        resources_height = 60
        self.draw_hexagonal_border(c, resources_x, y, resources_width, resources_height)

        c.setFont("Helvetica-Bold", 10)
        c.drawString(resources_x + 10, y + resources_height - 15, "RESOURCES")

        # Resource items
        c.setFont("Helvetica", 8)
        resource_y = y + resources_height - 30
        resources = [
            ("STAMINA POINTS", str(data.get("Grit Points", 0))),
            ("MANA POINTS", "0"),
            ("GRIT POINTS", str(data.get("Grit Points", 0)))
        ]

        for label, value in resources:
            c.drawString(resources_x + 10, resource_y, label)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(resources_x + 120, resource_y, value)
            c.setFont("Helvetica", 8)
            resource_y -= 12

    def draw_combat_section(self, c, x, y, data, width=300):
        """Draw the combat statistics section"""
        height = 80
        self.draw_hexagonal_border(c, x, y, width, height)

        # Gray background
        c.setFillColor(colors.lightgrey)
        c.rect(x + 2, y + 2, width - 4, height - 4, fill=1, stroke=0)

        # Combat title
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 10, y + height - 15, "COMBAT")

        # Combat formulas and values
        c.setFont("Helvetica", 9)
        formulas = [
            ("ATTACK / SPELL CHECK = CM + Prime", str(data.get("Spell Check", 0))),
            ("SAVE DC = 10 + CM + Prime", str(data.get("Save DC", 0))),
            ("INITIATIVE = CM + AGI", str(data.get("Initiative", 0)))
        ]

        formula_y = y + height - 35
        for formula, value in formulas:
            c.drawString(x + 10, formula_y, formula)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(x + width - 40, formula_y, value)
            c.setFont("Helvetica", 9)
            formula_y -= 15

    def draw_attacks_table(self, c, x, y, weapons, width=400):
        """Draw the attacks table"""
        height = 120
        self.draw_hexagonal_border(c, x, y, width, height)

        # Background
        c.setFillColor(colors.white)
        c.rect(x + 2, y + 2, width - 4, height - 4, fill=1, stroke=0)

        # Title
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 10, y + height - 15, "ATTACKS")

        # Table headers
        header_y = y + height - 35
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x + 10, header_y, "Name")
        c.drawString(x + 150, header_y, "Dmg.")
        c.drawString(x + 250, header_y, "Type")

        # Draw horizontal line under headers
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.line(x + 5, header_y - 5, x + width - 5, header_y - 5)

        # Weapon entries
        c.setFont("Helvetica", 8)
        row_height = 18
        for i in range(4):  # 4 attack slots
            row_y = header_y - 15 - (i * row_height)

            # Draw row separator lines
            if i > 0:
                c.line(x + 5, row_y + row_height - 5, x + width - 5, row_y + row_height - 5)

            # Fill with weapon data
            if i < len(weapons):
                weapon_name, damage, weapon_type = weapons[i]
                c.drawString(x + 10, row_y, weapon_name)
                c.drawString(x + 150, row_y, str(damage))
                c.drawString(x + 250, row_y, weapon_type)

    def draw_spellbook(self, c, x, y, data, character_data, width, height):
        """Draw the spellbook page with organized spells"""
        # Get spell slots for this character
        spell_slots = data.get("Spell Slots", {})
        selected_spells = data.get("Selected Spells", [])

        if not selected_spells:
            c.setFont("Helvetica", 12)
            c.drawString(x, y, "No spells known.")
            return

        # Show spell slots
        slots_y = y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x, slots_y, "SPELL SLOTS")

        slots_text = []
        for level, count in sorted(spell_slots.items()):
            if level == 0:
                slots_text.append(f"Cantrips: {count}")
            else:
                slots_text.append(f"Level {level}: {count}")

        c.setFont("Helvetica", 10)
        c.drawString(x, slots_y - 20, " | ".join(slots_text))

        # Organize spells by level
        spells_by_level = {}
        for spell_name in selected_spells:
            if spell_name in character_data.spell_database:
                spell_data = character_data.spell_database[spell_name]
                level = spell_data["level"]
                if level not in spells_by_level:
                    spells_by_level[level] = []
                spells_by_level[level].append((spell_name, spell_data))

        # Draw spells by level
        current_y = slots_y - 60

        for level in sorted(spells_by_level.keys()):
            spells = spells_by_level[level]

            # Level header
            c.setFont("Helvetica-Bold", 14)
            level_text = "CANTRIPS (0 LEVEL)" if level == 0 else f"LEVEL {level} SPELLS"
            c.drawString(x, current_y, level_text)
            current_y -= 25

            # Draw spells for this level
            for spell_name, spell_data in spells:
                current_y = self.draw_spell_entry(c, x, current_y, spell_name, spell_data, width - 100)
                current_y -= 20  # Space between spells

                # Check if we need a new page
                if current_y < 100:
                    c.showPage()
                    c.setFillColor(colors.white)
                    c.rect(0, 0, width, height, fill=1)

                    # Continue header
                    c.setFillColor(colors.black)
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(50, height - 50, f"{data.get('Name', 'Character')} - Spellbook (continued)")
                    current_y = height - 80

            current_y -= 10  # Extra space between spell levels

    def draw_spell_entry(self, c, x, y, spell_name, spell_data, max_width):
        """Draw a single spell entry"""
        entry_height = 80

        # Spell border
        self.draw_hexagonal_border(c, x, y - entry_height, max_width, entry_height)

        # Spell name
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.black)
        c.drawString(x + 10, y - 15, spell_name.upper())

        # Spell details in smaller text
        c.setFont("Helvetica", 9)
        details_y = y - 30

        # School and casting info
        details_line1 = f"School: {spell_data['school']} | Casting Time: {spell_data['casting_time']}"
        c.drawString(x + 10, details_y, details_line1)

        details_line2 = f"Range: {spell_data['range']} | Duration: {spell_data['duration']}"
        c.drawString(x + 10, details_y - 12, details_line2)

        # Description (wrapped)
        desc_y = details_y - 30
        c.setFont("Helvetica", 8)
        description = spell_data['description']

        # Simple text wrapping
        words = description.split()
        lines = []
        current_line = []
        line_width = 0
        max_line_width = max_width - 40  # Account for margins

        for word in words:
            word_width = c.stringWidth(word + " ", "Helvetica", 8)
            if line_width + word_width <= max_line_width:
                current_line.append(word)
                line_width += word_width
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                line_width = word_width

        if current_line:
            lines.append(" ".join(current_line))

        # Draw description lines
        for i, line in enumerate(lines[:2]):  # Limit to 2 lines to fit in box
            c.drawString(x + 10, desc_y - (i * 10), line)

        return y - entry_height

    def export_to_pdf(self, data, character_data):
        """Export character data to PDF with authentic DC20 styling"""
        file_name = data.get("Name", "Character") + ".pdf"
        c = canvas.Canvas(file_name, pagesize=letter)
        width, height = letter

        # === PAGE 1 CONTENT ONLY ===
        # White background
        c.setFillColor(colors.white)
        c.rect(0, 0, width, height, fill=1)

        # === HEADER SECTION ===
        self.draw_dc20_header(c, width, height, data)

        # === HEALTH AND RESOURCES ===
        resources_y = height - 200
        self.draw_resources_section(c, 50, resources_y, data)

        # === PRIME ATTRIBUTE ===
        prime_x = 450
        prime_y = resources_y  # Same Y level as health points and resources
        self.draw_prime_hexagon(c, prime_x, prime_y)

        # Add prime value
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 28)
        prime_value = str(data.get("Prime", 0))
        prime_width = c.stringWidth(prime_value, "Helvetica-Bold", 28)
        c.drawString(prime_x + 40 - prime_width / 2, prime_y + 35, prime_value)

        # === ATTRIBUTES SECTION ===
        attr_y = height - 350
        attr_spacing = 115

        # Draw four attribute hexagons
        attr_names = ["Might", "Agility", "Charisma", "Intelligence"]
        for i, attr_name in enumerate(attr_names):
            attr_x = 50 + (i * attr_spacing)
            attr_value = data.get(attr_name, 0)
            self.draw_attribute_hexagon(c, attr_x, attr_y, attr_name, attr_value)

        # === SKILLS SECTION ===
        skills_y = attr_y - 180

        # Parse and group skills
        skills_by_attr = {
            "Might": [], "Agility": [], "Charisma": [], "Intelligence": []
        }

        skill_to_attr_map = {}
        for skill_name, attr_name in character_data.skill_names:
            skill_to_attr_map[skill_name] = attr_name

        skill_entries = data["Skills"].split(', ')
        for entry in skill_entries:
            if ':' in entry:
                skill_name = entry.split(':')[0].strip()
                skill_value = entry.split(':')[1].split('(')[0].strip()
                training = entry.split('(')[1].replace(')', '') if '(' in entry else "None"

                if skill_name in skill_to_attr_map:
                    attr_name = skill_to_attr_map[skill_name]
                    skills_by_attr[attr_name].append((skill_name, skill_value, training))

        # Draw skill columns
        for i, (attr_name, skills_data) in enumerate(skills_by_attr.items()):
            skill_x = 50 + (i * attr_spacing)
            self.draw_skill_column(c, skill_x, skills_y, attr_name, skills_data)

        # === END PAGE 1 / START PAGE 2 ===
        c.showPage()

        # === PAGE 2 SETUP ===
        c.setFillColor(colors.white)
        c.rect(0, 0, width, height, fill=1)

        # Page 2 header
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 16)
        page2_title = f"{data.get('Name', 'Character')} - Combat & Equipment"
        c.drawString(50, height - 50, page2_title)

        # Separator line
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.line(50, height - 65, width - 50, height - 65)

        # === COMBAT SECTION (Page 2) ===
        combat_y_p2 = height - 150  # Moved down 2 lines (30 points)
        self.draw_combat_section(c, 50, combat_y_p2, data)

        # === ATTACKS SECTION (Page 2) ===
        attacks_y_p2 = combat_y_p2 - 135  # Moved down 1 line (15 points)  # Maintains relative spacing
        weapons = character_data.parse_weapons_from_inventory(
            data.get("Inventory", ""),
            data.get("Class", ""),
            data.get("Might", 0),
            data.get("Agility", 0),
            data.get("Combat Mastery", 0)
        )
        self.draw_attacks_table(c, 50, attacks_y_p2, weapons)

        # === INVENTORY SECTION (Page 2) ===
        inv_y_p2 = attacks_y_p2 - 150  # Maintain relative spacing
        inv_width = 450
        inv_height = 70

        self.draw_hexagonal_border(c, 50, inv_y_p2, inv_width, inv_height)
        c.setFillColor(colors.white)
        c.rect(52, inv_y_p2 + 2, inv_width - 4, inv_height - 4, fill=1, stroke=0)

        # Inventory title
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, inv_y_p2 + inv_height - 15, "INVENTORY")

        # Inventory items in columns
        c.setFont("Helvetica", 8)
        inventory_items = data.get("Inventory", "").split(', ')
        items_per_column = 3
        col_width = 130

        for i, item in enumerate(inventory_items[:12]):  # Limit to 12 items
            if item.strip():
                col = i // items_per_column
                row = i % items_per_column
                item_x = 60 + (col * col_width)
                item_y = inv_y_p2 + inv_height - 30 - (row * 12)
                c.drawString(item_x, item_y, f"• {item.strip()}")

        # Test text to verify page 2
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, "This is Page 2 - Combat & Equipment")

        # === START PAGE 3 (SPELLBOOK) ===
        if data.get("Selected Spells") and len(data.get("Selected Spells", [])) > 0:
            c.showPage()

            # === PAGE 3 SETUP ===
            c.setFillColor(colors.white)
            c.rect(0, 0, width, height, fill=1)

            # Page 3 header
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 16)
            page3_title = f"{data.get('Name', 'Character')} - Spellbook"
            c.drawString(50, height - 50, page3_title)

            # Separator line
            c.setStrokeColor(colors.black)
            c.setLineWidth(2)
            c.line(50, height - 65, width - 50, height - 65)

            # Draw spellbook content
            self.draw_spellbook(c, 50, height - 100, data, character_data, width, height)

        c.save()
        print(f"Enhanced DC20 character sheet saved as {file_name}")
        return True
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class PDFGenerator:
    def __init__(self):
        pass

    def draw_attribute_box(self, c, x, y, attr_name, attr_value, width=80, height=120):
        """Draw an attribute box similar to the character sheet"""
        # Main box
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(x, y, width, height)

        # Header with attribute name
        c.setFillColor(colors.lightgrey)
        c.rect(x, y + height - 25, width, 25, fill=1, stroke=1)

        # Attribute abbreviation
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        attr_abbrev = {"Might": "MIG", "Agility": "AGI", "Charisma": "CHA", "Intelligence": "INT"}
        text_x = x + width / 2
        text_y = y + height - 18
        text_width = c.stringWidth(attr_abbrev.get(attr_name, attr_name[:3]), "Helvetica-Bold", 12)
        c.drawString(text_x - text_width / 2, text_y, attr_abbrev.get(attr_name, attr_name[:3]))

        # Large attribute value
        c.setFont("Helvetica-Bold", 24)
        value_text = str(attr_value)
        value_width = c.stringWidth(value_text, "Helvetica-Bold", 24)
        c.drawString(text_x - value_width / 2, y + height / 2 - 8, value_text)

        # SAVE label at bottom
        c.setFont("Helvetica", 10)
        save_width = c.stringWidth("SAVE", "Helvetica", 10)
        c.drawString(text_x - save_width / 2, y + 10, "SAVE")

    def draw_skill_section(self, c, x, y, attr_name, skills_data, width=120):
        """Draw a skill section for an attribute"""
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)

        # Header
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.black)
        c.drawString(x, y, attr_name.upper())

        current_y = y - 20  # More space after header

        # Debug output
        print(f"Drawing skills for {attr_name}: {skills_data}")

        for skill_name, skill_value, training in skills_data:
            # Skill name - make sure we're setting the font and color properly
            c.setFont("Helvetica", 9)
            c.setFillColor(colors.black)
            skill_text = skill_name.upper()
            c.drawString(x, current_y, skill_text)
            print(f"  Drawing skill: {skill_text} at position ({x}, {current_y})")

            # Training boxes (5 boxes for expertise levels)
            box_size = 8
            boxes_start_x = x
            boxes_y = current_y - 18  # Closer to skill name

            c.setStrokeColor(colors.black)
            c.setLineWidth(1)

            for i in range(5):
                box_x = boxes_start_x + (i * (box_size + 2))

                # Draw empty box first
                c.setFillColor(colors.white)
                c.rect(box_x, boxes_y, box_size, box_size, stroke=1, fill=1)

                # Fill boxes based on training level
                if training == "Trained" and i == 0:
                    c.setFillColor(colors.black)
                    c.rect(box_x, boxes_y, box_size, box_size, fill=1, stroke=1)
                elif training == "Expert" and i <= 1:
                    c.setFillColor(colors.black)
                    c.rect(box_x, boxes_y, box_size, box_size, fill=1, stroke=1)

            current_y -= 35  # More space between skills

        # If no skills for this attribute, show placeholder
        if not skills_data:
            c.setFont("Helvetica", 8)
            c.setFillColor(colors.gray)
            c.drawString(x, current_y, "(No skills)")
            c.setFillColor(colors.black)

    def export_to_pdf(self, data, character_data):
        """Export character data to PDF"""
        file_name = data.get("Name", "Character") + ".pdf"
        c = canvas.Canvas(file_name, pagesize=letter)
        width, height = letter

        # Background color
        c.setFillColor(colors.white)
        c.rect(0, 0, width, height, fill=1)

        # === HEADER SECTION ===
        header_y = height - 60

        # Character Name
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.black)
        c.drawString(50, header_y, "CHARACTER NAME")
        c.setFont("Helvetica", 11)
        c.drawString(50, header_y - 15, data.get("Name", ""))

        # Class & Subclass
        c.setFont("Helvetica-Bold", 12)
        c.drawString(250, header_y, "CLASS & SUBCLASS")
        c.setFont("Helvetica", 11)
        subclass = data.get("Subclass", "")
        class_text = data.get("Class", "")
        if subclass:
            class_text += f" / {subclass}"
        c.drawString(250, header_y - 15, class_text)

        # Level (in box)
        level_box_x = width - 80
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(level_box_x, header_y - 20, 60, 40)
        c.setFont("Helvetica", 10)
        c.drawString(level_box_x + 20, header_y + 5, "LEVEL")
        c.setFont("Helvetica-Bold", 20)
        level_text = str(data.get("Level", 1))
        level_width = c.stringWidth(level_text, "Helvetica-Bold", 20)
        c.drawString(level_box_x + 30 - level_width / 2, header_y - 15, level_text)

        # Ancestry & Background (moved down to avoid overlap)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, header_y - 40, "ANCESTRY & BACKGROUND")
        c.setFont("Helvetica", 11)
        ancestry_bg = f"{data.get('Ancestry', '')} / {data.get('Background', '')}"
        c.drawString(50, header_y - 55, ancestry_bg)

        # Combat Mastery (moved to avoid overlap)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(250, header_y - 40, "COMBAT MASTERY")
        c.setFont("Helvetica-Bold", 16)
        c.drawString(250, header_y - 55, str(data.get("Combat Mastery", 0)))

        # === MAIN STATS SECTION ===
        stats_y = height - 180  # Moved down to avoid header overlap

        # Prime Attribute (large box)
        prime_x = 50
        c.setStrokeColor(colors.black)
        c.setLineWidth(3)
        c.rect(prime_x, stats_y, 60, 60)
        c.setFont("Helvetica-Bold", 24)
        prime_text = str(data.get("Prime", 0))
        prime_width = c.stringWidth(prime_text, "Helvetica-Bold", 24)
        c.drawString(prime_x + 30 - prime_width / 2, stats_y + 35, prime_text)

        c.setFont("Helvetica-Bold", 12)
        prime_label_width = c.stringWidth("PRIME", "Helvetica-Bold", 12)
        c.drawString(prime_x + 30 - prime_label_width / 2, stats_y + 15, "PRIME")

        c.setFont("Helvetica", 8)
        subtitle_text = "= Highest Attribute"
        subtitle_width = c.stringWidth(subtitle_text, "Helvetica", 8)
        c.drawString(prime_x + 30 - subtitle_width / 2, stats_y + 5, subtitle_text)

        # Health Points (positioned better)
        hp_x = 130
        hp = 10 + (int(data.get('Level', 1)) * int(data.get('Might', 0)))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(hp_x, stats_y + 40, "HEALTH POINTS")
        c.setFont("Helvetica-Bold", 24)
        c.drawString(hp_x + 20, stats_y + 15, str(hp))

        # Resources section (positioned to avoid overlap)
        resources_x = 350
        c.setFont("Helvetica-Bold", 12)
        c.drawString(resources_x, stats_y + 50, "RESOURCES")

        # Stamina Points
        c.setFont("Helvetica", 10)
        c.drawString(resources_x, stats_y + 35, "STAMINA POINTS")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(resources_x + 90, stats_y + 35, str(data.get("Grit Points", 0)))

        # Mana Points
        c.setFont("Helvetica", 10)
        c.drawString(resources_x, stats_y + 20, "MANA POINTS")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(resources_x + 90, stats_y + 20, "0")  # Placeholder

        # Grit Points
        c.setFont("Helvetica", 10)
        c.drawString(resources_x, stats_y + 5, "GRIT POINTS")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(resources_x + 90, stats_y + 5, str(data.get("Grit Points", 0)))

        # === ATTRIBUTES SECTION ===
        attr_y = height - 320  # Adjusted to accommodate new header spacing
        attr_spacing = 90

        # Draw attribute boxes
        attr_names = ["Might", "Agility", "Charisma", "Intelligence"]
        for i, attr_name in enumerate(attr_names):
            attr_x = 50 + (i * attr_spacing)
            attr_value = data.get(attr_name, 0)
            self.draw_attribute_box(c, attr_x, attr_y, attr_name, attr_value)

        # === SKILLS SECTION ===
        skills_y = attr_y - 200

        # Group skills by attribute - using the proper skill organization
        skills_by_attr = {
            "Might": [], "Agility": [], "Charisma": [], "Intelligence": []
        }

        # Map each skill to its attribute based on character_data.skill_names
        skill_to_attr_map = {}
        for skill_name, attr_name in character_data.skill_names:
            skill_to_attr_map[skill_name] = attr_name

        # Parse the skills string from character data
        skill_entries = data["Skills"].split(', ')
        for entry in skill_entries:
            if ':' in entry:
                skill_name = entry.split(':')[0].strip()
                skill_value = entry.split(':')[1].split('(')[0].strip()
                training = entry.split('(')[1].replace(')', '') if '(' in entry else "None"

                # Find which attribute this skill belongs to
                if skill_name in skill_to_attr_map:
                    attr_name = skill_to_attr_map[skill_name]
                    skills_by_attr[attr_name].append((skill_name, skill_value, training))
                else:
                    print(f"Warning: Skill {skill_name} not found in skill mapping")

        # Debug output
        print("Debug - Skills by attribute for PDF:")
        for attr, skills in skills_by_attr.items():
            print(f"  {attr}: {skills}")

        # Draw skill sections
        for i, (attr_name, skills_data) in enumerate(skills_by_attr.items()):
            skill_x = 50 + (i * attr_spacing)
            self.draw_skill_section(c, skill_x, skills_y, attr_name, skills_data)

        # === COMBAT SECTION ===
        combat_y = skills_y - 150
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, combat_y, "COMBAT")

        # Combat box background
        c.setFillColor(colors.lightgrey)
        c.rect(50, combat_y - 80, 300, 70, fill=1, stroke=1)
        c.setFillColor(colors.black)

        combat_stats = [
            ("ATTACK / SPELL CHECK", f"CM + Prime"),
            ("SAVE DC", f"10 + CM + Prime"),
            ("INITIATIVE", f"CM + AGI")
        ]

        current_y = combat_y - 20
        c.setFont("Helvetica", 10)
        for label, formula in combat_stats:
            c.drawString(55, current_y, f"{label} = {formula}")
            current_y -= 20

        # Add actual calculated values
        current_y = combat_y - 20
        c.setFont("Helvetica-Bold", 12)
        values = [
            str(data.get('Spell Check', 0)),
            str(data.get('Save DC', 0)),
            str(data.get('Initiative', 0))
        ]
        for value in values:
            c.drawString(280, current_y, value)
            current_y -= 20

        # === ATTACKS SECTION ===
        attacks_y = combat_y - 100
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, attacks_y, "ATTACKS")

        # Parse weapons from inventory with DC20 mechanics
        might = data.get("Might", 0)
        agility = data.get("Agility", 0)
        combat_mastery = data.get("Combat Mastery", 0)
        weapons = character_data.parse_weapons_from_inventory(
            data.get("Inventory", ""),
            data.get("Class", ""),
            might,
            agility,
            combat_mastery
        )

        # Attack table with proper borders
        table_x = 50
        table_y = attacks_y - 25
        table_width = 350
        row_height = 20

        # Headers
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.lightgrey)
        c.rect(table_x, table_y, table_width, row_height, fill=1, stroke=1)
        c.setFillColor(colors.black)

        c.drawString(table_x + 5, table_y + 6, "Name")
        c.drawString(table_x + 150, table_y + 6, "Dmg.")
        c.drawString(table_x + 250, table_y + 6, "Type")

        # Weapon rows
        c.setFillColor(colors.white)
        c.setFont("Helvetica", 9)

        for i in range(4):  # 4 attack slots
            row_y = table_y - ((i + 1) * row_height)
            c.rect(table_x, row_y, table_width, row_height, fill=1, stroke=1)

            # Vertical lines for columns
            c.line(table_x + 140, row_y, table_x + 140, row_y + row_height)
            c.line(table_x + 240, row_y, table_x + 240, row_y + row_height)

            # Fill with weapon data if available
            if i < len(weapons):
                weapon_name, damage, weapon_type = weapons[i]
                c.setFillColor(colors.black)
                c.drawString(table_x + 5, row_y + 6, weapon_name)
                c.drawString(table_x + 150, row_y + 6, damage)
                c.drawString(table_x + 250, row_y + 6, weapon_type)
                c.setFillColor(colors.white)

        # === INVENTORY SECTION ===
        inv_y = attacks_y - 140
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, inv_y, "INVENTORY")

        # Create inventory box
        inv_box_height = 80
        c.setStrokeColor(colors.black)
        c.setFillColor(colors.white)
        c.rect(50, inv_y - inv_box_height, 500, inv_box_height, fill=1, stroke=1)

        c.setFont("Helvetica", 9)
        inventory_items = data.get("Inventory", "").split(', ')
        current_y = inv_y - 15
        items_per_row = 3
        current_x = 55

        for i, item in enumerate(inventory_items):
            if item.strip():
                if i > 0 and i % items_per_row == 0:
                    current_y -= 12
                    current_x = 55
                c.drawString(current_x, current_y, f"• {item.strip()}")
                current_x += 160  # Space items horizontally

        # === DEFENSE ZONES (PDR, EDR, MDR) ===
        defense_y = inv_y - 100
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, defense_y, "DEFENSE ZONES")

        defense_types = ["PDR", "EDR", "MDR"]
        armor_rating = data.get("Armor Rating", 10)

        for i, defense_type in enumerate(defense_types):
            def_x = 400 + (i * 60)
            def_y = defense_y - 30

            # Defense box
            c.setStrokeColor(colors.black)
            c.setFillColor(colors.white)
            c.rect(def_x, def_y, 50, 40, fill=1, stroke=1)

            # Defense type label
            c.setFont("Helvetica-Bold", 10)
            label_width = c.stringWidth(defense_type, "Helvetica-Bold", 10)
            c.drawString(def_x + 25 - label_width / 2, def_y + 25, defense_type)

            # Defense value
            c.setFont("Helvetica-Bold", 14)
            if defense_type == "PDR":
                value = str(armor_rating)
            elif defense_type == "EDR":
                value = str(armor_rating - 2)  # Typically 2 less than PDR
            else:  # MDR
                value = str(armor_rating - 4)  # Typically 4 less than PDR

            value_width = c.stringWidth(value, "Helvetica-Bold", 14)
            c.drawString(def_x + 25 - value_width / 2, def_y + 8, value)

        c.save()
        print(f"Character sheet saved as {file_name}")
        return True
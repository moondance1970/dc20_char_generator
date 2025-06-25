import json
import os
from pathlib import Path

class FileManager:
    def __init__(self):
        self.characters_dir = Path("characters")
        self.characters_dir.mkdir(exist_ok=True)
    
    def save_character_data(self, data):
        """Save character data to JSON file"""
        char_name = data.get("Name", "Character").replace(" ", "_").replace("/", "_")
        json_file = self.characters_dir / f"{char_name}.json"
        
        try:
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Character data saved to {json_file}")
            return True
        except Exception as e:
            print(f"Error saving character data: {e}")
            return False
    
    def load_character_data(self, json_file):
        """Load character data from JSON file"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error loading character data: {e}")
            return None
    
    def get_available_characters(self):
        """Get list of available character files"""
        if not self.characters_dir.exists():
            return []
        
        characters = []
        for json_file in self.characters_dir.glob("*.json"):
            try:
                data = self.load_character_data(json_file)
                if data and "Name" in data:
                    characters.append((data["Name"], str(json_file)))
            except:
                continue
        
        return characters
    
    def delete_character(self, character_name):
        """Delete a character's JSON file"""
        char_filename = character_name.replace(" ", "_").replace("/", "_")
        json_file = self.characters_dir / f"{char_filename}.json"
        
        try:
            if json_file.exists():
                json_file.unlink()
                return True
        except Exception as e:
            print(f"Error deleting character: {e}")
        return False
import tkinter as tk
from tkinter import ttk, messagebox

def main():
    root = tk.Tk()
    root.title("DC20 Character Creator")
    root.geometry("800x900")  # Larger window to accommodate spell section

    # Import the updated modules
    try:
        from character_data import CharacterData
        from ui_components import CharacterCreatorUI
        from pdf_generator import PDFGenerator
        from file_manager import FileManager
    except ImportError as e:
        messagebox.showerror("Import Error", f"Failed to import modules: {e}")
        return

    # Initialize components
    character_data = CharacterData()
    file_manager = FileManager()
    pdf_generator = PDFGenerator()

    # Create and run the UI
    app = CharacterCreatorUI(root, character_data, file_manager, pdf_generator)

    # Add scrollbar to main window if needed
    root.mainloop()


if __name__ == "__main__":
    main()
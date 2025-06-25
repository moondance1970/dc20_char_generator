import tkinter as tk
from tkinter import ttk, messagebox
from character_data import CharacterData
from ui_components import CharacterCreatorUI
from pdf_generator import PDFGenerator
from file_manager import FileManager


def main():
    root = tk.Tk()
    root.title("DC20 Character Creator")

    # Initialize components
    character_data = CharacterData()
    file_manager = FileManager()
    pdf_generator = PDFGenerator()

    # Create and run the UI
    app = CharacterCreatorUI(root, character_data, file_manager, pdf_generator)

    root.mainloop()


if __name__ == "__main__":
    main()
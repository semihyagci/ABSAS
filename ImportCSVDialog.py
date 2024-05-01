import tkinter as tk
from tkinter import filedialog
import csv

class ImportCSVDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Import from CSV")
        self.geometry("300x100")

        self.file_path = ""

        browse_button = tk.Button(self, text="Browse Files", command=self.browse_files)
        browse_button.pack(pady=10)

        start_tagging_button = tk.Button(self, text="Start Tagging", command=self.start_tagging)
        start_tagging_button.pack(pady=5)

    def browse_files(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    def start_tagging(self):
        if self.file_path:
            self.destroy()
            tagging_dialog = TaggingDialog(self.master, self.file_path)
            tagging_dialog.grab_set()
            tagging_dialog.focus_set()

class TaggingDialog(tk.Toplevel):
    def __init__(self, master, file_path):
        super().__init__(master)
        self.title("Tagging Dialog")
        self.geometry("400x200")

        self.file_path = file_path
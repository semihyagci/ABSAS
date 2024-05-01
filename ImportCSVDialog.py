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

        # Read CSV file and extract values from 'Additional' column
        self.additional_options = self.read_csv()

        # Dropdown menu to display options from 'Additional' column
        self.selected_option = tk.StringVar(self)
        self.selected_option.set("")  # Default value
        dropdown_menu = tk.OptionMenu(self, self.selected_option, *self.additional_options)
        dropdown_menu.pack(pady=10)

    def read_csv(self):
        additional_options = []
        with open(self.file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'Additional' in row:
                    additional_options.append(row['Additional'])
        return additional_options

import tkinter as tk
from tkinter import filedialog
import csv


class ImportCSVDialog(tk.Toplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.title("Import from CSV")
        self.geometry("600x300")

        self.file_path = ""
        self.callback = callback

        file_frame = tk.Frame(self)
        file_frame.pack(pady=5)

        file_label = tk.Label(file_frame, text="File Path:")
        file_label.grid(row=0, column=0)

        self.file_path_entry = tk.Entry(file_frame, width=40)
        self.file_path_entry.grid(row=0, column=1)

        browse_button = tk.Button(file_frame, text="Browse Files", command=self.browse_files)
        browse_button.grid(row=0, column=2)

        load_button = tk.Button(self, text="Load Additional Aspects", command=self.start_tagging)
        load_button.pack(pady=10)

    def browse_files(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, self.file_path)

    def start_tagging(self):
        if self.file_path:
            csv_options = self.read_csv_options()
            self.callback(csv_options)
            self.destroy()

    def read_csv_options(self):
        csv_options = []
        with open(self.file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'Additional' in row:
                    csv_options.append(row['Additional'])
        return csv_options

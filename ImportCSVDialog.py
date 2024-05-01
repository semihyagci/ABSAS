import tkinter as tk
from tkinter import filedialog
import csv


class ImportCSVDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Import from CSV")
        self.geometry("600x300")

        self.file_path = ""

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
            self.destroy()
            tagging_dialog = TaggingDialog(self.master, self.file_path)
            tagging_dialog.grab_set()
            tagging_dialog.focus_set()


class TaggingDialog(tk.Toplevel):
    def __init__(self, master, file_path):
        super().__init__(master)
        self.title("Tagging Dialog")
        self.geometry("600x300")

        self.file_path = file_path

        self.csv_content = self.read_csv_file()

    def read_csv_file(self):
        csv_content = []
        try:
            with open(self.file_path, newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip the first row
                for row in csv_reader:
                    csv_content.append(row)
        except Exception as e:
            print(f"Error reading CSV file: {e}")

        print(csv_content)
        return csv_content

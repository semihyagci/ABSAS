import tkinter as tk
from tkinter import ttk
import csv

from AdditionalAspectTaggingApp import AdditionalAspectTaggingApp


class AdditionalAspectTemplate(tk.Frame):
    def __init__(self, master, id_num, text_list, dct, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.id_num = id_num
        self.text_list = text_list
        self.dct = dct
        self.text = ""
        self.create_widgets()

    def create_widgets(self):
        # Input Frame (Top Frame)
        input_frame = tk.Frame(self)
        input_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # id_label
        id_label = tk.Label(input_frame, text=f"You are adding aspects to row with the ID: {self.id_num}.")
        id_label.pack(anchor="w", padx=5, pady=5)

        # selected_text_label
        self.selected_text_label = tk.Label(input_frame, text=f"Selected text: {self.text}")
        self.selected_text_label.pack(anchor="w", padx=5, pady=5)

        # Label for "Text:"
        tk.Label(input_frame, text="Text:").pack(anchor="w", padx=0, pady=0)

        # AdditionalAspectTaggingApp
        self.text_entry = AdditionalAspectTaggingApp(input_frame, self.text_list, self.dct, self.id_num)
        self.text_entry.pack(anchor="w", padx=5, pady=5)

        # Matrix Frame (Middle Frame)
        self.matrix_frame = tk.Frame(self)
        self.matrix_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Matrix Header
        headers = ["ID", "Aspect Name", "Matched Word", "Aspect Type"]
        for i, header in enumerate(headers):
            tk.Label(self.matrix_frame, text=header).grid(row=0, column=i, padx=5, pady=5)

        # Third Frame (Bottom Frame)
        third_frame = tk.Frame(self)
        third_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        tk.Label(third_frame, text="Enter Aspect Name:").grid(row=0, column=0, padx=5, pady=5)
        self.aspect_name_entry = tk.Entry(third_frame)
        self.aspect_name_entry.grid(row=0, column=1, padx=5, pady=5)
        add_button = tk.Button(third_frame, text="Add Row", command=lambda: self.add_row(self.matrix_frame))
        add_button.grid(row=0, column=3, padx=5, pady=5)
        import_button = tk.Button(third_frame, text="Import from CSV", command=self.import_from_csv)
        import_button.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

    def add_row(self, matrix_frame):
        # Get the current number of rows in the matrix_frame
        current_row_count = matrix_frame.grid_size()[1]

        # Increment ID by 1
        new_id = current_row_count

        # Aspect Name
        aspect_name = self.aspect_name_entry.get()

        # Matched Word
        matched_word = self.text

        # Aspect Type
        self.aspect_type_var = tk.StringVar(matrix_frame, "Neutral")  # Default value
        aspect_type_dropdown = ttk.Combobox(matrix_frame, textvariable=self.aspect_type_var,
                                            values=["Neutral", "Positive", "Negative"])
        aspect_type_dropdown.grid(row=current_row_count, column=3, padx=5, pady=5)
        aspect_type = self.aspect_type_var.get()

        # Update the matrix_frame with the new row
        tk.Label(matrix_frame, text=str(new_id)).grid(row=current_row_count, column=0, padx=5, pady=5)
        tk.Label(matrix_frame, text=aspect_name).grid(row=current_row_count, column=1, padx=5, pady=5)
        tk.Label(matrix_frame, text=matched_word).grid(row=current_row_count, column=2, padx=5, pady=5)

    def assign_selected_row(self, word):
        self.text = word
        self.selected_text_label.config(text=f"Selected text: {self.text}")

    def import_from_csv(self):
        # Logic to import data from CSV
        pass

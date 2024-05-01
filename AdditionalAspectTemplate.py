import tkinter as tk

from AdditionalAspectTaggingApp import AdditionalAspectTaggingApp
from ImportCSVDialog import ImportCSVDialog


class AdditionalAspectTemplate(tk.Frame):
    def __init__(self, master, id_num, text_list, dct, *args, **kwargs):
        self.add_list = []
        super().__init__(master, *args, **kwargs)
        self.id_num = id_num
        self.text_list = text_list
        self.dct = dct
        self.text = ""
        self.create_widgets()
        self.unique = ""

    def create_widgets(self):
        input_frame = tk.Frame(self)
        input_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        id_label = tk.Label(input_frame, text=f"You are adding aspects to row with the ID: {self.id_num}.")
        id_label.pack(anchor="w", padx=5, pady=5)

        self.selected_text_label = tk.Label(input_frame, text=f"Selected text: {self.text}")
        self.selected_text_label.pack(anchor="w", padx=5, pady=5)

        tk.Label(input_frame, text="Text:").pack(anchor="w", padx=0, pady=0)

        self.text_entry = AdditionalAspectTaggingApp(input_frame, self.text_list, self.dct, self.id_num)
        self.text_entry.pack(anchor="w", padx=5, pady=5)

        self.matrix_frame = tk.Frame(self)
        self.matrix_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        headers = ["ID", "Aspect Name", "Matched Word", "Aspect Type"]
        for i, header in enumerate(headers):
            tk.Label(self.matrix_frame, text=header).grid(row=0, column=i, padx=5, pady=5)

        if "additional_aspect_list" in self.dct:
            for idx, aspect_tuple in enumerate(self.dct["additional_aspect_list"], start=1):
                indices,aspect_name, word, aspect_type = aspect_tuple
                start_index, end_index = map(str, indices.split(':'))
                start = f"1.{start_index}"
                end = f"1.{end_index}"
                # matched_word = self.text_entry.text.get(start, end)
                # Update the matrix_frame with the existing data
                tk.Label(self.matrix_frame, text=str(idx)).grid(row=idx, column=0, padx=5, pady=5)
                tk.Label(self.matrix_frame, text=aspect_name).grid(row=idx, column=1, padx=5, pady=5)
                tk.Label(self.matrix_frame, text=word).grid(row=idx, column=2, padx=5, pady=5)

                aspect_type_var = tk.StringVar(self,value=aspect_type)
                aspect_type_var.set(aspect_type)
                aspect_type_menu = tk.OptionMenu(self.matrix_frame, aspect_type_var, "Neutral", "Positive", "Negative")
                aspect_type_menu.grid(row=idx, column=3, padx=5, pady=5)

                self.add_list.append((indices, aspect_name, word, aspect_type_var))

        third_frame = tk.Frame(self)
        third_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        tk.Label(third_frame, text="Enter Aspect Name:").grid(row=0, column=0, padx=5, pady=5)
        self.aspect_name_entry = tk.Entry(third_frame)
        self.aspect_name_entry.grid(row=0, column=1, padx=5, pady=5)
        add_button = tk.Button(third_frame, text="Add Row", command=lambda: self.add_row(self.matrix_frame))
        add_button.grid(row=0, column=3, padx=5, pady=5)

        def clear_entry():
            self.aspect_name_entry.delete(0, 'end')

        add_button = tk.Button(third_frame, text="Add Row",
                               command=lambda: [self.add_row(self.matrix_frame), clear_entry()])
        add_button.grid(row=0, column=3, padx=5, pady=5)

        import_csv_button = tk.Button(third_frame, text="Import from CSV", command=self.import_from_csv)
        import_csv_button.grid(row=1, column=1,columnspan=4, padx=5, pady=5)

        save_button = tk.Button(third_frame, text="Save", command=self.save_additional)
        save_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


    def add_row(self, matrix_frame):
        current_row_count = matrix_frame.grid_size()[1]

        new_id = current_row_count

        aspect_name = self.aspect_name_entry.get()

        matched_word = self.text

        aspect_type_var = tk.StringVar(value="Neutral")

        aspect_type_menu = tk.OptionMenu(matrix_frame, aspect_type_var, "Neutral", "Positive", "Negative")
        aspect_type_menu.grid(row=current_row_count, column=3, padx=5, pady=5)

        tk.Label(matrix_frame, text=str(new_id)).grid(row=current_row_count, column=0, padx=5, pady=5)
        tk.Label(matrix_frame, text=aspect_name).grid(row=current_row_count, column=1, padx=5, pady=5)
        tk.Label(matrix_frame, text=matched_word).grid(row=current_row_count, column=2, padx=5, pady=5)
        new_tuple = (self.unique,aspect_name, matched_word, aspect_type_var)
        self.add_list.append(new_tuple)

    def assign_selected_row(self, word,word_start,word_end):
        self.text = word
        self.selected_text_label.config(text=f"Selected text: {self.text}")
        self.unique = (word_start.split(".")[1]) + ":" + word_end.split(".")[1]

    def import_from_csv(self):
        import_csv_dialog = ImportCSVDialog(self.master)
        import_csv_dialog.grab_set()
        import_csv_dialog.focus_set()

    def save_additional(self):
        updated_list = []

        if 'additional_aspect_list' in self.dct and self.dct['additional_aspect_list'] is not None:
            updated_list = self.dct['additional_aspect_list']

        for aspect_tuple in self.add_list:
            unique_id, aspect_name, matched_word, aspect_type_var = aspect_tuple
            aspect_type = aspect_type_var.get()  # Get the current aspect_type_var value

            # Check if the aspect name already exists in updated_list
            existing_index = None
            for i, tup in enumerate(updated_list):
                if tup[1] == aspect_name:
                    existing_index = i
                    break

            if existing_index is not None:
                # Update the aspect type if the aspect name already exists
                updated_list[existing_index] = (unique_id, aspect_name, matched_word, aspect_type)
            else:
                # Otherwise, append a new tuple
                updated_list.append((unique_id, aspect_name, matched_word, aspect_type))

        self.dct['additional_aspect_list'] = updated_list
        print("Updated additional aspect list:", self.dct['additional_aspect_list'])
        self.master.master.master.destroy()


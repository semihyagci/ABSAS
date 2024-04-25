import tkinter as tk

from AspectTaggingApp import AspectTaggingApp


class AdditionalAspectTemplate(tk.Frame):
    def __init__(self, master, id_num, text_list, dct, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.id_num = id_num
        self.text_list = text_list
        self.dct = dct
        self.create_widgets()

    def create_widgets(self):
        # Create label for row ID
        id_label = tk.Label(self, text=f"You are adding aspects to row with the ID: {self.id_num}.")
        id_label.pack(anchor="w", padx=5, pady=5)

        # Create label for "Text:"
        text_label = tk.Label(self, text=f"Text: {self.text_list}")
        text_label.pack(anchor="w", padx=5, pady=5)


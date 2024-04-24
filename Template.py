import tkinter as tk

from AspectTaggingApp import AspectTaggingApp


class Template(tk.Frame):
    def __init__(self, master, id_num, text_list, dct, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.id_num = id_num
        self.text_list = text_list
        self.dct = dct
        self.create_widgets()


    def create_widgets(self):
        # ID Label
        id_label = tk.Label(self, text=f"ID: {self.id_num}")
        id_label.grid(row=0, column=0, padx=5, pady=5)

        # Aspect Tagging Widget
        aspect_tagging_app = AspectTaggingApp(self, self.text_list,self.dct)
        aspect_tagging_app.grid(row=0, column=1, padx=5, pady=5)

        # Overall Aspect Dropdown
        options = ["Positive", "Negative", "Neutral"]
        self.aspect_var = tk.StringVar(self)
        self.aspect_var.set(options[2])  # Default value
        dropdown = tk.OptionMenu(self, self.aspect_var, *options)
        dropdown.grid(row=0, column=2, padx=5, pady=5)



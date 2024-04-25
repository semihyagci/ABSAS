import tkinter as tk
from AspectTaggingApp import AspectTaggingApp


class Template(tk.Frame):
    def __init__(self, master, id_num, text_list, dct, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.id_num = id_num
        self.text_list = text_list
        self.dct = dct
        print("inside template ")
        print("dict: ", dct)
        self.create_widgets()

    def create_widgets(self):
        # ID Label
        id_label = tk.Label(self, text=f"ID: {self.id_num}")
        id_label.grid(row=0, column=0, padx=5, pady=5)

        # Aspect Tagging Widget
        aspect_tagging_app = AspectTaggingApp(self, self.text_list, self.dct, self.id_num)
        aspect_tagging_app.grid(row=0, column=1, padx=5, pady=5)

        # Overall Aspect Dropdown
        options = ["Positive", "Negative", "Neutral"]
        self.aspect_var = tk.StringVar(self)
        overall_value = self.dct.get('overall', 'Neutral')  # Get the value of 'overall', default to 'Neutral'
        self.aspect_var.set(overall_value)  # Set the initial value of the dropdown
        dropdown = tk.OptionMenu(self, self.aspect_var, *options)
        dropdown.grid(row=0, column=2, padx=5, pady=5)

    def update_overall_aspect_dropdown(self, aspect):
        self.aspect_var.set(aspect)

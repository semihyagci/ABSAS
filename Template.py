import tkinter as tk

from AdditionalAspectTaggingApp import AdditionalAspectTaggingApp
from AdditionalAspectTemplate import AdditionalAspectTemplate
from AspectTaggingApp import AspectTaggingApp


class Template(tk.Frame):
    column_names_created = False
    def __init__(self, master, id_num, text_list, dct, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.id_num = id_num
        self.text_list = text_list
        self.dct = dct
        self.create_widgets()

    def create_widgets(self):
        if not Template.column_names_created:
            self.create_column_names()
            Template.column_names_created = True
        # ID Label
        id_label = tk.Label(self, text=f"ID: {self.id_num}")
        id_label.grid(row=1, column=0, padx=5, pady=5)

        # Aspect Tagging Widget
        aspect_tagging_app = AspectTaggingApp(self, self.text_list, self.dct, self.id_num)
        aspect_tagging_app.grid(row=1, column=1, padx=5, pady=5)

        # Overall Aspect Dropdown
        options = ["Positive", "Negative", "Neutral"]
        self.aspect_var = tk.StringVar(self)
        overall_value = self.dct.get('overall', 'Neutral')  # Get the value of 'overall', default to 'Neutral'
        self.aspect_var.set(overall_value)  # Set the initial value of the dropdown
        dropdown = tk.OptionMenu(self, self.aspect_var, *options)
        dropdown.grid(row=1, column=2, padx=5, pady=5)

        #ADDITIONAL ASPECT PART
        add_button = tk.Button(self, text="Add Additional Aspect", command=self.open_additional_aspect_dialog)
        add_button.grid(row=1, column=3, padx=5, pady=5)

    def open_additional_aspect_dialog(self):
        # Create a Toplevel window for the additional aspect dialog
        additional_aspect_dialog = tk.Toplevel(self)
        additional_aspect_dialog.title("Additional Aspect")

        additional_aspect_dialog.geometry("500x300")

        # Create a canvas and scrollbar for the Toplevel window
        canvas = tk.Canvas(additional_aspect_dialog)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(additional_aspect_dialog, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_configure)

        # Bind the mouse wheel event to the canvas
        additional_aspect_dialog.bind("<MouseWheel>", lambda event: self.scroll_canvas_here(event, canvas))

        # Create content for the scrollable frame
        content_template = AdditionalAspectTemplate(frame, self.id_num, self.text_list, self.dct)
        content_template.pack(anchor="w", padx=5, pady=5)

    def scroll_canvas_here(self, event, canvas):
        if event.delta > 0:
            canvas.yview_scroll(-1, "units")
        else:
            canvas.yview_scroll(1, "units")

    def create_column_names(self):
        # ID column
        id_label = tk.Label(self, text="ID")
        id_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        # Aspect Tagging column
        aspect_label = tk.Label(self, text="Text")
        aspect_label.grid(row=0, column=1, columnspan=1, padx=5, pady=1,sticky="n")

        # Overall Aspect column
        overall_label = tk.Label(self, text="Overall Aspect")
        overall_label.grid(row=0, column=2, padx=5, pady=5, sticky="n")

        # Additional Aspect column
        add_label = tk.Label(self, text="Additional Aspect")
        add_label.grid(row=0, column=3, padx=5, pady=5, sticky="n")

    def update_overall_aspect_dropdown(self, aspect):
        self.aspect_var.set(aspect)

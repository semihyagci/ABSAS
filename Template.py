import tkinter as tk

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
        id_label.grid(row=1, column=0, padx=5, pady=30, sticky="w")

        # Aspect Tagging Widget
        aspect_tagging_app = AspectTaggingApp(self, self.text_list, self.dct, self.id_num)
        aspect_tagging_app.grid(row=1, column=1, padx=5, pady=30, sticky="ew")

        # Overall Sentiment Dropdown
        options = ["Positive", "Negative", "Neutral"]
        self.sentiment_var = tk.StringVar(self)
        overall_value = self.dct.get('overall', 'Neutral')  # Get the value of 'overall', default to 'Neutral'
        self.sentiment_var.set(overall_value)  # Set the initial value of the dropdown
        dropdown = tk.OptionMenu(self, self.sentiment_var, *options)
        dropdown.grid(row=1, column=2, padx=20, pady=30, sticky="ew")

        # Afinn Score Label
        afinn_label = tk.Label(self, text=f"{self.dct['sentence_afinn_score']}")
        afinn_label.grid(row=1, column=3, padx=40, pady=30, sticky="ew")

        # ADDITIONAL ASPECT PART
        add_button = tk.Button(self, text="Add Additional Aspect", command=self.open_additional_aspect_dialog)
        add_button.grid(row=1, column=4, padx=40, pady=30, sticky="ew")

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
        column_frame = tk.Frame(self.master.master.master, bg="#CCCCCC")
        column_frame.pack(side="top", fill="x", padx=10, pady=(20, 5))  # Added vertical padding

        column_names = ["ID", "Text", "Overall Sentiment", "Afinn Score", "Additional Aspect"]
        for i, col_name in enumerate(column_names):
            label = tk.Label(column_frame, text=col_name, bg="#CCCCCC", padx=10, pady=5, font=("Arial", 14, "bold"))
            if i == 1:  # Add spacer label between 0 and 1 index columns
                spacer_label = tk.Label(column_frame, text="", bg="#CCCCCC", padx=125, pady=5)
                spacer_label.grid(row=0, column=(i * 2) - 1)  # Adjust column index for spacer label
            elif i == 2:  # Add spacer label between 1 and 2 index columns
                spacer_label = tk.Label(column_frame, text="", bg="#CCCCCC", padx=125, pady=5)
                spacer_label.grid(row=0, column=(i * 2) - 1)  # Adjust column index for spacer label
            label.grid(row=0, column=i * 2)  # Adjust column index for column label

        column_frame.place(relx=0.5, rely=0, anchor="n", relwidth=1.0)

    def update_overall_sentiment_dropdown(self, aspect):
        self.sentiment_var.set(aspect)

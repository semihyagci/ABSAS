import tkinter as tk
from tkinter import ttk

class AspectTaggingApp(tk.Frame):
    def __init__(self, master, sentences, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.sentences = sentences
        self.setup_widgets()

    def setup_widgets(self):
        input_frame = tk.Frame(self)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.text = self.create_scrollable_text(input_frame)
        self.text.bind("<Double-Button-1>", self.tag_word)

        self.text.insert(tk.END,self.sentences + "\n\n")
        self.text.config(state=tk.DISABLED)

    def create_scrollable_text(self,parent):
        text_scroll = tk.Scrollbar(parent, orient=tk.VERTICAL)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        horizontal_scroll = tk.Scrollbar(parent, orient=tk.HORIZONTAL)
        horizontal_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        text_widget = tk.Text(parent, wrap=tk.NONE, yscrollcommand=text_scroll.set,
                              xscrollcommand=horizontal_scroll.set)
        text_widget.pack(expand=True, fill=tk.BOTH)

        text_scroll.config(command=text_widget.yview)
        horizontal_scroll.config(command=text_widget.xview)

        return text_widget

    def tag_word(self, event):
        index = self.text.index(f"@{event.x},{event.y}")
        word_start = self.text.index(f"{index} wordstart")
        word_end = self.text.index(f"{index} wordend")
        word = self.text.get(word_start, word_end)

        aspect_window = tk.Toplevel(self)
        aspect_window.title("Aspect Tagging")

        aspect_label = tk.Label(aspect_window, text=f"Select aspect for the word: '{word}'")
        aspect_label.pack(pady=10)

        aspect_var = tk.StringVar()
        aspect_var.set("Positive")  # Default aspect
        aspect_options = ["Positive", "Neutral", "Negative"]
        aspect_menu = ttk.Combobox(aspect_window, textvariable=aspect_var, values=aspect_options, state="readonly")
        aspect_menu.pack(pady=5)

        confirm_button = tk.Button(aspect_window, text="Confirm",
                                   command=lambda: self.confirm_aspect(word_start, word_end, aspect_var.get(),
                                                                       aspect_window))
        confirm_button.pack(pady=5)

    def confirm_aspect(self, word_start, word_end, aspect, aspect_window):
        color = {"Positive": "green", "Negative": "red", "Neutral": "gray"}.get(aspect, "black")
        self.text.tag_add(aspect, word_start, word_end)
        self.text.tag_configure(aspect, foreground=color)
        aspect_window.destroy()  # Close the aspect tagging window

import tkinter as tk
from tkinter import ttk


class AdditionalAspectTaggingApp(tk.Frame):
    def __init__(self, master, sentence, dct, id_num, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.sentence = sentence
        self.dct= dct
        self.id_num = id_num
        self.setup_widgets()

    def setup_widgets(self):
        input_frame = tk.Frame(self)
        input_frame.pack(fill=tk.X, padx=2, pady=5)

        self.text = tk.Text(input_frame, wrap=tk.WORD, height=3, width=70)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(input_frame, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.insert(tk.END, self.sentence + "\n\n")
        self.text.config(yscrollcommand=scrollbar.set)

        self.text.bind("<Double-Button-1>", self.tag_word)
        self.text.bind("<MouseWheel>", self.on_text_scroll)

    def tag_word(self, event):
        index = self.text.index(f"@{event.x},{event.y}")
        word_start = self.text.index(f"{index} wordstart")
        word_end = self.text.index(f"{index} wordend")
        word = self.text.get(word_start, word_end)
        self.master.master.assign_selected_row(word)



    def on_text_scroll(self, event):
        # Determine the direction of scrolling
        scroll_direction = -1 if event.delta > 0 else 1
        # Scroll the text widget
        self.text.yview_scroll(scroll_direction, "units")
        # Stop the event propagation to prevent scrolling the outer window
        return "break"


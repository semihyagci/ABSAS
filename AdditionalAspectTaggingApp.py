import tkinter as tk
import sys
import re

class AdditionalAspectTaggingApp(tk.Frame):
    def __init__(self, master, sentence, dct, id_num, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.sentence = sentence
        self.dct = dct
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

        if sys.platform.startswith('darwin'):  # MacOS
            self.text.bind("<Button-2>", self.on_right_click)
        elif sys.platform.startswith('win'):  # Windows
            self.text.bind("<Button-3>", self.on_right_click)

        self.text.bind("<MouseWheel>", self.on_text_scroll)

        self.text.config(state=tk.DISABLED)

    def tag_word(self, start_index, end_index):
        selected_text = self.text.get(start_index, end_index)

        cleaned_text = re.sub(r'[^\w\s]', '', selected_text)

        match = re.search(re.escape(cleaned_text), selected_text)

        if match:
            cleaned_start_idx = start_index + f'+{match.start()}c'
            cleaned_end_idx = cleaned_start_idx + f'+{len(cleaned_text)}c'

            self.master.master.assign_selected_row(cleaned_text, cleaned_start_idx, cleaned_end_idx)

    def on_right_click(self, event):
        index = self.text.index(f"@{event.x},{event.y}")
        start_index = self.text.index("sel.first")
        end_index = self.text.index("sel.last")
        if start_index and end_index:
            self.tag_word(start_index, end_index)

    def on_text_scroll(self, event):
        scroll_direction = -1 if event.delta > 0 else 1
        self.text.yview_scroll(scroll_direction, "units")
        return "break"
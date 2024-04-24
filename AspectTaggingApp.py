import tkinter as tk
from tkinter import ttk



class AspectTaggingApp(tk.Frame):
    def __init__(self, master, sentence, dct, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.sentence = sentence
        self.setup_widgets()
        self.dct = dct
        x=str(self.sentence)
        self.words=x.split()


    def setup_widgets(self):
        input_frame = tk.Frame(self)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.text = tk.Text(input_frame, wrap=tk.WORD, height=10, width=70)  # Adjust height and width as needed
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text.bind("<Double-Button-1>", self.tag_word)
        # Scrollbar for the text widget
        scrollbar = tk.Scrollbar(input_frame, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scrollbar.set)

        self.text.insert(tk.END, self.sentence + "\n\n")
        self.text.config(state=tk.DISABLED)

        # Bind MouseWheel event to the inner text widget
        self.text.bind("<MouseWheel>", self.on_text_scroll)

    def on_text_scroll(self, event):
        # Determine the direction of scrolling
        scroll_direction = -1 if event.delta > 0 else 1
        # Scroll the text widget
        self.text.yview_scroll(scroll_direction, "units")
        # Stop the event propagation to prevent scrolling the outer window
        return "break"

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
        word = self.text.get(word_start, word_end)

        print("word: ", word, " aspect value: ", aspect)
        aspect_window.destroy()  # Close the aspect tagging window

import sys
import tkinter as tk
from tkinter import ttk
import re

class AspectTaggingApp(tk.Frame):
    def __init__(self, master, sentence, dct, id_num, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.sentence = sentence
        self.dct = dct
        self.id_num = id_num
        self.setup_widgets()

    def setup_widgets(self):
        input_frame = tk.Frame(self)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.text = tk.Text(input_frame, wrap=tk.WORD, height=10, width=70)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(input_frame, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scrollbar.set)


        if sys.platform.startswith('darwin'):  # MacOS
            self.text.bind("<Button-2>", self.on_right_click)
        elif sys.platform.startswith('win'):  # Windows
            self.text.bind("<Button-3>", self.on_right_click)

        # Bind mouse wheel scroll event
        self.text.bind("<MouseWheel>", self.on_text_scroll)

        # Pre-populate the text and apply aspects
        self.prepopulate_text_with_aspects()

    def calculate_overall_sentiment(self):
        # Count occurrences of each aspect
        sentiment_counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
        for _, aspect in self.dct['list']:
            sentiment_counts[aspect] += 1

        # Determine the overall aspect based on counts
        overall_sentiment = 'Neutral'  # Default overall aspect
        if sentiment_counts['Positive'] > sentiment_counts['Negative']:
            overall_sentiment = 'Positive'
        elif sentiment_counts['Negative'] > sentiment_counts['Positive']:
            overall_sentiment = 'Negative'

        return overall_sentiment

    def prepopulate_text_with_aspects(self):
        self.text.insert(tk.END, self.sentence + "\n\n")
        color = {"Positive": "green", "Negative": "red", "Neutral": "gray"}

        # Iterate through the list of aspects and apply them
        for aspect_data in self.dct['list']:
            unique_id, aspect = aspect_data
            start_idx, end_idx = unique_id.split(":")
            start = f"1.{start_idx}"
            end = f"1.{end_idx}"

            self.text.tag_add(aspect, start, end)
            self.text.tag_configure(aspect, foreground=color.get(aspect, "black"))

        self.text.config(state=tk.DISABLED)

    def on_text_scroll(self, event):
        # Determine the direction of scrolling
        scroll_direction = -1 if event.delta > 0 else 1
        # Scroll the text widget
        self.text.yview_scroll(scroll_direction, "units")
        # Stop the event propagation to prevent scrolling the outer window
        return "break"

    def on_right_click(self,event):
        start_index = self.text.index("sel.first")
        end_index = self.text.index("sel.last")
        if start_index and end_index:
            self.tag_word_sequence(start_index, end_index)

    def tag_word_sequence(self, start_index, end_index):
        selected_text = self.text.get(start_index, end_index)

        cleaned_text = re.sub(r'[^\w\s]', '', selected_text)

        match = re.search(re.escape(cleaned_text), selected_text)

        if match:
            cleaned_start_idx = start_index + f'+{match.start()}c'
            cleaned_end_idx = cleaned_start_idx + f'+{len(cleaned_text)}c'

            self.open_aspect_window(cleaned_start_idx, cleaned_end_idx, cleaned_text)

    def open_aspect_window(self, start_index, end_index, word):
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
                                   command=lambda: self.confirm_aspect(start_index, end_index, aspect_var.get(),
                                                                       aspect_window))
        confirm_button.pack(pady=5)

    def update_overall_sentiment(self):
        overall_sentiment = self.calculate_overall_sentiment()
        self.dct['overall'] = overall_sentiment
        #CALLBACK FUNCTION FOR OVERALL SENTIMENT VALUE
        self.master.update_overall_sentiment_dropdown(overall_sentiment)

    def confirm_aspect(self, word_start, word_end, aspect, aspect_window):
        # Define aspect colors
        color = {"Positive": "green", "Negative": "red", "Neutral": "gray"}

        # Remove any existing aspect tags from this word
        for tag in self.text.tag_names():
            if tag in color:
                self.text.tag_remove(tag, word_start, word_end)

        # Apply the new aspect and configure its appearance
        self.text.tag_add(aspect, word_start, word_end)
        self.text.tag_configure(aspect, foreground=color.get(aspect, "black"))

        # Optionally, save the word and aspect to the dictionary (shown here for completeness)
        word = self.text.get(word_start, word_end)
        unique_id = (word_start.split(".")[1]) + ":" + word_end.split(".")[1]

        for i, entry in enumerate(self.dct['list']):
            if isinstance(entry, tuple):
                self.dct['list'][i] = list(entry)
        updated = False
        for entry in self.dct["list"]:
            if entry[0] == unique_id:  # Check if the unique ID is already in the list
                entry[1] = aspect  # Update the aspect
                updated = True
                break
        if not updated:
            self.dct["list"].append([unique_id, aspect])

        self.update_overall_sentiment()

        aspect_window.destroy()



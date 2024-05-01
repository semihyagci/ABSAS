import csv
import sys
import tkinter as tk
from tkinter import filedialog
from pyabsa import ATEPCCheckpointManager
from Template import Template
import ast
from global_dict_list import global_dict_list
from afinn import Afinn
from sentence_splitter import SentenceSplitter

global_filename = ""


def analyze_sentiment(sentence):
    score = afinn.score(sentence)
    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment


def extract_aspects(sentence,aspect_extractor):
    result = aspect_extractor.extract_aspect(inference_source=[sentence], pred_sentiment=True)

    aspects = result[0]['aspect']
    sentiments = result[0]['sentiment']

    word_indices_sentiment_sentence = []

    for aspect, sentiment in zip(aspects, sentiments):
        index = sentence.find(aspect)

        while index != -1:
            end_index = index + len(aspect)

            unique_id = f"{index}:{end_index}"

            if (index == 0 or not sentence[index - 1].isalpha()) and (end_index == len(sentence) or not sentence[end_index].isalpha()):
                word_indices_sentiment_sentence.append([unique_id,aspect, sentiment])

            index = sentence.find(aspect, index + 1)

    return word_indices_sentiment_sentence

def import_file():
    global global_filename
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(tk.END, file_path)

        global_filename = file_path


def load_dataset():
    file_path = file_path_entry.get()
    if file_path:
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                dataset = file.read()
        elif file_path.endswith('.csv'):
            with open(file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                dataset = ''
                for row in reader:
                    dataset += row['sentence'] + '\n'  # Concatenate sentences from CSV
        else:
            print("Unsupported file format.")
            return
    else:
        dataset = text.get('1.0', tk.END)

    window_width = root.winfo_width()
    window_height = root.winfo_height()

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry(f"{window_width}x{window_height}")

    loading_label = tk.Label(root, text="Loading dataset...")
    loading_label.pack()

    root.after(500, lambda: dataset_loaded(loading_label, dataset))


def dataset_loaded(loading_label, dataset):
    loading_label.config(text="Dataset loaded successfully!")

    spacer_label = tk.Label(root, text="")
    spacer_label.pack(pady=20)

    preference_label = tk.Label(root,
                                text="Do you want to highlight your own aspects? (If you say no, our ABSA method will find all of the aspects.)")
    preference_label.pack()

    preference_var = tk.StringVar(value="No")
    radio_frame = tk.Frame(root)
    radio_frame.pack()

    own_aspects_radio = tk.Radiobutton(radio_frame, text="Yes", variable=preference_var, value="Yes")
    own_aspects_radio.pack(side=tk.LEFT, padx=10)

    recommendation_system_radio = tk.Radiobutton(radio_frame, text="No", variable=preference_var, value="No")
    recommendation_system_radio.pack(side=tk.LEFT, padx=10)

    splitter = SentenceSplitter(language='en')
    sentences = splitter.split(text=dataset)

    confirm_button = tk.Button(root, text="Confirm", command=lambda: confirm_choice(preference_var.get(), sentences))
    confirm_button.pack()


def parse_list(list_str):
    if not list_str.strip():
        return []
    else:
        list_data = ast.literal_eval(list_str)
        return list_data


def read_existing_csv(file_path):
    data_dict = {}

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            sentence_id = int(row['sentenceID'])
            sentence = row['sentence']
            list_data = parse_list(row['list'])
            overall_sentiment = row['overall']
            additional_aspect_list = parse_list(row['additional_aspect_list'])
            afinn_score = row['sentence_afinn_score']

            data_dict[sentence_id] = {'sentence': sentence, 'list': list_data, 'overall': overall_sentiment,
                                      'additional_aspect_list': additional_aspect_list, 'sentence_afinn_score':afinn_score}

    formatted_data = [{'sentenceID': k, 'sentence': v['sentence'], 'list': v['list'], 'overall': v['overall'],
                       'additional_aspect_list': v['additional_aspect_list'], 'sentence_afinn_score': v['sentence_afinn_score'] } for k, v in data_dict.items()]
    return formatted_data


def confirm_choice(choice, sentences):
    global global_filename
    if choice == "Yes":
        for widget in root.winfo_children():
            widget.destroy()
        root.geometry("1200x700")

        canvas = tk.Canvas(root)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        save_frame = tk.Frame(root, bg="#CCCCCC")
        save_frame.pack(side="bottom", fill="x", padx=10, pady=5)

        save_button = tk.Button(save_frame, text="Save", command=save_data)
        save_button.pack(pady=5, ipadx=20, ipady=10)

        save_frame.place(relx=0.5, rely=1.0, anchor="s", relwidth=1.0)

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_configure)

        if global_filename.endswith('.csv'):
            mylist = read_existing_csv(global_filename)
            for i in range(len(mylist)):
                if i == len(mylist) - 1:
                    bottom_padding = 60
                else:
                    bottom_padding = 5

                global_dict_list.append(mylist[i])
                template = Template(frame, id_num=i + 1, text_list=mylist[i]['sentence'], dct=mylist[i])
                template.grid(row=i + 1, column=0, columnspan=3, padx=5, pady=(30, bottom_padding), sticky="ew")
        else:
            for idx, input_text in enumerate(sentences):
                if idx == len(sentences) - 1:
                    bottom_padding = 60
                else:
                    bottom_padding = 5

                dct = {
                    "sentenceID": idx + 1,
                    "sentence": input_text,
                    "list": [],
                    "overall": "Neutral",
                    "additional_aspect_list": [],
                    "sentence_afinn_score": analyze_sentiment(input_text)
                }
                global_dict_list.append(dct)
                template = Template(frame, id_num=idx + 1, text_list=input_text, dct=dct)
                template.grid(row=idx + 1, column=0, columnspan=3, padx=5, pady=(30, bottom_padding), sticky="ew")

        root.bind("<MouseWheel>", lambda event: scroll_canvas(event, canvas))
    else:
        aspect_extractor = ATEPCCheckpointManager.get_aspect_extractor(checkpoint='english', auto_device=True)

        for widget in root.winfo_children():
            widget.destroy()
        root.geometry("1200x700")

        canvas = tk.Canvas(root)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        save_frame = tk.Frame(root, bg="#CCCCCC")
        save_frame.pack(side="bottom", fill="x", padx=10, pady=5)

        save_button = tk.Button(save_frame, text="Save", command=save_data)
        save_button.pack(pady=5, ipadx=20, ipady=10)

        save_frame.place(relx=0.5, rely=1.0, anchor="s", relwidth=1.0)

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_configure)

        if global_filename.endswith('.csv'):
            mylist = read_existing_csv(global_filename)
            for i in range(len(mylist)):
                if i == len(mylist) - 1:
                    bottom_padding = 60
                else:
                    bottom_padding = 5

                global_dict_list.append(mylist[i])
                template = Template(frame, id_num=i + 1, text_list=mylist[i]['sentence'], dct=mylist[i])
                template.grid(row=i + 1, column=0, columnspan=3, padx=5, pady=(30, bottom_padding), sticky="ew")
        else:
            for idx, input_text in enumerate(sentences):
                if idx == len(sentences) - 1:
                    bottom_padding = 60
                else:
                    bottom_padding = 5

                dct = {
                    "sentenceID": idx + 1,
                    "sentence": input_text,
                    "list": extract_aspects(input_text,aspect_extractor),
                    "overall": "Neutral",
                    "additional_aspect_list": [],
                    "sentence_afinn_score": analyze_sentiment(input_text)
                }
                global_dict_list.append(dct)
                template = Template(frame, id_num=idx + 1, text_list=input_text, dct=dct)
                template.grid(row=idx + 1, column=0, columnspan=3, padx=5, pady=(30, bottom_padding), sticky="ew")

        root.bind("<MouseWheel>", lambda event: scroll_canvas(event, canvas))


def scroll_canvas(event, canvas):
    if event.delta > 0:
        canvas.yview_scroll(-1, "units")
    else:
        canvas.yview_scroll(1, "units")


def save_data():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        print("Save cancelled.")
        return

    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['sentenceID', 'sentence', 'list', 'overall', 'additional_aspect_list','sentence_afinn_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in global_dict_list:
            writer.writerow(item)
    sys.exit()


def create_scrollable_text(parent):
    text_scroll = tk.Scrollbar(parent, orient=tk.VERTICAL)
    text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    horizontal_scroll = tk.Scrollbar(parent, orient=tk.HORIZONTAL)
    horizontal_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    text_widget = tk.Text(parent, wrap=tk.NONE, yscrollcommand=text_scroll.set, xscrollcommand=horizontal_scroll.set)
    text_widget.pack(expand=True, fill=tk.BOTH)

    text_scroll.config(command=text_widget.yview)
    horizontal_scroll.config(command=text_widget.xview)

    return text_widget


root = tk.Tk()
root.title("Dataset Loader")

afinn = Afinn()

text_frame = tk.Frame(root)
text_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

text_label = tk.Label(text_frame, text="Please enter your data into text area or upload it via using file:")
text_label.pack()

text = create_scrollable_text(text_frame)

file_frame = tk.Frame(root)
file_frame.pack(pady=5)

file_label = tk.Label(file_frame, text="File Path:")
file_label.grid(row=0, column=0)

file_path_entry = tk.Entry(file_frame, width=40)
file_path_entry.grid(row=0, column=1)

browse_button = tk.Button(file_frame, text="Browse Files", command=import_file)
browse_button.grid(row=0, column=2)

load_button = tk.Button(root, text="Load Dataset", command=load_dataset)
load_button.pack(pady=10)

root.mainloop()
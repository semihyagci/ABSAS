import csv
import sys
import tkinter as tk
from tkinter import filedialog
from sentence_splitter import SentenceSplitter
from Template import Template
import ast
from global_dict_list import global_dict_list
import os

global_filename = ""


# Import TXT or CSV files
def import_file():
    global global_filename
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(tk.END, file_path)

        # Store the filename in the global variable
        global_filename = os.path.basename(file_path)
        print("Uploaded file:", global_filename)


# Load dataset from TXT or CSV
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


# After dataset is loaded, present options to user
def dataset_loaded(loading_label, dataset):
    loading_label.config(text="Dataset loaded successfully!")

    spacer_label = tk.Label(root, text="")
    spacer_label.pack(pady=20)

    preference_label = tk.Label(root,
                                text="Do you want to highlight your own aspects or use our recommendation system?")
    preference_label.pack()

    preference_var = tk.StringVar(value="No")  # Default choice is "No"
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

    print("Divided sentences: ", sentences)


# Confirm user choice and proceed accordingly

def parse_list(list_str):
    if not list_str.strip():
        return []
    else:
        list_data = ast.literal_eval(list_str)  # Safely evaluate the string as a Python expression
        return [(start, sentiment) for start, sentiment in list_data]


def read_existing_csv(file_path):
    data_dict = {}

    with open(file_path, 'r') as csvfile:
        # Create a CSV reader object
        reader = csv.DictReader(csvfile)

        # Iterate over each row in the CSV file
        for row in reader:
            # Extract data from the row
            sentence_id = int(row['sentenceID'])
            sentence = row['sentence']
            list_data = parse_list(row['list'])

            # Store the data in the dictionary
            data_dict[sentence_id] = {'sentence': sentence, 'list': list_data}

    formatted_data = [{'sentenceID': k, 'sentence': v['sentence'], 'list': v['list']} for k, v in data_dict.items()]
    return formatted_data


def confirm_choice(choice, sentences):
    global global_filename
    if choice == "Yes":
        print("User chose to highlight their own aspects.")
        column_names = ["ID", "Text", "Overall Aspect"]
        for widget in root.winfo_children():
            widget.destroy()
        root.geometry("750x500")

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

        for col, name in enumerate(column_names):
            label = tk.Label(frame, text=name)
            label.grid(row=0, column=col, padx=5, pady=5)

        if global_filename.endswith('.csv'):
            mylist = read_existing_csv(global_filename)
            for i in range(len(mylist)):
                global_dict_list.append(mylist[i])
                template = Template(frame, id_num=i + 1, text_list=mylist[i]['sentence'], dct=mylist[i])
                template.grid(row=i + 1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        else:
            for idx, input_text in enumerate(sentences):
                dct = {
                    "sentenceID": idx + 1,
                    "sentence": input_text,
                    "list": [],
                }
                global_dict_list.append(dct)
                template = Template(frame, id_num=idx + 1, text_list=input_text, dct=dct)
                template.grid(row=idx + 1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

            root.bind("<MouseWheel>", lambda event: scroll_canvas(event, canvas))
    else:
        print("User chose to use the recommendation system.")
        # Handle recommendation system


# Scroll canvas based on mouse wheel events
def scroll_canvas(event, canvas):
    if event.delta > 0:
        canvas.yview_scroll(-1, "units")
    else:
        canvas.yview_scroll(1, "units")


# Save data to file
def save_data():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Ask user for file path
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        print("Save cancelled.")
        return

    # Write data to the chosen file path
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['sentenceID', 'sentence', 'list']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in global_dict_list:
            writer.writerow(item)

    print("Data saved successfully.")
    sys.exit()


# Create scrollable text widget
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


# Main Tkinter window
root = tk.Tk()
root.title("Dataset Loader")

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

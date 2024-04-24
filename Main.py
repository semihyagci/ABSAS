import tkinter as tk
from tkinter import filedialog
from sentence_splitter import SentenceSplitter
from Template import Template

#TXT IMPORT METHODU
def import_txt():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(tk.END, file_path)

#NEYLE IMPORT ETMİŞ ONU KONTROL EDİP AKSİYON ALIYO
def load_dataset():
    if file_path_entry.get():
        with open(file_path_entry.get(), 'r') as file:
            dataset = file.read()
    else:
        dataset = text.get('1.0', tk.END)

    window_width = root.winfo_width()
    window_height = root.winfo_height()

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry(f"{window_width}x{window_height}")

    loading_label = tk.Label(root, text="Loading dataset...")
    loading_label.pack()

    root.after(3000, lambda: dataset_loaded(loading_label,dataset))


#DATASET YÜKLENDİKTEN SONRA SORU KISMI
def dataset_loaded(loading_label,dataset):
    loading_label.config(text="Dataset loaded successfully!")
    print("Loaded dataset:", dataset)

    spacer_label = tk.Label(root, text="")
    spacer_label.pack(pady=20)

   #HIGHLIGHTING CHOICE RADIO BUTTON KISMI
    preference_label = tk.Label(root, text="Do you want to highlight your own aspects or use our recommendation system?")
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

    confirm_button = tk.Button(root, text="Confirm", command=lambda: confirm_choice(preference_var.get(),sentences))
    confirm_button.pack()

    print("Divided sentences: ", sentences)


def confirm_choice(choice,sentences):
    if choice == "Yes":
        print("User chose to highlight their own aspects.")
        column_names = ["ID", "Text", "Overall Aspect"]
        for widget in root.winfo_children():
            widget.destroy()
        root.geometry("750x500")

        for col, name in enumerate(column_names):
            label = tk.Label(root, text=name)
            label.grid(row=0, column=col, padx=5, pady=5)
        for idx, input_text in enumerate(sentences):
            template = Template(root, id_num=idx + 1, text_list=input_text)
            template.grid(row=idx + 1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
    else:
        print("User chose to use the recommendation system.")
        # Handle recommendation system


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

browse_button = tk.Button(file_frame, text="Browse Files", command=import_txt)
browse_button.grid(row=0, column=2)

load_button = tk.Button(root, text="Load Dataset", command=load_dataset)
load_button.pack(pady=10)

root.mainloop()
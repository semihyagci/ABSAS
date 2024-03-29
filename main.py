import tkinter as tk
from tkinter import filedialog
from sentence_splitter import SentenceSplitter

def import_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(tk.END, file_path)


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


def dataset_loaded(loading_label,dataset):
    loading_label.config(text="Dataset loaded successfully!")
    print("Loaded dataset:", dataset)
    splitter = SentenceSplitter(language='en')
    sentences = splitter.split(text=dataset)
    print("Divided sentences: ", sentences)


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

browse_button = tk.Button(file_frame, text="Browse Files", command=import_csv)
browse_button.grid(row=0, column=2)

load_button = tk.Button(root, text="Load Dataset", command=load_dataset)
load_button.pack(pady=10)

root.mainloop()

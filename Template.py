import tkinter as tk

class Template(tk.Frame):
    def __init__(self, master, id_num, text_list, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.id_num = id_num
        self.text_list = text_list
        self.create_widgets()

    def create_widgets(self):
        # ID Label
        id_label = tk.Label(self, text=f"ID: {self.id_num}")
        id_label.grid(row=0, column=0, padx=5, pady=5)

        # Text Widget
        text_widget = tk.Text(self, height=4, width=40)
        text_widget.insert(tk.END, f"{self.text_list}\n")
        text_widget.grid(row=0, column=1, padx=5, pady=5)

        # Overall Aspect Dropdown
        options = ["Positive", "Negative", "Neutral"]
        self.aspect_var = tk.StringVar(self)
        self.aspect_var.set(options[2])  # Default value
        dropdown = tk.OptionMenu(self, self.aspect_var, *options)
        dropdown.grid(row=0, column=2, padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()

    # Column Names
    column_names = ["ID", "Text", "Overall Aspect"]

    # Sample data
    input_text = ["Text A", "Text B", "Text C"]

    # Display column names
    for col, name in enumerate(column_names):
        label = tk.Label(root, text=name)
        label.grid(row=0, column=col, padx=5, pady=5)

    for idx, input_text in enumerate(input_text):
        template = Template(root, id_num=idx + 1, text_list=input_text)
        template.grid(row=idx + 1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

    root.mainloop()

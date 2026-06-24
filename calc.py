import tkinter as tk


def set_entry_text(text):
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, text)
    entry.config(state="readonly")


def add_character(char):
    current = entry.get()
    set_entry_text(current + char)


def calculate():
    expression = entry.get()
    try:
        result = str(eval(expression))
        set_entry_text(result)
    except Exception:
        set_entry_text("Error")


def clear():
    set_entry_text("")


root = tk.Tk()
root.title("Calculadora")
root.geometry("320x420")
root.resizable(False, False)

for i in range(4):
    root.grid_columnconfigure(i, weight=1, uniform="column")
for i in range(6):
    root.grid_rowconfigure(i, weight=1)

entry = tk.Entry(root, font=("Arial", 20), borderwidth=2, relief="ridge", justify="right", state="readonly")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10, sticky="nsew")

buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
]

for (text, row, col) in buttons:
    if text == '=':
        action = calculate
    else:
        action = lambda value=text: add_character(value)
    btn = tk.Button(root, text=text, font=("Arial", 18), command=action)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

clear_button = tk.Button(root, text='C', font=("Arial", 18), command=clear)
clear_button.grid(row=5, column=0, columnspan=4, padx=5, pady=(0,10), sticky="nsew")

root.mainloop()

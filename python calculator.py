import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.expression = ""

        self.create_widgets()

    def create_widgets(self):
        self.display = tk.Entry(self.root, font=("Arial", 20), bd=10, insertwidth=2, width=14, borderwidth=4)
        self.display.grid(row=0, column=0, columnspan=4)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            action = lambda x=button: self.click_event(x)
            b = tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=action)
            b.grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        clear_button = tk.Button(self.root, text='C', padx=20, pady=20, font=("Arial", 18), command=self.clear_display)
        clear_button.grid(row=row_val, column=0, columnspan=4, sticky="nsew")

    def click_event(self, key):
        if key == "=":
            try:
                self.expression = str(eval(self.expression))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, self.expression)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid Expression\n{e}")
                self.clear_display()
        else:
            self.expression += str(key)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)

    def clear_display(self):
        self.expression = ""
        self.display.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()

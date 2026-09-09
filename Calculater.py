import tkinter as tk
import ast
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Small Calculator")
        self.root.geometry("320x420")
        self.root.resizable(False, False)

        self.expression = ""

        # Display
        self.display = tk.Entry(root, font=("Arial", 24), justify="right", bd=10)
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Buttons
        buttons = [
            ("C", 1, 0), ("⌫", 1, 1), ("%", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("=", 5, 2, 2),
        ]

        for button in buttons:
            if len(button) == 3:
                text, row, col = button
                span = 1
            else:
                text, row, col, span = button

            btn = tk.Button(root, text=text, font=("Arial", 18), command=lambda value=text: self.on_click(value), width=5, height=2)
            btn.grid(row=row, column=col, columnspan=span, padx=5, pady=5, sticky="nsew")

        # Make grid stretch
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        for i in range(6):
            root.grid_rowconfigure(i, weight=1)

    def on_click(self, value):
        if value == "=":
            self.calculate()
        elif value == "C":
            self.expression = ""
            self.display.delete(0, tk.END)
        elif value == "⌫":
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
        elif value == "%":
            self.expression += "/100"
            self.display.insert(tk.END, value)
        else:
            self.expression += value
            self.display.insert(tk.END, value)

    def calculate(self):
        try:
            result = self.evaluate_expression(self.expression)
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.expression = str(result)
        except Exception:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            self.expression = ""

    def evaluate_expression(self, expression):
        # replace python-friendly syntax
        cleaned = expression.replace("×", "*").replace("÷", "/").replace("−", "-")
        allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Add, ast.Sub, ast.Mult, ast.Div,
                         ast.Pow, ast.USub, ast.UAdd, ast.Mod, ast.FloorDiv, ast.Num)

        tree = ast.parse(cleaned, mode="eval")
        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                raise ValueError("Invalid expression")

        result = eval(compile(tree, "<calculator>", "eval"), {"__builtins__": {}}, {"math": math})
        if isinstance(result, float):
            if result.is_integer():
                return int(result)
            return round(result, 8)
        return result

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

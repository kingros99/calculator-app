import tkinter as tk
import ast
import math
from collections import deque


class CalculationHistory:
    def __init__(self, max_size=5):
        self.max_size = max_size
        self._queue = deque(maxlen=max_size)

    def add(self, expression, result):
        self._queue.append({"expression": expression, "result": result})

    def clear(self):
        self._queue.clear()

    def get_history(self):
        return list(self._queue)


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Small Calculator")
        self.root.geometry("320x480")
        self.root.resizable(False, False)

        self.expression = ""
        self.history = CalculationHistory(max_size=5)

        # Display
        self.display = tk.Entry(root, font=("Arial", 24), justify="right", bd=10)
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # History list
        history_label = tk.Label(root, text="Last 5 calculations", font=("Arial", 10))
        history_label.grid(row=1, column=0, columnspan=4, padx=10, pady=(0, 5), sticky="w")

        self.history_list = tk.Listbox(root, height=5, font=("Arial", 11), justify="left")
        self.history_list.grid(row=2, column=0, columnspan=4, padx=10, pady=(0, 8), sticky="nsew")

        # Buttons
        buttons = [
            ("C", 3, 0), ("⌫", 3, 1), ("%", 3, 2), ("/", 3, 3),
            ("7", 4, 0), ("8", 4, 1), ("9", 4, 2), ("*", 4, 3),
            ("4", 5, 0), ("5", 5, 1), ("6", 5, 2), ("-", 5, 3),
            ("1", 6, 0), ("2", 6, 1), ("3", 6, 2), ("+", 6, 3),
            ("0", 7, 0), (".", 7, 1), ("=", 7, 2, 2),
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
        for i in range(8):
            root.grid_rowconfigure(i, weight=1)

        self.refresh_history_list()

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

    def refresh_history_list(self):
        self.history_list.delete(0, tk.END)
        entries = self.history.get_history()

        if not entries:
            self.history_list.insert(tk.END, "No calculations yet")
            return

        for item in entries:
            expression = item["expression"]
            result = item["result"]
            self.history_list.insert(tk.END, f"{expression} = {result}")

    def calculate(self):
        try:
            expression = self.expression
            result = self.evaluate_expression(expression)
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))

            self.history.add(expression, result)
            self.refresh_history_list()

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

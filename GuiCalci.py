import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, integrate, diff, solve, Matrix, Eq, I
import requests
import scipy.stats as stats
import seaborn as sns
import datetime
import random
import math
import json
from sklearn.linear_model import LinearRegression
from fractions import Fraction
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class UltimateCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ultimate Advanced Calculator")
        self.geometry("900x600")
        self.resizable(True, True)

        self.expression = ""
        self.result_var = tk.StringVar()
        self.history = []
        self.custom_functions = {}
        self.create_widgets()

    def create_widgets(self):
        """Creates the main UI components for the calculator."""
        # Main Frame for layout
        main_frame = tk.Frame(self, bg="#2E3A59")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Entry display for results
        entry_display_frame = tk.Frame(main_frame, bg="#2E3A59")
        entry_display_frame.pack(fill=tk.BOTH, padx=10, pady=15)

        # Entry for expressions
        entry = tk.Entry(entry_display_frame, textvariable=self.result_var, font=("Arial", 36), bd=10, bg="#FFFFFF", fg="#000000", justify='right')
        entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Button Frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.BOTH, expand=True)

        # Button configuration
        button_width = 8
        button_height = 3
        buttons = [
            '7', '8', '9', '/', 'Solve', 'Batch',
            '4', '5', '6', '*', 'Matrix',
            '1', '2', '3', '-', 'Prime',
            '0', '.', '=', '+', 'FFT',
            'C', 'Stats', 'Integrate', 'Differentiate', 'Geometry',
            'Rand Int', 'Rand Float', 'Bin->Dec', 'Dec->Bin', 'Unit Conv',
            'Roman->Int', 'Int->Roman', 'Base64 Encode', 'Base64 Decode', 'Physics',
            'Graph', 'Multi-Graph', 'Clear History', 'History', 'Quit',
            'Memory Store', 'Memory Recall', 'Dark Mode', 'Light Mode', 'Clear All',
            'Hypothesis Test', 'ANOVA', 'Chi-Square', 'Date Calculator', 
            'Currency Converter', 'Fraction Operations', 'Complex Numbers',
            '3D Graph', 'Scientific Functions', 'Linear Algebra', 'Solve DE', 
            'Data Import', 'Data Export', 'Correlation', 'Logarithm', 
            'Exponentiation', 'Simple Interest', 'Compound Interest', 
            'Standard Deviation', 'Variance', 'Swap', 'Custom Function'
        ]

        row_val = 0
        col_val = 0

        for button in buttons:
            btn = tk.Button(
                button_frame, text=button,
                padx=button_width, pady=button_height,
                font=("Arial", 12, 'bold'), width=10, height=3,
                command=lambda b=button: self.on_button_click(b),
                relief="solid", bd=2, bg="#5A7D9E", fg="white", activebackground="#4C6784"
            )
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=5, pady=5)

            # Bind button hover effects
            btn.bind("<Enter>", lambda e, btn=btn: btn.config(bg="#4C6784"))
            btn.bind("<Leave>", lambda e, btn=btn: btn.config(bg="#5A7D9E"))
            btn.bind("<ButtonPress>", lambda e, btn=btn: btn.config(relief="sunken"))
            btn.bind("<ButtonRelease>", lambda e, btn=btn: btn.config(relief="raised"))

            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1
        
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(5):
            button_frame.grid_columnconfigure(j, weight=1)

    def on_button_click(self, char):
        """Handles button click events depending on the button character."""
        if char == '=':
            self.calculate_result()
        elif char == 'C':
            self.clear_display()
        elif char == 'Batch':
            self.batch_operations()
        elif char == 'Custom Function':
            self.add_custom_function()
        elif char == 'Clear History':
            self.clear_history()
        elif char == 'Data Import':
            self.data_import()
        elif char == 'Data Export':
            self.data_export()
        elif char == 'Correlation':
            self.calculate_correlation()
        elif char == 'Logarithm':
            self.calculate_logarithm()
        elif char == 'Exponentiation':
            self.calculate_exponentiation()
        elif char == 'Simple Interest':
            self.calculate_simple_interest()
        elif char == 'Compound Interest':
            self.calculate_compound_interest()
        elif char == 'Standard Deviation':
            self.calculate_standard_deviation()
        elif char == 'Variance':
            self.calculate_variance()
        elif char == 'Swap':
            self.swap()
        elif char == 'Hypothesis Test':
            self.hypothesis_test()
        else:
            self.add_to_expression(char)

    def calculate_result(self):
        """Calculates the result of the current expression."""
        try:
            result = eval(self.expression, {"__builtins__": None}, self.custom_functions)  # Safe eval
            # Display result with padding for visibility
            formatted_result = f"{result:.4f}" if isinstance(result, (int, float)) else str(result)
            self.result_var.set(formatted_result)
            self.record_history(f"{self.expression} = {formatted_result}")
            self.expression = ""
        except Exception as e:
            self.result_var.set("Error")
            messagebox.showerror("Error", str(e))

    def add_to_expression(self, char):
        """Adds a character to the current expression."""
        self.expression += str(char)
        self.result_var.set(self.expression)

    def clear_display(self):
        """Clears the current expression."""
        self.expression = ""
        self.result_var.set("")

    def batch_operations(self):
        """Handles batch calculations."""
        batch_data = simpledialog.askstring("Batch Operations", "Enter expressions separated by semicolons:")
        if batch_data:
            results = []
            expressions = batch_data.split(';')
            for expr in expressions:
                try:
                    result = eval(expr, {"__builtins__": None}, self.custom_functions)
                    results.append(f"{expr} = {result}")
                except Exception as e:
                    results.append(f"Error in '{expr}': {e}")
            self.result_var.set("\n".join(results))
            self.record_history("\n".join(results))
    
    def add_custom_function(self):
        """Allows users to add a custom function."""
        func_name = simpledialog.askstring("Custom Function", "Enter function name (e.g., my_func):")
        func_body = simpledialog.askstring("Custom Function", "Enter function body (use x as input):")
        if func_name and func_body:
            self.custom_functions[func_name] = eval(f"lambda x: {func_body}")
            messagebox.showinfo("Success", f"Custom function '{func_name}' added!")

    def clear_history(self):
        """Clears the calculation history."""
        self.history.clear()
        messagebox.showinfo("History", "History cleared.")

    def record_history(self, entry):
        """Records an entry in the history."""
        self.history.append(entry)

    def calculate_correlation(self):
        """Calculates correlation between two datasets."""
        data_x = simpledialog.askstring("Correlation", "Enter first dataset (comma-separated):")
        data_y = simpledialog.askstring("Correlation", "Enter second dataset (comma-separated):")
        if data_x and data_y:
            x = np.array(list(map(float, data_x.split(','))))
            y = np.array(list(map(float, data_y.split(','))))
            correlation = np.corrcoef(x, y)[0, 1]
            self.result_var.set(f"Correlation Coefficient: {correlation:.4f}")
            self.record_history(f"Correlation: {correlation:.4f}")

    def calculate_logarithm(self):
        """Calculates the logarithm for a number."""
        number = simpledialog.askfloat("Logarithm", "Enter number:")
        base = simpledialog.askfloat("Logarithm", "Enter base (default is e):") or math.e
        if number is not None and base is not None:
            log_value = math.log(number, base)
            self.result_var.set(f"Log {base}({number}) = {log_value:.4f}")
            self.record_history(f"Log {base}({number}) = {log_value:.4f}")

    def calculate_exponentiation(self):
        """Calculates exponentiation for a number."""
        base = simpledialog.askfloat("Exponentiation", "Enter base:")
        exponent = simpledialog.askfloat("Exponentiation", "Enter exponent:")
        if base is not None and exponent is not None:
            result = base ** exponent
            self.result_var.set(f"{base}^{exponent} = {result:.4f}")
            self.record_history(f"{base}^{exponent} = {result:.4f}")

    def calculate_simple_interest(self):
        """Calculates simple interest."""
        principal = simpledialog.askfloat("Simple Interest", "Enter Principal:")
        rate = simpledialog.askfloat("Simple Interest", "Enter Rate (in %):")
        time = simpledialog.askfloat("Simple Interest", "Enter Time (in years):")
        if principal is not None and rate is not None and time is not None:
            interest = (principal * rate * time) / 100
            self.result_var.set(f"Simple Interest = {interest:.2f}")
            self.record_history(f"Simple Interest = {interest:.2f}")

    def calculate_compound_interest(self):
        """Calculates compound interest."""
        principal = simpledialog.askfloat("Compound Interest", "Enter Principal:")
        rate = simpledialog.askfloat("Compound Interest", "Enter Rate (in %):")
        time = simpledialog.askfloat("Compound Interest", "Enter Time (in years):")
        compound_frequency = simpledialog.askinteger("Compound Interest", "Enter Number of Years for Compounding (e.g. 12 for monthly):") or 1
        if principal is not None and rate is not None and time is not None:
            amount = principal * (1 + (rate / (compound_frequency * 100))) ** (compound_frequency * time)
            interest = amount - principal
            self.result_var.set(f"Compound Interest = {interest:.2f}")
            self.record_history(f"Compound Interest = {interest:.2f}")

    def calculate_standard_deviation(self):
        """Calculates standard deviation of a dataset."""
        data_input = simpledialog.askstring("Standard Deviation", "Enter numbers separated by commas:")
        if data_input:
            data = np.array(list(map(float, data_input.split(','))))
            std_dev = np.std(data)
            self.result_var.set(f"Standard Deviation = {std_dev:.4f}")
            self.record_history(f"Standard Deviation = {std_dev:.4f}")

    def calculate_variance(self):
        """Calculates variance of a dataset."""
        data_input = simpledialog.askstring("Variance", "Enter numbers separated by commas:")
        if data_input:
            data = np.array(list(map(float, data_input.split(','))))
            variance = np.var(data)
            self.result_var.set(f"Variance = {variance:.4f}")
            self.record_history(f"Variance = {variance:.4f}")

    def swap(self):
        """Swaps two numbers and displays the results."""
        num1 = simpledialog.askfloat("Swap", "Enter first number:")
        num2 = simpledialog.askfloat("Swap", "Enter second number:")
        if num1 is not None and num2 is not None:
            num1, num2 = num2, num1
            self.result_var.set(f"Swapped: num1 = {num1}, num2 = {num2}")
            self.record_history(f"Swapped: num1 = {num1}, num2 = {num2}")

    def data_import(self):
        """Import data from a CSV file."""
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if file_path:
            data = pd.read_csv(file_path)
            self.result_var.set(data.to_string(index=False))
            self.record_history(f"Imported data from {file_path}")

    def data_export(self):
        """Export data to a CSV file."""
        file_path = filedialog.asksaveasfilename(title="Save File", defaultextension=".csv", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if file_path:
            try:
                # Generating sample random data for demonstration
                data = np.random.rand(10, 2)  
                pd.DataFrame(data, columns=["Column1", "Column2"]).to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")

if __name__ == "__main__":
    app = UltimateCalculator()
    app.mainloop()
import tkinter as tk
from utils.bmi_calculator import BMICalculator
import pandas as pd

class SuggestionsTab:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.create_widgets()
    
    def create_widgets(self):
        """Create suggestions widgets"""
        content_frame = tk.Frame(self.parent)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.suggestion_text = tk.Text(content_frame, height=15, width=70, wrap='word')
        self.suggestion_text.pack(fill='both', expand=True)
        
        tk.Button(content_frame, text="Generate Suggestions", 
                 command=self.generate_suggestions).pack(pady=10)
    
    def generate_suggestions(self):
        """Generate health suggestions"""
        df = self.db_manager.get_dataframe()
        if df.empty:
            self.suggestion_text.delete('1.0', tk.END)
            self.suggestion_text.insert('1.0', "No data available. Please enter your health data first.")
            return
        
        latest = df.iloc[-1]
        bmi = latest['bmi']
        
        # Calculate weight trend
        weight_trend = 0
        if len(df) > 1:
            weight_trend = df['weight'].iloc[-1] - df['weight'].iloc[0]
        
        suggestions = BMICalculator.get_suggestions(bmi, weight_trend)
        
        # Format output
        output = "=== Health Suggestions ===\n\n"
        for i, suggestion in enumerate(suggestions, 1):
            output += f"{i}. {suggestion}\n"
        
        output += f"\nCurrent BMI: {bmi}\n"
        output += f"BMI Category: {BMICalculator.get_bmi_category(bmi).title()}\n"
        
        output += "\nRemember: These are general suggestions. Always consult healthcare professionals for personalized advice."
        
        self.suggestion_text.delete('1.0', tk.END)
        self.suggestion_text.insert('1.0', output)
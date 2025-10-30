import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class VisualizationTab:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.create_widgets()
    
    def create_widgets(self):
        """Create visualization widgets"""
        # Control frame
        control_frame = tk.Frame(self.parent)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="Show Weight Trend", 
                 command=self.plot_weight_trend).pack(side='left', padx=5)
        tk.Button(control_frame, text="Show BMI Chart", 
                 command=self.plot_bmi_chart).pack(side='left', padx=5)
        tk.Button(control_frame, text="Clear Charts", 
                 command=self.clear_charts).pack(side='left', padx=5)
        
        # Chart frame
        self.chart_frame = tk.Frame(self.parent)
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get data as DataFrame"""
        return self.db_manager.get_dataframe()
    
    def plot_weight_trend(self):
        """Plot weight trend chart"""
        df = self.get_dataframe()
        if df.empty:
            messagebox.showinfo("Info", "No data available for visualization")
            return
        
        self.clear_charts()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df['date'], df['weight'], marker='o', linewidth=2, markersize=6, color='#2196F3')
        ax.set_title('Weight Trend Over Time', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Weight (kg)')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        self.embed_chart(fig)
    
    def plot_bmi_chart(self):
        """Plot BMI chart with categories"""
        df = self.get_dataframe()
        if df.empty:
            messagebox.showinfo("Info", "No data available for visualization")
            return
        
        self.clear_charts()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        
        # BMI trend
        ax1.plot(df['date'], df['bmi'], marker='s', color='orange', linewidth=2)
        ax1.set_title('BMI Trend')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('BMI')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # BMI categories
        categories = ['Underweight', 'Normal', 'Overweight', 'Obese']
        bmi_values = [
            len(df[df['bmi'] < 18.5]), 
            len(df[(df['bmi'] >= 18.5) & (df['bmi'] < 25)]),
            len(df[(df['bmi'] >= 25) & (df['bmi'] < 30)]),
            len(df[df['bmi'] >= 30])
        ]
        
        colors = ['lightblue', 'lightgreen', 'yellow', 'lightcoral']
        ax2.pie(bmi_values, labels=categories, autopct='%1.1f%%', colors=colors)
        ax2.set_title('BMI Distribution')
        
        plt.tight_layout()
        self.embed_chart(fig)
    
    def embed_chart(self, fig):
        """Embed matplotlib chart in tkinter"""
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        self.current_canvas = canvas
    
    def clear_charts(self):
        """Clear all charts"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
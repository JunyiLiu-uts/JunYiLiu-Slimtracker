import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from models.health_data import HealthRecord
from utils.validators import validate_weight, validate_height

class DataTab:
    def __init__(self, parent, db_manager, refresh_callback: Callable):
        self.parent = parent
        self.db_manager = db_manager
        self.refresh_callback = refresh_callback
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create data entry widgets"""
        # Title
        title_label = tk.Label(self.parent, text="Enter Your Health Data", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.parent)
        input_frame.pack(pady=20)
        
        # Weight input
        tk.Label(input_frame, text="Weight (kg):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.weight_entry = tk.Entry(input_frame, width=20)
        self.weight_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Height input
        tk.Label(input_frame, text="Height (m):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.height_entry = tk.Entry(input_frame, width=20)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Notes input
        tk.Label(input_frame, text="Notes:").grid(row=2, column=0, padx=5, pady=5, sticky='ne')
        self.notes_entry = tk.Text(input_frame, width=30, height=4)
        self.notes_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.parent)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Save Data", command=self.save_data).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear All", command=self.clear_data).pack(side='left', padx=5)
        
        # Data display
        self.create_data_display()
    
    def create_data_display(self):
        """Create data display area"""
        tree_frame = tk.Frame(self.parent)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Date', 'Weight', 'Height', 'BMI', 'Notes')
        self.data_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=scrollbar.set)
        
        self.data_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Delete button
        tk.Button(self.parent, text="Delete Selected", command=self.delete_record).pack(pady=5)
    
    def save_data(self):
        """Save health data"""
        weight_str = self.weight_entry.get()
        height_str = self.height_entry.get()
        notes = self.notes_entry.get("1.0", tk.END).strip()
        
        # Validate inputs
        weight_valid, weight = validate_weight(weight_str)
        height_valid, height = validate_height(height_str)
        
        if not weight_valid or not height_valid:
            messagebox.showerror("Error", "Please enter valid weight (0-300 kg) and height (0-3 m)")
            return
        
        # Create and save record
        record = HealthRecord.create(weight, height, notes)
        if self.db_manager.save_record(record):
            messagebox.showinfo("Success", "Data saved successfully!")
            self.clear_entries()
            self.load_data()
            self.refresh_callback()
        else:
            messagebox.showerror("Error", "Failed to save data")
    
    def clear_entries(self):
        """Clear input fields"""
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.notes_entry.delete("1.0", tk.END)
    
    def clear_data(self):
        """Clear all input fields"""
        if messagebox.askyesno("Confirm", "Clear all input fields?"):
            self.clear_entries()
    
    def load_data(self):
        """Load data into treeview"""
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        records = self.db_manager.get_all_records()
        for record in records:
            self.data_tree.insert('', 'end', values=(
                record.id, record.date, record.weight, 
                record.height, record.bmi, record.notes
            ))
    
    def delete_record(self):
        """Delete selected record"""
        selected = self.data_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete selected record?"):
            for item in selected:
                record_id = self.data_tree.item(item, 'values')[0]
                if self.db_manager.delete_record(record_id):
                    self.load_data()
                    self.refresh_callback()
            messagebox.showinfo("Success", "Record deleted successfully!")
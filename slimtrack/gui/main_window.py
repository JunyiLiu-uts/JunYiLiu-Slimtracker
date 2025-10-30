import tkinter as tk
from tkinter import ttk
from database.db_manager import DatabaseManager
from gui.data_tab import DataTab
from gui.viz_tab import VisualizationTab
from gui.suggestions_tab import SuggestionsTab
from config.constants import DB_NAME

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("SlimTrack - Personal Health Manager")
        self.root.geometry("800x600")
        
        # Initialize database
        self.db_manager = DatabaseManager(DB_NAME)
        
        # Create GUI
        self.create_gui()
    
    def create_gui(self):
        """Create main application window"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.data_frame = ttk.Frame(self.notebook)
        self.viz_frame = ttk.Frame(self.notebook)
        self.suggest_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.data_frame, text="Data Entry")
        self.notebook.add(self.viz_frame, text="Progress Charts")
        self.notebook.add(self.suggest_frame, text="Health Suggestions")
        
        # Initialize tab components
        self.data_tab = DataTab(self.data_frame, self.db_manager, self.refresh_all)
        self.viz_tab = VisualizationTab(self.viz_frame, self.db_manager)
        self.suggest_tab = SuggestionsTab(self.suggest_frame, self.db_manager)
    
    def refresh_all(self):
        """Refresh all tabs when data changes"""
        self.viz_tab.clear_charts()
        self.suggest_tab.generate_suggestions()
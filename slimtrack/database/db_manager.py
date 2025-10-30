import sqlite3
import pandas as pd
from typing import List, Optional
from models.health_data import HealthRecord

class DatabaseManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS health_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    notes TEXT
                )
            ''')
            conn.commit()
    
    def save_record(self, record: HealthRecord) -> bool:
        """Save a health record to database"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO health_data (date, weight, height, bmi, notes)
                    VALUES (?, ?, ?, ?, ?)
                ''', (record.date, record.weight, record.height, record.bmi, record.notes))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving record: {e}")
            return False
    
    def get_all_records(self) -> List[HealthRecord]:
        """Retrieve all health records"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, date, weight, height, bmi, notes FROM health_data ORDER BY date')
                rows = cursor.fetchall()
                
                records = []
                for row in rows:
                    records.append(HealthRecord(
                        id=row[0],
                        date=row[1],
                        weight=row[2],
                        height=row[3],
                        bmi=row[4],
                        notes=row[5]
                    ))
                return records
        except Exception as e:
            print(f"Error retrieving records: {e}")
            return []
    
    def delete_record(self, record_id: int) -> bool:
        """Delete a record by ID"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM health_data WHERE id = ?', (record_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get data as pandas DataFrame"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                df = pd.read_sql_query('SELECT * FROM health_data ORDER BY date', conn)
                if not df.empty:
                    df['date'] = pd.to_datetime(df['date'])
                return df
        except Exception as e:
            print(f"Error getting DataFrame: {e}")
            return pd.DataFrame()
import sqlite3
import pandas as pd
from tabulate import tabulate
import os

def query_database(db_path):
  if not os.path.exists(db_path):
      print(f"Database file not found: {db_path}")
      return

  conn = sqlite3.connect(db_path)
  
  # Get list of tables
  cursor = conn.cursor()
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
  tables = cursor.fetchall()
  
  if not tables:
      print("No tables found in the database.")
      return

  for table in tables:
      table_name = table[0]
      print(f"\nTable: {table_name}")
      
      # Get column names
      cursor.execute(f"PRAGMA table_info({table_name})")
      columns = [col[1] for col in cursor.fetchall()]
      
      # Fetch all data from the table
      df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
      
      if df.empty:
          print("No data in this table.")
      else:
          print(f"Number of rows: {len(df)}")
          print("First few rows:")
          print(tabulate(df.head(), headers=columns, tablefmt="grid"))
          print(df['window_title'].value_counts())
          
          # Print some basic statistics
          print("\nDate range:")
          if 'timestamp' in df.columns:
              print(f"Earliest date: {df['timestamp'].min()}")
              print(f"Latest date: {df['timestamp'].max()}")
          
          if 'process_name' in df.columns:
              print("\nTop 5 processes by frequency:")
              print(df['process_name'].value_counts().head())

  conn.close()

if __name__ == "__main__":
  db_path = "activities.db"  # Update this if your database is located elsewhere
  query_database(db_path)
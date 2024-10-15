import psutil
import sqlite3
from datetime import datetime
import time
import win32gui
import win32process

class ActivityTracker:
  def __init__(self, db_path='activities.db'):
      self.db_path = db_path
      self.setup_database()

  def setup_database(self):
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            process_name TEXT,
            window_title TEXT,
            file_path TEXT,
            impact TEXT,
            todo TEXT
        )
    ''')
    conn.commit()
    conn.close()

  def get_active_window_info(self):
      try:
          window = win32gui.GetForegroundWindow()
          _, pid = win32process.GetWindowThreadProcessId(window)
          process = psutil.Process(pid)
          process_name = process.name()
          window_title = win32gui.GetWindowText(window)
          return process_name, window_title
      except Exception as e:
          print(f"Error getting window info: {e}")
          return "Unknown", "Unknown"

  def log_activity(self):
      process_name, window_title = self.get_active_window_info()
      timestamp = datetime.now().isoformat()

      conn = sqlite3.connect(self.db_path)
      cursor = conn.cursor()
      cursor.execute('''
          INSERT INTO activities (timestamp, process_name, window_title)
          VALUES (?, ?, ?)
      ''', (timestamp, process_name, window_title))
      conn.commit()
      conn.close()

  def run(self, interval=60):
      while True:
          self.log_activity()
          time.sleep(interval)

if __name__ == "__main__":
  tracker = ActivityTracker()
  tracker.run()
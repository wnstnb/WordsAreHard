import psutil
import json
from datetime import datetime
import time
import sqlite3

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
              impact TEXT,
              todo TEXT
          )
      ''')
      conn.commit()
      conn.close()

  def log_activity(self):
      current_process = psutil.Process()
      process_name = current_process.name()
      try:
          window_title = current_process.cmdline()[-1]
      except:
          window_title = "Unknown"

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
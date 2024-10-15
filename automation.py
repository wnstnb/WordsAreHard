# automation.py
import sqlite3
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from summarizer import Summarizer
import os
from dotenv import load_dotenv
load_dotenv()

class Automation:
  def __init__(self, db_path='activities.db', summarizer=None):
      self.db_path = db_path
      self.summarizer = summarizer or Summarizer(os.getenv('MODEL_PATH'))

  def get_activities(self, start_date, end_date):
      conn = sqlite3.connect(self.db_path)
      cursor = conn.cursor()
      cursor.execute('''
          SELECT * FROM activities 
          WHERE timestamp BETWEEN ? AND ?
          ORDER BY timestamp
      ''', (start_date.isoformat(), end_date.isoformat()))
      activities = cursor.fetchall()
      conn.close()
      return activities

  def generate_daily_summary(self):
      today = datetime.now().date()
      yesterday = today - timedelta(days=1)
      activities = self.get_activities(yesterday, today)
      summary = self.summarizer.summarize_activities(str(activities))
      return summary

  def generate_weekly_report(self):
      today = datetime.now().date()
      week_ago = today - timedelta(days=7)
      activities = self.get_activities(week_ago, today)
      summary = self.summarizer.summarize_activities(str(activities))
      return summary

  def send_email(self, subject, body, to_email):
      from_email = "your_email@example.com"
      msg = MIMEText(body)
      msg['Subject'] = subject
      msg['From'] = from_email
      msg['To'] = to_email

      s = smtplib.SMTP('localhost')
      s.send_message(msg)
      s.quit()

  def run_daily_automation(self):
      summary = self.generate_daily_summary()
      self.send_email("Daily Activity Summary", summary, "your_email@example.com")

  def run_weekly_automation(self):
      report = self.generate_weekly_report()
      self.send_email("Weekly Activity Report", report, "your_email@example.com")
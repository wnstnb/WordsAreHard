import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from summarizer import Summarizer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Dashboard:
  def __init__(self):
      logger.info("Initializing Dashboard")
      self.db_path = 'activities.db'
      logger.info("Initializing Summarizer (this may take a moment to download the model)")
      self.summarizer = Summarizer()
      logger.info("Dashboard initialization complete")

  def load_data(self):
      logger.info("Loading data from database")
      conn = sqlite3.connect(self.db_path)
      df = pd.read_sql_query("SELECT * FROM activities", conn)
      conn.close()
      logger.info(f"Loaded {len(df)} records from database")
      return df

  def get_activities(self, start_date, end_date):
    logger.info(f"Fetching activities from {start_date} to {end_date}")
    conn = sqlite3.connect(self.db_path)
    query = f"""
        SELECT * FROM activities 
        WHERE date(substr(timestamp, 1, 10)) BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY timestamp
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    logger.info(f"Fetched {len(df)} activities")
    return df
  
  def generate_summary(self, activities):
      logger.info("Generating summary")
      if activities.empty:
          logger.warning("No activities to summarize")
          return "No activities recorded in this period."
      
      summary = self.summarizer.summarize_activities(activities)
      logger.info("Summary generation complete")
      return summary

#   def generate_summary(self, activities):
#     logger.info("Generating summary")
#     activities_text = []
#     for activity in activities.itertuples():
#         # Assuming 'process_name' and 'window_title' are column names in your DataFrame
#         # Adjust these if your column names are different
#         process_name = getattr(activity, 'process_name', 'Unknown Process')
#         window_title = getattr(activity, 'window_title', 'Unknown Window')
#         activities_text.append(f"{process_name} - {window_title}")

#     activities_text = "\n".join(activities_text)

#     if not activities_text:
#         logger.warning("No activities to summarize")
#         return "No activities recorded in this period."

#     summary = self.summarizer.summarize_activities(activities_text)
#     logger.info("Summary generation complete")
#     return summary

  def run(self):
      logger.info("Starting dashboard")
      st.title("WordsAreHard - Activity Tracker Dashboard")

      df = self.load_data()

      # Time spent per application
      logger.info("Generating time spent chart")
      time_spent = df.groupby('process_name').size().sort_values(ascending=False)
      st.subheader("Time Spent per Application")
      st.bar_chart(time_spent)

      # Task impact distribution
      logger.info("Generating impact distribution chart")
      impact_dist = df['impact'].value_counts()
      st.subheader("Task Impact Distribution")
      fig = px.pie(values=impact_dist.values, names=impact_dist.index)
      st.plotly_chart(fig)

      # Pending TODOs
      logger.info("Displaying pending TODOs")
      todos = df[df['todo'].notnull()]
      st.subheader("Pending TODOs")
      for _, row in todos.iterrows():
          st.write(f"- {row['todo']} (Related to: {row['process_name']})")

      # Manual summary generation
      st.subheader("Generate Summary")
      summary_type = st.radio("Select summary type:", ("Daily", "Weekly", "Custom"))

      if summary_type == "Daily":
          if st.button("Generate Daily Summary"):
              logger.info("Generating daily summary")
              today = datetime.now().date()
              yesterday = today - timedelta(days=1)
              activities = self.get_activities(yesterday, today)
              summary = self.generate_summary(activities)
              st.text_area("Daily Summary", summary, height=200)

      elif summary_type == "Weekly":
          if st.button("Generate Weekly Report"):
              logger.info("Generating weekly report")
              today = datetime.now().date()
              week_ago = today - timedelta(days=7)
              activities = self.get_activities(week_ago, today)
              summary = self.generate_summary(activities)
              st.text_area("Weekly Report", summary, height=200)

      else:  # Custom date range
          col1, col2 = st.columns(2)
          start_date = col1.date_input("Start date")
          end_date = col2.date_input("End date")
          if st.button("Generate Custom Summary"):
              logger.info(f"Generating custom summary from {start_date} to {end_date}")
              activities = self.get_activities(start_date, end_date)
              summary = self.generate_summary(activities)
              st.text_area("Custom Summary", summary, height=200)

      logger.info("Dashboard rendering complete")

if __name__ == "__main__":
  logger.info("Starting WordsAreHard application")
  dashboard = Dashboard()
  dashboard.run()
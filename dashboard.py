import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from summarizer import Summarizer
import os
from dotenv import load_dotenv
load_dotenv()

class Dashboard:
    def __init__(self):
        self.db_path = 'activities.db'
        self.summarizer = Summarizer()

    def load_data(self):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM activities", conn)
        conn.close()
        return df

    def get_activities(self, start_date, end_date):
        conn = sqlite3.connect(self.db_path)
        query = f"""
                SELECT * FROM activities 
                WHERE timestamp BETWEEN '{start_date.isoformat()}' AND '{end_date.isoformat()}'
                ORDER BY timestamp
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def generate_summary(self, activities):
        activities_text = "\n".join([f"{a[2]} - {a[3]}" for a in activities])
        return self.summarizer.summarize_activities(activities_text)

    def run(self):
        st.title("WordsAreHard - Activity Tracker Dashboard")

        df = self.load_data()

        # Time spent per application
        time_spent = df.groupby('process_name').size().sort_values(ascending=False)
        st.subheader("Time Spent per Application")
        st.bar_chart(time_spent)

        # Task impact distribution
        impact_dist = df['impact'].value_counts()
        st.subheader("Task Impact Distribution")
        fig = px.pie(values=impact_dist.values, names=impact_dist.index)
        st.plotly_chart(fig)

        # Pending TODOs
        todos = df[df['todo'].notnull()]
        st.subheader("Pending TODOs")
        for _, row in todos.iterrows():
                st.write(f"- {row['todo']} (Related to: {row['process_name']})")

        # Manual summary generation
        st.subheader("Generate Summary")
        summary_type = st.radio("Select summary type:", ("Daily", "Weekly", "Custom"))

        if summary_type == "Daily":
            if st.button("Generate Daily Summary"):
                today = datetime.now().date()
                yesterday = today - timedelta(days=1)
                activities = self.get_activities(yesterday, today)
                summary = self.generate_summary(activities)
                st.text_area("Daily Summary", summary, height=200)

        elif summary_type == "Weekly":
            if st.button("Generate Weekly Report"):
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
                activities = self.get_activities(start_date, end_date)
                summary = self.generate_summary(activities)
                st.text_area("Custom Summary", summary, height=200)

if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()
import sqlite3

class Interaction:
  def __init__(self, db_path='activities.db'):
      self.db_path = db_path

  def assign_impact(self, activity_id, impact):
      conn = sqlite3.connect(self.db_path)
      cursor = conn.cursor()
      cursor.execute('UPDATE activities SET impact = ? WHERE id = ?', (impact, activity_id))
      conn.commit()
      conn.close()

  def add_todo(self, activity_id, todo):
      conn = sqlite3.connect(self.db_path)
      cursor = conn.cursor()
      cursor.execute('UPDATE activities SET todo = ? WHERE id = ?', (todo, activity_id))
      conn.commit()
      conn.close()

  def get_recent_activities(self, limit=10):
      conn = sqlite3.connect(self.db_path)
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM activities ORDER BY timestamp DESC LIMIT ?', (limit,))
      activities = cursor.fetchall()
      conn.close()
      return activities

  def interactive_session(self):
      activities = self.get_recent_activities()
      for activity in activities:
          print(f"Activity: {activity[2]} - {activity[3]}")
          impact = input("Assign impact (High/Medium/Low): ")
          self.assign_impact(activity[0], impact)
          todo = input("Add TODO (press enter to skip): ")
          if todo:
              self.add_todo(activity[0], todo)
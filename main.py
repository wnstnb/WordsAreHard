from activity_tracker import ActivityTracker
import threading

def main():
  tracker = ActivityTracker()

  # Run the activity tracker in a separate thread
  tracker_thread = threading.Thread(target=tracker.run)
  tracker_thread.start()

  print("Activity tracker is running. Use the Streamlit dashboard to interact with the data.")
  print("To stop the tracker, press Ctrl+C")

  try:
      tracker_thread.join()
  except KeyboardInterrupt:
      print("Stopping the activity tracker...")

if __name__ == "__main__":
  main()
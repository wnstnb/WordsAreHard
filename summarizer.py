from transformers import pipeline

class Summarizer:
  def __init__(self):
      self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

  def summarize_activities(self, activities):
      # Ensure the input is not too long for the model
      max_length = 1024
      if len(activities) > max_length:
          activities = activities[:max_length]
      
      summary = self.summarizer(activities, max_length=150, min_length=30, do_sample=False)
      return summary[0]['summary_text']
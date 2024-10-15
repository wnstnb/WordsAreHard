from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class Summarizer:
    def __init__(self):
        logger.info("Initializing Summarizer")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        logger.info("Summarizer initialized")

#   def summarize_activities(self, activities):
#       logger.info("Summarizing activities")
#       max_length = 1024
#       if len(activities) > max_length:
#           logger.warning(f"Input text truncated from {len(activities)} to {max_length} characters")
#           activities = activities[:max_length]
      
#       summary = self.summarizer(activities, max_length=150, min_length=30, do_sample=False)
#       logger.info("Summarization complete")
#       return summary[0]['summary_text']
  
    def summarize_activities(self, activities):
        # Prepare the input text with bullet points and file paths
        activities_text = "Here's a summary of recent activities:\n\n"
        for _, activity in activities.iterrows():
            activities_text += f"• {activity['process_name']} - {activity['window_title']}\n"
            activities_text += f"  File path: {activity['file_path']}\n\n"

        # Ensure the input is not too long for the model
        max_length = 1024
        if len(activities_text) > max_length:
            activities_text = activities_text[:max_length]

        # Generate summary
        summary = self.summarizer(activities_text, max_length=150, min_length=30, do_sample=False)

        # Post-process the summary to ensure it's in bullet point format
        summary_text = summary[0]['summary_text']
        bullet_points = summary_text.split('. ')
        formatted_summary = "Summary of activities:\n\n" + "\n".join([f"• {point.strip()}" for point in bullet_points if point.strip()])

        return formatted_summary
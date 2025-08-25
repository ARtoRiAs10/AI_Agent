# logger.py
import os
from datetime import datetime

class ConversationLogger:
    def __init__(self, log_directory="logs"):
        """
        Initializes the logger.
        Creates a log directory if it doesn't exist.
        Sets up a unique filename for the current debate session.
        """
        self.log_directory = log_directory
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)
        
        # Create a unique filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file_path = os.path.join(self.log_directory, f"debate_{timestamp}.txt")
        print(f"--- LOGGER: Conversation will be saved to {self.log_file_path} ---")

    def log(self, message: str):
        """
        Appends a message to the log file.
        Each message is written on a new line.
        """
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"--- LOGGER ERROR: Failed to write to log file: {e} ---")

    def log_turn(self, speaker: str, message: str):
        """
        A helper method to log a speaker's turn in a formatted way.
        """
        formatted_message = f"[{datetime.now().strftime('%H:%M:%S')}] {speaker}:\n{message}\n"
        self.log(formatted_message)

    def log_system_message(self, message: str):
        """
        A helper method to log system events or tool usage.
        """
        formatted_message = f"--- SYSTEM: {message} ---\n"
        self.log(formatted_message)
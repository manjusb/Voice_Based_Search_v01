import datetime

class InteractionLogger:
    def __init__(self, log_file="interaction_log.txt"):
        self.log_file = log_file

    def log_interaction(self, user_query, ai_response):
        """
        Logs the user's query and the AI's response to a file.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] User: {user_query}\n")
            f.write(f"[{timestamp}] AI: {ai_response}\n\n")

if __name__ == '__main__':
    # Example usage (for testing)
    logger = InteractionLogger()
    logger.log_interaction("What is the capital of France?", "The capital of France is Paris.")
    logger.log_interaction("What is 2 + 2?", "2 + 2 is 4.")
    print(f"Interactions logged to {logger.log_file}")
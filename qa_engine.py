import os
import google.generativeai as genai

class QASystem:
    def __init__(self):
        # Configure the API key from environment; masked default for public repos
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "XXXXXXXXXXXX"))
        self.model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        self.context = ""

    def load_context(self, text):
        """
        Loads the extracted text as context for answering questions.
        """
        self.context = text
        print(f"[DEBUG] Context loaded, length: {len(text)}")
        print(f"[DEBUG] Context preview: {text[:200]}")

    def answer_question(self, question):
        """
        Answers a question based on the loaded context using a powerful LLM.
        """
        if not self.context:
            return "I don't have any context to answer questions. Please upload a file first."

        # Handle specific queries
        if "help me with question" in question.lower():
            return self.answer_specific_question(question)

        prompt = f"Based on the following context, please answer the question.\n\nContext:\n{self.context}\n\nQuestion:\n{question}"

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred while generating an answer: {e}"

    def answer_specific_question(self, question):
        """
        Parses and answers a specific question (e.g., "help me with question 4 from chapter 3").
        """
        # This is a placeholder for a more sophisticated parsing logic.
        # For now, we'll just extract the numbers and assume they refer to chapters and questions.
        import re
        numbers = re.findall(r'\d+', question)
        if len(numbers) == 2:
            chapter, q_number = numbers
            return f"I will help you with question {q_number} from chapter {chapter}. Please provide the question text."
        elif len(numbers) == 1:
            q_number = numbers[0]
            return f"I will help you with question {q_number}. Please provide the question text."
        else:
            return "I can help with specific questions, but I need a question number. For example, say 'help me with question 4'."

if __name__ == '__main__':
    # Example usage (for testing)
    qa = QASystem()
    qa.load_context("The quick brown fox jumps over the lazy dog.")
    print(qa.answer_question("What did the fox jump over?"))
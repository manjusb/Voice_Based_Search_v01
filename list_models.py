import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "XXXXXXXXXXXX"))

for model in genai.list_models():
    print(model)
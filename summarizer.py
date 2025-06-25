import google.generativeai as genai
import os
from prompts import get_summary_prompt, get_timestamps_prompt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#  Set the Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#  Use a working free model
MODEL_NAME = "models/gemini-1.5-flash"  # This one works and is free

def get_model():
    try:
        return genai.GenerativeModel(model_name=MODEL_NAME)
    except Exception as e:
        print("Error loading model:", e)
        return None

#  Generate summary from transcript
def generate_summary(transcript):
    prompt = get_summary_prompt(transcript)
    model = get_model()
    if not model:
        return "Gemini Error: Could not load model."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

# Generate timestamps from transcript
def generate_timestamps(transcript):
    prompt = get_timestamps_prompt(transcript)
    model = get_model()
    if not model:
        return "Gemini Error: Could not load model."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

# Answer user questions about the video
def answer_question(transcript, question):
    prompt = f"""
You are an AI assistant. A user has watched a YouTube video, and this is its transcript:

\"\"\"{transcript[:6000]}\"\"\"

Now they have a question:
\"\"\"{question}\"\"\"

Answer in a clear and helpful way based only on the video content.
"""
    model = get_model()
    if not model:
        return "Gemini Error: Could not load model."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

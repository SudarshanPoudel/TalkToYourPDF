from dotenv import load_dotenv
import os
import google.generativeai as genai

PROMPT =  """
Answer the following question based on provided context, do not generate too much on your own.
If you can not find answer on following context, say "I don't know". But if provided context
gives you certain idea of the answer, try to answer as best as you can without much external
information. Also do not say anything about the context other then answer itself.

Question : {{Question}}
Context: {{Context}}
for context, here is the chat history as well: {{Chat_History}}
"""

# Load model
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")


def answer_question(question, context, history):
    prompt = PROMPT.replace("{{Question}}", question)
    prompt = prompt.replace("{{Context}}", context)
    prompt = prompt.replace("{{Chat_History}}", history)
    answer = model.generate_content(prompt).text
    return answer
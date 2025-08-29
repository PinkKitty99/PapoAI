from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

def refine_text(summary_text):
    prompt = f"""
You are an expert research poster editor. Improve the tone, clarity, and flow of the following academic poster content. Make it concise, readable, and suitable for a professional academic conference.

Preserve the original structure (sections and bullets), but make the language smoother and clearer.

Text:
{summary_text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            timeout=180,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f" Error in Editor Agent: {e}"
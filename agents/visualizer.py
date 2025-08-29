import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def suggest_visuals(summary_text):
    prompt = f"""
You are a research poster designer. Based on the academic summary below, suggest 1–2 visuals (charts, diagrams, illustrations, etc.) that would enhance each section.

## Introduction
- [visual description]

## Methodology
- [visual description]

## Results
- [visual description]

## Conclusion
- [visual description]

Summary:
{summary_text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            timeout=180,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in Visualization Agent: {e}"

def generate_image(prompt):
    try:
        print(prompt)
        response = client.images.generate(
            model='gpt-image-1',
            prompt=prompt,
            n=1,
            size= '1024x1024'
        )
        return f"data:image/png;base64,{response.data[0].b64_json}"
    except Exception as e:
        return f"Error generating image: {e}"
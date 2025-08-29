import fitz  
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def summarize_sections(text):
    prompt = f"""
You are an AI assistant helping a student prepare an academic poster.
Summarize the following paper text into labeled bullet-point sections for the poster.

You must output markdown in this exact format:

## Introduction
- [point]
- [point]

## Methodology
- [point]
- [point]

## Summary
- [point]

## Discussion
- [point]

## Results
- [point]

## Conclusion
- [point]

## LeftBubble
- [point]
- [point]

## RightBubble
- [point]
- [point]

DO NOT leave any section blank. If something is missing from the paper, write a reasonable placeholder.
Use markdown-style bullet points and aim for 3–5 items per section.

Text to summarize:
{text[:8000]}
"""

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content
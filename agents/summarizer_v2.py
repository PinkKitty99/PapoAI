import pymupdf  
import os
from openai import OpenAI

client = OpenAI()

def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def summarize_sections(text):
    instructions = f"""
You are an AI assistant helping a student prepare an academic poster.
Summarize the following paper text into labeled bullet-point sections for the poster.

You must output markdown in this exact format:

## Authors

[a line of authors]

## Institutions

[a line of institutions]

## Summary
- [point]

## Contributions
- [point]
- [point]
- [point]

## Methodology

[a paragraph of methodology]
- [point]
- [point]

## Results
- [point]
- [point]
- [point]

## Discussion
- [point]
- [point]


DO NOT leave any section blank. Use markdown-style bullet points and aim for 3–5 items per section.
"""

    response = client.responses.create(
        model="gpt-4.1",
        instructions=instructions,
        input=text,
    )
    return response.output_text
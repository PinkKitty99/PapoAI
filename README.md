# PapoAI: Research Poster Generator

PapoAI is a web application that automatically generates academic research posters from uploaded PDF papers. It uses AI agents for summarization, layout analysis, visualization suggestions, and text refinement to produce a polished HTML poster.

## Features
- Upload a research paper (PDF)
- Automatic extraction and summarization of paper content
- Document layout analysis using YOLOv10
- Visual suggestion for poster sections
- HTML poster generation with modern, girly pink design
- Optional text refinement for improved clarity

## How It Works
1. **Upload PDF**: Drag and drop your research paper.
2. **Text Extraction**: The app extracts text from the PDF.
3. **Layout Analysis**: Uses YOLOv10 to detect figures, tables, and captions.
4. **Summarization**: AI summarizes the paper into poster sections.
5. **Visual Suggestions**: AI suggests visuals for each section.
6. **Poster Generation**: Produces a beautiful HTML poster.

## Installation
1. Clone this repository:
   ```sh
   git clone <your-repo-url>
   cd PapoAI
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Run the Streamlit app:
```sh
streamlit run app.py
```
Then open the provided local URL in your browser.

## Project Structure
- `app.py` — Main Streamlit web app
- `agents/` — AI agents for summarization, visualization, layout, and editing
- `pdf_agent/` — PDF parsing and layout detection
- `html_template.html` — Poster HTML template

## Requirements
See `requirements.txt` for all dependencies. Key packages:
- streamlit
- openai
- huggingface_hub
- PyMuPDF
- doclayout_yolo
- python-dotenv
- torch
- opencv-python
- pillow
- pydantic

## Notes
- GPU acceleration (CUDA/MPS) is optional. The app will run on CPU if no GPU is available.
- Output HTML poster uses a shoujo girly pink theme for a modern, feminine look.

## License
MIT

## Authors
Group 8, Westlake University

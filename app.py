
from dotenv import load_dotenv
load_dotenv(verbose=True)

import streamlit as st
from agents.summarizer_v2 import extract_text_from_pdf, summarize_sections
from agents.visualizer_v2 import suggest_visuals
from agents.layout_v2 import generate_html_poster
from agents.editor import refine_text
import os

st.set_page_config(page_title="PapoAI", layout="wide")
st.title("📄 PapoAI — Research Poster Generator")

uploaded_file = st.file_uploader("Upload a research paper (PDF)", type="pdf")

image_url = None 

if uploaded_file:
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner(" Extracting text..."):
        text = extract_text_from_pdf(file_path)

    with st.spinner(" Analyzing document layout"):
        from pdf_agent import parse_pdf, prepare_model
        model = prepare_model()
        res_path = "outputs"
        figures, figure_captions, tables, table_captions = parse_pdf(
            model, file_path,
            os.path.join(res_path, "annot"),
            os.path.join(res_path, "fig"),
            os.path.join(res_path, "tab"),
        )

    with st.spinner(" Summarizing paper..."):
        summary = summarize_sections(text)

    st.markdown(" Poster Content Summary")
    st.markdown(summary)

    with st.spinner(" Analyzing for visual ideas..."):
        visuals = suggest_visuals(summary)

    st.markdown(" Suggested Visuals")
    st.json(visuals.model_dump_json())

    # st.markdown(" Generate a Visual")
    # image_prompt = st.text_input("Enter a description for the image (or paste from above):")

    # if st.button("Generate Image"):
    #     with st.spinner(" Generating image..."):
    #         image_url = generate_image(image_prompt)
    #         if isinstance(image_url, str):
    #             st.image(image_url, caption="Generated Visual")
    #         else:
    #             st.error(image_url)
  
    with st.spinner("Creating poster layout..."):
        html_code = generate_html_poster(visuals, figures[0], tables[0])
        st.success(" Poster layout created")
        # st.markdown(f"[ Download Poster HTML]({html_path})", unsafe_allow_html=True)
        st.components.v1.html(html_code, height=1800, scrolling=True)

    # if st.button("Improve Poster Clarity (editor agent)"):
    #     with st.spinner("Refining text..."):
    #         refined_summary = refine_text(summary)
    #         st.markdown("Polished Summary")
    #         st.markdown(refined_summary)
    #         summary=refined_summary

else:
    st.info("📂 Upload a PDF above to get started.")
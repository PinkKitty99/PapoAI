import os

def generate_html_poster(summary_text, image_url=None, extra_images=None, output_file="outputs/poster.html"):
    import os, re
    os.makedirs("outputs", exist_ok=True)

    def extract_section(text, section_name):
        pattern = rf"##\s*{section_name}[\s\S]*?(?=\n##|$)"
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            return "<p><em>Section not found</em></p >"
        section = re.sub(rf"##\s*{section_name}", "", match.group(0)).strip()
        bullets = [line.strip("- ").strip() for line in section.split('\n') if line.strip()]
        if not bullets:
            return f"<p>{section}</p >"
        return "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"

    if extra_images is None:
        extra_images = []

    html = f"""
    <html>
    <head>
        <title> PapoAI Research Poster</title>
        <style>
            body {{
                font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
                background: #fff5f8;
                margin: 0;
            }}
            .header {{
                background: linear-gradient(135deg, #ffc1d3, #ffd6e8);
                color: #8a4469;
                text-align: center;
                padding: 30px 20px;
                border-bottom: 4px dashed #fcb1c7;
            }}
            .header h1 {{
                font-size: 36px;
                margin: 0;
                font-weight: 700;
            }}
            .header p {{
                font-size: 18px;
                margin-top: 5px;
                font-style: italic;
            }}
            .poster {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                padding: 40px;
                max-width: 1200px;
                margin: auto;
            }}
            .section {{
                border-radius: 25px;
                padding: 25px;
                background: #ffe6ef;
                border: 2px dashed #f8a7b3;
                color: #6b3a4c;
                box-shadow: 0 4px 12px rgba(255,182,193, 0.3);
            }}
            .section h2::before {{
                content: attr(data-number) " ";
                background: #fff;
                color: #d6336c;
                border-radius: 50%;
                padding: 5px 10px;
                margin-right: 10px;
                font-weight: bold;
                font-size: 16px;
            }}
            .center-block {{
                grid-column: span 2;
                display: flex;
                justify-content: center;
                align-items: center;
                position: relative;
                margin: 40px 0;
            }}
            .highlight-circle {{
                background: #fff;
                border-radius: 50%;
                width: 400px;
                height: 400px;
                padding: 30px;
                border: 4px dashed #fcbad3;
                box-shadow: 0 0 20px rgba(255,192,203, 0.4);
                text-align: center;
                z-index: 1;
                position: relative;
            }}
            .highlight-circle h3 {{
                font-size: 22px;
                margin-bottom: 10px;
                color: #e75480;
            }}
            .highlight-circle p {{
                font-size: 15px;
            }}
            .side-bubble {{
                background: #ffe6ef;
                border: 2px dashed #fcbad3;
                padding: 20px;
                border-radius: 20px;
                width: 220px;
                box-shadow: 0 2px 10px rgba(255,192,203,0.2);
                position: absolute;
                top: 20%;
            }}
            .left-bubble {{
                left: 0px;
            }}
            .right-bubble {{
                right: 0px;
            }}
            ul {{ padding-left: 20px; }}
            li {{ margin-bottom: 6px; }}
            .image-gallery {{
                grid-column: span 2;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                margin-top: 30px;
            }}
            .image-gallery img {{
                border-radius: 15px;
                max-width: 300px;
                border: 2px solid #fcbad3;
                box-shadow: 0 2px 8px rgba(255,192,203, 0.2);
            }}
            .footer {{
                text-align: center;
                font-size: 14px;
                color: #a66;
                margin: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1> PapoAI: Paper to Poster Generator<h1>
            <p>By Group 8 - Westlake University - June 3rd 2024 <p>
        </div>

        <div class="poster">
            <div class="section" data-number="1">
                <h2 data-number="1">Introduction</h2>
                {extract_section(summary_text, "Introduction")}
            </div>
            <div class="section" data-number="2">
                <h2 data-number="2">Methodology</h2>
                {extract_section(summary_text, "Methodology")}
            </div>

            <div class="center-block">
                <div class="side-bubble left-bubble">
                    {extract_section(summary_text, "LeftBubble")}
                </div>
                <div class="highlight-circle">
                    <h3>✨ Highlights</h3>
                    <p>{extract_section(summary_text, "Summary")}</p >
                    {"< img src='" + image_url + "' alt='Main Image' style='max-width:90%; border-radius:15px; margin-top:10px;'/>" if image_url else ""}
                </div>
                <div class="side-bubble right-bubble">
                    {extract_section(summary_text, "RightBubble")}
                </div>
            </div>

            <div class="section" data-number="3">
                <h2 data-number="3">Discussion</h2>
                {extract_section(summary_text, "Discussion")}
            </div>
            <div class="section" data-number="4">
                <h2 data-number="4">Results</h2>
                {extract_section(summary_text, "Results")}
            </div>
            <div class="section" data-number="5">
                <h2 data-number="5">Conclusion</h2>
                {extract_section(summary_text, "Conclusion")}
            </div>
        </div>

        <div class="image-gallery">
            {''.join(f"< img src='{img}' alt='Figure'>" for img in extra_images)}
        </div>

        <div class="footer">
            © 2025 PapoAI
        </div>
    </body>
    </html>
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    return output_file


def extract_section(text, section_name):
    import re

    # Match section content from markdown-style input
    pattern = rf"##\s*{section_name}[\s\S]*?(?=\n##|$)"
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return "<p><em>Section not found</em></p >"

    section = match.group(0).strip()

    # Remove the section header
    section = re.sub(rf"##\s*{section_name}", "", section, flags=re.IGNORECASE).strip()

    # Convert bullet points to HTML list
    bullets = [line.strip('- ').strip() for line in section.split('\n') if line.strip()]
    if not bullets:
        return f"<p>{section}</p >"

    html_bullets = "<ul>" + "".join(f"<li>{point}</li>" for point in bullets) + "</ul>"
    return html_bullets
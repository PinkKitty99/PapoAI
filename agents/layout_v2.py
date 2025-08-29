import base64
from pathlib import Path

from .visualizer_v2 import Poster

def img_base64_url(img_path: Path):
    assert img_path.suffix.lower() == '.png', "Only support PNG images"
    data = base64.b64encode(img_path.read_bytes()).decode('utf-8')

    return "data:image/png;base64," + data

def generate_html_poster(poster: Poster, summary_figure: Path, results_table: Path, output_file="outputs/poster.html") -> str:

    import os
    fig_s = img_base64_url(summary_figure)
    tab_r = img_base64_url(results_table)

    template_path = os.path.join(os.path.dirname(__file__), '..', 'html_template.html')
    template_path = os.path.abspath(template_path)
    with open(template_path, 'r', encoding='utf-8') as fp:
        html = fp.read()

    html = html.replace('{title}', poster.title)
    html = html.replace('{authors}', poster.authors)
    html = html.replace('{institutions}', poster.institutions)
    html = html.replace('{summary}', poster.summary)
    html = html.replace('{summary_figure}', fig_s)
    html = html.replace('{contributions}', poster.contributions)
    html = html.replace('{methodology}', poster.methodology)
    html = html.replace('{results}', poster.results)
    html = html.replace('{results_figure}', tab_r)
    html = html.replace('{discussions}', poster.discussions)

    with open(output_file, 'w', encoding='utf-8') as fp:
        fp.write(html)
    return html
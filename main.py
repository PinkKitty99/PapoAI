import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import typer
from typing_extensions import Annotated

from huggingface_hub import hf_hub_download
from doclayout_yolo import YOLOv10

from pdf_agent import parse_pdf, prepare_model

app = typer.Typer()

@app.command()
def main(
    pdf_path: Annotated[str, typer.Option(help="Path to the PDF file")] = "target.pdf",
    res_path: Annotated[str, typer.Option(help="Output results path")] = "outputs",
    imgsz: Annotated[int, typer.Option(help="Image size for processing")] = 1024,
    line_width: Annotated[int, typer.Option(help="Line width for annotations")] = 5,
    font_size: Annotated[int, typer.Option(help="Font size for annotations")] = 20,
    conf: Annotated[float, typer.Option(help="Confidence threshold")] = 0.2,
):
    """Parse PDF documents and extract figures and tables using DocLayout-YOLO."""

    model = prepare_model()

    parse_pdf(
        model,
        pdf_path,
        os.path.join(res_path, "annot"),
        os.path.join(res_path, "fig"),
        os.path.join(res_path, "tab"),
        imgsz=imgsz,
        conf=conf,
        line_width=line_width,
        font_size=font_size,
    )


if __name__ == "__main__":
    app()

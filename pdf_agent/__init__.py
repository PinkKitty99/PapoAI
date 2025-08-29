import os
import cv2
import torch

from pathlib import Path

from huggingface_hub import hf_hub_download
from pydantic import BaseModel

from doclayout_yolo import YOLOv10
from pdf_agent.pdf2img import pdf2img

def prepare_model() -> YOLOv10:
    
    filepath = hf_hub_download(
        repo_id="juliozhao/DocLayout-YOLO-DocStructBench",
        filename="doclayout_yolo_docstructbench_imgsz1024.pt",
    )

    model = YOLOv10(filepath)

    return model


def parse_pdf(
    model: YOLOv10,
    pdf_path: str,
    out_annot_path: str,
    out_fig_path: str,
    out_tab_path: str,
    imgsz: int = 1024,
    conf: float = 0.2,
    line_width: int = 10,
    font_size: int = 80,
):
    for d in [out_annot_path, out_fig_path, out_tab_path]:
        os.makedirs(d, exist_ok=True)

    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps" if torch.backends.mps.is_available() else "cpu"
    )
    if device == "cpu":
        print("Warning: Running on CPU. Processing may be slow. For best performance, use a machine with CUDA or MPS support.")
    else:
        print(f"Using device: {device}")

    images = pdf2img(pdf_path)

    det_res = model.predict(
        images,
        imgsz=imgsz,
        conf=conf,
        device=device,
    )

    pdf_name = os.path.basename(pdf_path)

    figures, figure_captions, tables, table_captions = [], [], [], []
    for idx, res in enumerate(det_res):
        annotated_frame = res.plot(pil=True, line_width=line_width, font_size=font_size)
        output_path = os.path.join(
            out_annot_path, pdf_name.replace(".pdf", f"_{idx}_annot.jpg")
        )
        cv2.imwrite(output_path, annotated_frame)

        box_cls_count = dict()
        for box_idx, box_cls in enumerate(res.boxes.cls):
            box_cls = box_cls.item()
            box_cls_count[box_cls] = box_cls_count.get(box_cls, 0) + 1
            save_to = None
            if res.names[box_cls] == "figure":
                save_to = os.path.join(
                    out_fig_path,
                    pdf_name.replace(
                        ".pdf", f"_{idx}_fig_{box_cls_count[box_cls]}.png"
                    ),
                )
                figures.append(Path(save_to))
            elif res.names[box_cls] == "figure_caption":
                save_to = os.path.join(
                    out_fig_path,
                    pdf_name.replace(
                        ".pdf", f"_{idx}_figcap_{box_cls_count[box_cls]}.png"
                    ),
                )
                figure_captions.append(Path(save_to))
            elif res.names[box_cls] == "table":
                save_to = os.path.join(
                    out_tab_path,
                    pdf_name.replace(
                        ".pdf", f"_{idx}_tab_{box_cls_count[box_cls]}.png"
                    ),
                )
                tables.append(Path(save_to))
            elif res.names[box_cls] == "table_caption":
                save_to = os.path.join(
                    out_tab_path,
                    pdf_name.replace(
                        ".pdf", f"_{idx}_tabcap_{box_cls_count[box_cls]}.png"
                    ),
                )
                table_captions.append(Path(save_to))
            if save_to is not None:
                images[idx].crop(res.boxes.xyxy[box_idx].tolist()).save(
                    save_to, format="PNG"
                )
    
    return figures, figure_captions, tables, table_captions

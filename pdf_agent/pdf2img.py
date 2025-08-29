import pymupdf
from PIL import Image


def load_pdf_page(page: pymupdf.Page, dpi: int) -> Image.Image:
    pix = page.get_pixmap(matrix=pymupdf.Matrix(dpi / 72, dpi / 72))
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    if pix.width > 3000 or pix.height > 3000:
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1, 1), alpha=False)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    return image


def pdf2img(pdf_path: str) -> list[Image.Image]:
    images = []

    doc = pymupdf.open(pdf_path)
    for page in doc:
        image = load_pdf_page(page, dpi=250)
        images.append(image)

    return images


if __name__ == "__main__":
    print(pdf2img("target.pdf"))

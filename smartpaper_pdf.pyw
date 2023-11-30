#!/bin/python3

import os, sys

# install with: pip install img2pdf
import img2pdf

# install with: pip install pypdf
from pypdf import PdfWriter, PdfReader


def show_usage():
    print(f"Usage: {sys.argv[0]} <leremark folder path>")
    print(
        '\tThe leremark folder name ends with ".leremarkfolder". Inside it there are .leremark and .png files.'
    )


def get_pdf_path(leremark_folder_path):
    name = os.path.split(leremark_folder_path)[-1]
    original_pdf = name.replace(".leremarkfolder", "")
    return leremark_folder_path.replace(name, original_pdf)


def get_pages_to_modify(leremark_folder_path):
    dic = {}
    for file in os.listdir(leremark_folder_path):
        file_path = os.path.join(leremark_folder_path, file)
        if os.path.isfile(file_path):
            name, extension = os.path.splitext(file_path)
            name = os.path.split(name)[-1]  # ignore the full path
            if extension in [".png"]:
                dic[name] = {"index": int(name.replace("page", "")), "mask": file_path}
    return dic


def create_pdf_from_png_mask(output_name, mask_path, mask_box):
    with open(output_name, "wb") as f:
        f.write(img2pdf.convert(mask_path))

    layout_fun = img2pdf.get_layout_fun(
        pagesize=mask_box,
        imgsize=None,
        border=None,
        fit=img2pdf.FitMode.fill,
        auto_orient=False,
    )
    with open(output_name, "wb") as f:
        f.write(img2pdf.convert(mask_path, layout_fun=layout_fun))


def create_pdf(leremark_folder_path, output_pdf):
    original_pdf = get_pdf_path(leremark_folder_path)
    if not os.path.isfile(original_pdf):
        print("PDF file not found at expected location:", original_pdf)
        exit(1)

    print("original PDF file found at:", original_pdf)
    pdf_writer = PdfWriter(clone_from=original_pdf)

    pages = get_pages_to_modify(leremark_folder_path)
    print("page annotations found:", list(pages.keys()))

    print("starting...\n")
    for key in pages.keys():
        page = pages[key]
        number = page["index"]
        png_mask = page["mask"]
        print(f"processing page {number}")

        pdf_mask = f"temp{page['index']}.pdf"
        print(f"creating {pdf_mask} mask from {png_mask}")
        box = pdf_writer.pages[number - 1].mediabox
        mask_box = (box.width, box.height)
        print(f"page size is {mask_box}")
        create_pdf_from_png_mask(pdf_mask, png_mask, mask_box)

        stamp = PdfReader(pdf_mask).pages[0]
        pdf_writer.pages[number - 1].merge_page(
            stamp, over=True
        )  # set 'over' to False for watermarking
        os.remove(pdf_mask)
        print("done\n")

    pdf_writer.write(output_pdf)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_usage()
        exit(1)

    src_dir = sys.argv[1]
    output_pdf = os.path.abspath(os.path.split(get_pdf_path(src_dir))[-1])

    create_pdf(src_dir, output_pdf)
    print(f'created output: "{output_pdf}"')

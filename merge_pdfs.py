"""Merge all PDF files in a folder into a single PDF.

Usage:
    python merge_pdfs.py <input_folder> [output_file]

Requires:  pip install pypdf
"""
import sys
from pathlib import Path

from pypdf import PdfWriter


def merge_pdfs(folder: str, output_name: str = "merged.pdf") -> Path:
    folder_path = Path(folder)
    if not folder_path.is_dir():
        raise NotADirectoryError(f"Folder not found: {folder_path}")

    output_path = folder_path / output_name

    # Pick only .pdf files (case-insensitive), sorted by name,
    # and skip the output file in case it already exists from a previous run.
    pdf_files = sorted(
        (p for p in folder_path.iterdir()
         if p.is_file() and p.suffix.lower() == ".pdf" and p.resolve() != output_path.resolve()),
        key=lambda p: p.name.lower(),
    )

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {folder_path}")

    writer = PdfWriter()
    for pdf in pdf_files:
        try:
            writer.append(str(pdf))
            print(f"Added: {pdf.name}")
        except Exception as e:
            print(f"Skipped {pdf.name}: {e}")

    with open(output_path, "wb") as f:
        writer.write(f)
    writer.close()

    print(f"\nMerged {len(pdf_files)} file(s) into: {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python merge_pdfs.py <input_folder> [output_file]")
        sys.exit(1)
    merge_pdfs(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "merged.pdf")

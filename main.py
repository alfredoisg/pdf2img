import os
from pathlib import Path
from pdf2image import convert_from_path
import sys
from tqdm import tqdm

def convert_pdfs_in_directory(source_directory, output_directory):
    pdf_files = []
    # Collect all PDF file paths
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = Path(root) / file
                pdf_files.append(pdf_path)
    
    # Process each PDF with a progress bar
    for pdf_path in tqdm(pdf_files, desc="Converting PDFs"):
        output_subdir = Path(output_directory) / pdf_path.parent.relative_to(source_directory)
        output_subdir.mkdir(parents=True, exist_ok=True)
        
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        
        # Save each page as an image
        for i, image in enumerate(images):
            image_filename = output_subdir / f"{pdf_path.stem}_page_{i+1}.jpg"
            image.save(image_filename, 'JPEG')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <source_dir> <output_dir>")
        sys.exit(1)

    source_dir = sys.argv[1]
    output_dir = sys.argv[2]
    convert_pdfs_in_directory(source_dir, output_dir)


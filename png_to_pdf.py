import os
import sys
from PIL import Image

def convert_png_to_pdf(source_folder, destination_folder):
    # Ensure destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Loop through all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.lower().endswith('.png'):
            png_path = os.path.join(source_folder, filename)
            pdf_filename = os.path.splitext(filename)[0] + '.pdf'
            pdf_path = os.path.join(destination_folder, pdf_filename)

            try:
                # Open and convert image
                with Image.open(png_path) as img:
                    # Ensure image is in RGB mode (PDF requires this)
                    rgb_img = img.convert('RGB')
                    rgb_img.save(pdf_path, 'PDF')
                    print(f"Converted: {filename} -> {pdf_filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_png_to_pdf.py <source_folder> <destination_folder>")
        sys.exit(1)

    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]

    if not os.path.isdir(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist.")
        sys.exit(1)

    convert_png_to_pdf(source_folder, destination_folder)

if __name__ == "__main__":
    main()

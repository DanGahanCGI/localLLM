import os
from pdf2image import convert_from_bytes, convert_from_path
import pytesseract
import yaml
import requests
from pathlib import Path
def ocr_from_pdf(pdf_url):
    """Perform OCR on each page of an image-based PDF."""
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        pdf_bytes = response.content
        images = convert_from_bytes(pdf_bytes)
        pages_text = []
        for i, image in enumerate(images):
            page_text = pytesseract.image_to_string(image)
            pages_text.append(page_text)
        return pages_text
    except requests.exceptions.RequestException as e:
        print(f"Error accessing PDF URL {pdf_url}: {e}")
        return None

def write_to_markdown(text_list, output_file):
    """Write extracted text to a Markdown file."""
    with open(output_file, "w", encoding="utf-8") as file:
        for i, text in enumerate(text_list):
            file.write(f"# Page {i+1}\n\n")
            file.write(text)
            file.write("\n\n")

if __name__ == "__main__":
    # Load YAML file
    with open("/opt/scrape_content", "r") as file:
        data = yaml.safe_load(file)

       # Extract PDF URLs from the "image_based_pdf" tag in YAML file
    pdf_urls = data.get("image_based_pdf", [])

    # Iterate over each PDF URL
    for pdf_url in pdf_urls:
        # Perform OCR on the PDF URL and extract text
        extracted_text = ocr_from_pdf(pdf_url)


        # Define the output file name
        output_file = os.path.splitext(os.path.basename(pdf_url))[0] + ".md"
        file_path = Path("/opt/scraped_output") / output_file

        # Write the extracted text to a Markdown file
        write_to_markdown(extracted_text, file_path)

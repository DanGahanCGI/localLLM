import pdfplumber
import pypandoc
import requests
from urllib.parse import urlparse
from pathlib import Path
import yaml
import io

def extract_pdf_text(url):
    """Extract text content from a PDF URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        pdf_content = io.BytesIO(response.content)
        with pdfplumber.open(pdf_content) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error accessing PDF URL {url}: {e}")
        return None

def convert_to_markdown(content):
    """Convert content to Markdown format."""
    try:
        pypandoc.download_pandoc()
        markdown_content = pypandoc.convert_text(content, 'markdown', format='html')
        return markdown_content
    except Exception as e:
        print(f"Error converting content to Markdown: {e}")
        return None

if __name__ == '__main__':
    # Load YAML file
    with open("/opt/scrape_content", "r") as file:
        data = yaml.safe_load(file)

    # Extract PDF URLs from the YAML file
    pdf_urls = data.get("pdf", [])

    # Extract text from PDF URLs and convert to Markdown
    for url in pdf_urls:
        # Check if the URL starts with "http" or "https"
        if url.startswith("http://") or url.startswith("https://"):
            pdf_text = extract_pdf_text(url)
            if pdf_text:
                markdown_content = convert_to_markdown(pdf_text)
                if markdown_content:
                    # Get the output file name
                    parsed_url = urlparse(url)
                    file_name = f"{parsed_url.netloc}{parsed_url.path.replace('/', '_')}.md"
                    file_path = Path("/opt/scraped_output") / file_name

                    # Save Markdown content to a file
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(markdown_content)
                    print(f"Markdown content saved to {file_path}")
        else:
            print(f"Skipping non-HTTP/HTTPS URL: {url}")

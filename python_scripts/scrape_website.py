import requests
from bs4 import BeautifulSoup
import html2text
from urllib.parse import urljoin
import os
from urllib.parse import urlparse
import yaml

print("starting")
def scrape_websites(urls):
    for url in urls:
        scrape_website(url)

def scrape_website(base_url):
    visited_urls = set()
    urls_to_visit = [base_url]

    while urls_to_visit:
        url = urls_to_visit.pop(0)

        if url in visited_urls:
            continue

        visited_urls.add(url)

        try:
            response = requests.get(url)
            html_content = response.content
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {url}: {e}")
            continue

        soup = BeautifulSoup(html_content, "html.parser")

        # Extract the body content
        body = soup.find("main", {"id": "content"})

        if body:
            # Convert HTML to markdown
            converter = html2text.HTML2Text()
            markdown_content = converter.handle(str(body))

            # Save markdown content to a file
            save_markdown_file(url, markdown_content)


        # Find all links on the page
        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                absolute_url = urljoin(url, href)
                if absolute_url.startswith(base_url) and absolute_url not in visited_urls:
                    urls_to_visit.append(absolute_url)

def save_markdown_file(url, content):
    # Create a directory to store the files
    output_dir = "/opt/scraped_output"
    os.makedirs(output_dir, exist_ok=True)

    # Generate a file name based on the URL
    parsed_url = urlparse(url)
    file_name = f"{parsed_url.netloc}{parsed_url.path.replace('/', '_')}.md"
    file_path = os.path.join(output_dir, file_name)

    # Save the content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Markdown content saved to {file_path}")

# Load YAML file
with open("/opt/scrape_content", "r") as file:
    data = yaml.safe_load(file)

# Extract URLs under "html" section
html_urls = data.get("html", [])

# Example usage
scrape_websites(html_urls)

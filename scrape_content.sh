#!/bin/sh

cd /root
python -m venv .
./bin/pip install -r /opt/python_scripts/requirements.txt
./bin/python /opt/python_scripts/scrape_website.py
./bin/python /opt/python_scripts/scrape_pdf.py
apt-get update
apt-get install -y poppler-utils
apt-get install -y tesseract-ocr
./bin/python /opt/python_scripts/scrape_image_based_pdf.py
cat /opt/scraped_output/*.md > /opt/combinedScrapedContent.md
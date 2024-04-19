# Purpose

Quick and dirty repo for tools to run and experiment with open source LLMs locally.  Relies upon ollama, can either run it within a container or preferably natively as that'll get better performance with GPU access.

Use the compose files to bring services up.

There's a couple of scraping scripts included to scrape html, pdf and image based pdfs. All scraped content gets combined into combinedScrapedContent.md which can then be used to provide knowledge to the LLm through RAG. Add any sources to the scrape_content file before runing docker compose up.

The models file can be used to pull models on startup if not already present, just add them as a list one per line.

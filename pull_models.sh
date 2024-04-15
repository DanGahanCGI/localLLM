#!/bin/sh

while IFS= read -r model || [ -n "$model" ]; do
    curl -X POST \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$model\"}" \
    http://ollama:11434/api/pull
done < /opt/models
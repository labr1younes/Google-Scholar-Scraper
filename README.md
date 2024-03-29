# Google-Scholar-Scraper

## Overview

This Python script scrapes data from Google Scholar profiles, extracts relevant information, and converts it into a JSON file

## Prerequisites

Before running the script, ensure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

## JSON File Format
The generated JSON file (result.json) follows the following structure:
```
{
  "number_of_pages": 3,
  "number_of_profiles": 15,
  "profiles": [
    {
      "url": "https://scholar.google.com/citations/...",
      "name": "John Doe",
      "job_title": "Researcher",
      "workplace": "University of Example",
      "key_words": "machine learning, artificial intelligence, data science",
      "citations": "50",
      "h-index": "10",
      "i10-index": "5"
    },
    // ... (more profiles)
  ]
}
```

## License
This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code in this repository for personal or commercial purposes.

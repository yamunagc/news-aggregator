# News Information Aggregator

A Python desktop application that aggregates news articles from multiple online sources using a public web API and web scraping. Articles are fetched, enriched, cleaned, and presented through an interactive GUI with live search and data visualisations.

---

## Project Structure

```
news_aggregator/
├── main.py                  
├── requirements.txt                 
├── README.md
├── classes/
│   ├── __init__.py
│   ├── article.py           
│   ├── fetcher.py           
│   ├── scraper.py           
│   ├── processor.py         
│   ├── visualizer.py        
│   └── app.py               
├── tests/
│   ├── __init__.py
│   ├── test_article.py
│   ├── test_fetcher.py
│   └── test_processor.py
└── assets/                  
```

---

## Requirements

- Python 3.9 or higher
- A free NewsAPI key from [newsapi.org](https://newsapi.org/register)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yamunagc/news-aggregator.git
cd news-aggregator
```

### 2. Create a virtual environment

```bash
# Mac / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

- Get a free API key at [newsapi.org/register](https://newsapi.org/register)
- Create a `.env` file in the root folder
- Add your key:

```
NEWS_API_KEY=your_actual_key_here
```

### 5. Run the application

```bash
python main.py
```

---

## How to Use

1. Select a **category** from the dropdown (business, technology, sports, etc.)
2. Select the **number of articles** to fetch (5, 10, 15, or 20)
3. Click **Fetch News** - the app fetches, scrapes, and processes articles
4. Click any article in the left panel to see its full details
5. Use the **search box** to filter articles by title or source
6. Click **Show Charts** to view visualisations
7. Click any article URL to open it in your browser

---

## Running Tests

```bash
python -m unittest discover tests -v
```

---

## Dependencies

| Library | Version | Purpose |
|---|---|---|
| requests | 2.31.0 | HTTP calls to NewsAPI and article pages |
| beautifulsoup4 | 4.12.3 | HTML parsing and web scraping |
| pandas | 2.2.0 | Data merging, deduplication, cleaning |
| matplotlib | 3.8.2 | Bar and pie chart generation |
| newsapi-python | 0.2.7 | NewsAPI wrapper |
| python-dotenv | 1.0.0 | Secure API key loading from .env |
| lxml | 5.1.0 | HTML parser for BeautifulSoup |
| Pillow | 10.2.0 | Embedding chart images in GUI |

---

## Notes

- The `.env` file is listed in `.gitignore` and will never be pushed to GitHub
- Chart images are saved to the `assets/` folder and are also excluded from GitHub
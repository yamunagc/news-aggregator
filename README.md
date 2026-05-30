# News Information Aggregator with Web API and Scraping

## Overview

This project implements a Python-based News Information Aggregator that combines data retrieved from a public web API with additional information extracted through web scraping. The application was developed to satisfy the requirements of the assignment by integrating API consumption, HTML scraping, object-oriented design, data processing, visualization, testing, and graphical user interaction.

The system retrieves current news articles from NewsAPI, enriches article records by scraping source webpages, cleans and consolidates the collected data, and presents the results through a Tkinter-based graphical interface with an analytics dashboard. The implementation emphasizes modular structure, tested functionality, data consistency, and usability.

---

## Objectives

The project addresses the following core objectives:

- retrieval of news articles from a public API,
- extraction of additional article details through web scraping,
- combination of API and scraped data into a consolidated dataset,
- cleaning and normalization of collected data,
- removal of duplicate records,
- visualization of trends in the aggregated dataset,
- application of object-oriented programming principles,
- validation of critical functionality through unit testing,
- and provision of a user-friendly graphical user interface.

---

## Implemented Features

### Core functionality

- Live news retrieval using NewsAPI
- Category-based article fetching
- Configurable number of articles to fetch
- Web scraping of article content, author, and publication metadata where available
- Merging of API metadata with scraped data
- Data cleaning and duplicate removal
- Article browsing and detail viewing through a Tkinter GUI
- Analytics generation using Matplotlib
- Unit testing using Python's built-in `unittest` framework

### Additional functionality

- In-memory caching to reduce repeated API requests
- Search/filter functionality in the GUI
- Improved author cleaning to remove invalid byline text
- Fallback handling for sources that restrict full content extraction

---

## Technologies Used

The implementation uses the following libraries and tools:

- Python 3
- Tkinter
- NewsAPI
- Requests
- BeautifulSoup4
- Pandas
- Matplotlib
- Pillow
- python-dotenv
- unittest

Dependencies are pinned to specific versions in `requirements.txt` to improve reproducibility across execution environments.

---

## Requirements

The project uses the following dependency versions:

```txt
newsapi-python==0.2.7
requests==2.31.0
beautifulsoup4==4.12.3
pandas==2.2.0
matplotlib==3.8.2
python-dotenv==1.0.0
Pillow==11.2.1
```

---

## Project Structure

```text
news-aggregator/
│
├── classes/
│   ├── __init__.py
│   ├── app.py
│   ├── article.py
│   ├── fetcher.py
│   ├── processor.py
│   ├── scraper.py
│   └── visualizer.py
│
├── tests/
│   ├── __init__.py
│   ├── test_article.py
│   ├── test_fetcher.py
│   ├── test_processor.py
│   └── test_scraper.py
│
├── charts/          ← created automatically on first run
├── .env
├── main.py
├── requirements.txt
└── README.md
```

> **Note:** The `charts/` directory is not included in the repository. It is created automatically the first time the application generates visualisations.

---

## Architecture

The codebase follows an object-oriented design in which responsibilities are divided across dedicated classes.

### Main classes

#### `NewsArticle`
Base data model representing a generic article with shared fields such as title, URL, source, category, and publication date.

#### `APIArticle`
Subclass of `NewsArticle` representing article metadata obtained from NewsAPI, including description, image URL, and author fields.

#### `ScrapedArticle`
Subclass of `APIArticle` extended with scraped article content.

#### `NewsFetcher`
Handles communication with NewsAPI, validation of categories, fetch count handling, and request caching.

#### `Scraper`
Retrieves source webpages, extracts relevant content and metadata, and applies fallback logic when full scraping is unavailable.

#### `DataProcessor`
Merges article records, removes duplicates, cleans fields, standardizes metadata, and prepares structured data for analysis.

#### `Visualizer`
Generates analytics charts for article sources, categories, authors, and frequent title keywords.

#### `NewsApp`
Builds the Tkinter interface, manages user interaction, displays article content, and opens the analytics dashboard.

This structure improves modularity, maintainability, testability, and clarity of implementation.

---

## Environment Setup and Execution

The application is executed from the project root using a Python virtual environment. A virtual environment is used to isolate project dependencies from the global Python installation and ensure more predictable behavior across systems.

### 1. Open the project directory

The application should be executed from the folder containing `main.py`, `requirements.txt`, and the `classes/` directory.

Example:

```cmd
cd C:\Users\Usam\Downloads\news-aggregator
```

### 2. Confirm Python is available

A Python 3 installation is required.

```cmd
python --version
```

A valid Python version should be displayed.

### 3. Create a virtual environment

Create an isolated environment in the project root:

```cmd
python -m venv venv
```

### 4. Activate the virtual environment

On Windows Command Prompt:

```cmd
venv\Scripts\activate
```

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

After activation, the terminal typically shows a `(venv)` prefix.

### 5. Install dependencies

Install the required packages from `requirements.txt`:

```cmd
pip install -r requirements.txt
```

This installs all libraries required for API requests, scraping, processing, visualization, environment variable loading, and image handling.

---

## API Configuration

The application requires a valid NewsAPI key.

A `.env` file must be created in the project root directory. The file should contain the following entry:

```env
NEWS_API_KEY=your_actual_newsapi_key_here
```

### Notes

- The file name must be exactly `.env`
- The variable name must be exactly `NEWS_API_KEY`
- The file must be located in the same root directory as `main.py`
- The API key must be valid at runtime

The application uses `python-dotenv` to load this configuration automatically when it starts.

---

## Running the Application

Once the environment has been prepared and the `.env` file has been configured, the application can be launched from the project root.

```cmd
python main.py
```

### Runtime behavior

When the application starts successfully, the Tkinter GUI opens and provides the following workflow:

1. a news category is selected,
2. the number of articles to fetch is selected,
3. the fetch action is initiated,
4. the application retrieves metadata from NewsAPI,
5. additional article details are scraped from source webpages where possible,
6. the data is cleaned and consolidated,
7. the article list is displayed,
8. individual article records can be inspected in detail,
9. and analytics charts can be opened through the dashboard view.

### Interface capabilities

The GUI provides:

- category selection,
- fetch count selection,
- article retrieval controls,
- article list display,
- source and metadata display,
- content display,
- search/filter functionality,
- status messages,
- and chart access through an analytics window.

---

## Typical Execution Sequence

A complete Windows execution sequence is:

```cmd
cd C:\Users\Usam\Downloads\news-aggregator
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

If tests are to be run before application launch, the sequence becomes:

```cmd
cd C:\Users\Usam\Downloads\news-aggregator
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py" -v
python main.py
```

---

## Running the Test Suite

The project includes unit tests covering critical functionality.

### Run all tests

```cmd
python -m unittest discover -s tests -p "test_*.py" -v
```

### Run individual test modules

```cmd
python -m unittest tests.test_article
python -m unittest tests.test_fetcher
python -m unittest tests.test_processor
python -m unittest tests.test_scraper
```

### Covered behaviors

The test suite validates key behaviors such as:

- dataclass default values and article type identification,
- category normalization in the fetch layer,
- caching behavior,
- duplicate removal,
- metadata cleaning,
- invalid author filtering,
- scrape fallback behavior,
- and extraction of valid article content.

---

## Data Acquisition and Processing

The system combines two complementary data acquisition methods:

- API-based retrieval for structured article metadata,
- and webpage scraping for additional content and metadata not reliably provided by the API.

After retrieval, records are processed through a cleaning and normalization pipeline.

### Processing steps

- text normalization,
- duplicate removal,
- category standardization,
- author cleanup,
- content cleanup,
- invalid metadata suppression,
- and conversion into a Pandas DataFrame for analysis.

Special attention was given to noisy author fields, especially cases where webpage interface text or page metadata was mistakenly captured as an author name. Cleaning logic was introduced to prevent such values from appearing in the analytics output.

---

## Data Visualization

The analytics component uses Matplotlib to generate charts that summarize the dataset. Implemented visualizations include:

- Articles by Source
- Articles by Category
- Top Authors
- Frequent Title Keywords

These charts support exploratory analysis of the retrieved and processed news data.

---

## Caching

An in-memory caching mechanism was implemented in the fetch layer to reduce redundant API calls for repeated requests. This improves efficiency during repeated use and addresses the optional assignment feature relating to caching.

---

## Reliability and Error Handling

The project includes safeguards intended to improve runtime reliability:

- validation of unsupported categories,
- detection of missing API keys,
- fallback handling for failed scraping,
- support for partial data when websites restrict access,
- filtering of invalid author values,
- and controlled GUI updates during background fetching operations.

These measures improve resilience when working with third-party APIs and variable webpage structures.

---

## Ethical Considerations

The application uses publicly available API data and limited webpage scraping for educational purposes. The implementation avoids aggressive extraction behavior and uses caching to reduce unnecessary repeated requests. Where publishers restrict content access, the system falls back to partial information rather than attempting intrusive collection.

---

## Limitations

The implementation has several practical limitations:

- some websites restrict full article scraping,
- full article content is not always available,
- author metadata may be absent or inconsistent,
- webpage structures may change over time,
- analytics depend on the quality of runtime data,
- and external API limits may affect article retrieval.

Fallback behavior and cleaning logic are included to reduce the effect of these constraints.

---
University of Technology Sydney  
Assignment: Information Aggregator with Web API and Scraping

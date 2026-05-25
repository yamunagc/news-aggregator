# News Information Aggregator with Web API and Scraping

## Overview

This project implements a Python-based News Information Aggregator that combines data retrieved from a public web API with additional information extracted through web scraping. The system was developed to address the assignment requirements for integrating API consumption, HTML scraping, object-oriented design, data processing, visualization, testing, and graphical user interaction.

The application retrieves current news articles from NewsAPI, enriches article records by scraping source webpages, cleans and consolidates the collected data, and presents the results through a Tkinter-based interface with an analytics dashboard. The final implementation emphasizes modular architecture, tested functionality, data consistency, and usability.

---

## Objectives

The project addresses the following functional and design objectives:

- integration of a public news API for article retrieval, [file:374]
- extraction of additional article details through web scraping, [file:374]
- combination of API and scraped data into a consolidated dataset, [file:374]
- data cleaning, duplicate removal, and consistency handling, [file:374]
- visualization of article trends using charts, [file:374]
- application of object-oriented programming principles, [file:374]
- validation of critical functionality through unit testing, [file:374]
- and provision of a user-friendly graphical interface for exploration of the aggregated data. [file:374]

---

## Feature Summary

The implemented system includes the following features:

- live news retrieval using NewsAPI,
- category-based article fetching,
- configurable fetch count,
- web scraping of article content, author, and publication metadata where available,
- duplicate removal and structured data cleaning,
- analytics generation using Matplotlib,
- Tkinter-based article browsing and detailed article viewing,
- local caching to reduce repeated API requests,
- search and filtering within the GUI,
- and unit tests for core behaviors. [file:374]

In addition to the required baseline functionality, the system includes processing improvements for noisy bylines and scraped metadata, ensuring that charts such as Top Authors remain meaningful rather than reflecting webpage interface artifacts. [file:374]

---

## System Architecture

The codebase follows an object-oriented structure in which responsibilities are separated into focused classes.

### Core classes

#### `NewsArticle`
Base data model representing a generic news article with shared fields such as title, URL, source, category, and publication date.

#### `APIArticle`
Subclass of `NewsArticle` representing article data returned from NewsAPI, with support for description, image URL, and author metadata.

#### `ScrapedArticle`
Subclass of `APIArticle` extended with scraped article content.

#### `NewsFetcher`
Responsible for interaction with NewsAPI, validation of categories, fetch count handling, and caching of recent requests.

#### `Scraper`
Responsible for retrieving article webpages, extracting useful content and metadata, and handling fallback behavior when full extraction is not possible.

#### `DataProcessor`
Responsible for merging records, removing duplicates, cleaning content, standardizing metadata, and preparing tabular data for analysis.

#### `Visualizer`
Responsible for generating article analytics charts such as source distribution, category distribution, top authors, and title keywords.

#### `NewsApp`
Responsible for graphical user interaction, event handling, article display, and integration of analytics into the Tkinter interface.

This separation improves maintainability, readability, and testability while also demonstrating encapsulation, inheritance, and modular design. [file:374]

---

## Technologies and Dependencies

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

The project dependencies are pinned to specific versions in order to preserve reproducibility across environments. Repeatable dependency installation is a standard way to reduce variation between development and evaluation environments. [web:435][file:374]

### `requirements.txt`

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
│   ├── test_fetcher.py
│   ├── test_processor.py
│   └── test_scraper.py
│
├── charts/
├── .env
├── main.py
├── requirements.txt
└── README.md
```

---

## Execution

### Environment preparation

The application is executed from the project root using a Python virtual environment created with `venv`, which is the standard library module for isolated Python environments. Isolated environments help avoid conflicts with globally installed packages and support more predictable execution. [web:450][web:451]

Typical execution consists of:
1. creating a virtual environment,
2. activating the environment,
3. installing dependencies from `requirements.txt`,
4. configuring the required API key in a `.env` file,
5. and running the application entry point. [web:450][web:455][file:374]

### Environment variable configuration

The application requires a valid NewsAPI key. This key is loaded from a `.env` file through `python-dotenv`, which supports configuration through environment variables rather than hardcoding secrets into source files. [web:455][web:457]

The `.env` file must contain:

```env
NEWS_API_KEY=your_actual_newsapi_key_here
```

The `.env` file should be placed in the project root directory alongside `main.py`.

### Application launch

The application is launched through the main entry point:

```cmd
python main.py
```

When successfully started, the Tkinter GUI opens and provides controls for category selection, fetch count selection, article retrieval, article browsing, search/filtering, and chart display. [file:374]

### Execution flow

At runtime, the application performs the following sequence:

1. reads the NewsAPI key from the environment,
2. retrieves article metadata from NewsAPI,
3. converts API responses into structured article objects,
4. requests source webpages for enrichment,
5. scrapes additional content and metadata where available,
6. cleans and consolidates the combined dataset,
7. updates the GUI with processed article results,
8. and generates visual analytics on demand. [file:374]

### Typical operating sequence

Within the GUI, the expected operating sequence is:

1. select a category,
2. select the number of articles to retrieve,
3. initiate data retrieval,
4. review the fetched article list,
5. inspect individual article details,
6. and open the analytics dashboard for visualization of the processed dataset.

---

## Testing

The project includes unit tests implemented with Python’s built-in `unittest` framework, consistent with the assignment requirement for reliable and tested code. [file:374]

### Test coverage

The current test suite covers critical behaviors including:

- API fetch behavior and category normalization,
- API caching behavior,
- duplicate removal,
- content cleaning,
- author cleaning,
- scrape fallback logic,
- and extraction of valid article paragraphs.

### Test execution

All tests are executed with:

```cmd
python -m unittest discover -s tests -p "test_*.py" -v
```

Individual test modules may also be executed independently:

```cmd
python -m unittest tests.test_fetcher
python -m unittest tests.test_processor
python -m unittest tests.test_scraper
```

This testing approach provides evidence that major components behave correctly under expected and edge-case conditions. [file:374]

---

## Data Acquisition and Processing

The project combines two complementary data acquisition strategies:

- API-based retrieval for structured headline and metadata access, [file:374]
- and scraping-based retrieval for richer article-specific content not consistently available from the API. [file:374]

The resulting records are merged and then processed to improve data quality.

### Processing tasks

The processing pipeline includes:

- text normalization,
- duplicate removal,
- category standardization,
- author cleaning,
- content cleanup,
- and DataFrame generation for analysis.

Special attention was given to handling malformed or noisy author fields, particularly cases where webpage interface text was incorrectly captured as an author name. Cleaning rules were introduced to suppress such noise so that analytics remain interpretable. [file:374]

This processing stage is central to the quality of the final output because the usefulness of charts and article summaries depends directly on the reliability and consistency of the merged dataset. [file:374]

---

## Visualization

The analytics component uses Matplotlib to generate charts that summarize the aggregated dataset. The implemented visualizations include:

- articles by source,
- articles by category,
- top authors,
- and frequent title keywords. [file:374]

These charts provide a compact representation of the dataset and support exploratory inspection of the retrieved news articles. Data cleaning improvements were especially important for author and keyword charts, where noisy inputs could otherwise distort interpretation. [file:374]

---

## Graphical User Interface

The application interface is implemented using Tkinter, as permitted by the assignment brief. [file:374]

### Main interface elements

The GUI provides:

- category selection,
- article count selection,
- fetch controls,
- search/filter functionality,
- article list display,
- article metadata and content display,
- source link access,
- status feedback,
- and access to the analytics dashboard.

The interface design prioritizes clarity, straightforward interaction, and support for real-time exploration of aggregated data, aligning with the assignment’s focus on a user-friendly and interactive tool. [file:374]

---

## Caching

An in-memory caching mechanism was implemented in the API retrieval layer to reduce redundant calls for recently requested article sets. This supports the optional feature relating to caching and helps reduce unnecessary API requests and repeated processing. [file:374]

Caching improves practical efficiency during repeated use of the same category and fetch count combinations, particularly during testing and demonstration.

---

## Reliability and Error Handling

The codebase includes several mechanisms intended to improve robustness:

- validation of invalid categories,
- safe handling of missing API keys,
- fallback messaging when scraping fails,
- partial-content handling for restricted publishers,
- filtering of invalid author strings,
- and controlled GUI updates during threaded fetch operations.

These decisions were made to ensure that the application remains usable even when external services or webpage structures are inconsistent.

---

## Ethical and Legal Considerations

The project uses publicly available API data and limited webpage scraping for educational purposes. The implementation avoids aggressive crawling behavior and uses caching to reduce unnecessary repeated requests. Where websites limit the extraction of complete content, the application falls back to partial data rather than attempting intrusive collection. Ethical and legal considerations are an important part of responsible web data use and are explicitly relevant to this assignment context. [file:374]

---

## Limitations

The current implementation has several practical limitations:

- some publishers restrict full article access,
- source webpage structures vary and may affect scraping reliability,
- author metadata is not always available or trustworthy,
- analytics depend on the quality and diversity of runtime data,
- and API rate or access limits may affect available results.

Despite these constraints, the system includes fallback handling and cleaning logic to reduce the impact of incomplete or noisy third-party data.

---

## Submission Components

In addition to the source code, the overall submission package includes:

- the Python codebase structured around OOP principles, [file:374]
- unit tests, [file:374]
- this README with execution and dependency documentation, [file:374]
- GUI screenshots, [file:374]
- a brief report discussing design decisions and challenges, [file:374]
- and a presentation/video component as required by the assignment brief. [file:374]

---

## Screenshots

The final submission includes interface screenshots documenting:

- the main GUI,
- article retrieval results,
- detailed article view,
- analytics dashboard output,
- and successful unit test execution. [file:374]

---

University of Technology Sydney  
Assignment: Information Aggregator with Web API and Scraping

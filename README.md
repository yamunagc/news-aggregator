# News Information Aggregator with Web API and Scraping

## Overview

This project is a Python-based News Information Aggregator developed for the assignment **Information Aggregator with Web API and Scraping**. The program combines data collected from a public news API with additional information extracted through web scraping to create a richer and more interactive news exploration tool.

The application demonstrates the integration of:
- web API requests,
- HTML scraping,
- data cleaning and processing,
- object-oriented software design,
- data visualization,
- unit testing,
- and a graphical user interface (GUI).

The final system allows users to fetch recent news articles, enrich them with scraped article data, browse them through a Tkinter application, and view analytics about the collected dataset.

---

## Assignment Objectives Addressed

This project was designed to address the major goals of the assignment:

- Fetch news from a public API
- Scrape additional article details from source webpages
- Combine API and scraped data into a more complete dataset
- Clean data and remove duplicates
- Visualize article trends using charts
- Apply Object-Oriented Programming (OOP) principles
- Implement unit tests for critical functions
- Provide a user-friendly GUI
- Include optional features such as article count selection and caching

---

## Features

### Core Features

- Live news headline fetching using **NewsAPI**
- Category-based article retrieval
- Configurable number of articles to fetch
- Web scraping for additional article details such as:
  - article content,
  - author,
  - publication date
- Merging API data with scraped data
- Duplicate removal and data cleaning
- Visualization of aggregated data using charts
- Tkinter GUI for interactive use

### Additional Features

- Local in-memory caching to reduce unnecessary repeated API calls
- Search/filter bar in the GUI
- Analytics dashboard window
- Improved author cleaning to remove invalid byline text
- Fallback handling when article scraping is limited or unavailable

---

## Technologies Used

The project uses the following tools and libraries:

- **Python 3**
- **Tkinter** for GUI development
- **NewsAPI** for news article retrieval
- **Requests** for HTTP requests
- **BeautifulSoup4** for HTML parsing and scraping
- **Pandas** for structured data handling
- **Matplotlib** for analytics visualizations
- **Pillow** for image/chart rendering in Tkinter
- **python-dotenv** for environment variable loading
- **unittest** for automated testing

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

## OOP Design and Architecture

The application was designed using Object-Oriented Programming principles to improve modularity, readability, maintainability, and extensibility.

### Main Classes

#### `NewsArticle`
Base class representing a generic article with shared fields such as:
- title
- URL
- source
- category
- publication date

#### `APIArticle`
Extends `NewsArticle` to represent articles fetched from NewsAPI and includes:
- description
- image URL
- author

#### `ScrapedArticle`
Extends `APIArticle` by adding:
- full or partial scraped article content

#### `NewsFetcher`
Responsible for:
- connecting to NewsAPI,
- validating categories,
- fetching article data,
- and caching results to reduce repeated API requests.

#### `Scraper`
Responsible for:
- requesting article webpages,
- extracting additional information from HTML,
- cleaning scraped content,
- and providing fallback content when full extraction is unavailable.

#### `DataProcessor`
Responsible for:
- merging articles,
- removing duplicates,
- cleaning invalid data,
- standardizing fields,
- and converting article objects into a structured DataFrame for analysis.

#### `Visualizer`
Responsible for:
- generating charts for article analytics,
- such as articles by source, category, authors, and title keywords.

#### `NewsApp`
Responsible for:
- building and managing the Tkinter GUI,
- handling user interactions,
- displaying article content,
- and opening the analytics dashboard.

### OOP Principles Demonstrated

- **Encapsulation**: each class handles a specific responsibility
- **Inheritance**: `APIArticle` and `ScrapedArticle` extend the base `NewsArticle`
- **Modularity**: separate classes manage fetching, scraping, processing, visualization, and UI
- **Maintainability**: functionality is organized cleanly instead of being placed in one procedural script

---

## Installation and Setup

### 1. Download or clone the project

Place the project in a local working directory.

Example:

```cmd
C:\Users\Usam\Downloads\news-aggregator
```

### 2. Create a virtual environment

Open a terminal in the project root and run:

```cmd
python -m venv venv
```

### 3. Activate the virtual environment

On Windows:

```cmd
venv\Scripts\activate
```

### 4. Install required dependencies

```cmd
pip install -r requirements.txt
```

---

## Requirements

This project uses the following pinned package versions:

```txt
newsapi-python==0.2.7
requests==2.31.0
beautifulsoup4==4.12.3
pandas==2.2.0
matplotlib==3.8.2
python-dotenv==1.0.0
Pillow==11.2.1
```

Version pinning is used to improve reproducibility and ensure the project runs with the same dependency versions used during development and testing. [web:435]

---

## API Key Setup

This project uses **NewsAPI**, which requires an API key.

### Steps

1. Create an account at [NewsAPI](https://newsapi.org/)
2. Generate your API key
3. Create a file named `.env` in the project root
4. Add the following line:

```env
NEWS_API_KEY=your_actual_newsapi_key_here
```

### Important Note

Do **not** submit your real API key in the final assignment submission. If needed, submit an empty `.env.example` file instead, or mention in the README that the `.env` file must be created locally.

---

## How to Run the Application

From the project root, run:

```cmd
python main.py
```

This launches the Tkinter GUI.

### Using the Application

1. Select a news category from the dropdown menu
2. Select how many articles to fetch
3. Click **Fetch News**
4. Wait for API retrieval, scraping, and processing to complete
5. Browse the articles listed on the left panel
6. Click an article to view its full details on the right panel
7. Click **Analytics** to open the data visualization dashboard

---

## GUI Overview

The Tkinter GUI was designed to provide a user-friendly interface for exploring aggregated news data.

### Main GUI Components

- **Category selector**: allows users to choose a news category
- **Fetch count selector**: allows users to choose the number of articles to retrieve
- **Fetch button**: starts the aggregation process
- **Search bar**: filters displayed articles
- **Article list panel**: displays fetched articles
- **Article details panel**: displays title, metadata, source link, author, and content
- **Analytics button**: opens the dashboard with charts
- **Status bar**: shows fetch and processing status

### Analytics Dashboard

The dashboard displays generated charts for:
- article count by source,
- article count by category,
- top authors,
- and frequent title keywords.

---

## Data Collection Workflow

The application follows this general workflow:

1. Fetch article metadata from NewsAPI
2. Convert API responses into `APIArticle` objects
3. Visit article webpages using HTTP requests
4. Scrape useful content such as article text, authors, and dates
5. Store enriched data as `ScrapedArticle` objects
6. Merge all data into a combined collection
7. Clean and standardize the dataset
8. Remove duplicates
9. Display the cleaned results in the GUI
10. Generate analytical visualizations from the processed data

---

## Data Processing and Cleaning

The data processing stage is important because API and scraped content may be inconsistent, incomplete, or noisy.

### Cleaning tasks performed

- Removal of duplicate articles based on title and URL
- Standardization of categories to lowercase values
- Cleanup of article titles, descriptions, and content
- Cleanup of noisy author strings
- Filtering invalid metadata such as:
  - "Share"
  - "Save"
  - "Add as preferred on Google"
  - timestamp fragments such as "1 day ago"
  - publisher fragments inserted into bylines
- Replacement of missing authors with `"Unknown"`
- Removal of noisy page fragments from article content
- Conversion of cleaned data into a Pandas DataFrame for analysis

### Example issue addressed

Some scraped pages returned bylines that contained non-author metadata instead of actual names. These were cleaned so that the Top Authors chart displays meaningful author names rather than page interface text.

---

## Data Visualization

The application uses **Matplotlib** to generate the following visualizations:

- **Articles by Source**
- **Articles by Category**
- **Top Authors**
- **Frequent Title Keywords**

These visualizations help the user identify:
- which publishers contributed the most articles,
- which categories are most represented,
- which authors appear most often,
- and which keywords occur frequently in article titles.

---

## Caching

The project includes simple caching in the API fetcher.

### Purpose of caching

- reduce repeated API calls,
- improve responsiveness for repeated requests,
- and reduce unnecessary network traffic.

This supports the optional assignment feature related to caching and helps make the application more efficient. [file:374]

---

## Unit Testing

The project includes automated testing using Python’s built-in `unittest` framework.

### Test coverage includes

- API fetch category normalization
- API fetch caching behavior
- duplicate removal
- content and metadata cleaning
- invalid author cleanup
- scrape fallback behavior
- paragraph filtering for scraped content

### Running tests

To run all tests:

```cmd
python -m unittest discover -s tests -p "test_*.py" -v
```

To run individual test files:

```cmd
python -m unittest tests.test_fetcher
python -m unittest tests.test_processor
python -m unittest tests.test_scraper
```

Testing was included to satisfy the assignment requirement for reliable and validated code. [file:374]

---

## Error Handling and Robustness

The application includes several safeguards:

- graceful handling of missing API keys
- validation of invalid categories
- fallback messages when scraping fails
- support for partial article data when websites restrict access
- cleanup rules to avoid invalid chart entries
- GUI-safe background fetching and UI queue updates
- confirmation handling when the application is closed during fetching

These decisions improve resilience and usability.

---

## Ethical and Legal Considerations

This project uses public news data and limited educational scraping. Care was taken to follow ethical use principles:

- public news API used for primary retrieval
- scraping limited to publicly available article pages
- no aggressive crawling or mass extraction
- caching used to reduce repeated requests
- recognition that some publishers restrict content access
- respect for website structure and limited extraction where full access is unavailable

Ethical and legal awareness is an important part of working with web data. [file:374]

---

## Known Limitations

Although the application is functional, several limitations remain:

- some websites block or limit scraping,
- full article content cannot always be extracted,
- author information may still be unavailable for some sources,
- data quality depends on the structure of third-party websites,
- charts depend on the quality and diversity of fetched runtime data,
- and NewsAPI free-tier limitations may affect available results.

Where possible, fallback logic and cleaning rules are used to reduce the impact of these issues.

---

## Screenshots for Submission

Include the following screenshots in the final submission package:

1. Main GUI on startup
2. GUI after fetching articles
3. Article detail view
4. Analytics dashboard
5. Terminal showing successful unit test execution

These screenshots support the submission requirements for GUI implementation evidence. [file:374]

---

## How to Prepare the Final Submission

Before submission, ensure the folder contains:

- all Python source files
- the `tests/` folder
- `README.md`
- `requirements.txt`
- screenshots
- report
- presentation/video materials as required

### Do not include

- `venv/`
- `__pycache__/`
- a real `.env` file containing your API key
- unnecessary temporary files

A clean and well-organized submission improves readability and professionalism.

---

## Possible Future Improvements

If the project were extended further, possible improvements could include:

- exporting cleaned datasets to CSV
- more advanced analytics
- sentiment analysis on article content
- source-specific scraping rules
- asynchronous fetching for faster performance
- persistent caching on disk
- richer GUI filtering and sorting options

---

## Conclusion

This project demonstrates the integration of web APIs, web scraping, data processing, visualization, unit testing, OOP, and GUI development within a single Python application. It was designed to satisfy the assignment requirements while also improving usability, data quality, and code maintainability. [file:374]

---

## Author

**Usam Adhikari**  
University of Technology Sydney  
Assignment: Information Aggregator with Web API and Scraping

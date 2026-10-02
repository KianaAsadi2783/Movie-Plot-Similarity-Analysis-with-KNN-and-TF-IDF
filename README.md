# IMDb Movie Recommendation Engine

This project is a movie recommendation system that finds and suggests similar movies based on user-provided plot summaries. It leverages Natural Language Processing (NLP) techniques, specifically **TF-IDF (Term Frequency - Inverse Document Frequency)** and **Cosine Similarity**, to match user input with a database of top IMDb movies.

## Features
- Calculates term frequencies and inverse document frequencies to represent movie summaries as mathematical vectors.
- Computes cosine similarity to find the top 5 closest matches to a user's input summary.
- Includes a web scraper (using `BeautifulSoup`) to fetch the top 250 IMDb movies and their plot summaries (currently commented out to save time; data is pre-fetched and stored).
- Provides two implementations:
  1. **From Scratch (`IMDb_Manual.py`)**: Implements TF-IDF and cosine similarity calculation using basic mathematical operations and `numpy`.
  2. **Scikit-Learn Version (`IMDb_Scikit.py`)**: Uses the `scikit-learn` library for TF-IDF vectorization and cosine similarity calculation.

## Libraries and Tools
- **Python**
- **BeautifulSoup4 & Requests**: For web scraping (fetching summaries from IMDb)
- **NLTK**: For natural language processing (removing English stopwords)
- **NumPy**: For vector operations and dot product calculations
- **scikit-learn**: Used in the bonus script for efficient machine learning operations

## Requirements
Make sure you have Python installed along with the required libraries. You can install the dependencies using pip:
```bash
pip install requests beautifulsoup4 nltk numpy scikit-learn
```

*Note: You may need to download the `stopwords` dataset from NLTK if you haven't already. You can do this by running `import nltk; nltk.download('stopwords')` in a Python shell.*

## Running the Application
The repository contains pre-scraped and cleaned movie summaries in `Clean_Summaries.json`. This prevents the need to scrape the IMDb website every time the program runs.

1. **Run the manual implementation:**
   ```bash
   python IMDb_Manual.py
   ```
2. **Run the `scikit-learn` implementation:**
   ```bash
   python IMDb_Scikit.py
   ```

## Usage
Upon running the script, it will prompt you to enter a movie summary:
**Example Input:**
> _"a billionaire vigilante fights crime in a dark city"_

**Top 5 Matches:**
1. **The Dark Knight Rises**
2. **The Dark Knight**
3. **Batman Begins**
4. **Cidade de Deus**
5. **Metropolis**

The program will calculate the similarity between your input and the movies in the dataset and output the top 5 matching movies. You can continue entering summaries or stop the script.

## Project Structure
- `IMDb_Manual.py`: Core script implementing TF-IDF and Cosine Similarity from scratch.
- `IMDb_Scikit.py`: Alternative script doing the same tasks using `scikit-learn`.
- `Clean_Summaries.json`: Pre-processed JSON file containing the titles and clean summaries of the IMDb Top 250 movies.

## Authors
- **Kiana Asadi** - [KianaAsadi2783](https://github.com/KianaAsadi2783)
- **Parham Moafi** - [ParhamM83](https://github.com/ParhamM83)

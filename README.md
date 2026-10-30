# IMDb Movie Recommender

A small content-based movie similarity project that compares a manual TF-IDF implementation with scikit-learn.

## Features

- Collects movie titles and plot summaries into a local dataset when source access is permitted
- Implements TF-IDF and cosine similarity with Python's standard library
- Provides a second implementation using scikit-learn's TF-IDF vectorizer and nearest neighbors
- Keeps generated source data out of Git

## Project layout

- crawler.py collects page data into plot_summaries.txt.
- dataset.py reads local title;summary; rows.
- recommender_manual.py ranks titles with the manual TF-IDF implementation.
- recommender_sklearn.py ranks titles with scikit-learn.

## Requirements

- Python 3.10+
- requests
- Beautiful Soup
- scikit-learn

Install dependencies:

    python -m pip install requests beautifulsoup4 scikit-learn

## Prepare data

The dataset is not included. The optional crawler accesses IMDb pages, and their structure can change. Before running it, check the source's current terms and automated-access rules. Do not redistribute scraped plot summaries. For an offline run, provide a dataset you are permitted to use in the same title;summary; format.

When permitted:

    python crawler.py

The crawler writes plot_summaries.txt in the repository root and waits between detail-page requests. Git ignores this generated file.

## Get recommendations

Run either implementation from the repository root:

    python recommender_manual.py
    python recommender_sklearn.py

Enter a short plot description when prompted. Each program prints up to six similar titles with a cosine-similarity score. The query is not written into the dataset.

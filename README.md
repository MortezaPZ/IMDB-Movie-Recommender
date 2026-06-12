# 🎬 IMDB Movie Recommender

A content-based movie recommendation system built on the **IMDB Top 250** list. It scrapes plot summaries, computes **TF-IDF** vectors from scratch, and recommends similar movies using **cosine similarity**. 🍿

## ✨ Features

- 🕷️ **Web Scraper** (`crawler.py`) — collects and cleans plot summaries for the IMDB Top 250 movies
- 🧮 **TF-IDF from scratch** — implemented manually with `math` and basic Python (no `sklearn` for the core algorithm)
- 🔍 **Cosine Similarity Search** — takes a short plot description as input and returns the 6 most similar movies
- ⚡ **scikit-learn version** (`main.py`) — an alternative implementation using `TfidfVectorizer` and `KNeighborsClassifier`

## 📂 Project Structure

```
├── crawler.py              # Scrapes plot summaries from IMDB Top 250
├── recommender_manual.py   # TF-IDF + cosine similarity, implemented from scratch
├── recommender_sklearn.py  # TF-IDF + KNN using scikit-learn
└── plot_summaries.txt      # Generated dataset (movie name + cleaned summary)
```

## 🚀 Getting Started

### 1️⃣ Install dependencies

```bash
pip install requests beautifulsoup4 nltk numpy scikit-learn
```

### 2️⃣ Download NLTK stopwords (one-time setup)

```python
import nltk
nltk.download('stopwords')
```

### 3️⃣ Run the crawler to build the dataset

```bash
python crawler.py
```

This creates `plot_summaries.txt`, containing the IMDB Top 250 movie names and their cleaned plot summaries.

### 4️⃣ Get recommendations

```bash
python recommender_manual.py
```

You'll be asked to enter a short summary describing the kind of movie you're looking for. The script appends your input to `plot_summaries.txt`, computes TF-IDF vectors for all 251 entries (250 movies + your input), saves them to `tf_idf_number.txt`, and prints the **6 most similar movies** based on cosine similarity.

Alternatively, run the scikit-learn version:

```bash
python recommender_sklearn.py
```

## 🛠️ How It Works

1. **Scraping** — `crawler.py` fetches the IMDB Top 250 list, visits each movie's plot summary page, and cleans the text (removes punctuation and stopwords).
2. **TF-IDF** — for every word across all summaries, **TF (Term Frequency)** and **IDF (Inverse Document Frequency)** are calculated manually, and combined into a TF-IDF vector for each movie.
3. **Similarity Search** — the user's input summary is vectorized the same way, and **cosine similarity** is used to rank and return the closest matching movies.

## 📝 Notes

- Intermediate files (`p_s_1.txt`, `tf_idf_number.txt`) are generated automatically when running the recommender — no need to create them manually.
- `recommender_manual.py` is meant to demonstrate the math behind TF-IDF and cosine similarity step by step, without relying on machine learning libraries.

##👤 Author
Morteza Pazhoum — @MortezaPZ

K.N. Toosi University of Technology — Computer Science

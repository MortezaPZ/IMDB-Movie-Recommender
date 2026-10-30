"""Content-based recommendations using scikit-learn TF-IDF and nearest neighbors."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

from dataset import load_documents


def main() -> None:
    documents = load_documents()
    titles = [title for title, _ in documents]
    summaries = [summary for _, summary in documents]
    query = input("Describe the kind of movie you want: ").strip()
    if not query:
        print("Enter a non-empty description.")
        return

    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        matrix = vectorizer.fit_transform(summaries)
    except ValueError as error:
        print(f"Could not build the vocabulary: {error}")
        return

    query_vector = vectorizer.transform([query])
    if query_vector.nnz == 0:
        print("No query words matched the dataset vocabulary.")
        return

    neighbors = NearestNeighbors(
        metric="cosine",
        algorithm="brute",
        n_neighbors=min(6, len(documents)),
    )
    neighbors.fit(matrix)
    distances, indices = neighbors.kneighbors(query_vector)

    for rank, (distance, index) in enumerate(zip(distances[0], indices[0]), start=1):
        similarity = max(0.0, 1.0 - float(distance))
        print(f"{rank}. {titles[index]} — similarity {similarity:.3f}")


if __name__ == "__main__":
    main()

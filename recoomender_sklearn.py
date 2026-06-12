from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

with open('plot_summaries.txt', 'r', encoding='utf-8') as f:
    plot_summaries = [line.strip() for line in f.read().strip().split(';')]

input_summary = input('Please input the summary: ') # Get input summary from user
text_summaries = [summary for summary in plot_summaries[1::2]] # Extract text summaries

tfidf_vectorizer = TfidfVectorizer() # Create a TF-IDF vectorizer 
tfidf_matrix = tfidf_vectorizer.fit_transform(text_summaries) # transform the text summaries into a TF-IDF matrix

knn = KNeighborsClassifier(n_neighbors=5, metric='cosine') # crrat the Object of KNeighborsClassifier class
knn.fit(tfidf_matrix, range(len(text_summaries))) # fit the KNN

input_matrix = tfidf_vectorizer.transform([input_summary]) # Transform the input summary into a TF-IDF matrix 

cosine, recommendation_array = knn.kneighbors(input_matrix, n_neighbors=5) # Find the top 5 nearest neighbors

def main(): # Define the main function to print the recommended summaries
    for rank, index in enumerate(recommendation_array[0]):
        print(f"Rank {rank + 1}: {plot_summaries[index * 2]}")

if __name__ == "__main__":
    main()

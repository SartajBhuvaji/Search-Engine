# TF-IDF Document Search Engine



This project is part of the CPSC 5330 Big Data Analytics course and involves the development of a powerful TF-IDF Document Search Engine. The goal of this project is to create a system that can intelligently search and retrieve the most relevant documents for a given user query. TF-IDF (Term Frequency-Inverse Document Frequency) is a popular information retrieval technique used to assess the importance of terms in a document collection.

## Key Features
- Efficient Document Retrieval: Our search engine is optimized to quickly find and return documents that are most relevant to a user's query, enhancing the user's experience.

- Scalability: The engine is designed to handle large document collections, making it suitable for applications with extensive datasets.

- Flexible Querying: Users can input a wide range of queries, from single terms to complex phrases, and receive meaningful results.

- TF-IDF Ranking: We employ TF-IDF ranking to determine the significance of terms in documents, ensuring the most relevant documents are prioritized.


## Output
1 
![lab5sc1](https://github.com/SartajBhuvaji/Search-Engine/assets/31826483/721d1657-b644-4718-b345-504add149be0)

2
![lab5sc2](https://github.com/SartajBhuvaji/Search-Engine/assets/31826483/de458763-5658-49d6-a49d-1e5f857562dc)

## About TF-IDF [1]
TF-IDF (Term Frequency-Inverse Document Frequency) is a combination of two individual metrics, TF and IDF, respectively. TF-IDF is used when we have multiple documents. It is based on the idea that rare words contain more information about the content of a document than words that are used many times throughout all the documents.

A problem with scoring word frequency is that highly frequent words start to dominate in the document, but may not contain as much “informational content” to the model as rarer but perhaps domain-specific words. One approach is to rescale the frequency of words by how often they appear in all documents so that the scores for frequent words that are also frequent across all documents are penalized.

TF and IDF are calculated with the following formulas:
![tf-idf calculation](https://github.com/SartajBhuvaji/Search-Engine/assets/31826483/c15f0c0c-653d-4a1b-8152-ef14f176acdb)


where d refers to a document, N is the total number of documents, df is the number of documents with the term t. TF-IDF are word frequency scores that try to highlight words that are more interesting. The scores have the effect of highlighting words that are distinct in a given document.

The predictive modeling can be implemented by Python with scikit-learn. The TfidfVectorizer can tokenize documents, learn the vocabulary and inverse document frequency weightings, and encode new documents. Alternately, if there is a learned CountVectorizer, TfidfTransformer can be used to just calculate the inverse document frequencies and start encoding documents.


## References
- [1] "Introduction to Natural Language Processing — TF-IDF", By Kinder Chen, https://kinder-chen.medium.com/introduction-to-natural-language-processing-tf-idf-1507e907c19

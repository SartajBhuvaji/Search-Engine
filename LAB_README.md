# Lab 5: My Search Engine

This is a continuation of the TFIDF search system we started in Lab 3. 
In this lab, you will build your "search engine" that uses the TFIDF data produced in lab 3.
Lab 3 focused on the *Indexing (ingestion) Phase*, which took a set (corpus) of documents as input, and produced a set of parameters of the form `tfidf(doc_id, term)` for every document in the corpus and every term in every document.  

Now we move to build the *Query Phase*: 
The query phase is separate from the Index Phase. It is an interactive Flask web application written in Python, which works as follows:
1. a user inputs a line of words on the query webpage in a browser
2. the user input is sent to your web application on the EC2 server (where you host and run your Flask application)
3. the server (your Flask app) splits user input into words and converts them to terms just as in the indexing phase, so a query is a set of terms after removing stopwords (use the same stopwords.py)
4. the server queries your DynamoDB table to get TF-IDF values with respect to the query  
5. the server calculates a **relevance score** using this formula: $𝑟𝑒𝑙𝑒𝑣𝑎𝑛𝑐𝑒(𝑑𝑜𝑐, 𝑄) = \sum_{𝑡𝑒𝑟𝑚∈𝑄} \frac{𝑡𝑓𝑖𝑑𝑓(𝑑𝑜𝑐, 𝑡𝑒𝑟𝑚)}{|𝑄|}$, where $|𝑄|$ is the length of the terms in a user query.
6. based on the relevance score, the server selects and sends the user the five most relevant documents, in descending order of relevance – or fewer if there are fewer than five documents with relevance > 0
7. the user sees the relevant documents on a query result webpage

Note that the TF-IDF values are given in a `tfidf.csv` file, and you need to import it into your DynamoDB table, which will be queried by your Flask application. Besides, a `tfidf-small.csv` is also provided in this lab. You can used it to explore DynamoDB importing which could be efficient due to its smaller size.

### Grading and Requirements
When grading this lab, the grader will:
1. upload your code to an EC2 instance
2. configure AWS credentials (they can be obtained from Instructor's account, so you don't need to do anything)
3. run `python3 main.py` from your code folder
4. visit http://EC2_PUBLIC_IP:5330 and input queries to test your app

The above process infers the following **requirements**:
1. Your Flask web app must listen at port 5330  
2. The entry point of your web app must be `main.py` in your code folder
3. No arguments will be provided when running `python3 main.py`
4. You should use relative path whenever needed since the EC2 instance used for grading differs from yours.
5. Your DynamoDB table should exist (so don't delete it before the grading of this lab is released)

### Extra Credits (5 points)
I'll select up to two submissions that have a good UX/UI, and use them as demos for the future class. 
Something I am looking for includes, but is not limited to:
1. Robust code (clearly shouldn't crash when demonstrating)
2. Good-looking webpage
3. Augmented query results (e.g., returning the title and a summary of this book)

Winners will get five extra points. 
Note that there is no concrete rubric for selection, and hence it could be subjective to a certain extent, so feel free to skip this part of the lab. 

### Sample Output 
Note that this output is for calibrating your relevance score calculation. 
You can have different layout/UI design on your webpage.  
User query: *my brother is a whale, cool!*
| docid              | relevance score         |
|--------------------|-------------------------|
| melville-moby_dick | 720.9601429483332        |
| bryant-stories     | 88.87629390000001        |
| edgeworth-parents  | 24.470701442333333       |
| austen-sense       | 21.86658240066667        |
| shakespeare-caesar | 21.41452286666667        |


## Submission
A zip file with  
  1. a `code` folder that contains all your implementations. Make sure the `main.py` exists in this folder
  2. a retrospective report in `pdf`, a reflection on the assignment, with the following components:  
      - Your name   
      - How much time you spent on the assignment   
      - Were there aspects of the assignment that were particularly challenging or confusing?   
      - What were the main learning takeaways from this lab – that is, did it introduce 
         particular concepts or techniques that might help you as an analyst or engineer 
         in the future?

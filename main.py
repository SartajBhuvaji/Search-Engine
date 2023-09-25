# Lab 5: My Search Engine
# By: Sartaj Bhuvaji

from flask import Flask, render_template, request, render_template_string
from collections import defaultdict
from boto3.dynamodb.conditions import Key
import boto3
import re

#from stopwords import stopwords_set
stopwords_set = set(["a", "as", "able", "about", "above", "according", "accordingly",
       "across", "actually", "after", "afterwards", "again", "against", "aint", "all", "allow",
       "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among",
       "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway",
       "anyways", "anywhere", "apart", "appear","appreciate", "appropriate", "are", "arent", "around",
       "as", "aside", "ask", "asking", "associated", "at", "available", "away", "awfully", "be", "became",
       "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "believe", "below",
       "beside", "besides", "best", "better", "between", "beyond", "both", "brief", "but", "by", "cmon",
       "cs", "came", "can", "cant", "cannot", "cant", "cause", "causes", "certain", "certainly", "changes",
       "clearly", "co", "com", "come", "comes", "concerning", "consequently", "consider", "considering", "contain", "containing",
       "contains", "corresponding", "could", "couldnt", "course", "currently", "definitely", "described", "despite", "did", "didnt",
       "different", "do", "does", "doesnt", "doing", "dont", "done", "down", "downwards", "during", "each",
       "edu", "eg", "eight", "either", "else", "elsewhere", "enough", "entirely", "especially", "et", "etc",
       "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except",
       "far", "few", "ff", "fifth", "first", "five", "followed", "following", "follows", "for", "former",
       "formerly", "forth", "four", "from", "further", "furthermore", "get", "gets", "getting", "given", "gives",
       "go", "goes", "going", "gone", "got", "gotten", "greetings", "had", "hadnt", "happens", "hardly",
       "has", "hasnt", "have", "havent", "having", "he", "hes", "hello", "help", "hence", "her",
       "here", "heres", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself",
       "his", "hither", "hopefully", "how", "howbeit", "however", "i", "id", "ill", "im", "ive",
       "ie", "if", "ignored", "immediate", "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates",
       "inner", "insofar", "instead", "into", "inward", "is", "isnt", "it", "itd", "itll", "its",
       "its", "itself", "just", "keep", "keeps", "kept", "know", "knows", "known", "last", "lately",
       "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely",
       "little", "look", "looking", "looks", "ltd", "mainly", "many", "may", "maybe", "me", "mean",
       "meanwhile", "merely", "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself",
       "name", "namely", "nd", "near", "nearly", "necessary", "need", "needs", "neither", "never", "nevertheless",
       "new", "next", "nine", "no", "nobody", "non", "none", "noone", "nor", "normally", "not",
       "nothing", "novel", "now", "nowhere", "obviously", "of", "off", "often", "oh", "ok", "okay",
       "old", "on", "once", "one", "ones", "only", "onto", "or", "other", "others", "otherwise",
       "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "own", "particular", "particularly",
       "per", "perhaps", "placed", "please", "plus", "possible", "presumably", "probably", "provides", "que", "quite",
       "qv", "rather", "rd", "re", "really", "reasonably", "regarding", "regardless", "regards", "relatively", "respectively",
       "right", "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing",
       "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously",
       "seven", "several", "shall", "she", "should", "shouldnt", "since", "six", "so", "some", "somebody",
       "somehow", "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify",
       "specifying", "still", "sub", "such", "sup", "sure", "ts", "take", "taken", "tell", "tends",
       "th", "than", "thank", "thanks", "thanx", "that", "thats", "thats", "the", "their", "theirs",
       "them", "themselves", "then", "thence", "there", "theres", "thereafter", "thereby", "therefore", "therein", "theres",
       "thereupon", "these", "they", "theyd", "theyll", "theyre", "theyve", "think", "third", "this", "thorough",
       "thoroughly", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too",
       "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "twice", "two", "un",
       "under", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon", "us", "use", "used",
       "useful", "uses", "using", "usually", "value", "various", "very", "via", "viz", "vs", "want",
       "wants", "was", "wasnt", "way", "we", "wed", "well", "were", "weve", "welcome", "well",
       "went", "were", "werent", "what", "whats", "whatever", "when", "whence", "whenever", "where", "wheres",
       "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who",
       "whos", "whoever", "whole", "whom", "whose", "why", "will", "willing", "wish", "with", "within",
       "without", "wont", "wonder", "would", "would", "wouldnt", "yes", "yet", "you", "youd", "youll",
       "youre", "youve", "your", "yours", "yourself", "yourselves", "zero"])

#Book cover images
book_images = {
    'melville-moby_dick': 'moby_dick.jpg',
    'bryant-stories': 'stories.jpg',
    'shakespeare-caesar': 'caesar.jpg',
    'edgeworth-parents': 'parents.jpg',
    'austen-sense': 'sense.jpg',
    'shakespeare-hamlet' : 'hamlet.jpg',
    'austen-persuasion' : 'persuasion.jpg',
    'austen-emma' : 'emma.jpg',
    'chesterton-brown' : 'brown.jpg',
    'bible-kjv' : 'kjiv.jpg',
    'whitman-leaves' : 'leaves.jpg',
    'chesterton-ball': 'ball.jpg',
    'milton-paradise': 'paradise.jpg',
    'carroll-alice': 'alice.jpg',
    'chesterton-thursday': 'thursday.jpg',
    'shakespeare-macbeth': 'macbeth.jpg',
    'burgess-busterbrown': 'busterbrown.jpg',
    'blake-poems': 'poems.jpg'
}

#Book links from Amazon
amazon_links = {
    'melville-moby_dick': 'https://www.amazon.com/Moby-Dick-Herman-Melville/dp/1503280780',
    'bryant-stories': 'https://www.amazon.com/Kobe-Bryant-Inspiring-Basketballs-Basketball/dp/B0BM4BMCXZ/ref=tmm_hrd_swatch_0?_encoding=UTF8&qid=1683513816&sr=1-1',
    'shakespeare-caesar': 'https://www.amazon.com/Julius-Caesar-Folger-Shakespeare-Library/dp/0743482743/ref=sr_1_1?crid=1HVCGDPWBD202&keywords=shakespeare-caesar&qid=1683513844&s=books&sprefix=%2Cstripbooks%2C248&sr=1-1',
    'edgeworth-parents': 'https://www.amazon.com/Maria-Edgeworth-Parents-Assistant-Confidence/dp/1787806790/ref=sr_1_2?crid=2AG2QRFXQPW8J&keywords=edgeworth-parents&qid=1683513862&s=books&sprefix=edgeworth-parents%2Cstripbooks%2C212&sr=1-2',
    'austen-sense': 'https://www.amazon.com/Sense-Sensibility-Peacock-Jane-Austen/dp/B09ZBNRK9T/ref=sr_1_1?crid=31TXO3HTB07YT&keywords=austen-sense&qid=1683513883&s=books&sprefix=austen-sense%2Cstripbooks%2C214&sr=1-1',
    'shakespeare-hamlet' : 'https://www.amazon.com/Hamlet-Folger-Library-Shakespeare-William/dp/074347712X/ref=sr_1_1?crid=3AEQ8U0VRH040&keywords=shakespeare-hamlet&qid=1683513901&s=books&sprefix=austen-sense%2Cstripbooks%2C190&sr=1-1',
    'austen-persuasion' : 'https://www.amazon.com/Persuasion-Austens-Classic-Anniversary-Collection/dp/B09328MF8D/ref=sr_1_1?crid=256FJBVQJ9MJW&keywords=austen-persuasion&qid=1683513929&s=books&sprefix=austen-persuasion%2Cstripbooks%2C213&sr=1-1',
    'austen-emma' : 'https://www.amazon.com/Emma-Jane-Austen/dp/149366364X',
    'chesterton-brown' : 'https://www.amazon.com/Complete-Father-Brown-Stories/dp/1853260037',
    'bible-kjv' : 'https://www.amazon.com/Full-Size-Leather-Ribbon-Marker-Version/dp/1432132911/ref=sr_1_5?keywords=king+james+bible&qid=1683514002&sr=8-5',
    'whitman-leaves' : 'https://www.amazon.com/Leaves-Grass-Original-Walt-Whitman/dp/1449505716',
    'chesterton-ball': 'https://www.amazon.com/Ball-Cross-G-K-Chesterton/dp/1541117670',
    'milton-paradise': 'https://www.amazon.com/Paradise-Lost-John-Milton/dp/1975712625',
    'carroll-alice': 'https://www.amazon.com/Alices-Adventures-Wonderland-Lewis-Carroll/dp/1503222683',
    'chesterton-thursday': 'https://www.amazon.com/Man-Who-Was-Thursday/dp/1514350017',
    'shakespeare-macbeth': 'https://www.amazon.com/Macbeth-William-Shakespeare/dp/1514630583',
    'burgess-busterbrown': 'https://www.amazon.com/Adventures-Buster-Childrens-Thrift-Classics/dp/0486275647',
    'blake-poems': 'https://www.amazon.com/Blake-Poems-Everymans-Library-Pocket/dp/0679436332'
}

#Dynamo DB column names
column_names = ["book", "word", "value"]

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('tfidf') #'tfidf' -> table name 

app = Flask(__name__, template_folder='template', static_folder = 'images')
#templates > html files
#images > .jpg files

@app.route('/')
def index():
    return render_template('index.html') #Render home page


@app.route('/', methods=['POST'])
def process():
    #Collect User input
    text_input = request.form['text_input']
    
    words = text_input.strip().split()
    regex = re.compile('[^a-zA-Z]')
    output = []
    relevance_score = []
    book_sum = defaultdict(float)
    book_count = defaultdict(int)
    totalFilteredWords = 0

    for word in words:
        word_search = regex.sub('', word.lower())
        if len(word_search) > 0 and word_search not in stopwords_set:

            #Query Dynamo DB Table
            response = table.query( 
                KeyConditionExpression=Key('word').eq(word_search)
            )

            if response['Count'] > 0:
                totalFilteredWords+=1
                items = response['Items']
                books = [item['book'] for item in items]
                values = [item['value'] for item in items]

                book_values = [[book, value] for book, value in zip(books, values)]
                output.extend(book_values)

                for book, value in book_values:
                    if float(value) > 0.0:
                        book_sum[book] += float(value)
                        book_count[book] += 1
            else:
                text = f"The word {word_search} is not found in any books."
                text_output = f"<body style='background: url(./images/no_record.jpg)\
                                no-repeat center center fixed; background-size: 50% auto;'> {text}.</body>"
                render_template_string(text_output)

    #Calculate Relevence scores ass per given formula
    relevance_score = [[book, book_sum[book] / totalFilteredWords] for book in book_sum.keys()]
    relevance_score.sort(key=lambda x: x[1], reverse=True)

    #Display top 5 results # guideline no 6
    top_seven = relevance_score[:5]

    if len(relevance_score) == 0:
        #When no results found
        text_output = "<body style='background: url(./images/no_record.jpg) \
                    no-repeat center center fixed; background-size: 50% auto;'> <h2>No results found.</h2></body>"
    else:
        list_items = ""
        for book, score in top_seven:
            image_file  = book_images[book]
            img_src = "./images/" + image_file
            book_link = amazon_links[book]
            list_items += f"<li style='border: 1px solid black; padding: 8px; border-radius: 10px; margin-bottom: 10px; align: center'>\
                            <img src='{img_src}' width='50' height='70'>\
                            <div style='display: inline-block; margin-left: 20px;align =  center'>\
                                <p><a href={book_link}>{book}</a></p>\
                                <p>{score}</p>\
                            </div>\
                        </li>"

        text_output = f" <img src='./images/results.jpg'> \
                        <hr style='height: 5px; background-color: #177cd4; max-width: 100%;'> \
                        <div style='align: center;'>\
                        <ul style='list-style-type: none; padding: 0; max-width: 30%; '>{list_items}</ul>\
                        </div>"
        
    return render_template_string(text_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5330, debug=True) # http://3.95.175.94:5330 #http://{public_IpV4}:5330

    '''
    cd Lab5
    python3 main.py
    Flask runs on - https://{public_IpV4}:5330
    EC2 Instance ID: i-09ed5001317e09e0c
    '''
    '''
    # AWS Key name : Lab5KeyValuePair
    sudo apt update
    sudo apt install python3-pip
    pip install -r requirements.txt
    code ~/.aws/credentials > paste creds here
    '''

    '''
    Sample Query: my brother is a whale, cool!

    Output:
    melville-moby_dick
    720.9601429483332
    
    bryant-stories
    88.87629390000001
    
    edgeworth-parents
    24.470701442333333

    austen-sense
    21.86658240066667
    
    shakespeare-caesar
    21.41452286666667
    '''
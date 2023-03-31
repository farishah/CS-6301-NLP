#Farishah Nahrin
#CS 6301.M02 - Special Topics in Computer Science
#NLP

#Check if prerequistes are downloaded on your system
import sqlite3
import os
import re
import spacy
import string
import joblib
import random
import wikipedia
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import textwrap

nltk.download("punkt")
nltk.download("stopwords")

#Import ssl to get rid of SSL error
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()
stop_words = set(stopwords.words("english"))
#Debugging mode, to see if the response comes from my knowledge base or wikipedia!
debug = True

#Extract the main noun from the user's query.
#Noun chunks: a meaningful piece of text from the full text
#NLP technique used: Named Entity Recognition
def get_main_noun(query):
    #Load the small English model from spaCy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(query)
    #Extract noun chunks from the query
    noun_chunks = []
    for chunk in doc.noun_chunks:
        #Exclude chunks that contain pronouns, e.g. "I" or "Me"
        if not any(token.pos_ == "PRON" for token in chunk):
            #Get text of each token in the chunk that is not a stopword
            chunk_text = " ".join([token.text for token in chunk if not token.is_stop])
            noun_chunks.append(chunk_text)
    if len(noun_chunks) > 0:
        #Return the first noun chunk
        return noun_chunks[0]
    else:
        #If no noun chunks are found, try to find a standalone noun
        nouns = [
            token.text for token in doc if token.pos_ == "NOUN" and not token.is_stop
        ]
        if len(nouns) > 0:
            #Return the first noun
            return nouns[0]
        else:
            #If no nouns are found, return None
            return None

#NLP technique: NLTK to preprocess
#Preprocess the text by tokenizing it, converting it to lowercase, removing stop words and punctuation
def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in stop_words and token.isalnum()]
    return set(tokens)

#Jaccard similarity is a Text Similarity metric that measures the similarity between two sets,
#in this case, I'm comparing the set of words in the query and the set of words in the knowledge base key.
#Source: https://www.statology.org/jaccard-similarity-python/
#Source #2: https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50

#Source #2 says: "Jaccard similarity takes only unique set of words for each sentence while cosine similarity takes total length of the vectors."
#Jaccard Similarity calculates similarity based on the overlap of the words in the text, rather than their frequency.
#It handles variations in the length and quality of the text better. And is faster than Cosine Similarity because no dot product calculation is required.
def jaccard_similarity(a, b):
    intersection = len(a.intersection(b))
    union = len(a.union(b))
    return intersection / union if union > 0 else 0

#This function searches the knowledge base for the most similar item based on the NOUN from the user's query
def search_knowledge_base(noun, knowledge_base):
    #Check for direct matches using regular expressions
    for key in knowledge_base:
        if re.search(r"\b" + re.escape(noun) + r"\b", key, re.IGNORECASE):
            return knowledge_base[key]
    #Preprocess the knowledge base set keys
    kb_sets = {key: preprocess(key) for key in knowledge_base.keys()}
    #Compute Jaccard similarity between the noun and knowledge base keys to get an actual score!
    similarity_scores = {
        key: jaccard_similarity({noun}, kb_set) for key, kb_set in kb_sets.items()
    }
    #Get the most similar item in the knowledge base based on the score
    most_similar_key = max(similarity_scores, key=similarity_scores.get)
    #My knowledge base has keys that are mostly in 1-2 words, so that's what I'm comparing the similarity with
    #If the similarity score is above a certain threshold, return the result
    if similarity_scores[most_similar_key] > 0.0:
        result = knowledge_base[most_similar_key]
    else:
        result = None
    return result

#Retrieve knowledge base
knowledge_base = joblib.load('bangladeshknowledgebase.pkl')

#Retrieve information from the knowledge base or Wikipedia
def retrieve_information(noun):
    #First try to retrieve information from the knowledge base, then from Wikipedia
    #If a noun is found, search the knowledge base
    if noun is not None:
        result = search_knowledge_base(noun, knowledge_base)
        if result is not None:
            return result

    if debug:
        print("Knowledge base search failed. Trying Wikipedia...")

    #Use wikipedia to retrieve information
    #Source: https://pypi.org/project/wikipedia/
    try:
        result = wikipedia.summary("'" + noun + "'")
        if debug:
            print("Wikipedia primary search successful!")
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        #If the noun is ambiguous, ask the user to select the correct option, then retrieve the summary

        #Get the list of options
        options = e.options
        if debug:
            print("Wikipedia primary search failed. Trying options..., got options:", options)

        #Ask the user to select the correct option
        option_str = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(options)])
        user_input = input(
            f"Sorry, '{noun}' may refer to multiple pages. Please select the number corresponding to the preferred option, among the following:\n{option_str}\nEnter a number from 1 to {len(options)}: "
        )
        if debug:
            print("User input:", user_input)

        #Validate the user's input
        while (
                not user_input.isdigit()
                or int(user_input) < 1
                or int(user_input) > len(options)
        ):
            #If the input is invalid, ask the user to try again.
            user_input = input(
                f"Invalid input. Please enter a number from 1 to {len(options)}: "
            )
        #Retrieve the summary of the selected option
        selected_option = options[int(user_input) - 1]
        #Return the summary
        return wikipedia.summary(selected_option)

#Handles the connection to the database. Using sqlite3 (Python SQL library)
#Source: https://towardsdatascience.com/starting-with-sql-in-python-948e529586f2
def connect_to_db():
    conn = sqlite3.connect("user_data.db")
    return conn

#This function creates the tables in the database
def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT PRIMARY KEY, interest TEXT)''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS queries (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, query TEXT, noun TEXT, response TEXT)''')
    conn.commit()

#This function gets the user's interest from the database
def get_user_interest(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT interest FROM users WHERE name=?", (name,))
    result = cursor.fetchone()
    return result[0] if result else None

#This function adds a new user to the database
def add_user(conn, name, interest):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, interest) VALUES (?, ?)", (name, interest))
    conn.commit()

#This function updates the user's interest in the database
def update_user_interest(conn, name, interest):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET interest=? WHERE name=?", (interest, name))
    conn.commit()

#This function adds a new query to the database
def add_query(conn, name, query, noun, response):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO queries (name, query, noun, response) VALUES (?, ?, ?, ?)",
                   (name, query, noun, response))
    conn.commit()

#This function gets all the queries from a user
def get_user_queries(conn, name):
    cursor = conn.cursor()
    cursor.execute("SELECT id, query FROM queries WHERE name=?", (name,))
    return cursor.fetchall()

#This function gets the response about the user's interest, from the database
def get_query_response(conn, query_id):
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM queries WHERE id=?", (query_id,))
    result = cursor.fetchone()
    return result[0] if result else None

#User flow by greeting user
def greet_user():
    name = input("What is your name? ")
    return name.strip().lower()

#This function gets the user's preference from the database
def get_user_preference(conn, name, knowledge_base):
    interest = get_user_interest(conn, name)
    #Randomly pick up to 5 topics from the knoweldge base
    if interest:
        topics = random.sample(list(knowledge_base.keys()), 5)
        topics = ', '.join(topics)
        print(
            f'Welcome back, {name.title()}! Last time, you said you were interested in "{interest}". What are you interested in this time? Here are some sample topics I can tell you about: {topics} \n')
    else:
        topics = random.sample(list(knowledge_base.keys()), 5)
        topics = ', '.join(topics)
        interest = input(
            f"Hi {name.title()}, I am a chatbot that knows all about Bangladesh! Can you please tell me why you are interested in learning about Bangladesh? Here are some sample topics I can tell you about: {topics} \n")
        add_user(conn, name, interest)
        print(f"\nThank you {name.title()}. I will remember that.")
    return interest

#This function handles the user's query
def handle_query(conn, name, knowledge_base):
    query = input("Please enter your query, make sure to ask about one topic at a time: ").strip()
    if query.lower() == "bye":
        return False
    main_noun = get_main_noun(query)
    response = retrieve_information(main_noun)
    #Sentence tokenizing the response using NLTK by selecting the top 5 sentences, and then textwrap them to 70 characters
    #Then tokenize the response text into sentences
    sentences = nltk.sent_tokenize(response)
    #Select the top 5 sentences for the chatbot response
    top_sentences = sentences[:5]
    #Wrap each sentence into lines of maximum 10 characters
    for sentence in top_sentences:
        wrapped_text = textwrap.wrap(sentence, width=70, break_long_words=False)
        for line in wrapped_text:
            print(line)
    add_query(conn, name, query, main_noun, response)
    update_user_interest(conn, name, main_noun)
    return True

#This user flow shows the user's past queries
def show_past_queries(conn, name):
    queries = get_user_queries(conn, name)
    print(f"Here are your past queries, {name.title()}:")
    for query_id, query_text in queries:
        print(f"{query_id}. {query_text}")

#This user flow handles the user's past queries
def handle_past_query(conn):
    query_id = int(input("Enter the index of the query you want to see the response for: ").strip())
    response = get_query_response(conn, query_id)
    if response:
        print(f"Here is the response for the selected query:")
        #Tokenize the text into sentences
        sentences = nltk.sent_tokenize(response)
        #Select the top 5 sentences
        top_sentences = sentences[:5]
        #Wrap each sentence into lines of maximum 150 characters
        for sentence in top_sentences:
            wrapped_text = textwrap.wrap(sentence, width=150, break_long_words=False)
            for line in wrapped_text:
                print(line)
    else:
        print("Sorry, I couldn't find a response for that query index.")

#Initialize the knowledge base and database
knowledge_base = joblib.load('bangladeshknowledgebase.pkl')

conn = connect_to_db()
create_tables(conn)

#Main menu of chatbot allows user to choose from these three options:
name = greet_user()
interest = get_user_preference(conn, name, knowledge_base)
while True:
    choice = input("\nChoose an option:\n1. Ask a query\n2. See past queries\n3. Exit\n> ")
    choice = choice.strip('. ')
    if choice == "1":
        should_continue = handle_query(conn, name, knowledge_base)
        if not should_continue:
            print(f"Goodbye, {name.title()}!")
            break
    elif choice == "2":
        show_past_queries(conn, name)
        handle_past_query(conn)
    elif choice == "3":
        print(f"Goodbye, {name.title()}!")
        break
    else:
        print("Invalid option. Please try again.")

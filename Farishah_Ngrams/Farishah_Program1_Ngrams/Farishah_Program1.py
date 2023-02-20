#Farishah Nahrin
#CS 6301.M02 - Special Topics in Computer Science
#NLP

#Program 1 - Ngrams

#Source: Code inspired by https://github.com/kjmazidi/NLP/tree/master/Part_2-Words/Chapter_08_ngrams and #Source: Code inspired by https://github.com/kjmazidi/NLP/tree/master/Part_2-Words/Chapter_08_ngrams and https://github.com/kjmazidi/NLP/blob/master/Part_2-Words/Chapter_08_ngrams/8_ngrams_1.ipynb

#Check if prerequistes are downloaded on your system
from nltk.util import ngrams
from nltk import word_tokenize
from collections import Counter
import pickle

#Creating function to read data from the file and returns unigrams and bigrams of data
def get_data_from_file(file_path: str = None):
    #Open the file and read data!
    with open(file=file_path, mode='r') as file:
        data = file.read()
    #Replace \n newlines with spaces
    data = data.replace('\n', ' ')
    #Tokenize the text
    data = word_tokenize(data)
    #Retrieve unigrams and bigrams into respective lists
    unigram_data = list(ngrams(data, n=1))
    bigram_data = list(ngrams(data, n=2))
    #Using the counter class to count the bigrams and unigrams, which will process faster, and I'll also convert it to dictionary again
    #This will use the bigram and unigram ist to create respective dictionaries
    unigram_dict = dict(Counter(unigram_data))
    bigram_dict = dict(Counter(bigram_data))
    #Return the dictionaries
    return unigram_dict, bigram_dict

#Now I'll pickle the dict with the given file name
def pickle_dict(lang_dict: dict = None, file_path: str = None):
    with open(file_path, 'wb') as file:
        pickle.dump(lang_dict, file)

#Create file paths
if __name__ == "__main__":
    english_path = 'data/LangId.train.English'
    french_path = 'data/LangId.train.French'
    italian_path = 'data/LangId.train.Italian'
#Retrieve the unigrams and bigrams
    english_unigram, english_bigram = get_data_from_file(english_path)
    french_unigram, french_bigram = get_data_from_file(french_path)
    italian_unigram, italian_bigram = get_data_from_file(italian_path)
#Pickle the unigrams and bigrams (6 total)
    pickle_dict(english_unigram, 'unigram_english.pickle')
    pickle_dict(english_bigram, 'bigram_english.pickle')
    pickle_dict(french_unigram, 'unigram_french.pickle')
    pickle_dict(french_bigram, 'bigram_french.pickle')
    pickle_dict(italian_unigram, 'unigram_italian.pickle')
    pickle_dict(italian_bigram, 'bigram_italian.pickle')
#Farishah Nahrin
#CS 6301.M02 - Special Topics in Computer Science
#NLP

#Program 2 - Ngrams

#Source: Code inspired by https://github.com/kjmazidi/NLP/tree/master/Part_2-Words/Chapter_08_ngrams and https://github.com/kjmazidi/NLP/blob/master/Part_2-Words/Chapter_08_ngrams/8_ngrams_1.ipynb

#Check if prerequistes are downloaded on your system
from nltk.util import ngrams
from nltk import word_tokenize
import pickle

#Creating a function that unpickles a dictionary from a given file
def unpickle_dict(file_path: str = None):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

#Read the unigrams and bigrams from the files
unigram_english = unpickle_dict('unigram_english.pickle')
bigram_english = unpickle_dict('bigram_english.pickle')
unigram_french = unpickle_dict('unigram_french.pickle')
bigram_french = unpickle_dict('bigram_french.pickle')
unigram_italian = unpickle_dict('unigram_italian.pickle')
bigram_italian = unpickle_dict('bigram_italian.pickle')

#Measure V to use for later computations. V = the total vocabulary size, based on the formula given in the hints (add the lengths of the 3 unigram dictionaries)
v = len(unigram_english) + len(unigram_french) + len(unigram_italian)

#Creating a function that calculates probability with unigrams and bigrams
def probabilistic_language(text, unigrams, bigrams):
    #Create unigrams and bigrams
    test_unigrams = word_tokenize(text)
    test_bigrams = list(ngrams(test_unigrams, n=2))
    #Initiate laplace probability as 1 because it will be multiplied, since it can't be 0
    p_laplace = 1
    #Iterate this for all bigrams in test text
    for bigram in test_bigrams:
        #Get the bigram count or 0
        b = bigrams[bigram] if bigram in bigrams else 0
        #Get the unigram count or 0
        u = unigrams[bigram[0]] if bigram[0] in unigrams else 0
        #Apply the given formula from the ngrams program2 hint, from the instructions!
        p_laplace = p_laplace * ((b + 1) / (u + v))
    #Return the result (aka the probability)
    return p_laplace

#Creating a function that calculates probabilty for each language, by passing their unigram and bigram into the the defined functions
def detect_language(text):
    #Detect the probabilty for English
    english_prob = probabilistic_language(
        text=text,
        unigrams=unigram_english,
        bigrams=bigram_english)
    #Detect the probabilty for French
    french_prob = probabilistic_language(
        text=text,
        unigrams=unigram_french,
        bigrams=bigram_french)
    #Detect the probabilty for Italian
    italian_prob = probabilistic_language(
        text=text,
        unigrams=unigram_italian,
        bigrams=bigram_italian)
    #Extract the langnuage for the maximum probabiltiy only
    max_prob = max([(english_prob, "English"), (french_prob, 'French'), (italian_prob, 'Italian')])
    #Only return the name of the language
    return max_prob[1]

if __name__ == "__main__":
    #Read the test data
    with open('data/LangId.test') as file:
        test_data = file.read().split('\n')
    #Initiate test results as empty list
    test_result = []
    #Iterate on each line
    for i, line in enumerate(test_data):
        #If the lines are empty continue
        if line == '':
            continue
        #Detecting the language and appending the language_name results
        language = detect_language(line)
        test_result.append(language)
        #Write these results to a file
        with open('data/LangId.detected', 'a') as file:
            text = f"{i + 1} {language}\n"
            file.write(text)
    #Read the actual results
    with open('data/LangId.sol') as file:
        true_results = file.read().split('\n')
    #Get the number of total predictions because Accuracy = predicted/total
    total_predictions = len(test_result)
    #Initiate correct predictions as zero, and line numbers as empty list
    correct_predictions = 0
    incorrect_lines = []
    #Iterate for true results
    for i, language in enumerate(true_results):
        #If the result is empty continue
        if language == "":
            continue
        #If result is correct, increment the correct prediction number
        if language.split()[1] == test_result[i]:
            correct_predictions += 1
        #Otherwise, add line to incorrect line
        else:
            incorrect_lines.append(i + 1)
    #Output accuracy and incorrect lines
    print(f'Accuracy of correctly classified instances : {(correct_predictions / total_predictions) * 100:.2f}%')
    print('The incorrectly Identified Line Numbers are:', *incorrect_lines)

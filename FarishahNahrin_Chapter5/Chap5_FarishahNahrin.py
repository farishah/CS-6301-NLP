#Farishah Nahrin
#CS 6301.M02 - Special Topics in Computer Science
#NLP

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download
from nltk import pos_tag
import random
import sys

#Check if prerequistes are downloaded on your system
try:
    word_tokenize('Computer Science')
    lemmatizer = WordNetLemmatizer()
    lemmatizer.lemmatize("Science")
    pos_tag(['Science'])
    SW = stopwords.words('english')
except LookupError:
    download('punkt')
    download('wordnet')
    download('averaged_perceptron_tagger')
    lemmatizer = WordNetLemmatizer()
    lemmatizer.lemmatize("Science")
    SW = stopwords.words('english')

#Citing my main source: Used this https://github.com/kjmazidi/NLP/tree/master/Part_2-Words/Chapter_05_words
#and https://github.com/kjmazidi/NLP/tree/master/Part_2-Words/Chapter_06_pos_tagging

#Takes a file path, reads it, and prints the lexical diversity (which is the proportion of unique tokens)
#Lexical diversity = unique tokens divided by total tokens
def lexical_diversity(file_path):
    with open(file_path, 'r') as file:
        tokenized_words = word_tokenize(file.read())
    lexical_diversity = len(set(tokenized_words)) / len(tokenized_words)
    print(f"Lexical Diversity: {lexical_diversity:.2f} \n")

def preprocess(file_path):
    #Read the file and tokenize the words
    with open(file_path, 'r') as file:
        tokenized_words = word_tokenize(file.read())
    #Tokenize the lower-case raw text, reduce the tokens to only those that are alpha, not in the NLTK stopword list, and have length > 5
    tokenized_words = [word.lower() for word in tokenized_words if (word.lower() not in SW and len(word) > 5)]
    #Only allow alpha words
    tokenized_words = [word for word in tokenized_words if word.isalpha()]
    #Lemmatize the words
    lemmatized_tokens = set([lemmatizer.lemmatize(word) for word in tokenized_words])
    #Includes parts of speech tagging
    tagged_words = pos_tag(lemmatized_tokens)
    #Print the first 20 tagged
    print(tagged_words[:20], '\n')
    #Only get nouns
    nouns = [k for k, v in tagged_words if v == 'NN']
    #print the number of tokens and the number of nouns.
    print('Number of lemmatized tokens:', len(lemmatized_tokens))
    print('\nNumber of Nouns:', len(nouns))
    print()
    return nouns, tokenized_words

#Print the 50 most common words!
def get_top_50_nouns(nouns, tokens):
    #Create a Noun dictionary
    noun_dict = dict()
    #Iterate over all the tokens
    for word in tokens:
        #Check if a word is in the Nouns dictionary
        if word in nouns:
            if word in noun_dict:
                #if word is already present in noun_dict increment it's count
                noun_dict[word] += 1
            else:
                #Else, add the word to the noun_dict and give it count=1
                noun_dict[word] = 1
    #Sort all the nouns according to their counts
    noun_dict = sorted(noun_dict.items(), key=lambda x: x[1], reverse=True)[:50]
    print(noun_dict)
    #Only get top 50 nouns
    top_50_nouns = [noun[0] for noun in noun_dict]
    return top_50_nouns

def wordguessgame_anatomy(words):
    #Randomly chose a word from all the words pass to this
    word = random.choice(words)
    print("Let's play a word guessing game!")
    #Initiate the starting parameter
    points = 5
    guess = ''
    right_guess = []
    guessed = ' '.join(['_' for _ in word])
    print(guessed)

    #Continue 'till quess is ! or points are less than 0
    while points >= 0 and guess != '!':
        #Take the guess from the user
        guess = str(input('Guess a letter:'))
        #If the letter guessed is in the chosen word
        if guess in word:
            #Add guessed letter to right_guess list
            right_guess.append(guess)
            #Increment score
            points += 1
            print('Right! Score is', points)
            #Create string  like the one shown in the instructions:  v _ s s _ _
            guessed = ' '.join([l if l in right_guess else '_' for l in word])
        else:
            #If guess is not '!' and guess is wrong
            if guess != '!':
                #Subtract the score by 1 :(
                points -= 1
                print('Sorry, guess again. Score is', points)
        print(guessed)
        #If the guessed word is complete
        if "".join(guessed.split()) == word:
            #Choose another word
            word = random.choice(words)
            #Empty the right guess list
            right_guess = []
            #create string like _ _ _ _ _ _
            guessed = ' '.join(['_' for _ in word])
            print('You solved it!\n')
            print('Current score:', points)
            print('\nGuess another word')
            print(guessed)

if __name__ == "__main__":
    try:
        #Take the system arguments for file_path
        #I just added my actual file path, but as long as you my FarishahNahrin_Chapter5 saved in your file, the anat19.txt can be called from the directory.
        file_path = "/Users/farishahnahrin/Desktop/Farishah_Chap5Portfolio/FarishahNahrin_Chapter5/anat19.txt"
        #Print the lexical diversity
        lexical_diversity(file_path=file_path)
        #Preprocess the data
        nouns, tokens = preprocess(file_path=file_path)
        #Get top 50 nouns
        top_50_nouns = get_top_50_nouns(nouns=nouns, tokens=tokens)
        print()  #just to add an extra line
        #Start guessing game
        wordguessgame_anatomy(top_50_nouns)
    except IndexError:
        print('You need to pass the file path of "anat19.txt" ')


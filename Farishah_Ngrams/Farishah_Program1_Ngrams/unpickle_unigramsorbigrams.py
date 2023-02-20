#Farishah Nahrin
#CS 6301.M02 - Special Topics in Computer Science
#NLP

#This file was created, so that you can easily un-pickle the pickle file that was auto generated from my code
import pickle
import joblib
#As an example below, I've only un-pickled the bigram_english.pickle file, so feel free
#..to replace the file path and un-pickle the rest of the files
keyword_dict = joblib.load("/Users/farishahnahrin/Desktop/Farishah_Program1_Ngrams/bigram_english.pickle")
for key, value in keyword_dict.items():
    print(f"For the keyword '{key}' the sentences are: ", value, "\n" * 5)
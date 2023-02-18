#Farishah Nahrin
#CS 6301.M02 - Special Topics in Computer Science
#NLP

#This file was created, so that you can easily un-pickle the pickle file that was auto generated from my code
import pickle
import joblib
keyword_dict = joblib.load("/Users/farishahnahrin/Desktop/FarishahNahrin_WebCrawler/bangladeshknowledgebase.pkl")
for key, value in keyword_dict.items():
    print(f"For the keyword '{key}' the sentences are: ", value, "\n" * 5)

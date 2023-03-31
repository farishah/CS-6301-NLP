#Farishah Nahrin
#CS 6301.M02 - Special Topics in Computer Science
#NLP

#Check if prerequistes are downloaded on your system
import pyrootutils
import sys
root = pyrootutils.setup_root(
    search_from=sys.path[0],
    pythonpath=True,
)
import os
import re
import sys
import time
import pickle
import random
import string
import calendar
import requests
import traceback
import numpy as np
import pandas as pd
import urllib.request
import urllib3.request, urllib.parse, urllib.error
from scrapy.http import TextResponse, FormRequest, Request
from collections import deque
from datetime import timedelta, date
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize import RegexpTokenizer
import joblib
import time
from threading import Thread

import concurrent.futures

#The reason why I am using scrapy instead of BeautifulSoup, is because i have a bit more experience with Scrapy
#And the instructions said "be able to do web scraping with Beautiful Soup or other APIs" So this is the other API i have chosen to scrape with

#Created headers to use in the request!
#I have to use these headers from the browser, so that the website does not block the requests
#This also forces the website to believe that my requests are coming from the browser and not a script
#(or else the request won't work)
#Source: the virtualbangladesh headers in the Network tab of the of Inspect Element also https://www.updatable.com/docs/modifications/response-headers.html
#Source number 2: https://webtechsurvey.com/response-header/nel
conv = """access-control-allow-origin: *
age: 1755
cache-control: max-age=86400
cf-cache-status: HIT
cf-ray: 5ddcb84dab30e660-LHR
cf-request-id: 059dd184840000e66076bcb200000001
content-encoding: br
content-type: text/html
date: Tue, 12 Feb 2023 04:43:10 CST
status: 200
vary: Accept-Encoding
x-page-speed: 1.11.33.4-0"""
conv = conv.split("\n")
headers = dict()
#I'm removing the accept-encoding header - it's not needed, and it causes issues with the requests (not sure why)
#The ther headers above are needed for the requests to work though
for i in range(len(conv)):
    headers[conv[i].split(": ")[0]] = conv[i].split(": ")[1]
try:
    del headers["accept-encoding"]
except:
    pass


#Get all the URLs from starting URL
#Scraping all the links present in the website
#TextResponse object is from scrapy
req = requests.get("https://www.virtualbangladesh.com/", headers=headers)
response = TextResponse(req.url, body=req.text, encoding="utf-8")

#Retrieve URLs from the page
links_on_page = [i for i in response.xpath("//a/@href").extract()[1:]]

#Use the reg ex expression below to filter text
#re.match(r'[^\s].*[^\s]', i) matches any string that has at least one non-whitespace character at the beginning and at the end of the string.
def get_text(text):
    result = []
    for i in text:
        into = re.match(
            r"[^\s].*[^\s]", i
        )
        if into is not None:
            result.append(into.group())
    return ", ".join(result)

def process_link(link, dict):
    req = requests.get(link, headers=headers, timeout=None)
    #scraping text from the links
    #virtualbangldesh has bangla characters, and utf-8 allows me to read them as non-english characters
    response = TextResponse(req.url, body=req.text, encoding="utf-8")
    #Went through the code on the website and noticed it stores text under the classses with below mentioned name, like fusion-column-wrapper, post-content etc.
    text = response.xpath('//div[@class="post-content"]//text()').extract()
    fil_text = get_text(text)
    dict[link] = fil_text
#Scrape the text from the links in links_on_page.
#Store these in a dictionary with the key as the link and value as the scraped text
main_dict = dict()

#Use the concurrent futures to run the process_link function in parallel, via a pool of threads
#Because if they run after one another, it'll take a long time!
#Source: https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(process_link, links_on_page, [main_dict] * len(links_on_page))
#mapping method into a list containing the same main_dict object repeated len(links_on_page) times
#I am doing this to update the main_dict object with the processed data from each link in links_on_page
#with the updates applied in parallel using multiple threads.
#making sure each link on page can read/see the dictionary

#This func separates the last part of the url and replaces the '-' with ' ' and removes the 'www.' and '.com' from the url. e.g. https://www.virtualbangladesh.com/news/basic-info/ will be converted to 'basic info'
func = (
    lambda x: x.strip("/ ")
    .split("/")[-1]
    .replace("-", " ")
    .replace("www.", "")
    .replace(".com", "")
)

#Creating a list of all the keys
new_keys = list(main_dict.keys())

#Delete empty values
for key in new_keys:
    if main_dict[key] == "":
        print(key)
        del main_dict[key]
new_keys = list(main_dict.keys())
count = 0

#Delete keys with less than 50 words (as they're mostly useless information and just link farm pages)
for key in new_keys:
    if len(main_dict[key].split(" ")) < 50:
        count += 1
        del main_dict[key]
        new_keys.remove(key)
print("Total number of keys with less than 50 words: ", count)

#Create a new dictionary with the modified keys
mod_dict = {func(k): v for k, v in main_dict.items()}

#Dump the knowledge base into a pickle file!
joblib.dump(mod_dict, "bangladeshknowledgebase.pkl")

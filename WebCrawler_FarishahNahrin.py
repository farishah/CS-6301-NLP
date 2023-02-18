#Farishah Nahrin
#CS 6301.M02 - Special Topics in Computer Science
#NLP

#Check if prerequistes are downloaded on your system

#The reason why I am using scrapy instead of BeautifulSoup, is because i have a bit more experience with Scrapy
#And the instructions said "be able to do web scraping with Beautiful Soup or other APIs" So this is the other API i have chosen to scrape with
from scrapy.http import TextResponse, FormRequest, Request
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize import RegexpTokenizer
import joblib
import concurrent.futures

import re
import sys
import requests
import numpy as np
import pandas as pd

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
expect-ct: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
nel: {"report_to":"cf-nel","max_age":604800}
report-to: {"endpoints":[{"url":"https:\/\/a.nel.cloudflare.com\/report?lkg-colo=21&lkg-time=1601959390"}],"group":"cf-nel","max_age":604800}
server: cloudflare
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

#Get all the URLs from starting URL, plus some sites outside of the original domain
print("Getting all the URLs from the homepage...")
req = requests.get(
    "https://www.virtualbangladesh.com/news/english-news/", headers=headers
)
response = TextResponse(req.url, body=req.text, encoding="utf-8")

#Retrieve URLs from the page
links_on_page = [i for i in response.xpath("//a/@href").extract()[1:]]
bangla_links = [i for i in links_on_page if i.startswith("https://www.virtualbangladesh")]
extra_links = [i for i in links_on_page if not (i.startswith("https://www.virtualbangladesh") or i.startswith("http://virtualbangladesh"))]
req_links = ['financialexpress', 'thedailystar', 'unbnews', 'bangladesh']
spec_links = [i for i in extra_links if any(j in i for j in req_links)]

#Instructions said "outputs a list of at least 15 relevant URLs" since it said **at least,** i'm outputting 40
#(so 35 URLs come from the relevant pages, 5 come from outside of the original domain)

sub_bangla_links = np.random.choice(bangla_links, 40, replace=False)

#The regex expression "\s*[^\S\n]+" consists of two parts:
#The \s* does this: matches zero or more whitespace characters (like spaces, tabs, and newline characters).
#The * means "zero or more".
#The [^\S\n]+ means this: matches one or more characters that are not a whitespace character (that is, no spaces, tabs, or newline characters) and not a newline character
#The [^...] means this: it matches any character, not listed inside the square brackets.
#The \S character does this = matches any non-whitespace character
#The \n character does this: matches a newline character
#The + does this: it means "one or more".
#Source: https://regex101.com/
#Source number 2: https://www.freeformatter.com/regex-tester.html

#Use the reg ex expression below to filter text
def process_link(link, dict):
    req = requests.get(link, headers=headers, timeout=None)
    response = TextResponse(req.url, body=req.text, encoding="utf-8")
    text = response.xpath(
        '//div[@class="fusion-column-wrapper" or @class="post-content" or @class="pane-content" or @class="container"]//p/text()'
    ).extract()
    filter_text = ", ".join(
        [
            i
            for i in [re.sub("[^\S\n]+\|*", " ", item).strip() for item in text]
            if i != ""
        ]
    )
    dict[link] = filter_text
#Scrape the text from ALL the links in links_on_page.
#Store these in a dictionary with the key as the link and value as the scraped text
main_dict = dict()

#Use the concurrent features to run the process_link function in parallel
#Because if they run after one another, it'll take a long time!
#Source: https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_link, links_on_page, [main_dict] * len(links_on_page))

#Check if the outputRelevant folder exists, if not then make it
import os
if not os.path.exists("outputRelevant"):
    os.makedirs("outputRelevant")

#Display the links in the output and have the url be the name of the file with .txt as the extension
sub_bangla_links = list(sub_bangla_links)
spec_links = list(spec_links)
sub_bangla_links.extend(spec_links)
for i in sub_bangla_links:
    try:
        print("Processing link: ", i)
        file_name = (
            "outputRelevant/"
            + i.strip("/").lstrip("https://").replace("/", "\\")
            + ".txt"
        )
        with open(file_name, "w+") as f:
            f.write(main_dict[i])
    except:
        pass

#Combine all the text in main_dict into a single string
text = " ".join([main_dict[i] for i in main_dict])
#Output in lowercase only!
text = text.lower()

#Defining the tokenizer variable as a regex tokenizer, using '\w+', which means that:
#it matches one or more word characters, and then it uses the tokenizer to tokenize and split the string text...
#...into individual words. Then it stores the resulting list of tokens, the 'tokens' variable

#Tokenize
tokenizer = RegexpTokenizer(r"\w+")
tokens = tokenizer.tokenize(text)
#Remove stopwords
stop_words = set(stopwords.words("english"))
tokens = [token for token in tokens if token not in stop_words]
#Only return alpha tokens only
tokens = [token for token in tokens if token.isalpha()]

from collections import Counter
from math import log

#Now get the top 10 scraped keywords
def get_top_keywords(st, top_n=10):
    #Tokenize the string
    #st equals string
    terms = st
    #Find the term frequency of each term
    tf = Counter(terms)
    #Find the inverse document frequency of each term
    #This assumes that the total number of documents is the length of the string
    N = len(st)
    idf = {term: log(N / (tf[term] + 1)) for term in tf}
    #Find the TF-IDF weight of each term
    tfidf = {term: tf[term] * idf[term] for term in tf}
    #Sort the terms by their TF-IDF weight in descending order
    sorted_tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
    #Select the top n terms with the highest TF-IDF weight
    top_keywords = [term for term, weight in sorted_tfidf[:top_n]]
    return top_keywords

top_keywords = get_top_keywords(tokens, 40)
print("The top 40 keywords are: ", top_keywords)

""""
The top 40 words are:
['bangladesh', 'pakistan', 'র', 'east', 'league', 'bengal', 'government', 'west', 'awami', 'pakistani', 'national', 'people', 'political', 'new', 'state', 'one', 'ন', 'military', 'ব', 'ত', 'ক', 'bangla', 'also', 'dhaka', 'india', 'দ', 'first', 'would', 'ম', 'bengali', 'bangalis', 'two', 'bangali', 'স', 'ল', 'য', 'march', 'country', 'muslim', 'war']

My top 10 manually selected words are: 
['bangladesh', 'pakistan', 'east', 'awami', 'muslim', 'government', 'india', 'military', 'state', 'political']
"""

#These are the top 10 keywords i chose, from the top 40
top_keywords = [
    "bangladesh",
    "pakistan",
    "east",
    "awami",
    "muslim",
    "government",
    "india",
    "military",
    "state",
    "political",
]
print("The top 10 manually selected keywords are: ", top_keywords)
#Find where the top keywords are in the text, and print the sentences
print('\n' * 5)
count = 0

#Combine the 5 sentences together, for each keyword, into a string
#Store it in a dictionary with key as the keyword and value as the string
keyword_dict = dict()
for keyword in top_keywords:
    keyword_dict[keyword] = ""
    for sent in sent_tokenize(text):
        if keyword in sent:
            keyword_dict[keyword] += sent
            count += 1
        if count == 5:
            break
    print(f"For the keyword '{keyword}' the sentences are: ", keyword_dict[keyword], "\n" * 5)
    count = 0

#Dump the knowledge base into a pickle file!
joblib.dump(keyword_dict, "bangladeshknowledgebase.pkl")

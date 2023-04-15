# NLP
[Overview of NLP by Farishah](https://farishah.github.io/CS6301-NLP/Overview%20of%20NLP.pdf)

## Word Guessing Game
[Word Guess Game](https://github.com/farishah/CS6301-NLP/tree/main/FarishahNahrin_Chapter5)

## Web Crawler
[N-Grams Narrative](https://farishah.github.io/CS6301-NLP/FarishahNahrin_WebCrawler/Report_FarishahNahrin.pdf)

[Building a Corpus - Web Crawler](https://github.com/farishah/CS6301-NLP/tree/main/FarishahNahrin_WebCrawler)

Summary: The entire text data was aggregated from the relevant links. The code uses the requests library to fetch the HTML content of the virtualbangladesh site. Once the HTML content is fetched, it can be passed to the Scrapy library for parsing. The code then iterates through all the URLs on the site, and then it uses Requests and Scrapy again, to extract the relevant information. After aggregating all the scraped data, the code does the tokenization, which involves splitting the text into individual words or tokens. And this helps prepare the data for further processing, like filtering non-alphanumeric characters and removing stop words. Then the entire data is cleaned up and the sentence gets tokenized. The reason why I am using Scrapy instead of BeautifulSoup, is because I have a bit more experience with Scrapy. And the instructions said, "be able to do web  scraping with Beautiful Soup or other APIs" So this is the other API i have chosen to scrape with. It can also handle requests asynchronously. After extracting the text with Scrapy, the code could pass the text to sent_tokenize to split it into individual sentences. This allows for the processing on a sentence-level, which was used for the knowledge base. Then the top five sentences, for each keyword, contained this said keyword, and then it was combined with ‘,’ as a delimiter. To get the top 40 words, I tokenizd each string, found the term frequency of each term, found the inverse document frequency of each term, and then the TF-IDF weight of each term. Then I sorted the terms by their TF-IDF weight in descending order. Then, I selected the top 40 terms with the highest TF-IDF weight. The Top 10 Terms I picked was: ['bangladesh', 'pakistan', 'east', 'awami', 'muslim', 'government', 'india', 'military', 'state', 'political'].

## WordNet
[Deep Dive into WordNet](https://github.com/farishah/CS6301-NLP/blob/main/Farishah_Wordnet.ipynb)

Summary: WordNet is a "lexical database of nouns, verbs, adjectives and adverbs that provides short definitions called glosses, and use examples." WordNet started as a project at Princeton University, organized by George Miller. The primary premise of the project was "to support theories of human semantic memory, which suggested that people organize concepts mentally in some kind of hierarchy." In NLTK, WordNet is just another NLTK corpus reader, that is created for natural language processing and can be used for translating language automatically, text similarity, to disambiguate words, as a thesaurus. 

## N-Grams
[N-Grams Project](https://github.com/farishah/CS6301-NLP/tree/main/Farishah_Ngrams)

[N-Grams Narrative](https://farishah.github.io/CS6301-NLP/Farishah_Ngrams/Farishah_Narrative_Ngrams.pdf)

Project 1 Summary: Created function to read data from the file and returns unigrams and bigrams of data. Then, I replaced the newlines with spaces and tokenized the text. Then I retrieved the unigrams and bigrams into respective lists. I used the counter class to count the bigrams and unigrams, which will process faster, and I'll also convert it to dictionary again. Then I pickled these dictionaries. 

Project 2 Summary: Created a function that unpickles a dictionary from a given file. Then, I read the unigrams and bigrams from the files. Then I had a formula, to calculate "V." to use for later computations. V = the total vocabulary size, based on the formula given in the hints (which means to: add the lengths of the 3 unigram dictionaries). Then, I created a function that calculates probability with unigrams and bigrams - i first created the unigrams and bigrams, initialzed the laplace probability to 1, since it can't equal 0, and it will be a value that's multiplied. Then, I iterated this and applied it to all the text. Then I applied this formula: p_laplace = p_laplace * ((b + 1) / (u + v)). Then I created a function that calculates the probabilty for each language, by passing their unigram and bigram into the the defined functions. Then, I created another function that calculated the probability for each language, by referencing my previous function. Then, I extracted the langnuage for the maximum probabiltiy only. Next, I read the LangId.test file, then detected the results and wrote it to a file. Then I read the LangId.sol (correct classifications files), then I got the accuracy. 

## Sentence Parsing

[Sentence Parsing - Comparing the Three Types of Sentence Parsers](https://farishah.github.io/CS6301-NLP/Farishah_Nahrin_Sentence_Parsing.pdf)


## Chatbot Project

[Chatbot Report](https://farishah.github.io/CS6301-NLP/ChatbotReport_FarishahNahrin.pdf)

[Chatbot Project](https://github.com/farishah/CS6301-NLP/tree/main/FarishahNahrin_ChatBot)

## ACL Paper Summary
[ACL Paper Summary](https://farishah.github.io/CS6301-NLP/Farishah_Nahrin_ACL_Summary.pdf)

## Text Classification
[Text Classification 1](https://github.com/farishah/CS6301-NLP/tree/main/Farishah_Text_Classification_1)



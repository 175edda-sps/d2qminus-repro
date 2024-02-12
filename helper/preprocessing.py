import os, sys
sys.path.insert(0, os.getcwd())
import pyterrier as pt
import pandas as pd
import numpy
import pandas as pd
from helper import util
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer # Snowball Stemmer is also known as the Porter2
import re
import json
import logging
import argparse
# nltk.download('stopwords')
# nltk.download('punkt')
if not pt.started():
    pt.init(version='5.7', helper_version='0.0.7')
from pyterrier import autoclass


porter = PorterStemmer()
porter2 = SnowballStemmer(language='english')  # porter2 is the default in Pisa Indexer
terrier_stopwords = autoclass("org.terrier.terms.Stopwords")(None) # terrier_stopwords is the default in Pisa Indexer 



def en_stem(text, stemmer=porter2):
    # # Tokenize the input string into words
    # words = nltk.word_tokenize(text)
    # # Apply stemming to each word
    # stemmed_words = [porter.stem(word) for word in words]
    # # Join the stemmed words back into a string
    # stemmed_string = " ".join(stemmed_words)

    token_words= word_tokenize(text)
    return " ".join([stemmer.stem(word) for word in token_words])


def lower_case(text):
    # apply preprocessing steps on the given sentence
    text = text.lower()
    return text

def clean(text):
    text = re.sub(r"http\S+", " ", text)  # remove urls
    text = re.sub(r"RT ", " ", text)  # remove rt
    text = re.sub(r"@[\w]*", " ", text)  # remove handles
    text = re.sub(r"[\.\,\#_\|\:\?\?\/\=]", " ", text) # remove special characters
    text = re.sub(r"\t", " ", text)  # remove tabs
    text = re.sub(r"\n", " ", text)  # remove line jump
    text = re.sub(r"\s+", " ", text)  # remove extra white space
    text = text.strip()
    return text



def remove_punctuation(text):
    # Removing punctuations in string using regex
    text = re.sub(r'[^\w\s]', '', text)
    return text


def remove_stop_words(text, apply_nltk=False):
    '''
    text: input text to remove stopwords from
    apply_nltk: False: means apply terrier_stopwords
                        True: means apply nltk stopwords
    '''
    if apply_nltk:
        stop_words = stopwords.words()
        text = " ".join(word for word in text.split() if word not in stop_words)
    else: # apply terrier stopwords
        text = " ".join(word for word in text.split() if not terrier_stopwords.isStopword(word))
    return text


def preprocess(text, stop_words='terrier'):
    text  = clean(text)
    text  = remove_punctuation(text)
    text = lower_case(text)
    if stop_words == 'terrier':
        text = remove_stop_words(text, apply_nltk=False)
    elif stop_words == 'nltk':
        text = remove_stop_words(text, apply_nltk=True)
    text = en_stem(text)
    return text


def preprocess_list(text_list):
    return [preprocess(text) for text in text_list]


        
def join_queries(queries):
    return " mx12e34m ".join(queries)



def process(input_file, save_file, logger):

    df = pd.read_json(input_file, lines=True,)
    logger.info(f"Loaded the document with expansion queries file from this path {input_file}")


    df['queries_joined'] = df["predicted_queries"].apply(join_queries)
    logger.info("Done with joining each document queries into one string")

    df['queries_processed'] = df['queries_joined'].apply(preprocess)
    logger.info("Done with processing the query terms ")
    # df.drop(['queries_joined', 'predicted_queries'], axis=1, inplace=True)
    df.drop(['queries_joined',], axis=1, inplace=True)

    util.save_dataframe(df, save_file,)
    # df.to_json(save_file, orient='records', lines=True)
    logger.info("Done Saving the file")




def main():

    parser = argparse.ArgumentParser(description="Preprocessing expansion queries")
    parser.add_argument("--input", type=str, required=True, help="Path to the input data file")
    parser.add_argument("--log", type=str, required=True, help="Path to the log file")
    parser.add_argument("--output", type=str, required=True, help="Path to the save the output file")
    args = parser.parse_args()
    log_file = args.log
    input = args.input
    output = args.output
    
    logger = util.get_logger(log_file)
    logger.info(f"The log file is saved into : {log_file}")
    logger.info(f"The output file is saved into : {output}")
    logger.info(f"The input file is saved into : {input}")

    process(input, output, logger,)


if __name__ == "__main__":
    main()
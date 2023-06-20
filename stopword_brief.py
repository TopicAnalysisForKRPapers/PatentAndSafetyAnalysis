### aria1th@github

import os
import pandas as pd
from tqdm import tqdm
from collections import Counter # for counting words

encoding = 'utf-8'
def read_stopwords(stop_word_file):
    with open(stop_word_file, 'r', encoding=encoding) as f:
        stop_words = f.read().splitlines()
    return set(stop_words)

# use Komoran to tokenize
from konlpy.tag import Komoran
komoran = Komoran()

def tokenize(text):
    # check if text is string
    if not isinstance(text, str) or text == "":
        return ""
    return " ".join(komoran.morphs(text))

# select nouns only
def tokenize_nouns(text):
    # check if text is string
    if not isinstance(text, str) or text == "":
        return ""
    return " ".join(komoran.nouns(text))

# pos tagger
def pos_tagger(text):
    # check if text is string
    if not isinstance(text, str) or text == "":
        return ""
    return komoran.pos(text)

# select by set
def select_by_set(text, iterable):
    tagged = pos_tagger(text)
    # print types of pos tag
    #print(set([tag for word, tag in tagged]))
    if tagged == "":
        return ""
    return " ".join([word for word, tag in tagged if tag in iterable])

def remove_stopwords(text, stop_word_file):
    stop_words = read_stopwords(stop_word_file)
    return " ".join([word for word in str(text).split() if word not in stop_words])

def count_words(text, counter):
    for word in str(text).split():
        counter[word] += 1
    return counter

def apply_threshold(counter, threshold = 10):
    # return set of words whose count is above threshold
    return set([word for word, count in counter.items() if count >= threshold])

def prune_by_threshold(text, word_set):
    return " ".join([word for word in str(text).split() if word in word_set])

def apply_remove_stopwords(df, column, stop_word_file, tokenize_option:str|set|list = "nouns"):
    if tokenize_option == "nouns":
        tokenize_func = tokenize_nouns
    elif tokenize_option == "morphs":
        tokenize_func = tokenize
    elif type(tokenize_option) in [set, list]:
        # if tokenize_option is set, use select_by_set
        tokenize_func = lambda x: select_by_set(x, tokenize_option)
    else:
        raise ValueError("tokenize_option should be 'nouns' or 'morphs'")
    # first tokenize, with tqdm to show progress
    for i in tqdm(range(len(df))):
        df.iloc[i, column] = tokenize_func(df.iloc[i, column])
    # for all rows in column 4, apply remove_stopwords
    df.iloc[:, column] = df.iloc[:, column].apply(lambda x: remove_stopwords(x, stop_word_file))
    return df

def apply_count_threshold(df, column, threshold = 10):
    counter = Counter()
    # count words in column 4
    for i in tqdm(range(len(df))):
        counter = count_words(df.iloc[i, column], counter)
    # apply threshold
    word_set = apply_threshold(counter, threshold)
    # prune by threshold
    df.iloc[:, column] = df.iloc[:, column].apply(lambda x: prune_by_threshold(x, word_set))
    return df


path = r'C:\Users\Scarlet\Documents\카카오톡 받은 파일\teamproject'
csv = 'result_add1.csv'
stopwords = 'stopwordsKor_riss.txt'

df = pd.read_csv(os.path.join(path, csv), encoding='utf-8')

# column is 'abstract' at 5th (index 4)
# test default
df = apply_remove_stopwords(df, 4, os.path.join(path, stopwords))

# apply count threshold
df = apply_count_threshold(df, 4, threshold = 10)

# test with set {'NNG', 'NNP'} where NNG is common noun, NNP is proper noun
#df = apply_remove_stopwords(df, 4, os.path.join(path, stopwords), tokenize_option={'NNG', 'NNP'})

# test verb only
#df = apply_remove_stopwords(df, 4, os.path.join(path, stopwords), tokenize_option={'VV'})
# save as csv
df.to_csv(os.path.join(path, 'result_add1_stopwords.csv'), encoding='utf-8', index=False)
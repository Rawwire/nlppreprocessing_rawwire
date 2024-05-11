import os
import re
import sys
import spacy
import unicodedata
import numpy as np 
import pandas as pd 
from bs4 import BeautifulSoup as bs
from spacy.lang.en.stop_words import STOP_WORDS as stopwords 
from textblob import TextBlob



def _get_wordcount(x):
	length= len(str(x).split())
	return length

def _get_charcount(x):
	count=x.split()
	count="".join(count)
	count=len(count)
	return count

def _get_avgwordlength(x):
	avg= _get_charcount(x)/_get_wordcount(x)
	return avg

def _get_stopwordcount(x):
	swcount= len([i for i in x.split() if i in stopwords])
	return swcount 

def _get_hastagscount(x):
	htcount= len([i for i in x if i.startswith('#')])
	return htcount 

def _get_mentionscount(x):
	mcount=len([i for i in x if i.startswith('@')])
	return mcount

def _get_digitcount(x):
	dcount=len([i for i in x.split() if i.isdigit()])
	return dcount

def _get_uppercasecount(x):
	uccount=len([i for i in x if i.isupper()])
	return uccount

def _get_lowercasecount(x):
	lccount= len([i for i in x if i.islower()])
	return lccount

def _get_contractiontoexpansion(x):
    contractions = { 
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he'll've": "he will have",
        "he's": "he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how does",
        "i'd": "i would",
        "i'd've": "i would have",
        "i'll": "i will",
        "i'll've": "i will have",
        "i'm": "i am",
        "i've": "i have",
        "isn't": "is not",
        "it'd": "it would",
        "it'd've": "it would have",
        "it'll": "it will",
        "it'll've": "it will have",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she would",
        "she'd've": "she would have",
        "she'll": "she will",
        "she'll've": "she will have",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so is",
        "that'd": "that would",
        "that'd've": "that would have",
        "that's": "that is",
        "there'd": "there would",
        "there'd've": "there would have",
        "there's": "there is",
        "they'd": "they would",
        "they'd've": "they would have",
        "they'll": "they will",
        "they'll've": "they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        " u ": " you ",
        " ur ": " your ",
        " n ": " and ",
        "won't": "would not",
        'dis': 'this',
        'bak': 'back',
        'brng': 'bring',
        'wanna': "want to",
        'gonna': "going to",
        "i'll" : "i will",
        "it's" : "it is"
    }

    if type(x) is str:
        for key in contractions:
            value = contractions[key]
            x = x.replace(key, value)
        return x 
    else:
        return x


def _get_emailcount(x):
	emcount= len(re.findall(r'([a-z0-9+._-]+@[a-z0-9._-]+\.[a-z]+)',x))
	return emcount

def _remove_email(x):
	remail= re.sub(r"([a-z0-9+._-]+@[a-z0-9._-]+\.[a-z]+)",'',x)
	return remail 

def _get_urlcount(x):
	urlcount = len(re.findall(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', x))
	return urlcount

def _remove_url(x):
	rurl= re.sub(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '' , x)
	return rurl

def _remove_rt(x):
	rrt=re.sub(r'\brt\b', '' ,x).strip()
	return rrt 

def _remove_specialcharacters(x):
	rsp = re.sub(r'[^\w ]+','',x)
	return rsp 

def _remove_multiplespaces(x):
	rms= ' '.join(x.split())
	return rms 

def _remove_htmltags(x):
	rhtml = bs(x,'lxml').get_text().strip()
	return rhtml 

def _remove_accentedcharacters(x):
	rac=unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode('utf-8','ignore')
	return rac

def _remove_stopwords(x):
	rsw=' '.join([i for i in x.split() if i.lower() not in stopwords])
	return rsw 

def _convert_basetoroot(x):
	nlp=spacy.load('en_core_web_sm')
	x=str(x)
	x_list=[]
	doc= nlp(x)
	for token in doc:
		lemma= token.lemma_
		if lemma == '-PRON-' or lemma == 'be':
			lemma=token.text
		x_list.append(lemma)
	return ' '.join(x_list)

def _remove_commonword(x,n=20):
	freq_comm=pd.Series(x).value_counts()
	f20=freq_comm[:n]
	rcw=' '.join([i for i in x.split() if i not in f20])
	return rcw 

def _remove_rareword(x,n=20):
	freq_comm=pd.Series(x).value_counts()
	r20=freq_comm[-n:]
	rrw=' '.join([i for i in x.split() if i not in r20])
	return rrw 

def _spellingcorrection(x):
	sc=TextBlob(x).correct()
	return str(sc)









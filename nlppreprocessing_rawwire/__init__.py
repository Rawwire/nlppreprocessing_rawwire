from nlppreprocessing_rawwire import utils 

__version__ = "0.0.2"

def get_wordcount(x):
	return utils._get_wordcount(x)

def get_charcount(x):
	return utils._get_charcount(x)

def get_avgwordlength(x):
	return utils._get_avgwordlength(x)

def get_stopwordcount(x):
	return utils._get_stopwordcount(x)

def get_hastagscount(x):
	return utils._get_hastagscount(x)

def get_mentionscount(x):
	return utils._get_mentioncount(x)

def get_digitcount(x):
	return utils._get_digitcount(x)

def get_uppercasecount(x):
	return utils._get_uppercasecount(x)

def get_lowercasecount(x):
	return utils._get_lowercasecount(x)

def get_contractiontoexpansion(x):
	return utils._get_contractiontoexpansion(x)

def get_emailcount(x):
	return utils._get_emailcount(x)

def remove_email(x):
	return utils._remove_email(x)

def get_urlcount(x):
	return utils._get_urlcount(x)

def remove_url(x):
	return utils._remove_url(x)

def remove_rt(x):
	return utils._remove_rt(x)

def remove_specialcharacters(x):
	return utils._remove_specialcharacters(x)

def remove_multiplespaces(x):
	return utils._remove_multiplespaces(x)

def remove_htmltags(x):
	return utils._remove_htmltags(x)

def remove_accentedcharacters(x):
	return utils._remove_accentedcharacters(x)

def remove_stopwords(x):
	return utils._remove_stopwords(x)

def convert_basetoroot(x):
	return utils._convert_basetoroot(x)

def remove_commonword(x,n=20):
	return utils._remove_commonword(x,n=20)

def remove_rareword(x,n=20):
	return utils._remove_rareword(x,n=20)

def spellingcorrection(x):
	return utils._spellingcorrection(x)

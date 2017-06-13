from gensim import corpora, models
from gensim.utils import smart_open, simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.matutils import sparse2full
from gensim.models.ldamulticore import LdaMulticore as ldamc
from nltk.stem.wordnet import WordNetLemmatizer
from scipy.linalg import norm
#from scipy.spatial.distance import pdist, squareform
import os
import itertools
import numpy as np

lmtzr = WordNetLemmatizer()

def compute_distance(lda, l1, l2):
	d1 = sparse2full(l1, lda.num_topics)
	d2 = sparse2full(l2, lda.num_topics)
	#sim = np.sqrt(0.5 * ((np.sqrt(dense1) - np.sqrt(dense2))**2).sum())
	return hellinger(d1, d2)

def hellinger(p, q):
	#return squareform(pdist(np.sqrt(X)))/np.sqrt(2)
	return norm(np.sqrt(p) - np.sqrt(q)) / np.sqrt(2)

def tokenize(text):
	return [lmtzr.lemmatize(token) for token in simple_preprocess(text) if token not in STOPWORDS]

def print_topics(lda, dictionary, num_topics = 75):
	i = 0
	for topic in lda.show_topics(num_topics=num_topics, formatted=False):
        	i = i + 1
         	print "Topic #" + str(i) + ":",
         	for p, id in topic:
         		print dictionary[int(id)],
        	print ""

def build_lda(corpus_file, num_topics = 75):
	(dictionary, text, corp) = build_corpus(corpus_file)
	corpus = [dictionary.doc2bow(t) for t in corp]		
	lda = ldamc(corpus,num_topics = num_topics)
	# print_topics(lda, dictionary, num_topics)
	return lda

def build_corpus(corpus_file):
	with open(corpus_file,'r+') as f:
                corp = []
                text = ''
                for line in f:
                        corp.append(tokenize(line.lower()))
                        text = text + line.lower()

                dictionary = corpora.Dictionary(corp)
		return (dictionary, text, corp)

def get_lda_probs(lda_model,document_file):
		(dictionary, doc_text, corp) = build_corpus(document_file)
		# topics = lda.show_topics(num_topics=100, num_words=10)
		# vec_bow = dictionary.doc2bow(doc_text.lower().split())
		vec_bow = dictionary.doc2bow([lmtzr.lemmatize(token) for token in simple_preprocess(doc_text) if token not in STOPWORDS])
		vec_lsi = lda_model[vec_bow]
		return (vec_lsi, doc_text)
	
def find_most_dissimilar(disimilar_values):
	v = ''
	max_val = 0
	for k in disimilar_values.keys():
		if max_val < disimilar_values[k]:
			max_val = disimilar_values[k]
			v = k
			
	if max_val < 0.315673248997:
		v = (None,None)
	return v

def find_pairwise_dissimilar(lda_model, topic_dist, names):
	pairs = list(itertools.product(names,repeat=2))
	pairs_models = list(itertools.product(topic_dist, repeat=2))
	disimilar_values = {}
	for p in xrange(len(pairs)):
		# print pairs[p]
		val = compute_distance(lda_model,*pairs_models[p])
		# Average similarity between stories 0.315673248997
		disimilar_values[pairs[p]] = val

	return disimilar_values
	

# if __name__ == '__main__':
# 	lda_model = build_lda('../data/stories/story_data.dat', num_topics = 100)
# 	find_pairwise_dissimilar(lda_model)


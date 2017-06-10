from gensim import corpora, models
from gensim.utils import smart_open, simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models.ldamulticore import LdaMulticore as ldamc
from nltk.stem.wordnet import WordNetLemmatizer
from scipy.spatial.distance import pdist, squareform

lmtzr = WordNetLemmatizer()

def hellinger(X):
	return squareform(pdist(np.sqrt(X)))/np.sqrt(2)


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
	print_topics(lda, dictionary, num_topics)
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
		return vec_lsi
	

if __name__ == '__main__':
	lda_model = build_lda('../data/story_data.dat', num_topics = 100)
	print get_lda_probs(lda_model, '../data/clapping.dat')

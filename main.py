import sys
import random
import numpy as np

sys.path.append('topic_modelling/')

sys.path.append('chowmein/chowmein')

from label_topic import *
from topic_model import *
from smooth_values import smooth_values

if __name__ == '__main__':
	monument_time_final = smooth_values()
	detection = monument_time_final.keys()
	lda_model = build_lda('data/stories/story_data.dat', num_topics = 50)

	word_dist = {}
	for name in detection:
		word_dist[name] = get_lda_probs(lda_model, 'data/stories/'+name+'.dat')

	monument1,monument2 = find_pairwise_dissimilar(lda_model, word_dist.values(), word_dist.keys())

	_, idx1 = np.argmax(word_dist[monument1],axis=0)
	_, idx2 = np.argmax(word_dist[monument2],axis=0)

	parser = create_parser()

	args = parser.parse_args()
	labels = get_topic_labels(corpus_path=args.line_corpus_path,
		n_topics=args.n_topics,
		n_top_words=args.n_top_words,
		preprocessing_steps=args.preprocessing,
		n_cand_labels=args.n_cand_labels,
		label_min_df=args.label_min_df,
		label_tags=args.label_tags,
		n_labels=args.n_labels,
		lda_random_state=args.lda_random_state,
		lda_n_iter=args.lda_n_iter)

	m1 = labels[word_dist[monument1][idx1][0]]
	m2 = labels[word_dist[monument2][idx2][0]]
	r = random.randint(0,len(m1))
	print monument1
	print monument2
	print '========================================'
	print 'Would you like to listen to a story about the '+(' '.join(m1[r])) +' or the '+(' '.join(m2[r]))+'?'

	
	# print("\nTopical labels:")
	# print("-" * 20)

	# print labels
	# for i, labels in enumerate(labels):
		#print(u"Topic {}: {}\n".format(
		#i,
		#', '.join(map(lambda l: ' '.join(l), labels))
		#))




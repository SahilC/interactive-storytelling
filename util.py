import sys
import random

sys.path.append('topic_modelling/')
sys.path.append('chowmein/chowmein')

from label_topic import *
from topic_model import *
from collections import defaultdict

def calculate_lda_probs(lda_model, detection, lengths):
	word_dist = defaultdict(list)
	stories = defaultdict(list)
	for j in lengths:
		prob, story = get_lda_probs(lda_model, 'data/stories/'+j+'/Introduction.dat')
		word_dist['Introduction.dat'].append(prob)
		stories['Introduction.dat'].append(story)
		prob, story = get_lda_probs(lda_model, 'data/stories/'+j+'/Conclusion.dat')
		word_dist['Conclusion.dat'].append(prob)
		stories['Conclusion.dat'].append(story)

	for name in detection:
		for j in lengths:
			prob, story = get_lda_probs(lda_model, 'data/stories/'+j+'/'+name+'.dat')
			word_dist[name].append(prob)
			stories[name].append(story)
	return word_dist, stories

def get_labels_lda(lda_model):
	labels = get_topic_labels(corpus_path='data/stories/story_data.dat',
		n_topics=50,
		n_top_words=100,
		preprocessing_steps=['wordlen', 'stem', 'tag'],
		n_cand_labels=100,
		label_min_df=2,
		label_tags=['NN,NN', 'JJ,NN'],
		n_labels=10,
		lda_random_state=12345,
		lda_n_iter=400)
	return labels

def form_question(lda_model, labels, word_dist,used_keys = []):
	dissimilar_vals = find_pairwise_dissimilar(lda_model, [j[-1] for j in word_dist.values()], word_dist.keys(), used_keys)
	monument1, monument2 = find_most_dissimilar(dissimilar_vals)

	# print monument1
	# print monument2
	# print '======================================='
	# Find maximum disimilar topics for the topics with the maximum magnitude -- Need to experiment
	_, idx1 = np.argmax(word_dist[monument1][-1],axis=0)
	_, idx2 = np.argmax(word_dist[monument2][-1],axis=0)

	
	m1 = labels[word_dist[monument1][-1][idx1][0]]
	m2 = labels[word_dist[monument2][-1][idx2][0]]
	r1 = random.randint(0,len(m1)-1)
	r2 = random.randint(0,len(m2)-1)
	
	question = {}	
	question['opt1'] = ' '.join(m1[r1])
	# print '========================================'
	question['opt2'] = ' '.join(m2[r2])
	question['m1'] = monument1
	question['m2'] = monument2


	# print 'Would you like to listen to a story about the '+ opt1 +' or the '+ opt2 +'?'
	# opt_select = raw_input()

	# selected = 0
	# if opt_select in opt1:
	# 	selected = monument1
		
	# elif opt_select in opt2:
	# 	selected = monument2

	# if selected == 0:
	# 	print 'Input valid option'

	return question
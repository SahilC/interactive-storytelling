import sys
import random
import numpy as np

sys.path.append('topic_modelling/')

sys.path.append('chowmein/chowmein')

from label_topic import *
from linalg2 import *
from smooth_values import smooth_values
from smooth_values import process_nodetects
from topic_model import *
from util import *

# Settings for code
num_topics = 50
lengths = ['short','long']
filler_types = ['kings','generic']

if __name__ == '__main__':
	monument_time_final, grouped_L = smooth_values()
	idx, idx_monument, stories_order, story_idx = process_nodetects(grouped_L)

	for i in idx_monument.keys():
		monument_time_final[i] += grouped_L[idx_monument[i]][1]

	detection = monument_time_final.keys()
	lda_model = build_lda('data/stories/story_data.dat', num_topics = num_topics)

	word_dist, stories = calculate_lda_probs(lda_model, detection, lengths)

	generic_word_dist = defaultdict(list)
	for j in filler_types:
		for name in os.listdir('data/stories/'+j+'/'):
			prob, story = get_lda_probs(lda_model, 'data/stories/'+j+'/'+name)
			generic_word_dist[name].append(prob)
			stories[name].append(story)

	selected = None
	# selected = form_question(lda_model, word_dist)

	# for p in dissimilar_vals.keys():
	# 	if p[0] == selected and dissimilar_vals[p] < 0.315673248997 and p[1] != selected:
	# 		print p[1], dissimilar_vals[p]

	final_monument_stories = solve_lp_for_stories(monument_time_final, stories, lda_model, selected, word_dist, len(lengths))

	# print stories_order

	print greedy_solver(lda_model, stories_order, story_idx, word_dist, stories, generic_word_dist, grouped_L, idx)





	
	# print("\nTopical labels:")
	# print("-" * 20)

	# print labels
	# for i, labels in enumerate(labels):
		#print(u"Topic {}: {}\n".format(
		#i,
		#', '.join(map(lambda l: ' '.join(l), labels))
		#))




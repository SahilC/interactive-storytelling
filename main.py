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
lengths = ['short','medium','long']
filler_types = ['kings','generic']

def build_stories(file_name):
	monument_time_final, grouped_L = smooth_values(file_name)
	idx, idx_monument, stories_order, story_idx = process_nodetects(grouped_L, monument_time_final)

	# Add the smooth times to monuments time.
	for i in idx_monument.keys():
		monument_time_final[i] += grouped_L[idx_monument[i]][1]

	detection = monument_time_final.keys()

	# Build LDA model for our story data
	lda_model = build_lda('data/stories/story_data.dat', num_topics = num_topics)

	# Compute the LDA probabilites for each of the stories
	word_dist, stories = calculate_lda_probs(lda_model, detection, lengths)

	# Solve LP to select stories about the monuments
	final_monument_stories, final_time = solve_lp_for_stories(monument_time_final, stories, lda_model, word_dist, len(lengths))

	# Populate Datastructures with the LDA probs
	generic_word_dist = defaultdict(list)
	for j in filler_types:
		for name in os.listdir('data/stories/'+j+'/'):
			prob, story = get_lda_probs(lda_model, 'data/stories/'+j+'/'+name)
			generic_word_dist[name].append(prob)
			stories[name].append(story)
			final_monument_stories[name] = story
	# Greedily solve for solution to the Q & A
	selected_stories, gap_fillers = greedy_solver(lda_model, stories_order, story_idx, word_dist, stories, generic_word_dist, grouped_L, idx)
	
	g_x = lp_gap_solver(lda_model, stories, story_idx, word_dist, generic_word_dist, grouped_L, idx)
	# print '================================================'
	final_order = get_final_order(gap_fillers, story_idx, stories_order, grouped_L, monument_time_final, final_time)
	print final_order
	return {'final':final_order ,'stories':stories,'num_gaps':len(idx),'idx':idx, 'final_stories':final_monument_stories}

def very_bad_code(file_name, upvoted, downvoted):
	monument_time_final, grouped_L = smooth_values(file_name)
	idx, idx_monument, stories_order, story_idx = process_nodetects(grouped_L, monument_time_final)

	# Add the smooth times to monuments time.
	for i in idx_monument.keys():
		monument_time_final[i] += grouped_L[idx_monument[i]][1]

	detection = monument_time_final.keys()

	# Build LDA model for our story data
	lda_model = build_lda('data/stories/story_data.dat', num_topics = num_topics)

	# Compute the LDA probabilites for each of the stories
	word_dist, stories = calculate_lda_probs(lda_model, detection, lengths)

	# Populate Datastructures with the LDA probs
	generic_word_dist = defaultdict(list)
	for j in filler_types:
		for name in os.listdir('data/stories/'+j+'/'):
			prob, story = get_lda_probs(lda_model, 'data/stories/'+j+'/'+name)
			generic_word_dist[name].append(prob)
			stories[name].append(story)

	g_x = lp_gap_solver(lda_model, stories, story_idx, word_dist, generic_word_dist, grouped_L, idx, upvoted, downvoted)
	return g_x

if __name__ == '__main__':
	build_stories('data/FILE0573.MOV.txt')
			
	# print("\nTopical labels:")
	# print("-" * 20)

	# print labels
	# for i, labels in enumerate(labels):
		#print(u"Topic {}: {}\n".format(
		#i,
		#', '.join(map(lambda l: ' '.join(l), labels))
		#))




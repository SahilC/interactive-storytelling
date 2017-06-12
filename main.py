import sys

sys.path.append('topic_modelling/')

from topic_model import *
from smooth_values import smooth_values

if __name__ == '__main__':
	monument_time_final = smooth_values()
	detection = monument_time_final.keys()
	lda_model = build_lda('data/stories/story_data.dat', num_topics = 50)

	topic_dist = []
	names = []
	for name in detection:
		topic_dist.append(get_lda_probs(lda_model, 'data/stories/'+name+'.dat'))
		names.append(name)

	print find_pairwise_dissimilar(lda_model, topic_dist, names)

import sys
import numpy as np
import math

from cvxpy import *
from collections import defaultdict

sys.path.append('topic_modelling/')

from topic_model import *

def summary_information(summary):
    time_taken_to_speak_one_word = 2.616
    val = len(summary.split())/time_taken_to_speak_one_word
    return val

def greedy_solver(grouped_L, idx):
    # for i in idx:
    return None

def get_monuments_story(points, l_opts, s_stories,lda_model, selected = None , topic_dist = {}, max_num_s = 3):
    # This function solves the LP
    # as formulated in the report
    # For the time being, the information
    # content of the content summaries and
    # Glue summaries have been fixed.

    # Taking information content as 1
    # for both content and glue sentences

    information_in_content = 1

    s_x = Bool(len(points),max_num_s)


    # Objective Function.
    # In objective function, just change what type of information is to be used.

    objective = Maximize(sum_entries(mul_elemwise(s_stories,s_x)))
    # if selected:
    #     summary_selection += -s_y[i]*sum([ sum([s_x[i][j]*compute_distance(lda_model, topic_dist[selected][j],topic_dist[i][j]) for j in s_sequence])  for i in points ])
    # # summary_selection += sum([ sum([ ((s_x[i][j]*summary_information(content_summaries[i][j], "length_based")) ) for j in s_sequence ]) for i in edges])
    # # Following are the constraints
    constraints = []
    # for i in xrange(len(points)):
    constraints.append(sum_entries(s_x, axis=1) <= np.ones(len(points)))

    # For this constraint always length is used, doesn't matter if Information above is based on content
    # for i in xrange(len(points)):
    constraints.append( sum_entries(mul_elemwise(s_stories,s_x), axis = 1) <= l_opts) 

    problem = Problem(objective, constraints)
    problem.solve()

    print ("-----------------------------")
    # print s_x.value

    return s_x


def build_stories(points, l_opts, s_stories , s_x, max_num_s, stories):
     # Generate final Summary.

    final_summary = {}
    final_time = {}
    for i in xrange(len(points)):
        for j in xrange(max_num_s):
            if ( np.abs(1-s_x[i,j].value) <= 0.0001 ):
                final_summary[points[i]] = str(stories[points[i]][j])
                final_time[points[i]] = s_stories[i][j]

    for i in xrange(len(points)):
        if points[i] not in final_summary.keys():
            final_summary[points[i]] = ""
            final_time[points[i]] = 0
        # else:
        #     print points[i]
        #     print final_summary[points[i]]
        #     print final_time[points[i]]
        #     print l_opts[points[i]]
        #     print '===================='

    # print("final_videos : " + str(final_summary))
    # print("final_time : " + str(final_time))

    lp_error = []
    path_summary = ''
    for i in points:
        lp_error.append(np.int32(np.abs(l_opts[i] - final_time[i])))

    print("STORY SUMMED_ERROR : " + str(lp_error))
    return final_summary

def solve_lp_for_stories(l_opts = {}, stories = defaultdict(list) ,lda_model = None, selected = None, topic_distances = {}, max_num_s = 3):
    # Build parameters for story-generation 
    points = l_opts.keys()
    s_stories = np.zeros((len(points), max_num_s),dtype=np.float64)
    t_stories = np.zeros((len(points), max_num_s),dtype=np.float64)
    tot = 0
    l_ot = []
    for i in xrange(len(points)):
        l_ot.append(l_opts[points[i]])
        for j in xrange(max_num_s):
            s_stories[i][j] = summary_information(stories[points[i]][j])
            t_stories[i][j] = summary_information(stories[points[i]][j])
            # print points[i],l_opts[points[i]], s_stories[i][j]
        # print '========================='
    
        # tot += l_opts[i]
    l_ot = np.array(l_ot)

    s_x = get_monuments_story(points, l_ot, s_stories, lda_model, selected, topic_distances, max_num_s)
    story = build_stories(points, l_opts, t_stories, s_x, max_num_s, stories)
    return story






import sys
import numpy as np
import math
import random

from cvxpy import *
from collections import defaultdict

sys.path.append('topic_modelling/')

from topic_model import *
from util import *

def summary_information(summary):
    time_taken_to_speak_one_word = 2.616
    val = len(summary.split())/time_taken_to_speak_one_word
    return val

def get_final_order(gap_fillers, story_idx, story_order, monument_time):
    final_order = []
    cumulative_time = 0
    for j in xrange(len(story_idx)-1):
        final_order.append({'name':story_order[j],'time':cumulative_time,'type':'story'})
        cumulative_time += monument_time[story_order[j]]
        for i in gap_fillers.keys():
            if story_idx[j] < i and i < story_idx[j+1]:
                temp = gap_fillers[i]['time']
                gap_fillers[i]['time'] = cumulative_time

                final_order.append(gap_fillers[i])
                cumulative_time += temp
    # print "Final Story time:"
    # print cumulative_time

    return final_order

def lp_gap_solver(lda_model, story, story_idx, word_dist, generic_word_dist, grouped_L, idx, upvoted = [], downvoted = []):
    possible_stories = []
    for i in idx:
        for j in xrange(len(story_idx)-1):
            if story_idx[j] < i and i < story_idx[j+1]:
                m1 =  grouped_L[story_idx[j]][0]
                m2 =  grouped_L[story_idx[j+1]][0]
                possible_stories.append([i,m1,m2,grouped_L[i][1]])
                break

    g_x = Bool(len(idx),len(generic_word_dist.keys()))

    s_stories = np.zeros((len(idx),len(generic_word_dist.keys())),dtype=np.float64)

    constraints = []
    keys = generic_word_dist.keys()
    for i in xrange(len(idx)):
        for j in xrange(len(keys)):
            s_stories[i][j] = (1-find_distance(lda_model, word_dist, generic_word_dist, possible_stories[i][1],possible_stories[i][2], keys[j])) 
            for k in upvoted:
                if k != '':
                    if k in word_dist.keys():
                        d1 = word_dist[k][-1]
                    else:
                        d1 = generic_word_dist[k][-1]
                    print d1
                    print generic_word_dist[keys[j]][-1]
                    s_stories[i][j] += (1-compute_distance(lda_model, d1, generic_word_dist[keys[j]][-1]))  
            for k  in downvoted:
                d1 = ''
                if k != '':
                    if k in word_dist.keys():
                        d1 = word_dist[k][-1]
                    else:
                        d1 = generic_word_dist[k][-1]
                    s_stories[i][j] += compute_distance(lda_model, d1, generic_word_dist[keys[j]][-1])
            constraints.append((summary_information(story[keys[j]][-1]))*g_x[i,j] <= possible_stories[i][-1])

    # Objective Function.
    # In objective function, just change what type of information is to be used.

    objective = Maximize(sum_entries(mul_elemwise(s_stories,g_x)))
    
    # # Following are the constraints
    
    constraints.append(sum_entries(g_x, axis=1) == np.ones(len(idx)))
        
    constraints.append(sum_entries(g_x, axis=0) <= np.ones((1,len(generic_word_dist.keys()))))

    # For this constraint always length is used, doesn't matter if Information above is based on content
    # constraints.append( sum_entries(mul_elemwise(s_stories,s_x), axis = 1) <= l_opts) 

    problem = Problem(objective, constraints)
    problem.solve()

    print g_x.value
    for i in xrange(len(idx)):
        for j in xrange(len(keys)):
            # print idx[i],keys[j], possible_stories[i][-1], summary_information(story[keys[j]][-1])
            if (1-g_x.value[i,j]) <= 0.00000001:
                print idx[i],keys[j], possible_stories[i][-1], summary_information(story[keys[j]][-1])

    print "-----------------------------"
    return g_x
        

def greedy_solver(lda_model, story_order, story_idx, word_dist, stories, generic_word_dist, grouped_L, idx):
    used_stories = []
    new_order = []
    labels = get_labels_lda(lda_model)
    gap_fillers = {}
    for i in idx:
        possible_stories = []
        for j in xrange(len(story_idx)-1):
            if story_idx[j] < i and i < story_idx[j+1]:
                m1 =  grouped_L[story_idx[j]][0]
                m2 =  grouped_L[story_idx[j+1]][0]
                break
        # m1 = grouped_L[i-1][0]
        # m2 = grouped_L[i+1][0]
        # print m1
        # print m2
        # print 'GAP:',i
        flag = True
        for j in generic_word_dist.keys():
            val1 = compute_distance(lda_model, word_dist[m1][-1], generic_word_dist[j][-1])
            val2 = compute_distance(lda_model, word_dist[m2][-1], generic_word_dist[j][-1])
            # print j, summary_information(stories[j][-1]), grouped_L[i][1]
            if val1 < 0.3 and val2 < 0.3 and summary_information(stories[j][-1]) < grouped_L[i][1] and j not in used_stories:
                # print stories[j][-1]
                used_stories.append(j)
                gap_fillers[i] = {'story':j,'type':'story','time':summary_information(stories[j][-1])}
                flag = False
                break
            elif summary_information(stories[j][-1]) < grouped_L[i][1]:
                possible_stories.append(j)
        if flag:
            # print m1
            # print m2
            # print used_stories
            # print len(used_stories)
            if len(possible_stories) == 0:
                selected = None
            elif len(possible_stories) == 1:
                if possible_stories[-1] not in used_stories:
                    selected = possible_stories[-1]
                else: 
                    selected = None
                gap_fillers[i] = {'story':selected,'type':'story','time':grouped_L[i][1]}
            else:
                selected = form_question(lda_model, labels, generic_word_dist, used_stories)
                gap_fillers[i] = {'story':selected,'type':'question','time':grouped_L[i][1]}
            used_stories.append(selected)
            # print stories[selected][-1]
            # print '==========================='
    
    return used_stories, gap_fillers

def get_monuments_story(points, l_opts, s_stories,lda_model, topic_dist = {}, max_num_s = 3):
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

    # print("STORY SUMMED_ERROR : " + str(lp_error))
    return final_summary

def solve_lp_for_stories(l_opts = {}, stories = defaultdict(list) ,lda_model = None, topic_distances = {}, max_num_s = 3):
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

    s_x = get_monuments_story(points, l_ot, s_stories, lda_model, topic_distances, max_num_s)
    story = build_stories(points, l_opts, t_stories, s_x, max_num_s, stories)
    return story





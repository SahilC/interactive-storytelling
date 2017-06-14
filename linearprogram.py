
import pulp
import sys

from collections import defaultdict

sys.path.append('topic_modelling/')

from topic_model import *

def summary_information(summary):
    time_taken_to_speak_one_word = 2.616
    val = len(summary.split())/time_taken_to_speak_one_word
    return val

def get_monuments_story(points, l_opts, s_stories,lda_model, selected = None , topic_dist = {}, max_num_s = 3):
    # This function solves the LP
    # as formulated in the report
    # For the time being, the information
    # content of the content summaries and
    # Glue summaries have been fixed.

    # Taking information content as 1
    # for both content and glue sentences

    information_in_content = 1

    s_sequence = range(0,max_num_s)
    s_x = pulp.LpVariable.dicts("selected_content_stories",
                                (points, s_sequence),
                                0,
                                1,
                                pulp.LpInteger)


    summary_selection = pulp.LpProblem("story selection problem",pulp.LpMaximize)


    # Objective Function.
    # In objective function, just change what type of information is to be used.

    summary_selection += sum([ sum([ ((s_x[i][j]*s_stories[i][j])) for j in s_sequence ]) for i in points])
    if selected:
        pass
        #summary_selection += -1*sum([ sum([s_x[i][j]*compute_distance(lda_model, topic_dist[selected][j],topic_dist[i][j]) for j in s_sequence])  for i in points ])
    # summary_selection += sum([ sum([ ((s_x[i][j]*summary_information(content_summaries[i][j], "length_based")) ) for j in s_sequence ]) for i in edges])
    # Following are the constraints
    for i in s_x:
        summary_selection += (sum([ s_x[i][j] for j in s_sequence ]) == 1)

    # For this constraint always length is used, doesn't matter if Information above is based on content
    for i in s_x:
        summary_selection += sum([ ((s_x[i][j]*s_stories[i][j])) for j in s_sequence ]) <= l_opts[i]

    summary_selection.solve()

    print ("-----------------------------")

    return (s_x, s_sequence)


def build_stories(points, l_opts, s_stories , s_x, s_sequence, stories):
     # Generate final Summary.

    final_summary = {}
    final_time = {}
    for i in s_x:
        for j in s_sequence:
            # print s_x[i][j].value(),
            if (int(s_x[i][j].value())==1):
                final_summary[i] = str(stories[i][j])
                final_time[i] = s_stories[i][j]
        # print 

    for i in s_x:
        if i not in final_summary.keys():
            final_summary[i] = ""
            final_time[i] = 0

    print("final_videos : " + str(final_summary))
    print("final_time : " + str(final_time))

    lp_error = []
    path_summary = ''
    for i in points:
        lp_error.append(int(float(abs(l_opts[i] - final_time[i]))))

    print("STORY SUMMED_ERROR : " + str(lp_error))
    return final_summary

def solve_lp_for_stories(l_opts = {}, stories = defaultdict(list) ,lda_model = None, selected = None, topic_distances = {}, max_num_s = 3):
    # Build parameters for story-generation 
    points = l_opts.keys()
    s_stories = defaultdict(list)
    tot = 0
    for i in l_opts.keys():
        for j in xrange(0,max_num_s):
            s_stories[i].append(None)

        for j in xrange(0,max_num_s):
            s_stories[i][j] = summary_information(stories[i][j])
            # print l_opts[i], s_stories[i][j],
        # print 
    
        tot += l_opts[i]


    s_x, s_seq = get_monuments_story(points, l_opts, s_stories, lda_model, selected, topic_distances, max_num_s)
    story = build_stories(points, l_opts, s_stories, s_x, s_seq, stories)
    return story




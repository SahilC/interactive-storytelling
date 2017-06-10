import pulp

def summary_information(summary):
    time_taken_to_speak_one_word = 2.616
    val = len(summary.split())/time_taken_to_speak_one_word
    return val

def get_path_video_lp(edges, content_summaries, l_opts, s_edges, max_num_s):
    # This function solves the LP
    # as formulated in the report
    # For the time being, the information
    # content of the content summaries and
    # Glue summaries have been fixed.

    # Taking information content as 1
    # for both content and glue sentences

    information_in_content = 1
    information_in_glue = 1

    alpha = 1
    beta = 1

    s_sequence = range(0,max_num_s)
    s_x = pulp.LpVariable.dicts("selected_content_videos",
                                (edges, s_sequence),
                                0,
                                1,
                                pulp.LpInteger)


    summary_selection = pulp.LpProblem("video selection problem",pulp.LpMaximize)


    # Objective Function.
    # In objective function, just change what type of information is to be used.

    summary_selection += sum([ sum([ ((s_x[i][j]*s_edges[i][j][1])) for j in s_sequence ]) for i in edges])
    # summary_selection += sum([ sum([ ((s_x[i][j]*summary_information(content_summaries[i][j], "length_based")) ) for j in s_sequence ]) for i in edges])
    # Following are the constraints
    for i in s_x:
        summary_selection += sum([ s_x[i][j] for j in s_sequence ]) <= 1

    # For this constraint always length is used, doesn't matter if Information above is based on content
    for i in s_x:
        summary_selection += sum([ ((s_x[i][j]*s_edges[i][j][1])) for j in s_sequence ]) <= l_opts[i]

    summary_selection.solve()

    # Generate final Summary.
    final_summary = {}
    final_time = {}

    print ("-----------------------------")

    for i in s_x:
        for j in s_sequence:
            if (int(s_x[i][j].value())==1):
                final_summary[i] = str(content_summaries[i][j])
                final_time[i] = s_edges[i][j][1]

    for i in s_x:
        if i not in final_summary.keys():
            final_summary[i] = ""

    print("final_videos : " + str(final_summary))
    print("final_time : " + str(final_time))

    lp_error = []
    path_summary = ''
    for i in edges:
        lp_error.append(int(float(abs(l_opts[i] - final_time[i]))))

    print("VIDEO LP_SUMMED_ERROR : " + str(lp_error))
    return str(final_summary)

# def get_path_summary_lp(edges, content_summaries, glue_summaries, l_opts, s_edges, g_edges, max_num_s):
#     # This function solves the LP
#     # as formulated in the report
#     # For the time being, the information
#     # content of the content summaries and
#     # Glue summaries have been fixed.

#     # Taking information content as 1
#     # for both content and glue sentences

#     information_in_content = 1
#     information_in_glue = 1

#     alpha = 1
#     beta = 1

#     s_sequence = range(0,max_num_s)
#     s_x = pulp.LpVariable.dicts("selected_content_summaries",
#                                 (edges, s_sequence),
#                                 0,
#                                 1,
#                                 pulp.LpInteger)

#     g_x = pulp.LpVariable.dicts("selected_glue_summaries",
#                                 (edges, s_sequence),
#                                 0,
#                                 1,
#                                 pulp.LpInteger)

#     summary_selection = pulp.LpProblem("summary selection problem",
#                                 pulp.LpMaximize)


#     # Objective Function.
#     # In objective function, just change what type of information is to be used.

#     summary_selection += sum([ sum([ ((s_x[i][j]*summary_information(content_summaries[i][j])) + ( g_x[i][j]*summary_information(glue_summaries[i][j]) )) for j in s_sequence ]) for i in edges])
#     # summary_selection += sum([ sum([ ((s_x[i][j]*summary_information(content_summaries[i][j], "length_based")) ) for j in s_sequence ]) for i in edges])
#     # Following are the constraints
#     for i in s_x:
#         summary_selection += sum([ s_x[i][j] for j in s_sequence ]) <= 1

#     for i in g_x:
#         summary_selection += sum([ g_x[i][j] for j in s_sequence ]) <= 1

#     # For this constraint always length is used, doesn't matter if Information above is based on content
#     for i in s_x:
#         summary_selection += sum([ ((s_x[i][j]*summary_information(content_summaries[i][j]))+( g_x[i][j]*summary_information(glue_summaries[i][j]))) for j in s_sequence ]) <= l_opts[i]

#     summary_selection.solve()

#     # Generate final Summary.
#     final_summary = {}
#     final_summary_glue = {}
#     final_summary_content = {}

#     for i in s_x:
#         for j in s_sequence:
#             if (int(g_x[i][j].value())==1):
#                 final_summary[i] = glue_summaries[i][j]
#                 final_summary_glue[i] = glue_summaries[i][j]
#         if i not in final_summary_glue.keys():
#             final_summary_glue[i] = ""

#     print ("-----------------------------")

#     for i in s_x:
#         for j in s_sequence:
#             if (int(s_x[i][j].value())==1):
#                 if i in final_summary.keys():
#                     final_summary[i] = final_summary[i] + str(content_summaries[i][j])
#                 else:
#                     final_summary[i] = str(content_summaries[i][j])
#                 final_summary_content[i] = str(content_summaries[i][j])
#         if i not in final_summary_content.keys():
#             final_summary_content[i] = ""

#     for i in s_x:
#         if i not in final_summary.keys():
#             final_summary[i] = ""

#     print("final_summary : " + str(final_summary_content))

#     lp_error = []
#     path_summary = ''
#     for i in edges:
#         print l_opts[i]
#         lp_error.append(int(float(abs(l_opts[i] - summary_information(final_summary_content[i])))))
#         path_summary = path_summary + str(final_summary[i])
#     print("LP_SUMMED_ERROR : " + str(lp_error))
#     return str(path_summary)

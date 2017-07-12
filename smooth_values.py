from collections import defaultdict
from collections import Counter
from itertools import groupby
import numpy as np

# Mapping of merged interest points
story_mapping = {
		'curtainwall':'balahissardarwaza', 
		'balahissardarwaza':'balahissardarwaza', 
		'clappingportico':'balahissardarwaza',
		'victoriacannon':'balahissardarwaza',
		'guestroom':'akkannamadannaoffices',
		'guestroommosque': 'akkannamadannaoffices',
		'akkannamadannaoffice':'akkannamadannaoffices',
		'naginabagh':'naginabagh', 
		'naginamosque':'naginabagh',
		'lowertank':'commonerstairs', 
		'commonerstairs':'commonerstairs', 
		'middletank':'commonerstairs', 
		'uppertank':'commonerstairs',
		'ramdasjail':'ramdasjail', 
		'ambarkhana':'ramdasjail',
		'ambharkhana':'ramdasjail',
		'royalstairs':'royalstairs', 
		'zenanabodyguards':'royalstairs',
		'hallofwhispers':'ranimahal', 
		'ranimahal':'ranimahal', 
		'shahihammam':'ranimahal',
}

def process_nodetects(grouped_L, monument_time_final, sampling_rate = 5):
	idx = []
	idx_monument = {}
	i = 0
	stories_order = []
	story_idx = []
	for (k,v) in grouped_L:
		if k not in stories_order and k != 'NoDetect':
			stories_order.append(k)
			v = 0
			i_val = 0
			max_val = 0
			for (k1,v1) in grouped_L:
				if max_val < v1 and k1 == k:
					# other_monuments = []
					max_val = v1
					i_val = v
				v += 1
			story_idx.append(i_val)
		elif i < (len(grouped_L) - 1) and grouped_L[i+1][0] == grouped_L[i-1][0] and k == 'NoDetect':
			if grouped_L[i-1][0] != 'NoDetect':
				monument_time_final[grouped_L[i-1][0]] += v
		elif k == 'NoDetect' and v < 10:
			if grouped_L[i-1][0] != 'NoDetect':
				monument_time_final[grouped_L[i-1][0]] += v
		elif k == 'NoDetect' and v > 10:
			idx.append(i)
		i += 1

	sorted_idx = np.argsort(story_idx)
	stories_order = [stories_order[i] for i in sorted_idx]
	story_idx = [story_idx[i] for i in sorted_idx]
	return idx, idx_monument, stories_order, story_idx

def smooth_values(file_name = 'data/FILE0573.MOV.txt', sampling_rate = 1):
	
	monument_time_final = defaultdict(int)
	order = 1
	detection = []
	detection2 = []
	
	# Read detections from generated file
	with open(file_name,'r+') as f:
		lines = f.read().split("\n")
		c = 0	
		for l in lines:
			if c % sampling_rate == 0:
				val = l.split(" ")
				if val[1].split("_")[0] in story_mapping.keys():
					temp = story_mapping[val[1].split("_")[0]]
					detection.append(temp)
					detection2.append(temp)
				else:	
					detection.append(val[1].split("_")[0])
					detection2.append(val[1].split("_")[0])
			c += 1

	# Iterate over them and smooth the detections
	
	t = 0	
	for l in xrange(0,len(lines),sampling_rate):
		val = lines[l].split(" ")
		if float(val[2])*float(val[3]) < 1:
			detection2[t] = 'NoDetect'
		t+=1
	
	t = 0
	for l in xrange(0, len(lines),sampling_rate):
		val = lines[l].split(" ")
		v = ''
		# other_monuments = []
		tot = 0
		order = 15
		max_val = 0
		# other_monuments = [None]
		v = '' 
		# while(len(other_monuments) != 0):
		lower = t - order
		upper = t + order
		if lower < 0:
			lower = 0
		if upper >= len(detection2):
			upper = len(detection2) - 1

		max_freq = Counter(detection2[lower:upper])
		
		for k in max_freq.keys():
			tot += max_freq[k]
			if max_val < max_freq[k]:
				# other_monuments = []
				max_val = max_freq[k]
				v = k
			# elif max_val == max_freq[k]:
			# 	other_monuments.append(k)

		if v != 'NoDetect' and v != '' and max_val > order:
		 	monument_time_final[v] += 1

		if v != '' and max_val > order:
			detection[t] = v
		else:
			detection[t] = 'NoDetect'			
			#frame_detections[val[0]]['detection'] = val[1]
			#frame_detections[val[0]]['threshold'] = float(val[2])*float(val[3])
			# print val[0],val[1]
			# if monument != v:
			# 	print 'Correction',v
		
		# for i in xrange(len(detection2)):
		# 	if detection2[i] not in monument_time.keys():
		# 		detection2[i] = 'NoDetect'
		# 	else:
		# 		monument_time_final[detection2[i]] += 1

		t += 1
	# print detection2
	# print monument_time_final
	tot = 0
	for i in monument_time_final.keys():
		monument_time_final[i]*= (sampling_rate / 30.0)
		tot += monument_time_final[i]

	# print '=================================='
	grouped_L = []
	for k,g in groupby(detection):
		val = sum(1 for i in g)
		if val > 10:
			if len(grouped_L) > 0 and grouped_L[-1][0] == k:
				grouped_L[-1][1] += (sampling_rate / 30.0)*val
			else:
				grouped_L.append([k, (sampling_rate / 30.0)*val])
	
	for i in xrange(len(grouped_L) -1):
		if grouped_L[i][0] != 'NoDetect' and grouped_L[i + 1][0] == 'NoDetect':
			monument_time_final[grouped_L[i][0]] += grouped_L[i + 1][1]

	print grouped_L
	# print monument_time_final

	return monument_time_final, grouped_L
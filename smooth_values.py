from collections import defaultdict
from collections import Counter
from itertools import groupby

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
			story_idx.append(i)
		elif i < (len(grouped_L) - 1) and grouped_L[i+1][0] == grouped_L[i-1][0] and k == 'NoDetect':
			monument_time_final[grouped_L[i-1][0]] += v
		elif k == 'NoDetect' and v < 10:
			monument_time_final[grouped_L[i-1][0]] += v
		elif k == 'NoDetect' and v > 10:
			idx.append(i)
		i += 1

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
		if float(val[2])*float(val[3]) < 3:
			detection2[t] = 'NoDetect'
		t+=1

	
	t = 0
	for l in xrange(order,len(lines) - order,sampling_rate):
		val = lines[l].split(" ")
		order = 30
		other_monuments = [None]
		v = '' 
		while(len(other_monuments) != 0):
			order += 2
			max_freq = Counter(detection2[t-order:t+order])
			v = ''
			max_val = 0
			other_monuments = []
			for k in max_freq.keys():
				if max_val < max_freq[k]:
					other_monuments = []
					max_val = max_freq[k]
					v = k
				elif max_val == max_freq[k]:
					other_monuments.append(k)

		if len(other_monuments) == 0:
			if v != 'NoDetect' and v != '':
			 	monument_time_final[v] += 1
			
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
		monument_time_final[i]*= (sampling_rate / 24.0)
		tot += monument_time_final[i]

	grouped_L = []
	for k,g in groupby(detection2):
		val = sum(1 for i in g)
		if val > 10:
			if len(grouped_L) > 0 and grouped_L[-1][0] == k:
				grouped_L[-1][1] += (sampling_rate / 24.0)*val
			else:
				grouped_L.append([k, (sampling_rate / 24.0)*val])
	print monument_time_final
	print grouped_L
	print '========================'
	return monument_time_final, grouped_L
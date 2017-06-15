from collections import defaultdict
from collections import Counter
from itertools import groupby

# Mapping of merged interest points
story_mapping = {
		'curtainwall':'balahissardarwaza', 
		'balahissardarwaza':'balahissardarwaza', 
		'clappingportico':'balahissardarwaza',
		'victoriacannon':'balahissardarwaza',
		'guestroom':'akkannamadannaoffice', 
		'akkannamadannaoffice':'akkannamadannaoffice',
		'naginabagh':'naginabagh', 
		'naginamosque':'naginabagh',
		'lowertank':'commonerstairs', 
		'commonerstairs':'commonerstairs', 
		'middletank':'commonerstairs', 
		'uppertank':'commonerstairs',
		'ramdasjail':'ramdasjail', 
		'ambarkhana':'ramdasjail',
		'royalstairs':'royalstairs', 
		'zenanabodyguards':'royalstairs',
		'hallofwhispers':'ranimahal', 
		'ranimahal':'ranimahal', 
		'shahihammam':'ranimahal',
}

def process_nodetects(grouped_L, sampling_rate = 5):
	idx = []
	i = 0
	for (k,v) in grouped_L:
		if k == 'NoDetect' and v > 10:
			idx.append(i)
		i += 1

	idx_monument = {}
	for i in idx:
		if grouped_L[i+1][0] == grouped_L[i-1][0]:
			idx_monument[grouped_L[i-1][0]] = i
	return idx, idx_monument

def smooth_values(file_name = 'data/FILE0573.MOV.txt', sampling_rate = 5):
	
	monument_time = defaultdict(int)
	order = 1
	detection = []
	detection2 = []
	
	# Read detections from generated file
	with open(file_name,'r+') as f:
		lines = f.read().split("\n")	
		for l in lines:
			val = l.split(" ")
			if val[1].split("_")[0] in story_mapping.keys():
				temp = story_mapping[val[1].split("_")[0]]
				detection.append(temp)
				detection2.append(temp)
			else:	
				detection.append(val[1].split("_")[0])
				detection2.append(val[1].split("_")[0])

	# Iterate over them and smooth the detections
	for l in xrange(order,len(lines) - order):
		val = lines[l].split(" ")
		order = 1
		other_monuments = [None]
		v = '' 
		while(len(other_monuments) != 0):
			order += 2
			max_freq = Counter(detection[l-order:l+order])
			v = ''
			max_val = 0
			other_monuments = []
			for k in max_freq.keys():
				# print k,max_freq[k],'===================='
				if max_val < max_freq[k]:
					other_monuments = []
					max_val = max_freq[k]
					v = k
				elif max_val == max_freq[k]:
					other_monuments.append(k)
			# print '==================='
			
		if len(other_monuments) == 0:
		 	detection2[l] = v

		 
		if float(val[2])*float(val[3]) > 3:
			monument_time[v] += 1
			#frame_detections[val[0]]['detection'] = val[1]
			#frame_detections[val[0]]['threshold'] = float(val[2])*float(val[3])
			# print val[0],val[1]
			# if monument != v:
			# 	print 'Correction',v
		monument_time_final = defaultdict(int)
		for i in xrange(len(detection2)):
			if detection2[i] not in monument_time.keys():
				detection2[i] = 'NoDetect'
			else:
				monument_time_final[detection2[i]] += 1

		tot = 0
		for i in monument_time_final.keys():
			monument_time_final[i]*= (sampling_rate / 24.0)
			tot += monument_time_final[i]

	# print detection2
	grouped_L = []
	for k,g in groupby(detection2):
		val = sum(1 for i in g)
		if val > 10:
			if len(grouped_L) > 0 and grouped_L[-1][0] == k:
				grouped_L[-1][1] += (sampling_rate / 24.0)*val
			else:
				grouped_L.append([k, (sampling_rate / 24.0)*val])
	return monument_time_final, grouped_L
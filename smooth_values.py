from collections import defaultdict
from collections import Counter

def smooth_values(file_name = 'data/FILE0573.MOV.txt', sampling_rate = 5):
	with open(file_name,'r+') as f:
		lines = f.read().split("\n")
		monument_time = defaultdict(int)
		detection = []
		detection2 = []
		for l in lines:
			val = l.split(" ")
			detection.append(val[1].split("_")[0])
			detection2.append(val[1].split("_")[0])

		for l in xrange(50,len(lines)):
			val = lines[l].split(" ")
			order = 1
			others = ['what']
			v = detection2[l] 
			# while(len(others) != 0):
			# 	order += 2
			# 	max_freq = Counter(detection[l-order:l+order])
			# 	v = ''
			# 	max_val = 0
			# 	others = []
			# 	for k in max_freq.keys():
			# 		# print k,max_freq[k],'===================='
			# 		if max_val < max_freq[k]:
			# 			others = []
			# 			max_val = max_freq[k]
			# 			v = k
			# 		elif max_val == max_freq[k]:
			# 			others.append(k)
			# 	# print '==================='
				
			# if len(others) == 0:
			#  	detection2[l] = v

			 
			if float(val[2])*float(val[3]) > 0:
				monument_time[v] += 1
				#frame_detections[val[0]]['detection'] = val[1]
				#frame_detections[val[0]]['threshold'] = float(val[2])*float(val[3])
				# print val[0],val[1]
				# if monument != v:
				# 	print 'Correction',v
		tot = 0
		for m in monument_time.keys():
			monument_time[m] *= sampling_rate
			tot += monument_time[m]

		# tot /= (30.0*60)
		print tot
		print '================'

	return monument_time


if __name__ == '__main__':
	print smooth_values()


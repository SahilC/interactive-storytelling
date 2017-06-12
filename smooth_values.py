from collections import defaultdict
from collections import Counter

def smooth_values(file_name = 'data/FILE0573.MOV.txt', sampling_rate = 5):
	with open(file_name,'r+') as f:
		lines = f.read().split("\n")
		monument_time = defaultdict(int)
		order = 1
		detection = []
		detection2 = []
		for l in lines:
			val = l.split(" ")
			detection.append(val[1].split("_")[0])
			detection2.append(val[1].split("_")[0])


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

			 
			if float(val[2])*float(val[3]) > 5:
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

		print detection2
		# print monument_time_final
		# tot /= (30.0*60)
		tot = 0
		for i in monument_time_final.keys():
			monument_time_final[i]*= (sampling_rate / 24.0)
			tot += monument_time_final[i]

		print monument_time_final
		print tot
		# print '================'

	return monument_time


if __name__ == '__main__':
	print smooth_values()


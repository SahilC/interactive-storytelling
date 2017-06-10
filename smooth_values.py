from collections import defaultdict
def smooth_values(file_name = 'data/FILE0573.MOV.txt', sampling_rate = 5):
	with open(file_name,'r+') as f:
		lines = f.read().split("\n")
		monument_time = defaultdict(int)
		for l in lines:
			val = l.split(" ")
			if float(val[2])*float(val[3]) > 0:
				monument = val[1].split("_")[0]
				monument_time[monument] += 1
				#frame_detections[val[0]]['detection'] = val[1]
				#frame_detections[val[0]]['threshold'] = float(val[2])*float(val[3])
				print val[0],val[1]
		tot = 0
		for m in monument_time.keys():
			monument_time[m] *= sampling_rate
			tot += monument_time[m]

		tot /= (30.0*60)
		print tot
		print '================'

	return monument_time


if __name__ == '__main__':
	print smooth_values()


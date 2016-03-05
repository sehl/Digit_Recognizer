# Sara E. Hansen-Lund
# For use with Kaggle Digit Recognizer data
# Uses python 2.7 & numpy
# March 5, 2016
from numpy import mean
from numpy import std
from math import sqrt

TRAIN = '_train.csv'
TEST = '_test.csv'

def get_data(filename):
	data = dict(zip([ i for i in range(10) ], [ [] for i in range(10)]))
	with open(filename) as f:
		header = f.readline()
		for line in f:
			d = line[:-1].split(',')

			data[int(d[0])].append([ int(n) for n in d[1:] ])
			
	return data

def get_means_and_devs(data):
	
	means = dict()
	stddevs = dict()
	for cat in data:
		means[cat] = [ mean(row) for row in zip(*(data[cat])) ]
		stddevs[cat] = [ std(row) for row in zip(*(data[cat])) ]

	return means, stddevs

# sums the absolute value of the z-scores for the given pixels for each category type.
# m: the mean dictionary
# s: the standard deviation dictionary
# pixels=None indicates that all pixels are to be summed
# returns a list of the sums for each category
def calc_sum_devs(data, m, s, pixels=None):
	results = list()
	for cat in m:
		results.append(sum([ abs(data[i] - m[cat][i]) / (s[cat][i]+1) for i in range(784) ]))
	
	return results

# sums the absolute value of the z-scores for the given pixels for each category type.
# m: the mean dictionary
# pixels=None indicates that all pixels are to be summed
# returns a list of the sums for each category
def calc_euc_dists(data, m, pixels=None):
	results = list()
	for cat in m:
		results.append(sqrt(sum([ (data[i] - m[cat][i])**2 for i in range(784) ])))
	
	return results

# Method 1 is using the sum of the z-scores for each category
# Method 2 is using the euclidean distance from the means of each category
def main():
	avgs, stds = get_means_and_devs(get_data(TRAIN))

	data = get_data(TEST)
	total = 0
	correct1 = 0
	correct2 = 0
	for cat in data:
		for d in data[cat]:
			r1 = calc_sum_devs(d, avgs, stds)
			predicted1 = r1.index(min(r1))
			r2 = calc_sum_devs(d, avgs, stds)
			predicted2 = r2.index(min(r2))
#			print(r)
#			print('actual: ' + str(cat) + '\t'\
#				+ 'predicted: ' + str(predicted))

			total += 1
			if cat == predicted1:
				correct1 += 1
			if cat == predicted2:
				correct2 += 1
#			else:
#				print(r)
#				print('actual: ' + str(cat) + '\t'\
#					+ 'predicted: ' + str(predicted))
	
	print(str(total) + " data tested")
	print("Method 1: " + str(correct1) + " predicted correctly")
	print("Method 1: " + str(round(100.0*correct1 / total, 2)) + "% correct")
	print("Method 2: " + str(correct2) + " predicted correctly")
	print("Method 2: " + str(round(100.0*correct2 / total, 2)) + "% correct")


if __name__ == '__main__':
	main()



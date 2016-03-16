# Sara E. Hansen-Lund
# For use with Kaggle Digit Recognizer data
# Uses python 2.7, numpy, & sklearn.cluster.KMeans
# March 7, 2016
import numpy as np
from scipy.misc import imsave
from scipy.misc import imresize
from scipy.spatial.distance import euclidean
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression

TRAIN = 'data/train.csv'
TEST = 'data/test.csv'

NUM_CLUSTERS = 100

# retrieves a dict mapping categories to training data. Data is presented
# as a list of images represented as 2-d numpy arrays.
def get_data(filename):
	data = dict(zip([ i for i in range(10) ], [ [] for i in range(10)]))
	with open(filename) as f:
		header = f.readline()
		for line in f:
			d = line[:-1].split(',')

			data[int(d[0])].append([ int(n) for n in d[1:] ])
			
	return data

# data is a dict mapping categories to a list of data values
# returns a dict mapping expanded categories to their respective mean arrays
def get_means(data):
	learner = KMeans(n_clusters=NUM_CLUSTERS)
	means = dict()
	for cat in data:
		learner.fit(data[cat])
		for i in range(NUM_CLUSTERS):
			means[int(cat*NUM_CLUSTERS + i)] = learner.cluster_centers_[i]

	return means

# datum is a single 784 item numpy array representing a trimmed digit image
# means is the dict mapping expanded categories to their means
# returns a list of predicted values for the given datum
def predict(data, means):
	predictions = list()
	for c in means:
		predictions.append(euclidean(data, means[c]))
	
	return predictions

def main():
	training = get_data(TRAIN)
	# train the learner and retrieve the means
	avgs = get_means(training)

# 	# save images to file as png
# 	for cat in avgs:
# 		arr = np.reshape(np.array(avgs[cat]), (28,28))
# 		arr = imresize(arr, 6.0)
# 		imsave('images/avg_v8_' + str(cat) + '.png', arr)

	# retrieve mean array for training data
	mean_dists = list()
	cats = list()
	for c in training:
		for d in training[c]:
			mean_dists.append(predict(d, avgs))
			cats.append(c)
	
	# Train a logistic regression classifier on means.
	learner = LogisticRegression(random_state=96, solver='newton-cg', n_jobs=-1)
	learner.fit(mean_dists, cats)

	# retrieve test data
	data = np.loadtxt(TEST, delimiter=',', skiprows=1)

	# retrieve mean array for test data
	mean_dists = list()
	for d in data:
		mean_dists.append(predict(d, avgs))
	
	output = learner.predict(mean_dists)

	np.savetxt('output.csv', output, fmt='%d', delimiter=',')


if __name__ == '__main__':
	main()



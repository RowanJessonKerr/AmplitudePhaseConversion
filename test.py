import numpy as np
import random
from matplotlib import pyplot as plt

dists = np.linspace(0,300, int(1e6))

bins = np.arange(250,300, 10)
removals = []

for i in range(len(bins) -1):
    filt = np.logical_and(dists > bins[i], dists <= bins[i+1])
    nums = np.count_nonzero(filt)

    reduceBy = len(dists) -  int (nums * ((300 - bins[i]) / 50))
    indices = np.nonzero(filt)[0] ## indices of trues
    minIndex = indices[0]
    maxIndex = indices[-1]
    print(reduceBy)

    for j in range(reduceBy):
        removalIndex = random.randrange(minIndex, maxIndex + 1)
        while (removalIndex in removals):
            removalIndex = random.randrange(minIndex, maxIndex + 1)

        removals.append(removalIndex)
        
np.delete(dists, removals)

plt.yticks([])

plt.scatter(dists, np.zeros([len(dists)]), s= 0.1)
plt.show()








# y = (300 - x) / 50
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
def saveHistogram(array,tiles,path):
    assert(isinstance(array,np.ndarray))
    assert(array.shape[1] == len(titles))

    for i in range(len(titles)):
        plt.clf()
        fig = plt.figure('fig')
        sns.displot(array[:,i],bins=20)
        plt.xlabel(titles[i])
        plt.savefig(os.path.join(path,titles[i]+'png'))

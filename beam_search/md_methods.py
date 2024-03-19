import numpy as np
import pandas as pd

def apply_cca(dataset=None, descriptives=None):

    datasetcca = dataset.copy()
    #print(datasetcca.shape)
    datasetcca.dropna(inplace=True)
    #print(datasetcca.shape)
    datasetcca.reset_index(inplace=True)

    return datasetcca
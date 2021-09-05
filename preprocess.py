import numpy as np
import pandas as pd

import read_hbsc_dnsssu_mpalc as rhdm

def preprocess(data_name=None, trend_name=None, remove_data=None):

    if data_name == 'HBSC_DNSSSU':
        if trend_name == 'MPALC':
            dataset, attributes, descriptives = rhdm.load_and_preprocess(trend_name=trend_name, 
                                                                         remove_data=remove_data)

    return dataset, attributes, descriptives



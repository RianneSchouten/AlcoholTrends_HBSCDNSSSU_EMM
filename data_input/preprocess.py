import numpy as np
import pandas as pd

import data_input.HBSC_DNSSSU.MPALC.read_hbsc_dnsssu_mpalc as rhdm

def preprocess(data_params=None):

    if data_params['data_name'] == 'HBSC_DNSSSU':
        if data_params['trend_name'] == 'MPALC':
            dataset, attributes, descriptives = rhdm.load_and_preprocess(data_params)

    return dataset, attributes, descriptives



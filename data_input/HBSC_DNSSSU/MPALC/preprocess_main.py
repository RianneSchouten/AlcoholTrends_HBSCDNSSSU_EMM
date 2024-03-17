import numpy as np
import pandas as pd


def main(data_params=None,prop=None):

    path_to_data = "C:/Users/20200059/Documents/Data/HBSC/Data/AlcoholTrends_HBSCDNSSSU_EMM/"
    name_dataset = path_to_data + 'PeilHBSC20032019_' + data_params['trend_name'] + '_incomplete.sav'
    dfinc = pd.read_spss(name_dataset)
    print(dfinc.head())

    # create the complete dataset
    name_dataset = path_to_data + 'PeilHBSC20032019_' + data_params['trend_name'] + '.sav'
    dfcom = pd.read_spss(name_dataset)
    print(dfcom.head())

    # based on prop
    # create a slice of the incomplete dataset

    # create a slice of the complete dataset

    # save both slices

if __name__ == '__main__':

    main(data_params={'trend_name':'MPALC'},
         prop=0.2)
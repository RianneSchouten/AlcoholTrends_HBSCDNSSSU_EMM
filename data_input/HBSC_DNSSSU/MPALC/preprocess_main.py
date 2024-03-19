import numpy as np
import pandas as pd
import random 
import pyreadstat

def main(data_params=None,prop=None):

    path_to_data = "C:/Users/20200059/Documents/Data/HBSC/Data/AlcoholTrends_HBSCDNSSSU_EMM/"
    name_dataset = path_to_data + 'PeilHBSC20032019_' + data_params['trend_name'] + '_incomplete.sav'
    dfinc = pd.read_spss(name_dataset)
    # remove all DNSSSU data
    dfinc_short = dfinc.loc[dfinc['meting'].isin([2005,2009,2013,2017])]

    # create the complete dataset
    name_dataset = path_to_data + 'PeilHBSC20032019_' + data_params['trend_name'] + '_complete.sav'
    dfcom = pd.read_spss(name_dataset)
    # remove all DNSSSU data
    dfcom_short = dfcom.loc[dfcom['meting'].isin([2005,2009,2013,2017])]

    # based on prop
    # create a slice of the incomplete dataset
    random.seed(2024)
    dfinc_short.reset_index(inplace=True,drop=True)
    idx = list(dfinc_short.index.values)
    sel_idx = random.sample(idx,k=int(np.round(prop*len(dfinc_short),0)))
    dfinc_slice = dfinc_short.iloc[sel_idx]
    dfinc_slice.reset_index(drop=True,inplace=True)

    # create a slice of the complete dataset
    random.seed(2024)
    dfcom_short.reset_index(inplace=True,drop=True)
    idx = list(dfcom_short.index.values)
    sel_idx = random.sample(idx,k=int(np.round(prop*len(dfcom_short),0)))
    dfcom_slice = dfcom_short.iloc[sel_idx]
    dfcom_slice.reset_index(drop=True,inplace=True)

    # save both slices
    pyreadstat.write_sav(dfinc_slice, 'slice/PeilHBSC20032019_MPALC_incomplete.sav') 
    pyreadstat.write_sav(dfcom_slice, 'slice/PeilHBSC20032019_MPALC_complete.sav')   

if __name__ == '__main__':

    main(data_params={'trend_name':'MPALC'}, prop=0.2)
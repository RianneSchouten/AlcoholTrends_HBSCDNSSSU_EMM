import numpy as np
import pandas as pd
import random 
import pyreadstat

def main(data_params=None,prop=None):

    path_to_data = "C:/Users/20200059/Documents/Data/HBSC/Data/AlcoholTrends_HBSCDNSSSU_EMM/"
    name_dataset = path_to_data + 'PeilHBSC20032019_' + data_params['trend_name'] + '_incomplete.sav'
    dfinc = pd.read_spss(name_dataset)

    # create the complete dataset
    name_dataset = path_to_data + 'PeilHBSC20032019_' + data_params['trend_name'] + '_complete.sav'
    dfcom = pd.read_spss(name_dataset)

    # based on prop
    # create a slice of the incomplete dataset
    random.seed(2024)
    idx = list(dfinc.index.values)
    sel_idx = random.sample(idx,k=int(np.round(prop*len(dfinc),0)))
    dfinc_slice = dfinc.iloc[sel_idx]
    dfinc_slice.reset_index(drop=True,inplace=True)

    # create a slice of the complete dataset
    random.seed(2024)
    idx = list(dfcom.index.values)
    sel_idx = random.sample(idx,k=int(np.round(prop*len(dfcom),0)))
    dfcom_slice = dfcom.iloc[sel_idx]
    dfcom_slice.reset_index(drop=True,inplace=True)

    # save both slices
    pyreadstat.write_sav(dfinc_slice, 'slice/PeilHBSC20032019_MPALC_incomplete.sav') 
    pyreadstat.write_sav(dfcom_slice, 'slice/PeilHBSC20032019_MPALC_complete.sav')   

if __name__ == '__main__':

    main(data_params={'trend_name':'MPALC'}, prop=0.2)
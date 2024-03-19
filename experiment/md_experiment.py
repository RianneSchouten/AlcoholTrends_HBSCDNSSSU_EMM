import numpy as np
import pandas as pd
import itertools as it
import random
from pyampute.ampute import MultivariateAmputation

import beam_search.beam_search as bs

def run_md_experiment(result_emm=None, md_params=None,
                      dataset=None, attributes=None, descriptives=None, model_params=None, 
                      beam_search_params=None, wcs_params=None, constraints=None):

    # set up storage of results
    coll_result_emm = result_emm.iloc[0:2]
    coll_result_emm.reset_index(drop=False,inplace=True)
    info = pd.DataFrame({'md':[None,None,None],'prop':[0,0,0],'mech':[None,None,None]})
    coll_result_emm = pd.concat([coll_result_emm, info], axis=1)
    print(coll_result_emm)

    # prepare all parameter combinations
    paramset = list(it.product(md_params['md'], md_params['prop'], md_params['mech']))
    for params in paramset: 
        print(params)

        # make dataset incomplete
        df_inc = generate_missing_data(df=dataset, params=params, md_params=md_params)

        # perform beam search with md approach
        beam_search_params['q'] = 1
        result_emm_temp, general_params, considered_subgroups = bs.beam_search(dataset=df_inc, md_method=params[0],
                                                                          attributes=attributes, descriptives=descriptives, 
                                                                          model_params=model_params, beam_search_params=beam_search_params, 
                                                                          wcs_params=wcs_params, constraints=constraints)
    
        # store result, update result_emm with all findings
        coll_result_emm = evaluate_result(coll_result_emm=coll_result_emm, result_emm_temp=result_emm_temp, params=params)

    return coll_result_emm

def generate_missing_data(df=None, params=None, md_params=None):

    print(df.isnull().sum()) 
    df_inc = df.copy()

    prop = params[1]
    mech = params[2]

    if mech == 'mcar':
        df_inc = generate_mcar(df=df, prop=prop, dep_var=md_params['dep_var'])
    if mech == 'mar':
        df_inc = generate_mar(df=df, prop=prop, dep_var=md_params['dep_var'], indep_var=md_params['indep_var'])
    #if mech == 'mnar':
    #    df_inc = generate_mnar()

    print(df_inc.isnull().sum()) 

    return df_inc

def generate_mcar(df=None, prop=None, dep_var=None):

    idx = list(df.index.values)
    sel_idx = random.sample(idx,k=int(np.round(prop*len(df),0)))
    
    df_inc = df.copy()
    df_inc.loc[sel_idx, dep_var] = np.nan

    return df_inc

def generate_mar(df=None, prop=None, dep_var=None, indep_var=None):

    pred = indep_var[0]
    print(pred)
    print(df[pred].values)
    print(df.dtypes)

    df_inc = df.copy()

    return df_inc

def evaluate_result(coll_result_emm=None, result_emm_temp=None, params=None):

    print(coll_result_emm)    
    
    result_emm_temp.reset_index(drop=False,inplace=True)
    info = pd.DataFrame({'md':[params[0]]*3,'prop':[params[1]]*3,'mech':[params[2]]*3})
    result_emm_temp_info = pd.concat([result_emm_temp, info], axis=1)
    print(result_emm_temp_info)
    
    coll_result_emm_added = pd.concat([coll_result_emm, result_emm_temp_info], ignore_index=True)
    
    print(coll_result_emm_added)

    return coll_result_emm_added
import numpy as np
import pandas as pd

import data_input.preprocess as pp
import beam_search.beam_search as bs
import beam_search.distribution_false_discoveries as dfd
import evaluation.analyze_subgroups as asub

def analysis(data_params=None, model_params=None, beam_search_params=None, 
             constraints=None, dfd_params=None, wcs_params=None):

    dataset, attributes, descriptives = pp.preprocess(data_params=data_params)
    print(descriptives)
    print(attributes)
    #print(dataset.dtypes)
    print(dataset.shape)
    print(dataset.head())

    # check if distribution has to be made
    if dfd_params['make']:
        # build dfd, as a pd.DataFrame where the quality values are a list, and other values are distribution params
        distribution_params = dfd.distribution_false_discoveries_params(m=dfd_params['m'], model_params=model_params,
                                                                        beam_search_params=beam_search_params,
                                                                        dataset=dataset, attributes=attributes, descriptives=descriptives, 
                                                                        wcs_params=wcs_params, constraints=constraints)

    else:
        distribution_params = None               

    # a single run
    result_emm, general_params, considered_subgroups = bs.beam_search(dataset=dataset, attributes=attributes, descriptives=descriptives, 
                                                                      model_params=model_params, beam_search_params=beam_search_params, 
                                                                      wcs_params=wcs_params, constraints=constraints)

    #print(result_emm)
    #print(considered_subgroups)

    if model_params['trend_var'] == 'prev':
        analyze_var = 'prev'
    else: 
        analyze_var = 'mov_prev'

    sgs, jsmatrix = asub.analyze_subgroups(dataset=dataset, attributes=attributes, descriptives=descriptives, 
                                           result_emm=result_emm, general_params=general_params, 
                                           beam_search_params=beam_search_params, model_params=model_params,
                                           analyze_var=analyze_var)

    return result_emm, general_params, considered_subgroups, distribution_params, sgs, jsmatrix
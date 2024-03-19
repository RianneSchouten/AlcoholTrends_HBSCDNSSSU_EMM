import numpy as np
import pandas as pd
import os

import data_input.preprocess as pp
import beam_search.beam_search as bs
import beam_search.distribution_false_discoveries as dfd
import evaluation.analyze_subgroups as asub
import experiment.md_experiment as md
import experiment.save_and_store as ss

def md_analysis(data_params=None, model_params=None, beam_search_params=None, 
                constraints=None, dfd_params=None, wcs_params=None, md_params=None,
                output_to_path=None, file_name=None, all_params=None):

    md_methods = beam_search_params['md']
    for method in md_methods:
        print(method)
        result_emm, general_params, considered_subgroups, distribution_params, sgs, jsmatrix = analysis(data_params=data_params, md_method=method,
                                                                                                        model_params=model_params, beam_search_params=beam_search_params,       
                                                                                                        constraints=constraints, dfd_params=dfd_params, wcs_params=wcs_params)
        
        all_params['md'] = method
        output_to_path_extended = output_to_path + '/' + method + '/'
        if not os.path.exists(output_to_path_extended):
            os.makedirs(output_to_path_extended)
        ss.save_one_emm_result(result_emm=result_emm, general_params=general_params, considered_subgroups=considered_subgroups, 
                               distribution_params=distribution_params, sgs=sgs, jsmatrix=jsmatrix, output_to_path=output_to_path_extended, 
                               file_name=file_name, all_params=all_params)

def analysis(data_params=None, md_method=None, model_params=None, beam_search_params=None, 
             constraints=None, dfd_params=None, wcs_params=None, md_params=None):

    dataset, attributes, descriptives = pp.preprocess(data_params=data_params)
    #print(descriptives)
    #print(attributes)
    #print(dataset.dtypes)
    print(dataset.shape)
    #print(dataset.head())

    # a single run
    #
    result_emm, general_params, considered_subgroups = bs.beam_search(dataset=dataset, md_method=md_method, attributes=attributes, descriptives=descriptives, 
                                                                      model_params=model_params, beam_search_params=beam_search_params, 
                                                                      wcs_params=wcs_params, constraints=constraints)

    # check if distribution has to be made
    if dfd_params['make']:
        # build dfd, as a pd.DataFrame where the quality values are a list, and other values are distribution params
        distribution_params = dfd.distribution_false_discoveries_params(m=dfd_params['m'], model_params=model_params,
                                                                        beam_search_params=beam_search_params, md_method=md_method,
                                                                        dataset=dataset, attributes=attributes, descriptives=descriptives, 
                                                                        wcs_params=wcs_params, constraints=constraints)

    else:
        distribution_params = None   

    if model_params['trend_var'] == 'prev':
        analyze_var = 'prev'
    else: 
       analyze_var = 'mov_prev'            

    if 'evaluate_jsim' in wcs_params.keys():
        if wcs_params['evaluate_jsim']:
            sgs, jsmatrix = asub.analyze_subgroups(dataset=dataset, md_method=md_method, attributes=attributes, descriptives=descriptives, 
                                           result_emm=result_emm, general_params=general_params, 
                                           beam_search_params=beam_search_params, model_params=model_params,
                                           analyze_var=analyze_var)
        else:
            sgs = pd.DataFrame()
            jsmatrix = pd.DataFrame()
    else:
        sgs, jsmatrix = asub.analyze_subgroups(dataset=dataset, md_method=md_method, attributes=attributes, descriptives=descriptives, 
                                           result_emm=result_emm, general_params=general_params, 
                                           beam_search_params=beam_search_params, model_params=model_params,
                                           analyze_var=analyze_var)

    if md_params is not None:
        if 'run_experiment'in md_params.keys():
            if md_params['run_experiment']:
                result_emm = md.run_md_experiment(result_emm=result_emm, md_params=md_params,
                                          dataset=dataset, attributes=attributes, descriptives=descriptives, 
                                          model_params=model_params, beam_search_params=beam_search_params, 
                                          wcs_params=wcs_params, constraints=constraints)

    return result_emm, general_params, considered_subgroups, distribution_params, sgs, jsmatrix
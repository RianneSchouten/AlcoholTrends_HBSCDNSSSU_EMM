import numpy as np
import pandas as pd
import os

import experiment.analysis as an
import experiment.save_and_store as ss

def main(data_params=None, 
         beam_search_params=None, model_params=None,
         constraints=None, wcs_params=None,
         dfd_params=None, date=None,
         output_to=None):
    
    # create path and empty output file 
    output_to_path = output_to + data_params['data_name'] + '/' + data_params['trend_name'] + '/' + 'date' + str(date) + '/'
    if not os.path.exists(output_to_path):
        os.makedirs(output_to_path)  
    file_name = model_params['trend_var'] + '_' + model_params['qm']

    all_params = {**data_params, **beam_search_params, **dfd_params, **wcs_params, **model_params, **{'date':date}}
    print(all_params)

    # result_analysis is a df
    if 'md' in beam_search_params.keys():
        # apply md to bs        
        an.md_analysis(data_params=data_params, model_params=model_params,beam_search_params=beam_search_params, 
                       constraints=constraints, dfd_params=dfd_params, wcs_params=wcs_params, 
                       output_to_path=output_to_path, file_name=file_name, all_params=all_params)
    else:
        result_emm, general_params, considered_subgroups, distribution_params, sgs, jsmatrix = an.analysis(data_params=data_params,
                                                                                        model_params=model_params,
                                                                                        beam_search_params=beam_search_params, 
                                                                                        constraints=constraints,
                                                                                        dfd_params=dfd_params, 
                                                                                        wcs_params=wcs_params)
        ss.save_one_emm_result(result_emm=result_emm, general_params=general_params, considered_subgroups=considered_subgroups, 
                               distribution_params=distribution_params, sgs=sgs, jsmatrix=jsmatrix, output_to_path=output_to_path, 
                               file_name=file_name, all_params=all_params)
  

if __name__ == '__main__':

    # current options for trend_var: prev, prev_slope, mov_prev, mov_prev_slope, mean, ratio
    # current options for hypothesis: data, value
    # current options for value: any value in combination with hypothesis: value
    # current options for use_se (if hypothesis = value): True, False, 'multiply'
    # current options for qm: max, count, average, sum, min, countsum
    # current options for threshold: any value (<) in combination with qm: count

    '''    
    main(data_params = {'data_name':'HBSC_DNSSSU', 'trend_name':'MPALC', 
                        'remove_data':False, 'incomplete':True, 'take_slice':False}, 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 
                         'qm': 'max', 'threshold': None, 'order': 'max', 'round': 1},
         constraints = {'min_size': 0.05, 'min_occassions': 1.0},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, 
         date=17032024, 
         output_to='./data_output/')

    main(data_params = {'data_name':'HBSC_DNSSSU', 'trend_name':'MPALC', 
                        'remove_data':False, 'incomplete':True, 'take_slice':False},  
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20},
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'data', 'value': None, 'use_se': None, 
                         'qm': 'max', 'threshold': None, 'order': 'max', 'round': 1},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, 
         date=18032024, 
         output_to='./data_output/')

    main(data_params = {'data_name':'HBSC_DNSSSU', 'trend_name':'MPALC', 
                        'remove_data':False, 'incomplete':True, 'take_slice':False},  
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'value', 'value': 0.0, 'use_se': False, 
                         'qm': 'countsum', 'threshold': 0.01, 'order': 'max', 'round': 4}, # change threshold to 0.005 or 0.02
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, 
         date=19032024, 
         output_to='./data_output/')  
    '''
    '''
    # experiments with various md approaches
    main(data_params = {'data_name':'HBSC_DNSSSU', 'trend_name':'MPALC', 
                        'remove_data':False, 'incomplete':True, 'take_slice':False}, 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 10, 'md':['cca','ignore','ignore_and_allow','ignore_allow_and_both']}, 
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 
                         'qm': 'max', 'threshold': None, 'order': 'max', 'round': 1},
         constraints = {'min_size': 0.05, 'min_occassions': 1.0},
         dfd_params = {'make': True, 'm': 10},
         md_params = {'run_experiment': False},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80, 'evaluate_jsim': True}, 
         date=20032024, 
         output_to='./data_output/')
    
    main(data_params = {'data_name':'HBSC_DNSSSU', 'trend_name':'MPALC', 
                        'remove_data':False, 'incomplete':True, 'take_slice':False}, 
         beam_search_params = {'b': 8, 'w': 60, 'd': 3, 'q': 20, 'md':['ignore_allow_and_both']}, 
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 
                         'qm': 'max', 'threshold': None, 'order': 'max', 'round': 1},
         constraints = {'min_size': 0.05, 'min_occassions': 1.0},
         dfd_params = {'make': False, 'm': 10},
         md_params = {'run_experiment': False},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80, 'evaluate_jsim': False}, 
         date=21032024, 
         output_to='./data_output/')
    '''

    
import numpy as np
import pandas as pd
import os

import experiment.analysis as an

def main(data_params=None, qm=None, 
         beam_search_params=None, model_params=None,
         constraints=None, wcs_params=None,
         dfd_params=None, date=None,
         output_to=None):
    
    # create path and empty output file 
    output_to_path = output_to + data_params['data_name'] + '/' + data_params['trend_name'] + '/' + 'date' + str(date) + '/'
    if not os.path.exists(output_to_path):
        os.makedirs(output_to_path)  
    file_name = output_to_path + model_params['trend_var'] + '_' + model_params['qm']
    #excel_file_name, sheet_names = ssr.create_empty_output_file(output_to_path=output_to_path)

    # location of dfd
    #data_output_location = save_location + data_name + '/' + trend_name + '/' + str(date) + '_' + str(qm) + '_' + \
    #    str(list(beam_search_params.values())) + '_' + str(list(constraints.values())) + '_' + \
    #        str(list(dfd_params.values())) + '_' + str(list(wcs_params.values())) + '_' + \
    #            str(list(model_params.values())) + '.xlsx'

    # result_analysis is a df
    result_emm, general_params, considered_subgroups, distribution_params, sgs, jsmatrix = an.analysis(data_params=data_params,
                                                                                        model_params=model_params,
                                                                                        beam_search_params=beam_search_params, 
                                                                                        constraints=constraints,
                                                                                        dfd_params=dfd_params, 
                                                                                        wcs_params=wcs_params)

    #print(result_emm)
    #print(general_params)
    #print(considered_subgroups)
    #print(distribution_params)

    # save   
    subgroup_numbers = result_emm.sg.unique()
    for j in subgroup_numbers:
        sg = result_emm.loc[result_emm.sg == j, ]
        params = sg.iloc[2].params 
        params.reset_index(inplace=True,names=['meting'])
        params.to_csv(file_name + '_' + str(j) + '.txt', sep='\t', index=False)

    beam_search_params.update(dfd_params)
    beam_search_params.update(constraints)
    beam_search_params.update(wcs_params)
    beam_search_params.update(model_params)
    beam_search_params.update({'date': date})
    analysis_info = pd.DataFrame(beam_search_params, index=[0])
    general_params_pd = general_params['params']
    
    dfs = {'result_emm': result_emm, 'analysis_info': analysis_info, 
           'considered_subgroups': pd.DataFrame(considered_subgroups), 
           'general_params_pd': general_params_pd, 
           'distribution_params': pd.DataFrame(distribution_params),
           'sgs':sgs, 'jsmatrix':jsmatrix}
    
    writer = pd.ExcelWriter(file_name + '.xlsx', engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)
    writer.close()    

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

    # with sliced data
    main(data_params = {'data_name':'HBSC_DNSSSU', 'trend_name':'MPALC', 
                        'remove_data':False, 'incomplete':False, 'take_slice':True}, 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 
                         'qm': 'max', 'threshold': None, 'order': 'max', 'round': 1},
         constraints = {'min_size': 0.05, 'min_occassions': 1.0},
         dfd_params = {'make': False, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, 
         date=20032024, 
         output_to='./data_output/')
    

    
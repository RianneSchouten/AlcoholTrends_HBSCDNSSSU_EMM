import numpy as np
import pandas as pd

import analysis as an

def main(data_name=None, trend_name=None, 
         remove_data=None, incomplete=None, qm=None, 
         beam_search_params=None, model_params=None,
         constraints=None, wcs_params=None,
         dfd_params=None, date=None,
         save_location=None):

    # location of dfd
    data_output_location = save_location + data_name + '/' + trend_name + '/' + str(date) + '_' + str(qm) + '_' + \
        str(list(beam_search_params.values())) + '_' + str(list(constraints.values())) + '_' + \
            str(list(dfd_params.values())) + '_' + str(list(wcs_params.values())) + '_' + \
                str(list(model_params.values())) + '.xlsx'

    # result_analysis is a df
    print(beam_search_params)
    result_emm, general_params, considered_subgroups, distribution_params = an.analysis(data_name=data_name,
                                                                                        trend_name=trend_name,
                                                                                        remove_data=remove_data,
                                                                                        incomplete=incomplete,
                                                                                        model_params=model_params,
                                                                                        beam_search_params=beam_search_params, 
                                                                                        constraints=constraints,
                                                                                        dfd_params=dfd_params, 
                                                                                        wcs_params=wcs_params)

    print(result_emm)
    print(general_params)
    print(considered_subgroups)

    # save        
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
           'distribution_params': pd.DataFrame(distribution_params)}
    
    writer = pd.ExcelWriter(data_output_location, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)
    writer.save()    

if __name__ == '__main__':

    # current options for trend_var: prev, prev_slope, mov_prev, mov_prev_slope, mean, ratio
    # current options for hypothesis: data, value
    # current options for value: any value in combination with hypothesis: value
    # current options for use_se (if hypothesis = value): True, False, 'multiply'
    # current options for qm: max, count, average, sum, min, countsum
    # current options for threshold: any value (<) in combination with qm: count

    #### HBSC and DNSSSU
    # Adapted runs dec 2021
    # With incomplete, non-split dataset 
    # exceptionality type 1
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', remove_data=False, incomplete=True, 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 
                         'qm': 'max', 'threshold': None, 'order': 'max', 'round': 1},
         constraints = {'min_size': 0.05, 'min_occassions': 1.0},
         dfd_params = {'make': True, 'm': 10},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, 
         date=20211214, 
         save_location='./data_output/')

    # exceptionality type 2    
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', remove_data=False, incomplete=True, 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20},
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'data', 'value': None, 'use_se': None, 
                         'qm': 'max', 'threshold': None, 'order': 'max', 'round': 1},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': True, 'm': 10},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, 
         date=20211215, 
         save_location='./data_output/')

    # exceptionality type 3
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', remove_data=False, incomplete=True, 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'value', 'value': 0.0, 'use_se': False, 
                         'qm': 'countsum', 'threshold': 0.01, 'order': 'max', 'round': 4}, # change threshold to 0.005 or 0.02
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, 
         date=20211221, 
         save_location='./data_output/')  

    # Adapted runs aug 2021
    # Variable school year is removed
    # children <12 and >16 are removed
    '''
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', remove_data=True,
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 
                         'qm': 'max', 'threshold': None, 'order': 'max', 'round': 1},
         constraints = {'min_size': 0.05, 'min_occassions': 1.0},
         dfd_params = {'make': True, 'm': 10},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210817, 
         save_location='./data_output/')
    
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', remove_data=True,
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20},
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'data', 'value': None, 'use_se': None, 
                         'qm': 'max', 'threshold': None, 'order': 'max', 'round': 1},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': True, 'm': 10},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, 
         date=20211021, 
         save_location='./data_output/')
 
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', remove_data=True,
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'value', 'value': 0.0, 'use_se': False, 
                         'qm': 'count', 'threshold': 0.01, 'order': 'max', 'round': 1},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': True, 'm': 10},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20211021, 
         save_location='./data_output/')
    '''
    '''
    # Original runs may/june 2021
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, # 20 descriptive attributes
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 1.0},
         dfd_params = {'make': False, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210605, 
         save_location='./data_output/')

    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20},
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': False, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210605, 
         save_location='./data_output/')

    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'value', 'value': 0.0, 'use_se': False, 'qm': 'count', 'threshold': 0.01, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': False, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210605, 
         save_location='./data_output/')
    '''
    

    
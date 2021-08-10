import numpy as np
import pandas as pd

import analysis as an

def main(data_input=None, qm=None, 
         beam_search_params=None, 
         constraints=None, wcs_params=None,
         dfd_params=None, date=None,
         save_location=None):

    # location of dfd
    data_output_location = save_location + data_input + '/' + data_input + '_' + str(qm) + '_' + \
        str(list(beam_search_params.values())) + '_' + str(list(constraints.values())) + '_' + \
            str(list(wcs_params.values())) + '.xlsx'

    # result_analysis is a df
    print(beam_search_params)
    result_emm, general_params, considered_subgroups, distribution_params = an.analysis(data_input=data_input,
                                                                                        qm=qm, 
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
    beam_search_params.update({'date': date})
    analysis_info = pd.DataFrame(beam_search_params, index=[0])
    general_params_pd = general_params['params']
    dfs = {'result_emm': result_emm, 'analysis_info': analysis_info, 
           'considered_subgroups': pd.DataFrame(considered_subgroups), 
           'general_params_pd': general_params_pd, 
           'distribution_params': pd.DataFrame(distribution_params)}
    
    writer = pd.ExcelWriter(data_output_location, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()    

if __name__ == '__main__':

    main(data_input='MPALC_70',
         qm=['nr_mean_zero'],
         #qm=['max_prev_slope'],
         #qm=['max_prev'],
         #qm=['max_prev_slope', 'max_prev'],
         #qm=['nr_mean_zero', 'max_prev_slope', 'max_prev'],
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, # first level gives 80 subgroups, we keep 1/2 = 40
         constraints = {'min_size': 0.05},
         dfd_params = {'make': True, 'm': 100}, 
         wcs_params = {'gamma': 0.9, 'stop_number_description_selection': 80}, # two times the beam width
         date=20210511, 
         save_location='./data_output/')


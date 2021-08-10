import numpy as np
import pandas as pd

import preprocess as pp
import collect_qualities as qu
import select_subgroup as ss

def import_subgroup_from_resultlist(outcome_attr=None, file_name=None, subgroup_numbers=None):

    dataset, attributes, descriptives = pp.preprocess(data_input=outcome_attr)
    result_emm, analysis_info, considered_subgroups, general_params_pd = load_result_emm(file_name=outcome_attr + '/' + file_name + '.xlsx')
    data_size = np.sum(general_params_pd['n'].values) 
    #print(result_emm)

    sgn = subgroup_numbers[0]
        
    sg = result_emm.loc[result_emm.sg == sgn, ]
    desc_series = sg.iloc[0, ].dropna().drop(['sg'])
    desc_dict = desc_series.apply(eval).to_dict()

    subgroup, idx, subgroup_compl, idx2 = ss.select_subgroup(description=desc_dict, df=dataset, descriptives=descriptives)
    subgroup_params, is_replaced = qu.calculate_subgroup_parameters(subgroup=subgroup, attributes=attributes)
    params = subgroup_params['params']
    params['size'] = np.repeat(subgroup_params['sg_size'] / data_size,9)
    all_params = params

    if len(subgroup_numbers) > 1:        
        for sgn in subgroup_numbers[1:]:

            #print(sgn)

            sg = result_emm.loc[result_emm.sg == sgn, ]
            desc_series = sg.iloc[0, ].dropna().drop(['sg'])
            desc_dict = desc_series.apply(eval).to_dict()

            subgroup, idx, subgroup_compl, idx2 = ss.select_subgroup(description=desc_dict, df=dataset, descriptives=descriptives)
            subgroup_params_more, is_replaced = qu.calculate_subgroup_parameters(subgroup=subgroup, attributes=attributes)
            params = subgroup_params_more['params']
            params['size'] = np.repeat(subgroup_params_more['sg_size'] / data_size, 9)
            all_params = all_params.append(params)

    all_params['subgroup'] = np.repeat(subgroup_numbers, 9)
    #location = 'C:/Users/20200059/Documents/Github/analysis_alcoholtrends_emm_hbscpeil/data_output/' + outcome_attr + '/' + file_name + '_subgroup_params_' + str(subgroup_numbers) + '.xlsx'
    #all_params.to_excel(location, index=False)

    return general_params_pd, all_params

def load_result_emm(file_name=None):

    location = 'C:/Users/20200059/Documents/Github/analysis_alcoholtrends_emm_hbscpeil/data_output/' + file_name
    sheets = pd.read_excel(location, sheet_name=['result_emm', 'analysis_info', 'considered_subgroups', 'general_params_pd'])

    result_emm = sheets['result_emm']
    analysis_info = sheets['analysis_info']
    considered_subgroups = sheets['considered_subgroups']
    general_params_pd = sheets['general_params_pd']

    return result_emm, analysis_info, considered_subgroups, general_params_pd

'''
general_params_pd, all_params = import_subgroup_from_resultlist(outcome_attr="MPALC",
                                                                file_name="MPALC_['max_slope']_[8, 25, 3, 15, 0.05, False, 3, None, None]_[None, None]_20210428", 
                                                                subgroup_numbers=np.arange(14))
'''


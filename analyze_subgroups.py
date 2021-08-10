import numpy as np
import pandas as pd

import preprocess as pp
import collect_qualities as qu
import select_subgroup as ss
import import_subgroup as iss

def analyze_subgroups(data_name=None, trend_name=None, file_name=None, remove_data=None,
                      subgroup_numbers=None, beam_search_params=None):

    dataset, attributes, descriptives = pp.preprocess(data_name=data_name, trend_name=trend_name, remove_data=remove_data)
    result_emm, analysis_info, considered_subgroups, general_params_pd, distribution_params = \
            iss.load_result_emm(file_name=data_name + '/' + trend_name + '/' + file_name + '.xlsx')
    data_size = np.sum(general_params_pd['n'].values) 

    result_emm = result_emm.iloc[:,1:]
    general_params_params = general_params_pd.set_index(attributes['time_attribute'])

    sgn = subgroup_numbers[0]        
    sg = result_emm.loc[result_emm.sg == sgn, ]
    desc_series = sg.iloc[0,].dropna().drop(['sg'])
    desc_dict = desc_series.apply(eval).to_dict()
    emm_series = sg.iloc[1,]
    
    model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'}
    general_params = {'params': general_params_params, 'data_size': data_size}

    description = []
    cov = []
    qv = []

    print(desc_dict)
    keys = list(desc_dict.keys())
    dict_new = {}
    for key in keys:
        print(key)
        dict_new[key] = desc_dict[key]
        print(dict_new)
        subgroup, idx, subgroup_compl, idx2 = ss.select_subgroup(description=dict_new, df=dataset, descriptives=descriptives)
        subgroup_params = qu.calculate_first_part_subgroup_parameters(subgroup=subgroup, attributes=attributes, 
                                                                      model_params=model_params, general_params=general_params)
        subgroup_params = qu.calculate_second_part_subgroup_parameters(subgroup_params=subgroup_params, subgroup=subgroup, 
                                                                       attributes=attributes, model_params=model_params)                                    

        description.append(dict_new.copy())
        print(description)
        cov.append(subgroup_params['sg_size']/data_size)

        desc_qm = qu.add_qm(desc=dict_new, general_params=general_params, subgroup_params=subgroup_params, 
                            model_params=model_params, beam_search_params=beam_search_params)            
        qm_value = desc_qm['qualities']['qm_value']
        qv.append(qm_value)

    result = pd.DataFrame({'description': description, 'cov': cov, 'qv': qv})  
    result.to_csv('data_output/' + data_name + '/' + trend_name + '/' + 'insp_desc_' + file_name + '.csv')                    
    
    return result

result = analyze_subgroups(data_name = "HBSC_DNSSSU",
                           trend_name = "MPALC",
                           file_name = "20210810_None_[8, 40, 3, 20]_[0.05, 1.0]_[False, 100]_[0.9, 80]_['prev', 'data', None, None, 'max', None, 'max']",
                           remove_data = True,
                           subgroup_numbers=[0],
                           beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20})

print(result)
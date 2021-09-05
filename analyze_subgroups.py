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
    model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 
                    'qm': 'max', 'threshold': None, 'order': 'max', 'round': 1}
    general_params = {'params': general_params_params, 'data_size': data_size}

    js = {}
    for sgn in subgroup_numbers:

        #print(sgn)

        sg = result_emm.loc[result_emm.sg == sgn, ]
        desc_series = sg.iloc[0,].dropna().drop(['sg'])
        desc_dict = desc_series.apply(eval).to_dict()
        qv_series = sg.iloc[2,]
        lorder = eval(sg.iloc[1,].loc['literal_order'])
        #print(lorder)  

        description = []
        cov = []
        qv = []
        covch = []
        qvimpr = []

        #print(desc_dict)
        keys = list(desc_dict.keys())
        dict_new = {}
        i = 0
        for key in lorder:

            #print(key)
            dict_new[key] = desc_dict[key]

            subgroup, idx, subgroup_compl, idx2 = ss.select_subgroup(description=dict_new, df=dataset, descriptives=descriptives)
            subgroup_params = qu.calculate_first_part_subgroup_parameters(subgroup=subgroup, attributes=attributes, 
                                                                      model_params=model_params, general_params=general_params)
            subgroup_params = qu.calculate_second_part_subgroup_parameters(subgroup_params=subgroup_params, subgroup=subgroup, 
                                                                       attributes=attributes, model_params=model_params)                                    

            description.append(dict_new.copy())
            cov.append(subgroup_params['sg_size']/data_size)

            desc_qm = qu.add_qm(desc=dict_new, general_params=general_params, subgroup_params=subgroup_params, 
                            model_params=model_params, beam_search_params=beam_search_params)            
            qm_value = desc_qm['qualities']['qm_value']
            qv.append(qm_value)

            if i > 0:
                covch.append((cov[i-1]-cov[i])/cov[i-1])
                qvimpr.append((qv[i]-qv[i-1])/qv[i-1])
            else:
                covch.append((1-cov[i])/1)
                qvimpr.append(np.nan)

            if i == (len(lorder)-1):
                # save idx
                js[str(dict_new)] = idx

            i += 1    

        res = pd.DataFrame({'sg': list(np.repeat(sgn,len(lorder))),
                                   'description': description, 
                                   'cov': cov, 'qv': qv, 
                                   'covch': covch, 'qvimpr': qvimpr})

        if sgn == 0:
            result = res
        else:
            result = result.append(res, ignore_index=True)     

    jsmatrix = calculate_jaccard_similarity(js=js)     
    dfs = {'sgs': result, 'jsmatrix': jsmatrix}

    writer = pd.ExcelWriter('data_output/' + data_name + '/' + trend_name + '/' + 'insp_desc_' + file_name + '.xlsx', engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)
    writer.save()  

    #result.to_csv('data_output/' + data_name + '/' + trend_name + '/' + 'insp_desc_' + file_name + '.csv')                    
    
    return result

def calculate_jaccard_similarity(js=None):

    ds = {}
    keys = list(js.keys())
    for key in keys:
        #print(key)
        ds[key] = {}        
        for other_key in keys:
            idx1 = js[key]
            idx2 = js[other_key]

            # overlap idx
            len_cap = len(np.intersect1d(idx1, idx2))
            # difference idx
            len_cup = len(np.union1d(idx1, idx2))
            # jaccard similarity
            value = len_cap / len_cup
            ds[key][other_key] = value
        
    jsmatrix = pd.DataFrame(ds)

    return jsmatrix

result = analyze_subgroups(data_name = "HBSC_DNSSSU",
                           trend_name = "MPALC",
                           file_name = "20210817_None_[8, 40, 3, 20]_[0.05, 1.0]_[True, 10]_[0.9, 80]_['prev', 'data', None, None, 'max', None, 'max', 1]",
                           remove_data = True,
                           subgroup_numbers=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
                           beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20})

print(result)
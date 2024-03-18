import numpy as np
import pandas as pd

import beam_search.collect_qualities as qu
import beam_search.select_subgroup as ss

def analyze_subgroups(dataset=None, attributes=None, descriptives=None, 
                      result_emm=None, general_params=None, 
                      subgroup_numbers=None, beam_search_params=None, model_params=None,analyze_var=None):

    #dataset, attributes, descriptives = pp.preprocess(data_name=data_name, trend_name=trend_name, remove_data=remove_data, incomplete=incomplete)
    #result_emm, analysis_info, considered_subgroups, general_params_pd, distribution_params = \
    #        iss.load_result_emm(file_name=data_name + '/' + trend_name + '/' + file_name + '.xlsx')
    
    data_size = general_params['data_size']
    #result_emm = result_emm.iloc[:,1:]
    paramspd = general_params['params']
    subgroup_numbers = result_emm.sg.unique()

    js = {}
    for sgn in subgroup_numbers:

        sg = result_emm.loc[result_emm.sg == sgn, ]
        desc_series = sg.iloc[0,].dropna().drop(['sg'])
        desc_dict = desc_series.to_dict()
        qv_series = sg.iloc[2,]
        #lorder = eval(sg.iloc[1,].loc['literal_order'])
        lorder = sg.iloc[1,].loc['literal_order']

        description = []
        size = []
        cov = []
        qv = []
        covch = []
        qvimpr = []

        #print(desc_dict)
        keys = list(desc_dict.keys())
        dict_new = {}
        i = 0
        for key in lorder:

            if key == 'dom_pruning':
                dict_new = desc_dict
            else:
                dict_new[key] = desc_dict[key]

            subgroup, idx, subgroup_compl, idx2 = ss.select_subgroup(description=dict_new, df=dataset, descriptives=descriptives)
            subgroup_params = qu.calculate_first_part_subgroup_parameters(subgroup=subgroup, attributes=attributes, 
                                                                      model_params=model_params, general_params=general_params)
            subgroup_params = qu.calculate_second_part_subgroup_parameters(subgroup_params=subgroup_params, subgroup=subgroup, 
                                                                       attributes=attributes, model_params=model_params)                                    

            description.append(dict_new.copy())
            size.append(subgroup_params['sg_size'])
            cov.append(subgroup_params['sg_size']/data_size)

            desc_qm = qu.add_qm(desc=dict_new, general_params=general_params, subgroup_params=subgroup_params, 
                            model_params=model_params, beam_search_params=beam_search_params)            
            #print(desc_qm['qualities']['params'])
            paramspd['condition' + str(sgn+1) + str(i+1)] = \
                desc_qm['qualities']['params'][analyze_var]
            
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
                                   'size': size,
                                   'cov': cov, 'qv': qv, 
                                   'covch': covch, 'qvimpr': qvimpr})

        if sgn == 0:
            result = res
        else:
            result = pd.concat([result, res], ignore_index=True)
            #result = result.append(res, ignore_index=True)     

    jsmatrix = calculate_jaccard_similarity(js=js)     
    sgs_result = result                 
    
    return sgs_result, jsmatrix

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


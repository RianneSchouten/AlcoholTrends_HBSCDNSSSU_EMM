import numpy as np
import pandas as pd
       
def save_one_emm_result(result_emm=None, general_params=None, considered_subgroups=None, distribution_params=None, 
                        sgs=None, jsmatrix=None, 
                        output_to_path=None, file_name=None, all_params=None):

    if 'run_experiment' in all_params.keys():
            save_subgroup_params(result_emm=None, file_name=output_to_path + file_name)
    else:
        save_subgroup_params(result_emm=result_emm, file_name=output_to_path + file_name)
    
    dfs = {'result_emm': result_emm, 'analysis_info': pd.DataFrame(all_params, index=[0]), 
           'considered_subgroups': pd.DataFrame(considered_subgroups), 
           'general_params_pd': general_params['params'], 
           'distribution_params': pd.DataFrame(distribution_params),
           'sgs':sgs, 'jsmatrix':jsmatrix}
    
    writer = pd.ExcelWriter(output_to_path + file_name + '.xlsx', engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)
    writer.close()    

def save_subgroup_params(result_emm=None, file_name=None):

    subgroup_numbers = result_emm.sg.unique()
    for j in subgroup_numbers:
        sg = result_emm.loc[result_emm.sg == j, ]
        params = sg.iloc[2].params 
        params.reset_index(inplace=True,names=['meting'])
        params.to_csv(file_name + '_' + str(j) + '.txt', sep='\t', index=False)
    
    return True
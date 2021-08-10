import numpy as np

import parameters as pa
import measures as me

def calculate_general_parameters(dataset=None, attributes=None, constraints=None):

    params, is_replaced = pa.calculate_params(dataset=dataset, attributes=attributes)
    params_with_min = pa.calculate_minimum_size(params=params, min_size=constraints['min_size'])    

    general_params = {'data_size': len(dataset), 'params': params_with_min}

    return general_params

def calculate_subgroup_parameters(subgroup=None, attributes=None):

    params, is_replaced = pa.calculate_params(dataset=subgroup, attributes=attributes)
    subgroup_params = {'sg_size': np.sum(params['n']), 'params': params}

    return subgroup_params, is_replaced

def add_qm(desc=None, general_params=None, subgroup_params=None, qm=None, beam_search_params=None):

    if beam_search_params['pareto']:
                
        qm_max_prev = me.calculate_max_prev(general_params=general_params, subgroup_params=subgroup_params)     
        qm_max_prev_slope = me.calculate_max_prev_slope(general_params=general_params, subgroup_params=subgroup_params) 
        qm_max_mean = me.calculate_max_mean(general_params=general_params, subgroup_params=subgroup_params)      
        qm_max_mean_slope = me.calculate_max_mean_slope(general_params=general_params, subgroup_params=subgroup_params)
        nr_prev_zero = me.calculate_nr_zero_prev_slopes(general_params=general_params, subgroup_params=subgroup_params)  
        nr_mean_zero = me.calculate_nr_zero_mean_slopes(general_params=general_params, subgroup_params=subgroup_params) 
        
        qm_max_prev.update(qm_max_prev_slope)  
        qm_max_prev.update(qm_max_mean)
        qm_max_prev.update(qm_max_mean_slope)
        qm_max_prev.update(nr_prev_zero)
        qm_max_prev.update(nr_mean_zero)
        qms = qm_max_prev  

    else:

        if qm == 'max_prev_slope':
            qms = me.calculate_max_prev_slope(general_params=general_params, subgroup_params=subgroup_params) 
        elif qm == 'max_prev':
            qms = me.calculate_max_prev(general_params=general_params, subgroup_params=subgroup_params)     
        elif qm == 'nr_prev_zero':
            qms = me.calculate_nr_zero_prev_slopes(general_params=general_params, subgroup_params=subgroup_params)  
        elif qm == 'nr_mean_zero':
            qms = me.calculate_nr_zero_mean_slopes(general_params=general_params, subgroup_params=subgroup_params)  

    # add new measures to the qualities part
    # we add sg_size here so that it will become part of the output
    desc_qm = desc.copy()
    qms['sg_size'] = np.round(subgroup_params['sg_size'] / general_params['data_size'],2)
    qms['sg_idx'] = subgroup_params['sg_idx']
    desc_qm['qualities'] = qms

    return desc_qm




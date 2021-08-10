import numpy as np
import pandas as pd

def calculate_nr_zero_mean_slopes(general_params=None, subgroup_params=None):

    slopes = subgroup_params['params']['mean_slope']
    number_zero_mean_slopes = np.sum(slopes.abs() < 0.01)

    #sg_fraction = subgroup_params['sg_size'] / general_params['data_size']
    #complement_fraction = (general_params['data_size'] - subgroup_params['sg_size']) / general_params['data_size']
    #entropy = sg_fraction * np.log(sg_fraction) - complement_fraction * np.log(complement_fraction)

    #nr_mean_zero = entropy * number_zero_mean_slopes

    nr_mean_zero = number_zero_mean_slopes
    sum_mean_zero = np.round(np.sum(slopes[slopes.abs() < 0.01].abs()),3)

    qm = {'nr_mean_zero': nr_mean_zero, 'sum_mean_zero': sum_mean_zero}

    return qm

def calculate_nr_zero_prev_slopes(general_params=None, subgroup_params=None):

    slopes = subgroup_params['params']['prev_slope']
    number_zero_prev_slopes = np.sum(slopes.abs() < 0.05)

    #sg_fraction = subgroup_params['sg_size'] / general_params['data_size']
    #complement_fraction = (general_params['data_size'] - subgroup_params['sg_size']) / general_params['data_size']
    #entropy = sg_fraction * np.log(sg_fraction) - complement_fraction * np.log(complement_fraction)

    #nr_prev_zero = entropy * number_zero_prev_slopes
    nr_prev_zero = number_zero_prev_slopes

    qm = {'nr_prev_zero': nr_prev_zero}

    return qm

def calculate_max_prev(general_params=None, subgroup_params=None):

    dif = general_params['params']['prev'] - subgroup_params['params']['prev']
    z_prev = dif / subgroup_params['params']['prev_se']
    max_prev = np.round(z_prev.abs().max(),2)

    qm = {'max_prev': max_prev}

    return qm

def calculate_max_mean(general_params=None, subgroup_params=None):

    dif = general_params['params']['mean'] - subgroup_params['params']['mean']
    z_mean = dif / subgroup_params['params']['mean_se']

    #np.nan can be ignored
    max_mean = np.round(z_mean.abs().max(),2)

    qm = {'max_mean': max_mean}

    return qm

def calculate_max_mean_slope(general_params=None, subgroup_params=None):

    dif = general_params['params']['mean_slope'] - subgroup_params['params']['mean_slope']
    z_mean_slope = dif / subgroup_params['params']['mean_slope_se'] 
    
    # np.nans can be ignored
    max_mean_slope = np.round(z_mean_slope.abs().max(),2)
    max_mean_slope_index = z_mean_slope.abs().idxmax()

    qm = {'max_mean_slope': max_mean_slope, 'max_mean_slope_index': max_mean_slope_index}

    return qm 

def calculate_max_prev_slope(general_params=None, subgroup_params=None):

    dif = general_params['params']['prev_slope'] - subgroup_params['params']['prev_slope']
    z_prev_slope = dif / subgroup_params['params']['prev_slope_se'] 

    # np.nan can be ignored
    max_prev_slope = np.round(z_prev_slope.abs().max(),2)
    max_prev_slope_index = z_prev_slope.abs().idxmax()

    qm = {'max_prev_slope': max_prev_slope, 'max_prev_slope_index': max_prev_slope_index}

    return qm
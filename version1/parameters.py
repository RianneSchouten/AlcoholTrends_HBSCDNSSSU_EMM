import numpy as np
import pandas as pd

def calculate_params(dataset=None, attributes=None):

    id_attribute = attributes['id_attribute']
    time_attribute = attributes['time_attribute']
    outcome_attribute = attributes['outcome_attribute']

    # calculate counts
    counts = dataset.groupby(time_attribute)[id_attribute].nunique()

    # calculate prevs
    counts_prevs = counts.join(dataset.groupby(time_attribute)[outcome_attribute].mean())
    counts_prevs_rename = counts_prevs.rename(columns={id_attribute[0]:'n', outcome_attribute[0]:'prev'})

    # smoothing of trend
    counts_prevs_means = smooth_trend(counts_prevs=counts_prevs_rename)
    #column_name = 'mean'
    #column_name = 'prev'
    
    # calculate ses of both columns
    counts_prevs_means_ses = calculate_prev_mean_ses(counts_prevs_means=counts_prevs_means)

    # calculate other parameters
    counts_prevs_means_ses_slopes = calculate_slopes(counts_prevs_means_ses=counts_prevs_means_ses)
    counts_prevs_means_ses_slopes_ses, is_replaced = calculate_slopes_ses(counts_prevs_means_ses_slopes=counts_prevs_means_ses_slopes)
    
    #counts_prevs_means_ses_slopes_ses_curves = calculate_curves(counts_prevs_means_ses_slopes_ses=counts_prevs_means_ses_slopes_ses, column_name=column_name)
    #counts_prevs_means_ses_slopes_ses_curves_ses = calculate_curves_ses(counts_prevs_means_ses_slopes_ses_curves=counts_prevs_means_ses_slopes_ses_curves, column_name=column_name)

    params = counts_prevs_means_ses_slopes_ses.copy()

    return params, is_replaced

def smooth_trend(counts_prevs=None):

    # weighted average  
    prevs = counts_prevs['prev'].values
    n = counts_prevs['n'].values
    totals = prevs*n
    means = (totals[1:] + totals[:-1]) / (n[1:] + n[:-1])
    ns = n[1:] + n[:-1]
    
    counts_prevs_means = counts_prevs.copy()
    counts_prevs_means['mean'] = np.append(means, [np.nan])
    counts_prevs_means['n_mean'] = np.append(ns, [np.nan])

    return counts_prevs_means

def calculate_prev_mean_ses(counts_prevs_means=None):

    # se of prev
    theta = counts_prevs_means['prev'].values
    var = (theta * (1 - theta)) / counts_prevs_means['n'].values
    ses = np.sqrt(var)

    counts_prevs_means_ses = counts_prevs_means.copy()
    counts_prevs_means_ses['prev_se'] = ses

    # se of mean
    thetas = counts_prevs_means['mean'].values
    vars = (thetas * (1 - thetas)) / counts_prevs_means['n_mean'].values
    sess = np.sqrt(vars)

    counts_prevs_means_ses['mean_se'] = sess

    return counts_prevs_means_ses

def calculate_slopes(counts_prevs_means_ses=None):

    # slope of prev
    thetas = counts_prevs_means_ses['prev'].values
    slopes = thetas[1:] - thetas[:-1]

    counts_prevs_means_ses_slopes = counts_prevs_means_ses.copy()
    new_column_name = 'prev' + '_slope'
    counts_prevs_means_ses_slopes[new_column_name] = np.append(slopes, [np.nan])

    # slope of mean
    thetas = counts_prevs_means_ses['mean'].values
    slopes = thetas[1:] - thetas[:-1]
    counts_prevs_means_ses_slopes['mean' + '_slope'] = np.append(slopes, [np.nan])

    return counts_prevs_means_ses_slopes

def calculate_slopes_ses(counts_prevs_means_ses_slopes=None):

    # se of slope of prev
    column_name_se = 'prev' + '_se'
    ses = counts_prevs_means_ses_slopes[column_name_se].values
    var = ses**2
    sum_var = var[1:] + var[:-1]
    slopes_ses = np.sqrt(sum_var)

    counts_prevs_means_ses_slopes_ses = counts_prevs_means_ses_slopes.copy()
    new_column_name = 'prev' + '_slope_se'
    counts_prevs_means_ses_slopes_ses[new_column_name] = np.append(slopes_ses, [np.nan])

    # it is only a problem if two years in a row have an se of 0
    # for small subgroups, prev and se can be 0.0
    # we replace these small se values with the minimum se of other years
    is_replaced = False
    counts_prevs_means_ses_slopes_ses_copy = counts_prevs_means_ses_slopes_ses.copy()
    idx_replace = counts_prevs_means_ses_slopes_ses_copy[new_column_name] == 0.0
    if np.sum(idx_replace) > 0:
        counts_prevs_means_ses_slopes_ses_copy.loc[idx_replace, new_column_name] = \
            np.min(counts_prevs_means_ses_slopes_ses.loc[~idx_replace, new_column_name])
        is_replaced = True

    # se of slope of mean
    column_name_se = 'mean' + '_se'
    ses = counts_prevs_means_ses_slopes_ses_copy[column_name_se].values
    var = ses**2
    sum_var = var[1:] + var[:-1]
    slopes_ses = np.sqrt(sum_var)

    new_column_name = 'mean' + '_slope_se'
    counts_prevs_means_ses_slopes_ses_copy[new_column_name] = np.append(slopes_ses, [np.nan])

    # it is only a problem if two years in a row have an se of 0
    # for small subgroups, prev and se can be 0.0
    # we replace these small se values with the minimum se of other years
    counts_prevs_means_ses_slopes_ses_copy_copy = counts_prevs_means_ses_slopes_ses_copy.copy()
    idx_replace = counts_prevs_means_ses_slopes_ses_copy_copy[new_column_name] == 0.0
    if np.sum(idx_replace) > 0:
        counts_prevs_means_ses_slopes_ses_copy_copy.loc[idx_replace, new_column_name] = \
            np.min(counts_prevs_means_ses_slopes_ses_copy.loc[~idx_replace, new_column_name])

    return counts_prevs_means_ses_slopes_ses_copy_copy, is_replaced

'''
def calculate_curves(counts_prevs_means_ses_slopes_ses=None, column_name=None):

    column_name_slope = column_name + '_slope'
    thetas = counts_prevs_means_ses_slopes_ses[column_name_slope].values
    curves = thetas[1:] - thetas[:-1]

    counts_prevs_means_ses_slopes_ses_curves = counts_prevs_means_ses_slopes_ses.copy()
    new_column_name = column_name + '_curve'
    counts_prevs_means_ses_slopes_ses_curves[new_column_name] = np.append(curves, [np.nan])

    return counts_prevs_means_ses_slopes_ses_curves

def calculate_curves_ses(counts_prevs_means_ses_slopes_ses_curves=None, column_name=None):

    column_name_slope_se = column_name + '_slope_se'
    ses = counts_prevs_means_ses_slopes_ses_curves[column_name_slope_se].values
    var = ses**2
    sum_var = var[1:] + var[:-1]
    curves_ses = np.sqrt(sum_var)

    counts_prevs_means_ses_slopes_ses_curves_ses = counts_prevs_means_ses_slopes_ses_curves.copy()
    new_column_name = column_name + '_curve_se'
    counts_prevs_means_ses_slopes_ses_curves_ses[new_column_name] = np.append(curves_ses, [np.nan])

    # for small subgroups, prev and se can be 0.0
    # we replace these small se values with the minimum se of other years
    counts_prevs_means_ses_slopes_ses_curves_ses_copy = counts_prevs_means_ses_slopes_ses_curves_ses.copy()
    idx_replace = counts_prevs_means_ses_slopes_ses_curves_ses[new_column_name] == 0.0
    if np.sum(idx_replace) > 0:
        counts_prevs_means_ses_slopes_ses_curves_ses_copy.loc[idx_replace, new_column_name] = \
            np.min(counts_prevs_means_ses_slopes_ses_curves_ses.loc[~idx_replace, new_column_name])

    return counts_prevs_means_ses_slopes_ses_curves_ses_copy
'''
def calculate_minimum_size(params=None, min_size=None):

    params['min_size'] = params['n']*min_size

    return params




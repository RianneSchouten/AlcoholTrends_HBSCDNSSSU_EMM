import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def pareto_prepare_beam_and_candidate_result_set(candidate_result_set=None, cq_satisfied=None, quality_measures=None, beam_search_params=None):

    '''
    # make scatterplot
    qualities = [cq_satisfied[i]['qualities'] for i in np.arange(len(cq_satisfied))]
    qualities_pd = pd.DataFrame(qualities)
    plot = make_scatterplot(qualities_pd=qualities_pd)
    '''
    
    candidate_queue = select_pareto_descriptions(cq_satisfied=cq_satisfied, quality_measures=quality_measures, beam_search_params=beam_search_params)

    # add the beam to the result set
    candidate_result_set.append(candidate_queue) # creates a nested list
    candidate_result_set_long = [item for sublist in candidate_result_set for item in sublist] # unlist alle elements

    result_set = select_pareto_descriptions(cq_satisfied=candidate_result_set_long, quality_measures=quality_measures, beam_search_params=beam_search_params)

    return [result_set], candidate_queue

def select_pareto_descriptions(cq_satisfied=None, quality_measures=None, beam_search_params=None):

    name1 = quality_measures[0]
    name2 = quality_measures[1]

    # extract quality values cq
    cq = cq_satisfied.copy()
    qv_list = [{'id': i, name1: cq[i]['qualities'][name1], name2: cq[i]['qualities'][name2]} for i in np.arange(len(cq))]
    qv = pd.DataFrame(qv_list)

    # select the values on the pareto front
    pv = calculate_pareto_front(qv=qv, name1=name1, name2=name2)

    # select the according subgroups for the candidate queue
    # perform a random sampling if there are too many subgroups
    idx_pv = pv.loc[pv['pv'], 'id'].values
    if len(idx_pv) < beam_search_params['w']:
        candidate_queue = [cq[i] for i in idx_pv]
    else:
        print('need to do sampling')
        candidate_queue = [cq[i] for i in idx_pv]
        #do sampling

    return candidate_queue

def calculate_pareto_front(qv=None, name1=None, name2=None):

    # first order dimension 1, with nested sort for dimension 2
    # it is import for the for loop that the index values are reset
    pv = qv.sort_values(by=[name1, name2], ascending=False).reset_index(drop=True)

    # for loop over dimension 2
    pv['pv'] = np.nan
    pv['lower_bound'] = np.nan
    pv.loc[0, 'lower_bound'] = 0.0
    for i in np.arange(len(pv)):
        if pv.loc[i, name2] > pv.loc[i, 'lower_bound']:
            pv.loc[i, 'pv'] = True
            if i+1 < len(pv): pv.loc[i+1, 'lower_bound'] = pv.loc[i, name2]
        else: 
            pv.loc[i, 'pv'] = False
            if i+1 < len(pv): pv.loc[i+1, 'lower_bound'] = pv.loc[i, 'lower_bound']

    return pv

def sample_pareto_descs():

    return 10

def make_scatterplot(qualities_pd=None):

    names = ['max_mean_slope', 'max_prev_slope', 
             'max_prev', 'max_mean', 
             'nr_prev_zero', 'nr_mean_zero']
    n = len(names)

    fig, axs = plt.subplots(n, n)
    fig.set_figheight(15)
    fig.set_figwidth(15)

    for i in np.arange(0, n):
        x_name = names[i]
        x_values = qualities_pd[x_name].values
        for j in np.arange(0, n):
            y_name = names[j]
            y_values = qualities_pd[y_name].values
            axs[i, j].scatter(x_values, y_values)
            if j == 0:
                axs[i,j].set_ylabel(x_name)
            if i == 0:
                axs[i,j].set_title(y_name)
    
    plt.savefig('C:/Users/20200059/Documents/Github/analysis_alcoholtrends_emm_hbscpeil/data_output/MPALC_70/scatters_quality_measures.png')
    #plt.show()

    return plot
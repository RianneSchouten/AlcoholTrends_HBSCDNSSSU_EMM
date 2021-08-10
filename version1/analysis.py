import numpy as np
import pandas as pd

import preprocess as pp
import beam_search as bs
import distribution_false_discoveries as dfd

def analysis(data_input=None, data_output_location=None, qm=None, beam_search_params=None, constraints=None, dfd_params=None, wcs_params=None):

    dataset, attributes, descriptives = pp.preprocess(data_input=data_input)

    # if there is just one quality measure
    if len(qm) == 1:

        beam_search_params['pareto'] = False

        # check if distribution has to be made
        if dfd_params['make']:
            # build dfd, as a pd.DataFrame where the quality values are a list, and other values are distribution params
            distribution_params = dfd.distribution_false_discoveries_params(m=dfd_params['m'], qm=qm[0],
                                                                            beam_search_params=beam_search_params,
                                                                            dataset=dataset, attributes=attributes, descriptives=descriptives, 
                                                                            wcs_params=wcs_params, constraints=constraints)

        else:
            distribution_params = None               

        # a single run
        print(beam_search_params)
        result_emm, general_params, considered_subgroups = bs.beam_search(dataset=dataset, attributes=attributes, descriptives=descriptives, 
                                                                          qm=qm[0], beam_search_params=beam_search_params, wcs_params=wcs_params,
                                                                          constraints=constraints)
    
    # run beam search with pareto front
    else:

        beam_search_params['pareto'] = True
        result_emm, general_params, considered_subgroups = bs.beam_search(dataset=dataset, attributes=attributes, descriptives=descriptives, 
                                                                          qm=qm, beam_search_params=beam_search_params, wcs_params=wcs_params,
                                                                          constraints=constraints)

    result_analysis = result_emm

    return result_analysis, general_params, considered_subgroups, distribution_params
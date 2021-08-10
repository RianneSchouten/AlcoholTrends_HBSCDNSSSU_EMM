import numpy as np
import pandas as pd
import itertools as it

import select_subgroup as ss
import collect_qualities as qu
import constraints as cs

def apply_dominance_pruning(result_set=None, dataset=None, descriptives=None, attributes=None, general_params=None, qm=None, beam_search_params=None):

    print('start pruning')
    pruned_descriptions = get_new_descriptions(result_set=result_set)
    pruned_subgroups, n_small_groups, n_is_replaced = get_new_qualities(pruned_descriptions=pruned_descriptions, dataset=dataset, 
                                                                        descriptives=descriptives, attributes=attributes, 
                                                                        general_params=general_params, qm=qm, beam_search_params=beam_search_params)
    # append with result_set, to keep the original subgroups as well
    all_subgroups = [result_set.copy()]
    all_subgroups.append(pruned_subgroups)
    all_subgroups = [item for sublist in all_subgroups for item in sublist]

    return all_subgroups, len(pruned_descriptions), n_small_groups, n_is_replaced

def get_new_descriptions(result_set=None):

    pruned_descriptions = []
    for existing_subgroup in result_set:

        old_desc = existing_subgroup['description']
        items_old_desc = old_desc.items()

        for r in np.arange(1, len(list(items_old_desc))):
            combs = list(it.combinations(items_old_desc, r=r))
            combs_r = [{'description': dict(desc)} for desc in combs]
            pruned_descriptions.append(combs_r)

    pruned_descriptions = [item for sublist in pruned_descriptions for item in sublist]

    return pruned_descriptions

def get_new_qualities(pruned_descriptions=None, dataset=None, descriptives=None, attributes=None, general_params=None, qm=None, beam_search_params=None):

    pruned_subgroups = []
    n_small_groups = 0
    n_is_replaced = 0
    for desc in pruned_descriptions:

        #print(desc)

        subgroup, idx_sg, subgroup_compl, idx_compl = ss.select_subgroup(description=desc['description'], df=dataset, descriptives=descriptives)
        subgroup_params, is_replaced = qu.calculate_subgroup_parameters(subgroup=subgroup, attributes=attributes)
        subgroup_params['sg_idx'] = idx_sg # necessary for weighting when selecting beam, see below

        # a check on subgroup size
        constraint_check_size = cs.constraint_subgroup_size(general_params=general_params, subgroup_params=subgroup_params)
        if not constraint_check_size:
            n_small_groups += 1
        else: 
            # we only want this to count if the sample size is large enough
            if is_replaced:
                n_is_replaced += 1 

            # quality value
            desc_qm = qu.add_qm(desc=desc, general_params=general_params, subgroup_params=subgroup_params, 
                                qm=qm, beam_search_params=beam_search_params) 
            #print(desc_qm.keys())
            pruned_subgroups.append(desc_qm)   

    return pruned_subgroups, n_small_groups, n_is_replaced
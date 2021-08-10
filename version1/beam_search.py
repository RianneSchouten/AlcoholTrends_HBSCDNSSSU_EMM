import numpy as np
import pandas as pd

import collect_qualities as qu
import refinements as rf
import select_subgroup as ss
import constraints as cs
import prepare_beam as pb
import prepare_result as pr
import dominance_pruning as dp

def beam_search(dataset=None, attributes=None, descriptives=None, qm=None, beam_search_params=None, wcs_params=None, constraints=None):

    general_params = qu.calculate_general_parameters(dataset=dataset, attributes=attributes, constraints=constraints)
    candidate_queue, nominal_values = rf.create_starting_descriptions(dataset=dataset, descriptives=descriptives, b=beam_search_params['b'])

    candidate_result_set = []
    considered_subgroups = {}
    for d_i in range(1, beam_search_params['d']+1):

        print('d_i', d_i)

        n_consd = 0
        n_small_groups = 0
        n_sim_descs = 0
        n_is_replaced = 0

        cq_satisfied = []
        for seed in candidate_queue:

            #print('seed', seed)

            if d_i == 1:
                seed_set = []
                seed_set.append(seed)
            else:                
                subgroup, idx_sg, subgroup_compl, idx_compl = ss.select_subgroup(description=seed['description'], df=dataset, descriptives=descriptives)
                seed_set = rf.refine_seed(seed=seed, subgroup=subgroup, descriptives=descriptives, b=beam_search_params['b'], nominal_values=nominal_values)

            for desc in seed_set:

                #print('desc', desc)
                n_consd += 1

                # a check for similar descriptions
                check_similar_description = cs.similar_description(desc=desc, cq_satisfied=cq_satisfied)    

                if not check_similar_description:
                    n_sim_descs += 1
                    #print('redundancy_check_description false for ', desc)
                else:

                    subgroup, idx_sg, subgroup_compl, idx_compl = ss.select_subgroup(description=desc['description'], df=dataset, descriptives=descriptives)
                    subgroup_params, is_replaced = qu.calculate_subgroup_parameters(subgroup=subgroup, attributes=attributes)
                    subgroup_params['sg_idx'] = idx_sg # necessary for weighting when selecting beam, see below
                            
                    # a check on subgroup size
                    constraint_check_size = cs.constraint_subgroup_size(general_params=general_params, subgroup_params=subgroup_params)
                    if not constraint_check_size:
                        n_small_groups += 1
                        #print('constraint_check_size false for ', desc)
                    else: 
                        # we only want this to count if the sample size is large enough
                        if is_replaced:
                            n_is_replaced += 1 

                        # quality value
                        desc_qm = qu.add_qm(desc=desc, general_params=general_params, subgroup_params=subgroup_params, 
                                            qm=qm, beam_search_params=beam_search_params) 
                        cq_satisfied.append(desc_qm)                                                               
                    
        considered_subgroups['level_' + str(d_i)] = {'n_consd': n_consd, 'n_sim_descs': n_sim_descs, 
                                                     'n_small_groups': n_small_groups, 'n_is_replaced': n_is_replaced}

        # below we prepare the result set and beam (candidate_queue) for the next level
        # there, we apply description based selection and cover based selection to prevent issues with redundancy
        beam_search_params.update({'d_i': d_i})
        candidate_result_set, candidate_queue, n_redun_descs = pb.collect_beam_and_candidate_result_set(candidate_result_set=candidate_result_set, cq_satisfied=cq_satisfied, 
                                                                                                        qm=qm, beam_search_params=beam_search_params, 
                                                                                                        data_size=general_params['data_size'], wcs_params=wcs_params)
        considered_subgroups['level_' + str(d_i)]['n_redun_decs'] = n_redun_descs

    if not beam_search_params['pareto']:

        result_set, rs_n_redun_descs = pr.select_result_set(candidate_result_set=candidate_result_set[0], qm=qm, beam_search_params=beam_search_params, 
                                                            data_size=general_params['data_size'], wcs_params=wcs_params)

        # apply dominance pruning
        result_set_pruned, n_consd, n_small_groups, n_is_replaced = dp.apply_dominance_pruning(result_set=result_set, dataset=dataset, descriptives=descriptives, attributes=attributes, 
                                                                                               general_params=general_params, qm=qm, beam_search_params=beam_search_params)
        # again apply description and cover based selection
        final_result_set, rs_n_redun_descs = pr.select_result_set(candidate_result_set=result_set_pruned, qm=qm, beam_search_params=beam_search_params, 
                                                                  data_size=general_params['data_size'], wcs_params=wcs_params)
        
        considered_subgroups['dominance_pruning'] = {'n_consd': n_consd, 'n_sim_descs': None, 
                                                     'n_small_groups': n_small_groups, 'n_is_replaced': n_is_replaced,
                                                     'n_redun_decs': rs_n_redun_descs}

    else:

        final_result_set = candidate_result_set[0]

    # result_set is a dictionary
    # result_emm is a dataframe with the descriptive attributes on the columns, and q*2 rows
    result_emm = pr.prepare_result_list(result_set=final_result_set)

    return result_emm, general_params, considered_subgroups
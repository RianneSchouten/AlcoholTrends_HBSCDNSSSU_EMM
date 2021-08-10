import numpy as np

# because the descriptions are saved in a dictionary
# it is possible to compare them without reordering them
# the binary, nominal (tuple), ordinal (Index) and numerical (tuple) can be handled
def similar_description(desc=None, cq_satisfied=None):

    check_similar_description = True

    # check for redundant descriptions (the exact same description but in another order)
    # the comparison has to be done with the candidate queue of the current iteration only
    # this queue is saved in cq_satisfied
    # in theory, a refinement at the current level can be similar to a desc from an earlier level
    # this can happen for numerical and ordinal attributes
    # changes are low that those descriptions will end up in the result list together
    for seed in cq_satisfied:
        if desc['description'] == seed['description']:
            check_similar_description = False
            break

    return check_similar_description

# per year/meting, the size should be at least min_size 
# the cutoff values are saved in general_params
def constraint_subgroup_size(general_params=None, subgroup_params=None):

    subgroup_values = subgroup_params['params']['n'].values
    
    if len(subgroup_values) == 9:        
        difs = subgroup_values - general_params['params']['min_size'].values
        # if difs > 0 for all years, then we agree with this subgroup
        constraint_check_size = np.all(difs > 0)
    else:
        constraint_check_size = False

    return constraint_check_size
                    
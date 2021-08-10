import numpy as np
import itertools as it

def create_starting_descriptions(dataset=None, descriptives=None, b=None):

    cq_bin = refine_binary_attributes(seed=None, dataset=dataset, subgroup=None, binary_attributes=descriptives['bin_atts'])    
    
    cq_bin_nom, nominal_values = refine_nominal_attributes(cq=cq_bin, seed=None, dataset=dataset, subgroup=None, 
                                                           nominal_attributes=descriptives['nom_atts'], nominal_values=None)
    
    cq_bin_nom_num = refine_numerical_attributes(cq=cq_bin_nom, seed=None, dataset=dataset, subgroup=None, 
                                                 numerical_attributes=descriptives['num_atts'], b=b)

    cq_bin_nom_num_ord = refine_ordinal_attributes(cq=cq_bin_nom_num, seed=None, dataset=dataset, subgroup=None, 
                                                   ordinal_attributes=descriptives['ord_atts'])

    return cq_bin_nom_num_ord, nominal_values

def refine_seed(seed=None, subgroup=None, descriptives=None, b=None, nominal_values=None):

    cq_bin = refine_binary_attributes(seed=seed, dataset=None, subgroup=subgroup, binary_attributes=descriptives['bin_atts'])

    cq_bin_nom = refine_nominal_attributes(cq=cq_bin, seed=seed, dataset=None, subgroup=subgroup, 
                                           nominal_attributes=descriptives['nom_atts'], nominal_values=nominal_values)
    
    cq_bin_nom_num = refine_numerical_attributes(cq=cq_bin_nom, seed=seed, dataset=None, subgroup=subgroup, 
                                                 numerical_attributes=descriptives['num_atts'], b=b)

    cq_bin_nom_num_ord = refine_ordinal_attributes(cq=cq_bin_nom_num, seed=seed, dataset=None, subgroup=subgroup, 
                                                   ordinal_attributes=descriptives['ord_atts'])
 
    return cq_bin_nom_num_ord

def refine_numerical_attributes(cq=None, seed=None, dataset=None, subgroup=None, numerical_attributes=None, b=None):

    refined_cq = cq

    quantiles = np.linspace(0, 1, b+1)[1:-1] # for 4 quantiles, this results in 0.25, 0.5, 0.75
    
    # first candidate queue
    if seed is None:
        for attribute in numerical_attributes:
            
            values = dataset[attribute]

            # continue with quantile split
            min_value = values.quantile(0.0) 
            max_value = values.quantile(1.0)
              
            for i in range(b-1):
                value = values.quantile(quantiles[i], interpolation='linear')

                refined_cq.append({'description' : {attribute : (min_value, value)}})
                refined_cq.append({'description' : {attribute : (value, max_value)}})       

    # refinements for existing candidate queue
    else:    
        description = seed['description']        
        for attribute in numerical_attributes:
            
            values = subgroup[attribute]
            
            # continue with quantile split
            # only if there are real numbers left in the subgroup
            min_value = values.quantile(0.0) 
            max_value = values.quantile(1.0)
                
            for i in range(b-1):

                value = values.quantile(quantiles[i], interpolation='linear')

                temp_desc = description.copy()
                temp_desc[attribute] = (min_value, value) # this replaces the original boundaries for this attribute
                refined_cq.append({'description' : temp_desc})

                temp_desc_2 = description.copy()
                temp_desc_2[attribute] = (value, max_value) # this replaces the original boundaries for this attribute
                refined_cq.append({'description' : temp_desc_2})     

    return  refined_cq

def refine_nominal_attributes(cq=None, seed=None, dataset=None, subgroup=None, nominal_attributes=None, nominal_values=None):

    refined_cq = cq

    # first candidate queue
    if seed is None:

        nominal_values = {}

        for attribute in nominal_attributes:
            
            values = dataset[attribute].unique()
            nominal_values.update({attribute: values})

            for i in range(len(values)):

                value = values[i]
                refined_cq.append({'description' : {attribute : (1.0, value)}}) # 1.0 indicates == this nominal value
                refined_cq.append({'description' : {attribute : (0.0, value)}}) # 0.0 indicates != this nominal value

        return refined_cq, nominal_values

    # refinements for existing candidate queue
    else:
        
        description = seed['description']

        for attribute in nominal_attributes:
            if not attribute in list(description.keys()):

                values = nominal_values[attribute]

                for i in range(len(values)):

                    value = values[i]
                    tup1 = (1.0, value)
                    tup0 = (0.0, value)

                    temp_desc = description.copy()
                    
                    '''
                    # We don't make a list. We make only one literal per nominal attribute per description.
                    # Because peil/hbsc's nominal attributes do not have many categories, we can include both 0.0 and 1.0 
                    if attribute in list(temp_desc.keys()):
                        temp_tuple_list = temp_desc[attribute].copy()
                        # if the (1.0, value) is already there, no need to add either tup1 or tup0
                        # if the (1.0, value) is not there, tup1 can be added, whether or not (0,0, value) is there.
                        if tup1 not in temp_tuple_list:
                            temp_tuple_list.append(tup1)
                            temp_desc[attribute] = temp_tuple_list
                            refined_cq.append({'description' : temp_desc})
                    else:
                        temp_desc[attribute] = [tup1] # every one-tuple description also has a list, to be able to add other tuples later on      
                        refined_cq.append({'description' : temp_desc})

                    temp_desc = description.copy()
                    if attribute in list(temp_desc.keys()):
                        temp_tuple_list = temp_desc[attribute].copy()
                        # if the (0.0, value) is already there, tup0 does not have to be added
                        # if the (0,0, value) is not there, and in addition (1.0, value) is not there, then tup0 can be added
                        if ((tup0 not in temp_tuple_list) and (tup1 not in temp_tuple_list)):
                            temp_tuple_list.append(tup0)
                            temp_desc[attribute] = temp_tuple_list
                            refined_cq.append({'description' : temp_desc})
                    else:
                        temp_desc[attribute] = [tup0]     
                        refined_cq.append({'description' : temp_desc})
                    '''

                    temp_desc[attribute] = tup1
                    refined_cq.append({'description' : temp_desc})

                    temp_desc_2 = description.copy()
                    temp_desc_2[attribute] = tup0
                    refined_cq.append({'description' : temp_desc_2})
        
        return refined_cq

def refine_binary_attributes(seed=None, dataset=None, subgroup=None, binary_attributes=None):

    refined_cq = []

    # first candidate queue
    if seed is None:

        for attribute in binary_attributes:
            
            values = dataset[attribute].unique()
            refined_cq.append({'description' : {attribute : [values[0]]}})
            refined_cq.append({'description' : {attribute : [values[1]]}})

    # refinements for a seed
    else:
        
        description = seed['description']

        for attribute in binary_attributes:
            if not attribute in list(description.keys()):
                
                values = subgroup[attribute].unique()
                for i in range(len(values)):

                    value = values[i]
                    temp_desc = description.copy()
                    temp_desc[attribute] = [value]
                    refined_cq.append({'description' : temp_desc})

    return  refined_cq     

def refine_ordinal_attributes(cq=None, seed=None, dataset=None, subgroup=None, ordinal_attributes=None):

    refined_cq = cq

    # first candidate queue
    if seed is None:
        for attribute in ordinal_attributes:
            
            cat_values = dataset[attribute].cat.categories
            for i in range(len(cat_values)-1):
                
                refined_cq.append({'description' : {attribute : list(cat_values[0:i+1].values)}})
                refined_cq.append({'description' : {attribute : list(cat_values[i+1:].values)}})       

    # refinements for existing candidate queue
    else:    
        description = seed['description']        
        for attribute in ordinal_attributes:
            
            cat_values = subgroup[attribute].cat.categories

            # if len = 1, nothing needs to happen
            if len(cat_values) > 1:               
                for i in range(len(cat_values)-1):

                    temp_desc = description.copy()
                    temp_desc[attribute] = list(cat_values[0:i+1]) # this replaces the original boundaries for this attribute
                    refined_cq.append({'description' : temp_desc})

                    temp_desc_2 = description.copy()
                    temp_desc_2[attribute] = list(cat_values[i+1:]) # this replaces the original boundaries for this attribute
                    refined_cq.append({'description' : temp_desc_2})     

    return  refined_cq
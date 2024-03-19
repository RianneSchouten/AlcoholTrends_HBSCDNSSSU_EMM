import numpy as np
import pandas as pd

def select_subgroup(description=None, df=None, descriptives=None, md_method=None):

    #description_copy = description.copy()
    #order = description_copy.pop('literal_order')
    pairs = list(description.items())
    #print(md_method)

    num_atts = descriptives['num_atts']
    bin_atts = descriptives['bin_atts']
    nom_atts = descriptives['nom_atts']
    ord_atts = descriptives['ord_atts']

    if len(pairs) == 0:
        idx = []
    else: 
        # select all indices as a starting point
        idx = df.index.values

        for pair in pairs:

            #print(pair)

            att = pair[0]
            sel = pair[1]#[0] #sel[1][1] contains the order of the literal

            if att in bin_atts:
            
                idx = select_bin_att(idx=idx, att=att, sel=sel, df=df, md_method=md_method)
        
            elif att in num_atts:

                idx = select_num_att(idx=idx, att=att, sel=sel, df=df, md_method=md_method)

            elif att in nom_atts:

                idx = select_nom_att(idx=idx, att=att, sel=sel, df=df, md_method=md_method)

            elif att in ord_atts:

                idx = select_ord_att(idx=idx, att=att, sel=sel, df=df, md_method=md_method)
     
    all_idx = df.index.values
    idx_compl = np.setdiff1d(all_idx, idx)
    
    # this should be loc!!
    # make sure the dataset is sorted at the beginning of the algorithm
    subgroup = df.loc[idx]
    subgroup_compl = df.loc[idx_compl]

    #print(list(idx_sg))
    #print(list(idx_compl))

    return subgroup, list(idx), subgroup_compl, list(idx_compl)

def select_bin_att(idx=None, att=None, sel=None, df=None, md_method=None):

    idx_in = idx.copy()

    if md_method in ['ignore','cca']:
        # there will be no sel with np.nan (see refinements.py)
        sel_idx = df[df[att] == sel[0]].index.values

    if md_method == 'ignore_and_allow':
        # we allow for separate selection of rows with missing values
        # this is indicated by the sel itself
        if len(sel) == 1:
            if 'NaN' == sel[0]: # allow
                sel_idx = df[df[att].isnull()].index.values
            else: # ignore
                sel_idx = df[df[att] == sel[0]].index.values
        else:
            print('there is a problem')

    if md_method == 'ignore_allow_and_both':
        if len(sel) == 2: # both
            sel_idx_1 = df[df[att] == sel[0]].index.values
            sel_idx_2 = df[df[att].isnull()].index.values
            sel_idx = np.union1d(sel_idx_1, sel_idx_2)
        elif len(sel) == 1:
            if 'NaN' == sel[0]: # allow
                sel_idx = df[df[att].isnull()].index.values
            else: # ignore
                sel_idx = df[df[att] == sel[0]].index.values
        else:
            print('there is a problem')

    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out

def select_num_att(idx=None, att=None, sel=None, df=None, md_method=None):

    idx_in = idx.copy()

    if md_method in ['ignore','cca']:
        low_idx =  df[df[att] >= sel[0]].index.values # value can be equal to the lower bound
        up_idx = df[df[att] <= sel[1]].index.values # value can be equal to the upper bound            
        sel_idx = np.intersect1d(low_idx, up_idx)
    
    if md_method == 'ignore_and_allow':
        if len(sel) == 1:
            if 'NaN' == sel[0]: # allow
                sel_idx = df[df[att].isnull()].index.values
            else:
                print('there is a problem')
        else: # ignore
            low_idx =  df[df[att] >= sel[0]].index.values # value can be equal to the lower bound
            up_idx = df[df[att] <= sel[1]].index.values # value can be equal to the upper bound            
            sel_idx = np.intersect1d(low_idx, up_idx)
    
    if md_method == 'ignore_allow_and_both':
        if len(sel) == 3: # both
            sel_idx_1 = df[df[att].isnull()].index.values
            low_idx =  df[df[att] >= sel[0]].index.values # value can be equal to the lower bound
            up_idx = df[df[att] <= sel[1]].index.values # value can be equal to the upper bound            
            sel_idx_2 = np.intersect1d(low_idx, up_idx)
            sel_idx = np.union1d(sel_idx_1, sel_idx_2)
        elif len(sel) == 1:
            if 'NaN' == sel[0]: # allow
                sel_idx = df[df[att].isnull()].index.values
            else:
                print('there is a problem')
        else: # ignore
            low_idx =  df[df[att] >= sel[0]].index.values # value can be equal to the lower bound
            up_idx = df[df[att] <= sel[1]].index.values # value can be equal to the upper bound            
            sel_idx = np.intersect1d(low_idx, up_idx)
    
    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out

def select_nom_att(idx=None, att=None, sel=None, df=None, md_method=None):

    idx_in = idx.copy()
    tup = sel

    if md_method in ['ignore','cca']:
        # when the first value is a 1, then take all datapoints with the value in position two
        if tup[0] == 1.0:
            df_drop = df[df[att].notnull()]
            sel_idx = df_drop[df_drop[att] == tup[1]].index.values
            idx_in = np.intersect1d(idx_in, sel_idx)        
        # when the first value is a 0, then take all datapoints that do not have the value in position two
        elif tup[0] == 0.0:
            df_drop = df[df[att].notnull()]
            sel_idx = df_drop[df_drop[att] != tup[1]].index.values
            idx_in = np.intersect1d(idx_in, sel_idx)

    if md_method == 'ignore_and_allow':
        if len(tup) == 1:
            if 'NaN' == tup[0]: # allow
                sel_idx = df[df[att].isnull()].index.values
                idx_in = np.intersect1d(idx_in, sel_idx)
            else:
                print('there is a problem')
        else: # ignore
            # when the first value is a 1, then take all datapoints with the value in position two
            if tup[0] == 1.0:
                df_drop = df[df[att].notnull()]
                sel_idx = df_drop[df_drop[att] == tup[1]].index.values
                idx_in = np.intersect1d(idx_in, sel_idx)        
            # when the first value is a 0, then take all datapoints that do not have the value in position two
            elif tup[0] == 0.0:
                df_drop = df[df[att].notnull()]
                sel_idx = df_drop[df_drop[att] != tup[1]].index.values
                idx_in = np.intersect1d(idx_in, sel_idx)

    if md_method == 'ignore_allow_and_both':
        if len(tup) == 1:
            if 'NaN' == tup[0]: # allow
                sel_idx = df[df[att].isnull()].index.values
                idx_in = np.intersect1d(idx_in, sel_idx)
            else:
                print('there is a problem')
        elif len(tup) == 3: # both
            if 'NaN' == tup[2]:
                # when the first value is a 1, then take all datapoints with the value in position two
                if tup[0] == 1.0:
                    df_drop = df[df[att].notnull()]
                    sel_idx = df_drop[df_drop[att] == tup[1]].index.values
                    idx_in = np.intersect1d(idx_in, sel_idx)        
                # when the first value is a 0, then take all datapoints that do not have the value in position two
                elif tup[0] == 0.0:
                    df_drop = df[df[att].notnull()]
                    sel_idx = df_drop[df_drop[att] != tup[1]].index.values
                    idx_in = np.intersect1d(idx_in, sel_idx)
                sel_idx_1 = df[df[att].isnull()].index.values
                idx_in = np.union1d(idx_in, sel_idx_1)
            else:
                print('there is a problem')
        elif len(tup) == 2: # ignore
            # when the first value is a 1, then take all datapoints with the value in position two
            if tup[0] == 1.0:
                df_drop = df[df[att].notnull()]
                sel_idx = df_drop[df_drop[att] == tup[1]].index.values
                idx_in = np.intersect1d(idx_in, sel_idx)        
            # when the first value is a 0, then take all datapoints that do not have the value in position two
            elif tup[0] == 0.0:
                df_drop = df[df[att].notnull()]
                sel_idx = df_drop[df_drop[att] != tup[1]].index.values
                idx_in = np.intersect1d(idx_in, sel_idx)
        else:
            print('there is a problem')

    idx_out = idx_in.copy()

    return idx_out    

def select_ord_att(idx=None, att=None, sel=None, df=None, md_method=None):

    idx_in = idx.copy()     

    if md_method in ['ignore','cca']:   
        sel_idx = df[df[att].isin(sel)].index.values

    if md_method == 'ignore_and_allow':
        if len(sel) == 1:
            if 'NaN' == sel[0]: # allow
                sel_idx = df[df[att].isnull()].index.values
            else: # ignore
                sel_idx = df[df[att].isin(sel)].index.values
        else: # ignore
            # a loop over all categories in the description
            # cases that equal either of the categories should be selected
            sel_idx = df[df[att].isin(sel)].index.values

    if md_method == 'ignore_allow_and_both':
        if len(sel) == 1:
            if 'NaN' == sel[0]: # allow
                sel_idx = df[df[att].isnull()].index.values
            else: # ignore
                sel_idx = df[df[att].isin(sel)].index.values
        elif len(sel) == 2:
            if 'NaN' == sel[1]: # both
                sel_idx_1 = df[df[att].isnull()].index.values
                sel_idx_2 = df[df[att].isin(sel[0])].index.values
                sel_idx = np.union1d(sel_idx_1, sel_idx_2)
            else: # ignore
                sel_idx = df[df[att].isin(sel)].index.values
        else: # ignore
            sel_idx = df[df[att].isin(sel)].index.values

    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out   
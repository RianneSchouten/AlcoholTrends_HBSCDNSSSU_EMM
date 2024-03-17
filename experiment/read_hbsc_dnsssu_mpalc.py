import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype

def load_and_preprocess(trend_name=None, remove_data=None, incomplete=None):

    data = load(trend_name=trend_name, incomplete=incomplete)
    if remove_data:
        data = remove(data=data)
    dataset, attributes, descriptives = define_attributes(data=data, remove_data=remove_data, incomplete=incomplete)

    return dataset, attributes, descriptives

def define_attributes(data=None, remove_data=None, incomplete=None):

    time_attribute = ['meting']
    outcome_attribute = ['mpalc']

    data_sorted = data.sort_values(['meting'], ascending=[True]).reset_index(drop=True)
    data_sorted['id'] = np.arange(len(data_sorted))

    id_attribute = ['id']
    if remove_data:
        skip_attributes = ['leerjaar']     
    elif incomplete:
        skip_attributes = []    
    else:
        cat_type_leerjaar = CategoricalDtype(categories=[1.0, 2.0, 3.0, 4.0], ordered=True)
        data_sorted['leerjaar'] = data_sorted['leerjaar'].astype(cat_type_leerjaar)
        skip_attributes = [] 

    dataset = data_sorted.drop(skip_attributes, axis=1)         

    num_atts = ['lft', 'cijferleven']
    bin_atts = ['sekse', 'vollgezin']
    nom_atts = ['etngroep3', 'vaderbaan', 'moederbaan']
    if remove_data | incomplete:
        ord_atts = ['schnivo', 'stedgem', 'spijbel']
    else:
        ord_atts = ['schnivo', 'leerjaar', 'stedgem', 'spijbel']

    for att in ord_atts:
        print(att)
        print(dataset[att].cat.categories)

    print(dataset.describe())

    descriptives = {'num_atts': num_atts, 'bin_atts': bin_atts, 'nom_atts': nom_atts, 'ord_atts': ord_atts}

    attributes = {'time_attribute': time_attribute, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'outcome_attribute': outcome_attribute}

    return dataset, attributes, descriptives

def remove(data=None):

    print(data.shape)
    #print(len(data[(data['lft'] < 12) | (data['lft'] > 16)]))
    data = data[(data['lft'] > 11) & (data['lft'] < 17)]
    print(data.shape)
    #print(data.lft.unique())

    return data

def load(trend_name=None, incomplete=None):

    if incomplete:
        name_dataset = 'PeilHBSC20032019_' + trend_name + '_incomplete'
    else:
        name_dataset = 'PeilHBSC20032019_' + trend_name + '_70'
    location = 'C:/Users/20200059/Documents/Projects/ContextSpecificEffectsHBSC/Analysis/Data/' + name_dataset + '.sav'

    dataset = pd.read_spss(location)
    #print(dataset.shape)
    #print(data.head(20))
    #print(data.isnull().sum())     
    #print(dataset.dtypes) 

    # prepare right type per variable
    print(dataset['schnivo'].cat.categories)
    new_order_schnivo = [1,2,0,3]
    cat_type_schnivo = CategoricalDtype(categories=[list(dataset['schnivo'].cat.categories)[i] for i in new_order_schnivo], ordered=True)
    dataset['schnivo'] = dataset['schnivo'].astype(cat_type_schnivo)
    print(dataset['schnivo'].cat.categories)

    # leerjaar will be done later, because it depends on whether it is available in the dataset or not

    print(dataset['stedgem'].cat.categories)
    new_order_stedgem = [1,3,0,2,4]
    cat_type_stedgem = CategoricalDtype(categories=[list(dataset['stedgem'].cat.categories)[i] for i in new_order_stedgem], ordered=True)
    dataset['stedgem'] = dataset['stedgem'].astype(cat_type_stedgem)
    print(dataset['stedgem'].cat.categories)

    print(dataset['spijbel'].cat.categories)
    new_order_spijbel = []
    cat_type_spijbel = CategoricalDtype(categories=list(dataset['spijbel'].cat.categories), ordered=True)
    dataset['spijbel'] = dataset['spijbel'].astype(cat_type_spijbel)
    print(dataset['spijbel'].cat.categories)

    dataset['sekse'] = dataset['sekse'].astype(object)
    dataset['vollgezin'] = dataset['vollgezin'].astype(object)
    dataset['etngroep3'] = dataset['etngroep3'].astype(object)
    dataset['vaderbaan'] = dataset['vaderbaan'].astype(object)
    dataset['moederbaan'] = dataset['moederbaan'].astype(object)   

    return dataset
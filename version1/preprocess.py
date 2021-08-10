import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype

def preprocess(data_input=None):

    data = load(data_input=data_input)
    dataset, attributes, descriptives = define_attributes(data=data)

    return dataset, attributes, descriptives

def define_attributes(data=None):

    time_attribute = ['meting']
    outcome_attribute = ['mpalc']

    data_sorted = data.sort_values(['meting'], ascending=[True]).reset_index(drop=True)
    data_sorted['id'] = np.arange(len(data_sorted))

    id_attribute = ['id']
    skip_attributes = []

    dataset = data_sorted.drop(skip_attributes, axis=1)         

    num_atts = ['lft', 'cijferleven']
    bin_atts = ['sekse', 'vollgezin']
    nom_atts = ['etngroep3', 'vaderbaan', 'moederbaan']
    ord_atts = ['schnivo', 'leerjaar', 'stedgem', 'spijbel']

    descriptives = {'num_atts': num_atts, 'bin_atts': bin_atts, 'nom_atts': nom_atts, 'ord_atts': ord_atts}

    attributes = {'time_attribute': time_attribute, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'outcome_attribute': outcome_attribute}

    return dataset, attributes, descriptives

def load(data_input=None):

    name_dataset = 'PeilHBSC20032019_' + str(data_input)
    location = 'C:/Users/20200059/Documents/Projects/ContextSpecificEffectsHBSC/Analysis/Data/' + name_dataset + '.sav'

    dataset = pd.read_spss(location)
    #print(dataset.shape)
    #print(data.head(20))
    #print(data.isnull().sum())     
    #print(dataset.dtypes)

    # prepare right type per variable   
    cat_type_schnivo = CategoricalDtype(categories=["VMBO-p/t", "VMBO-t/HAVO", "HAVO/VWO", "VWO"], ordered=True)
    dataset['schnivo'] = dataset['schnivo'].astype(cat_type_schnivo)

    cat_type_leerjaar = CategoricalDtype(categories=[1.0, 2.0, 3.0, 4.0], ordered=True)
    dataset['leerjaar'] = dataset['leerjaar'].astype(cat_type_leerjaar)

    cat_type_stedgem = CategoricalDtype(categories=["niet stedelijk", "weinig stedelijk", "matig stedelijk", "sterk stedelijk", "zeer sterk stedelijk"], ordered=True)
    dataset['stedgem'] = dataset['stedgem'].astype(cat_type_stedgem)

    cat_type_spijbel = CategoricalDtype(categories=["0 uur", "1 lesuur", "2 lesuren", "3 of 4 lesuren", "5 of 6 lesuren", "7 of meer lesuren"], ordered=True)
    dataset['spijbel'] = dataset['spijbel'].astype(cat_type_spijbel)

    dataset['sekse'] = dataset['sekse'].astype(object)
    dataset['vollgezin'] = dataset['vollgezin'].astype(object)
    dataset['etngroep3'] = dataset['etngroep3'].astype(object)
    dataset['vaderbaan'] = dataset['vaderbaan'].astype(object)
    dataset['moederbaan'] = dataset['moederbaan'].astype(object)   

    return dataset

import numpy as np
import pandas as pd
import os

import experiment.analysis as an
import experiment.save_and_store_result as ssr

def main(data_name=None, data_from=None, datasets_names=None, synthetic_params=None, sim_params=None, extra_info=None, date=None, output_to=None):

    # create path and empty output file 
    output_to_path = output_to + data_name + '/' + 'date' + str(date) + '/'
    if not os.path.exists(output_to_path):
        os.makedirs(output_to_path)    
    excel_file_name, sheet_names = ssr.create_empty_output_file(output_to_path=output_to_path)

    if synthetic_params is None: 
        an.analysis(data_name=data_name, data_from=data_from, datasets_names=datasets_names, sim_params=sim_params,
                    extra_info=extra_info, output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)
    
    elif synthetic_params is not None:
        an.synthetic_analysis(datasets_names=datasets_names, synthetic_params=synthetic_params, data_from=data_from, sim_params=sim_params, 
                              extra_info=extra_info, output_to_path=output_to_path, excel_file_name=excel_file_name, sheet_names=sheet_names)

    ssr.final_update_result(excel_file_name=excel_file_name, sheet_names=sheet_names)

if __name__ == '__main__':

    main(data_name=None, data_from=None, datasets_names=None, synthetic_params=None, sim_params=None, extra_info=None, date=None, output_to=None)
    

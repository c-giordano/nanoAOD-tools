#!/home/cmsuser/cmssw/slc6_amd64_gcc630/cms/cmssw/CMSSW_9_4_9/external/slc6_amd64_gcc630/bin/python
# coding: utf-8


import ROOT
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 500)
import root_pandas
import xgboost as xgb
from ML_config import fetch_configuration, file_dir, fetch_file_list
import os
import sys


def boosted_decision_top_tagging(config, config_dict, file_list, tree_name):

    data_dir = file_dir()
    data_orig = pd.DataFrame()

    if sys.argv[1]=='S':
        file_name = data_dir + 'Tprime_' + sys.argv[2] + '_treeMerged.root'
    else:
        file_name = data_dir + 'unpackedBkg_treeMerged.root'
 
    data_orig = data_orig.append(root_pandas.read_root(file_name, tree_name), ignore_index=True)
    data_orig = data_orig.query(config_dict['bin'])

    sample = file_list[0][7:]
    data_orig = data_orig.query('Sample=='+sample)

    truth = 'Top_High_Truth'

    X_test_total = data_orig[config_dict['variables_'+tree_name]]

    # Load model
    model_path = '/home/diefer/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/bin/JSON/'
    model_bdt = xgb.XGBClassifier()
    model_bdt.load_model(model_path + config +'_'+ tree_name +'.json')

    y_pred_total = model_bdt.predict_proba(X_test_total)[:, 1]
    data_orig['BDT_Score'] = y_pred_total

    # Save output
    tree_path = '/home/diefer/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/bin/Root/Tprime/BDT_scores/'
    data_orig.to_root(tree_path + config +'_'+ tree_name + file_list[0][6:] + '.root', 'scores')



if __name__ == "__main__":

    config_dic = fetch_configuration()
    file_list = fetch_file_list()

    for single_file in file_list:
        if file_list[single_file]:

            for config in config_dic:
                if config_dic[config]['Electrons']:
                    if config_dic[config]['enable_merged']:
                        boosted_decision_top_tagging(config, config_dic[config], [single_file], 'el_merged')
                    if config_dic[config]['enable_resolved']:
                        boosted_decision_top_tagging(config, config_dic[config], [single_file], 'el_resolved')

                if config_dic[config]['Muons']:
                    if config_dic[config]['enable_merged']:
                        boosted_decision_top_tagging(config, config_dic[config], [single_file], 'mu_merged')
                    if config_dic[config]['enable_resolved']:
                        boosted_decision_top_tagging(config, config_dic[config], [single_file], 'mu_resolved')


#!/home/cmsuser/cmssw/slc6_amd64_gcc630/cms/cmssw/CMSSW_9_4_9/external/slc6_amd64_gcc630/bin/python
# coding: utf-8


import ROOT
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 500)
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
plt.rcParams['figure.figsize'] = (14, 7)
import root_pandas
from sklearn.model_selection import train_test_split, GridSearchCV
import xgboost as xgb
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score, confusion_matrix, auc, roc_curve
from ML_config import fetch_configuration, pre_cut_mu, pre_cut_el, file_dir, fetch_file_list
from time import time
import warnings
import concurrent.futures
 
def hyperparameters_search(config, config_dict, tree_name):

    n_estimators = [100]#,150,200]
    #learning_rate = [.01,.05,.1]
    #max_depth = [3,4,5]
    min_child_weight = [4,5]
    #reg_alpha = [.01,.05,.1]


    hyperparameters = {
                       'n_estimators' : n_estimators,
                       #'learning_rate': learning_rate,
                       #'max_depth' : max_depth,
                       'min_child_weight' : min_child_weight,
                       #'reg_alpha' : reg_alpha
                        }

    truth = 'Top_High_Truth'

    data_dir = file_dir()
    file_name = data_dir + 'Tprime_1200_treeMerged.root'

    data = root_pandas.read_root(file_name, tree_name)
    data = data.query(config_dict['bin'])
    if(tree_name[:2]=='el'):
        data = data.query(pre_cut_el())
    if(tree_name[:2]=='mu'):
        data = data.query(pre_cut_mu())
    data = data.query(config_dict['preselection_'+tree_name[:2]])

    X, y = data[config_dict['variables_'+tree_name]], data[truth].values

    assert y.size > 0
    model_bdt = xgb.XGBClassifier()

    grid = GridSearchCV(estimator=model_bdt, param_grid=hyperparameters, n_jobs=-1, scoring='accuracy', return_train_score=True)

    grid.fit(X, y)

    return pd.DataFrame.from_dict(grid.cv_results_)

def hyperparameters_search_parallel(arg):
    ret = []
    ret = hyperparameters_search(config=arg[0], config_dict=arg[1], tree_name=arg[2])
    return ret


if __name__ == "__main__":
    warnings.filterwarnings(action='ignore', category=DeprecationWarning)
    config_dic = fetch_configuration()
    args = []

    for config in config_dic:
        if config_dic[config]['Electrons']:
            if config_dic[config]['enable_merged']:
                args.append([config, config_dic[config], 'el_merged'])
            if config_dic[config]['enable_resolved']:
                args.append([config, config_dic[config], 'el_resolved'])
        if config_dic[config]['Muons']:
            if config_dic[config]['enable_merged']:
                args.append([config, config_dic[config], 'mu_merged'])
            if config_dic[config]['enable_resolved']:
                args.append([config, config_dic[config], 'mu_resolved'])

        with concurrent.futures.ProcessPoolExecutor() as executor:
           dataframes = executor.map(hyperparameters_search_parallel, args)
    dataframes = list(dataframes)
  
    for i in range(len(dataframes)):
        dataframes[i].to_csv('Csv/Hyperparameters/Tprime_1200/' + args[i][0] + '_' + args[i][2] + '.csv', index=False)

def fetch_configuration():

    el_all = [
                   'MET',
                   'MET_phi',
                   'Jet_Mass',
                   'Jet_Pt',
                   'Jet_Eta',
                   'Jet_Phi',
                   'Jet_DeepFlavB',
                   'Electron_Pt',
                   'Electron_Eta',
                   'Electron_Phi',
                   'Electron_Charge',
                   'Electron_Dxy',
                   'Electron_DxyErr',
                   'Electron_Dz',
                   'Electron_DzErr',
                   'Electron_cutBased',
                   'Electron_MiniIso',
                   'Electron_Iso03',
                   'Electron_mvaIsoL',
                   'Electron_mvaIso90',
                   'Electron_mvaIso80',
                   'Electron_mvanoIsoL',
                   'Electron_mvanoIso90',
                   'Electron_mvanoIso80',
                   'Electron_Over_Jet_Pt',
                   'Top_Mass',
                   'Top_Pt',
                   'Top_Eta',
                   'Top_Phi',
                   'Top_E',
                   'Top2_Mass',
                   'Top2_Pt',
                   'Top2_Eta',
                   'Top2_Phi',
                   'Top2_E',
                   'Top_mT',
                   'Top_Jet_Unboosted_Mass',
                   'Top_Jet_Unboosted_Pt',
                   'Top_Jet_Unboosted_Eta',
                   'Top_Jet_Unboosted_Phi',
                   'Top_Jet_Unboosted_E',
                   'Top_Lep_Unboosted_Mass',
                   'Top_Lep_Unboosted_Pt',
                   'Top_Lep_Unboosted_Eta',
                   'Top_Lep_Unboosted_Phi',
                   'Top_Lep_Unboosted_E',
                   'Top_Relative_Pt',
                   'Top_Costheta',
                   'Top_dR'
                   ]
    mu_all = [
                   'MET',
                   'MET_phi',
                   'Jet_Mass',
                   'Jet_Pt',
                   'Jet_Eta',
                   'Jet_Phi',
                   'Jet_DeepFlavB',
                   'Muon_Pt',
                   'Muon_Eta',
                   'Muon_Phi',
                   'Muon_Charge',
                   'Muon_Dxy',
                   'Muon_DxyErr',
                   'Muon_Dz',
                   'Muon_DzErr',
                   'Muon_isLoose',
                   'Muon_isMedium',
                   'Muon_isTight',
                   'Muon_isGlobal',
                   'Muon_isTracker',
                   'Muon_nStations',
                   'Muon_nTrackerLayers',
                   'Muon_MiniIso',
                   'Muon_Iso04',
                   'Muon_Over_Jet_Pt',
                   'Top_Mass',
                   'Top_Pt',
                   'Top_Eta',
                   'Top_Phi',
                   'Top_E',
                   'Top2_Mass',
                   'Top2_Pt',
                   'Top2_Eta',
                   'Top2_Phi',
                   'Top2_E',
                   'Top_mT',
                   'Top_Jet_Unboosted_Mass',
                   'Top_Jet_Unboosted_Pt',
                   'Top_Jet_Unboosted_Eta',
                   'Top_Jet_Unboosted_Phi',
                   'Top_Jet_Unboosted_E',
                   'Top_Lep_Unboosted_Mass',
                   'Top_Lep_Unboosted_Pt',
                   'Top_Lep_Unboosted_Eta',
                   'Top_Lep_Unboosted_Phi',
                   'Top_Lep_Unboosted_E',
                   'Top_Relative_Pt',
                   'Top_Costheta',
                   'Top_dR'
                   ]

    low_pt_el_merged = [
                   #'MET',
                   'Jet_Mass',
                   'Jet_Pt',
                   'Jet_DeepFlavB',
                   #'Electron_Pt',
                   'Electron_Dxy',
                   #'Electron_DxyErr',
                   'Electron_Dz',
                   #'Electron_DzErr',
                   'Electron_MiniIso',
                   'Electron_Iso03',
                   'Electron_Over_Jet_Pt',
                   'Top_Mass',
                   'Top_Pt',
                   'Top_mT',
                   'Top_Relative_Pt',
                   'Top_Costheta',
                   'Top_dR'
                   ]

    low_pt_mu_merged = [
                   #'MET',
                   'Jet_Mass',
                   'Jet_DeepFlavB',
                   #'Muon_Pt',
                   'Muon_Dxy',
                   #'Muon_DxyErr',
                   'Muon_Dz',
                   #'Muon_DzErr',
                   'Muon_MiniIso',
                   'Muon_Iso04',
                   'Muon_Over_Jet_Pt',
                   'Top_Mass',
                   'Top_Pt',
                   #'Top_mT',
                   'Top_Relative_Pt',
                   #'Top_Costheta',
                   'Top_dR'
                   ]

    low_pt_el_resolved = [
                   'Jet_Mass',
                   'Jet_Pt',
                   'Jet_DeepFlavB',
                   'Electron_Pt',
                   'Electron_Dxy',
                   'Electron_DxyErr',
                   'Electron_Dz',
                   'Electron_DzErr',
                   'Electron_MiniIso',
                   'Electron_Iso03',
                   'Electron_Over_Jet_Pt',
                   'Top_Mass',
                   'Top_Pt',
                   'Top2_Mass',
                   'Top2_Pt',
                   'Top_mT',
                   'Top_Relative_Pt',
                   'Top_Costheta',
                   'Top_dR',
                   ]

    low_pt_mu_resolved = [
                   'Jet_Mass',
                   'Jet_Pt',
                   'Jet_DeepFlavB',
                   #'Muon_Pt',
                   'Muon_Dxy',
                   'Muon_DxyErr',
                   'Muon_Dz',
                   'Muon_DzErr',
                   'Muon_MiniIso',
                   'Muon_Iso04',
                   #'Muon_Over_Jet_Pt',
                   'Top_Mass',
                   'Top_Pt',
                   'Top2_Mass',
                   #'Top2_Pt',
                   #'Top_mT',
                   #'Top_Relative_Pt',
                   'Top_Costheta',
                   'Top_dR',
                   ]

    high_pt_el_resolved = [
                       'Jet_Mass',
                       'Jet_Pt',
                       'Jet_DeepFlavB',
                       'Electron_Dxy',
                       #'Electron_DxyErr',
                       'Electron_Dz',
                       #'Electron_DzErr',
                       'Electron_MiniIso',
                       'Electron_Iso03',
                       'Top_Mass',
                       'Top2_Mass',
                       'Top_mT',
                       #'Top_Jet_Unboosted_Pt',
                       #'Top_Lep_Unboosted_Pt',
                       'Top_Relative_Pt',
                       #'Top_Costheta',
                       'Top_dR'
                       ]

    high_pt_mu_resolved = [
                       #'MET',
                       'Jet_Mass',
                       'Jet_DeepFlavB',
                       'Muon_Dxy',
                       #'Muon_Dz',
                       'Muon_MiniIso',
                       'Muon_Iso04',
                       'Top_Mass',
                       'Top2_Mass',
                       'Top_mT',
                       #'Top_Jet_Unboosted_Pt',
                       #'Top_Lep_Unboosted_Pt',
                       'Top_Relative_Pt',
                       'Top_dR'
                       ]

    high_pt_el_merged = [
                       #'MET',
                       'Jet_Mass',
                       'Jet_DeepFlavB',
                       'Electron_Dxy',
                       'Electron_Dz',                    
                       'Electron_MiniIso',
                       'Electron_Iso03',                      
                       'Electron_Over_Jet_Pt',
                       'Top_Mass',                                        
                       'Top_mT',
                       'Top_Relative_Pt',
                       'Top_dR'
                       ]

    high_pt_mu_merged = [
                       'Jet_Mass',
                       'Jet_DeepFlavB',
                       'Muon_Dxy',
                       'Muon_Dz',
                       'Muon_MiniIso',
                       'Muon_Iso04',
                       #'Muon_Over_Jet_Pt',
                       'Top_Mass',
                       'Top_Pt',
                       'Top_mT',
                       'Top_Relative_Pt',
                       'Top_Costheta',
                       #'Top_dR'
                       ]



    dic = {
        'high_pt': {
            'Electrons' : True,
            'Muons' : True,
            'enable_merged' : True,
            'enable_resolved' : False,
            'preselection_el': 'Tau_High_Truth==0',
            'preselection_mu': 'Tau_High_Truth==0',
            'bin' : 'Top_Pt>=500',
            'variables_el_resolved': high_pt_el_resolved,
            'variables_el_merged': high_pt_el_merged,
            'variables_mu_resolved': high_pt_mu_resolved,
            'variables_mu_merged': high_pt_mu_merged,
            'threshold_el_merged' : .6,
            'threshold_el_resolved' : .1,
            'threshold_mu_merged' : .6,
            'threshold_mu_resolved' : .1,
            'n_estimators_el_merged' : 130,
            'max_depth_el_merged' : 4,
            'min_child_weight_el_merged' : 5,
            'reg_alpha_el_merged' : .01,
            'n_estimators_el_resolved' : 100,
            'max_depth_el_resolved' : 4,
            'min_child_weight_el_resolved' : 4,
            'reg_alpha_el_resolved' : 1,
            'n_estimators_mu_merged' : 130,
            'max_depth_mu_merged' : 4,
            'min_child_weight_mu_merged' : 5,
            'reg_alpha_mu_merged' : .01,
            'n_estimators_mu_resolved' : 100,
            'max_depth_mu_resolved' : 4,
            'min_child_weight_mu_resolved' : 4,
            'reg_alpha_mu_resolved' : 1,
        },
        'low_pt': {
            'Electrons' : True,
            'Muons' : True,
            'enable_merged' : False,
            'enable_resolved' : False,
            'preselection_el': 'Tau_High_Truth==0',
            'preselection_mu': 'Tau_High_Truth==0',
            'bin' : 'Top_Pt<500',
            'variables_el_resolved': low_pt_el_resolved,
            'variables_el_merged': low_pt_el_merged,
            'variables_mu_resolved': low_pt_mu_resolved,
            'variables_mu_merged': low_pt_mu_merged,
            'threshold_el_merged' : .5,
            'threshold_el_resolved' : .2,
            'threshold_mu_merged' : .5,
            'threshold_mu_resolved' : .2,
            'n_estimators_el_resolved' : 150,
            'max_depth_el_resolved' : 4,
            'min_child_weight_el_resolved' : 5,
            'reg_alpha_el_resolved' : .1,
            'n_estimators_el_merged' : 130,
            'max_depth_el_merged' : 4,
            'min_child_weight_el_merged' : 4,
            'reg_alpha_el_merged' : .01,
            'n_estimators_mu_resolved' : 100,
            'max_depth_mu_resolved' : 4,
            'min_child_weight_mu_resolved' : 5,
            'reg_alpha_mu_resolved' : .01,#Better to use params. that minimize overtraining
            'n_estimators_mu_merged' : 130,
            'max_depth_mu_merged' : 4,
            'min_child_weight_mu_merged' : 4,
            'reg_alpha_mu_merged' : .01,
        },
    }

    return dic

def standard_Tprime_mu_resolved_cut():
    return '(Muon_Iso04<0.13) & (Top_Relative_Pt>22) & (Top_Mass>130) & (Jet_DeepFlavB>0.0494)'

def standard_Tprime_mu_merged_cut():
    return '(Jet_DeepFlavB>0.0494) & (Muon_Dxy<0.002) & (Muon_Dxy>-0.002) & (Top_Relative_Pt>5) & (Muon_MiniIso<0.25) & (Muon_Over_Jet_Pt<0.65)'

def standard_Tprime_el_resolved_cut():
    return '(Electron_mvanoIso90==1) & (Electron_Iso03<0.12) & (Top_Relative_Pt>22) & (Top_Mass>139) & (Jet_DeepFlavB>0.0494)'

def standard_Tprime_el_merged_cut():
    return '(Electron_MiniIso<0.1) & (Electron_mvanoIsoL==1) & (Top_Relative_Pt>5) & (Jet_DeepFlavB>0.0494) & (Electron_Over_Jet_Pt<0.6) & (Electron_Dxy<0.005) & (Electron_Dxy>-0.005)'

def pre_cut_mu():
    return '(Muon_isLoose==1) & (Muon_MiniIso<4) & (Muon_Dxy<0.02) & (Muon_Dxy>-0.02)'
    #return '(Muon_MiniIso<5) & (Muon_Dxy<0.1) & (Muon_Dxy>-0.1)'

def pre_cut_el():
    return '(Electron_mvanoIsoL==1) & (Electron_MiniIso<4) & (Electron_Dxy<0.05) & (Electron_Dxy>-0.05)'
    #return '(Electron_MiniIso<5) & (Electron_Dxy<0.1) & (Electron_Dxy>-0.1)'

def file_dir():
    return '/home/diefer/workdir/CMSSW_9_4_9/src/Wprime/WprimeAnalysis/bin/MergedTrees/'

def fetch_file_list():

    dic = {
           'Tprime_1200' : False,
           'Tprime_1800' : False,
           'Tprime_1200+1800' : True
          }

    return dic


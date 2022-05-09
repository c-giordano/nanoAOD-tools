import ROOT
import os

base_var_top = ['Lep_Over_Jet_Pt','nu_M','mT','pt_rel','Costheta','dR']
base_var_lep = ['dxy','dz','miniPFRelIso_all','pfRelIso03_all']
base_var_jet = ['mass','btagDeepFlavB']
base_var_MET = []

class training:
	def __init__(self, label, files, var_top, var_lep, var_jet, var_MET, category, lepton, pt_cut, score_cut):
		self.label = label
		self.files = files
		self.var_top = var_top
		self.var_lep = var_lep
		self.var_jet = var_jet
		self.var_MET= var_MET
		self.category = category # 1 is merged, 0 is resolved
		self.lepton = lepton # 0 is muon, 1 is electron
		self.pt_cut = pt_cut
		self.score_cut = score_cut

high=[1000,100000]
medium=[500,1000]
low=[0,500]

model_dir = '../model/JSON/true_vs_false/'
model_dir_tsa = '../model/TSA/'

#1 = high_pt_mu_merg
var_top_1 = ['nu_M','nu_pt','nu_e','e','mT','Jet_unboosted_pt','Jet_unboosted_e','Jet_unboosted_phi','Lep_unboosted_pt','Lep_unboosted_eta','Lep_unboosted_e','pt_rel','Costheta', 'dR']
var_mu_1  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso04_all','Over_Jet_Pt']
var_jet_1 = ['mass','pt','phi','btagDeepFlavB']
var_MET_1 = ['pt']

#2 = high_pt_mu_res
var_top_2 = ['nu_M','nu_pt','nu_e','M','pt','e','mT','Jet_unboosted_pt','Jet_unboosted_eta','Jet_unboosted_e','Lep_unboosted_eta','Lep_unboosted_phi','Lep_unboosted_e','pt_rel','Costheta','dR']
var_mu_2  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso04_all','Over_Jet_Pt']
var_jet_2 = ['mass','pt','btagDeepFlavB']
var_MET_2 = ['pt']

#3 = high_pt_el_merg
var_top_3 = ['nu_M','nu_pt','nu_e','e','mT','Jet_unboosted_e','Jet_unboosted_pt','Jet_unboosted_phi','Lep_unboosted_M','Lep_unboosted_pt','Lep_unboosted_phi','Lep_unboosted_eta','pt_rel','dR']
var_el_3  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso03_all','mvaFall17V1noIso',"Over_Jet_Pt"]
var_jet_3 = ['mass','pt','phi','btagDeepFlavB']
var_MET_3 = ['pt','phi']

#4 = high_pt_el_res
var_top_4 = ['nu_M','nu_pt','nu_e','M','e','mT','Jet_unboosted_e','Jet_unboosted_eta','Jet_unboosted_pt','Jet_unboosted_phi','Lep_unboosted_M','Lep_unboosted_eta','Lep_unboosted_phi', 'pt_rel','Costheta','dR']
var_el_4  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso03_all','Over_Jet_Pt']
var_jet_4 = ['mass','pt','btagDeepFlavB']
var_MET_4 = ['pt','phi']

#5 = medium_pt_mu_merg
var_top_5 = [ 'nu_M', 'nu_pt', 'nu_e', 'e', 'mT','Jet_unboosted_pt','Jet_unboosted_phi','Jet_unboosted_e','Jet_unboosted_eta','Lep_unboosted_e','Lep_unboosted_pt','Lep_unboosted_phi','pt_rel','Costheta','dR']
var_mu_5  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso04_all','Over_Jet_Pt']
var_jet_5 = ['mass','pt','phi','btagDeepFlavB']
var_MET_5 = ['pt']

#6 = medium_pt_mu_res
var_top_6 = ['nu_M','nu_pt','nu_e','M','pt','e','mT','Jet_unboosted_e','Jet_unboosted_pt','Jet_unboosted_phi','Lep_unboosted_M','Lep_unboosted_phi','Lep_unboosted_e','pt_rel','Costheta','dR']
var_mu_6  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso04_all','Over_Jet_Pt']
var_jet_6 = ['mass','pt','eta','btagDeepFlavB']
var_MET_6 = ['pt','phi']

#7 = medium_pt_el_merg
var_top_7 = [ 'nu_M', 'nu_pt','nu_e','e', 'mT','Jet_unboosted_e','Jet_unboosted_phi','Lep_unboosted_M','Lep_unboosted_eta','pt_rel', 'dR']
var_el_7  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso03_all','Over_Jet_Pt']
var_jet_7 = ['mass','pt','phi','btagDeepFlavB']
var_MET_7 = ['pt']

#8 = medium_pt_el_res
var_top_8 = ['nu_M','nu_pt','nu_e','phi','pt','e','mT','Jet_unboosted_pt','Lep_unboosted_e','Lep_unboosted_M','Lep_unboosted_phi','Lep_unboosted_pt','Lep_unboosted_eta','pt_rel','Costheta','dR']
var_el_8  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso03_all','Over_Jet_Pt']
var_jet_8 = ['mass','pt','phi','btagDeepFlavB']
var_MET_8 = ['pt','phi']

#9 = low_pt_mu_merg
var_top_9 = ['nu_M','nu_pt','nu_e','e','mT','Jet_unboosted_pt','Jet_unboosted_e','Lep_unboosted_eta','pt_rel','Costheta','dR']
var_mu_9  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso04_all','Over_Jet_Pt']
var_jet_9 = ['mass','pt','btagDeepFlavB']
var_MET_9 = ['phi']

#10 = low_pt_mu_res
var_top_10 = ['nu_M','nu_pt','nu_e','M','pt','eta','e','mT','Jet_unboosted_e','Jet_unboosted_eta','Lep_unboosted_e','Lep_unboosted_phi','pt_rel','Costheta','dR']
var_mu_10  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso04_all','Over_Jet_Pt']
var_jet_10 = ['mass','pt','eta','btagDeepFlavB']
var_MET_10 = ['phi']

#11 = low_pt_el_merg
var_top_11 = ['nu_M','nu_pt','nu_e','e','mT','Jet_unboosted_pt','Jet_unboosted_phi','Lep_unboosted_e','Lep_unboosted_eta','pt_rel','Costheta','dR']
var_el_11  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso03_all','Over_Jet_Pt']
var_jet_11 = ['mass','pt','btagDeepFlavB']
var_MET_11 = ['pt']

#12 = low_pt_el_res
var_top_12 = ['nu_M','nu_pt','nu_e','M','e','mT','Jet_unboosted_e','Lep_unboosted_M','Lep_unboosted_eta','pt_rel','Costheta','dR']
var_el_12  = ['pt','phi','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso03_all','Over_Jet_Pt']
var_jet_12 = ['mass','pt','btagDeepFlavB']
var_MET_12 = ['pt','phi']



# Arrays with score cuts for different working points

sig_eff_90 = [.15, .20, .51, .60, .15, .22, .285, .69]
bkg_rej_90 = [.2316, .0653, .3626, .0542, .4786, .0517, .4184, .1038, .0163, .0062, .0082, .0424]#da modificare !!!

#category ->   0 = resolved  ;   1 = merged
#lepton ->     0 = muon      ;   1 = electron


BDT_Wprime_high_pt_mu_merg = training("BDT_Wprime_high_pt_mu_merg", model_dir+'high_pt_mu_merged.json',var_top_1, var_mu_1, var_jet_1, var_MET_1, 1, 0 , high, bkg_rej_90[0])          #1
BDT_Wprime_high_pt_mu_res = training("BDT_Wprime_high_pt_mu_res", model_dir+'high_pt_mu_resolved.json',var_top_2, var_mu_2, var_jet_2, var_MET_2, 0, 0 , high, bkg_rej_90[1])          #2
BDT_Wprime_high_pt_el_merg = training("BDT_Wprime_high_pt_el_merg", model_dir+'high_pt_el_merged.json',var_top_3, var_el_3, var_jet_3, var_MET_3, 1, 1 , high, bkg_rej_90[2])          #3
BDT_Wprime_high_pt_el_res = training("BDT_Wprime_high_pt_el_res", model_dir+'high_pt_el_resolved.json',var_top_4, var_el_4, var_jet_4, var_MET_4, 0, 1 , high, bkg_rej_90[3] )         #4

BDT_Wprime_medium_pt_mu_merg = training("BDT_Wprime_medium_pt_mu_merg", model_dir+'medium_pt_mu_merged.json',var_top_5, var_mu_5, var_jet_5, var_MET_5, 1, 0 , medium, bkg_rej_90[4])  #5
BDT_Wprime_medium_pt_mu_res = training("BDT_Wprime_medium_pt_mu_res", model_dir+'medium_pt_mu_resolved.json',var_top_6, var_mu_6, var_jet_6, var_MET_6, 0, 0 , medium, bkg_rej_90[5])  #6
BDT_Wprime_medium_pt_el_merg = training("BDT_Wprime_medium_pt_el_merg", model_dir+'medium_pt_el_merged.json',var_top_7, var_el_7, var_jet_7, var_MET_7, 1, 1 , medium, bkg_rej_90[6])  #7
BDT_Wprime_medium_pt_el_res = training("BDT_Wprime_medium_pt_el_res", model_dir+'medium_pt_el_resolved.json',var_top_8, var_el_8, var_jet_8, var_MET_8, 0, 1 , medium, bkg_rej_90[7] ) #8

BDT_Wprime_low_pt_mu_merg = training("BDT_Wprime_low_pt_mu_merg", model_dir+'low_pt_mu_merged.json',var_top_9, var_mu_9, var_jet_9, var_MET_9, 1, 0 , low, bkg_rej_90[8])              #9
BDT_Wprime_low_pt_mu_res = training("BDT_Wprime_low_pt_mu_res", model_dir+'low_pt_mu_resolved.json',var_top_10, var_mu_10, var_jet_10, var_MET_10, 0, 0 , low, bkg_rej_90[9])         #10
BDT_Wprime_low_pt_el_merg = training("BDT_Wprime_low_pt_el_merg", model_dir+'low_pt_el_merged.json',var_top_11, var_el_11, var_jet_11, var_MET_11, 1, 1 , low, bkg_rej_90[10])         #11
BDT_Wprime_low_pt_el_res = training("BDT_Wprime_low_pt_el_res", model_dir+'low_pt_el_resolved.json',var_top_12, var_el_12, var_jet_12, var_MET_12, 0, 1 , low, bkg_rej_90[11])         #12


training_dict = {"Wprime":[BDT_Wprime_high_pt_mu_merg,     #1
                           BDT_Wprime_high_pt_mu_res,      #2
                           BDT_Wprime_high_pt_el_merg,     #3
                           BDT_Wprime_high_pt_el_res,      #4

                           BDT_Wprime_medium_pt_mu_merg,   #5                      
                           BDT_Wprime_medium_pt_mu_res,    #6
                           BDT_Wprime_medium_pt_el_merg,   #7
                           BDT_Wprime_medium_pt_el_res,    #8

                           BDT_Wprime_low_pt_mu_merg,      #9
                           BDT_Wprime_low_pt_mu_res,       #10
                           BDT_Wprime_low_pt_el_merg,      #11
                           BDT_Wprime_low_pt_el_res]}      #12



class training_topsa:
	def __init__(self, label, files, var_topsa, lepton, pt_cut, score_cut):
		self.label = label
		self.files = files
		self.var_topsa = var_topsa
		self.lepton = lepton # 0 is muon, 1 is electron
		self.pt_cut = pt_cut
		self.score_cut = score_cut


bkg_rej_wp90_topsa = [.612,       #1
                      .237,       #2
                      .476,       #3
                      .164,       #4
                      .057,       #5
                      .030        #6
]


var_topsa_1 = ['nu_pt',
               'nu_eta',
               'nu_M',
               'Lep_unboosted_M',
               'Lep_unboosted_pt',
               'Lep_unboosted_phi',
               'Lep_unboosted_eta',
               'Lep_unboosted_e',
               'Jsa_unboosted_pt',
               'Jsa_unboosted_e',
               'bRegRes',
               'btagDeepC',
               'btagDeepFlavB',
               'btagDeepFlavC',
               'cRegRes',
               'chEmEF',
               'muonSubtrFactor',
               'puIdDisc',
               'rawFactor'
               ]

var_topsa_2 = ['nu_pt',
               'nu_eta',
               'Lep_unboosted_M',
               'Lep_unboosted_pt',
               'Jsa_unboosted_pt',
               'Jsa_unboosted_e',
               'bRegCorr',
               'bRegRes',
               'btagCMVA',
               'btagDeepC',
               'btagDeepFlavC',
               'cRegCorr',
               'cRegRes',
               'chEmEF',
               'muonSubtrFactor',
               'partonFlavour',
               'puIdDisc',
               'rawFactor'
               ]

var_topsa_3 = ['nu_pt',
               'nu_eta',
               'nu_M',
               'Lep_unboosted_M',
               'Lep_unboosted_pt',
               'Lep_unboosted_phi',
               'Lep_unboosted_eta',
               'Lep_unboosted_e',
               'Jsa_unboosted_pt',
               'Jsa_unboosted_e',
               'bRegRes',
               'btagDeepC',
               'btagDeepFlavB',
               'btagDeepFlavC',
               'cRegRes',
               'chEmEF',
               'muonSubtrFactor',
               'puIdDisc',
               'rawFactor'
               ]
var_topsa_4 = ['nu_pt',
               'nu_eta',
               'Lep_unboosted_M',
               'Lep_unboosted_pt',
               'Jsa_unboosted_pt',
               'Jsa_unboosted_e',
               'bRegCorr',
               'bRegRes',
               'btagCMVA',
               'btagDeepC',
               'btagDeepFlavC',
               'cRegCorr',
               'cRegRes',
               'chEmEF',
               'muonSubtrFactor',
               'partonFlavour',
               'puIdDisc',
               'rawFactor'
               ]
var_topsa_5 = ['nu_pt',
               'nu_eta',
               'nu_M',
               'Lep_unboosted_M',
               'Lep_unboosted_pt',
               'Lep_unboosted_phi',
               'Lep_unboosted_eta',
               'Lep_unboosted_e',
               'Jsa_unboosted_pt',
               'Jsa_unboosted_e',
               'bRegCorr',
               'muonSubtrFactor',
               'partonFlavour'
               ]
var_topsa_6 = [ 'nu_pt',
                'nu_M',
                'Lep_unboosted_M',
                'Lep_unboosted_pt',
                'Lep_unboosted_e',
                'Jsa_unboosted_pt',
                'Jsa_unboosted_e',
                'area',
                'bRegCorr',
                'bRegRes',
                'btagCMVA',
                'btagCSVV2',
                'cRegCorr',
                'cRegRes',
                'chEmEF',
                'partonFlavour',
                'puIdDisc',
                'rawFactor'


]

BDT_high_pt_topstandalone_mu = training_topsa("BDT_high_pt_topstandalone_mu", model_dir_tsa + "Training_high_pt_topstandalone_el.json", var_topsa_1, 0, high, bkg_rej_wp90_topsa[0]) #1
BDT_high_pt_topstandalone_el = training_topsa("BDT_high_pt_topstandalone_el", model_dir_tsa + "Training_high_pt_topstandalone_el.json", var_topsa_2, 1, high, bkg_rej_wp90_topsa[1]) #2
BDT_medium_pt_topstandalone_mu = training_topsa("BDT_medium_pt_topstandalone_mu", model_dir_tsa + "Training_medium_pt_topstandalone_el.json", var_topsa_3, 0, medium, bkg_rej_wp90_topsa[2]) #3
BDT_medium_pt_topstandalone_el = training_topsa("BDT_medium_pt_topstandalone_el", model_dir_tsa + "Training_medium_pt_topstandalone_el.json", var_topsa_4, 1, medium, bkg_rej_wp90_topsa[3]) #4
BDT_low_pt_topstandalone_mu = training_topsa("BDT_low_pt_topstandalone_mu", model_dir_tsa + "Training_low_pt_topstandalone_el.json", var_topsa_5, 0, low, bkg_rej_wp90_topsa[4]) #5
BDT_low_pt_topstandalone_el = training_topsa("BDT_low_pt_topstandalone_el", model_dir_tsa + "Training_low_pt_topstandalone_el.json", var_topsa_6, 1, low, bkg_rej_wp90_topsa[5]) #6



training_dict_sa = {"TopSA":[BDT_high_pt_topstandalone_mu,          #1
                              BDT_high_pt_topstandalone_el,          #2
                              BDT_medium_pt_topstandalone_mu,        #3
                              BDT_medium_pt_topstandalone_el,        #4
                              BDT_low_pt_topstandalone_mu,           #5
                              BDT_low_pt_topstandalone_el]}          #6




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

high=[500,100000]
low=[0,500]

model_dir = '../model/JSON/'

#variabili 1 training
var_top1 = ['Lep_Over_Jet_Pt', 'nu_M', 'nu_pt', 'mT', 'pt_rel', 'Costheta', 'dR']
var_el1  = ['dxy','dz','miniPFRelIso_all','pfRelIso03_all']
var_jet1 = ['mass','pt','btagDeepFlavB']

#variabili 2 training
var_top2 = ['Lep_Over_Jet_Pt','nu_M','nu_pt','M','pt','mT','pt_rel','Costheta','dR']
var_el2  = ['pt','dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso03_all']
var_jet2 = ['mass','pt','btagDeepFlavB']

#variabili 3 training
var_top3 = ['Lep_Over_Jet_Pt','nu_M','mT','pt_rel','dR']
var_el3  = ['dxy','dz','miniPFRelIso_all','pfRelIso03_all']
var_jet3 = ['mass','btagDeepFlavB']

#variabili 4 training
var_top4 = ['nu_M','M','mT','pt_rel','dR']
var_el4  = ['dxy','dz','miniPFRelIso_all','pfRelIso03_all']
var_jet4 = ['mass','pt','btagDeepFlavB']

#variabili 5 training
var_top5 = ['Lep_Over_Jet_Pt', 'nu_M', 'nu_pt', 'pt_rel', 'dR']
var_mu5  = ['dxy','dz','miniPFRelIso_all','pfRelIso04_all']
var_jet5 = ['mass','btagDeepFlavB']

#variabili 6 training
var_top6 = ['nu_M','nu_pt','M','Costheta','dR']
var_mu6  = ['dxy','dxyErr','dz','dzErr','miniPFRelIso_all','pfRelIso04_all']
var_jet6 = ['mass','pt','btagDeepFlavB']

#variabili 7 training
var_top7 = ['nu_M','nu_pt','mT','pt_rel','Costheta']
var_mu7  = ['dxy','dz','miniPFRelIso_all','pfRelIso04_all']
var_jet7 = ['mass','btagDeepFlavB']

#variabili 8 training
var_top8 = ['nu_M','M','mT','pt_rel','dR']
var_mu8  = ['dxy','miniPFRelIso_all','pfRelIso04_all']
var_jet8 = ['mass','btagDeepFlavB']


# Arrays with score cuts for different working points

sig_eff_90 = [.15, .20, .51, .60, .15, .22, .285, .69]
bkg_rej_90 = [.02, .065, .175, .365, .01, .04, .025, .38]

BDT_Tprime_low_el_merg = training("BDT_Tprime_low_el_merg",model_dir+'low_pt_el_merged.json',var_top1, var_el1, var_jet1, base_var_MET, 1, 1 , low, bkg_rej_90[0])
BDT_Tprime_low_el_res = training("BDT_Tprime_low_el_res",model_dir+'low_pt_el_resolved.json',var_top2, var_el2, var_jet2, base_var_MET, 0, 1 , low, bkg_rej_90[1])
BDT_Tprime_high_el_merg = training("BDT_Tprime_high_el_merg",model_dir+'high_pt_el_merged.json',var_top3, var_el3, var_jet3, base_var_MET, 1, 1 , high, bkg_rej_90[2])
BDT_Tprime_high_el_res = training("BDT_Tprime_high_el_res",model_dir+'high_pt_el_resolved.json',var_top4, var_el4, var_jet4, base_var_MET, 0, 1 , high, bkg_rej_90[3] )
BDT_Tprime_low_mu_merg = training("BDT_Tprime_low_mu_merg",model_dir+'low_pt_mu_merged.json',var_top5, var_mu5, var_jet5, base_var_MET, 1, 0 , low, bkg_rej_90[4])
BDT_Tprime_low_mu_res = training("BDT_Tprime_low_mu_res",model_dir+'low_pt_mu_resolved.json',var_top6, var_mu6, var_jet6, base_var_MET, 0, 0 , low, bkg_rej_90[5])
BDT_Tprime_high_mu_merg = training("BDT_Tprime_high_mu_merg",model_dir+'high_pt_mu_merged.json',var_top7, var_mu7, var_jet7, base_var_MET, 1, 0 , high, bkg_rej_90[6])
BDT_Tprime_high_mu_res = training("BDT_Tprime_high_mu_res",model_dir+'high_pt_mu_resolved.json',var_top8, var_mu8, var_jet8, base_var_MET, 0, 0 , high, bkg_rej_90[7])


training_dict = {"BDT_Tprime":[BDT_Tprime_low_el_merg,BDT_Tprime_low_el_res,BDT_Tprime_high_el_merg,BDT_Tprime_high_el_res,BDT_Tprime_low_mu_merg,BDT_Tprime_low_mu_res,BDT_Tprime_high_mu_merg,BDT_Tprime_high_mu_res]}



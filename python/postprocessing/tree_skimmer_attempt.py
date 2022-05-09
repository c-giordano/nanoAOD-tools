#!/bin/env python
import os
##print(os.environ)
##print("**********************************************************************")
##print("**********************************************************************")
##print("**********************************************************************")
##print(str(os.environ.get('PYTHONPATH')))
##print(str(os.environ.get('PYTHON3PATH')))
import sys
##print("*************** This is system version info ***************************")
##print(sys.version_info)
#import platform
##print("*************** This is python version info ***************************")
##print(platform.python_version())
import ROOT
##print("Succesfully imported ROOT")
import math
import datetime
import copy
from array import array
from skimtree_utils import *
print("ok \n")
import xgboost as xgb
import numpy as np
from training import *
from samples.samples import *

print("all import are ok \n")


training = training_dict["Wprime"]
training_topsa = training_dict_sa["TopSA"]

folder = sys.argv[4]

sample = sample_dict[sys.argv[1]]
part_idx = sys.argv[2]
file_list = list(map(str, sys.argv[3].strip('[]').split(',')))

MCReco = True
DeltaFilter = True
bjetSwitch = False # True #
startTime = datetime.datetime.now()
print("Starting running at " + str(startTime))

ROOT.gROOT.SetBatch()

#leadingjet_ptcut = 150.

chain = ROOT.TChain('Events')

for infile in file_list: 
    print("Adding %s to the chain" %(infile))
    chain.Add(infile)
print("Number of events in chain " + str(chain.GetEntries()))
print("Number of events in tree from chain " + str((chain.GetTree()).GetEntries()))
tree = InputTree(chain)
isMC = True
scenarios = ["nominal", "jesUp", "jesDown", "jerUp", "jerDown"] 
if ('Data' in sample.label):
    isMC = False
    scenarios = ["nominal"]
MCReco = MCReco * isMC



if not os.path.exists("/eos/user/c/cgiordan/Wprime/nosynch/"+str(folder)+"/"+sample.label+"/"):
    os.makedirs("/eos/user/c/cgiordan/Wprime/nosynch/"+str(folder)+"/"+sample.label+"/")
#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
outTreeFile = ROOT.TFile("/eos/user/c/cgiordan/Wprime/nosynch/"+str(folder)+"/"+sample.label+"/"+sample.label+"_part"+str(part_idx)+".root", "RECREATE") 

# output file
trees = []
for i in range(10):
    trees.append(None)
#systZero = systWeights()
# defining the operations to be done with the systWeights class
maxSysts = 0
addPDF = True
addQ2 = False
addTopPt = False
addVHF = False
addTTSplit = False
addTopTagging = False
addWTagging = False
addTrigSF = False
nPDF = 0

systTree = systWeights()
systTree.prepareDefault(True, addQ2, addPDF, addTopPt, addVHF, addTTSplit)

for scenario in scenarios:
    systTree.addSelection(scenario)

systTree.initTreesSysts(trees, outTreeFile)
systTree.setWeightName("w_nominal",1.)
def reco(scenario, isMC, addPDF, training, training_topsa):
    isNominal = False
    if scenario == 'nominal':
        isNominal = True
    print(scenario)
    
    verbose = False
    #High Pt
    Top_pt_high_pt_mu_merg = array.array('f',[0.]) 
    Top_eta_high_pt_mu_merg = array.array('f',[0.]) 
    Top_phi_high_pt_mu_merg = array.array('f',[0.]) 
    Top_M_high_pt_mu_merg = array.array('f',[0.]) 
    Top_Score_high_pt_mu_merg = array.array('f',[0.]) 
    Top_MC_high_pt_mu_merg = array.array('i',[0]) #if isMC:
    Top_deepJetScore_high_pt_mu_merg = array.array('f',[0.])     
    bjet_pt_high_pt_mu_merg = array.array('f',[0.])
    bjet_eta_high_pt_mu_merg = array.array('f',[0.])
    bjet_phi_high_pt_mu_merg = array.array('f',[0.])
    bjet_M_high_pt_mu_merg = array.array('f',[0.])

    Top_pt_high_pt_mu_res = array.array('f',[0.]) 
    Top_eta_high_pt_mu_res = array.array('f',[0.]) 
    Top_phi_high_pt_mu_res = array.array('f',[0.]) 
    Top_M_high_pt_mu_res = array.array('f',[0.]) 
    Top_Score_high_pt_mu_res = array.array('f',[0.]) 
    Top_MC_high_pt_mu_res = array.array('i',[0]) #if isMC:
    Top_deepJetScore_high_pt_mu_res = array.array('f',[0.])     
    bjet_pt_high_pt_mu_res = array.array('f',[0.])
    bjet_eta_high_pt_mu_res = array.array('f',[0.])
    bjet_phi_high_pt_mu_res = array.array('f',[0.])
    bjet_M_high_pt_mu_res = array.array('f',[0.])

    Top_pt_high_pt_el_merg = array.array('f',[0.]) 
    Top_eta_high_pt_el_merg = array.array('f',[0.]) 
    Top_phi_high_pt_el_merg = array.array('f',[0.]) 
    Top_M_high_pt_el_merg = array.array('f',[0.]) 
    Top_Score_high_pt_el_merg = array.array('f',[0.]) 
    Top_MC_high_pt_el_merg = array.array('i',[0]) #if isMC:
    Top_deepJetScore_high_pt_el_merg = array.array('f',[0.])     
    bjet_pt_high_pt_el_merg = array.array('f',[0.])
    bjet_eta_high_pt_el_merg = array.array('f',[0.])
    bjet_phi_high_pt_el_merg = array.array('f',[0.])
    bjet_M_high_pt_el_merg = array.array('f',[0.])

    Top_pt_high_pt_el_res = array.array('f',[0.]) 
    Top_eta_high_pt_el_res = array.array('f',[0.]) 
    Top_phi_high_pt_el_res = array.array('f',[0.]) 
    Top_M_high_pt_el_res = array.array('f',[0.]) 
    Top_Score_high_pt_el_res = array.array('f',[0.]) 
    Top_MC_high_pt_el_res = array.array('i',[0]) #if isMC:
    Top_deepJetScore_high_pt_el_res = array.array('f',[0.])     
    bjet_pt_high_pt_el_res = array.array('f',[0.])
    bjet_eta_high_pt_el_res = array.array('f',[0.])
    bjet_phi_high_pt_el_res = array.array('f',[0.])
    bjet_M_high_pt_el_res = array.array('f',[0.])

    #Medium Pt
    Top_pt_medium_pt_mu_merg = array.array('f',[0.]) 
    Top_eta_medium_pt_mu_merg = array.array('f',[0.]) 
    Top_phi_medium_pt_mu_merg = array.array('f',[0.]) 
    Top_M_medium_pt_mu_merg = array.array('f',[0.]) 
    Top_Score_medium_pt_mu_merg = array.array('f',[0.]) 
    Top_MC_medium_pt_mu_merg = array.array('i',[0]) #if isMC:
    Top_deepJetScore_medium_pt_mu_merg = array.array('f',[0.])     
    bjet_pt_medium_pt_mu_merg = array.array('f',[0.])
    bjet_eta_medium_pt_mu_merg = array.array('f',[0.])
    bjet_phi_medium_pt_mu_merg = array.array('f',[0.])
    bjet_M_medium_pt_mu_merg = array.array('f',[0.])

    Top_pt_medium_pt_mu_res = array.array('f',[0.]) 
    Top_eta_medium_pt_mu_res = array.array('f',[0.]) 
    Top_phi_medium_pt_mu_res = array.array('f',[0.]) 
    Top_M_medium_pt_mu_res = array.array('f',[0.]) 
    Top_Score_medium_pt_mu_res = array.array('f',[0.]) 
    Top_MC_medium_pt_mu_res = array.array('i',[0]) #if isMC:
    Top_deepJetScore_medium_pt_mu_res = array.array('f',[0.])     
    bjet_pt_medium_pt_mu_res = array.array('f',[0.])
    bjet_eta_medium_pt_mu_res = array.array('f',[0.])
    bjet_phi_medium_pt_mu_res = array.array('f',[0.])
    bjet_M_medium_pt_mu_res = array.array('f',[0.])

    Top_pt_medium_pt_el_merg = array.array('f',[0.]) 
    Top_eta_medium_pt_el_merg = array.array('f',[0.]) 
    Top_phi_medium_pt_el_merg = array.array('f',[0.]) 
    Top_M_medium_pt_el_merg = array.array('f',[0.]) 
    Top_Score_medium_pt_el_merg = array.array('f',[0.]) 
    Top_MC_medium_pt_el_merg = array.array('i',[0]) #if isMC:
    Top_deepJetScore_medium_pt_el_merg = array.array('f',[0.])     
    bjet_pt_medium_pt_el_merg = array.array('f',[0.])
    bjet_eta_medium_pt_el_merg = array.array('f',[0.])
    bjet_phi_medium_pt_el_merg = array.array('f',[0.])
    bjet_M_medium_pt_el_merg = array.array('f',[0.])

    Top_pt_medium_pt_el_res = array.array('f',[0.]) 
    Top_eta_medium_pt_el_res = array.array('f',[0.]) 
    Top_phi_medium_pt_el_res = array.array('f',[0.]) 
    Top_M_medium_pt_el_res = array.array('f',[0.]) 
    Top_Score_medium_pt_el_res = array.array('f',[0.]) 
    Top_MC_medium_pt_el_res = array.array('i',[0]) #if isMC:
    Top_deepJetScore_medium_pt_el_res = array.array('f',[0.])     
    bjet_pt_medium_pt_el_res = array.array('f',[0.])
    bjet_eta_medium_pt_el_res = array.array('f',[0.])
    bjet_phi_medium_pt_el_res = array.array('f',[0.])
    bjet_M_medium_pt_el_res = array.array('f',[0.])

    #Low Pt
    Top_pt_low_pt_mu_merg = array.array('f',[0.]) 
    Top_eta_low_pt_mu_merg = array.array('f',[0.]) 
    Top_phi_low_pt_mu_merg = array.array('f',[0.]) 
    Top_M_low_pt_mu_merg = array.array('f',[0.]) 
    Top_Score_low_pt_mu_merg = array.array('f',[0.]) 
    Top_MC_low_pt_mu_merg = array.array('i',[0]) #if isMC:
    Top_deepJetScore_low_pt_mu_merg = array.array('f',[0.])     
    bjet_pt_low_pt_mu_merg = array.array('f',[0.])
    bjet_eta_low_pt_mu_merg = array.array('f',[0.])
    bjet_phi_low_pt_mu_merg = array.array('f',[0.])
    bjet_M_low_pt_mu_merg = array.array('f',[0.])

    Top_pt_low_pt_mu_res = array.array('f',[0.]) 
    Top_eta_low_pt_mu_res = array.array('f',[0.]) 
    Top_phi_low_pt_mu_res = array.array('f',[0.]) 
    Top_M_low_pt_mu_res = array.array('f',[0.]) 
    Top_Score_low_pt_mu_res = array.array('f',[0.]) 
    Top_MC_low_pt_mu_res = array.array('i',[0]) #if isMC:
    Top_deepJetScore_low_pt_mu_res = array.array('f',[0.])     
    bjet_pt_low_pt_mu_res = array.array('f',[0.])
    bjet_eta_low_pt_mu_res = array.array('f',[0.])
    bjet_phi_low_pt_mu_res = array.array('f',[0.])
    bjet_M_low_pt_mu_res = array.array('f',[0.])

    Top_pt_low_pt_el_merg = array.array('f',[0.]) 
    Top_eta_low_pt_el_merg = array.array('f',[0.]) 
    Top_phi_low_pt_el_merg = array.array('f',[0.]) 
    Top_M_low_pt_el_merg = array.array('f',[0.]) 
    Top_Score_low_pt_el_merg = array.array('f',[0.]) 
    Top_MC_low_pt_el_merg = array.array('i',[0]) #if isMC:
    Top_deepJetScore_low_pt_el_merg = array.array('f',[0.])     
    bjet_pt_low_pt_el_merg = array.array('f',[0.])
    bjet_eta_low_pt_el_merg = array.array('f',[0.])
    bjet_phi_low_pt_el_merg = array.array('f',[0.])
    bjet_M_low_pt_el_merg = array.array('f',[0.])

    Top_pt_low_pt_el_res = array.array('f',[0.]) 
    Top_eta_low_pt_el_res = array.array('f',[0.]) 
    Top_phi_low_pt_el_res = array.array('f',[0.]) 
    Top_M_low_pt_el_res = array.array('f',[0.]) 
    Top_Score_low_pt_el_res = array.array('f',[0.]) 
    Top_MC_low_pt_el_res = array.array('i',[0]) #if isMC:
    Top_deepJetScore_low_pt_el_res = array.array('f',[0.])     
    bjet_pt_low_pt_el_res = array.array('f',[0.])
    bjet_eta_low_pt_el_res = array.array('f',[0.])
    bjet_phi_low_pt_el_res = array.array('f',[0.])
    bjet_M_low_pt_el_res = array.array('f',[0.])


    ################STANDALONE######################

    TopSA_pt_high_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_eta_high_pt_topstandalone_mu = array.array('f',[0.])     
    TopSA_phi_high_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_M_high_pt_topstandalone_mu = array.array('f',[0.])     
    TopSA_Score_high_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_MC_high_pt_topstandalone_mu = array.array('i',[0]) 

    TopSA_pt_high_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_eta_high_pt_topstandalone_el = array.array('f',[0.])     
    TopSA_phi_high_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_M_high_pt_topstandalone_el = array.array('f',[0.])     
    TopSA_Score_high_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_MC_high_pt_topstandalone_el = array.array('i',[0]) 


    TopSA_pt_medium_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_eta_medium_pt_topstandalone_mu = array.array('f',[0.])     
    TopSA_phi_medium_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_M_medium_pt_topstandalone_mu = array.array('f',[0.])     
    TopSA_Score_medium_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_MC_medium_pt_topstandalone_mu = array.array('i',[0]) 

    TopSA_pt_medium_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_eta_medium_pt_topstandalone_el = array.array('f',[0.])     
    TopSA_phi_medium_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_M_medium_pt_topstandalone_el = array.array('f',[0.])     
    TopSA_Score_medium_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_MC_medium_pt_topstandalone_el = array.array('i',[0]) 

    TopSA_pt_low_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_eta_low_pt_topstandalone_mu = array.array('f',[0.])     
    TopSA_phi_low_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_M_low_pt_topstandalone_mu = array.array('f',[0.])     
    TopSA_Score_low_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_MC_low_pt_topstandalone_mu = array.array('i',[0]) 

    TopSA_pt_low_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_eta_low_pt_topstandalone_el = array.array('f',[0.])     
    TopSA_phi_low_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_M_low_pt_topstandalone_el = array.array('f',[0.])     
    TopSA_Score_low_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_MC_low_pt_topstandalone_el = array.array('i',[0]) 
    ######################Jet + Standalone
    TopSA_jet_pt_high_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_jet_eta_high_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_jet_phi_high_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_jet_M_high_pt_topstandalone_mu = array.array('f',[0.]) 
    
    TopSA_jet_pt_high_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_jet_eta_high_pt_topstandalone_el = array.array('f',[0.])     
    TopSA_jet_phi_high_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_jet_M_high_pt_topstandalone_el = array.array('f',[0.])     


    TopSA_jet_pt_medium_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_jet_eta_medium_pt_topstandalone_mu = array.array('f',[0.])     
    TopSA_jet_phi_medium_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_jet_M_medium_pt_topstandalone_mu = array.array('f',[0.])     

    TopSA_jet_pt_medium_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_jet_eta_medium_pt_topstandalone_el = array.array('f',[0.])     
    TopSA_jet_phi_medium_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_jet_M_medium_pt_topstandalone_el = array.array('f',[0.])     

    TopSA_jet_pt_low_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_jet_eta_low_pt_topstandalone_mu = array.array('f',[0.])     
    TopSA_jet_phi_low_pt_topstandalone_mu = array.array('f',[0.]) 
    TopSA_jet_M_low_pt_topstandalone_mu = array.array('f',[0.])     

    TopSA_jet_pt_low_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_jet_eta_low_pt_topstandalone_el = array.array('f',[0.])     
    TopSA_jet_phi_low_pt_topstandalone_el = array.array('f',[0.]) 
    TopSA_jet_M_low_pt_topstandalone_el = array.array('f',[0.])     

    bjet_pt_high_pt_topstandalone_mu = array.array('f',[0.])     
    bjet_eta_high_pt_topstandalone_mu = array.array('f',[0.])     
    bjet_phi_high_pt_topstandalone_mu = array.array('f',[0.])     
    bjet_M_high_pt_topstandalone_mu = array.array('f',[0.])     
    TopSA_deepJetScore_high_pt_topstandalone_mu = array.array('f',[0.])     

    bjet_pt_high_pt_topstandalone_el = array.array('f',[0.])     
    bjet_eta_high_pt_topstandalone_el = array.array('f',[0.])     
    bjet_phi_high_pt_topstandalone_el = array.array('f',[0.])     
    bjet_M_high_pt_topstandalone_el = array.array('f',[0.])     
    TopSA_deepJetScore_high_pt_topstandalone_el = array.array('f',[0.])     

    bjet_pt_medium_pt_topstandalone_mu = array.array('f',[0.])     
    bjet_eta_medium_pt_topstandalone_mu = array.array('f',[0.])     
    bjet_phi_medium_pt_topstandalone_mu = array.array('f',[0.])     
    bjet_M_medium_pt_topstandalone_mu = array.array('f',[0.])     
    TopSA_deepJetScore_medium_pt_topstandalone_mu = array.array('f',[0.])     

    bjet_pt_medium_pt_topstandalone_el = array.array('f',[0.])     
    bjet_eta_medium_pt_topstandalone_el = array.array('f',[0.])     
    bjet_phi_medium_pt_topstandalone_el = array.array('f',[0.])     
    bjet_M_medium_pt_topstandalone_el = array.array('f',[0.])     
    TopSA_deepJetScore_medium_pt_topstandalone_el = array.array('f',[0.])     

    bjet_pt_low_pt_topstandalone_mu = array.array('f',[0.])     
    bjet_eta_low_pt_topstandalone_mu = array.array('f',[0.])     
    bjet_phi_low_pt_topstandalone_mu = array.array('f',[0.])     
    bjet_M_low_pt_topstandalone_mu = array.array('f',[0.])     
    TopSA_deepJetScore_low_pt_topstandalone_mu = array.array('f',[0.])     

    bjet_pt_low_pt_topstandalone_el = array.array('f',[0.])     
    bjet_eta_low_pt_topstandalone_el = array.array('f',[0.])     
    bjet_phi_low_pt_topstandalone_el = array.array('f',[0.])     
    bjet_M_low_pt_topstandalone_el = array.array('f',[0.])         
    TopSA_deepJetScore_low_pt_topstandalone_el = array.array('f',[0.])     
    
    #Wprime 
    WP_M_high_pt_el_merg = array.array('f',[0.])
    WP_pt_high_pt_el_merg = array.array('f',[0.])
    WP_eta_high_pt_el_merg = array.array('f',[0.])
    WP_phi_high_pt_el_merg = array.array('f',[0.])
    
    WP_M_high_pt_el_res = array.array('f',[0.])
    WP_pt_high_pt_el_res = array.array('f',[0.])
    WP_eta_high_pt_el_res = array.array('f',[0.])
    WP_phi_high_pt_el_res = array.array('f',[0.])
    
    WP_M_high_pt_mu_merg = array.array('f',[0.])
    WP_pt_high_pt_mu_merg = array.array('f',[0.])
    WP_eta_high_pt_mu_merg = array.array('f',[0.])
    WP_phi_high_pt_mu_merg = array.array('f',[0.])
    
    WP_M_high_pt_mu_res = array.array('f',[0.])
    WP_pt_high_pt_mu_res = array.array('f',[0.])
    WP_eta_high_pt_mu_res = array.array('f',[0.])
    WP_phi_high_pt_mu_res = array.array('f',[0.])
    
    WP_M_medium_pt_el_merg = array.array('f',[0.])
    WP_pt_medium_pt_el_merg = array.array('f',[0.])
    WP_eta_medium_pt_el_merg = array.array('f',[0.])
    WP_phi_medium_pt_el_merg = array.array('f',[0.])
    
    WP_M_medium_pt_el_res = array.array('f',[0.])
    WP_pt_medium_pt_el_res = array.array('f',[0.])
    WP_eta_medium_pt_el_res = array.array('f',[0.])
    WP_phi_medium_pt_el_res = array.array('f',[0.])

    WP_M_medium_pt_mu_merg = array.array('f',[0.])
    WP_pt_medium_pt_mu_merg = array.array('f',[0.])
    WP_eta_medium_pt_mu_merg = array.array('f',[0.])
    WP_phi_medium_pt_mu_merg = array.array('f',[0.])
    
    WP_M_medium_pt_mu_res = array.array('f',[0.])
    WP_pt_medium_pt_mu_res = array.array('f',[0.])
    WP_eta_medium_pt_mu_res = array.array('f',[0.])
    WP_phi_medium_pt_mu_res = array.array('f',[0.])

    WP_M_low_pt_el_merg = array.array('f',[0.])
    WP_pt_low_pt_el_merg = array.array('f',[0.])
    WP_eta_low_pt_el_merg = array.array('f',[0.])
    WP_phi_low_pt_el_merg = array.array('f',[0.])

    WP_M_low_pt_el_res = array.array('f',[0.])
    WP_pt_low_pt_el_res = array.array('f',[0.])
    WP_eta_low_pt_el_res = array.array('f',[0.])
    WP_phi_low_pt_el_res = array.array('f',[0.])

    WP_M_low_pt_mu_merg = array.array('f',[0.])
    WP_pt_low_pt_mu_merg = array.array('f',[0.])
    WP_eta_low_pt_mu_merg = array.array('f',[0.])
    WP_phi_low_pt_mu_merg = array.array('f',[0.])

    WP_M_low_pt_mu_res = array.array('f',[0.])
    WP_pt_low_pt_mu_res = array.array('f',[0.])
    WP_eta_low_pt_mu_res = array.array('f',[0.])
    WP_phi_low_pt_mu_res = array.array('f',[0.])
    

    WP_M_high_pt_topstandalone_el = array.array('f',[0.])
    WP_pt_high_pt_topstandalone_el = array.array('f',[0.])
    WP_eta_high_pt_topstandalone_el = array.array('f',[0.])
    WP_phi_high_pt_topstandalone_el = array.array('f',[0.])

    WP_M_high_pt_topstandalone_mu = array.array('f',[0.])
    WP_pt_high_pt_topstandalone_mu = array.array('f',[0.])
    WP_eta_high_pt_topstandalone_mu = array.array('f',[0.])
    WP_phi_high_pt_topstandalone_mu = array.array('f',[0.])

    WP_M_medium_pt_topstandalone_el = array.array('f',[0.])
    WP_pt_medium_pt_topstandalone_el = array.array('f',[0.])
    WP_eta_medium_pt_topstandalone_el = array.array('f',[0.])
    WP_phi_medium_pt_topstandalone_el = array.array('f',[0.])

    WP_M_medium_pt_topstandalone_mu = array.array('f',[0.])
    WP_pt_medium_pt_topstandalone_mu = array.array('f',[0.])
    WP_eta_medium_pt_topstandalone_mu = array.array('f',[0.])
    WP_phi_medium_pt_topstandalone_mu = array.array('f',[0.])

    WP_M_low_pt_topstandalone_el = array.array('f',[0.])
    WP_pt_low_pt_topstandalone_el = array.array('f',[0.])
    WP_eta_low_pt_topstandalone_el = array.array('f',[0.])
    WP_phi_low_pt_topstandalone_el = array.array('f',[0.])

    WP_M_low_pt_topstandalone_mu = array.array('f',[0.])
    WP_pt_low_pt_topstandalone_mu = array.array('f',[0.])
    WP_eta_low_pt_topstandalone_mu = array.array('f',[0.])
    WP_phi_low_pt_topstandalone_mu = array.array('f',[0.])


    ######################MET pt

    MET_pt = array.array('f',[0.])


    w_nominal = array.array('f',[1.])

    #High pt
    systTree.branchTreesSysts(trees, scenario,"w_nominal",outTreeFile,w_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_pt_high_pt_mu_merg",outTreeFile,Top_pt_high_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_high_pt_mu_merg",outTreeFile,Top_eta_high_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_high_pt_mu_merg",outTreeFile,Top_phi_high_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_high_pt_mu_merg",outTreeFile,Top_M_high_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_high_pt_mu_merg",outTreeFile,Top_Score_high_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_high_pt_mu_merg",outTreeFile,Top_MC_high_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_high_pt_mu_merg",outTreeFile,Top_deepJetScore_high_pt_mu_merg)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_high_pt_mu_merg",outTreeFile,bjet_pt_high_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_high_pt_mu_merg",outTreeFile,bjet_eta_high_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_high_pt_mu_merg",outTreeFile,bjet_phi_high_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_high_pt_mu_merg",outTreeFile,bjet_M_high_pt_mu_merg)


    systTree.branchTreesSysts(trees, scenario,"Top_pt_high_pt_mu_res",outTreeFile,Top_pt_high_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_high_pt_mu_res",outTreeFile,Top_eta_high_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_high_pt_mu_res",outTreeFile,Top_phi_high_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_high_pt_mu_res",outTreeFile,Top_M_high_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_high_pt_mu_res",outTreeFile,Top_Score_high_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_high_pt_mu_res",outTreeFile,Top_MC_high_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_high_pt_mu_res",outTreeFile,Top_deepJetScore_high_pt_mu_res)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_high_pt_mu_res",outTreeFile,bjet_pt_high_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_high_pt_mu_res",outTreeFile,bjet_eta_high_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_high_pt_mu_res",outTreeFile,bjet_phi_high_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_high_pt_mu_res",outTreeFile,bjet_M_high_pt_mu_res)


    systTree.branchTreesSysts(trees, scenario,"Top_pt_high_pt_el_merg",outTreeFile,Top_pt_high_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_high_pt_el_merg",outTreeFile,Top_eta_high_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_high_pt_el_merg",outTreeFile,Top_phi_high_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_high_pt_el_merg",outTreeFile,Top_M_high_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_high_pt_el_merg",outTreeFile,Top_Score_high_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_high_pt_el_merg",outTreeFile,Top_MC_high_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_high_pt_el_merg",outTreeFile,Top_deepJetScore_high_pt_el_merg)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_high_pt_el_merg",outTreeFile,bjet_pt_high_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_high_pt_el_merg",outTreeFile,bjet_eta_high_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_high_pt_el_merg",outTreeFile,bjet_phi_high_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_high_pt_el_merg",outTreeFile,bjet_M_high_pt_el_merg)


    systTree.branchTreesSysts(trees, scenario,"Top_pt_high_pt_el_res",outTreeFile,Top_pt_high_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_high_pt_el_res",outTreeFile,Top_eta_high_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_high_pt_el_res",outTreeFile,Top_phi_high_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_high_pt_el_res",outTreeFile,Top_M_high_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_high_pt_el_res",outTreeFile,Top_Score_high_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_high_pt_el_res",outTreeFile,Top_MC_high_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_high_pt_el_res",outTreeFile,Top_deepJetScore_high_pt_el_res)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_high_pt_el_res",outTreeFile,bjet_pt_high_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_high_pt_el_res",outTreeFile,bjet_eta_high_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_high_pt_el_res",outTreeFile,bjet_phi_high_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_high_pt_el_res",outTreeFile,bjet_M_high_pt_el_res)


    #Medium pt
    systTree.branchTreesSysts(trees, scenario,"Top_pt_medium_pt_mu_merg",outTreeFile,Top_pt_medium_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_medium_pt_mu_merg",outTreeFile,Top_eta_medium_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_medium_pt_mu_merg",outTreeFile,Top_phi_medium_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_medium_pt_mu_merg",outTreeFile,Top_M_medium_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_medium_pt_mu_merg",outTreeFile,Top_Score_medium_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_medium_pt_mu_merg",outTreeFile,Top_MC_medium_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_medium_pt_mu_merg",outTreeFile,Top_deepJetScore_medium_pt_mu_merg)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_medium_pt_mu_merg",outTreeFile,bjet_pt_medium_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_medium_pt_mu_merg",outTreeFile,bjet_eta_medium_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_medium_pt_mu_merg",outTreeFile,bjet_phi_medium_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_medium_pt_mu_merg",outTreeFile,bjet_M_medium_pt_mu_merg)


    systTree.branchTreesSysts(trees, scenario,"Top_pt_medium_pt_mu_res",outTreeFile,Top_pt_medium_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_medium_pt_mu_res",outTreeFile,Top_eta_medium_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_medium_pt_mu_res",outTreeFile,Top_phi_medium_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_medium_pt_mu_res",outTreeFile,Top_M_medium_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_medium_pt_mu_res",outTreeFile,Top_Score_medium_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_medium_pt_mu_res",outTreeFile,Top_MC_medium_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_medium_pt_mu_res",outTreeFile,Top_deepJetScore_medium_pt_mu_res)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_medium_pt_mu_res",outTreeFile,bjet_pt_medium_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_medium_pt_mu_res",outTreeFile,bjet_eta_medium_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_medium_pt_mu_res",outTreeFile,bjet_phi_medium_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_medium_pt_mu_res",outTreeFile,bjet_M_medium_pt_mu_res)


    systTree.branchTreesSysts(trees, scenario,"Top_pt_medium_pt_el_merg",outTreeFile,Top_pt_medium_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_medium_pt_el_merg",outTreeFile,Top_eta_medium_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_medium_pt_el_merg",outTreeFile,Top_phi_medium_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_medium_pt_el_merg",outTreeFile,Top_M_medium_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_medium_pt_el_merg",outTreeFile,Top_Score_medium_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_medium_pt_el_merg",outTreeFile,Top_MC_medium_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_medium_pt_el_merg",outTreeFile,Top_deepJetScore_medium_pt_el_merg)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_medium_pt_el_merg",outTreeFile,bjet_pt_medium_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_medium_pt_el_merg",outTreeFile,bjet_eta_medium_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_medium_pt_el_merg",outTreeFile,bjet_phi_medium_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_medium_pt_el_merg",outTreeFile,bjet_M_medium_pt_el_merg)

    systTree.branchTreesSysts(trees, scenario,"Top_pt_medium_pt_el_res",outTreeFile,Top_pt_medium_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_medium_pt_el_res",outTreeFile,Top_eta_medium_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_medium_pt_el_res",outTreeFile,Top_phi_medium_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_medium_pt_el_res",outTreeFile,Top_M_medium_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_medium_pt_el_res",outTreeFile,Top_Score_medium_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_medium_pt_el_res",outTreeFile,Top_MC_medium_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_medium_pt_el_res",outTreeFile,Top_deepJetScore_medium_pt_el_res)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_medium_pt_el_res",outTreeFile,bjet_pt_medium_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_medium_pt_el_res",outTreeFile,bjet_eta_medium_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_medium_pt_el_res",outTreeFile,bjet_phi_medium_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_medium_pt_el_res",outTreeFile,bjet_M_medium_pt_el_res)


    #Low pt
    systTree.branchTreesSysts(trees, scenario,"Top_pt_low_pt_mu_merg",outTreeFile,Top_pt_low_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_low_pt_mu_merg",outTreeFile,Top_eta_low_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_low_pt_mu_merg",outTreeFile,Top_phi_low_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_low_pt_mu_merg",outTreeFile,Top_M_low_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_low_pt_mu_merg",outTreeFile,Top_Score_low_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_low_pt_mu_merg",outTreeFile,Top_MC_low_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_low_pt_mu_merg",outTreeFile,Top_deepJetScore_low_pt_mu_merg)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_low_pt_mu_merg",outTreeFile,bjet_pt_low_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_low_pt_mu_merg",outTreeFile,bjet_eta_low_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_low_pt_mu_merg",outTreeFile,bjet_phi_low_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_low_pt_mu_merg",outTreeFile,bjet_M_low_pt_mu_merg)

    systTree.branchTreesSysts(trees, scenario,"Top_pt_low_pt_mu_res",outTreeFile,Top_pt_low_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_low_pt_mu_res",outTreeFile,Top_eta_low_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_low_pt_mu_res",outTreeFile,Top_phi_low_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_low_pt_mu_res",outTreeFile,Top_M_low_pt_mu_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_low_pt_mu_res",outTreeFile,Top_Score_low_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_low_pt_mu_res",outTreeFile,Top_MC_low_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_low_pt_mu_res",outTreeFile,Top_deepJetScore_low_pt_mu_res)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_low_pt_mu_res",outTreeFile,bjet_pt_low_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_low_pt_mu_res",outTreeFile,bjet_eta_low_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_low_pt_mu_res",outTreeFile,bjet_phi_low_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_low_pt_mu_res",outTreeFile,bjet_M_low_pt_mu_res)

    systTree.branchTreesSysts(trees, scenario,"Top_pt_low_pt_el_merg",outTreeFile,Top_pt_low_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_low_pt_el_merg",outTreeFile,Top_eta_low_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_low_pt_el_merg",outTreeFile,Top_phi_low_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_low_pt_el_merg",outTreeFile,Top_M_low_pt_el_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_low_pt_el_merg",outTreeFile,Top_Score_low_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_low_pt_el_merg",outTreeFile,Top_MC_low_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_low_pt_el_merg",outTreeFile,Top_deepJetScore_low_pt_el_merg)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_low_pt_el_merg",outTreeFile,bjet_pt_low_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_low_pt_el_merg",outTreeFile,bjet_eta_low_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_low_pt_el_merg",outTreeFile,bjet_phi_low_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_low_pt_el_merg",outTreeFile,bjet_M_low_pt_el_merg)

    systTree.branchTreesSysts(trees, scenario,"Top_pt_low_pt_el_res",outTreeFile,Top_pt_low_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_low_pt_el_res",outTreeFile,Top_eta_low_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_low_pt_el_res",outTreeFile,Top_phi_low_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_low_pt_el_res",outTreeFile,Top_M_low_pt_el_res) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_low_pt_el_res",outTreeFile,Top_Score_low_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_low_pt_el_res",outTreeFile,Top_MC_low_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"Top_deepJetScore_low_pt_el_res",outTreeFile,Top_deepJetScore_low_pt_el_res)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_low_pt_el_res",outTreeFile,bjet_pt_low_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_low_pt_el_res",outTreeFile,bjet_eta_low_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_low_pt_el_res",outTreeFile,bjet_phi_low_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_low_pt_el_res",outTreeFile,bjet_M_low_pt_el_res)

    #####################################STANDALONE#######################################
    systTree.branchTreesSysts(trees, scenario,"TopSA_pt_high_pt_topstandalone_mu",outTreeFile,TopSA_pt_high_pt_topstandalone_mu) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_eta_high_pt_topstandalone_mu",outTreeFile,TopSA_eta_high_pt_topstandalone_mu)     
    systTree.branchTreesSysts(trees, scenario,"TopSA_phi_high_pt_topstandalone_mu",outTreeFile,TopSA_phi_high_pt_topstandalone_mu) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_M_high_pt_topstandalone_mu",outTreeFile,TopSA_M_high_pt_topstandalone_mu)     
    systTree.branchTreesSysts(trees, scenario,"TopSA_Score_high_pt_topstandalone_mu",outTreeFile,TopSA_Score_high_pt_topstandalone_mu) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_MC_high_pt_topstandalone_mu",outTreeFile,TopSA_MC_high_pt_topstandalone_mu)

    systTree.branchTreesSysts(trees, scenario,"TopSA_pt_high_pt_topstandalone_el",outTreeFile,TopSA_pt_high_pt_topstandalone_el) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_eta_high_pt_topstandalone_el",outTreeFile,TopSA_eta_high_pt_topstandalone_el)     
    systTree.branchTreesSysts(trees, scenario,"TopSA_phi_high_pt_topstandalone_el",outTreeFile,TopSA_phi_high_pt_topstandalone_el) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_M_high_pt_topstandalone_el",outTreeFile,TopSA_M_high_pt_topstandalone_el)     
    systTree.branchTreesSysts(trees, scenario,"TopSA_Score_high_pt_topstandalone_el",outTreeFile,TopSA_Score_high_pt_topstandalone_el) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_MC_high_pt_topstandalone_el",outTreeFile,TopSA_MC_high_pt_topstandalone_el)


    systTree.branchTreesSysts(trees, scenario,"TopSA_pt_medium_pt_topstandalone_mu",outTreeFile,TopSA_pt_medium_pt_topstandalone_mu) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_eta_medium_pt_topstandalone_mu",outTreeFile,TopSA_eta_medium_pt_topstandalone_mu)    
    systTree.branchTreesSysts(trees, scenario,"TopSA_phi_medium_pt_topstandalone_mu",outTreeFile,TopSA_phi_medium_pt_topstandalone_mu) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_M_medium_pt_topstandalone_mu",outTreeFile,TopSA_M_medium_pt_topstandalone_mu)     
    systTree.branchTreesSysts(trees, scenario,"TopSA_Score_medium_pt_topstandalone_mu",outTreeFile,TopSA_Score_medium_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_MC_medium_pt_topstandalone_mu",outTreeFile,TopSA_MC_medium_pt_topstandalone_mu)

    systTree.branchTreesSysts(trees, scenario,"TopSA_pt_medium_pt_topstandalone_el",outTreeFile,TopSA_pt_medium_pt_topstandalone_el) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_eta_medium_pt_topstandalone_el",outTreeFile,TopSA_eta_medium_pt_topstandalone_el)    
    systTree.branchTreesSysts(trees, scenario,"TopSA_phi_medium_pt_topstandalone_el",outTreeFile,TopSA_phi_medium_pt_topstandalone_el) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_M_medium_pt_topstandalone_el",outTreeFile,TopSA_M_medium_pt_topstandalone_el)     
    systTree.branchTreesSysts(trees, scenario,"TopSA_Score_medium_pt_topstandalone_el",outTreeFile,TopSA_Score_medium_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_MC_medium_pt_topstandalone_el",outTreeFile,TopSA_MC_medium_pt_topstandalone_el)

    systTree.branchTreesSysts(trees, scenario,"TopSA_pt_low_pt_topstandalone_mu",outTreeFile,TopSA_pt_low_pt_topstandalone_mu) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_eta_low_pt_topstandalone_mu",outTreeFile,TopSA_eta_low_pt_topstandalone_mu)     
    systTree.branchTreesSysts(trees, scenario,"TopSA_phi_low_pt_topstandalone_mu",outTreeFile,TopSA_phi_low_pt_topstandalone_mu) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_M_low_pt_topstandalone_mu",outTreeFile,TopSA_M_low_pt_topstandalone_mu)     
    systTree.branchTreesSysts(trees, scenario,"TopSA_Score_low_pt_topstandalone_mu",outTreeFile,TopSA_Score_low_pt_topstandalone_mu) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_MC_low_pt_topstandalone_mu",outTreeFile,TopSA_MC_low_pt_topstandalone_mu)

    systTree.branchTreesSysts(trees, scenario,"TopSA_pt_low_pt_topstandalone_el",outTreeFile,TopSA_pt_low_pt_topstandalone_el) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_eta_low_pt_topstandalone_el",outTreeFile,TopSA_eta_low_pt_topstandalone_el)     
    systTree.branchTreesSysts(trees, scenario,"TopSA_phi_low_pt_topstandalone_el",outTreeFile,TopSA_phi_low_pt_topstandalone_el) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_M_low_pt_topstandalone_el",outTreeFile,TopSA_M_low_pt_topstandalone_el)     
    systTree.branchTreesSysts(trees, scenario,"TopSA_Score_low_pt_topstandalone_el",outTreeFile,TopSA_Score_low_pt_topstandalone_el) 
    systTree.branchTreesSysts(trees, scenario,"TopSA_MC_low_pt_topstandalone_el",outTreeFile,TopSA_Score_low_pt_topstandalone_el)


    systTree.branchTreesSysts(trees, scenario,"WP_M_high_pt_el_merg",outTreeFile,WP_M_high_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_high_pt_el_merg",outTreeFile,WP_pt_high_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_high_pt_el_merg",outTreeFile,WP_eta_high_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_high_pt_el_merg",outTreeFile,WP_phi_high_pt_el_merg)

    systTree.branchTreesSysts(trees, scenario,"WP_M_high_pt_el_res",outTreeFile,WP_M_high_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_high_pt_el_res",outTreeFile,WP_pt_high_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_high_pt_el_res",outTreeFile,WP_eta_high_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_high_pt_el_res",outTreeFile,WP_phi_high_pt_el_res)

    systTree.branchTreesSysts(trees, scenario,"WP_M_high_pt_mu_merg",outTreeFile,WP_M_high_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_high_pt_mu_merg",outTreeFile,WP_pt_high_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_high_pt_mu_merg",outTreeFile,WP_eta_high_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_high_pt_mu_merg",outTreeFile,WP_phi_high_pt_mu_merg)

    systTree.branchTreesSysts(trees, scenario,"WP_M_high_pt_mu_res",outTreeFile,WP_M_high_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_high_pt_mu_res",outTreeFile,WP_pt_high_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_high_pt_mu_res",outTreeFile,WP_eta_high_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_high_pt_mu_res",outTreeFile,WP_phi_high_pt_mu_res)


    systTree.branchTreesSysts(trees, scenario,"WP_M_medium_pt_el_merg",outTreeFile,WP_M_medium_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_medium_pt_el_merg",outTreeFile,WP_pt_medium_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_medium_pt_el_merg",outTreeFile,WP_eta_medium_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_medium_pt_el_merg",outTreeFile,WP_phi_medium_pt_el_merg)

    systTree.branchTreesSysts(trees, scenario,"WP_M_medium_pt_el_res",outTreeFile,WP_M_medium_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_medium_pt_el_res",outTreeFile,WP_pt_medium_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_medium_pt_el_res",outTreeFile,WP_eta_medium_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_medium_pt_el_res",outTreeFile,WP_phi_medium_pt_el_res)

    systTree.branchTreesSysts(trees, scenario,"WP_M_medium_pt_mu_merg",outTreeFile,WP_M_medium_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_medium_pt_mu_merg",outTreeFile,WP_pt_medium_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_medium_pt_mu_merg",outTreeFile,WP_eta_medium_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_medium_pt_mu_merg",outTreeFile,WP_phi_medium_pt_mu_merg)

    systTree.branchTreesSysts(trees, scenario,"WP_M_medium_pt_mu_res",outTreeFile,WP_M_medium_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_medium_pt_mu_res",outTreeFile,WP_pt_medium_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_medium_pt_mu_res",outTreeFile,WP_eta_medium_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_medium_pt_mu_res",outTreeFile,WP_phi_medium_pt_mu_res)

    systTree.branchTreesSysts(trees, scenario,"WP_M_low_pt_el_merg",outTreeFile,WP_M_low_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_low_pt_el_merg",outTreeFile,WP_pt_low_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_low_pt_el_merg",outTreeFile,WP_eta_low_pt_el_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_low_pt_el_merg",outTreeFile,WP_phi_low_pt_el_merg)

    systTree.branchTreesSysts(trees, scenario,"WP_M_low_pt_el_res",outTreeFile,WP_M_low_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_low_pt_el_res",outTreeFile,WP_pt_low_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_low_pt_el_res",outTreeFile,WP_eta_low_pt_el_res)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_low_pt_el_res",outTreeFile,WP_phi_low_pt_el_res)

    systTree.branchTreesSysts(trees, scenario,"WP_M_low_pt_mu_merg",outTreeFile,WP_M_low_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_low_pt_mu_merg",outTreeFile,WP_pt_low_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_low_pt_mu_merg",outTreeFile,WP_eta_low_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_low_pt_mu_merg",outTreeFile,WP_phi_low_pt_mu_merg)

    systTree.branchTreesSysts(trees, scenario,"WP_M_low_pt_mu_res",outTreeFile,WP_M_low_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_low_pt_mu_res",outTreeFile,WP_pt_low_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_low_pt_mu_res",outTreeFile,WP_eta_low_pt_mu_res)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_low_pt_mu_res",outTreeFile,WP_phi_low_pt_mu_res)


    systTree.branchTreesSysts(trees, scenario,"WP_M_high_pt_topstandalone_el", outTreeFile,WP_M_high_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_high_pt_topstandalone_el", outTreeFile,WP_pt_high_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_high_pt_topstandalone_el", outTreeFile,WP_eta_high_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_high_pt_topstandalone_el", outTreeFile,WP_phi_high_pt_topstandalone_el)

    systTree.branchTreesSysts(trees, scenario,"WP_M_high_pt_topstandalone_mu",outTreeFile,WP_M_high_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_high_pt_topstandalone_mu", outTreeFile,WP_pt_high_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_high_pt_topstandalone_mu", outTreeFile,WP_eta_high_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_high_pt_topstandalone_mu", outTreeFile,WP_phi_high_pt_topstandalone_mu)

    systTree.branchTreesSysts(trees, scenario,"WP_M_medium_pt_topstandalone_el",outTreeFile,WP_M_medium_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_medium_pt_topstandalone_el", outTreeFile,WP_pt_medium_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_medium_pt_topstandalone_el", outTreeFile,WP_eta_medium_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_medium_pt_topstandalone_el", outTreeFile,WP_phi_medium_pt_topstandalone_el)

    systTree.branchTreesSysts(trees, scenario,"WP_M_medium_pt_topstandalone_mu",outTreeFile,WP_M_medium_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_medium_pt_topstandalone_mu", outTreeFile,WP_pt_medium_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_medium_pt_topstandalone_mu", outTreeFile,WP_eta_medium_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_medium_pt_topstandalone_mu", outTreeFile,WP_phi_medium_pt_topstandalone_mu)

    systTree.branchTreesSysts(trees, scenario,"WP_M_low_pt_topstandalone_el",outTreeFile,WP_M_low_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_low_pt_topstandalone_el", outTreeFile,WP_pt_low_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_low_pt_topstandalone_el", outTreeFile,WP_eta_low_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_low_pt_topstandalone_el", outTreeFile,WP_phi_low_pt_topstandalone_el)

    systTree.branchTreesSysts(trees, scenario,"WP_M_low_pt_topstandalone_mu",outTreeFile,WP_M_low_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"WP_pt_low_pt_topstandalone_mu", outTreeFile,WP_pt_low_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"WP_eta_low_pt_topstandalone_mu", outTreeFile,WP_eta_low_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"WP_phi_low_pt_topstandalone_mu", outTreeFile,WP_phi_low_pt_topstandalone_mu)


    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_pt_high_pt_topstandalone_mu",outTreeFile,TopSA_jet_pt_high_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_eta_high_pt_topstandalone_mu",outTreeFile,TopSA_jet_eta_high_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_phi_high_pt_topstandalone_mu",outTreeFile,TopSA_jet_phi_high_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_M_high_pt_topstandalone_mu",outTreeFile,TopSA_jet_M_high_pt_topstandalone_mu)

    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_pt_high_pt_topstandalone_el",outTreeFile,TopSA_jet_pt_high_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_eta_high_pt_topstandalone_el",outTreeFile,TopSA_jet_eta_high_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_phi_high_pt_topstandalone_el",outTreeFile,TopSA_jet_phi_high_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_M_high_pt_topstandalone_el",outTreeFile,TopSA_jet_M_high_pt_topstandalone_el)


    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_pt_medium_pt_topstandalone_mu",outTreeFile,TopSA_jet_pt_medium_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_eta_medium_pt_topstandalone_mu",outTreeFile,TopSA_jet_eta_medium_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_phi_medium_pt_topstandalone_mu",outTreeFile,TopSA_jet_phi_medium_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_M_medium_pt_topstandalone_mu",outTreeFile,TopSA_jet_M_medium_pt_topstandalone_mu)

    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_pt_medium_pt_topstandalone_el",outTreeFile,TopSA_jet_pt_medium_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_eta_medium_pt_topstandalone_el",outTreeFile,TopSA_jet_eta_medium_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_phi_medium_pt_topstandalone_el",outTreeFile,TopSA_jet_phi_medium_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_M_medium_pt_topstandalone_el",outTreeFile,TopSA_jet_M_medium_pt_topstandalone_el)


    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_pt_low_pt_topstandalone_mu",outTreeFile,TopSA_jet_pt_low_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_eta_low_pt_topstandalone_mu",outTreeFile,TopSA_jet_eta_low_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_phi_low_pt_topstandalone_mu",outTreeFile,TopSA_jet_phi_low_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_M_low_pt_topstandalone_mu",outTreeFile,TopSA_jet_M_low_pt_topstandalone_mu)

    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_pt_low_pt_topstandalone_el",outTreeFile,TopSA_jet_pt_low_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_eta_low_pt_topstandalone_el",outTreeFile,TopSA_jet_eta_low_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_phi_low_pt_topstandalone_el",outTreeFile,TopSA_jet_phi_low_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_jet_M_low_pt_topstandalone_el",outTreeFile,TopSA_jet_M_low_pt_topstandalone_el)

    #outTreeFile


    #b-jets for SA category
    systTree.branchTreesSysts(trees, scenario,"bjet_pt_high_pt_topstandalone_mu",outTreeFile,bjet_pt_high_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_high_pt_topstandalone_mu",outTreeFile,bjet_eta_high_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_high_pt_topstandalone_mu",outTreeFile,bjet_phi_high_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_high_pt_topstandalone_mu",outTreeFile,bjet_M_high_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_deepJetScore_high_pt_topstandalone_mu",outTreeFile,TopSA_deepJetScore_high_pt_topstandalone_mu)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_high_pt_topstandalone_el",outTreeFile,bjet_pt_high_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_high_pt_topstandalone_el",outTreeFile,bjet_eta_high_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_high_pt_topstandalone_el",outTreeFile,bjet_phi_high_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_high_pt_topstandalone_el",outTreeFile,bjet_M_high_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_deepJetScore_high_pt_topstandalone_el",outTreeFile,TopSA_deepJetScore_high_pt_topstandalone_el)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_medium_pt_topstandalone_mu",outTreeFile,bjet_pt_medium_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_medium_pt_topstandalone_mu",outTreeFile,bjet_eta_medium_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_medium_pt_topstandalone_mu",outTreeFile,bjet_phi_medium_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_medium_pt_topstandalone_mu",outTreeFile,bjet_M_medium_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_deepJetScore_medium_pt_topstandalone_mu",outTreeFile,TopSA_deepJetScore_medium_pt_topstandalone_mu)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_medium_pt_topstandalone_el",outTreeFile,bjet_pt_medium_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_medium_pt_topstandalone_el",outTreeFile,bjet_eta_medium_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_medium_pt_topstandalone_el",outTreeFile,bjet_phi_medium_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_medium_pt_topstandalone_el",outTreeFile,bjet_M_medium_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_deepJetScore_medium_pt_topstandalone_el",outTreeFile,TopSA_deepJetScore_medium_pt_topstandalone_el)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_low_pt_topstandalone_mu",outTreeFile,bjet_pt_low_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_low_pt_topstandalone_mu",outTreeFile,bjet_eta_low_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_low_pt_topstandalone_mu",outTreeFile,bjet_phi_low_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_low_pt_topstandalone_mu",outTreeFile,bjet_M_low_pt_topstandalone_mu)
    systTree.branchTreesSysts(trees, scenario,"TopSA_deepJetScore_low_pt_topstandalone_mu",outTreeFile,TopSA_deepJetScore_low_pt_topstandalone_mu)

    systTree.branchTreesSysts(trees, scenario,"bjet_pt_low_pt_topstandalone_el",outTreeFile,bjet_pt_low_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"bjet_eta_low_pt_topstandalone_el",outTreeFile,bjet_eta_low_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"bjet_phi_low_pt_topstandalone_el",outTreeFile,bjet_phi_low_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"bjet_M_low_pt_topstandalone_el",outTreeFile,bjet_M_low_pt_topstandalone_el)
    systTree.branchTreesSysts(trees, scenario,"TopSA_deepJetScore_low_pt_topstandalone_el",outTreeFile,TopSA_deepJetScore_low_pt_topstandalone_el)

    systTree.branchTreesSysts(trees, scenario,"MET_pt",outTreeFile,MET_pt)

    

    h_genweight = ROOT.TH1F("h_genweight", "h_genweight", 1, -0.5, 0.5)

    #N=200
    N= tree.GetEntries()
    h_genweight.SetBinContent(1, N)

    outTreeFile.cd()
    h_genweight.Write()
    
    


    #for i in range(tree.GetEntries()):
    for i in range(N):
        event = Event(tree,i)    
        jets = Collection(event, "Jet")             # jets[j1].btagDeepFlavB  ---> medium discriminant cut = 0.2783
        tops = Collection(event,"Top")
        met = Object(event, "MET")
        electron = Collection(event, "Electron")
        muon = Collection(event, "Muon")
        topsa = Collection(event, "TopSA")
        genpart = Collection(event, "GenPart")
        nelectron = len(electron)
        nmuon = len(muon)
        ntop = len(tops)
        #ntopsa = len(topsa)
        fatjets = Collection(event,"FatJet")
        Met_pt = met.pt
        if i%100 == 0:
            print("Processed ", i+1, " out of ", tree.GetEntries(), " events")
        
        
        w_nominal[0]= 1.

        # requiring mtt < 700 to merge inclusive tt with the mtt > 700
        if('TT_incl' in sample.label or 'TT_semilep_2018' in sample.label or 'TT_SemiLep_2017' in sample.label):
            top_q4 = ROOT.TLorentzVector()
            antitop_q4 = ROOT.TLorentzVector()
            tt_q4 = ROOT.TLorentzVector()
            
            for genp in genpart:
                if(genp.genPartIdxMother == 0 and genp.pdgId == 6):
                    top_q4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
                elif(genp.genPartIdxMother == 0 and genp.pdgId == -6):
                    antitop_q4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
            tt_q4 = top_q4 + antitop_q4
            if(tt_q4.M() > 700.):
                w_nominal[0] *= 0 #trick to make the events with mtt > 700 count zero
                continue

    
        
        Top_high_pt_mu_merg_momentum = ROOT.TLorentzVector()
        Top_high_pt_mu_res_momentum = ROOT.TLorentzVector()
        Top_high_pt_el_merg_momentum = ROOT.TLorentzVector()
        Top_high_pt_el_res_momentum = ROOT.TLorentzVector()
        Top_medium_pt_mu_merg_momentum = ROOT.TLorentzVector()
        Top_medium_pt_mu_res_momentum = ROOT.TLorentzVector()
        Top_medium_pt_el_merg_momentum = ROOT.TLorentzVector()
        Top_medium_pt_el_res_momentum = ROOT.TLorentzVector()
        Top_low_pt_mu_merg_momentum = ROOT.TLorentzVector()
        Top_low_pt_mu_res_momentum = ROOT.TLorentzVector()
        Top_low_pt_el_merg_momentum = ROOT.TLorentzVector()
        Top_low_pt_el_res_momentum = ROOT.TLorentzVector()
        
        TopSA_high_pt_topstandalone_mu_momentum = ROOT.TLorentzVector()
        TopSA_high_pt_topstandalone_el_momentum = ROOT.TLorentzVector()
        TopSA_medium_pt_topstandalone_mu_momentum = ROOT.TLorentzVector()
        TopSA_medium_pt_topstandalone_el_momentum = ROOT.TLorentzVector()
        TopSA_low_pt_topstandalone_mu_momentum = ROOT.TLorentzVector()
        TopSA_low_pt_topstandalone_el_momentum = ROOT.TLorentzVector()

        
        bjet_high_pt_mu_merg_momentum = ROOT.TLorentzVector()
        WP_momentum = ROOT.TLorentzVector()
        WP_momentum_2 = ROOT.TLorentzVector()

        all_coll=[]
        all_coll_wp90=[]
        all_coll_sa = []
        all_coll_sa_wp90 = []
        allTops = list(filter(lambda x : x.pt>=(-100), tops))
        allJets = list(filter(lambda x : x.pt>=(-100) , jets))
        goodJets = list(filter(lambda x : x.pt>=(30) , jets))
        
        bjets, nobjets = bjet_filter(allJets, 'DeepFlv', 'M')
        bjets_score = []

        allJsa_el = list(filter(lambda x : (x.chEmEF!=0), jets))
        allJsa_mu = list(filter(lambda x : (x.muEF!=0) , jets))
        bJsa_el, nobJsa_el = bjet_filter(allJsa_el, 'DeepFlv', 'M')
        bJsa_mu, nobJsa_mu = bjet_filter(allJsa_mu, 'DeepFlv', 'M')

        

        #if sys.argv[4]=='Standard':
        for train in training:
            new_coll=[]
            new_coll_wp90=[]
            score=[]
            score_=-999
            clf = xgb.XGBClassifier()
            clf.load_model(train.files)
            if train.lepton == 1:
                good_top = list(filter(lambda x: 
                                       (x.nu_pt>= train.pt_cut[0]) and (x.nu_pt<train.pt_cut[1])
                                       and (x.Is_dR_merg == train.category)
                                       and (x.el_index != -1) and (electron[x.el_index].mvaFall17V2noIso_WPL==1)
                                       and (electron[x.el_index].miniPFRelIso_all<4) and (abs(electron[x.el_index].dxy)<0.5)
                                       ,tops))
                                       
                is_el=True
            else:
                good_top = list(filter(lambda x: 
                                       (x.nu_pt>= train.pt_cut[0]) and (x.nu_pt<train.pt_cut[1])
                                       and (x.Is_dR_merg == train.category)
                                       and (x.mu_index != -1) and (muon[x.mu_index].looseId==1)
                                       and (muon[x.mu_index].miniPFRelIso_all<5) and (abs(muon[x.mu_index].dxy)<0.5)
                                       ,tops))
                is_el=False



            for top in good_top:
                lista=[]
                score_=-999
                for m in train.var_MET: lista.append(met[m])
                MET_pt[0] = (met.pt)
                #print(MET_pt)
                for j in train.var_jet: lista.append(jets[int(top.bjet_index)][j])
                if is_el:
                    for el in train.var_lep: 
                        if(el=="Over_Jet_Pt"):
                            lista.append(electron[int(top.el_index)].pt/jets[int(top.bjet_index)].pt)
                        else:
                            lista.append(electron[int(top.el_index)][el])

                    #close_el, dRmin_el = closest(top, goodbJets)
                    if(verbose):print("dRmin_el is ", dRmin_el)
                else:
                    for mu in train.var_lep: 
                        if(mu=="Over_Jet_Pt"):
                            lista.append(muon[int(top.mu_index)].pt/jets[int(top.bjet_index)].pt)
                        else:
                            lista.append(muon[int(top.mu_index)][mu])

                    #close_mu, dRmin_mu = closest(top, goodbJets)
                    if(verbose):print("dRmin_mu is ", dRmin_mu)

                for t in train.var_top:  
                    if(t=="mT"):
                        mttemp=math.sqrt(top.pt*met.pt*2*(1-math.cos(deltaPhi(met.phi,top.phi))))
                        lista.append(mttemp) 
                    else:
                        lista.append(top[t]) 
                        
                



                X = np.array([lista,])

                score_ = clf.predict_proba(X)[0, 1]                
                score.append(score_)
                new_coll.append([top,score_])
                #print("score: ",score)
                #print(train.score_cut," for ", train.label)
                if (score_>train.score_cut):
                    #print("Appending done correctly")
                    new_coll_wp90.append([top,score_])

                    

            if(len(new_coll)>0): 
                new_coll =  [x for _,x in sorted(zip([new_coll[i][-1] for i in range(len(score))],new_coll))]
                new_coll.reverse()
                if(len(new_coll_wp90)>0):
                    new_coll_wp90 =  [x for _,x in sorted(zip([new_coll_wp90[i][-1] for i in range(len(new_coll_wp90))],new_coll_wp90))]
                    new_coll_wp90.reverse()

            all_coll = all_coll +  new_coll
            all_coll_wp90 = all_coll_wp90 + new_coll_wp90


            if(len(new_coll_wp90)>0):
                goodbJets = list(filter(lambda x: x.pt>=30 and allJets.index(x)!=new_coll_wp90[0][0].bjet_index , bjets))
                bjet_momentum = ROOT.TLorentzVector()
                if (len(goodbJets)>0):
                    bjet_momentum.SetPtEtaPhiM(goodbJets[0].pt,goodbJets[0].eta,goodbJets[0].phi, goodbJets[0].mass)
                    for j in goodbJets:
                        bjets_score = j.btagDeepFlavB
                else:
                    bjet_momentum.SetPtEtaPhiM(0,0,0,0)

            ######################  HIGH PT  ########################
            if (train.label)=='BDT_Wprime_high_pt_mu_merg':
                #print("ENter ", train.label)
                if (len(new_coll_wp90)>0):
                    Top_pt_high_pt_mu_merg[0] = new_coll_wp90[0][0].nu_pt
                    #print("Top_pt for ",train.label," ", Top_pt_high_pt_mu_merg[0])
                    Top_eta_high_pt_mu_merg[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_high_pt_mu_merg[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_high_pt_mu_merg[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_high_pt_mu_merg[0] = new_coll_wp90[0][1]
                    
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_high_pt_mu_merg[0] = 1
                    else:
                        Top_MC_high_pt_mu_merg[0] = 0

                    Top_high_pt_mu_merg_momentum.SetPtEtaPhiM(Top_pt_high_pt_mu_merg[0], Top_eta_high_pt_mu_merg[0], Top_phi_high_pt_mu_merg[0], Top_M_high_pt_mu_merg[0])
                    if (len(goodbJets)>0):

                        WP_momentum = Top_high_pt_mu_merg_momentum + bjet_momentum
                        WP_M_high_pt_mu_merg[0]=(WP_momentum.M())
                        WP_pt_high_pt_mu_merg[0]=(WP_momentum.Pt())
                        WP_eta_high_pt_mu_merg[0]=(WP_momentum.Eta())
                        WP_phi_high_pt_mu_merg[0]=(WP_momentum.Phi())
                        Top_deepJetScore_high_pt_mu_merg[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_high_pt_mu_merg[0] = (bjet_momentum.Pt())
                        bjet_eta_high_pt_mu_merg[0] = (bjet_momentum.Eta())
                        bjet_phi_high_pt_mu_merg[0] = (bjet_momentum.Phi())
                        bjet_M_high_pt_mu_merg[0] = (bjet_momentum.M())
                        #print("bjet_pt_high_pt_mu_merg", bjet_pt_high_pt_mu_merg[0])
                        #print("bjet_eta_high_pt_mu_merg", bjet_eta_high_pt_mu_merg[0])
                        #print("bjet_phi_high_pt_mu_merg", bjet_phi_high_pt_mu_merg[0])
                        #print("bjet_M_high_pt_mu_merg", bjet_M_high_pt_mu_merg[0])
                    else:
                        WP_M_high_pt_mu_merg[0]=-999.
                        WP_pt_high_pt_mu_merg[0]=-999.
                        WP_eta_high_pt_mu_merg[0]=-999.
                        WP_phi_high_pt_mu_merg[0]=-999.
                        Top_deepJetScore_high_pt_mu_merg[0] = -999.
                        bjet_pt_high_pt_mu_merg[0] = -999.
                        bjet_eta_high_pt_mu_merg[0] = -999.
                        bjet_phi_high_pt_mu_merg[0] = -999.
                        bjet_M_high_pt_mu_merg[0] = -999.
                        #print("bjet_M_high_pt_mu_merg", bjet_M_high_pt_mu_merg[0])
                else:
                    WP_M_high_pt_mu_merg[0]=-999.
                    WP_pt_high_pt_mu_merg[0]=-999.
                    WP_eta_high_pt_mu_merg[0]=-999.
                    WP_phi_high_pt_mu_merg[0]=-999.
                    Top_pt_high_pt_mu_merg[0] = -999.
                    Top_eta_high_pt_mu_merg[0] = -999.
                    Top_phi_high_pt_mu_merg[0] = -999.
                    Top_M_high_pt_mu_merg[0] = -999.
                    Top_Score_high_pt_mu_merg[0] = -999
                    Top_deepJetScore_high_pt_mu_merg[0] = -999.
                    bjet_pt_high_pt_mu_merg[0] = -999.
                    bjet_eta_high_pt_mu_merg[0] = -999.
                    bjet_phi_high_pt_mu_merg[0] = -999.
                    bjet_M_high_pt_mu_merg[0] = -999.
                    #print("bjet_pt_high_pt_mu_merg", bjet_pt_high_pt_mu_merg[0])
                    #print("bjet_eta_high_pt_mu_merg", bjet_eta_high_pt_mu_merg[0])
                    #print("bjet_phi_high_pt_mu_merg", bjet_phi_high_pt_mu_merg[0])
                    #print("bjet_M_high_pt_mu_merg", bjet_M_high_pt_mu_merg[0])

            if (train.label)=='BDT_Wprime_high_pt_mu_res':
                if (len(new_coll_wp90)>0):
                    Top_pt_high_pt_mu_res[0] = new_coll_wp90[0][0].nu_pt
                    #print("Top_pt for ",train.label," ", Top_pt_high_pt_mu_res[0])
                    Top_eta_high_pt_mu_res[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_high_pt_mu_res[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_high_pt_mu_res[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_high_pt_mu_res[0] = new_coll_wp90[0][1]
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_high_pt_mu_res[0] = 1
                    else:
                    
                        Top_MC_high_pt_mu_res[0] = 0

                    Top_high_pt_mu_res_momentum.SetPtEtaPhiM(Top_pt_high_pt_mu_res[0], Top_eta_high_pt_mu_res[0], Top_phi_high_pt_mu_res[0], Top_M_high_pt_mu_res[0])
                    if (len(goodbJets)>0):
                        WP_momentum = Top_high_pt_mu_res_momentum + bjet_momentum
                        WP_M_high_pt_mu_res[0]=(WP_momentum.M())
                        WP_pt_high_pt_mu_res[0]=(WP_momentum.Pt())
                        WP_eta_high_pt_mu_res[0]=(WP_momentum.Eta())
                        WP_phi_high_pt_mu_res[0]=(WP_momentum.Phi())
                        Top_deepJetScore_high_pt_mu_res[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_high_pt_mu_res[0] = (bjet_momentum.Pt())
                        bjet_eta_high_pt_mu_res[0] = (bjet_momentum.Eta())
                        bjet_phi_high_pt_mu_res[0] = (bjet_momentum.Phi())
                        bjet_M_high_pt_mu_res[0] = (bjet_momentum.M())
                        #print("bjet_pt_high_pt_mu_res", bjet_pt_high_pt_mu_res[0])
                        #print("bjet_eta_high_pt_mu_res", bjet_eta_high_pt_mu_res[0])
                        #print("bjet_phi_high_pt_mu_res", bjet_phi_high_pt_mu_res[0])
                        #print("bjet_M_high_pt_mu_res", bjet_M_high_pt_mu_res[0])

                        #print("bjet_M_high_pt_mu_res", bjet_M_high_pt_mu_res[0])
                    else:
                        WP_M_high_pt_mu_res[0]=-999.
                        WP_pt_high_pt_mu_res[0]=-999.
                        WP_eta_high_pt_mu_res[0]=-999.
                        WP_phi_high_pt_mu_res[0]=-999.
                        Top_deepJetScore_high_pt_mu_res[0] = -999.
                        bjet_pt_high_pt_mu_res[0] = -999.
                        bjet_eta_high_pt_mu_res[0] = -999.
                        bjet_phi_high_pt_mu_res[0] = -999.
                        bjet_M_high_pt_mu_res[0] = -999.
                else:
                    WP_M_high_pt_mu_res[0]=-999.
                    WP_pt_high_pt_mu_res[0]=-999.
                    WP_eta_high_pt_mu_res[0]=-999.
                    WP_phi_high_pt_mu_res[0]=-999.
                    Top_pt_high_pt_mu_res[0] = -999.
                    Top_eta_high_pt_mu_res[0] = -999.
                    Top_phi_high_pt_mu_res[0] = -999.
                    Top_M_high_pt_mu_res[0] = -999.
                    Top_Score_high_pt_mu_res[0] = -999
                    Top_deepJetScore_high_pt_mu_res[0] = -999.
                    bjet_pt_high_pt_mu_res[0] = -999.
                    bjet_eta_high_pt_mu_res[0] = -999.
                    bjet_phi_high_pt_mu_res[0] = -999.
                    bjet_M_high_pt_mu_res[0] = -999.
                    #print("bjet_pt_high_pt_mu_res", bjet_pt_high_pt_mu_res[0])
                    #print("bjet_eta_high_pt_mu_res", bjet_eta_high_pt_mu_res[0])
                    #print("bjet_phi_high_pt_mu_res", bjet_phi_high_pt_mu_res[0])
                    #print("bjet_M_high_pt_mu_res", bjet_M_high_pt_mu_res[0])



            if (train.label)=='BDT_Wprime_high_pt_el_merg':
                if (len(new_coll_wp90)>0):
                    Top_pt_high_pt_el_merg[0] = new_coll_wp90[0][0].nu_pt
                    Top_eta_high_pt_el_merg[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_high_pt_el_merg[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_high_pt_el_merg[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_high_pt_el_merg[0] = new_coll_wp90[0][1]
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_high_pt_el_merg[0] = 1
                    else:
                        Top_MC_high_pt_el_merg[0] = 0

                    Top_high_pt_el_merg_momentum.SetPtEtaPhiM(Top_pt_high_pt_el_merg[0], Top_eta_high_pt_el_merg[0], Top_phi_high_pt_el_merg[0], Top_M_high_pt_el_merg[0])
                    if (len(goodbJets)>0):
                        if(verbose):print(len(goodbJets))
                        WP_momentum = Top_high_pt_el_merg_momentum + bjet_momentum
                        WP_M_high_pt_el_merg[0]=(WP_momentum.M())
                        WP_pt_high_pt_el_merg[0]=(WP_momentum.Pt())
                        WP_eta_high_pt_el_merg[0]=(WP_momentum.Eta())
                        WP_phi_high_pt_el_merg[0]=(WP_momentum.Phi())
                        Top_deepJetScore_high_pt_el_merg[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_high_pt_el_merg[0] = (bjet_momentum.Pt())
                        bjet_eta_high_pt_el_merg[0] = (bjet_momentum.Eta())
                        bjet_phi_high_pt_el_merg[0] = (bjet_momentum.Phi())
                        bjet_M_high_pt_el_merg[0] = (bjet_momentum.M())
                    else:
                        WP_M_high_pt_el_merg[0]=-999.
                        WP_pt_high_pt_el_merg[0]=-999.
                        WP_eta_high_pt_el_merg[0]=-999.
                        WP_phi_high_pt_el_merg[0]=-999.
                        Top_deepJetScore_high_pt_el_merg[0] = -999.
                        bjet_pt_high_pt_el_merg[0] = -999.
                        bjet_eta_high_pt_el_merg[0] = -999.
                        bjet_phi_high_pt_el_merg[0] = -999.
                        bjet_M_high_pt_el_merg[0] = -999.

                else:
                    WP_M_high_pt_el_merg[0]=-999.
                    WP_pt_high_pt_el_merg[0]=-999.
                    WP_eta_high_pt_el_merg[0]=-999.
                    WP_phi_high_pt_el_merg[0]=-999.
                    Top_pt_high_pt_el_merg[0] = -999.
                    Top_eta_high_pt_el_merg[0] = -999.
                    Top_phi_high_pt_el_merg[0] = -999.
                    Top_M_high_pt_el_merg[0] = -999.
                    Top_Score_high_pt_el_merg[0] = -999
                    Top_deepJetScore_high_pt_el_merg[0] = -999.
                    bjet_pt_high_pt_el_merg[0] = -999.
                    bjet_eta_high_pt_el_merg[0] = -999.
                    bjet_phi_high_pt_el_merg[0] = -999.
                    bjet_M_high_pt_el_merg[0] = -999.
                    #print("bjet_pt_high_pt_el_merg", bjet_pt_high_pt_el_merg[0])
                    #print("bjet_eta_high_pt_el_merg", bjet_eta_high_pt_el_merg[0])
                    #print("bjet_phi_high_pt_el_merg", bjet_phi_high_pt_el_merg[0])
                    #print("bjet_M_high_pt_el_merg", bjet_M_high_pt_el_merg[0])


            if (train.label)=='BDT_Wprime_high_pt_el_res':
                if (len(new_coll_wp90)>0):
                    Top_pt_high_pt_el_res[0] = new_coll_wp90[0][0].nu_pt
                    Top_eta_high_pt_el_res[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_high_pt_el_res[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_high_pt_el_res[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_high_pt_el_res[0] = new_coll_wp90[0][1]
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_high_pt_el_res[0] = 1
                    else:
                        Top_MC_high_pt_el_res[0] = 0
                    
                    Top_high_pt_el_res_momentum.SetPtEtaPhiM(Top_pt_high_pt_el_res[0], Top_eta_high_pt_el_res[0], Top_phi_high_pt_el_res[0], Top_M_high_pt_el_res[0])
                    if (len(goodbJets)>0):
                        WP_momentum = Top_high_pt_el_res_momentum + bjet_momentum
                        WP_M_high_pt_el_res[0]=(WP_momentum.M())
                        WP_pt_high_pt_el_res[0]=(WP_momentum.Pt())
                        WP_eta_high_pt_el_res[0]=(WP_momentum.Eta())
                        WP_phi_high_pt_el_res[0]=(WP_momentum.Phi())
                        Top_deepJetScore_high_pt_el_res[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_high_pt_el_res[0] = (bjet_momentum.Pt())
                        bjet_eta_high_pt_el_res[0] = (bjet_momentum.Eta())
                        bjet_phi_high_pt_el_res[0] = (bjet_momentum.Phi())
                        bjet_M_high_pt_el_res[0] = (bjet_momentum.M())
                        #print("bjet_M_high_pt_el_res", bjet_M_high_pt_el_res[0])

                    else:
                        WP_M_high_pt_el_res[0]=-999.
                        WP_pt_high_pt_el_res[0]=-999.
                        WP_eta_high_pt_el_res[0]=-999.
                        WP_phi_high_pt_el_res[0]=-999.
                        Top_deepJetScore_high_pt_el_res[0] = -999.
                        bjet_pt_high_pt_el_res[0] = -999.
                        bjet_eta_high_pt_el_res[0] =-999.
                        bjet_phi_high_pt_el_res[0] =  -999.
                        bjet_M_high_pt_el_res[0] =  -999.

                else:
                    WP_M_high_pt_el_res[0]=-999.
                    WP_pt_high_pt_el_res[0]=-999.
                    WP_eta_high_pt_el_res[0]=-999.
                    WP_phi_high_pt_el_res[0]=-999.
                    Top_pt_high_pt_el_res[0] = -999.
                    Top_eta_high_pt_el_res[0] = -999. 
                    Top_phi_high_pt_el_res[0] = -999.
                    Top_M_high_pt_el_res[0] = -999.
                    Top_Score_high_pt_el_res[0] = -999
                    Top_deepJetScore_high_pt_el_res[0] = -999.
                    bjet_pt_high_pt_el_res[0] = -999.
                    bjet_eta_high_pt_el_res[0] =-999.
                    bjet_phi_high_pt_el_res[0] =  -999.
                    bjet_M_high_pt_el_res[0] =  -999.


            #####################  MEDIUM PT  ######################
            if (train.label)=='BDT_Wprime_medium_pt_mu_merg':
                if (len(new_coll_wp90)>0):
                    Top_pt_medium_pt_mu_merg[0] = new_coll_wp90[0][0].nu_pt
                    Top_eta_medium_pt_mu_merg[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_medium_pt_mu_merg[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_medium_pt_mu_merg[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_medium_pt_mu_merg[0] = new_coll_wp90[0][1]
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_medium_pt_mu_merg[0] = 1
                    else:
                        Top_MC_medium_pt_mu_merg[0] = 0
       
                    Top_medium_pt_mu_merg_momentum.SetPtEtaPhiM(Top_pt_medium_pt_mu_merg[0], Top_eta_medium_pt_mu_merg[0], Top_phi_medium_pt_mu_merg[0], Top_M_medium_pt_mu_merg[0])
                    if (len(goodbJets)>0):
                        WP_momentum = Top_medium_pt_mu_merg_momentum + bjet_momentum
                        WP_M_medium_pt_mu_merg[0]=(WP_momentum.M())
                        WP_pt_medium_pt_mu_merg[0]=(WP_momentum.Pt())
                        WP_eta_medium_pt_mu_merg[0]=(WP_momentum.Eta())
                        WP_phi_medium_pt_mu_merg[0]=(WP_momentum.Phi())
                        Top_deepJetScore_medium_pt_mu_merg[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_medium_pt_mu_merg[0] = (bjet_momentum.Pt())
                        bjet_eta_medium_pt_mu_merg[0] = (bjet_momentum.Eta())
                        bjet_phi_medium_pt_mu_merg[0] = (bjet_momentum.Phi())
                        bjet_M_medium_pt_mu_merg[0] = (bjet_momentum.M())

                    else:
                        WP_M_medium_pt_mu_merg[0]=-999.
                        WP_pt_medium_pt_mu_merg[0]=-999.
                        WP_eta_medium_pt_mu_merg[0]=-999.
                        WP_phi_medium_pt_mu_merg[0]=-999.
                        Top_deepJetScore_medium_pt_mu_merg[0] = -999.
                        bjet_pt_medium_pt_mu_merg[0] = -999.
                        bjet_eta_medium_pt_mu_merg[0] = -999.
                        bjet_phi_medium_pt_mu_merg[0] = -999.
                        bjet_M_medium_pt_mu_merg[0] = -999.

       
                else:
                    WP_M_medium_pt_mu_merg[0]=-999.
                    WP_pt_medium_pt_mu_merg[0]=-999.
                    WP_eta_medium_pt_mu_merg[0]=-999.
                    WP_phi_medium_pt_mu_merg[0]=-999.
                    Top_pt_medium_pt_mu_merg[0] = -999.
                    Top_eta_medium_pt_mu_merg[0] = -999.
                    Top_phi_medium_pt_mu_merg[0] = -999.
                    Top_M_medium_pt_mu_merg[0] = -999.
                    Top_Score_medium_pt_mu_merg[0] = -999
                    Top_deepJetScore_medium_pt_mu_merg[0] = -999.
                    bjet_pt_medium_pt_mu_merg[0] = -999.
                    bjet_eta_medium_pt_mu_merg[0] = -999.
                    bjet_phi_medium_pt_mu_merg[0] = -999.
                    bjet_M_medium_pt_mu_merg[0] = -999.


            if (train.label)=='BDT_Wprime_medium_pt_mu_res':
                if (len(new_coll_wp90)>0):
                    Top_pt_medium_pt_mu_res[0] = new_coll_wp90[0][0].nu_pt
                    Top_eta_medium_pt_mu_res[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_medium_pt_mu_res[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_medium_pt_mu_res[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_medium_pt_mu_res[0] = new_coll_wp90[0][1]
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_medium_pt_mu_res[0] = 1
                    else:
                        Top_MC_medium_pt_mu_res[0] = 0
       
                    Top_medium_pt_mu_res_momentum.SetPtEtaPhiM(Top_pt_medium_pt_mu_res[0], Top_eta_medium_pt_mu_res[0], Top_phi_medium_pt_mu_res[0], Top_M_medium_pt_mu_res[0])
                    if (len(goodbJets)>0):
                        WP_momentum = Top_medium_pt_mu_res_momentum + bjet_momentum
                        WP_M_medium_pt_mu_res[0]=(WP_momentum.M())
                        WP_pt_medium_pt_mu_res[0]=(WP_momentum.Pt())
                        WP_eta_medium_pt_mu_res[0]=(WP_momentum.Eta())
                        WP_phi_medium_pt_mu_res[0]=(WP_momentum.Phi())

                        Top_deepJetScore_medium_pt_mu_res[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_medium_pt_mu_res[0] = (bjet_momentum.Pt())
                        bjet_eta_medium_pt_mu_res[0] = (bjet_momentum.Eta())
                        bjet_phi_medium_pt_mu_res[0] = (bjet_momentum.Phi())
                        bjet_M_medium_pt_mu_res[0] = (bjet_momentum.M())

                    else:
                        WP_M_medium_pt_mu_res[0]=-999.
                        WP_pt_medium_pt_mu_res[0]=-999.
                        WP_eta_medium_pt_mu_res[0]=-999.
                        WP_phi_medium_pt_mu_res[0]=-999.

                        Top_deepJetScore_medium_pt_mu_res[0]= -999.
                        bjet_pt_medium_pt_mu_res[0] = -999.
                        bjet_eta_medium_pt_mu_res[0] = -999.
                        bjet_phi_medium_pt_mu_res[0] = -999.
                        bjet_M_medium_pt_mu_res[0] = -999.
       
                else:
                    WP_M_medium_pt_mu_res[0]=-999.
                    WP_pt_medium_pt_mu_res[0]=-999.
                    WP_eta_medium_pt_mu_res[0]=-999.
                    WP_phi_medium_pt_mu_res[0]=-999.

                    Top_pt_medium_pt_mu_res[0] = -999.
                    Top_eta_medium_pt_mu_res[0] = -999.
                    Top_phi_medium_pt_mu_res[0] = -999.
                    Top_M_medium_pt_mu_res[0] = -999.
                    Top_Score_medium_pt_mu_res[0] = -999
                    Top_deepJetScore_medium_pt_mu_res[0]= -999.
                    bjet_pt_medium_pt_mu_res[0] = -999.
                    bjet_eta_medium_pt_mu_res[0] = -999.
                    bjet_phi_medium_pt_mu_res[0] = -999.
                    bjet_M_medium_pt_mu_res[0] = -999.


            if (train.label)=='BDT_Wprime_medium_pt_el_merg':
                if (len(new_coll_wp90)>0):
                    Top_pt_medium_pt_el_merg[0] = new_coll_wp90[0][0].nu_pt
                    Top_eta_medium_pt_el_merg[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_medium_pt_el_merg[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_medium_pt_el_merg[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_medium_pt_el_merg[0] = new_coll_wp90[0][1]
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_medium_pt_el_merg[0] = 1
                    else:
                        Top_MC_medium_pt_el_merg[0] = 0
                    
                    Top_medium_pt_el_merg_momentum.SetPtEtaPhiM(Top_pt_medium_pt_el_merg[0], Top_eta_medium_pt_el_merg[0], Top_phi_medium_pt_el_merg[0], Top_M_medium_pt_el_merg[0])
                    if (len(goodbJets)>0):
                        WP_momentum = Top_medium_pt_el_merg_momentum + bjet_momentum
                        WP_M_medium_pt_el_merg[0]=(WP_momentum.M())
                        WP_pt_medium_pt_el_merg[0]=(WP_momentum.Pt())
                        WP_eta_medium_pt_el_merg[0]=(WP_momentum.Eta())
                        WP_phi_medium_pt_el_merg[0]=(WP_momentum.Phi())

                        Top_deepJetScore_medium_pt_el_merg[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_medium_pt_el_merg[0] = (bjet_momentum.Pt())
                        bjet_eta_medium_pt_el_merg[0] = (bjet_momentum.Eta())
                        bjet_phi_medium_pt_el_merg[0] = (bjet_momentum.Phi())
                        bjet_M_medium_pt_el_merg[0] = (bjet_momentum.M())

                    else:
                        WP_M_medium_pt_el_merg[0]=-999.
                        WP_pt_medium_pt_el_merg[0]=-999.
                        WP_eta_medium_pt_el_merg[0]=-999.
                        WP_phi_medium_pt_el_merg[0]=-999.

                        Top_deepJetScore_medium_pt_el_merg[0] = -999.
                        bjet_pt_medium_pt_el_merg[0] = -999.
                        bjet_eta_medium_pt_el_merg[0] = -999.
                        bjet_phi_medium_pt_el_merg[0] = -999.
                        bjet_M_medium_pt_el_merg[0] = -999.
                    
                else:
                    WP_M_medium_pt_el_merg[0]=-999.
                    WP_pt_medium_pt_el_merg[0]=-999.
                    WP_eta_medium_pt_el_merg[0]=-999.
                    WP_phi_medium_pt_el_merg[0]=-999.
                    Top_pt_medium_pt_el_merg[0] = -999.
                    Top_eta_medium_pt_el_merg[0] = -999.
                    Top_phi_medium_pt_el_merg[0] = -999.
                    Top_M_medium_pt_el_merg[0] = -999.
                    Top_Score_medium_pt_el_merg[0] = -999
                    Top_deepJetScore_medium_pt_el_merg[0] = -999.
                    bjet_pt_medium_pt_el_merg[0] = -999.
                    bjet_eta_medium_pt_el_merg[0] = -999.
                    bjet_phi_medium_pt_el_merg[0] = -999.
                    bjet_M_medium_pt_el_merg[0] = -999.
                    

            if (train.label)=='BDT_Wprime_medium_pt_el_res':
                if (len(new_coll_wp90)>0):
                    Top_pt_medium_pt_el_res[0] = new_coll_wp90[0][0].nu_pt
                    Top_eta_medium_pt_el_res[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_medium_pt_el_res[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_medium_pt_el_res[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_medium_pt_el_res[0] = new_coll_wp90[0][1]
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_medium_pt_el_res[0] = 1
                    else:
                        Top_MC_medium_pt_el_res[0] = 0
                    
                    Top_medium_pt_el_res_momentum.SetPtEtaPhiM(Top_pt_medium_pt_el_res[0], Top_eta_medium_pt_el_res[0], Top_phi_medium_pt_el_res[0], Top_M_medium_pt_el_res[0])
                    if (len(goodbJets)>0):
                        WP_momentum = Top_medium_pt_el_res_momentum + bjet_momentum
                        WP_M_medium_pt_el_res[0]=(WP_momentum.M())
                        WP_pt_medium_pt_el_res[0]=(WP_momentum.Pt())
                        WP_eta_medium_pt_el_res[0]=(WP_momentum.Eta())
                        WP_phi_medium_pt_el_res[0]=(WP_momentum.Phi())

                        Top_deepJetScore_medium_pt_el_res[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_medium_pt_el_res[0] = (bjet_momentum.Pt())
                        bjet_eta_medium_pt_el_res[0] = (bjet_momentum.Eta())
                        bjet_phi_medium_pt_el_res[0] = (bjet_momentum.Phi())
                        bjet_M_medium_pt_el_res[0] = (bjet_momentum.M())

                    else:
                        WP_M_medium_pt_el_res[0]=-999.
                        WP_pt_medium_pt_el_res[0]=-999.
                        WP_eta_medium_pt_el_res[0]=-999.
                        WP_phi_medium_pt_el_res[0]=-999.

                        Top_deepJetScore_medium_pt_el_res[0] = -999.
                        bjet_pt_medium_pt_el_res[0] = -999.
                        bjet_eta_medium_pt_el_res[0] = -999.
                        bjet_phi_medium_pt_el_res[0] = -999.
                        bjet_M_medium_pt_el_res[0] = -999.
                    
                else:
                    WP_M_medium_pt_el_res[0]=-999.
                    WP_pt_medium_pt_el_res[0]=-999.
                    WP_eta_medium_pt_el_res[0]=-999.
                    WP_phi_medium_pt_el_res[0]=-999.
                    Top_pt_medium_pt_el_res[0] = -999.
                    Top_eta_medium_pt_el_res[0] = -999. 
                    Top_phi_medium_pt_el_res[0] = -999.
                    Top_M_medium_pt_el_res[0] = -999.
                    Top_Score_medium_pt_el_res[0] = -999
                    Top_deepJetScore_medium_pt_el_res[0] = -999.
                    bjet_pt_medium_pt_el_res[0] = -999.
                    bjet_eta_medium_pt_el_res[0] = -999.
                    bjet_phi_medium_pt_el_res[0] = -999.
                    bjet_M_medium_pt_el_res[0] = -999.


            #######################  LOW PT  #########################
            if (train.label)=='BDT_Wprime_low_pt_mu_merg':
                if (len(new_coll_wp90)>0):
                    Top_pt_low_pt_mu_merg[0] = new_coll_wp90[0][0].nu_pt
                    Top_eta_low_pt_mu_merg[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_low_pt_mu_merg[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_low_pt_mu_merg[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_low_pt_mu_merg[0] = new_coll_wp90[0][1]
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_low_pt_mu_merg[0] = 1
                    else:
                        Top_MC_low_pt_mu_merg[0] = 0

                    Top_low_pt_mu_merg_momentum.SetPtEtaPhiM(Top_pt_low_pt_mu_merg[0], Top_eta_low_pt_mu_merg[0], Top_phi_low_pt_mu_merg[0], Top_M_low_pt_mu_merg[0])
                    if (len(goodbJets)>0):
                        WP_momentum = Top_low_pt_mu_merg_momentum + bjet_momentum
                        WP_M_low_pt_mu_merg[0]=(WP_momentum.M())
                        WP_pt_low_pt_mu_merg[0]=(WP_momentum.Pt())
                        WP_eta_low_pt_mu_merg[0]=(WP_momentum.Eta())
                        WP_phi_low_pt_mu_merg[0]=(WP_momentum.Phi())
                        Top_deepJetScore_low_pt_mu_merg[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_low_pt_mu_merg[0] = (bjet_momentum.Pt())
                        bjet_eta_low_pt_mu_merg[0] = (bjet_momentum.Eta())
                        bjet_phi_low_pt_mu_merg[0] = (bjet_momentum.Phi())
                        bjet_M_low_pt_mu_merg[0] = (bjet_momentum.M())

                    else:
                        WP_M_low_pt_mu_merg[0]=-999.
                        WP_pt_low_pt_mu_merg[0]=-999.
                        WP_eta_low_pt_mu_merg[0]=-999.
                        WP_phi_low_pt_mu_merg[0]=-999.

                        Top_deepJetScore_low_pt_mu_merg[0] = -999.
                        bjet_pt_low_pt_mu_merg[0] = -999.
                        bjet_eta_low_pt_mu_merg[0] = -999.
                        bjet_phi_low_pt_mu_merg[0] = -999.
                        bjet_M_low_pt_mu_merg[0] = -999.

                else:
                    WP_M_low_pt_mu_merg[0]=-999.
                    WP_pt_low_pt_mu_merg[0]=-999.
                    WP_eta_low_pt_mu_merg[0]=-999.
                    WP_phi_low_pt_mu_merg[0]=-999.
                    Top_pt_low_pt_mu_merg[0] = -999.
                    Top_eta_low_pt_mu_merg[0] = -999.
                    Top_phi_low_pt_mu_merg[0] = -999.
                    Top_M_low_pt_mu_merg[0] = -999.
                    Top_Score_low_pt_mu_merg[0] = -999
                    Top_deepJetScore_low_pt_mu_merg[0] = -999.
                    bjet_pt_low_pt_mu_merg[0] = -999.
                    bjet_eta_low_pt_mu_merg[0] = -999.
                    bjet_phi_low_pt_mu_merg[0] = -999.
                    bjet_M_low_pt_mu_merg[0] = -999.


            if (train.label)=='BDT_Wprime_low_pt_mu_res':
                if (len(new_coll_wp90)>0):
                    Top_pt_low_pt_mu_res[0] = new_coll_wp90[0][0].nu_pt
                    Top_eta_low_pt_mu_res[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_low_pt_mu_res[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_low_pt_mu_res[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_low_pt_mu_res[0] = new_coll_wp90[0][1]
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_low_pt_mu_res[0] = 1
                    else:
                        Top_MC_low_pt_mu_res[0] = 0

                    Top_low_pt_mu_res_momentum.SetPtEtaPhiM(Top_pt_low_pt_mu_res[0], Top_eta_low_pt_mu_res[0], Top_phi_low_pt_mu_res[0], Top_M_low_pt_mu_res[0])
                    if (len(goodbJets)>0):
                        WP_momentum = Top_low_pt_mu_res_momentum + bjet_momentum
                        WP_M_low_pt_mu_res[0]=(WP_momentum.M())
                        WP_pt_low_pt_mu_res[0]=(WP_momentum.Pt())
                        WP_eta_low_pt_mu_res[0]=(WP_momentum.Eta())
                        WP_phi_low_pt_mu_res[0]=(WP_momentum.Phi())
                        Top_deepJetScore_low_pt_mu_res[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_low_pt_mu_res[0] = (bjet_momentum.Pt())
                        bjet_eta_low_pt_mu_res[0] = (bjet_momentum.Eta())
                        bjet_phi_low_pt_mu_res[0] = (bjet_momentum.Phi())
                        bjet_M_low_pt_mu_res[0] = (bjet_momentum.M())

                    else:
                        WP_M_low_pt_mu_res[0]=-999.
                        WP_pt_low_pt_mu_res[0]=-999.
                        WP_eta_low_pt_mu_res[0]=-999.
                        WP_phi_low_pt_mu_res[0]=-999.
                        Top_deepJetScore_low_pt_mu_res[0] = -999.
                        bjet_pt_low_pt_mu_res[0] = -999.
                        bjet_eta_low_pt_mu_res[0] = -999.
                        bjet_phi_low_pt_mu_res[0] = -999.
                        bjet_M_low_pt_mu_res[0] = -999.

                else:
                    WP_M_low_pt_mu_res[0]=-999.
                    WP_pt_low_pt_mu_res[0]=-999.
                    WP_eta_low_pt_mu_res[0]=-999.
                    WP_phi_low_pt_mu_res[0]=-999.
                    Top_pt_low_pt_mu_res[0] = -999.
                    Top_eta_low_pt_mu_res[0] = -999.
                    Top_phi_low_pt_mu_res[0] = -999.
                    Top_M_low_pt_mu_res[0] = -999.
                    Top_Score_low_pt_mu_res[0] = -999
                    Top_deepJetScore_low_pt_mu_res[0] = -999.
                    bjet_pt_low_pt_mu_res[0] = -999.
                    bjet_eta_low_pt_mu_res[0] = -999.
                    bjet_phi_low_pt_mu_res[0] = -999.
                    bjet_M_low_pt_mu_res[0] = -999.


            if (train.label)=='BDT_Wprime_low_pt_el_merg':
                if (len(new_coll_wp90)>0):
                    Top_pt_low_pt_el_merg[0] = new_coll_wp90[0][0].nu_pt
                    Top_eta_low_pt_el_merg[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_low_pt_el_merg[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_low_pt_el_merg[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_low_pt_el_merg[0] = new_coll_wp90[0][1]
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_low_pt_el_merg[0] = 1
                    else:
                        Top_MC_low_pt_el_merg[0] = 0

                    Top_low_pt_el_merg_momentum.SetPtEtaPhiM(Top_pt_low_pt_el_merg[0], Top_eta_low_pt_el_merg[0], Top_phi_low_pt_el_merg[0], Top_M_low_pt_el_merg[0])
                    if (len(goodbJets)>0):
                        WP_momentum = Top_low_pt_el_merg_momentum + bjet_momentum
                        WP_M_low_pt_el_merg[0]=(WP_momentum.M())
                        WP_pt_low_pt_el_merg[0]=(WP_momentum.Pt())
                        WP_eta_low_pt_el_merg[0]=(WP_momentum.Eta())
                        WP_phi_low_pt_el_merg[0]=(WP_momentum.Phi())

                        Top_deepJetScore_low_pt_el_merg[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_low_pt_el_merg[0] = (bjet_momentum.Pt())
                        bjet_eta_low_pt_el_merg[0] = (bjet_momentum.Eta())
                        bjet_phi_low_pt_el_merg[0] = (bjet_momentum.Phi())
                        bjet_M_low_pt_el_merg[0] = (bjet_momentum.M())

                    else:
                        WP_M_low_pt_el_merg[0]=-999.
                        WP_pt_low_pt_el_merg[0]=-999.
                        WP_eta_low_pt_el_merg[0]=-999.
                        WP_phi_low_pt_el_merg[0]=-999.
                        Top_deepJetScore_low_pt_el_merg[0] = -999.
                        bjet_pt_low_pt_el_merg[0] = -999.
                        bjet_eta_low_pt_el_merg[0] = -999.
                        bjet_phi_low_pt_el_merg[0] = -999.
                        bjet_M_low_pt_el_merg[0] = -999.

                else:
                    WP_M_low_pt_el_merg[0]=-999.
                    WP_pt_low_pt_el_merg[0]=-999.
                    WP_eta_low_pt_el_merg[0]=-999.
                    WP_phi_low_pt_el_merg[0]=-999.
                    Top_pt_low_pt_el_merg[0] = -999.
                    Top_eta_low_pt_el_merg[0] = -999.
                    Top_phi_low_pt_el_merg[0] = -999.
                    Top_M_low_pt_el_merg[0] = -999.
                    Top_Score_low_pt_el_merg[0] = -999
                    Top_deepJetScore_low_pt_el_merg[0] = -999.
                    bjet_pt_low_pt_el_merg[0] = -999.
                    bjet_eta_low_pt_el_merg[0] = -999.
                    bjet_phi_low_pt_el_merg[0] = -999.
                    bjet_M_low_pt_el_merg[0] = -999.

                        
            if (train.label)=='BDT_Wprime_low_pt_el_res':
                if (len(new_coll_wp90)>0):
                    Top_pt_low_pt_el_res[0] = new_coll_wp90[0][0].nu_pt
                    Top_eta_low_pt_el_res[0] = new_coll_wp90[0][0].nu_eta 
                    Top_phi_low_pt_el_res[0] = new_coll_wp90[0][0].nu_phi 
                    Top_M_low_pt_el_res[0] = new_coll_wp90[0][0].nu_M 
                    Top_Score_low_pt_el_res[0] = new_coll_wp90[0][1]
                    if(new_coll_wp90[0][0].LHE_Truth==0): 
                        Top_MC_low_pt_el_res[0] = 1
                    else:
                        Top_MC_low_pt_el_res[0] = 0
                    
                    Top_low_pt_el_res_momentum.SetPtEtaPhiM(Top_pt_low_pt_el_res[0], Top_eta_low_pt_el_res[0], Top_phi_low_pt_el_res[0], Top_M_low_pt_el_res[0])
                    if (len(goodbJets)>0):
                        WP_momentum = Top_low_pt_el_res_momentum + bjet_momentum
                        WP_M_low_pt_el_res[0]=(WP_momentum.M())
                        WP_pt_low_pt_el_res[0]=(WP_momentum.Pt())
                        WP_eta_low_pt_el_res[0]=(WP_momentum.Eta())
                        WP_phi_low_pt_el_res[0]=(WP_momentum.Phi())
                        Top_deepJetScore_low_pt_el_res[0] = goodbJets[0].btagDeepFlavB
                        bjet_pt_low_pt_el_res[0] = (bjet_momentum.Pt())
                        bjet_eta_low_pt_el_res[0] = (bjet_momentum.Eta())
                        bjet_phi_low_pt_el_res[0] = (bjet_momentum.Phi())
                        bjet_M_low_pt_el_res[0] = (bjet_momentum.M())

                    else:
                        WP_M_low_pt_el_res[0]=-999.
                        WP_pt_low_pt_el_res[0]=-999.
                        WP_eta_low_pt_el_res[0]=-999.
                        WP_phi_low_pt_el_res[0]=-999.

                        Top_deepJetScore_low_pt_el_res[0] = -999.
                        bjet_pt_low_pt_el_res[0] = -999.
                        bjet_eta_low_pt_el_res[0] = -999.
                        bjet_phi_low_pt_el_res[0] = -999.
                        bjet_M_low_pt_el_res[0] = -999.

                else:
                    WP_M_low_pt_el_res[0]=-999.
                    WP_pt_low_pt_el_res[0]=-999.
                    WP_eta_low_pt_el_res[0]=-999.
                    WP_phi_low_pt_el_res[0]=-999.
                    Top_pt_low_pt_el_res[0] = -999.
                    Top_eta_low_pt_el_res[0] = -999. 
                    Top_phi_low_pt_el_res[0] = -999.
                    Top_M_low_pt_el_res[0] = -999.
                    Top_Score_low_pt_el_res[0] = -999
                    Top_deepJetScore_low_pt_el_res[0] = -999.
                    bjet_pt_low_pt_el_res[0] = -999.
                    bjet_eta_low_pt_el_res[0] = -999.
                    bjet_phi_low_pt_el_res[0] = -999.
                    bjet_M_low_pt_el_res[0] = -999.
                    

        ####################################### STANDALONE ####################################
        for train_sa in training_topsa:
            new_coll_sa=[]
            new_coll_sa_wp90=[]
            score_sa=[]
            score_sa_=-999
            clf_sa = xgb.XGBClassifier()
            clf_sa.load_model(train_sa.files)
            if train_sa.lepton == 1:
                good_topsa = list(filter(lambda x: 
                                         (x.nu_pt>= train_sa.pt_cut[0]) 
                                         and (x.nu_pt<train_sa.pt_cut[1]) 
                                         and (x.el_index != -1) ,
                                         topsa))
                
                is_el_sa=True
            else:
                good_topsa = list(filter(lambda x: 
                                         (x.nu_pt>= train_sa.pt_cut[0]) 
                                         and (x.nu_pt<train_sa.pt_cut[1]) 
                                         and (x.mu_index != -1)
                                         ,topsa))
                is_el_sa=False

            for tsa in good_topsa:
                lista_sa = []
                score_sa_=-999
                for t in train_sa.var_topsa : 
                    lista_sa.append(tsa[t])

                X = np.array([lista_sa,])
                score_sa_=clf_sa.predict_proba(X)[0,1]
                score_sa.append(score_sa_)
                new_coll_sa.append([tsa,score_sa_])
                if (score_sa_>train_sa.score_cut): 
                    new_coll_sa_wp90.append([tsa,score_sa_])
                    #print(" top sa, label ", train_sa.label," ; score: ",score_sa_," ; passing the threshold ",train_sa.score_cut )

            if(len(new_coll_sa)>0):
                new_coll_sa =  [x for _,x in sorted(zip([new_coll_sa[i][-1] for i in range(len(score_sa))],new_coll_sa))]
                new_coll_sa.reverse()
                if(len(new_coll_sa_wp90)>0):
                    new_coll_sa_wp90 =  [x for _,x in sorted(zip([new_coll_sa_wp90[i][-1] for i in range(len(new_coll_sa_wp90))],new_coll_sa_wp90))]
                    new_coll_sa_wp90.reverse()

            all_coll_sa = all_coll_sa + new_coll_sa
            all_coll_sa_wp90 = all_coll_sa_wp90 + new_coll_sa_wp90

            if(len(new_coll_sa_wp90)>0):
                goodJsa_el = list(filter(lambda x: x.pt>=30 and allJets.index(x)!=new_coll_sa_wp90[0][0].mu_index , bjets))
                goodJsa_mu = list(filter(lambda x: x.pt>=30 and allJets.index(x)!=new_coll_sa_wp90[0][0].el_index , bjets))
                bjsa_el_momentum = ROOT.TLorentzVector()
                bjsa_mu_momentum = ROOT.TLorentzVector()
                #bjsa_mu_score[0] =goodJsa_mu[0].btagDeepFlavB #Segnalibro
                
                if (len(goodJsa_el)>0):
                    bjsa_el_momentum.SetPtEtaPhiM(goodJsa_el[0].pt,goodJsa_el[0].eta,goodJsa_el[0].phi, goodJsa_el[0].mass)
                elif (len(goodJsa_mu)>0):
                    bjsa_mu_momentum.SetPtEtaPhiM(goodJsa_mu[0].pt,goodJsa_mu[0].eta,goodJsa_mu[0].phi, goodJsa_mu[0].mass)

                else: continue

                

            ###########################STANDALONE###########################################
            if (train_sa.label)=='BDT_high_pt_topstandalone_mu':
                if (len(new_coll_sa_wp90)>0):
                    TopSA_pt_high_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_pt
                    TopSA_eta_high_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_eta 
                    TopSA_phi_high_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_phi 
                    TopSA_M_high_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_M 
                    TopSA_Score_high_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][1]

                    TopSA_jet_pt_high_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                    TopSA_jet_eta_high_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                    TopSA_jet_phi_high_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                    TopSA_jet_M_high_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI

                    if(new_coll_sa_wp90[0][0].Truth==0) and (abs(jets[int(new_coll_sa_wp90[0][0].Jet_index)].partonFlavour)==5): #corretta
                        TopSA_MC_high_pt_topstandalone_mu[0] = 1
                    else:
                        TopSA_MC_high_pt_topstandalone_mu[0] = 0

                    TopSA_high_pt_topstandalone_mu_momentum.SetPtEtaPhiM(TopSA_jet_pt_high_pt_topstandalone_mu[0], TopSA_jet_eta_high_pt_topstandalone_mu[0], TopSA_jet_phi_high_pt_topstandalone_mu[0], TopSA_jet_M_high_pt_topstandalone_mu[0])
                   
                    if (len(goodJsa_mu)>0):
                        WP_momentum = TopSA_high_pt_topstandalone_mu_momentum + bjsa_mu_momentum
                        WP_M_high_pt_topstandalone_mu[0]=(WP_momentum.M())
                        WP_pt_high_pt_topstandalone_mu[0]=(WP_momentum.Pt())
                        WP_eta_high_pt_topstandalone_mu[0]=(WP_momentum.Eta())
                        WP_phi_high_pt_topstandalone_mu[0]=(WP_momentum.Phi())
                        bjet_pt_high_pt_topstandalone_mu[0]=(bjsa_mu_momentum.Pt())
                        bjet_eta_high_pt_topstandalone_mu[0]=(bjsa_mu_momentum.Eta())
                        bjet_phi_high_pt_topstandalone_mu[0]=(bjsa_mu_momentum.Phi())
                        bjet_M_high_pt_topstandalone_mu[0]=(bjsa_mu_momentum.M())
                        #print(bjet_pt_high_pt_topstandalone_mu)
                        TopSA_deepJetScore_high_pt_topstandalone_mu[0] = goodJsa_mu[0].btagDeepFlavB
                        TopSA_jet_pt_high_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                        TopSA_jet_eta_high_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                        TopSA_jet_phi_high_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                        TopSA_jet_M_high_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI
                        #print("TopSA_jet_pt_high_pt_topstandalone_mu", TopSA_jet_pt_high_pt_topstandalone_mu[0])
                        #print("TopSA_jet_eta_high_pt_topstandalone_mu", TopSA_jet_eta_high_pt_topstandalone_mu[0])
                        #print("TopSA_jet_phi_high_pt_topstandalone_mu", TopSA_jet_phi_high_pt_topstandalone_mu[0])
                        #print("TopSA_jet_M_high_pt_topstandalone_mu", TopSA_jet_M_high_pt_topstandalone_mu[0])
        
                    else:
                        WP_M_high_pt_topstandalone_mu[0]=-999.
                        WP_pt_high_pt_topstandalone_mu[0]=-999.
                        WP_eta_high_pt_topstandalone_mu[0]=-999.
                        WP_phi_high_pt_topstandalone_mu[0]=-999.
                        bjet_pt_high_pt_topstandalone_mu[0]=-999.
                        bjet_eta_high_pt_topstandalone_mu[0]=-999.
                        bjet_phi_high_pt_topstandalone_mu[0]=-999.
                        bjet_M_high_pt_topstandalone_mu[0]=-999.
                        TopSA_deepJetScore_high_pt_topstandalone_mu[0] = -999.
                        
                else:
                    WP_M_high_pt_topstandalone_mu[0]=-999.
                    WP_pt_high_pt_topstandalone_mu[0]=-999.
                    WP_eta_high_pt_topstandalone_mu[0]=-999.
                    WP_phi_high_pt_topstandalone_mu[0]=-999.
                    TopSA_pt_high_pt_topstandalone_mu[0] = -999.
                    TopSA_eta_high_pt_topstandalone_mu[0] = -999.
                    TopSA_phi_high_pt_topstandalone_mu[0] = -999.
                    TopSA_M_high_pt_topstandalone_mu[0] = -999.
                    TopSA_Score_high_pt_topstandalone_mu[0] = -999
                    TopSA_deepJetScore_high_pt_topstandalone_mu[0] = -999.

                    TopSA_jet_pt_high_pt_topstandalone_mu[0] = -999.
                    TopSA_jet_eta_high_pt_topstandalone_mu[0] = -999.
                    TopSA_jet_phi_high_pt_topstandalone_mu[0] = -999.
                    TopSA_jet_M_high_pt_topstandalone_mu[0] = -999.
                    #print("TopSA_jet_pt_high_pt_topstandalone_mu", TopSA_jet_pt_high_pt_topstandalone_mu[0])
                    #print("TopSA_jet_eta_high_pt_topstandalone_mu", TopSA_jet_eta_high_pt_topstandalone_mu[0])
                    #print("TopSA_jet_phi_high_pt_topstandalone_mu", TopSA_jet_phi_high_pt_topstandalone_mu[0])
                    #print("TopSA_jet_M_high_pt_topstandalone_mu", TopSA_jet_M_high_pt_topstandalone_mu[0])


                    bjet_pt_high_pt_topstandalone_mu[0]=-999.
                    bjet_eta_high_pt_topstandalone_mu[0]=-999.
                    bjet_phi_high_pt_topstandalone_mu[0]=-999.
                    bjet_M_high_pt_topstandalone_mu[0]=-999.
                    #print("TopSA_jet_M_high_pt_topstandalone_mu", TopSA_jet_M_high_pt_topstandalone_mu[0])
                    
            if (train_sa.label)=='BDT_high_pt_topstandalone_el':
                if (len(new_coll_sa_wp90)>0):
                    TopSA_pt_high_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_pt
                    TopSA_eta_high_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_eta 
                    TopSA_phi_high_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_phi 
                    TopSA_M_high_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_M 
                    TopSA_Score_high_pt_topstandalone_el[0] = new_coll_sa_wp90[0][1]

                    TopSA_jet_pt_high_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                    TopSA_jet_eta_high_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                    TopSA_jet_phi_high_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                    TopSA_jet_M_high_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI

                    
                    if(new_coll_sa_wp90[0][0].Truth==0) and (abs(jets[int(new_coll_sa_wp90[0][0].Jet_index)].partonFlavour)==5): #corretta 
                        TopSA_MC_high_pt_topstandalone_el[0] = 1
                    else:
                        TopSA_MC_high_pt_topstandalone_el[0] = 0

                    TopSA_high_pt_topstandalone_el_momentum.SetPtEtaPhiM(TopSA_jet_pt_high_pt_topstandalone_el[0], TopSA_jet_eta_high_pt_topstandalone_el[0], TopSA_jet_phi_high_pt_topstandalone_el[0], TopSA_jet_M_high_pt_topstandalone_el[0])
                   
                    if (len(goodJsa_el)>0):
                        WP_momentum = TopSA_high_pt_topstandalone_el_momentum + bjsa_el_momentum
                        WP_M_high_pt_topstandalone_el[0]=(WP_momentum.M())
                        WP_pt_high_pt_topstandalone_el[0]=(WP_momentum.Pt())
                        WP_eta_high_pt_topstandalone_el[0]=(WP_momentum.Eta())
                        WP_phi_high_pt_topstandalone_el[0]=(WP_momentum.Phi())

                        bjet_pt_high_pt_topstandalone_el[0]=(bjsa_el_momentum.Pt())
                        bjet_eta_high_pt_topstandalone_el[0]=(bjsa_el_momentum.Eta())
                        bjet_phi_high_pt_topstandalone_el[0]=(bjsa_el_momentum.Phi())
                        bjet_M_high_pt_topstandalone_el[0]=(bjsa_el_momentum.M())
                        TopSA_deepJetScore_high_pt_topstandalone_el[0] = goodJsa_el[0].btagDeepFlavB
                        TopSA_jet_pt_high_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                        TopSA_jet_eta_high_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                        TopSA_jet_phi_high_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                        TopSA_jet_M_high_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI

                    
                    else:
                        WP_M_high_pt_topstandalone_el[0]=-999.
                        WP_pt_high_pt_topstandalone_el[0]=-999.
                        WP_eta_high_pt_topstandalone_el[0]=-999.
                        WP_phi_high_pt_topstandalone_el[0]=-999.
                        bjet_pt_high_pt_topstandalone_el[0]=-999.
                        bjet_eta_high_pt_topstandalone_el[0]=-999.
                        bjet_phi_high_pt_topstandalone_el[0]=-999.
                        bjet_M_high_pt_topstandalone_el[0]=-999.
                        TopSA_deepJetScore_high_pt_topstandalone_el[0] = -999.
                        

                else:
                    WP_M_high_pt_topstandalone_el[0]=-999.
                    WP_pt_high_pt_topstandalone_el[0]=-999.
                    WP_eta_high_pt_topstandalone_el[0]=-999.
                    WP_phi_high_pt_topstandalone_el[0]=-999.
                    TopSA_pt_high_pt_topstandalone_el[0] = -999.
                    TopSA_eta_high_pt_topstandalone_el[0] = -999.
                    TopSA_phi_high_pt_topstandalone_el[0] = -999.
                    TopSA_M_high_pt_topstandalone_el[0] = -999.
                    TopSA_Score_high_pt_topstandalone_el[0] = -999
                    TopSA_deepJetScore_high_pt_topstandalone_el[0] = -999.

                    TopSA_jet_pt_high_pt_topstandalone_el[0] = -999.
                    TopSA_jet_eta_high_pt_topstandalone_el[0] = -999.
                    TopSA_jet_phi_high_pt_topstandalone_el[0] = -999.
                    TopSA_jet_M_high_pt_topstandalone_el[0] = -999.

                    bjet_pt_high_pt_topstandalone_el[0]=-999.
                    bjet_eta_high_pt_topstandalone_el[0]=-999.
                    bjet_phi_high_pt_topstandalone_el[0]=-999.
                    bjet_M_high_pt_topstandalone_el[0]=-999.


            if (train_sa.label)=='BDT_medium_pt_topstandalone_mu':
                if (len(new_coll_sa_wp90)>0):
                    TopSA_pt_medium_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_pt
                    TopSA_eta_medium_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_eta 
                    TopSA_phi_medium_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_phi 
                    TopSA_M_medium_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_M 
                    TopSA_Score_medium_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][1]

                    TopSA_jet_pt_medium_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                    TopSA_jet_eta_medium_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                    TopSA_jet_phi_medium_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                    TopSA_jet_M_medium_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI


                    if(new_coll_sa_wp90[0][0].Truth==0) and (abs(jets[int(new_coll_sa_wp90[0][0].Jet_index)].partonFlavour)==5): #corretta 
                        TopSA_MC_medium_pt_topstandalone_mu[0] = 1
                    else:
                        TopSA_MC_medium_pt_topstandalone_mu[0] = 0

                    TopSA_medium_pt_topstandalone_mu_momentum.SetPtEtaPhiM(TopSA_jet_pt_medium_pt_topstandalone_mu[0], TopSA_jet_eta_medium_pt_topstandalone_mu[0], TopSA_jet_phi_medium_pt_topstandalone_mu[0], TopSA_jet_M_medium_pt_topstandalone_mu[0])
                   
                    if (len(goodJsa_mu)>0):
                        WP_momentum = TopSA_medium_pt_topstandalone_mu_momentum + bjsa_mu_momentum
                        WP_M_medium_pt_topstandalone_mu[0]=(WP_momentum.M())
                        WP_pt_medium_pt_topstandalone_mu[0]=(WP_momentum.Pt())
                        WP_eta_medium_pt_topstandalone_mu[0]=(WP_momentum.Eta())
                        WP_phi_medium_pt_topstandalone_mu[0]=(WP_momentum.Phi())

                        bjet_pt_medium_pt_topstandalone_mu[0]=(bjsa_mu_momentum.Pt())
                        bjet_eta_medium_pt_topstandalone_mu[0]=(bjsa_mu_momentum.Eta())
                        bjet_phi_medium_pt_topstandalone_mu[0]=(bjsa_mu_momentum.Phi())
                        bjet_M_medium_pt_topstandalone_mu[0]=(bjsa_mu_momentum.M())
                        TopSA_deepJetScore_medium_pt_topstandalone_mu[0] = goodJsa_mu[0].btagDeepFlavB
                        TopSA_jet_pt_medium_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                        TopSA_jet_eta_medium_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                        TopSA_jet_phi_medium_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                        TopSA_jet_M_medium_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI
                    
                    else:
                        WP_M_medium_pt_topstandalone_mu[0]=-999.
                        WP_pt_medium_pt_topstandalone_mu[0]=-999.
                        WP_eta_medium_pt_topstandalone_mu[0]=-999.
                        WP_phi_medium_pt_topstandalone_mu[0]=-999.
                        bjet_pt_medium_pt_topstandalone_mu[0]=-999.
                        bjet_eta_medium_pt_topstandalone_mu[0]=-999.
                        bjet_phi_medium_pt_topstandalone_mu[0]=-999.
                        bjet_M_medium_pt_topstandalone_mu[0]=-999.
                        TopSA_deepJetScore_medium_pt_topstandalone_mu[0] = -999.
                        
                else:
                    WP_M_medium_pt_topstandalone_mu[0]=-999.
                    WP_pt_medium_pt_topstandalone_mu[0]=-999.
                    WP_eta_medium_pt_topstandalone_mu[0]=-999.
                    WP_phi_medium_pt_topstandalone_mu[0]=-999.
                    TopSA_pt_medium_pt_topstandalone_mu[0] = -999.
                    TopSA_eta_medium_pt_topstandalone_mu[0] = -999.
                    TopSA_phi_medium_pt_topstandalone_mu[0] = -999.
                    TopSA_M_medium_pt_topstandalone_mu[0] = -999.
                    TopSA_Score_medium_pt_topstandalone_mu[0] = -999
                    TopSA_deepJetScore_medium_pt_topstandalone_mu[0] = -999.

                    TopSA_jet_pt_medium_pt_topstandalone_mu[0] = -999.
                    TopSA_jet_eta_medium_pt_topstandalone_mu[0] = -999.
                    TopSA_jet_phi_medium_pt_topstandalone_mu[0] = -999.
                    TopSA_jet_M_medium_pt_topstandalone_mu[0] = -999.

                    bjet_pt_medium_pt_topstandalone_mu[0]=-999.
                    bjet_eta_medium_pt_topstandalone_mu[0]=-999.
                    bjet_phi_medium_pt_topstandalone_mu[0]=-999.
                    bjet_M_medium_pt_topstandalone_mu[0]=-999.


            if (train_sa.label)=='BDT_medium_pt_topstandalone_el':
                if (len(new_coll_sa_wp90)>0):
                    TopSA_pt_medium_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_pt
                    TopSA_eta_medium_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_eta 
                    TopSA_phi_medium_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_phi 
                    TopSA_M_medium_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_M 
                    TopSA_Score_medium_pt_topstandalone_el[0] = new_coll_sa_wp90[0][1]


                    TopSA_jet_pt_medium_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                    TopSA_jet_eta_medium_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                    TopSA_jet_phi_medium_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                    TopSA_jet_M_medium_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI


                    if(new_coll_sa_wp90[0][0].Truth==0) and (abs(jets[int(new_coll_sa_wp90[0][0].Jet_index)].partonFlavour)==5): #corretta 
                        TopSA_MC_medium_pt_topstandalone_el[0] = 1
                    else:
                        TopSA_MC_medium_pt_topstandalone_el[0] = 0


                    TopSA_medium_pt_topstandalone_el_momentum.SetPtEtaPhiM(TopSA_jet_pt_medium_pt_topstandalone_el[0], TopSA_jet_eta_medium_pt_topstandalone_el[0], TopSA_jet_phi_medium_pt_topstandalone_el[0], TopSA_jet_M_medium_pt_topstandalone_el[0])
                   
                    if (len(goodJsa_el)>0):
                        WP_momentum = TopSA_medium_pt_topstandalone_el_momentum + bjsa_el_momentum
                        WP_M_medium_pt_topstandalone_el[0]=(WP_momentum.M())
                        WP_pt_medium_pt_topstandalone_el[0]=(WP_momentum.Pt())
                        WP_eta_medium_pt_topstandalone_el[0]=(WP_momentum.Eta())
                        WP_phi_medium_pt_topstandalone_el[0]=(WP_momentum.Phi())

                        bjet_pt_medium_pt_topstandalone_el[0]=(bjsa_el_momentum.Pt())
                        bjet_eta_medium_pt_topstandalone_el[0]=(bjsa_el_momentum.Eta())
                        bjet_phi_medium_pt_topstandalone_el[0]=(bjsa_el_momentum.Phi())
                        bjet_M_medium_pt_topstandalone_el[0]=(bjsa_el_momentum.M())
                        TopSA_deepJetScore_medium_pt_topstandalone_el[0] = goodJsa_el[0].btagDeepFlavB
                        TopSA_jet_pt_medium_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                        TopSA_jet_eta_medium_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                        TopSA_jet_phi_medium_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                        TopSA_jet_M_medium_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI

                    
                    else:
                        WP_M_medium_pt_topstandalone_el[0]=-999.
                        WP_pt_medium_pt_topstandalone_el[0]=-999.
                        WP_eta_medium_pt_topstandalone_el[0]=-999.
                        WP_phi_medium_pt_topstandalone_el[0]=-999.

                        bjet_pt_medium_pt_topstandalone_el[0]= -999.
                        bjet_eta_medium_pt_topstandalone_el[0]= -999.
                        bjet_phi_medium_pt_topstandalone_el[0]= -999.
                        bjet_M_medium_pt_topstandalone_el[0]= -999.
                        TopSA_deepJetScore_medium_pt_topstandalone_el[0] = -999.

                else:
                    WP_M_medium_pt_topstandalone_el[0]=-999.
                    WP_pt_medium_pt_topstandalone_el[0]=-999.
                    WP_eta_medium_pt_topstandalone_el[0]=-999.
                    WP_phi_medium_pt_topstandalone_el[0]=-999.

                    TopSA_pt_medium_pt_topstandalone_el[0] = -999.
                    TopSA_eta_medium_pt_topstandalone_el[0] = -999.
                    TopSA_phi_medium_pt_topstandalone_el[0] = -999.
                    TopSA_M_medium_pt_topstandalone_el[0] = -999.
                    TopSA_Score_medium_pt_topstandalone_el[0] = -999
                    TopSA_deepJetScore_medium_pt_topstandalone_el[0] = -999.

                    TopSA_jet_pt_medium_pt_topstandalone_el[0] = -999.
                    TopSA_jet_eta_medium_pt_topstandalone_el[0] = -999.
                    TopSA_jet_phi_medium_pt_topstandalone_el[0] = -999.
                    TopSA_jet_M_medium_pt_topstandalone_el[0] = -999.

                    bjet_pt_medium_pt_topstandalone_el[0]= -999.
                    bjet_eta_medium_pt_topstandalone_el[0]= -999.
                    bjet_phi_medium_pt_topstandalone_el[0]= -999.
                    bjet_M_medium_pt_topstandalone_el[0]= -999.


            if (train_sa.label)=='BDT_low_pt_topstandalone_mu':
                if (len(new_coll_sa_wp90)>0):
                    TopSA_pt_low_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_pt
                    TopSA_eta_low_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_eta 
                    TopSA_phi_low_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_phi 
                    TopSA_M_low_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][0].nu_M 
                    TopSA_Score_low_pt_topstandalone_mu[0] = new_coll_sa_wp90[0][1]
                    
                    TopSA_jet_pt_low_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                    TopSA_jet_eta_low_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                    TopSA_jet_phi_low_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                    TopSA_jet_M_low_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI

                    if(new_coll_sa_wp90[0][0].Truth==0)  and (abs(jets[int(new_coll_sa_wp90[0][0].Jet_index)].partonFlavour)==5): #corretta 
                        TopSA_MC_low_pt_topstandalone_mu[0] = 1
                    else:
                        TopSA_MC_low_pt_topstandalone_mu[0] = 0
                    
                    TopSA_low_pt_topstandalone_mu_momentum.SetPtEtaPhiM(TopSA_jet_pt_low_pt_topstandalone_mu[0], TopSA_jet_eta_low_pt_topstandalone_mu[0], TopSA_jet_phi_low_pt_topstandalone_mu[0], TopSA_jet_M_low_pt_topstandalone_mu[0])
                   
                    if (len(goodJsa_mu)>0):
                        WP_momentum = TopSA_low_pt_topstandalone_mu_momentum + bjsa_mu_momentum
                        WP_M_low_pt_topstandalone_mu[0]=(WP_momentum.M())
                        WP_pt_low_pt_topstandalone_mu[0]=(WP_momentum.Pt())
                        WP_eta_low_pt_topstandalone_mu[0]=(WP_momentum.Eta())
                        WP_phi_low_pt_topstandalone_mu[0]=(WP_momentum.Phi())

                        bjet_pt_low_pt_topstandalone_mu[0]=(bjsa_mu_momentum.Pt())
                        bjet_eta_low_pt_topstandalone_mu[0]=(bjsa_mu_momentum.Eta())
                        bjet_phi_low_pt_topstandalone_mu[0]=(bjsa_mu_momentum.Phi())
                        bjet_M_low_pt_topstandalone_mu[0]=(bjsa_mu_momentum.M())
                        TopSA_deepJetScore_low_pt_topstandalone_mu[0] = goodJsa_mu[0].btagDeepFlavB
                        TopSA_jet_pt_low_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                        TopSA_jet_eta_low_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                        TopSA_jet_phi_low_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                        TopSA_jet_M_low_pt_topstandalone_mu[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI
                    
                    else:
                        WP_M_low_pt_topstandalone_mu[0]=-999.
                        WP_pt_low_pt_topstandalone_mu[0]=-999
                        WP_eta_low_pt_topstandalone_mu[0]=-999
                        WP_phi_low_pt_topstandalone_mu[0]=-999

                        bjet_pt_low_pt_topstandalone_mu[0]= -999.
                        bjet_eta_low_pt_topstandalone_mu[0]= -999.
                        bjet_phi_low_pt_topstandalone_mu[0]=  -999.
                        bjet_M_low_pt_topstandalone_mu[0]= -999.
                        TopSA_deepJetScore_low_pt_topstandalone_mu[0] = -999.

                else:
                    WP_M_low_pt_topstandalone_mu[0]=-999.
                    WP_pt_low_pt_topstandalone_mu[0]=-999
                    WP_eta_low_pt_topstandalone_mu[0]=-999
                    WP_phi_low_pt_topstandalone_mu[0]=-999
                    TopSA_pt_low_pt_topstandalone_mu[0] = -999.
                    TopSA_eta_low_pt_topstandalone_mu[0] = -999.
                    TopSA_phi_low_pt_topstandalone_mu[0] = -999.
                    TopSA_M_low_pt_topstandalone_mu[0] = -999.
                    TopSA_Score_low_pt_topstandalone_mu[0] = -999
                    TopSA_deepJetScore_low_pt_topstandalone_mu[0] = -999.               
                    TopSA_jet_pt_low_pt_topstandalone_mu[0] = -999.
                    TopSA_jet_eta_low_pt_topstandalone_mu[0] = -999.
                    TopSA_jet_phi_low_pt_topstandalone_mu[0] = -999.
                    TopSA_jet_M_low_pt_topstandalone_mu[0] = -999.

                    bjet_pt_low_pt_topstandalone_mu[0]=  -999.
                    bjet_eta_low_pt_topstandalone_mu[0]=  -999.
                    bjet_phi_low_pt_topstandalone_mu[0]=  -999.
                    bjet_M_low_pt_topstandalone_mu[0]=  -999.


            if (train_sa.label)=='BDT_low_pt_topstandalone_el':
                if (len(new_coll_sa_wp90)>0):
                    TopSA_pt_low_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_pt
                    TopSA_eta_low_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_eta 
                    TopSA_phi_low_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_phi 
                    TopSA_M_low_pt_topstandalone_el[0] = new_coll_sa_wp90[0][0].nu_M 
                    TopSA_Score_low_pt_topstandalone_el[0] = new_coll_sa_wp90[0][1]

                    TopSA_jet_pt_low_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                    TopSA_jet_eta_low_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                    TopSA_jet_phi_low_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                    TopSA_jet_M_low_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI


                    if(new_coll_sa_wp90[0][0].Truth==0)  and (abs(jets[int(new_coll_sa_wp90[0][0].Jet_index)].partonFlavour)==5): #corretta 
                        TopSA_MC_low_pt_topstandalone_el[0] = 1
                    else:
                        TopSA_MC_low_pt_topstandalone_el[0] = 0


                    TopSA_low_pt_topstandalone_el_momentum.SetPtEtaPhiM(TopSA_jet_pt_low_pt_topstandalone_el[0], TopSA_jet_eta_low_pt_topstandalone_el[0], TopSA_jet_phi_low_pt_topstandalone_el[0], TopSA_jet_M_low_pt_topstandalone_el[0])
                   
                    if (len(goodJsa_el)>0):
                        WP_momentum = TopSA_low_pt_topstandalone_el_momentum + bjsa_el_momentum
                        WP_M_low_pt_topstandalone_el[0]=(WP_momentum.M())
                        WP_pt_low_pt_topstandalone_el[0]=(WP_momentum.Pt())
                        WP_eta_low_pt_topstandalone_el[0]=(WP_momentum.Eta())
                        WP_phi_low_pt_topstandalone_el[0]=(WP_momentum.Phi())

                        bjet_pt_low_pt_topstandalone_el[0]=(bjsa_el_momentum.Pt())
                        bjet_eta_low_pt_topstandalone_el[0]=(bjsa_el_momentum.Eta())
                        bjet_phi_low_pt_topstandalone_el[0]=(bjsa_el_momentum.Phi())
                        bjet_M_low_pt_topstandalone_el[0]=(bjsa_el_momentum.M())
                        TopSA_deepJetScore_low_pt_topstandalone_el[0] = goodJsa_el[0].btagDeepFlavB
                        #print("bjet_M_low_pt_topstandalone_el", bjet_M_low_pt_topstandalone_el[0])
                        TopSA_jet_pt_low_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].pt
                        TopSA_jet_eta_low_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].eta
                        TopSA_jet_phi_low_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].phi
                        TopSA_jet_M_low_pt_topstandalone_el[0] = jets[int(new_coll_sa_wp90[0][0].Jet_index)].mass #REMINDER QUESTI SO PIU' BELLILLI

                    else:
                        WP_M_low_pt_topstandalone_el[0]=-999.
                        WP_pt_low_pt_topstandalone_el[0]=-999.
                        WP_eta_low_pt_topstandalone_el[0]=-999.
                        WP_phi_low_pt_topstandalone_el[0]=-999.

                        bjet_pt_low_pt_topstandalone_el[0]=  -999.
                        bjet_eta_low_pt_topstandalone_el[0]=  -999.
                        bjet_phi_low_pt_topstandalone_el[0]=  -999.
                        bjet_M_low_pt_topstandalone_el[0]=  -999.
                        TopSA_deepJetScore_low_pt_topstandalone_el[0] = -999.


                else:
                    WP_M_low_pt_topstandalone_el[0]=-999.
                    WP_pt_low_pt_topstandalone_el[0]=-999.
                    WP_eta_low_pt_topstandalone_el[0]=-999.
                    WP_phi_low_pt_topstandalone_el[0]=-999.
                    TopSA_pt_low_pt_topstandalone_el[0] = -999.
                    TopSA_eta_low_pt_topstandalone_el[0] = -999.
                    TopSA_phi_low_pt_topstandalone_el[0] = -999.
                    TopSA_M_low_pt_topstandalone_el[0] = -999.
                    TopSA_Score_low_pt_topstandalone_el[0] = -999
                    TopSA_deepJetScore_low_pt_topstandalone_el[0] = -999.
                
                    TopSA_jet_pt_low_pt_topstandalone_el[0] = -999.
                    TopSA_jet_eta_low_pt_topstandalone_el[0] = -999.
                    TopSA_jet_phi_low_pt_topstandalone_el[0] = -999.
                    TopSA_jet_M_low_pt_topstandalone_el[0] = -999.

                    bjet_pt_low_pt_topstandalone_el[0]=  -999.
                    bjet_eta_low_pt_topstandalone_el[0]=  -999.
                    bjet_phi_low_pt_topstandalone_el[0]=  -999.
                    bjet_M_low_pt_topstandalone_el[0]=  -999.


        systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal[0]))

        systTree.fillTreesSysts(trees, scenario)

 
    systTree.writeTreesSysts(trees, outTreeFile)


reco("nominal",isMC,addPDF, training, training_topsa)





endTime = datetime.datetime.now()
print("Ending running at " + str(endTime))

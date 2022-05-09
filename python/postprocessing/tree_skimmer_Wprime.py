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

if sys.argv[4] == None: training = training_dict["Wprime"]
else: training = training_dict[sys.argv[4]]

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



if not os.path.exists("/eos/user/c/cgiordan/Wprime/nosynch/v0/"+sample.label+"/"):
    os.makedirs("/eos/user/c/cgiordan/Wprime/nosynch/v0/"+sample.label+"/")
#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
outTreeFile = ROOT.TFile("/eos/user/c/cgiordan/Wprime/nosynch/v0/"+sample.label+"/"+sample.label+"_part"+str(part_idx)+".root", "RECREATE") 

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

def reco(scenario, isMC, addPDF, training):
    isNominal = False
    if scenario == 'nominal':
        isNominal = True
    print(scenario)


    Top_pt_high_pt_mu_merg = array.array('f',[0.]) 
    Top_eta_high_pt_mu_merg = array.array('f',[0.]) 
    Top_phi_high_pt_mu_merg = array.array('f',[0.]) 
    Top_M_high_pt_mu_merg = array.array('f',[0.]) 
    Top_Score_high_pt_mu_merg = array.array('f',[0.]) 
    Top_MC_high_pt_mu_merg = array.array('i',[0]) #if isMC:

    Top_pt2_nominal = array.array('f',[0.]) 
    Top_eta2_nominal = array.array('f',[0.]) 
    Top_phi2_nominal = array.array('f',[0.]) 
    Top_M2_nominal = array.array('f',[0.]) 
    Top_Score2_nominal = array.array('f',[0.]) 
    Top_MC2_nominal = array.array('i',[0])

    Top_pt3_nominal = array.array('f',[0.]) 
    Top_eta3_nominal = array.array('f',[0.]) 
    Top_phi3_nominal = array.array('f',[0.]) 
    Top_M3_nominal = array.array('f',[0.]) 
    Top_Score3_nominal = array.array('f',[0.])
    Top_MC3_nominal = array.array('i',[0]) 

    Top_pt1_0p5_nominal = array.array('f',[0.]) 
    Top_eta1_0p5_nominal = array.array('f',[0.]) 
    Top_phi1_0p5_nominal = array.array('f',[0.]) 
    Top_M1_0p5_nominal = array.array('f',[0.]) 
    Top_Score1_0p5_nominal = array.array('f',[0.]) 
    Top_MC1_0p5_nominal = array.array('i',[0])

    Top_pt2_0p5_nominal = array.array('f',[0.]) 
    Top_eta2_0p5_nominal = array.array('f',[0.]) 
    Top_phi2_0p5_nominal = array.array('f',[0.]) 
    Top_M2_0p5_nominal = array.array('f',[0.]) 
    Top_Score2_0p5_nominal = array.array('f',[0.]) 
    Top_MC2_0p5_nominal = array.array('i',[0])

    Top_pt3_0p5_nominal = array.array('f',[0.]) 
    Top_eta3_0p5_nominal = array.array('f',[0.]) 
    Top_phi3_0p5_nominal = array.array('f',[0.]) 
    Top_M3_0p5_nominal = array.array('f',[0.]) 
    Top_Score3_0p5_nominal = array.array('f',[0.])
    Top_MC3_0p5_nominal = array.array('i',[0]) 

    Top_pt1_wp90_nominal = array.array('f',[0.]) 
    Top_eta1_wp90_nominal = array.array('f',[0.]) 
    Top_phi1_wp90_nominal = array.array('f',[0.]) 
    Top_M1_wp90_nominal = array.array('f',[0.]) 
    Top_Score1_wp90_nominal = array.array('f',[0.]) 
    Top_MC1_wp90_nominal = array.array('i',[0])

    Top_pt2_wp90_nominal = array.array('f',[0.]) 
    Top_eta2_wp90_nominal = array.array('f',[0.]) 
    Top_phi2_wp90_nominal = array.array('f',[0.]) 
    Top_M2_wp90_nominal = array.array('f',[0.]) 
    Top_Score2_wp90_nominal = array.array('f',[0.]) 
    Top_MC2_wp90_nominal = array.array('i',[0])

    Top_pt3_wp90_nominal = array.array('f',[0.]) 
    Top_eta3_wp90_nominal = array.array('f',[0.]) 
    Top_phi3_wp90_nominal = array.array('f',[0.]) 
    Top_M3_wp90_nominal = array.array('f',[0.]) 
    Top_Score3_wp90_nominal = array.array('f',[0.])
    Top_MC3_wp90_nominal = array.array('i',[0])


    systTree.branchTreesSysts(trees, scenario,"Top_pt_high_pt_mu_merg",outTreeFile,Top_pt_high_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta_high_pt_mu_merg",outTreeFile,Top_eta_high_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi_high_pt_mu_merg",outTreeFile,Top_phi_high_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_M_high_pt_mu_merg",outTreeFile,Top_M_high_pt_mu_merg) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score_high_pt_mu_merg",outTreeFile,Top_Score_high_pt_mu_merg)
    systTree.branchTreesSysts(trees, scenario,"Top_MC_high_pt_mu_merg",outTreeFile,Top_MC_high_pt_mu_merg)

    systTree.branchTreesSysts(trees, scenario,"Top_pt2_nominal",outTreeFile,Top_pt2_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta2_nominal",outTreeFile,Top_eta2_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi2_nominal",outTreeFile,Top_phi2_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_M2_nominal",outTreeFile,Top_M2_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score2_nominal",outTreeFile,Top_Score2_nominal)
    systTree.branchTreesSysts(trees, scenario,"Top_MC2_nominal",outTreeFile,Top_MC2_nominal)

    systTree.branchTreesSysts(trees, scenario,"Top_pt3_nominal",outTreeFile,Top_pt3_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta3_nominal",outTreeFile,Top_eta3_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi3_nominal",outTreeFile,Top_phi3_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_M3_nominal",outTreeFile,Top_M3_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score3_nominal",outTreeFile,Top_Score3_nominal)
    systTree.branchTreesSysts(trees, scenario,"Top_MC3_nominal",outTreeFile,Top_MC3_nominal)


    systTree.branchTreesSysts(trees, scenario,"Top_pt1_0p5_nominal",outTreeFile,Top_pt1_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta1_0p5_nominal",outTreeFile,Top_eta1_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi1_0p5_nominal",outTreeFile,Top_phi1_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_M1_0p5_nominal",outTreeFile,Top_M1_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score1_0p5_nominal",outTreeFile,Top_Score1_0p5_nominal)
    systTree.branchTreesSysts(trees, scenario,"Top_MC1_0p5_nominal",outTreeFile,Top_MC1_0p5_nominal)

    systTree.branchTreesSysts(trees, scenario,"Top_pt2_0p5_nominal",outTreeFile,Top_pt2_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta2_0p5_nominal",outTreeFile,Top_eta2_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi2_0p5_nominal",outTreeFile,Top_phi2_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_M2_0p5_nominal",outTreeFile,Top_M2_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score2_0p5_nominal",outTreeFile,Top_Score2_0p5_nominal)
    systTree.branchTreesSysts(trees, scenario,"Top_MC2_0p5_nominal",outTreeFile,Top_MC2_0p5_nominal)

    systTree.branchTreesSysts(trees, scenario,"Top_pt3_0p5_nominal",outTreeFile,Top_pt3_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta3_0p5_nominal",outTreeFile,Top_eta3_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi3_0p5_nominal",outTreeFile,Top_phi3_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_M3_0p5_nominal",outTreeFile,Top_M3_0p5_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score3_0p5_nominal",outTreeFile,Top_Score3_0p5_nominal)
    systTree.branchTreesSysts(trees, scenario,"Top_MC3_0p5_nominal",outTreeFile,Top_MC3_0p5_nominal)


    systTree.branchTreesSysts(trees, scenario,"Top_pt1_wp90_nominal",outTreeFile,Top_pt1_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta1_wp90_nominal",outTreeFile,Top_eta1_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi1_wp90_nominal",outTreeFile,Top_phi1_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_M1_wp90_nominal",outTreeFile,Top_M1_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score1_wp90_nominal",outTreeFile,Top_Score1_wp90_nominal)
    systTree.branchTreesSysts(trees, scenario,"Top_MC1_wp90_nominal",outTreeFile,Top_MC1_wp90_nominal)

    systTree.branchTreesSysts(trees, scenario,"Top_pt2_wp90_nominal",outTreeFile,Top_pt2_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta2_wp90_nominal",outTreeFile,Top_eta2_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi2_wp90_nominal",outTreeFile,Top_phi2_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_M2_wp90_nominal",outTreeFile,Top_M2_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score2_wp90_nominal",outTreeFile,Top_Score2_wp90_nominal)
    systTree.branchTreesSysts(trees, scenario,"Top_MC2_wp90_nominal",outTreeFile,Top_MC2_wp90_nominal)

    systTree.branchTreesSysts(trees, scenario,"Top_pt3_wp90_nominal",outTreeFile,Top_pt3_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_eta3_wp90_nominal",outTreeFile,Top_eta3_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_phi3_wp90_nominal",outTreeFile,Top_phi3_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_M3_wp90_nominal",outTreeFile,Top_M3_wp90_nominal) 
    systTree.branchTreesSysts(trees, scenario,"Top_Score3_wp90_nominal",outTreeFile,Top_Score3_wp90_nominal)
    systTree.branchTreesSysts(trees, scenario,"Top_MC3_wp90_nominal",outTreeFile,Top_MC3_wp90_nominal)


    h_genweight = ROOT.TH1F("h_genweight", "h_genweight", 1, -0.5, 0.5)

    N = 2000
    #N= tree.GetEntries()
    h_genweight.SetBinContent(1, N)

    outTreeFile.cd()
    h_genweight.Write()
    



#    for i in range(tree.GetEntries()):
    for i in range(N):
        event = Event(tree,i)    
        jets = Collection(event, "Jet")             # jets[j1].btagDeepFlavB  ---> medium discriminant cut = 0.2783
        tops = Collection(event,"Top")
        met = Object(event, "MET")
        electron = Collection(event, "Electron")
        muon = Collection(event, "Muon")
        nelectron = len(electron)
        nmuon = len(muon)
        ntop = len(tops)
        fatjets = Collection(event,"FatJet")
        
        if i%100 == 0:
            print("Processed ", i+1, " out of ", tree.GetEntries(), " events")
        
 
        all_coll=[]
        all_coll_wp90=[]

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
                                                and (x.el_index != -1)
                                                ,tops))
                is_el=True
            else:
                good_top = list(filter(lambda x: 
                                                (x.nu_pt>= train.pt_cut[0]) and (x.nu_pt<train.pt_cut[1])
                                                and (x.Is_dR_merg == train.category)
                                                and (x.mu_index != -1)
                                                ,tops))
                is_el=False


            for top in good_top:
                lista=[]
                score_=-999
                for m in train.var_MET: lista.append(met[m])
                for j in train.var_jet: lista.append(jets[int(top.bjet_index)][j])
                if is_el:
                    for el in train.var_lep: 
                        if(el=="Over_Jet_Pt"):
                            lista.append(electron[int(top.el_index)].pt/jets[int(top.bjet_index)].pt)
                        else:
                            lista.append(electron[int(top.el_index)][el])
                else:
                    for mu in train.var_lep: 
                        if(mu=="Over_Jet_Pt"):
                            lista.append(muon[int(top.mu_index)].pt/jets[int(top.bjet_index)].pt)
                        else:
                            lista.append(muon[int(top.mu_index)][mu])
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
                if (score_>train.score_cut): new_coll_wp90.append([top,score_])
                
            if(len(new_coll)>0): 
                new_coll =  [x for _,x in sorted(zip([new_coll[i][-1] for i in range(len(score))],new_coll))]
                new_coll.reverse()
                if(len(new_coll_wp90)>0):
                    new_coll_wp90 =  [x for _,x in sorted(zip([new_coll_wp90[i][-1] for i in range(len(new_coll_wp90))],new_coll_wp90))]
                    new_coll_wp90.reverse()

            all_coll = all_coll +  new_coll
            all_coll_wp90 = all_coll_wp90 + new_coll_wp90
            



        if(len(all_coll)==0): continue

        all_coll_0p5 = list(filter(lambda x: x[-1]>=0.5,all_coll))

        Top_pt_high_pt_mu_merg[0] = all_coll[0][0].nu_pt 
        Top_eta_high_pt_mu_merg[0] = all_coll[0][0].nu_eta 
        Top_phi_high_pt_mu_merg[0] = all_coll[0][0].nu_phi 
        Top_M_high_pt_mu_merg[0] = all_coll[0][0].nu_M 
        Top_Score_high_pt_mu_merg[0] = all_coll[0][1]
        if(all_coll[0][0].LHE_Truth==0): Top_MC_high_pt_mu_merg[0] = 1
        else: Top_MC_high_pt_mu_merg[0] = 0

        if len(all_coll_0p5)>0:
            Top_pt1_0p5_nominal[0] = all_coll_0p5[0][0].nu_pt 
            Top_eta1_0p5_nominal[0] = all_coll_0p5[0][0].nu_eta 
            Top_phi1_0p5_nominal[0] = all_coll_0p5[0][0].nu_phi 
            Top_M1_0p5_nominal[0] = all_coll_0p5[0][0].nu_M 
            Top_Score1_0p5_nominal[0] = all_coll_0p5[0][1]
            if(all_coll_0p5[0][0].LHE_Truth==0): Top_MC1_0p5_nominal[0] = 1
            else: Top_MC1_0p5_nominal[0] = 0
        else:
            Top_pt1_0p5_nominal[0] = -999 
            Top_eta1_0p5_nominal[0] = -999 
            Top_phi1_0p5_nominal[0] = -999
            Top_M1_0p5_nominal[0] = -999
            Top_Score1_0p5_nominal[0] = -999            
            Top_MC1_0p5_nominal[0] = 0

            Top_pt2_0p5_nominal[0] = -999 
            Top_eta2_0p5_nominal[0] = -999 
            Top_phi2_0p5_nominal[0] = -999 
            Top_M2_0p5_nominal[0] = -999 
            Top_Score2_0p5_nominal[0] = -999
            Top_MC2_0p5_nominal[0] = 0

            Top_pt3_0p5_nominal[0] = -999 
            Top_eta3_0p5_nominal[0] = -999 
            Top_phi3_0p5_nominal[0] = -999 
            Top_M3_0p5_nominal[0] = -999 
            Top_Score3_0p5_nominal[0] = -999
            Top_MC3_0p5_nominal[0] = 0

        if len(all_coll_wp90)>0:
            Top_pt1_wp90_nominal[0] = all_coll_wp90[0][0].nu_pt 
            Top_eta1_wp90_nominal[0] = all_coll_wp90[0][0].nu_eta 
            Top_phi1_wp90_nominal[0] = all_coll_wp90[0][0].nu_phi 
            Top_M1_wp90_nominal[0] = all_coll_wp90[0][0].nu_M 
            Top_Score1_wp90_nominal[0] = all_coll_wp90[0][1]
            if(all_coll_wp90[0][0].LHE_Truth==0): Top_MC1_wp90_nominal[0] = 1
            else: Top_MC1_wp90_nominal[0] = 0
        else:
            Top_pt1_wp90_nominal[0] = -999 
            Top_eta1_wp90_nominal[0] = -999 
            Top_phi1_wp90_nominal[0] = -999
            Top_M1_wp90_nominal[0] = -999
            Top_Score1_wp90_nominal[0] = -999            
            Top_MC1_wp90_nominal[0] = 0

            Top_pt2_wp90_nominal[0] = -999 
            Top_eta2_wp90_nominal[0] = -999 
            Top_phi2_wp90_nominal[0] = -999 
            Top_M2_wp90_nominal[0] = -999 
            Top_Score2_wp90_nominal[0] = -999
            Top_MC2_wp90_nominal[0] = 0

            Top_pt3_wp90_nominal[0] = -999 
            Top_eta3_wp90_nominal[0] = -999 
            Top_phi3_wp90_nominal[0] = -999 
            Top_M3_wp90_nominal[0] = -999 
            Top_Score3_wp90_nominal[0] = -999
            Top_MC3_wp90_nominal[0] = 0


        if(len(all_coll)>1):
            Top_pt2_nominal[0] = all_coll[1][0].nu_pt 
            Top_eta2_nominal[0] = all_coll[1][0].nu_eta 
            Top_phi2_nominal[0] = all_coll[1][0].nu_phi 
            Top_M2_nominal[0] = all_coll[1][0].nu_M 
            Top_Score2_nominal[0] = all_coll[1][1]
            if(all_coll[1][0].LHE_Truth==0): Top_MC2_nominal[0] = 1
            else: Top_MC2_nominal[0] = 0

        else:
            Top_pt2_nominal[0] = -999 
            Top_eta2_nominal[0] = -999 
            Top_phi2_nominal[0] = -999 
            Top_M2_nominal[0] = -999 
            Top_Score2_nominal[0] = -999
            Top_MC2_nominal[0] = 0

            Top_pt3_nominal[0] = -999 
            Top_eta3_nominal[0] = -999 
            Top_phi3_nominal[0] = -999 
            Top_M3_nominal[0] = -999 
            Top_Score3_nominal[0] = -999
            Top_MC3_nominal[0] = 0
        

        if len(all_coll_0p5)>1:
            Top_pt2_0p5_nominal[0] = all_coll_0p5[1][0].nu_pt 
            Top_eta2_0p5_nominal[0] = all_coll_0p5[1][0].nu_eta 
            Top_phi2_0p5_nominal[0] = all_coll_0p5[1][0].nu_phi 
            Top_M2_0p5_nominal[0] = all_coll_0p5[1][0].nu_M 
            Top_Score2_0p5_nominal[0] = all_coll_0p5[1][1]
            if(all_coll_0p5[1][0].LHE_Truth==0): Top_MC2_0p5_nominal[0] = 1
            else: Top_MC2_0p5_nominal[0] = 0
        else:

            Top_pt2_0p5_nominal[0] = -999 
            Top_eta2_0p5_nominal[0] = -999 
            Top_phi2_0p5_nominal[0] = -999 
            Top_M2_0p5_nominal[0] = -999 
            Top_Score2_0p5_nominal[0] = -999
            Top_MC2_0p5_nominal[0] = 0

            Top_pt3_0p5_nominal[0] = -999 
            Top_eta3_0p5_nominal[0] = -999 
            Top_phi3_0p5_nominal[0] = -999 
            Top_M3_0p5_nominal[0] = -999 
            Top_Score3_0p5_nominal[0] = -999
            Top_MC3_0p5_nominal[0] = 0

        if len(all_coll_wp90)>1:
            Top_pt2_wp90_nominal[0] = all_coll_wp90[1][0].nu_pt 
            Top_eta2_wp90_nominal[0] = all_coll_wp90[1][0].nu_eta 
            Top_phi2_wp90_nominal[0] = all_coll_wp90[1][0].nu_phi 
            Top_M2_wp90_nominal[0] = all_coll_wp90[1][0].nu_M 
            Top_Score2_wp90_nominal[0] = all_coll_wp90[1][1]
            if(all_coll_wp90[1][0].LHE_Truth==0): Top_MC2_wp90_nominal[0] = 1
            else: Top_MC2_wp90_nominal[0] = 0
        else:

            Top_pt2_wp90_nominal[0] = -999 
            Top_eta2_wp90_nominal[0] = -999 
            Top_phi2_wp90_nominal[0] = -999 
            Top_M2_wp90_nominal[0] = -999 
            Top_Score2_wp90_nominal[0] = -999
            Top_MC2_wp90_nominal[0] = 0

            Top_pt3_wp90_nominal[0] = -999 
            Top_eta3_wp90_nominal[0] = -999 
            Top_phi3_wp90_nominal[0] = -999 
            Top_M3_wp90_nominal[0] = -999 
            Top_Score3_wp90_nominal[0] = -999
            Top_MC3_wp90_nominal[0] = 0

        if(len(all_coll)>2):
            Top_pt3_nominal[0] = all_coll[2][0].nu_pt 
            Top_eta3_nominal[0] = all_coll[2][0].nu_eta 
            Top_phi3_nominal[0] = all_coll[2][0].nu_phi 
            Top_M3_nominal[0] = all_coll[2][0].nu_M 
            Top_Score3_nominal[0] = all_coll[2][1]
            if(all_coll[2][0].LHE_Truth==0): Top_MC3_nominal[0] = 1
            else: Top_MC3_nominal[0] = 0

        else:
            Top_pt3_nominal[0] = -999 
            Top_eta3_nominal[0] = -999 
            Top_phi3_nominal[0] = -999 
            Top_M3_nominal[0] = -999 
            Top_Score3_nominal[0] = -999
            Top_MC3_nominal[0] = 0

        if len(all_coll_0p5)>2:
            Top_pt3_0p5_nominal[0] = all_coll_0p5[2][0].nu_pt 
            Top_eta3_0p5_nominal[0] = all_coll_0p5[2][0].nu_eta 
            Top_phi3_0p5_nominal[0] = all_coll_0p5[2][0].nu_phi 
            Top_M3_0p5_nominal[0] = all_coll_0p5[2][0].nu_M 
            Top_Score3_0p5_nominal[0] = all_coll_0p5[2][1]
            if(all_coll_0p5[2][0].LHE_Truth==0): Top_MC3_0p5_nominal[0] = 1
            else: Top_MC3_0p5_nominal[0] = 0
        else:

            Top_pt3_0p5_nominal[0] = -999 
            Top_eta3_0p5_nominal[0] = -999 
            Top_phi3_0p5_nominal[0] = -999 
            Top_M3_0p5_nominal[0] = -999 
            Top_Score3_0p5_nominal[0] = -999
            Top_MC3_0p5_nominal[0] = 0

        if len(all_coll_wp90)>2:
            Top_pt3_wp90_nominal[0] = all_coll_wp90[2][0].nu_pt 
            Top_eta3_wp90_nominal[0] = all_coll_wp90[2][0].nu_eta 
            Top_phi3_wp90_nominal[0] = all_coll_wp90[2][0].nu_phi 
            Top_M3_wp90_nominal[0] = all_coll_wp90[2][0].nu_M 
            Top_Score3_wp90_nominal[0] = all_coll_wp90[2][1]
            if(all_coll_wp90[2][0].LHE_Truth==0): Top_MC3_wp90_nominal[0] = 1
            else: Top_MC3_wp90_nominal[0] = 0
        else:

            Top_pt3_wp90_nominal[0] = -999 
            Top_eta3_wp90_nominal[0] = -999 
            Top_phi3_wp90_nominal[0] = -999 
            Top_M3_wp90_nominal[0] = -999 
            Top_Score3_wp90_nominal[0] = -999
            Top_MC3_wp90_nominal[0] = 0



        systTree.fillTreesSysts(trees, scenario)

 
    systTree.writeTreesSysts(trees, outTreeFile)


reco("nominal",isMC,addPDF, training)


endTime = datetime.datetime.now()
print("Ending running at " + str(endTime))

#!/bin/env python3
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

if sys.argv[4] == 'remote':
    from samples import *
    Debug = False
else:
    from samples.samples import *
    Debug = True
if sys.argv[4] == 'remote':
    sample = sample_dict[sys.argv[1]]
    part_idx = sys.argv[2]
    file_list = list(map(str, sys.argv[3].strip('[]').split(',')))
else:
    file_list= list(map(str,sys.argv[3].strip('[]').split(',')))
    sample.label= sys.argv[1]
    part_idx = sys.argv[2]
    Debug=False
MCReco = True
DeltaFilter = True
bjetSwitch = False # True #
startTime = datetime.datetime.now()
print("Starting running at " + str(startTime))

ROOT.gROOT.SetBatch()

leadingjet_ptcut = 150.

chain = ROOT.TChain('Events')
#print(chain)
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

#++++++++++++++++++++++++++++++++++
#++   branching the new trees    ++
#++++++++++++++++++++++++++++++++++
outTreeFile = ROOT.TFile(sample.label+"_part"+str(part_idx)+".root", "RECREATE") # output file
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

systTree.setWeightName("LHESF", 1.)
systTree.setWeightName("LHEUp", 1.)
systTree.setWeightName("LHEDown", 1.)
systTree.setWeightName("puSF",1.)
systTree.setWeightName("puUp",1.)
systTree.setWeightName("puDown",1.)
systTree.setWeightName("lepSF",1.)
systTree.setWeightName("lepUp",1.)
systTree.setWeightName("lepDown",1.)
systTree.setWeightName("PFSF",1.)
systTree.setWeightName("PFUp",1.)
systTree.setWeightName("PFDown",1.)


#++++++++++++++++++++++++++++++++++
#++     variables to branch      ++
#++++++++++++++++++++++++++++++++++

def reco(scenario, isMC, addPDF, MCReco):
    isNominal = False
    if scenario == 'nominal':
        isNominal = True
    print(scenario)
    #++++++++++++++++++++++++++++++++++
    #++      Nominal category        ++
    #++++++++++++++++++++++++++++++++++
    #Reconstructed Tprime
    if MCReco:
        MC_Tprime_pt_nominal = array.array('f', [0.])
        MC_Tprime_eta_nominal = array.array('f', [0.])
        MC_Tprime_phi_nominal = array.array('f', [0.])
        MC_Tprime_m_nominal = array.array('f', [0.])
        MC_Tprime_mt_nominal = array.array('f', [0.])
        GenPart_Tprime_pt_nominal = array.array('f', [0.])
        GenPart_Tprime_eta_nominal = array.array('f', [0.])
        GenPart_Tprime_phi_nominal = array.array('f', [0.])
        GenPart_Tprime_m_nominal = array.array('f', [0.])
        GenPart_Tprime_mt_nominal = array.array('f', [0.])

    best_Tprime_pt_nominal = array.array('f', [0.])
    best_Tprime_eta_nominal = array.array('f', [0.])
    best_Tprime_phi_nominal = array.array('f', [0.])
    best_Tprime_m_nominal = array.array('f', [0.])
    best_Tprime_mt_nominal = array.array('f', [0.])
    
    #Reconstructed Top
    if MCReco:
        MC_RecoTop_pt_nominal = array.array('f', [0.])
        MC_RecoTop_eta_nominal = array.array('f', [0.])
        MC_RecoTop_phi_nominal = array.array('f', [0.])
        MC_RecoTop_m_nominal = array.array('f', [0.])
        MC_RecoTop_mt_nominal = array.array('f', [0.])
        GenPart_Top_pt_nominal = array.array('f', [0.])
        GenPart_Top_eta_nominal = array.array('f', [0.])
        GenPart_Top_phi_nominal = array.array('f', [0.])
        GenPart_Top_m_nominal = array.array('f', [0.])
        GenPart_Top_mt_nominal = array.array('f', [0.])
        MC_RecoTop_isNeg_nominal = array.array('i', [0])
        MC_RecoTop_chi2_nominal = array.array('i', [0])
    best_RecoTop_pt_nominal = array.array('f', [0.])
    best_RecoTop_eta_nominal = array.array('f', [0.])
    best_RecoTop_phi_nominal = array.array('f', [0.])
    best_RecoTop_m_nominal = array.array('f', [0.])
    best_RecoTop_mt_nominal = array.array('f', [0.])
    best_RecoTop_isNeg_nominal = array.array('i', [0])
    best_RecoTop_chi2_nominal = array.array('i', [0])
    best_RecoTop_costheta_nominal = array.array('f', [0.])
    best_RecoTop_costhetalep_nominal = array.array('f', [0.])
    best_RecoTop_high_truth_nominal = array.array('i', [0])    

    #Reconstructed Z
    if MCReco:
        MC_RecoZ_pt_nominal = array.array('f', [0.])
        MC_RecoZ_eta_nominal = array.array('f', [0.])
        MC_RecoZ_phi_nominal = array.array('f', [0.])
        MC_RecoZ_m_nominal = array.array('f', [0.])
        MC_RecoZ_mt_nominal = array.array('f', [0.])
        GenPart_Z_pt_nominal = array.array('f', [0.])
        GenPart_Z_eta_nominal = array.array('f', [0.])
        GenPart_Z_phi_nominal = array.array('f', [0.])
        GenPart_Z_m_nominal = array.array('f', [0.])
        GenPart_Z_mt_nominal = array.array('f', [0.])
        MC_RecoZ_chi2_nominal = array.array('i', [0])
    best_RecoZ_pt_nominal = array.array('f', [0.])
    best_RecoZ_eta_nominal = array.array('f', [0.])
    best_RecoZ_phi_nominal = array.array('f', [0.])
    best_RecoZ_m_nominal = array.array('f', [0.])
    best_RecoZ_mt_nominal = array.array('f', [0.])
    best_RecoZ_sub_b_nominal = array.array('i', [0])
    best_RecoZ_chi2_nominal = array.array('i', [0])

    #nZ or nH reco
    nZ_LP_nominal = array.array('i', [0])
    nZ_TP_nominal = array.array('i', [0])
    nZ_LPDeepTag_nominal = array.array('i', [0])
    nZ_TPDeepTag_nominal = array.array('i', [0])

    nH_LP_nominal = array.array('i', [0])
    nH_TP_nominal = array.array('i', [0])
    nH_LPDeepTag_nominal = array.array('i', [0])
    nH_TPDeepTag_nominal = array.array('i', [0])

    nTop_nominal = array.array('i', [0])


    
    MET_pt_nominal = array.array('f', [0.])
    MET_phi_nominal = array.array('f', [0.])
    

    
    w_nominal_nominal = array.array('f', [0.])
    w_PDF_nominal = array.array('f', [0.]*110)


    
    total_events = 1.
    lumi = {'2016': 35.9, "2017": 41.53, "2018": 59.7}
    #++++++++++++++++++++++++++++++++++
    #++   branching the new trees    ++
    #++++++++++++++++++++++++++++++++++
    if MCReco:
        systTree.branchTreesSysts(trees, scenario, "MC_Tprime_pt", outTreeFile, MC_Tprime_pt_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_Tprime_eta", outTreeFile, MC_Tprime_eta_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_Tprime_phi", outTreeFile, MC_Tprime_phi_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_Tprime_m", outTreeFile, MC_Tprime_m_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_Tprime_mt", outTreeFile, MC_Tprime_mt_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_Tprime_pt", outTreeFile, GenPart_Tprime_pt_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_Tprime_eta", outTreeFile, GenPart_Tprime_eta_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_Tprime_phi", outTreeFile, GenPart_Tprime_phi_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_Tprime_m", outTreeFile, GenPart_Tprime_m_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_Tprime_mt", outTreeFile, GenPart_Tprime_mt_nominal)

    systTree.branchTreesSysts(trees, scenario, "best_Tprime_pt", outTreeFile, best_Tprime_pt_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_Tprime_eta", outTreeFile, best_Tprime_eta_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_Tprime_phi", outTreeFile, best_Tprime_phi_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_Tprime_m", outTreeFile, best_Tprime_m_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_Tprime_mt", outTreeFile, best_Tprime_mt_nominal)
    

    if MCReco:
        systTree.branchTreesSysts(trees, scenario, "MC_top_pt", outTreeFile, MC_RecoTop_pt_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_top_eta", outTreeFile, MC_RecoTop_eta_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_top_phi", outTreeFile, MC_RecoTop_phi_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_top_m", outTreeFile, MC_RecoTop_m_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_top_mt", outTreeFile, MC_RecoTop_mt_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_top_pt", outTreeFile, GenPart_Top_pt_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_top_eta", outTreeFile, GenPart_Top_eta_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_top_phi", outTreeFile, GenPart_Top_phi_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_top_m", outTreeFile, GenPart_Top_m_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_top_mt", outTreeFile, GenPart_Top_mt_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_top_isNeg", outTreeFile, MC_RecoTop_isNeg_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_pt", outTreeFile, best_RecoTop_pt_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_eta", outTreeFile, best_RecoTop_eta_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_phi", outTreeFile, best_RecoTop_phi_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_m", outTreeFile, best_RecoTop_m_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_costheta", outTreeFile, best_RecoTop_costheta_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_costhetalep", outTreeFile, best_RecoTop_costhetalep_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_mt", outTreeFile, best_RecoTop_mt_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_isNeg", outTreeFile, best_RecoTop_isNeg_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_high_truth", outTreeFile, best_RecoTop_high_truth_nominal)

    if MCReco:
        systTree.branchTreesSysts(trees, scenario, "MC_Z_pt", outTreeFile, MC_RecoZ_pt_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_Z_eta", outTreeFile, MC_RecoZ_eta_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_Z_phi", outTreeFile, MC_RecoZ_phi_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_Z_m", outTreeFile, MC_RecoZ_m_nominal)
        systTree.branchTreesSysts(trees, scenario, "MC_Z_mt", outTreeFile, MC_RecoZ_mt_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_Z_pt", outTreeFile, GenPart_Z_pt_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_Z_eta", outTreeFile, GenPart_Z_eta_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_Z_phi", outTreeFile, GenPart_Z_phi_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_Z_m", outTreeFile, GenPart_Z_m_nominal)
        systTree.branchTreesSysts(trees, scenario, "GenPart_Z_mt", outTreeFile, GenPart_Z_mt_nominal)

    systTree.branchTreesSysts(trees, scenario, "best_Z_pt", outTreeFile, best_RecoZ_pt_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_Z_eta", outTreeFile, best_RecoZ_eta_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_Z_phi", outTreeFile, best_RecoZ_phi_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_Z_m", outTreeFile, best_RecoZ_m_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_Z_mt", outTreeFile, best_RecoZ_mt_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_Z_sub_b", outTreeFile, best_RecoZ_sub_b_nominal)
   
    systTree.branchTreesSysts(trees, scenario, "MET_pt", outTreeFile, MET_pt_nominal)
    systTree.branchTreesSysts(trees, scenario, "MET_phi", outTreeFile, MET_phi_nominal)

    """ 
    nZ or nH branching
    """

    systTree.branchTreesSysts(trees, scenario, "nZ_LP", outTreeFile, nZ_LP_nominal)
    systTree.branchTreesSysts(trees, scenario, "nZ_TP", outTreeFile, nZ_TP_nominal)
    systTree.branchTreesSysts(trees, scenario, "nZ_LPDeepTag", outTreeFile, nZ_LPDeepTag_nominal)
    systTree.branchTreesSysts(trees, scenario, "nZ_TPDeepTag", outTreeFile, nZ_TPDeepTag_nominal)

    systTree.branchTreesSysts(trees, scenario, "nH_LP", outTreeFile, nH_LP_nominal)
    systTree.branchTreesSysts(trees, scenario, "nH_TP", outTreeFile, nH_TP_nominal)
    systTree.branchTreesSysts(trees, scenario, "nH_LPDeepTag", outTreeFile, nH_LPDeepTag_nominal)
    systTree.branchTreesSysts(trees, scenario, "nH_TPDeepTag", outTreeFile, nH_TPDeepTag_nominal)

    systTree.branchTreesSysts(trees, scenario, "nTop", outTreeFile, nTop_nominal)



   
    #print("Is MC: " + str(isMC) + "      option addPDF: " + str(addPDF))
    if(isMC and addPDF):
        systTree.branchTreesSysts(trees, scenario, "w_PDF", outTreeFile, w_PDF_nominal)
    if('TT_' in sample.label): 
        systTree.branchTreesSysts(trees, scenario, "nlep", outTreeFile, nlep_nominal)
    ################################################################################################################################################################################################################################
    
    #++++++++++++++++++++++++++++++++++
    #++      taking MC weights       ++
    #++++++++++++++++++++++++++++++++++
    print("isMC: ", isMC)
    """
    if(isMC):
        h_genweight = ROOT.TH1F()
        h_genweight.SetNameTitle('h_genweight', 'h_genweight')
        h_PDFweight = ROOT.TH1F()
        h_PDFweight.SetNameTitle("h_PDFweight","h_PDFweight")
        for infile in file_list: 
            newfile = ROOT.TFile.Open(infile)
            dirc = ROOT.TDirectory()
            dirc = newfile.Get("plots")
            h_genw_tmp = ROOT.TH1F(dirc.Get("h_genweight"))
            if(dirc.GetListOfKeys().Contains("h_PDFweight")):
                h_pdfw_tmp = ROOT.TH1F(dirc.Get("h_PDFweight"))
                
                if(ROOT.TH1F(h_PDFweight).Integral() < 1.):
                    h_PDFweight.SetBins(h_pdfw_tmp.GetXaxis().GetNbins(), h_pdfw_tmp.GetXaxis().GetXmin(), h_pdfw_tmp.GetXaxis().GetXmax())
                    print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(ROOT.TH1F(dirc.Get("h_genweight")).GetBinContent(1), ROOT.TH1F(dirc.Get("h_PDFweight")).GetNbinsX()))
                h_PDFweight.Add(h_pdfw_tmp)
            else:
                addPDF = False
            if(ROOT.TH1F(h_genweight).Integral() < 1.):
                h_genweight.SetBins(h_genw_tmp.GetXaxis().GetNbins(), h_genw_tmp.GetXaxis().GetXmin(), h_genw_tmp.GetXaxis().GetXmax())
            h_genweight.Add(h_genw_tmp)
        print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genweight.GetBinContent(1), h_PDFweight.GetNbinsX()))
        lheweight = h_genweight.GetBinContent(2)/h_genweight.GetBinContent(1)
    """
    #++++++++++++++++++++++++++++++++++
    #++      Efficiency studies      ++
    #++++++++++++++++++++++++++++++++++
    neutrino_failed = 0
    nrecochi = 0
    nrecoclosest = 0
    nrecosublead = 0
    nrecobest = 0
    nbinseff = 10
    h_eff_mu = ROOT.TH1D("h_eff_mu", "h_eff_mu", nbinseff, 0, nbinseff)
    h_eff_ele = ROOT.TH1D("h_eff_ele", "h_eff_ele", nbinseff, 0, nbinseff)
    h_cutFL= ROOT.TH1F("h_cutFL","h_cutFL",4,0,4)
    h_cutFL.Fill("Total",200000)
    h_cutFL.SetBinError(0,173)
    h_MC_topM   = ROOT.TH1F("h_MC_top","",30,1,-1)
    h_best_topM = ROOT.TH1F("h_best_top","",30,1,-1)
    
    #++++++++++++++++++++++++++++++++++
    #++   looping over the events    ++
    #++++++++++++++++++++++++++++++++++
    for i in range(tree.GetEntries()):
        w_nominal_nominal[0] = 1.

        # tree.GetEntry(i)
        # print(tree.Top_Score[0])
        #++++++++++++++++++++++++++++++++++
        #++        taking objects        ++
        #++++++++++++++++++++++++++++++++++
        if Debug:
            #print("evento n. " + str(i))
            if i > 2000:
                break
                
        if not Debug and i%5000 == 0:
            print("Event #", i+1, " out of ", tree.GetEntries())
        h_cutFL.Fill("Preselection",1)
        event = Event(tree,i)
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        njets = len(jets)
        fatjets = Collection(event, "FatJet")
        HT = Object(event, "HT")
        PV = Object(event, "PV")
        HLT = Object(event, "HLT")
        Flag = Object(event, 'Flag')
        met = Object(event, "MET")        
        MET = {'metPx': met.pt*ROOT.TMath.Cos(met.phi), 'metPy': met.pt*ROOT.TMath.Sin(met.phi)}
        Top = Collection(event, "Top")
        genpart = None
        
        h_eff_mu.Fill('Total', 1)
        h_eff_ele.Fill('Total', 1)
        if isMC:
            genpart = Collection(event, "GenPart")
            LHE = Collection(event, "LHEPart")
            LHEScaleWeight = Collection(event, 'LHEScaleWeight')
            lheSF = 1.
            lheUp = 1.
            lheDown = 1.
            """
            if len(LHEScaleWeight) > 1:
                lhemin = min([LHEScaleWeight[g].__getattr__("") for g in range(len(LHEScaleWeight))])
                lhemax = max([LHEScaleWeight[g].__getattr__("") for g in range(len(LHEScaleWeight))])
                lheSF = lheweight * LHEScaleWeight[4].__getattr__("")
                lheUp = lheweight * lhemax
                lheDown = lheweight * lhemin
            """
            systTree.setWeightName("LHESF", copy.deepcopy(lheSF))
            systTree.setWeightName("LHEUp", copy.deepcopy(lheUp))
            systTree.setWeightName("LHEDown", copy.deepcopy(lheDown))

        chain.GetEntry(i)

        if scenario == 'jesUp':
            MET = {'metPx': met.pt_jesTotalUp*ROOT.TMath.Cos(met.phi_jesTotalUp), 'metPy': met.pt_jesTotalUp*ROOT.TMath.Sin(met.phi_jesTotalUp)}
            for jet in jets:
                jet.pt = jet.pt_jesTotalUp
                jet.mass = jet.mass_jesTotalUp 
            for fatjet in fatjets:
                fatjet.pt = fatjet.pt_jesTotalUp
                fatjet.mass = fatjet.mass_jesTotalUp 
                fatjet.msoftdrop = fatjet.msoftdrop_jesTotalUp
        elif scenario == 'jesDown':
            MET = {'metPx': met.pt_jesTotalDown*ROOT.TMath.Cos(met.phi_jesTotalDown), 'metPy': met.pt_jesTotalDown*ROOT.TMath.Sin(met.phi_jesTotalDown)}
            for jet in jets:
                jet.pt = jet.pt_jesTotalDown
                jet.mass = jet.mass_jesTotalDown 
            for fatjet in fatjets:
                fatjet.pt = fatjet.pt_jesTotalDown
                fatjet.mass = fatjet.mass_jesTotalDown 
                fatjet.msoftdrop = fatjet.msoftdrop_jesTotalDown
        elif scenario == 'jerUp':
            MET = {'metPx': met.pt_jerUp*ROOT.TMath.Cos(met.phi_jerUp), 'metPy': met.pt_jerUp*ROOT.TMath.Sin(met.phi_jerUp)}
            for jet in jets:
                jet.pt = jet.pt_jerUp
                jet.mass = jet.mass_jerUp 
            for fatjet in fatjets:
                fatjet.pt = fatjet.pt_jerUp
                fatjet.mass = fatjet.mass_jerUp 
                fatjet.msoftdrop = fatjet.msoftdrop_jerUp
        elif scenario == 'jerDown':
            MET = {'metPx': met.pt_jerDown*ROOT.TMath.Cos(met.phi_jerDown), 'metPy': met.pt_jerDown*ROOT.TMath.Sin(met.phi_jerDown)}
            for jet in jets:
                jet.pt = jet.pt_jerDown
                jet.mass = jet.mass_jerDown 
            for fatjet in fatjets:
                fatjet.pt = fatjet.pt_jerDown
                fatjet.mass = fatjet.mass_jerDown 
                fatjet.msoftdrop = fatjet.msoftdrop_jerDown
        #++++++++++++++++++++++++++++++++++
        #++      defining variables      ++
        #++++++++++++++++++++++++++++++++++
        tightlep = None
        tightlep_p4 = None
        tightlep_p4t = None
        tightlep_SF = None
        tightlep_SFUp = None
        tightlep_SFDown = None
        recomet_p4t = None
        PF_SF = None
        PF_SFUp = None
        PF_SFDown = None
        PU_SF = None
        PU_SFUp = None
        PU_SFDown = None
        #++++++++++++++++++++++++++++++++++
        #++    starting the analysis     ++
        #++++++++++++++++++++++++++++++++++
        VetoMu = get_LooseMu(muons)
        goodMu = get_Mu(muons)
        VetoEle = get_LooseEle(electrons)
        goodEle = get_Ele(electrons)
        sample.year = "2017"
        #year = sample.year
        if(isMC):
            runPeriod = None
        else:
            runPeriod = sample.runP
        passmu, passEle, passHT,passph, noTrigger = trig_map(HLT, sample.year, runPeriod,None)
        """
        passed_mu_nominal[0] = int(passMu)
        passed_ele_nominal[0] = int(passEle)
        passed_ht_nominal[0] = int(passHT)
        """
        isMuon=(len(goodMu) == 1)
        isElectron=(len(goodEle) == 1)
        #isMuon = (len(goodMu) == 1) and (len(goodEle) == 0) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passMu or passHT)
        #isElectron = (len(goodMu) == 0) and (len(goodEle) == 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passEle or passHT)

        if(isMC):
            doublecounting = False
        else:
            doublecounting = True
        #Double counting removal
        if('DataMu' in sample.label and passMu):
            doublecounting = False
        if('DataEle' in sample.label and (not passMu and passEle)):
            doublecounting = False
        if('DataHT' in sample.label and (passHT and not passMu and not passEle)):
            doublecounting = False
            
        if doublecounting:
            continue

        #######################################
        ## Removing events with HEM problem  ##
        #######################################
        passesMETHEMVeto = HEMveto(jets, electrons)
        if(sample.year == 2018 and not passesMETHEMVeto):
            if(not isMC and chain.run > 319077.):
                continue
            elif(isMC):
                w_nominal_nominal[0] *= 0.354
                
        if len(goodMu) == 1:
            h_eff_mu.Fill('Good Mu', 1)
            if len(goodEle) == 0:
                h_eff_mu.Fill('Good Ele', 1)
            if len(VetoMu) == 0:
                h_eff_mu.Fill('Veto Mu', 1)
            if len(VetoEle) == 0:
                h_eff_mu.Fill('Veto Ele', 1)
        if len(goodEle) == 1:
            h_eff_ele.Fill('Good Ele', 1)
            if len(goodMu) == 0:
                h_eff_ele.Fill('Good Mu', 1)
            if len(VetoMu) == 0:
                h_eff_ele.Fill('Veto Mu', 1)
            if len(VetoEle) == 0:
                h_eff_ele.Fill('Veto Ele', 1)

        ######################################
        ## Selecting only jets with pt>100  ##
        ######################################
        btagreco = False
        goodJets = get_Jet(jets, 100)
        bjets, nobjets = bjet_filter(goodJets, 'DeepFlv', 'L')
        bjets_all = bjet_filter(jets, 'DeepFlv', 'L')
        if(len(bjets) > 1):
            btagreco = True
       
        #if Debug:
        #print("len bjets: ", len(bjets), "nbJet_pt100_nominal: ", nbJet_pt100_nominal[0])

        ##print(len(fatjets))
        #++++++++++++++++++++++++++++++++++
        #++    plots for lep-jet dis     ++
        #++++++++++++++++++++++++++++++++++
        #lepjet,drmin = closest(tightlep, get_Jet(jets, 15))
        #ptrel = get_ptrel(tightlep, lepjet)
        #if(isMuon):
        #    h_drmin_ptrel_mu.Fill(drmin,ptrel)
        if(len(goodJets) >= 2):
            if isMuon:
                h_eff_mu.Fill('good jets >2', int(isMuon))
            elif isElectron:
                h_eff_ele.Fill('good jets >2', int(isElectron))
        if(len(fatjets) >= 2):
            if isMuon:
                h_eff_mu.Fill('fat jets >2', int(isMuon))
            elif isElectron:
                h_eff_ele.Fill('fat jets >2', int(isElectron))
                
        #if (len(goodJets) < 2 or len(fatjets) < 2):
            #continue
            
        if isMuon:
            h_eff_mu.Fill('passMu+jetsel', int(isMuon))
        elif isElectron:
            h_eff_ele.Fill('passEle+jetsel', int(isElectron))
        """
        if(isMuon):
            isEle_nominal[0] = 0
            isMu_nominal[0] = 1
            tightlep = goodMu[0]
            tightlep_p4 = copy.deepcopy(tightlep.p4())#ROOT.TLorentzVector()
            tightlep_p4t = copy.deepcopy(tightlep.p4())
            tightlep_p4t.SetPz(0.)
            if(isMC):
                tightlep_SF = goodMu[0].effSF
                tightlep_SFUp = goodMu[0].effSF_errUp
                tightlep_SFDown = goodMu[0].effSF_errDown
                systTree.setWeightName("lepSF", copy.deepcopy(tightlep_SF))
                systTree.setWeightName("lepUp", copy.deepcopy(tightlep_SFUp))
                systTree.setWeightName("lepDown", copy.deepcopy(tightlep_SFDown))
        elif(isElectron):
            isEle_nominal[0] = 1
            isMu_nominal[0] = 0
            tightlep = goodEle[0]
            tightlep_p4 = ROOT.TLorentzVector()
            tightlep_p4.SetPtEtaPhiM(goodEle[0].pt,goodEle[0].eta,goodEle[0].phi,goodEle[0].mass)
            tightlep_p4t = copy.deepcopy(tightlep.p4())
            tightlep_p4t.SetPz(0.)
            if(isMC):
                tightlep_SF = goodEle[0].effSF
                tightlep_SFUp = goodEle[0].effSF_errUp
                tightlep_SFDown = goodEle[0].effSF_errDown
                systTree.setWeightName("lepSF", copy.deepcopy(tightlep_SF))
                systTree.setWeightName("lepUp", copy.deepcopy(tightlep_SFUp))
                systTree.setWeightName("lepDown", copy.deepcopy(tightlep_SFDown))
        else:
            ##print('Event %i not a good' %(i))
            continue
        """
        recotop = TopUtilities()
        #veto on events with "pathological" reco neutrino
        #tent_neutrino = recotop.NuMomentum(tightlep.p4().Px(), tightlep.p4().Py(), tightlep.p4().Pz(), tightlep.p4().Pt(), tightlep.p4().E(), MET['metPx'], MET['metPy'])
        ##print(" <<<<<<<<<<<<<<<<<<<<<<<< lepton is %f " %tightlep.p4().M())
        #if tent_neutrino[0] == None:
        #    neutrino_failed += 1
        #    continue

        """
        if(isMC):
            PF_SF = chain.PrefireWeight
            PF_SFUp = chain.PrefireWeight_Up
            PF_SFDown = chain.PrefireWeight_Down
            systTree.setWeightName("PFSF", copy.deepcopy(PF_SF))
            systTree.setWeightName("PFUp", copy.deepcopy(PF_SFUp))
            systTree.setWeightName("PFDown", copy.deepcopy(PF_SFDown))
            
            PU_SF = chain.puWeight
            PU_SFUp = chain.puWeightUp
            PU_SFDown = chain.puWeightDown
            systTree.setWeightName("puSF", copy.deepcopy(PU_SF))
            systTree.setWeightName("puUp", copy.deepcopy(PU_SFUp))
            systTree.setWeightName("puDown", copy.deepcopy(PU_SFDown))
            
            btagSF, btagUp, btagDown = btagcalc(goodJets)
            systTree.setWeightName("btagSF", copy.deepcopy(btagSF))
            systTree.setWeightName("btagUp", copy.deepcopy(btagUp))
            systTree.setWeightName("btagDown", copy.deepcopy(btagDown))

            mistagSF, mistagUp, mistagDown = mistagcalc(goodJets)
            systTree.setWeightName("mistagSF", copy.deepcopy(mistagSF))
            systTree.setWeightName("mistagUp", copy.deepcopy(mistagUp))
            systTree.setWeightName("mistagDown", copy.deepcopy(mistagDown))
        """
        recomet_p4t = ROOT.TLorentzVector()
        recomet_p4t.SetPtEtaPhiM(met.pt, 0., met.phi, 0)
        
        MET_pt_nominal[0] = met.pt
        MET_phi_nominal[0] = met.phi
        
    
            

            
        # requiring mtt < 700 to merge inclusive tt with the mtt > 700
        if('TT_incl' in sample.label):
            top_q4 = ROOT.TLorentzVector()  
            antitop_q4 = ROOT.TLorentzVector()  
            tt_q4 = ROOT.TLorentzVector()  
            for genp in genpart:
                if(genp.genPartIdxMother_prompt == 0 and genp.pdgId == 6):
                    top_q4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
                elif(genp.genPartIdxMother_prompt == 0 and genp.pdgId == -6):
                    antitop_q4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
            tt_q4 = top_q4 + antitop_q4
            if(tt_q4.M() > 700.):
                w_nominal_nominal[0] *= 0 #trick to make the events with mtt > 700 count zero

        # trying to understand the composition of the ttbar background
        if('TT_' in sample.label):
            lhe_ele = 0
            lhe_mu = 0
            lhe_tau = 0
            nlep_nominal[0] = 0
            for lhep in LHE:
                if(abs(lhep.pdgId) == 11):
                    lhe_ele += 1
                elif(abs(lhep.pdgId) == 13):
                    lhe_mu += 1
                elif(abs(lhep.pdgId) == 15):
                    for genp in genpart:
                        ##print("pdg id " + str(genp.pdgId) + " and mother is " + str(genp.genPartIdxMother))
                        if((abs(genp.pdgId) == 11 or abs(genp.pdgId) == 13) and genp.genPartIdxMother_prompt > 0):
                            ##print(" with pdg id " + str(genpart[int(genp.genPartIdxMother)].pdgId))
                            abs(genpart[genp.genPartIdxMother_prompt].pdgId) == 15
                            lhe_tau += 1 #inventare un modo per contare eventi leptonici da tau
            #nlep_nominal[0] = lhe_ele + lhe_mu + lhe_tau
                            
        # checking the top 4-vector at LHE level 
        if Debug and isMC:
            for genp in genpart:
                if(abs(genp.pdgId) == 6):
                    top_q4 = ROOT.TLorentzVector()
                    top_q4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
                    ##print( " top 4-vector at GEN level is (%f, %f, %f, %f) and mass %f "%(genp.pt, genp.eta, genp.phi, top_q4.E(), top_q4.M()))
                    
        
   

        #MCtruth event reconstruction
        if MCReco:
            #GenParticles
            gentopFound = False
            genZFound = False
            #genHFound = False
            gentop_p4 = ROOT.TLorentzVector()
            genZ_p4 = ROOT.TLorentzVector()
            #genH_p4 = ROOT.TLorentzVector()

            if('tZq' in sample.label): PDGID=23   #For the moment like this, when bckg maybe define Signal_Type=sys.argv[], where Z or H
            if('tHq' in sample.label): PDGID=25
            for genp in genpart:
                if gentopFound == True and genZFound == True:
                    break

                if abs(genp.pdgId) == 6 and gentopFound == False:
                    if genp.genPartIdxMother_prompt >-1 and abs(genpart[genp.genPartIdxMother].pdgId)!=6:
                        gentop_p4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
                        gentopFound = True
                if abs(genp.pdgId) == PDGID and genZFound == False:
                    if genp.genPartIdxMother_prompt >-1 and genpart[genp.genPartIdxMother].pdgId!=PDGID:
                        genZ_p4.SetPtEtaPhiM(genp.pt, genp.eta, genp.phi, genp.mass)
                        genZFound = True
                #else:
                    #continue

            ##print(gentop, genbott)
            if gentopFound and genZFound:
                genTprime_p4 = gentop_p4 + genZ_p4
                GenPart_Tprime_m_nominal[0] = genTprime_p4.M()
                GenPart_Tprime_mt_nominal[0] = genTprime_p4.Mt()
                GenPart_Tprime_pt_nominal[0] = genTprime_p4.Pt()
                GenPart_Tprime_eta_nominal[0] = genTprime_p4.Eta()
                GenPart_Tprime_phi_nominal[0] = genTprime_p4.Phi()
            else:
                GenPart_Tprime_m_nominal[0] = -100.
                GenPart_Tprime_mt_nominal[0] = -100.
                GenPart_Tprime_pt_nominal[0] = -100.
                GenPart_Tprime_eta_nominal[0] = -100.
                GenPart_Tprime_phi_nominal[0] = -100.

            if  gentopFound==False:
                GenPart_Top_m_nominal[0] = -100.
                GenPart_Top_mt_nominal[0] = -100.
                GenPart_Top_pt_nominal[0] = -100.
                GenPart_Top_eta_nominal[0] = -100.
                GenPart_Top_phi_nominal[0] = -100.
            else:
                GenPart_Top_m_nominal[0] = gentop_p4.M()
                GenPart_Top_mt_nominal[0] = gentop_p4.Mt()
                GenPart_Top_pt_nominal[0] = gentop_p4.Pt()
                GenPart_Top_eta_nominal[0] = gentop_p4.Eta()
                GenPart_Top_phi_nominal[0] = gentop_p4.Phi()

            if genZFound==False:
                GenPart_Z_m_nominal[0] = -100.
                GenPart_Z_mt_nominal[0] = -100.
                GenPart_Z_pt_nominal[0] = -100.
                GenPart_Z_eta_nominal[0] = -100.
                GenPart_Z_phi_nominal[0] = -100.
            else:
                GenPart_Z_m_nominal[0] = genZ_p4.M()
                GenPart_Z_mt_nominal[0] = genZ_p4.Mt()
                GenPart_Z_pt_nominal[0] = genZ_p4.Pt()
                GenPart_Z_eta_nominal[0] = genZ_p4.Eta()
                GenPart_Z_phi_nominal[0] = genZ_p4.Phi()

           

            
            foundMCtrue_top=False
            for top in Top:
                if top.High_Truth==0:
                    MC_RecoTop_m_nominal[0] = top.nu_M
                    MC_RecoTop_mt_nominal[0] = -100.
                    MC_RecoTop_pt_nominal[0] = top.nu_pt
                    MC_RecoTop_eta_nominal[0] = top.nu_eta
                    MC_RecoTop_phi_nominal[0] = top.nu_phi
                    MC_RecoTop_isNeg_nominal[0] = -1
                    foundMCtrue_top=True
                    h_MC_topM.Fill(MC_RecoTop_m_nominal[0])
            if foundMCtrue_top==False:
                MC_RecoTop_m_nominal[0] = -100.
                MC_RecoTop_mt_nominal[0] = -100.
                MC_RecoTop_pt_nominal[0] = -100.
                MC_RecoTop_eta_nominal[0] = -100.
                MC_RecoTop_phi_nominal[0] = -100.
                #h_MC_topM.Fill(MC_RecoTop_m_nominal[0])

            foundMctrue_Z=False
            for fatjet in fatjets:
                for gen in genpart:
                    if abs(gen.pdgId) == PDGID:
                        if genpart[gen.genPartIdxMother].pdgId!=PDGID:
                            genZ_p4.SetPtEtaPhiM(gen.pt, gen.eta, gen.phi, gen.mass)
                            fatjet_p4 = ROOT.TLorentzVector()
                            fatjet_p4.SetPtEtaPhiM(fatjet.pt, fatjet.eta, fatjet.phi, fatjet.mass)
                            if deltaR(fatjet_p4.Eta(), fatjet_p4.Phi(), genZ_p4.Eta(), genZ_p4.Phi())<0.4: #Originally 0.1, Orso suggests 0.4 maybe
                                MC_RecoZ_m_nominal[0] = fatjet_p4.M()
                                MC_RecoZ_mt_nominal[0] = fatjet_p4.Mt()
                                MC_RecoZ_pt_nominal[0] = fatjet_p4.Pt()
                                MC_RecoZ_eta_nominal[0] = fatjet_p4.Eta()
                                MC_RecoZ_phi_nominal[0] = fatjet_p4.Phi()
                                foundMctrue_Z= True


            if foundMctrue_Z ==False:
                MC_RecoZ_m_nominal[0] = -100.
                MC_RecoZ_mt_nominal[0] = -100.
                MC_RecoZ_pt_nominal[0] = -100.
                MC_RecoZ_eta_nominal[0] = -100.
                MC_RecoZ_phi_nominal[0] = -100.

            if (foundMctrue_Z==True and foundMCtrue_top==True):
                Z_p4 = ROOT.TLorentzVector()
                Z_p4.SetPtEtaPhiM(MC_RecoZ_pt_nominal[0],MC_RecoZ_eta_nominal[0],MC_RecoZ_phi_nominal[0],MC_RecoZ_m_nominal[0])
                Top_p4 = ROOT.TLorentzVector()
                Top_p4.SetPtEtaPhiM(MC_RecoTop_pt_nominal[0],MC_RecoTop_eta_nominal[0],MC_RecoTop_phi_nominal[0],MC_RecoTop_m_nominal[0])
                Tprime_p4= Z_p4 + Top_p4
                MC_Tprime_m_nominal[0] = Tprime_p4.M()
                MC_Tprime_mt_nominal[0] = Tprime_p4.Mt()
                MC_Tprime_pt_nominal[0] = Tprime_p4.Pt()
                MC_Tprime_eta_nominal[0] = Tprime_p4.Eta()
                MC_Tprime_phi_nominal[0] = Tprime_p4.Phi()  
            else : 

                MC_Tprime_m_nominal[0] = -100.
                MC_Tprime_mt_nominal[0] = -100.
                MC_Tprime_pt_nominal[0] = -100.
                MC_Tprime_eta_nominal[0] = -100.
                MC_Tprime_phi_nominal[0] = -100.

            

            
                
                    
        Zfatjets = list(filter(lambda x : x.msoftdrop>60 and x.msoftdrop<105  and (x.tau2/x.tau1)<0.75, fatjets))
        Hfatjets = list(filter(lambda x : x.msoftdrop>105 and x.msoftdrop<140 and (x.tau2/x.tau1)<0.75, fatjets))
        #Hfatjets = list(filter(lambda x : x.msoftdrop>105 and x.msoftdrop<140 and x.deepTagMD_HbbvsQCD>0.8, fatjets))



        nZ_LP_nominal[0] = len(list(filter(lambda x : x.msoftdrop>60 and x.msoftdrop<105  and (x.tau2/x.tau1)<0.75, fatjets)))        
        nZ_TP_nominal[0] = len(list(filter(lambda x : x.msoftdrop>60 and x.msoftdrop<105  and (x.tau2/x.tau1)<0.35 , fatjets))) # da vedere
        nZ_LPDeepTag_nominal[0] = len(list(filter(lambda x : x.msoftdrop>60 and x.msoftdrop<105 and x.deepTagMD_ZvsQCD>0.25, fatjets)))
        nZ_TPDeepTag_nominal[0] = len(list(filter(lambda x : x.msoftdrop>60 and x.msoftdrop<105 and x.deepTagMD_ZvsQCD>0.73, fatjets)))

        nH_LP_nominal[0] = len(list(filter(lambda x : x.msoftdrop>105 and x.msoftdrop<140 and (x.tau2/x.tau1)<0.75, fatjets)))
        nH_TP_nominal[0] = len(list(filter(lambda x : x.msoftdrop>105 and x.msoftdrop<140 and (x.tau2/x.tau1)<0.35 , fatjets))) # da vedere
        nH_LPDeepTag_nominal[0] = len(list(filter(lambda x : x.msoftdrop>105 and x.msoftdrop<140 and x.deepTagMD_HbbvsQCD>0.8, fatjets)))
        nH_TPDeepTag_nominal[0] = len(list(filter(lambda x : x.msoftdrop>105 and x.msoftdrop<140 and x.deepTagMD_HbbvsQCD>0.9, fatjets)))

       
        nSub_b=0

        if len(Zfatjets)>0:
            h_cutFL.Fill("nZ>0",1)
            dR_sub_b1= 999
            dR_sub_b2= 999
            sub_b1=None
            sub_b2 =None
            bjets_all= list(filter(lambda x : x.btagDeepFlavB>=0.0494, jets))
            if (len(bjets_all)>0): sub_b1, dR_sub_b1 = closest(Zfatjets[0],bjets_all)
            if (sub_b1!=None):
                bjets_all.remove(sub_b1)
                sub_b2, dR_sub_b2 = closest(Zfatjets[0],bjets_all)
            if (dR_sub_b1 <=0.4 or dR_sub_b2<=0.4):
                if (dR_sub_b1 <=0.4 and dR_sub_b2<=0.4): nSub_b=2
                else: nSub_b=1
       

        #top_recobjet = list(filter(lambda x : jets[int(x.bjet_index)].btagDeepFlavB>=0.0494 and ( ( x.el_index!=-1 and ( (x.Is_dR_merg==0 and electrons[int(x.el_index)].mvaFall17V2noIso_WP90==1 and electrons[int(x.el_index)].pfRelIso03_all<0.12 and x.pt_rel>22.0 and x.nu_M>139.0) or (x.Is_dR_merg==1 and electrons[int(x.el_index)].miniPFRelIso_all<0.1 and electrons[int(x.el_index)].mvaFall17V2noIso_WPL==1 and x.pt_rel>5.0 and (electrons[int(x.el_index)].pt/jets[int(x.bjet_index)].pt)<0.6 and abs(electrons[x.el_index].dxy)<0.005) ) ) or ( x.mu_index!=-1 and ( (x.Is_dR_merg==0 and muons[int(x.mu_index)].pfRelIso04_all<0.13 and x.pt_rel>22.0 and x.nu_M>130.0) or (x.Is_dR_merg==1 and abs(muons[int(x.mu_index)].dxy)<0.002 and x.pt_rel>5.0 and (muons[int(x.mu_index)].pt/jets[int(x.bjet_index)].pt)<0.65 and muons[int(x.mu_index)].miniPFRelIso_all<0.25) ) ) ), Top))

        #print(type(Top[0].nu_pt))
        #print(type(Top[0].Score))
        #print(Top[0].Score)
        top_recobjet = list(filter(lambda x : ( ( x.el_index!=-1 and ( x.Is_dR_merg==0 and ((x.nu_pt<=500 and x.Score>0.71) or (x.nu_pt>500 and x.Score>0.889)) or x.Is_dR_merg==1 and ((x.nu_pt<=500 and x.Score>0.603) or (x.nu_pt>500 and x.Score>0.625)) ) ) or ( x.mu_index!=-1 and ( x.Is_dR_merg==0 and ((x.nu_pt<=500 and x.Score>0.664) or (x.nu_pt>500 and x.Score>0.894)) or x.Is_dR_merg==1 and ((x.nu_pt<=500 and x.Score>0.661) or (x.nu_pt>500 and x.Score>0.526)) ) ) ), Top))



        #top_recobjet = list(filter(lambda x : jets[int(x.bjet_index)].btagDeepFlavB>=0.0494 and (x.el_index!=-1 or x.mu_index!=-1), Top))
        #list(filter(lambda x : jets[x.bjet_index] in bjets_all, Top))
        #if len(top_recobjet)==0:
            #continue
        top_recobjet.sort(key = lambda x: x.pt, reverse = True)

        nTop_nominal[0] = len(top_recobjet)

     
        
        highptJets = get_Jet(goodJets, leadingjet_ptcut)
        #if len(highptJets) < 1:
            #continue

        if btagreco:
            goodJets = copy.copy(bjets)
            highptJets = get_Jet(goodJets, leadingjet_ptcut)
        
        #if ( (len(Zfatjets)>0 or len(Hfatjets)>0) and len(top_recobjet)>0 ):
        if ( len(Hfatjets)>0 and len(top_recobjet)>0 ):
            h_cutFL.Fill("nRecoTop_stdcut>0",1)
            besttop_p4 =ROOT.TLorentzVector()  
            besttop_p4.SetPtEtaPhiM(top_recobjet[0].nu_pt,top_recobjet[0].nu_eta,top_recobjet[0].nu_phi,top_recobjet[0].nu_M)
            
            #if(len(Zfatjets)>0 and len(Hfatjets)==0):
            #    bestZ_p4 = Zfatjets[0].p4()
            #if(len(Zfatjets)==0 and len(Hfatjets)>0):
            #    bestZ_p4 = Hfatjets[0].p4()
            #if(len(Zfatjets)>0 and len(Hfatjets)>0):
            #    bestZ_p4 = Hfatjets[0].p4()
            
            bestZ_p4 = Hfatjets[0].p4()

            bestTprime_p4 = besttop_p4 + bestZ_p4
            best_Tprime_m_nominal[0] = bestTprime_p4.M()
            best_Tprime_mt_nominal[0] = bestTprime_p4.Mt()
            best_Tprime_pt_nominal[0] = bestTprime_p4.Pt()
            best_Tprime_eta_nominal[0] = bestTprime_p4.Eta()
            best_Tprime_phi_nominal[0] = bestTprime_p4.Phi()

            best_RecoTop_m_nominal[0] = besttop_p4.M()
            best_RecoTop_mt_nominal[0] = besttop_p4.Mt()
            best_RecoTop_pt_nominal[0] = besttop_p4.Pt()
            best_RecoTop_eta_nominal[0] = besttop_p4.Eta()
            best_RecoTop_phi_nominal[0] = besttop_p4.Phi()
            best_RecoTop_high_truth_nominal[0] = top_recobjet[0].High_Truth
            h_best_topM.Fill(best_RecoTop_m_nominal[0])

            best_RecoZ_m_nominal[0] = bestZ_p4.M()
            best_RecoZ_mt_nominal[0] = bestZ_p4.Mt()
            best_RecoZ_pt_nominal[0] = bestZ_p4.Pt()
            best_RecoZ_eta_nominal[0] = bestZ_p4.Eta()
            best_RecoZ_phi_nominal[0] = bestZ_p4.Phi()
            best_RecoZ_sub_b_nominal[0] = nSub_b
        else:
            best_Tprime_m_nominal[0] = -100.
            best_Tprime_mt_nominal[0] = -100.
            best_Tprime_pt_nominal[0] = -100.
            best_Tprime_eta_nominal[0] = -100.
            best_Tprime_phi_nominal[0] = -100.
            best_RecoTop_m_nominal[0] = -100.
            best_RecoTop_mt_nominal[0] = -100.
            best_RecoTop_pt_nominal[0] = -100.
            best_RecoTop_eta_nominal[0] = -100.
            best_RecoTop_phi_nominal[0] = -100.
            best_RecoTop_high_truth_nominal[0] = -1
            #h_best_topM.Fill(best_RecoTop_m_nominal[0])
            

            best_RecoZ_m_nominal[0] = -100.
            best_RecoZ_mt_nominal[0] = -100.
            best_RecoZ_pt_nominal[0] = -100.
            best_RecoZ_eta_nominal[0] = -100.
            best_RecoZ_phi_nominal[0] = -100.
            best_RecoZ_sub_b_nominal[0] = -1

        """
        if ( len(top_recobjet)>0 ):
            h_cutFL.Fill("nRecoTop_stdcut>0",1)
            besttop_p4 =ROOT.TLorentzVector()  
            besttop_p4.SetPtEtaPhiM(top_recobjet[0].nu_pt,top_recobjet[0].nu_eta,top_recobjet[0].nu_phi,top_recobjet[0].nu_M)

            best_RecoTop_m_nominal[0] = besttop_p4.M()
            best_RecoTop_mt_nominal[0] = besttop_p4.Mt()
            best_RecoTop_pt_nominal[0] = besttop_p4.Pt()
            best_RecoTop_eta_nominal[0] = besttop_p4.Eta()
            best_RecoTop_phi_nominal[0] = besttop_p4.Phi()
            best_RecoTop_high_truth_nominal[0] = top_recobjet[0].High_Truth
            h_best_topM.Fill(best_RecoTop_m_nominal[0])
        else:
            best_RecoTop_m_nominal[0] = -100.
            best_RecoTop_mt_nominal[0] = -100.
            best_RecoTop_pt_nominal[0] = -100.
            best_RecoTop_eta_nominal[0] = -100.
            best_RecoTop_phi_nominal[0] = -100.
            best_RecoTop_high_truth_nominal[0] = -1


        if ( (len(Zfatjets)>0 or len(Hfatjets)>0) and len(top_recobjet)>0 ):

            if(len(Zfatjets)>0 and len(Hfatjets)==0):
                bestZ_p4 = Zfatjets[0].p4()
            if(len(Zfatjets)==0 and len(Hfatjets)>0):
                bestZ_p4 = Hfatjets[0].p4()
            if(len(Zfatjets)>0 and len(Hfatjets)>0):
                bestZ_p4 = Hfatjets[0].p4()

            bestTprime_p4 = besttop_p4 + bestZ_p4
            best_Tprime_m_nominal[0] = bestTprime_p4.M()
            best_Tprime_mt_nominal[0] = bestTprime_p4.Mt()
            best_Tprime_pt_nominal[0] = bestTprime_p4.Pt()
            best_Tprime_eta_nominal[0] = bestTprime_p4.Eta()
            best_Tprime_phi_nominal[0] = bestTprime_p4.Phi()

            best_RecoZ_m_nominal[0] = bestZ_p4.M()
            best_RecoZ_mt_nominal[0] = bestZ_p4.Mt()
            best_RecoZ_pt_nominal[0] = bestZ_p4.Pt()
            best_RecoZ_eta_nominal[0] = bestZ_p4.Eta()
            best_RecoZ_phi_nominal[0] = bestZ_p4.Phi()
            best_RecoZ_sub_b_nominal[0] = nSub_b
        else:
            best_Tprime_m_nominal[0] = -100.
            best_Tprime_mt_nominal[0] = -100.
            best_Tprime_pt_nominal[0] = -100.
            best_Tprime_eta_nominal[0] = -100.
            best_Tprime_phi_nominal[0] = -100.

            #h_best_topM.Fill(best_RecoTop_m_nominal[0])
            
            best_RecoZ_m_nominal[0] = -100.
            best_RecoZ_mt_nominal[0] = -100.
            best_RecoZ_pt_nominal[0] = -100.
            best_RecoZ_eta_nominal[0] = -100.
            best_RecoZ_phi_nominal[0] = -100.
            best_RecoZ_sub_b_nominal[0] = -1
        
        """
        
        systTree.setWeightName("w_nominal",copy.deepcopy(w_nominal_nominal[0]))
        systTree.fillTreesSysts(trees, scenario)
    if isNominal:
        outTreeFile.cd()
        if(isMC):
            h_cutFL.Write()
            #print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genweight.GetBinContent(1), h_PDFweight.GetNbinsX()))
            #h_genweight.Write()
            #h_PDFweight.Write()
            #h_eff_mu.Write()
            #h_eff_ele.Write()
            h_MC_topM.Write()
            h_best_topM.Write()

    systTree.writeTreesSysts(trees, outTreeFile)
    print("Number of events in output tree nominal " + str(trees[0].GetEntries()))
    if isMC:
        print("Number of events in output tree jesUp " + str(trees[1].GetEntries()))
        print("Number of events in output tree jesDown " + str(trees[2].GetEntries()))
        print("Number of events in output tree jerUp " + str(trees[3].GetEntries()))
        print("Number of events in output tree jerDown " + str(trees[4].GetEntries()))

reco("nominal",isMC,addPDF, MCReco)
#Per ora solo nominal poi dopo metto il loop
#for scenario in scenarios:
#    reco(scenario, isMC, addPDF, MCReco)

#if Debug:
    #print("Event with neutrino failed: ", neutrino_failed, " out of ", str(50000))
#else:
    #print("Event with neutrino failed: ", neutrino_failed, " out of ", tree.GetEntries())

#trees[0].Print()

endTime = datetime.datetime.now()
print("Ending running at " + str(endTime))

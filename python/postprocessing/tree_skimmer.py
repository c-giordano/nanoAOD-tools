#!/bin/env python3
import os
import sys
import ROOT
import math
import datetime
import copy
from array import array
from skimtree_utils import *
from samples.samples import *

Debug = False
sample = sample_dict[sys.argv[1]]
part_idx = sys.argv[2]
file_list = list(map(str, sys.argv[3].strip('[]').split(',')))

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
outTreeFile = ROOT.TFile(sys.argv[4] + '/' + sample.label+"_part"+str(part_idx)+".root", "RECREATE") # output file
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
systTree.setWeightName("trigSF",1.)
systTree.setWeightName("trigUp",1.)
systTree.setWeightName("trigDown",1.)
systTree.setWeightName("PFSF",1.)
systTree.setWeightName("PFUp",1.)
systTree.setWeightName("PFDown",1.)
systTree.setWeightName("btagSF",1.)
systTree.setWeightName("btagUp",1.)
systTree.setWeightName("btagDown",1.)
systTree.setWeightName("mistagUp",1.)
systTree.setWeightName("mistagDown",1.)
systTree.setWeightName("pdf_totalUp", 1.)
systTree.setWeightName("pdf_totalDown", 1.)


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
    #Reconstructed Wprime
    Wprime_pt = array.array('f', [0.])
    Wprime_eta = array.array('f', [0.])
    Wprime_phi = array.array('f', [0.])
    Wprime_m = array.array('f', [0.])

    best_top_pt = array.array('f', [0.])
    best_top_eta = array.array('f', [0.])
    best_top_phi = array.array('f', [0.])
    best_top_m = array.array('f', [0.])
        
    nJet_lowpt = array.array('i', [0])
    nfatJet = array.array('i', [0])
    nJet_pt100 = array.array('i', [0])
    nbJet_lowpt = array.array('i', [0])
    nbJet_pt100 = array.array('i', [0])

    #Muon
    muon_pt = array.array('f', [0.])
    muon_eta = array.array('f', [0.])

    #MET     
    MET_pt = array.array('f', [0.])
    MET_phi = array.array('f', [0.])

    #Number of primary vertexes
    nPV_tot = array.array('f', [0.])
    nPV_good = array.array('f', [0.])
    
    lumi = {'2016': 35.9, "2017": 41.53, "2018": 59.7}
    #++++++++++++++++++++++++++++++++++
    #++   branching the new trees    ++
    #++++++++++++++++++++++++++++++++++
    systTree.branchTreesSysts(trees, scenario, "Wprime_pt", outTreeFile, Wprime_pt_nominal)
    systTree.branchTreesSysts(trees, scenario, "Wprime_eta", outTreeFile, Wprime_eta_nominal)
    systTree.branchTreesSysts(trees, scenario, "Wprime_phi", outTreeFile, Wprime_phi_nominal)
    systTree.branchTreesSysts(trees, scenario, "Wprime_m", outTreeFile, Wprime_m_nominal)
    
    systTree.branchTreesSysts(trees, scenario, "njet_lowpt", outTreeFile, nJet_lowpt_nominal)
    systTree.branchTreesSysts(trees, scenario, "njet_pt100", outTreeFile, nJet_pt100_nominal)
    systTree.branchTreesSysts(trees, scenario, "nfatjet", outTreeFile, nfatJet_nominal)
    systTree.branchTreesSysts(trees, scenario, "nbjet_lowpt", outTreeFile, nbJet_lowpt_nominal)
    systTree.branchTreesSysts(trees, scenario, "nbjet_pt100", outTreeFile, nbJet_pt100_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_pt", outTreeFile, best_RecoTop_pt_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_eta", outTreeFile, best_RecoTop_eta_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_phi", outTreeFile, best_RecoTop_phi_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_m", outTreeFile, best_RecoTop_m_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_costheta", outTreeFile, best_RecoTop_costheta_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_costhetalep", outTreeFile, best_RecoTop_costhetalep_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_mt", outTreeFile, best_RecoTop_mt_nominal)
    systTree.branchTreesSysts(trees, scenario, "best_top_isNeg", outTreeFile, best_RecoTop_isNeg_nominal)

    systTree.branchTreesSysts(trees, scenario, "muon_pt", outTreeFile, muon_pt_nominal)
    systTree.branchTreesSysts(trees, scenario, "muon_eta", outTreeFile, muon_eta_nominal)

    systTree.branchTreesSysts(trees, scenario, "muon_pt_tuneP", outTreeFile, muon_pt_tuneP_nominal)
    systTree.branchTreesSysts(trees, scenario, "muon_pt_tuneP_pull", outTreeFile, muon_pt_tuneP_pull_nominal)
    systTree.branchTreesSysts(trees, scenario, "lepMET_deltaphi", outTreeFile, lepMET_deltaPhi_nominal)
    systTree.branchTreesSysts(trees, scenario, "lepMETpt_HT_nominal", outTreeFile, lepMETpt_HT_nominal)

    systTree.branchTreesSysts(trees, scenario, "passed_mu", outTreeFile, passed_mu_nominal)
    systTree.branchTreesSysts(trees, scenario, "passed_ele", outTreeFile, passed_ele_nominal)
    systTree.branchTreesSysts(trees, scenario, "passed_ht", outTreeFile, passed_ht_nominal)
    systTree.branchTreesSysts(trees, scenario, "nPV_good", outTreeFile, nPV_good_nominal)
    systTree.branchTreesSysts(trees, scenario, "nPV_tot", outTreeFile, nPV_tot_nominal)
    systTree.branchTreesSysts(trees, scenario, "isEle", outTreeFile, isEle_nominal)
    systTree.branchTreesSysts(trees, scenario, "isMu", outTreeFile, isMu_nominal)
    systTree.branchTreesSysts(trees, scenario, "Event_HT", outTreeFile, Event_HT_nominal)
    systTree.branchTreesSysts(trees, scenario, "MET_pt", outTreeFile, MET_pt_nominal)
    systTree.branchTreesSysts(trees, scenario, "MET_phi", outTreeFile, MET_phi_nominal)
    
    #print("Is MC: " + str(isMC) + "      option addPDF: " + str(addPDF))
    if(isMC and addPDF):
        systTree.branchTreesSysts(trees, scenario, "w_PDF", outTreeFile, w_PDF_nominal)
    if('TT_' in sample.label): 
        systTree.branchTreesSysts(trees, scenario, "nlep", outTreeFile, nlep_nominal)
    ################################################################################################################################################################################################################################
    
    #++++++++++++++++++++++++++++++++++
    #++      taking MC weights       ++
    #++++++++++++++++++++++++++++++++++
    # This part of the code takes care of collecting the MC weight for the correct normalization of the MC samples and for the production of the PDF weights variations
    print("isMC: ", isMC)
    pdf_xsweight = 1.
    pdf_weight_sum = 0.
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
                    for i in range(1, h_pdfw_tmp.GetXaxis().GetNbins()+1):
                        pdf_weight_sum += h_pdfw_tmp.GetBinContent(i)
                    pdf_weight_sum /= h_pdfw_tmp.GetXaxis().GetNbins()
                    print(pdf_weight_sum)
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
        pdf_xsweight = pdf_weight_sum/h_genweight.GetBinContent(1)
        #print(pdf_xsweight)

    #++++++++++++++++++++++++++++++++++
    #++   looping over the events    ++
    #++++++++++++++++++++++++++++++++++
    for i in range(tree.GetEntries()):
        w_nominal_nominal[0] = 1.
        if Debug:
            if i > 2000:
                break
        if i%5000 == 1:
            print("Event #", i, " out of ", int(tree.GetEntries()))
        #++++++++++++++++++++++++++++++++++
        #++        taking objects        ++
        #++++++++++++++++++++++++++++++++++
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
        
        chain.GetEntry(i) #this is needed for branches that are not compatible with the NANOAOD convention (e.g. )

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
        recomet_p4t = None
        #++++++++++++++++++++++++++++++++++
        #++    starting the analysis     ++
        #++++++++++++++++++++++++++++++++++
        VetoMu = get_LooseMu(muons)
        goodMu = get_Mu(muons)
        VetoEle = get_LooseEle(electrons)
        goodEle = get_Ele(electrons)
        year = sample.year
        if(isMC):
            runPeriod = None
        else:
            runPeriod = sample.runP
        passMu, passEle, passHT, passPh, noTrigger = trig_map(HLT, year, runPeriod, chain.run)
        passed_mu_nominal[0] = int(passMu)
        passed_ele_nominal[0] = int(passEle)
        passed_ht_nominal[0] = int(passHT)
        isMuon = (len(goodMu) == 1) and (len(goodEle) == 0) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passMu or passHT)
        isElectron = (len(goodMu) == 0) and (len(goodEle) == 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and (passEle or passHT)

        if(isMC):
            doublecounting = False
        else:
            doublecounting = True
        #Double counting removal
        if('DataMu' in sample.label and passMu):
            doublecounting = False
        if year == 2018:
            if('DataEle' in sample.label and (not passMu and (passEle or passPh))):
                doublecounting = False
        else:
            if('DataEle' in sample.label and (not passMu and passEle)):
                doublecounting = False
            if('DataPh' in sample.label and (passPh and not passMu and not passEle)):
                doublecounting = False
        if('DataHT' in sample.label and (passHT and not passMu and not passEle and not passPh)):
            doublecounting = False
            
        if doublecounting:
            continue

        ######################################
        ## Selecting only jets with pt>100  ##
        ######################################
        goodJets = get_Jet(jets, 100)
        bjets, nobjets = bjet_filter(goodJets, 'DeepFlv', 'M')
        if(len(bjets) > 1):
            btagreco = True
        nJet_pt100_nominal[0] = len(goodJets)
        nbJet_pt100_nominal[0] = len(bjets)
        nfatJet_nominal[0] = len(fatjets)
        nJet_lowpt_nominal[0] = len(jets) - len(goodJets)

        # this function filters the jets returning b jets and non b jets according to the tagger and the WP chosen 
        nbJet_lowpt_nominal[0] = len(bjet_filter(jets, 'DeepFlv', 'M')[0]) - len(bjets)
        
        # this part take care of writing the variations of the MC weight relative to the LHE scale and the PDFs variations
        if isMC:
            genpart = Collection(event, "GenPart")
            LHE = Collection(event, "LHEPart")
            LHEScaleWeight = Collection(event, 'LHEScaleWeight')
            lheSF = 1.
            lheUp = 1.
            lheDown = 1.
            pdf_totalUp = 1.
            pdf_totalDown = 1.
            if scenario == 'nominal':
                if len(LHEScaleWeight) > 1:
                    lhemin = min([LHEScaleWeight[g].__getattr__("") for g in range(len(LHEScaleWeight))])
                    lhemax = max([LHEScaleWeight[g].__getattr__("") for g in range(len(LHEScaleWeight))])
                    lheSF = lheweight * LHEScaleWeight[4].__getattr__("")
                    lheUp = lheweight * lhemax
                    lheDown = lheweight * lhemin
                if addPDF:
                    LHEPdfWeight = Collection(event, 'LHEPdfWeight')
                    mean_pdf = 0.
                    rms = 0.
                    for pdfw, i in zip(LHEPdfWeight, range(1, len(LHEPdfWeight)+1)):
                        mean_pdf += pdfw.__getattr__("")
                    mean_pdf /= len(LHEPdfWeight)
                    #print(mean_pdf)
                    for pdfw, i in zip(LHEPdfWeight, range(1, len(LHEPdfWeight)+1)):
                        rms += (pdfw.__getattr__("")-mean_pdf)**2
                    rms = math.sqrt(rms/len(LHEPdfWeight))
                    #print(rms)
                    pdf_totalUp = (1+rms)*pdf_xsweight
                    pdf_totalDown = (1-rms)*pdf_xsweight
                    #print(pdf_totalUp, pdf_totalDown)
                systTree.setWeightName("pdf_totalUp", copy.deepcopy(pdf_totalUp))
                systTree.setWeightName("pdf_totalDown", copy.deepcopy(pdf_totalDown))
                systTree.setWeightName("LHESF", copy.deepcopy(lheSF))
                systTree.setWeightName("LHEUp", copy.deepcopy(lheUp))
                systTree.setWeightName("LHEDown", copy.deepcopy(lheDown))

        if(isMuon):
            tightlep = goodMu[0]
            tightlep_p4 = copy.deepcopy(tightlep.p4())#ROOT.TLorentzVector()

        recotop = TopUtilities()
        #veto on events with "pathological" reco neutrino
        tent_neutrino = recotop.NuMomentum(tightlep.p4().Px(), tightlep.p4().Py(), tightlep.p4().Pz(), tightlep.p4().Pt(), tightlep.p4().E(), MET['metPx'], MET['metPy'])
        if tent_neutrino[0] == None:
            neutrino_failed += 1
            continue
        recomet_p4t = ROOT.TLorentzVector()
        recomet_p4t.SetPtEtaPhiM(met.pt, 0., met.phi, 0)
        
        nPV_good[0] = PV.npvsGood
        nPV_tot[0] = PV.npvs
        
        MET_pt[0] = met.pt
        MET_phi[0] = met.phi

        #DetReco(nstruction)
            
        ## top reconstruction
        recotop_p4, IsNeg_chi, dR_lepjet = recotop.top4Momentum(tightlep.p4(), goodJets[1].p4(), MET['metPx'], MET['metPy'])
        topjet_p4t = copy.deepcopy(chi_jet_p4)
        topjet_p4t.SetPz(0.)
        recotop_p4t = tightlep_p4t + jet_p4t + recomet_p4t
        promptjet_p4t = copy.deepcopy(goodJets[0].p4())
        RecoTop_costheta[0] = recotop.costhetapol(tightlep.p4(), goodJets[1].p4(), recotop_p4) 
        RecoTop_costhetalep[0] = recotop.costhetapollep(tightlep.p4(), recotop_p4) 

        #Wprime reco                                                                        
        if chi_recotop_p4 != None and tightlep != None:
            chi_Wprime_p4 = chi_recotop_p4 + chi_promptjet.p4()
            chi_Wprime_p4t = chi_recotop_p4t + chi_promptjet_p4t
            chi_Wprime_m[0] = chi_Wprime_p4.M()
            chi_Wprime_mt[0] = chi_Wprime_p4t.M()
            chi_Wprime_pt[0] = chi_Wprime_p4.Pt()
            chi_Wprime_eta[0] = chi_Wprime_p4.Eta()
            chi_Wprime_phi[0] = chi_Wprime_p4.Phi()
            chi_RecoTop_m[0] = chi_recotop_p4.M()
            chi_RecoTop_mt[0] = chi_recotop_p4t.M()
            chi_RecoTop_pt[0] = chi_recotop_p4.Pt()
            chi_RecoTop_eta[0] = chi_recotop_p4.Eta()
            chi_RecoTop_phi[0] = chi_recotop_p4.Phi()
            chi_RecoTop_isNeg[0] = int(IsNeg_chi)
            chi_TopJet_m[0] = chi_jet_p4.M()
            chi_TopJet_pt[0] = chi_jet_p4.Pt()
            chi_TopJet_eta[0] = chi_jet_p4.Eta()
            chi_TopJet_phi[0] = chi_jet_p4.Phi()
            chi_TopJet_isBTagged[0] = copy.deepcopy(is_chi_topjet_btag) #int(len(bjet_filter([chi_jet], 'DeepFlv', 'M')[0]))
            ##print("chi_TopJet_isBTagged: ", chi_TopJet_isBTagged[0])
            chi_TopJet_dRLepJet[0] = copy.deepcopy(chi_dR_lepjet)
            chi_WpJet_m[0] = chi_promptjet.p4().M()
            chi_WpJet_pt[0] = chi_promptjet.p4().Pt()
            chi_WpJet_eta[0] = chi_promptjet.p4().Eta()
            chi_WpJet_phi[0] = chi_promptjet.p4().Phi()
            chi_WpJet_isBTagged[0] = copy.deepcopy(is_chi_Wpjet_btag) #int(len(bjet_filter([chi_promptjet], 'DeepFlv', 'M')[0]))
            ##print("chi_WpJet_isBTagged: ", chi_WpJet_isBTagged[0])
            closAK8, dR_bestWAK4AK8 = closest(chi_promptjet, fatjets) 
            ptrel_bestWAK4_closestAK8[0] = chi_promptjet.pt/closAK8.pt
            deltaR_bestWAK4_closestAK8[0] = copy.deepcopy(dR_bestWAK4AK8)
            chi_topW_jets_pt[0] = (chi_jet_p4 + chi_promptjet.p4()).Pt()
            chi_topW_jets_deltaR[0] = deltaR(chi_jet_p4.Eta(), chi_jet_p4.Phi(), chi_promptjet.p4().Eta(), chi_promptjet.p4().Phi())
            chi_topW_jets_deltaphi[0] = deltaPhi(chi_jet_p4.Phi(), chi_promptjet.p4().Phi())
                ##print("chi W' mass: ", chi_Wprime_p4.M())
            if isMC:
                best_TopJet_hadronflv[0] = best_jet.hadronFlavour
                best_TopJet_partonflv[0] = best_jet.partonFlavour
                best_TopJet_hadronflv[0] = best_promptjet.hadronFlavour
                best_TopJet_partonflv[0] = best_promptjet.partonFlavour
            ##print( "best W' mass: ", best_Wprime_p4.M())
        
        systTree.setWeightName("w",copy.deepcopy(w[0]))
        systTree.fillTreesSysts(trees, scenario)
    outTreeFile.cd()
    if scenario == 'nominal':
        trees[0].Write()
        if(isMC):
            #print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genweight.GetBinContent(1), h_PDFweight.GetNbinsX()))
            h_genweight.Write()
            h_PDFweight.Write()
            h_eff_mu.Write()
            h_eff_ele.Write()
    elif scenario == 'jesUp':
        trees[1].Write()
    elif scenario == 'jesDown':
        trees[2].Write()
    elif scenario == 'jerUp':
        trees[3].Write()
    elif scenario == 'jerDown':
        trees[4].Write()

    print("Number of events in output tree nominal " + str(trees[0].GetEntries()))
    if isMC:
        print("Number of events in output tree jesUp " + str(trees[1].GetEntries()))
        print("Number of events in output tree jesDown " + str(trees[2].GetEntries()))
        print("Number of events in output tree jerUp " + str(trees[3].GetEntries()))
        print("Number of events in output tree jerDown " + str(trees[4].GetEntries()))

for scenario in scenarios:
    reco(scenario, isMC, addPDF, MCReco)
#if Debug:
    #print("Event with neutrino failed: ", neutrino_failed, " out of ", str(50000))
#else:
    #print("Event with neutrino failed: ", neutrino_failed, " out of ", tree.GetEntries())

#trees[0].Print()

endTime = datetime.datetime.now()
print("Ending running at " + str(endTime))

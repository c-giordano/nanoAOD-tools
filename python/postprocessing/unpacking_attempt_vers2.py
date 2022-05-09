import ROOT
import copy
import math
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *



class unpacking_vers2(Module):
    def __init__(self,isMC=1):
        self.isMC = isMC
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        """nTop"""
        self.out.branch("nTop", "i")

        """Branch variabili top senza nu"""
        self.out.branch("Top_pt","F", lenVar="nTop")
        self.out.branch("Top_eta","F", lenVar="nTop")
        self.out.branch("Top_phi","F", lenVar="nTop")
        self.out.branch("Top_e","F", lenVar="nTop")
        self.out.branch("Top_mass","F", lenVar="nTop")

        """Branch variabili top con nu"""

        self.out.branch("Top_nu_pt","F", lenVar="nTop")
        self.out.branch("Top_nu_eta","F", lenVar="nTop")
        self.out.branch("Top_nu_phi","F", lenVar="nTop")
        self.out.branch("Top_nu_e","F", lenVar="nTop")
        self.out.branch("Top_nu_mass","F", lenVar="nTop")
        
        """Branch indici goodJet, goodMu e goodEl"""
        self.out.branch("Top_bjet_index","I", lenVar="nTop")
        self.out.branch("Top_mu_index","I", lenVar="nTop")
        self.out.branch("Top_el_index","I", lenVar="nTop")

        """Muon and bjet unboosted (top frame)"""
        
        self.out.branch("Top_Jet_unboosted_pt","F", lenVar="nTop")
        self.out.branch("Top_Jet_unboosted_eta","F", lenVar="nTop")
        self.out.branch("Top_Jet_unboosted_phi","F", lenVar="nTop")
        self.out.branch("Top_Jet_unboosted_e","F", lenVar="nTop")
        self.out.branch("Top_Jet_unboosted_mass","F", lenVar="nTop")
        self.out.branch("Top_Jet_has_promptLep","O", lenVar="nTop")

        self.out.branch("Top_Lep_unboosted_pt","F", lenVar="nTop")
        self.out.branch("Top_Lep_unboosted_eta","F", lenVar="nTop")
        self.out.branch("Top_Lep_unboosted_phi","F", lenVar="nTop")
        self.out.branch("Top_Lep_unboosted_e","F", lenVar="nTop")
        self.out.branch("Top_Lep_unboosted_mass","F", lenVar="nTop")
        
        self.out.branch("Top_pt_rel","F", lenVar="nTop")
        self.out.branch("Top_Is_dR_merg","I", lenVar="nTop")
        self.out.branch("Top_Costheta","F", lenVar="nTop")
        self.out.branch("Top_dR","F",lenVar="nTop")


        """Variabili per la definizione della Truth"""
        
        self.out.branch("Top_LHE_Truth", "i", lenVar="nTop") #It is i, you can put I or F I
        self.out.branch("Lepton_LHE_Flavour", "F", lenVar="nTop")
        
        self.out.branch("Muon_mindR","F", lenVar="nMuon")
        self.out.branch("Muon_mindR_jIndex","I", lenVar="nMuon")
        self.out.branch("Electron_mindR","F", lenVar="nElectron")
        self.out.branch("Electron_mindR_jIndex","I", lenVar="nElectron")
        
               
        """Branch variabili jet standalone (no leptoni)"""
       
        self.out.branch("nGoodJsa", "i")
        self.out.branch("Jsa_pt", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_eta", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_phi", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_e", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_M", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_index", "I", lenVar="allJet")

        self.out.branch("Jsa_Lep_char_pt", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Lep_char_phi", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Lep_char_eta", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Lep_char_M", "F", lenVar="nGoodJsa")

        self.out.branch("Jsa_Lep_mu_pt", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Lep_mu_phi", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Lep_mu_eta", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Lep_mu_M", "F", lenVar="nGoodJsa")
       
        self.out.branch("Jsa_Bjet_char_pt", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Bjet_char_phi", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Bjet_char_eta", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Bjet_char_M", "F", lenVar="nGoodJsa")

        self.out.branch("Jsa_Bjet_mu_pt", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Bjet_mu_phi", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Bjet_mu_eta", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Bjet_mu_M", "F", lenVar="nGoodJsa")

        self.out.branch("Jsa_area", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_bRegCorr", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_bRegRes", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_btagCMVA", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_btagCSVV2", "F", lenVar="nGoodJsa")

        self.out.branch("Jsa_btagDeepB", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_btagDeepC", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_btagDeepFlavB", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_btagDeepFlavC", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_cRegCorr", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_cRegRes", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_chEmEF", "F", lenVar="nGoodJsa")

        self.out.branch("Jsa_muEF", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_muonSubtrFactor", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_partonFlavour", "I", lenVar="nGoodJsa")

        self.out.branch("Jsa_puIdDisc", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_rawFactor", "F", lenVar="nGoodJsa")

       
        self.out.branch("Jsa_index", "F", lenVar="nGoodJsa")
        self.out.branch("Jsa_Truth", "I", lenVar="nGoodJsa")

        self.out.branch("nTopSA", "i")
        self.out.branch("TopSA_nu_pt", "F", lenVar="nTopSA")
        self.out.branch("TopSA_nu_phi", "F", lenVar="nTopSA")
        self.out.branch("TopSA_nu_eta", "F", lenVar="nTopSA")
        self.out.branch("TopSA_nu_M", "F", lenVar="nTopSA")

        self.out.branch("TopSA_Lep_unboosted_pt", "F", lenVar="nTopSA")
        self.out.branch("TopSA_Lep_unboosted_eta", "F", lenVar="nTopSA")
        self.out.branch("TopSA_Lep_unboosted_phi", "F", lenVar="nTopSA")
        self.out.branch("TopSA_Lep_unboosted_e", "F", lenVar="nTopSA")
        self.out.branch("TopSA_Lep_unboosted_M", "F", lenVar="nTopSA")

        self.out.branch("TopSA_Jsa_unboosted_pt", "F", lenVar="nTopSA")
        self.out.branch("TopSA_Jsa_unboosted_eta", "F", lenVar="nTopSA")
        self.out.branch("TopSA_Jsa_unboosted_phi", "F", lenVar="nTopSA")
        self.out.branch("TopSA_Jsa_unboosted_e", "F", lenVar="nTopSA")
        self.out.branch("TopSA_Jsa_unboosted_M", "F", lenVar="nTopSA")
        self.out.branch("TopSA_Truth", "I", lenVar="nTopSA")
        self.out.branch("TopSA_Jsa_index", "F", lenVar="nTopSA")
        self.out.branch("TopSA_Jet_index", "I", lenVar="nTopSA")

        self.out.branch("TopSA_area", "F", lenVar="nTopSA")
        self.out.branch("TopSA_bRegCorr", "F", lenVar="nTopSA")
        self.out.branch("TopSA_bRegRes", "F", lenVar="nTopSA")
        self.out.branch("TopSA_btagCMVA", "F", lenVar="nTopSA")
        self.out.branch("TopSA_btagCSVV2", "F", lenVar="nTopSA")

        self.out.branch("TopSA_btagDeepB", "F", lenVar="nTopSA")
        self.out.branch("TopSA_btagDeepC", "F", lenVar="nTopSA")
        self.out.branch("TopSA_btagDeepFlavB", "F", lenVar="nTopSA")
        self.out.branch("TopSA_btagDeepFlavC", "F", lenVar="nTopSA")
        self.out.branch("TopSA_cRegCorr", "F", lenVar="nTopSA")
        self.out.branch("TopSA_cRegRes", "F", lenVar="nTopSA")
        self.out.branch("TopSA_chEmEF", "F", lenVar="nTopSA")

        self.out.branch("TopSA_muEF", "F", lenVar="nTopSA")
        self.out.branch("TopSA_muonSubtrFactor", "F", lenVar="nTopSA")
        self.out.branch("TopSA_partonFlavour", "I", lenVar="nTopSA")

        self.out.branch("TopSA_puIdDisc", "F", lenVar="nTopSA")
        self.out.branch("TopSA_rawFactor", "F", lenVar="nTopSA")

        self.out.branch("TopSA_mu_index","I", lenVar="nTopSA")#Ok
        self.out.branch("TopSA_el_index","I", lenVar="nTopSA")#Ok

        self.out.branch("TopSA_is_El_there", "I", lenVar="nGoodJsa")
        self.out.branch("TopSA_is_Mu_there", "I", lenVar="nGoodJsa")

        """Branch variabili top 'wrong' (ricostruiti con leptone sbagliato)"""
        self.out.branch("Top_Wrong_pt", "F", lenVar="nGoodJet")
        self.out.branch("Top_Wrong_eta", "F", lenVar="nGoodJet")
        self.out.branch("Top_Wrong_phi", "F", lenVar="nGoodJet")
        self.out.branch("Top_Wrong_e", "F", lenVar="nGoodJet")
        self.out.branch("Top_Wrong_M", "F", lenVar="nGoodJet")

        
        """Variabili per la promptness"""

        self.out.branch("Is_Muon_Prompt", "O", lenVar="nGoodMu")
        self.out.branch("Is_El_Prompt", "O", lenVar="nGoodEl")

        """Variabile discrepancy tra lep LHE e lep reco"""
        self.out.branch("Is_Jet_Standalone", "O", lenVar= "nGoodJet")
        self.out.branch("Is_Top_Wrong", "O", lenVar= "nGoodJsa")

        self.out.branch("Jsa_has_LHElep", "I", lenVar="nGoodJsa")

        """Tallies"""
        self.ninit=0
        self.counttruetops=0
        self.countmatchingmuons=0


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        verbose=False
        self.ninit = self.ninit+1
        if(self.ninit%100==0):print("event n ", self.ninit)
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        electrons = Collection(event, "Electron")
        MET = Object(event, "MET")
        #LHE = Collection(event, "LHEPart")
        if self.isMC==1 :
            genpart = Collection(event, "GenPart")
            LHE = Collection(event, "LHEPart")
    
        
        """Variabili top senza nu"""
        top_momentum=ROOT.TLorentzVector()
        top_pt = []
        top_phi = []
        top_eta = []
        top_e = []
        top_mass = []

        """Variabili top con nu"""
        top_nu_momentum_utils= TopUtilities()
        top_nu_pt = []
        top_nu_phi = []
        top_nu_eta = []
        top_nu_e = []
        top_nu_mass = []
        
        top_nu_momentum = ROOT.TLorentzVector()
        top_nu_momentum_neg = ROOT.TLorentzVector()
        IsmcNeg = False
        IsmcNeg_jsa = False
        mcdR_lepjet = None
        mcdR_jsa = None
        costheta = []

        top_lhe_truth = []
        topsa_truth = []

        """Variabili jet standalone"""
        jsa_momentum = ROOT.TLorentzVector()
        jsa_pt = []
        jsa_phi = []
        jsa_eta = []
        jsa_M = []
        jsa_e = []

        lep_char_momentum = ROOT.TLorentzVector()
        lep_char_pt = []
        lep_char_pt_copy = []
        lep_char_phi = []
        lep_char_eta = []
        lep_char_M = []
        lep_char_phi_copy = []
        lep_char_eta_copy = []
        lep_char_M_copy = []

        lep_mu_momentum = ROOT.TLorentzVector()
        lep_mu_pt = []
        lep_mu_phi = []
        lep_mu_eta = []
        lep_mu_M = []
        lep_mu_pt_copy = []
        lep_mu_phi_copy = []
        lep_mu_eta_copy = []
        lep_mu_M_copy = []

        bjet_char_momentum = ROOT.TLorentzVector()
        bjet_char_pt = []
        bjet_char_phi = []
        bjet_char_eta = []
        bjet_char_M = []
        bjet_char_pt_copy = []
        bjet_char_phi_copy = []
        bjet_char_eta_copy = []
        bjet_char_M_copy = []


        bjet_mu_momentum = ROOT.TLorentzVector()
        bjet_mu_pt = []
        bjet_mu_phi = []
        bjet_mu_eta = []
        bjet_mu_M = []
        bjet_mu_pt_copy = []
        bjet_mu_phi_copy = []
        bjet_mu_eta_copy = []
        bjet_mu_M_copy = []

        jsa_index = []
        jsa_truth = []
        
        topsa_nu_momentum_utils = TopUtilities()
        topsa_nu_momentum = ROOT.TLorentzVector()
        topsa_nu_momentum_neg = ROOT.TLorentzVector()
        topsa_nu_pt = []
        topsa_nu_phi = []
        topsa_nu_eta = []
        topsa_nu_M = []
        topsa_jsa_index = []

        lepsa_unboosted_momentum = ROOT.TLorentzVector()
        lepsa_unboosted_pt =[]
        lepsa_unboosted_phi = []
        lepsa_unboosted_eta = []
        lepsa_unboosted_e = []
        lepsa_unboosted_M = []

        jsa_unboosted_momentum = ROOT.TLorentzVector()
        jsa_unboosted_pt =[]
        jsa_unboosted_phi = []
        jsa_unboosted_eta = []
        jsa_unboosted_e = []
        jsa_unboosted_M = []


        jsa_area = []
        jsa_bRegCorr = []
        jsa_bRegRes = []
        jsa_btagCMVA = []
        jsa_btagCSVV2 = []

        jsa_btagDeepB = []
        jsa_btagDeepC = []
        jsa_btagDeepFlavB = []
        jsa_btagDeepFlavC = []
        jsa_cRegCorr = []
        jsa_cRegRes = []
        jsa_chEmEF = []

        jsa_muEF = []
        jsa_muonSubtrFactor = []
        jsa_partonFlavour = []

        jsa_puIdDisc = []
        jsa_rawFactor = []

        topsa_area = []
        topsa_bRegCorr = []
        topsa_bRegRes = []
        topsa_btagCMVA = []
        topsa_btagCSVV2 = []

        topsa_btagDeepB = []
        topsa_btagDeepC = []
        topsa_btagDeepFlavB = []
        topsa_btagDeepFlavC = []
        topsa_cRegCorr = []
        topsa_cRegRes = []
        topsa_chEmEF = []

        topsa_muEF = []
        topsa_muonSubtrFactor = []
        topsa_partonFlavour = []

        topsa_puIdDisc = []
        topsa_rawFactor = []

        topsa_mu_index = []
        topsa_el_index = []

        """variabili bjet e muon"""
        top_bjet_index = []
        top_mu_index = []
        top_el_index = []

        lep_unboosted_momentum = ROOT.TLorentzVector()
        lep_unboosted_pt =[]
        lep_unboosted_phi = []
        lep_unboosted_eta = []
        lep_unboosted_e = []
        lep_unboosted_mass = []

        jet_unboosted_momentum = ROOT.TLorentzVector()
        jet_unboosted_pt =[]
        jet_unboosted_phi = []
        jet_unboosted_eta = []
        jet_unboosted_e = []
        jet_unboosted_mass = []

        top_pt_rel = []
        is_dR_merg = []
        top_dR = []

        """Top truth = 6"""
        top_wrong_momentum = ROOT.TLorentzVector()
        top_wrong_pt = []
        top_wrong_phi = []
        top_wrong_eta = []
        top_wrong_M = []
        top_wrong_e = []

        #top_high_truth = []
        jet_has_pL = []

        lep_MomId = []
        muon_mindR = []
        muon_mindR_jIndex = []
        electron_mindR = []
        electron_mindR_jIndex = []

        goodmu_mindR = []
        goodel_mindR = []
        
        is_el_there = []
        is_mu_there = []

        #lepton_flavour = []
        lepton_lhe_flavour = []

        is_mu_prompt_index = []
        is_el_prompt_index = []

        is_mu_good_index = []
        is_el_good_index = []
        

        is_jet_standalone_index = []
        jsa_has_LHElep = []
        is_top_wrong_index = []
                
        bjets, nobjets = bjet_filter(jets, 'DeepCSV', 'L')
        
        goodMu = list(filter(lambda x : x.pt>10, muons))
        goodJet = list(filter(lambda x :  x.pt>30, jets)) #noDeePCSV
        goodEl = list(filter(lambda x : x.pt>10, electrons))

        allMu = list(filter(lambda x : x.pt>0, muons))
        allJet = list(filter(lambda x : x.pt>0, jets))
        allEl = list(filter(lambda x : x.pt>0, electrons))

        nGoodMu = len(goodMu)
        nGoodEl = len(goodEl)
        nGoodJet= len(goodJet)

        nGoodJsa = 0 
        nTopSA = 0
        nTop = (nGoodMu + nGoodEl)*nGoodJet
              
        topsa_jsa_index_temp=0
        topsa_jet_index=[]
        if len(goodJet)>0:

            """Creazione di jet standalone e top jsa"""
            #verbose = True
            for j in allJet:


                if j in goodJet:

                    is_jet_standalone_temp = False
                    jsa_truth_temp = 0
                    closemu, dRmin_mu = closest(j, goodMu)
                    closeel, dRmin_el = closest(j, goodEl)

                    if (dRmin_mu>0.4 or dRmin_el>0.4): #continue
                        jsa_index.append(goodJet.index(j))
                        jsa_has_LHElep_temp = 0
                        is_jet_standalone_temp = True
                        jsa_truth_temp = 1
                        nGoodJsa +=1
                        
                        is_el_there_temp=0
                        is_mu_there_temp=0


                        jsa_area.append(copy.deepcopy(j.area))
                        jsa_bRegCorr.append(copy.deepcopy(j.bRegCorr))
                        jsa_bRegRes.append(copy.deepcopy(j.bRegRes))
                        jsa_btagCMVA.append(copy.deepcopy(j.btagCMVA))
                        jsa_btagCSVV2.append(copy.deepcopy(j.btagCSVV2))
                    
                        jsa_btagDeepB.append(copy.deepcopy(j.btagDeepB))
                        jsa_btagDeepC.append(copy.deepcopy(j.btagDeepC))
                        jsa_btagDeepFlavB.append(copy.deepcopy(j.btagDeepFlavB))
                        jsa_btagDeepFlavC.append(copy.deepcopy(j.btagDeepFlavC))
                        jsa_cRegCorr.append(copy.deepcopy(j.cRegCorr))
                        jsa_cRegRes.append(copy.deepcopy(j.cRegRes))
                        jsa_chEmEF.append(copy.deepcopy(j.chEmEF))
                        
                        jsa_muEF.append(copy.deepcopy(j.muEF))
                        jsa_muonSubtrFactor.append(copy.deepcopy(j.muonSubtrFactor))
                        jsa_partonFlavour.append(copy.deepcopy(j.partonFlavour))

                        jsa_puIdDisc.append(copy.deepcopy(j.puIdDisc))
                        jsa_rawFactor.append(copy.deepcopy(j.rawFactor))


                        jsa_momentum = j.p4()
                        jsa_pt.append(jsa_momentum.Pt())
                        jsa_phi.append(jsa_momentum.Phi())
                        jsa_eta.append(jsa_momentum.Eta())
                        jsa_M.append(jsa_momentum.M())

                        lep_char_momentum = j.p4()*j.chEmEF
                        lep_char_pt.append(lep_char_momentum.Pt())
                        lep_char_phi.append(lep_char_momentum.Phi())
                        lep_char_eta.append(lep_char_momentum.Eta())
                        lep_char_M.append(lep_char_momentum.M())
                        lep_char_pt_copy = copy.deepcopy(lep_char_pt)
                        lep_char_phi_copy = copy.deepcopy(lep_char_phi)
                        lep_char_eta_copy = copy.deepcopy(lep_char_eta)
                        lep_char_M_copy = copy.deepcopy(lep_char_M)

                        lep_mu_momentum = j.p4()*j.muEF
                        lep_mu_pt.append(lep_mu_momentum.Pt())
                        lep_mu_phi.append(lep_mu_momentum.Phi())
                        lep_mu_eta.append(lep_mu_momentum.Eta())
                        lep_mu_M.append(lep_mu_momentum.M())
                        lep_mu_pt_copy = copy.deepcopy(lep_mu_pt)
                        lep_mu_phi_copy = copy.deepcopy(lep_mu_phi)
                        lep_mu_eta_copy = copy.deepcopy(lep_mu_eta)
                        lep_mu_M_copy = copy.deepcopy(lep_mu_M)
                        
                        bjet_char_momentum = j.p4()*(1-j.chEmEF)
                        bjet_char_pt.append(bjet_char_momentum.Pt())
                        bjet_char_phi.append(bjet_char_momentum.Phi())
                        bjet_char_eta.append(bjet_char_momentum.Eta())
                        bjet_char_M.append(bjet_char_momentum.M())
                        bjet_char_pt_copy = copy.deepcopy(bjet_char_pt)
                        bjet_char_phi_copy = copy.deepcopy(bjet_char_phi)
                        bjet_char_eta_copy = copy.deepcopy(bjet_char_eta)
                        bjet_char_M_copy = copy.deepcopy(bjet_char_M)
                        
                        bjet_mu_momentum = j.p4()*(1-j.muEF)
                        bjet_mu_pt.append(bjet_mu_momentum.Pt())
                        bjet_mu_phi.append(bjet_mu_momentum.Phi())
                        bjet_mu_eta.append(bjet_mu_momentum.Eta())
                        bjet_mu_M.append(bjet_mu_momentum.M())
                        bjet_mu_pt_copy = copy.deepcopy(bjet_mu_pt)
                        bjet_mu_phi_copy = copy.deepcopy(bjet_mu_phi)
                        bjet_mu_eta_copy = copy.deepcopy(bjet_mu_eta)
                        bjet_mu_M_copy = copy.deepcopy(bjet_mu_M)
                       

                        
                        for l in LHE:
                            if (abs(l.pdgId)==11) and deltaR(j.p4().Eta(),j.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <0.4:
                                jsa_has_LHElep_temp = 11
                                
                            if (abs(l.pdgId)==13) and deltaR(j.p4().Eta(),j.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <0.4:
                                jsa_has_LHElep_temp = 13

                                                                                
                        jsa_has_LHElep.append(jsa_has_LHElep_temp)
                        

                        
                        #print("jet sa # ", topsa_jsa_index_temp)
                        if (j.chEmEF!=0):# and (j.muEF!=0)):
                            
                            topsa_mu_index.append(-1)
                            topsa_el_index.append(allJet.index(j))
                            
                            is_el_there_temp =1
                            nTopSA=nTopSA+1
                            topsa_nu_momentum, IsmcNeg_sa, mcdR_lepjet_sa = topsa_nu_momentum_utils.top4Momentum(lep_char_momentum,bjet_char_momentum,MET.pt*math.cos(MET.phi),MET.pt*math.sin(MET.phi))
                            if topsa_nu_momentum is None:
                                return False
                            topsa_jet_index.append(allJet.index(j))
                            print("Jet index for topsa el", topsa_jet_index)
                            topsa_jsa_index.append(topsa_jsa_index_temp)
                            topsa_nu_pt.append(topsa_nu_momentum.Pt())
                            topsa_nu_phi.append(topsa_nu_momentum.Phi())
                            topsa_nu_eta.append(topsa_nu_momentum.Eta())
                            topsa_nu_M.append(topsa_nu_momentum.M())

                            topsa_area.append(copy.deepcopy(j.area))
                            topsa_bRegCorr.append(copy.deepcopy(j.bRegCorr))
                            topsa_bRegRes.append(copy.deepcopy(j.bRegRes))
                            topsa_btagCMVA.append(copy.deepcopy(j.btagCMVA))
                            topsa_btagCSVV2.append(copy.deepcopy(j.btagCSVV2))
                    
                            topsa_btagDeepB.append(copy.deepcopy(j.btagDeepB))
                            topsa_btagDeepC.append(copy.deepcopy(j.btagDeepC))
                            topsa_btagDeepFlavB.append(copy.deepcopy(j.btagDeepFlavB))
                            topsa_btagDeepFlavC.append(copy.deepcopy(j.btagDeepFlavC))
                            topsa_cRegCorr.append(copy.deepcopy(j.cRegCorr))
                            topsa_cRegRes.append(copy.deepcopy(j.cRegRes))
                            topsa_chEmEF.append(copy.deepcopy(j.chEmEF))
                        
                            topsa_muEF.append(copy.deepcopy(j.muEF))
                            topsa_muonSubtrFactor.append(copy.deepcopy(j.muonSubtrFactor))
                            topsa_partonFlavour.append(copy.deepcopy(j.partonFlavour))

                            topsa_puIdDisc.append(copy.deepcopy(j.puIdDisc))
                            topsa_rawFactor.append(copy.deepcopy(j.rawFactor))

                            

                            topsa_nu_momentum_neg.SetPxPyPzE(-topsa_nu_momentum.Px(),-topsa_nu_momentum.Py(),-topsa_nu_momentum.Pz(),topsa_nu_momentum.E())

                            lepsa_unboosted_momentum = j.p4()*j.chEmEF
                            lepsa_unboosted_momentum.Boost(topsa_nu_momentum_neg.BoostVector())
                            lepsa_unboosted_pt.append(lepsa_unboosted_momentum.Pt())
                            lepsa_unboosted_phi.append(lepsa_unboosted_momentum.Phi())
                            lepsa_unboosted_eta.append(lepsa_unboosted_momentum.Eta())
                            lepsa_unboosted_e.append(lepsa_unboosted_momentum.E())
                            lepsa_unboosted_M.append(lepsa_unboosted_momentum.M())

                            jsa_unboosted_momentum = j.p4()*(1-j.chEmEF)
                            jsa_unboosted_momentum.Boost(topsa_nu_momentum_neg.BoostVector())

                            jsa_unboosted_pt.append(jsa_unboosted_momentum.Pt())
                            jsa_unboosted_phi.append(jsa_unboosted_momentum.Phi())
                            jsa_unboosted_eta.append(jsa_unboosted_momentum.Eta())
                            jsa_unboosted_e.append(jsa_unboosted_momentum.E())
                            jsa_unboosted_M.append(jsa_unboosted_momentum.M())

                            """Truth definition for chEmEF"""
                            if (is_jet_standalone_temp==True) and (is_el_there_temp==True) and (jsa_has_LHElep_temp==11):
                                topsa_truth_char_val = 0
                            if(is_jet_standalone_temp==True) and (is_el_there_temp==True) and (jsa_has_LHElep_temp!=11):
                                topsa_truth_char_val = 1                            
                            topsa_truth.append(topsa_truth_char_val)

                        if (j.muEF!=0):

                            topsa_mu_index.append(allJet.index(j))
                            topsa_el_index.append(-1)

                            is_mu_there_temp=1
                            
                            nTopSA=nTopSA+1
                            topsa_nu_momentum, IsmcNeg_sa, mcdR_lepjet_sa = topsa_nu_momentum_utils.top4Momentum(lep_mu_momentum,bjet_mu_momentum,MET.pt*math.cos(MET.phi),MET.pt*math.sin(MET.phi))
                            if topsa_nu_momentum is None:
                                return False
                        
                            topsa_jet_index.append(allJet.index(j))
                            print("Jet index for topsa mu", topsa_jet_index)
                            topsa_jsa_index.append(topsa_jsa_index_temp)
                            topsa_nu_pt.append(topsa_nu_momentum.Pt())
                            topsa_nu_phi.append(topsa_nu_momentum.Phi())
                            topsa_nu_eta.append(topsa_nu_momentum.Eta())
                            topsa_nu_M.append(topsa_nu_momentum.M())

                            topsa_nu_momentum_neg.SetPxPyPzE(-topsa_nu_momentum.Px(),-topsa_nu_momentum.Py(),-topsa_nu_momentum.Pz(),topsa_nu_momentum.E())

                            lepsa_unboosted_momentum = j.p4()*j.muEF
                            lepsa_unboosted_momentum.Boost(topsa_nu_momentum_neg.BoostVector())
                            lepsa_unboosted_pt.append(lepsa_unboosted_momentum.Pt())
                            lepsa_unboosted_phi.append(lepsa_unboosted_momentum.Phi())
                            lepsa_unboosted_eta.append(lepsa_unboosted_momentum.Eta())
                            lepsa_unboosted_e.append(lepsa_unboosted_momentum.E())
                            lepsa_unboosted_M.append(lepsa_unboosted_momentum.M())

                            jsa_unboosted_momentum = j.p4()*(1-j.muEF)
                            jsa_unboosted_momentum.Boost(topsa_nu_momentum_neg.BoostVector())

                            jsa_unboosted_pt.append(jsa_unboosted_momentum.Pt())
                            jsa_unboosted_phi.append(jsa_unboosted_momentum.Phi())
                            jsa_unboosted_eta.append(jsa_unboosted_momentum.Eta())
                            jsa_unboosted_e.append(jsa_unboosted_momentum.E())
                            jsa_unboosted_M.append(jsa_unboosted_momentum.M())
                            
                            """Truth definition for muEF"""
                            if (is_jet_standalone_temp==True) and (is_mu_there_temp==True) and (jsa_has_LHElep_temp==13):
                                topsa_truth_mu_val = 0
                            if(is_jet_standalone_temp==True) and (is_mu_there_temp==True) and (jsa_has_LHElep_temp!=13):
                                topsa_truth_mu_val = 1                            
                            topsa_truth.append(topsa_truth_mu_val)
                        
                        is_el_there.append(is_el_there_temp)
                        is_mu_there.append(is_mu_there_temp)
                        
                        #topsa_mu_index.append(topsa_mu_index_temp)
                        #topsa_el_index.append(topsa_el_index_temp)
                        
                        topsa_jsa_index_temp=topsa_jsa_index_temp+1
                    
                    
                    is_jet_standalone_index.append(is_jet_standalone_temp)
                    #jsa_truth.append(jsa_truth_temp)


                                
                    
        if ((len(goodMu)>0 or len(goodEl)>0) and len(goodJet)>0 ):
            
            """Creazione Min_dr per leptoni"""
            
            for m in allMu:
                minDr_temp =999
                minDr_indx_temp= -1
                for j in allJet:
                    if j in goodJet:
                        if (deltaR(j.p4().Eta(),j.p4().Phi(),m.p4().Eta(),m.p4().Phi())< minDr_temp):
                            minDr_temp = deltaR(j.p4().Eta(),j.p4().Phi(),m.p4().Eta(),m.p4().Phi())
                            minDr_indx_temp = allJet.index(j)
                muon_mindR.append(minDr_temp)
                muon_mindR_jIndex.append(minDr_indx_temp)

                
            
            for e in allEl:
                minDr_temp =999
                minDr_indx_temp= -1
                for j in allJet:
                    if j in goodJet:
                        if (deltaR(j.p4().Eta(),j.p4().Phi(),e.p4().Eta(),e.p4().Phi())< minDr_temp):
                            minDr_temp = deltaR(j.p4().Eta(),j.p4().Phi(),e.p4().Eta(),e.p4().Phi())
                            minDr_indx_temp = allJet.index(j)
                electron_mindR.append(minDr_temp)
                electron_mindR_jIndex.append(minDr_indx_temp)
            
            

            """Creazione variabili LHE e promptness definition per i muoni"""
            for m in allMu:
                
                if m in goodMu:
                    
                    is_muon_prompt = False
                    muon_LHE_match = False #If there is no match at LHE level
                    muon_from_tau = 0
                    if(verbose):print ("in goodmu with pt ", m.p4().Pt())
                    for l in LHE:
                        if((abs(l.pdgId) == 13)):
                            if(verbose):print("goodMu in LHE- Eta:", l.p4().Eta(), "   Phi:", l.p4().Phi())
                            if(verbose):print("goodMu - Eta:", m.p4().Eta(), "   Phi:", m.p4().Phi())
                            
                            if (deltaR(m.p4().Eta(),m.p4().Phi(),l.p4().Eta(),l.p4().Phi()) > 0.1): continue
                            
                            self.countmatchingmuons=self.countmatchingmuons+1
                            if(verbose):print("n matching muons ",self.countmatchingmuons)
                            muon_LHE_match = True
                            
                            is_muon_prompt=True
                    
                    is_mu_prompt_index.append(is_muon_prompt)
                    if (verbose):print("goodMu index append:", is_muon_prompt, "good mu index m:", is_mu_prompt_index)
                    if (verbose):print("goodMu index m",goodMu.index(m)," goodMu pt ", m.p4().Pt())
                     

            """Creazione variabili LHE e promptness definition per gli elettroni"""

            for e in allEl:
                
                if e in goodEl:
                    is_el_from_tau = 0
                    is_el_prompt = False
                    electron_LHE_match = False
                    for l in LHE:
                        if((abs(l.pdgId) == 11) and  (deltaR(e.p4().Eta(),e.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <=0.3)):#check value for dR!!! I have seen also 0.1 for electrons??
                            electron_LHE_match = True
                            
                            is_el_prompt=True
                                                
                    is_el_prompt_index.append(is_el_prompt)
                                            
            """Creazione top cands"""

            for j in allJet:  
                
                
                if j in goodJet:

                    is_jet_true = False
                    jet_LHE_match = False
                    #lepton_flavour_temp = 0
                    jet_has_promptLep = False 
                    is_top_wrong = False
                    lepton_lhe_flavour_temp=0
                    goodmu_mindR_temp = 0
                    goodel_mindR_temp = 0
                    goodmu_mindR_Index_temp = -1
                    goodel_mindR_Index_temp = -1
                    
                    if abs(j.partonFlavour)==5:

                        is_jet_true = True

                    for l in LHE:
    
                        if((abs(l.pdgId) == 5)) and (deltaR(j.p4().Eta(),j.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <0.4) :
                            jet_LHE_match = True
                                

                        if((abs(l.pdgId) == 13)) and deltaR(j.p4().Eta(),j.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <0.4:
                            jet_has_promptLep=True
                            lepton_lhe_flavour_temp=l.pdgId
 
                            closemu,goodmu_mindR_temp = closest(l, goodMu)
            
                            if goodmu_mindR_temp>0.1:
                                
                                is_top_wrong = True
                                
                                
                        if((abs(l.pdgId) == 11)) and deltaR(j.p4().Eta(),j.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <0.4:
                            jet_has_promptLep=True
                            lepton_lhe_flavour_temp=l.pdgId

                            closeel,goodel_mindR_temp = closest(l, goodEl)
                            
                            if goodel_mindR_temp>0.3:
                                
                                is_top_wrong = True
                                                    
                    goodmu_mindR.append(goodmu_mindR_temp)
                    goodel_mindR.append(goodel_mindR_temp)
                    
                                        
                    jet_has_pL.append(jet_has_promptLep)
                    is_top_wrong_index.append(is_top_wrong)
                    
                    

                    if (is_top_wrong == True):
                        #top_wrong_momemtum.SetPtEtaPhiM(j.pt, j.eta, j.phi, j.mass)
                        top_wrong_pt.append(j.pt)
                        top_wrong_phi.append(j.phi)
                        top_wrong_eta.append(j.eta)
                        #top_wrong_e.append(j.)
                        top_wrong_M.append(j.mass)

                    else:
                        top_wrong_pt.append(-999.0)
                        top_wrong_phi.append(-999.0)
                        top_wrong_eta.append(-999.0)
                        top_wrong_e.append(-999.0)
                        top_wrong_M.append(-999.0)
                    
                    
                    
                    for m in allMu:
                        
                        if m in goodMu:
                            
                            is_muon_prompt = is_mu_prompt_index[goodMu.index(m)]
                            #jet_has_pL.append(jet_has_promptLep)

                            #lepton_flavour_temp = (-13)*(m.charge)
                            top_bjet_index.append(allJet.index(j))
                            top_mu_index.append(allMu.index(m))
                            top_el_index.append(-1)
                            
                            
                            if deltaR(j.p4().Eta(),j.p4().Phi(),m.p4().Eta(),m.p4().Phi()) <=0.4 :
                                is_dR_merg.append(1)
                            elif( deltaR(j.p4().Eta(),j.p4().Phi(),m.p4().Eta(),m.p4().Phi()) <=2 and deltaR(j.p4().Eta(),j.p4().Phi(),m.p4().Eta(),m.p4().Phi()) >0.4):
                                is_dR_merg.append(0)
                            else: 
                                is_dR_merg.append(-1)
                                


                            if deltaR(j.p4().Eta(),j.p4().Phi(),m.p4().Eta(),m.p4().Phi()) <=0.4 :
                                top_momentum = j.p4() 
                                top_nu_momentum, IsmcNeg, mcdR_lepjet = top_nu_momentum_utils.top4Momentum(m.p4(),j.p4()-m.p4(),MET.pt*math.cos(MET.phi),MET.pt*math.sin(MET.phi))
                            else:
                                top_momentum = (j.p4() + m.p4())
                                top_nu_momentum, IsmcNeg, mcdR_lepjet = top_nu_momentum_utils.top4Momentum(m.p4(),j.p4(),MET.pt*math.cos(MET.phi),MET.pt*math.sin(MET.phi))
                            top_pt.append(top_momentum.Pt())
                            top_phi.append(top_momentum.Phi())
                            top_eta.append(top_momentum.Eta())
                            top_e.append(top_momentum.E())
                            top_mass.append(top_momentum.M())

         
                            if top_nu_momentum is None:
                               return False

                            top_nu_pt.append(top_nu_momentum.Pt())
                            top_nu_phi.append(top_nu_momentum.Phi())
                            top_nu_eta.append(top_nu_momentum.Eta())
                            top_nu_e.append(top_nu_momentum.E())
                            top_nu_mass.append(top_nu_momentum.M())  


                            top_pt_rel.append(((m.p4().Vect()).Cross(j.p4().Vect())).Mag()/((j.p4().Vect()).Mag())) 

                            """unboosting"""
                            top_nu_momentum_neg.SetPxPyPzE(-top_nu_momentum.Px(),-top_nu_momentum.Py(),-top_nu_momentum.Pz(),top_nu_momentum.E())

                            lep_unboosted_momentum = m.p4()
                            lep_unboosted_momentum.Boost(top_nu_momentum_neg.BoostVector())
                            lep_unboosted_pt.append(lep_unboosted_momentum.Pt())
                            lep_unboosted_phi.append(lep_unboosted_momentum.Phi())
                            lep_unboosted_eta.append(lep_unboosted_momentum.Eta())
                            lep_unboosted_e.append(lep_unboosted_momentum.E())
                            lep_unboosted_mass.append(lep_unboosted_momentum.M())

                            jet_unboosted_momentum = j.p4()
                            jet_unboosted_momentum.Boost(top_nu_momentum_neg.BoostVector())

                            jet_unboosted_pt.append(jet_unboosted_momentum.Pt())
                            jet_unboosted_phi.append(jet_unboosted_momentum.Phi())
                            jet_unboosted_eta.append(jet_unboosted_momentum.Eta())
                            jet_unboosted_e.append(jet_unboosted_momentum.E())
                            jet_unboosted_mass.append(jet_unboosted_momentum.M())

                            if deltaR(j.p4().Eta(),j.p4().Phi(),m.p4().Eta(),m.p4().Phi()) <=0.4:
                                top_dR.append(deltaR((j.p4()-m.p4()).Eta(),(j.p4()-m.p4()).Phi(),m.p4().Eta(),m.p4().Phi()))
                            else:
                                top_dR.append(deltaR(j.p4().Eta(),j.p4().Phi(),m.p4().Eta(),m.p4().Phi()))                                

                            costheta.append(top_nu_momentum_utils.costhetapol(m.p4(),j.p4(),top_nu_momentum))

                        
    

                            if(verbose):print('--- Muon ---')
                            
                            top_lhe_truth_val_mu =11

                            if(verbose):print("is truth 0?", (is_jet_true == True and is_muon_prompt== True and (j.partonFlavour*m.charge)>0))
                            if(verbose):print("is jet true",is_jet_true, " muon promppt ", is_muon_prompt, " partonFlavour ",j.partonFlavour, " muonvcharge ", m.charge )

                            if((is_jet_true == True and is_muon_prompt== True and (j.partonFlavour*m.charge)>0)):
                                top_lhe_truth_val_mu=0
                                self.counttruetops=self.counttruetops+1
                                if(verbose):print(" partial count true tops ", self.counttruetops)
                                


                            if (is_jet_true == True and is_muon_prompt== True):
                                if (j.partonFlavour*m.charge)>0:
                                    top_lhe_truth_val_mu = (0)
                                    if(verbose):print('is truth 0')
                                else: 
                                    top_lhe_truth_val_mu = (1)
                                    if(verbose):print('is truth 1')
                                        
                            if (is_jet_true == True  and is_muon_prompt== False and jet_has_promptLep == True):
                                top_lhe_truth_val_mu = (2)
                                if(verbose):print('is truth 2')

                            if (is_jet_true == True  and is_muon_prompt== False and jet_has_promptLep == False):
                                top_lhe_truth_val_mu = (3)
                                if(verbose):print('is truth 3')

                            if (is_jet_true == False and is_muon_prompt== True):
                                top_lhe_truth_val_mu = (4)
                                if(verbose):print('is truth 4')

                            if (is_jet_true == False and is_muon_prompt== False):
                                top_lhe_truth_val_mu = (5)
                                if(verbose):print('is truth 5')
                                
                            if (is_jet_true == True and jet_has_promptLep == True and is_top_wrong == True):
                                top_lhe_truth_val_mu = (6)

                            if(verbose):print('Size Top_LHE_Truth: ',len(top_lhe_truth), " ntop ",nTop)

                            
                            top_lhe_truth.append(top_lhe_truth_val_mu)
                            lepton_lhe_flavour.append(lepton_lhe_flavour_temp)
                            
                    for e in allEl:
                        
                        if e in goodEl:
                            is_el_prompt = is_el_prompt_index[goodEl.index(e)]    
                            #lepton_flavour_temp = (-11)*(e.charge)
                            top_bjet_index.append(allJet.index(j))
                            top_mu_index.append(-1)
                            top_el_index.append(allEl.index(e))
                            #jet_has_pL.append(jet_has_promptLep)

                            if deltaR(j.p4().Eta(),j.p4().Phi(),e.p4().Eta(),e.p4().Phi()) <=0.4 :
                                is_dR_merg.append(1)
                            elif( deltaR(j.p4().Eta(),j.p4().Phi(),e.p4().Eta(),e.p4().Phi()) <=2 and deltaR(j.p4().Eta(),j.p4().Phi(),e.p4().Eta(),e.p4().Phi()) >0.4):
                                is_dR_merg.append(0)
                            else: 
                                is_dR_merg.append(-1)
                                
          
                            if deltaR(j.p4().Eta(),j.p4().Phi(),e.p4().Eta(),e.p4().Phi()) <=0.4 :
                                top_momentum = j.p4() 
                                top_nu_momentum, IsmcNeg, mcdR_lepjet = top_nu_momentum_utils.top4Momentum(e.p4(),j.p4()-e.p4(),MET.pt*math.cos(MET.phi),MET.pt*math.sin(MET.phi))
                            else:
                                top_momentum = (j.p4() + e.p4())
                                top_nu_momentum, IsmcNeg, mcdR_lepjet = top_nu_momentum_utils.top4Momentum(e.p4(),j.p4(),MET.pt*math.cos(MET.phi),MET.pt*math.sin(MET.phi))
                            top_pt.append(top_momentum.Pt())
                            top_phi.append(top_momentum.Phi())
                            top_eta.append(top_momentum.Eta())
                            top_e.append(top_momentum.E())
                            top_mass.append(top_momentum.M())


                            if top_nu_momentum is None:
                               return False
         
                            top_nu_pt.append(top_nu_momentum.Pt())
                            top_nu_phi.append(top_nu_momentum.Phi())
                            top_nu_eta.append(top_nu_momentum.Eta())
                            top_nu_e.append(top_nu_momentum.E())
                            top_nu_mass.append(top_nu_momentum.M())  

          
                            top_pt_rel.append(((e.p4().Vect()).Cross(j.p4().Vect())).Mag()/((j.p4().Vect()).Mag())) 

                            
                            """unboosting"""
                            top_nu_momentum_neg.SetPxPyPzE(-top_nu_momentum.Px(),-top_nu_momentum.Py(),-top_nu_momentum.Pz(),top_nu_momentum.E())

                            lep_unboosted_momentum = e.p4()
                            lep_unboosted_momentum.Boost(top_nu_momentum_neg.BoostVector())
                            lep_unboosted_pt.append(lep_unboosted_momentum.Pt())
                            lep_unboosted_phi.append(lep_unboosted_momentum.Phi())
                            lep_unboosted_eta.append(lep_unboosted_momentum.Eta())
                            lep_unboosted_e.append(lep_unboosted_momentum.E())
                            lep_unboosted_mass.append(lep_unboosted_momentum.M())

                            jet_unboosted_momentum = j.p4()
                            jet_unboosted_momentum.Boost(top_nu_momentum_neg.BoostVector())

                            jet_unboosted_pt.append(jet_unboosted_momentum.Pt())
                            jet_unboosted_phi.append(jet_unboosted_momentum.Phi())
                            jet_unboosted_eta.append(jet_unboosted_momentum.Eta())
                            jet_unboosted_e.append(jet_unboosted_momentum.E())
                            jet_unboosted_mass.append(jet_unboosted_momentum.M())


                            if deltaR(j.p4().Eta(),j.p4().Phi(),e.p4().Eta(),e.p4().Phi()) <=0.1:
                                top_dR.append(deltaR((j.p4()-e.p4()).Eta(),(j.p4()-e.p4()).Phi(),e.p4().Eta(),e.p4().Phi()))
                            else:
                                top_dR.append(deltaR(j.p4().Eta(),j.p4().Phi(),e.p4().Eta(),e.p4().Phi())) 

                            costheta.append(top_nu_momentum_utils.costhetapol(e.p4(),j.p4(),top_nu_momentum))
                            
                            if(verbose):print('--- Electron ---')

                            top_lhe_truth_val_el=11

                            if (is_jet_true == True and is_el_prompt== True) and (j.partonFlavour*e.charge)>0:
                                top_lhe_truth_val_el=0
                                self.counttruetops=self.counttruetops+1
                                if(verbose):print(" partial count true tops ", self.counttruetops)
 
                            if(is_jet_true == True and is_el_prompt== True):
                                if (j.partonFlavour*e.charge)>0:
                                    top_lhe_truth_val_el = (0)
                                    if(verbose):print('is truth 0')
                                else:
                                    top_lhe_truth_val_el = (1)
                                    if(verbose):print('is truth 1')

                            if (is_jet_true == True and is_el_prompt== False and jet_has_promptLep == True):
                                top_lhe_truth_val_el = (2)
                                if(verbose):print('is truth 2')

                            if (is_jet_true == True and is_el_prompt== False and jet_has_promptLep == False):
                                top_lhe_truth_val_el = (3)
                                if(verbose):print('is truth 3')
                            if (is_jet_true == False  and is_el_prompt== True):
                                top_lhe_truth_val_el = (4)
                                if(verbose):print('is truth 4')

                            if (is_jet_true == False and is_el_prompt== False):
                                top_lhe_truth_val_el = (5)
                                if(verbose):print('is truth 5')

                            if (is_jet_true == True and jet_has_promptLep == True and is_top_wrong == True):
                               top_lhe_truth_val_el = (6)

                            top_lhe_truth.append(top_lhe_truth_val_el)
                            lepton_lhe_flavour.append(lepton_lhe_flavour_temp)

                            if(verbose):print('Size Top_LHE_Truth: ',len(top_lhe_truth), " ntop ",nTop)
                        

                    #lepton_flavour.append(lepton_flavour_temp)
        #IMPORTANT: Here it should be better to reject the events with ONLY tops with DeltaR>2                        

        """Tops"""

        self.out.fillBranch("nTop", nTop)

        self.out.fillBranch("Top_pt", top_pt)
        self.out.fillBranch("Top_phi", top_phi)
        self.out.fillBranch("Top_eta", top_eta)
        self.out.fillBranch("Top_e", top_e)
        self.out.fillBranch("Top_mass", top_mass)
        
        self.out.fillBranch("Top_nu_pt", top_nu_pt)
        self.out.fillBranch("Top_nu_phi", top_nu_phi)
        self.out.fillBranch("Top_nu_eta", top_nu_eta)
        self.out.fillBranch("Top_nu_e", top_nu_e)
        self.out.fillBranch("Top_nu_mass", top_nu_mass)
        
        self.out.fillBranch("Top_bjet_index", top_bjet_index)
        self.out.fillBranch("Top_mu_index", top_mu_index)
        self.out.fillBranch("Top_el_index", top_el_index)
        
        self.out.fillBranch("Top_Jet_unboosted_pt",jet_unboosted_pt) 
        self.out.fillBranch("Top_Jet_unboosted_eta",jet_unboosted_eta)
        self.out.fillBranch("Top_Jet_unboosted_phi",jet_unboosted_phi)
        self.out.fillBranch("Top_Jet_unboosted_e",jet_unboosted_e)
        self.out.fillBranch("Top_Jet_unboosted_mass",jet_unboosted_mass)

        self.out.fillBranch("Top_Jet_has_promptLep",jet_has_pL)
                
        self.out.fillBranch("Top_Lep_unboosted_pt",lep_unboosted_pt) 
        self.out.fillBranch("Top_Lep_unboosted_eta",lep_unboosted_eta)
        self.out.fillBranch("Top_Lep_unboosted_phi",lep_unboosted_phi)
        self.out.fillBranch("Top_Lep_unboosted_e",lep_unboosted_e)
        self.out.fillBranch("Top_Lep_unboosted_mass",lep_unboosted_mass)
        self.out.fillBranch("Top_pt_rel", top_pt_rel)
        self.out.fillBranch("Top_Is_dR_merg",is_dR_merg)
        self.out.fillBranch("Top_Costheta", costheta)
        self.out.fillBranch("Top_dR", top_dR)
        
        self.out.fillBranch("Muon_mindR", muon_mindR)
        self.out.fillBranch("Muon_mindR_jIndex", muon_mindR_jIndex)
        self.out.fillBranch("Electron_mindR", electron_mindR)
        self.out.fillBranch("Electron_mindR_jIndex", electron_mindR_jIndex)

        #self.out.fillBranch("Lepton_Flavour", lepton_flavour)
        self.out.fillBranch("Lepton_LHE_Flavour", lepton_lhe_flavour)
        if(verbose):print(" final count true tops ", self.counttruetops)

        self.out.fillBranch("Top_LHE_Truth", top_lhe_truth)


        """Good muons, electrons e jets"""

        self.out.fillBranch("nGoodJsa", nGoodJsa)

        self.out.fillBranch("Jsa_pt", jsa_pt)
        self.out.fillBranch("Jsa_eta", jsa_eta)
        self.out.fillBranch("Jsa_phi", jsa_phi)
        self.out.fillBranch("Jsa_e", jsa_e)
        self.out.fillBranch("Jsa_M", jsa_M)
        
        self.out.fillBranch("Jsa_Lep_char_pt", lep_char_pt_copy)
        self.out.fillBranch("Jsa_Lep_char_phi", lep_char_phi_copy)
        self.out.fillBranch("Jsa_Lep_char_eta", lep_char_eta_copy)
        self.out.fillBranch("Jsa_Lep_char_M", lep_char_M_copy)

        self.out.fillBranch("Jsa_Lep_mu_pt", lep_mu_pt_copy)
        self.out.fillBranch("Jsa_Lep_mu_phi", lep_mu_phi_copy)
        self.out.fillBranch("Jsa_Lep_mu_eta", lep_mu_eta_copy)
        self.out.fillBranch("Jsa_Lep_mu_M", lep_mu_M_copy)

        self.out.fillBranch("Jsa_Bjet_mu_pt", bjet_mu_pt_copy)
        self.out.fillBranch("Jsa_Bjet_mu_phi", bjet_mu_phi_copy)
        self.out.fillBranch("Jsa_Bjet_mu_eta", bjet_mu_eta_copy)
        self.out.fillBranch("Jsa_Bjet_mu_M", bjet_mu_M_copy)

        self.out.fillBranch("Jsa_area", jsa_area)
        self.out.fillBranch("Jsa_bRegCorr", jsa_bRegCorr)
        self.out.fillBranch("Jsa_bRegRes", jsa_bRegRes)
        self.out.fillBranch("Jsa_btagCMVA", jsa_btagCMVA)
        self.out.fillBranch("Jsa_btagCSVV2", jsa_btagCSVV2)
        self.out.fillBranch("Jsa_btagDeepB", jsa_btagDeepB)
        self.out.fillBranch("Jsa_btagDeepC", jsa_btagDeepC)
        self.out.fillBranch("Jsa_btagDeepFlavB", jsa_btagDeepFlavB)
        self.out.fillBranch("Jsa_btagDeepFlavC", jsa_btagDeepFlavC)
        self.out.fillBranch("Jsa_cRegCorr", jsa_cRegCorr)
        self.out.fillBranch("Jsa_cRegRes", jsa_cRegRes)
        self.out.fillBranch("Jsa_chEmEF", jsa_chEmEF)
        self.out.fillBranch("Jsa_muEF", jsa_muEF)
        self.out.fillBranch("Jsa_muonSubtrFactor", jsa_muonSubtrFactor)
        

        self.out.fillBranch("Jsa_puIdDisc", jsa_puIdDisc)
        self.out.fillBranch("Jsa_rawFactor", jsa_rawFactor)

        self.out.fillBranch("Jsa_index", jsa_index)

        self.out.fillBranch("nTopSA", nTopSA)
        self.out.fillBranch("TopSA_nu_pt", topsa_nu_pt)
        self.out.fillBranch("TopSA_nu_phi", topsa_nu_phi)
        self.out.fillBranch("TopSA_nu_eta", topsa_nu_eta)
        self.out.fillBranch("TopSA_nu_M", topsa_nu_M)

        self.out.fillBranch("TopSA_Lep_unboosted_pt",lepsa_unboosted_pt) 
        self.out.fillBranch("TopSA_Lep_unboosted_eta",lepsa_unboosted_eta)
        self.out.fillBranch("TopSA_Lep_unboosted_phi",lepsa_unboosted_phi)
        self.out.fillBranch("TopSA_Lep_unboosted_e",lepsa_unboosted_e)
        self.out.fillBranch("TopSA_Lep_unboosted_M",lepsa_unboosted_M)

        self.out.fillBranch("TopSA_Jsa_unboosted_pt",jsa_unboosted_pt) 
        self.out.fillBranch("TopSA_Jsa_unboosted_eta",jsa_unboosted_eta)
        self.out.fillBranch("TopSA_Jsa_unboosted_phi",jsa_unboosted_phi)
        self.out.fillBranch("TopSA_Jsa_unboosted_e",jsa_unboosted_e)
        self.out.fillBranch("TopSA_Jsa_unboosted_M",jsa_unboosted_M)        
        self.out.fillBranch("TopSA_Truth", topsa_truth)
        self.out.fillBranch("TopSA_Jsa_index",topsa_jsa_index)
        self.out.fillBranch("TopSA_Jet_index",topsa_jet_index)


        self.out.fillBranch("TopSA_area", topsa_area)
        self.out.fillBranch("TopSA_bRegCorr", topsa_bRegCorr)
        self.out.fillBranch("TopSA_bRegRes", topsa_bRegRes)
        self.out.fillBranch("TopSA_btagCMVA", topsa_btagCMVA)
        self.out.fillBranch("TopSA_btagCSVV2", topsa_btagCSVV2)

        self.out.fillBranch("TopSA_btagDeepB", topsa_btagDeepB)
        self.out.fillBranch("TopSA_btagDeepC", topsa_btagDeepC)
        self.out.fillBranch("TopSA_btagDeepFlavB", topsa_btagDeepFlavB)
        self.out.fillBranch("TopSA_btagDeepFlavC", topsa_btagDeepFlavC)
        self.out.fillBranch("TopSA_cRegCorr", topsa_cRegCorr)
        self.out.fillBranch("TopSA_cRegRes", topsa_cRegRes)
        self.out.fillBranch("TopSA_chEmEF", topsa_chEmEF)

        self.out.fillBranch("TopSA_muEF", topsa_muEF)
        self.out.fillBranch("TopSA_muonSubtrFactor", topsa_muonSubtrFactor)
        self.out.fillBranch("TopSA_partonFlavour", topsa_partonFlavour)

        self.out.fillBranch("TopSA_puIdDisc", topsa_puIdDisc)
        self.out.fillBranch("TopSA_rawFactor", topsa_rawFactor)
        
        self.out.fillBranch("Jsa_Truth", jsa_truth)
        self.out.fillBranch("Jsa_has_LHElep", jsa_has_LHElep)

        self.out.fillBranch("TopSA_mu_index", topsa_mu_index)#Ok
        self.out.fillBranch("TopSA_el_index", topsa_el_index)#Ok


        self.out.fillBranch("TopSA_is_El_there", is_el_there)
        self.out.fillBranch("TopSA_is_Mu_there", is_mu_there)

        self.out.fillBranch("Top_Wrong_pt", top_wrong_pt)
        self.out.fillBranch("Top_Wrong_eta", top_wrong_eta)
        self.out.fillBranch("Top_Wrong_phi", top_wrong_phi)
        self.out.fillBranch("Top_Wrong_e", top_wrong_e)
        self.out.fillBranch("Top_Wrong_M", top_wrong_M)
                        
        """Branches LHE"""
        

        """Promptness"""
        self.out.fillBranch("Is_Muon_Prompt", is_mu_prompt_index)
        self.out.fillBranch("Is_El_Prompt", is_el_prompt_index)
        
        """New Top Categories"""
        self.out.fillBranch("Is_Jet_Standalone", is_jet_standalone_index)
        self.out.fillBranch("Is_Top_Wrong", is_top_wrong_index)
        
        return True

unpacking_MC = lambda: unpacking_vers2(1)
unpacking_Data = lambda: unpacking_vers2(0)



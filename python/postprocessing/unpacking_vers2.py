import ROOT
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
        self.out.branch("Top_M","F", lenVar="nTop")

        """Branch variabili top con nu"""

        self.out.branch("Top_nu_pt","F", lenVar="nTop") 
        self.out.branch("Top_nu_eta","F", lenVar="nTop")
        self.out.branch("Top_nu_phi","F", lenVar="nTop")
        self.out.branch("Top_nu_e","F", lenVar="nTop")
        self.out.branch("Top_nu_M","F", lenVar="nTop")
        
        """Branch indici goodJet e goodMu"""
        self.out.branch("Top_bjet_index","I", lenVar="nTop")
        self.out.branch("Top_mu_index","I", lenVar="nTop")
        self.out.branch("Top_el_index","I", lenVar="nTop")

        """Muon and bjet unboosted (top frame)"""
        
        self.out.branch("Top_Jet_unboosted_pt","F", lenVar="nTop") 
        self.out.branch("Top_Jet_unboosted_eta","F", lenVar="nTop")
        self.out.branch("Top_Jet_unboosted_phi","F", lenVar="nTop")
        self.out.branch("Top_Jet_unboosted_e","F", lenVar="nTop")
        self.out.branch("Top_Jet_unboosted_M","F", lenVar="nTop")
        self.out.branch("Top_Jet_has_promptLep","O", lenVar="nTop")

        self.out.branch("Top_Lep_unboosted_pt","F", lenVar="nTop") 
        self.out.branch("Top_Lep_unboosted_eta","F", lenVar="nTop")
        self.out.branch("Top_Lep_unboosted_phi","F", lenVar="nTop")
        self.out.branch("Top_Lep_unboosted_e","F", lenVar="nTop")
        self.out.branch("Top_Lep_unboosted_M","F", lenVar="nTop")
        
        self.out.branch("Top_pt_rel","F", lenVar="nTop")
        self.out.branch("Top_Is_dR_merg","I", lenVar="nTop")
        self.out.branch("Top_Costheta","F", lenVar="nTop")
        self.out.branch("Top_dR","F",lenVar="nTop")

        """Branch variabili Top senza leptone (jet standalone)"""
        self.out.branch("Top_Jet_Standalone_pt", "F", lenVar="nTop")
        self.out.branch("Top_Jet_Standalone_eta", "F", lenVar="nTop")
        self.out.branch("Top_Jet_Standalone_phi", "F", lenVar="nTop")
        self.out.branch("Top_Jet_Standalone_e", "F", lenVar="nTop")
        self.out.branch("Top_Jet_Standalone_M", "F", lenVar="nTop")


        """Variabili per la definizione della Truth"""
        
        self.out.branch("Top_LHE_Truth", "i", lenVar="nTop") #It is i, you can put I or F I
        self.out.branch("Lepton_Flavour", "F", lenVar="nTop") # It is I, you can putalso F
        self.out.branch("Lepton_LHE_Flavour", "F", lenVar="nTop")
        
        self.out.branch("Muon_mindR","F", lenVar="nMuon")
        self.out.branch("Muon_mindR_jIndex","I", lenVar="nMuon")
        self.out.branch("Electron_mindR","F", lenVar="nElectron")
        self.out.branch("Electron_mindR_jIndex","I", lenVar="nElectron")
        
        """Branches per i good muons e electrons"""
        
        self.out.branch("nGoodMu", "i")
        self.out.branch("GoodMu_pt", "F", lenVar="nGoodMu")
        self.out.branch("GoodMu_eta", "F", lenVar="nGoodMu")
        self.out.branch("GoodMu_phi", "F", lenVar="nGoodMu")
        
        self.out.branch("nGoodEl", "i")
        self.out.branch("GoodEl_pt", "F", lenVar="nGoodEl")
        self.out.branch("GoodEl_eta", "F", lenVar="nGoodEl")
        self.out.branch("GoodEl_phi", "F", lenVar="nGoodEl")
        
        self.out.branch("nGoodJet", "i")

#        self.out.branch("GoodMu_mindR", "F", lenVar="nGoodMu")
#        self.out.branch("GoodEl_mindR", "F", lenVar="nGoodEl")

        """Branches LHE"""
        
        self.out.branch("LHEPart_Mu_dR", "F", lenVar="nGoodMu")
        self.out.branch("LHEPart_Mu_pt", "F", lenVar="nGoodMu")
        self.out.branch("LHEPart_Mu_eta", "F", lenVar="nGoodMu")
        self.out.branch("LHEPart_Mu_phi", "F", lenVar="nGoodMu")

        self.out.branch("LHEPart_El_dR", "F", lenVar="nGoodEl")
        self.out.branch("LHEPart_El_pt", "F", lenVar="nGoodEl")
        self.out.branch("LHEPart_El_eta", "F", lenVar="nGoodEl")
        self.out.branch("LHEPart_El_phi", "F", lenVar="nGoodEl")

        self.out.branch("LHEPart_Jet_dR", "F", lenVar="nGoodJet")
        self.out.branch("LHEPart_Jet_pt", "F", lenVar="nGoodJet")
        self.out.branch("LHEPart_Jet_eta", "F", lenVar="nGoodJet")
        self.out.branch("LHEPart_Jet_phi", "F", lenVar="nGoodJet")

        """Variabili per la promptness"""

        self.out.branch("Is_Muon_Prompt", "O", lenVar="nGoodMu")
        self.out.branch("Is_El_Prompt", "O", lenVar="nGoodEl")

        """Nuova top category con lep LHE ma senza lep reco"""
        #self.out.branch("Top_JetStandalone_M", "F", lenvar= "nTop")        
        #self.out.branch("Top_JetStandalone_pt", "F", lenvar= "nTop")
        #self.out.branch("Top_JetStandalone_eta", "F", lenvar= "nTop")
        #self.out.branch("Top_JetStandalone_phi", "F", lenvar= "nTop")

        """Variabile discrepancy tra lep LHE e lep reco"""
        self.out.branch("Is_Jet_Standalone", "O", lenVar= "nGoodJet")

        self.ninit=0
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
        top_M = []

        """Variabili top con nu"""
        top_nu_momentum_utils= TopUtilities()
        top_nu_pt = []
        top_nu_phi = []
        top_nu_eta = []
        top_nu_e = []
        top_nu_M = []

        top_nu_momentum = ROOT.TLorentzVector()
        top_nu_momentum_neg = ROOT.TLorentzVector()
        IsmcNeg = False
        mcdR_lepjet = None
        costheta = []

        top_lhe_truth = []
        
        """variabili bjet e muon"""
        top_bjet_index = []
        top_mu_index = []
        top_el_index = []

        lep_unboosted_momentum = ROOT.TLorentzVector()
        lep_unboosted_pt =[]
        lep_unboosted_phi = []
        lep_unboosted_eta = []
        lep_unboosted_e = []
        lep_unboosted_M = []

        jet_unboosted_momentum = ROOT.TLorentzVector()
        jet_unboosted_pt =[]
        jet_unboosted_phi = []
        jet_unboosted_eta = []
        jet_unboosted_e = []
        jet_unboosted_M = []

        top_pt_rel = []
        is_dR_merg = []
        top_dR = []

        """Variabili jet standalone"""
        #top_jsa_momentum = ROOT.TLorentzVector()
        #top_jsa_pt = []
        #top_jsa_phi = []
        #top_jsa_eta = []
        #top_jsa_M = []
        #top_jsa_e = []

        top_high_truth = []
        jet_has_pL = []

        lep_MomId = []
        muon_mindR = []
        muon_mindR_jIndex = []
        electron_mindR = []
        electron_mindR_jIndex = []

        goodmu_mindR = []
        goodmu_mindR_jIndex = []
        goodel_mindR = []
        goodel_mindR_jIndex = []

        goodmu_momentum = ROOT.TLorentzVector()
        goodmu_pt = []
        goodmu_eta = []
        goodmu_phi = []

        goodel_momentum = ROOT.TLorentzVector()
        goodel_pt = []
        goodel_eta = []
        goodel_phi = []

        lhe_Mu_dR = []
        lhe_Mu_momentum = ROOT.TLorentzVector()
        lhe_Mu_pt = []
        lhe_Mu_eta = []
        lhe_Mu_phi = []
        
        lhe_El_dR = []
        lhe_El_momentum = ROOT.TLorentzVector()
        lhe_El_pt = []
        lhe_El_eta = []
        lhe_El_phi = []

        lhe_Jet_dR = []
        lhe_Jet_momentum = ROOT.TLorentzVector()
        lhe_Jet_pt = []
        lhe_Jet_eta = []
        lhe_Jet_phi = []

        lepton_flavour = []
        lepton_lhe_flavour = []

        is_mu_prompt_index = []
        is_el_prompt_index = []

        #goodmu_minDr = []
        #goodel_minDr = []
        
        is_jet_standalone = []
        is_jet_standalone_index = []

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

        nTop = (nGoodMu + nGoodEl)*nGoodJet
                
                    
            
        if not ((len(goodMu)>0 or len(goodEl)>0) and len(goodJet)>0 ):
            
            return False
        
        else:

            """
            Creazione Min_dr per leptoni
            """
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

                #goodMu.minDr = muon_minDR_jIndex#farlo per tutte le variabili per cui fai il loop all'interno dei goodMu nestato nel loop dei jet

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


#            for m in allMu:

#                if m in goodMu:

#                    is_muon_prompt = False
#                    muon_LHE_match = False #If there is no match at LHE level
#                    muon_from_tau = 0
#                    for l in LHE:
#                        if((abs(l.pdgId) == 13) and  (deltaR(m.p4().Eta(),m.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <= 0.1)):
#                            
#                            muon_LHE_match = True
#                            lhe_Mu_dR.append(deltaR(m.p4().Eta(),m.p4().Phi(),l.p4().Eta(),l.p4().Phi()))
#                            lhe_Mu_momentum = l.p4()
#                            lhe_Mu_pt.append(lhe_Mu_momentum.Pt())
#                            lhe_Mu_eta.append(lhe_Mu_momentum.Eta())
#                            lhe_Mu_phi.append(lhe_Mu_momentum.Phi())
#                            is_muon_prompt=True
#                    if muon_LHE_match == False:
#                        lhe_Mu_dR.append(-999.0) # Fill this out with -999 for example, since this variables are empty for the good muons when they are not matched at LHE level.
#                        lhe_Mu_pt.append(-999.0)
#                        lhe_Mu_eta.append(-999.0)
#                        lhe_Mu_phi.append(-999.0)
                            
                        #lepton_flavour.append(l.pdgId)
#                    is_mu_prompt_index.append(is_muon_prompt)
#                    if (verbose):print("goodMu index append:", is_muon_prompt, "good mu index m:", is_mu_prompt_index)
#                    if (verbose):print("goodMu index m",goodMu.index(m)," goodMu pt ", m.p4().Pt())
#                    goodmu_momentum = m.p4()
#                    goodmu_pt.append(goodmu_momentum.Pt())
#                    goodmu_eta.append(goodmu_momentum.Eta())
#                    goodmu_phi.append(goodmu_momentum.Phi())
 
            
            for e in allEl:
                
                if e in goodEl:
                    is_el_from_tau = 0
                    is_el_prompt = False
                    electron_LHE_match = False
                    for l in LHE:
                        if((abs(l.pdgId) == 11) and  (deltaR(e.p4().Eta(),e.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <=0.3)):#check value for dR!!! I have seen also 0.1 for electrons??
                            electron_LHE_match = True
                            lhe_El_dR.append(deltaR(e.p4().Eta(),e.p4().Phi(),l.p4().Eta(),l.p4().Phi()))
                            lhe_El_momentum = l.p4()
                            lhe_El_pt.append(lhe_El_momentum.Pt())
                            lhe_El_eta.append(lhe_El_momentum.Eta())
                            lhe_El_phi.append(lhe_El_momentum.Phi())
                            is_el_prompt=True
                    if electron_LHE_match == False:
                        lhe_El_dR.append(-999.0)
                        lhe_El_pt.append(-999.0)
                        lhe_El_eta.append(-999.0)
                        lhe_El_phi.append(-999.0)
                            
                    is_el_prompt_index.append(is_el_prompt)
                    goodel_momentum = e.p4()
                    goodel_pt.append(goodel_momentum.Pt())
                    goodel_eta.append(goodel_momentum.Eta())
                    goodel_phi.append(goodel_momentum.Phi())
                        
            """Creazione top cands"""

            for j in allJet:  

                if j in goodJet:

                    is_jet_true = False
                    jet_LHE_match = False
                    
                    jet_has_promptLep = False 
                    is_jet_standalone = False
                    if abs(j.partonFlavour)==5:
                        is_jet_true = True
                    for l in LHE:
                        if((abs(l.pdgId) == 5)) and (deltaR(j.p4().Eta(),j.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <0.4) :
                                jet_LHE_match = True
                                lhe_Jet_dR.append(deltaR(j.p4().Eta(),j.p4().Phi(),l.p4().Eta(),l.p4().Phi()))
                                lhe_Jet_momentum = l.p4()
                                lhe_Jet_pt.append(lhe_Jet_momentum.Pt())
                                lhe_Jet_eta.append(lhe_Jet_momentum.Eta())
                                lhe_Jet_phi.append(lhe_Jet_momentum.Phi())
                                #is_jet_true = True
                        if((abs(l.pdgId) == 13)) and deltaR(j.p4().Eta(),j.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <0.4:
                            jet_has_promptLep=True
                            lepton_lhe_flavour.append(l.pdgId)

                            goodmu_mindR = closest(l, goodMu)
                            if goodmu_mindR>0.1:
                                is_jet_standalone = True
                        if((abs(l.pdgId) == 11)) and deltaR(j.p4().Eta(),j.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <0.4:
                            jet_has_promptLep=True
                            lepton_lhe_flavour.append(l.pdgId)

                            goodel_mindR = closest(l, goodEl)
                            if goodel_mindR>0.3:
                                is_jet_standalone = True

                    jet_has_pL.append(jet_has_promptLep)
                    
                    if jet_LHE_match == False:
                        lhe_Jet_dR.append(-999.0)
                        lhe_Jet_pt.append(-999.0)
                        lhe_Jet_eta.append(-999.0)
                        lhe_Jet_phi.append(-999.0)
                                    
                    is_jet_standalone_index.append(is_jet_standalone)


                    for m in allMu:
                        
                        if m in goodMu:
                            #is_muon_prompt = is_mu_prompt_index[goodMu.index(m)]
                            #jet_has_pL.append(jet_has_promptLep)
                            is_muon_prompt = False
                            muon_LHE_match = False #If there is no match at LHE level
                            muon_from_tau = 0

                            goodmu_momentum = m.p4()
                            goodmu_pt.append(goodmu_momentum.Pt())
                            goodmu_eta.append(goodmu_momentum.Eta())
                            goodmu_phi.append(goodmu_momentum.Phi())

                            lepton_flavour.append((-13)*(m.charge))
                            top_bjet_index.append(allJet.index(j))
                            top_mu_index.append(allMu.index(m))
                            top_el_index.append(-1)
                            

                            for l in LHE:
                                if((abs(l.pdgId) == 13) and  (deltaR(m.p4().Eta(),m.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <= 0.1)):
                                    print(" we are in LHE, eta phi is:",l.p4().Eta(), " ",l.p4().Phi()," goodMu in LHE eta phi is: ",m.p4().Eta(), " ",m.p4().Phi())
                                    muon_LHE_match = True
                                    lhe_Mu_dR.append(deltaR(m.p4().Eta(),m.p4().Phi(),l.p4().Eta(),l.p4().Phi()))
                                    lhe_Mu_momentum = l.p4()
                                    lhe_Mu_pt.append(lhe_Mu_momentum.Pt())
                                    lhe_Mu_eta.append(lhe_Mu_momentum.Eta())
                                    lhe_Mu_phi.append(lhe_Mu_momentum.Phi())
                                    is_muon_prompt=True
                            if muon_LHE_match == False:
                                lhe_Mu_dR.append(-999.0) # Fill this out with -999 for example, since this variables are empty for the good muons when they are not matched at LHE level.
                                lhe_Mu_pt.append(-999.0)
                                lhe_Mu_eta.append(-999.0)
                                lhe_Mu_phi.append(-999.0)
                            

                                if((abs(l.pdgId) == 13)) and deltaR(j.p4().Eta(),j.p4().Phi(),l.p4().Eta(),l.p4().Phi()) <0.4:
                                    jet_has_promptLep=True
                                    lepton_lhe_flavour.append(l.pdgId)

                            goodmu_mindR = closest(l, goodMu)
                            if goodmu_mindR>0.1:
                                is_jet_standalone = True
                        
                            is_mu_prompt_index.append(is_muon_prompt)
                            print ("muon prompt label: ", is_mu_prompt_index)

#                            lepton_flavour.append((-13)*(m.charge))
#                            top_bjet_index.append(allJet.index(j))
#                            top_mu_index.append(allMu.index(m))
#                            top_el_index.append(-1)
                            
                            
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
                            top_M.append(top_momentum.M())
#                            jet_has_pL.append(is_muon_prompt)

         
                            if top_nu_momentum is None:
                               return False

                            top_nu_pt.append(top_nu_momentum.Pt())
                            top_nu_phi.append(top_nu_momentum.Phi())
                            top_nu_eta.append(top_nu_momentum.Eta())
                            top_nu_e.append(top_nu_momentum.E())
                            top_nu_M.append(top_nu_momentum.M())  

#                            good_muon_pt.append(good_muon_momentum.Pt())
#                            good_muon_eta.append(good_muon_momentum.Eta())
#                            good_muon_phi.append(good_muon_momentum.Phi())


                            top_pt_rel.append(((m.p4().Vect()).Cross(j.p4().Vect())).Mag()/((j.p4().Vect()).Mag())) 

                            """unboosting"""
                            top_nu_momentum_neg.SetPxPyPzE(-top_nu_momentum.Px(),-top_nu_momentum.Py(),-top_nu_momentum.Pz(),top_nu_momentum.E())

                            lep_unboosted_momentum = m.p4()
                            lep_unboosted_momentum.Boost(top_nu_momentum_neg.BoostVector())
                            lep_unboosted_pt.append(lep_unboosted_momentum.Pt())
                            lep_unboosted_phi.append(lep_unboosted_momentum.Phi())
                            lep_unboosted_eta.append(lep_unboosted_momentum.Eta())
                            lep_unboosted_e.append(lep_unboosted_momentum.E())
                            lep_unboosted_M.append(lep_unboosted_momentum.M())

                            jet_unboosted_momentum = j.p4()
                            jet_unboosted_momentum.Boost(top_nu_momentum_neg.BoostVector())

                            jet_unboosted_pt.append(jet_unboosted_momentum.Pt())
                            jet_unboosted_phi.append(jet_unboosted_momentum.Phi())
                            jet_unboosted_eta.append(jet_unboosted_momentum.Eta())
                            jet_unboosted_e.append(jet_unboosted_momentum.E())
                            jet_unboosted_M.append(jet_unboosted_momentum.M())

                            if deltaR(j.p4().Eta(),j.p4().Phi(),m.p4().Eta(),m.p4().Phi()) <=0.4:
                                top_dR.append(deltaR((j.p4()-m.p4()).Eta(),(j.p4()-m.p4()).Phi(),m.p4().Eta(),m.p4().Phi()))
                            else:
                                top_dR.append(deltaR(j.p4().Eta(),j.p4().Phi(),m.p4().Eta(),m.p4().Phi()))                                

                            costheta.append(top_nu_momentum_utils.costhetapol(m.p4(),j.p4(),top_nu_momentum))

                        
    
                            #is_jet_standalone = is_jet_standalone_index[LHE.index(l)]

                            if(verbose):print('--- Muon ---')
                            
                            if (is_jet_true == True and is_muon_prompt== True):
                                if (j.partonFlavour*m.charge)>0:
                                    top_lhe_truth.append(0)
                                    if(verbose):print('is truth 0')
                                else: 
                                    top_lhe_truth.append(1)
                                    if(verbose):print('is truth 1')
                                        
                            if (is_jet_true == True  and is_muon_prompt== False and jet_has_promptLep == True):
                                top_lhe_truth.append(2)
                                if(verbose):print('is truth 2')

                            if (is_jet_true == True  and is_muon_prompt== False and jet_has_promptLep == False):
                                top_lhe_truth.append(3)
                                if(verbose):print('is truth 3')

                            if (is_jet_true == False and is_muon_prompt== True):
                                top_lhe_truth.append(4)
                                if(verbose):print('is truth 4')

                            if (is_jet_true == False and is_muon_prompt== False):
                                top_lhe_truth.append(5)
                                if(verbose):print('is truth 5')
                                
                            if (is_jet_true == True and jet_has_promptLep == True and is_jet_standalone == True):
                                top_lhe_truth.append(6)

                            if(verbose):print('Size Top_LHE_Truth: ',len(top_lhe_truth), " ntop ",nTop)
                                
                    
                    for e in allEl:
                        
                        if e in goodEl:
                            is_el_prompt = is_el_prompt_index[goodEl.index(e)]    
                            lepton_flavour.append((-11)*(e.charge))
                            top_bjet_index.append(allJet.index(j))
                            top_mu_index.append(-1)
                            top_el_index.append(allEl.index(e))
        

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
                            top_M.append(top_momentum.M())
#                            jet_has_pL.append(is_el_prompt)

                            if top_nu_momentum is None:
                               return False
         
                            top_nu_pt.append(top_nu_momentum.Pt())
                            top_nu_phi.append(top_nu_momentum.Phi())
                            top_nu_eta.append(top_nu_momentum.Eta())
                            top_nu_e.append(top_nu_momentum.E())
                            top_nu_M.append(top_nu_momentum.M())  

          
                            top_pt_rel.append(((e.p4().Vect()).Cross(j.p4().Vect())).Mag()/((j.p4().Vect()).Mag())) 

                            #ood_el_pt.append(good_el_momentum.Pt())
                            #ood_el_eta.append(good_el_momentum.Eta())
                            #ood_el_phi.append(good_el_momentum.Phi())
                            
                                  
                            
                            """unboosting"""
                            top_nu_momentum_neg.SetPxPyPzE(-top_nu_momentum.Px(),-top_nu_momentum.Py(),-top_nu_momentum.Pz(),top_nu_momentum.E())

                            lep_unboosted_momentum = e.p4()
                            lep_unboosted_momentum.Boost(top_nu_momentum_neg.BoostVector())
                            lep_unboosted_pt.append(lep_unboosted_momentum.Pt())
                            lep_unboosted_phi.append(lep_unboosted_momentum.Phi())
                            lep_unboosted_eta.append(lep_unboosted_momentum.Eta())
                            lep_unboosted_e.append(lep_unboosted_momentum.E())
                            lep_unboosted_M.append(lep_unboosted_momentum.M())

                            jet_unboosted_momentum = j.p4()
                            jet_unboosted_momentum.Boost(top_nu_momentum_neg.BoostVector())

                            jet_unboosted_pt.append(jet_unboosted_momentum.Pt())
                            jet_unboosted_phi.append(jet_unboosted_momentum.Phi())
                            jet_unboosted_eta.append(jet_unboosted_momentum.Eta())
                            jet_unboosted_e.append(jet_unboosted_momentum.E())
                            jet_unboosted_M.append(jet_unboosted_momentum.M())


                            if deltaR(j.p4().Eta(),j.p4().Phi(),e.p4().Eta(),e.p4().Phi()) <=0.1:
                                top_dR.append(deltaR((j.p4()-e.p4()).Eta(),(j.p4()-e.p4()).Phi(),e.p4().Eta(),e.p4().Phi()))
                            else:
                                top_dR.append(deltaR(j.p4().Eta(),j.p4().Phi(),e.p4().Eta(),e.p4().Phi())) 

                            costheta.append(top_nu_momentum_utils.costhetapol(e.p4(),j.p4(),top_nu_momentum))
                            
                            if(verbose):print('--- Electron ---')

                            if (is_jet_true == True and is_el_prompt== True):
                                if (j.partonFlavour*e.charge)>0:
                                    top_lhe_truth.append(0)
                                    if(verbose):print('is truth 0')
                                else:
                                    top_lhe_truth.append(1)
                                    if(verbose):print('is truth 1')

                            if (is_jet_true == True and is_el_prompt== False and jet_has_promptLep == True):
                                top_lhe_truth.append(2)
                                if(verbose):print('is truth 2')

                            if (is_jet_true == True and is_el_prompt== False and jet_has_promptLep == False):
                                top_lhe_truth.append(3)
                                if(verbose):print('is truth 3')
                            if (is_jet_true == False  and is_el_prompt== True):
                                top_lhe_truth.append(4)
                                if(verbose):print('is truth 4')

                            if (is_jet_true == False and is_el_prompt== False):
                                top_lhe_truth.append(5)
                                if(verbose):print('is truth 5')

                            if (is_jet_true == True and jet_has_promptLep == True and is_jet_standalone == True):
                                top_lhe_truth.append(6)

                            if(verbose):print('Size Top_LHE_Truth: ',len(top_lhe_truth), " ntop ",nTop)




        #IMPORTANT: Here it should be better to reject the events with ONLY tops with DeltaR>2                        

        self.out.fillBranch("nTop", nTop)
       
        self.out.fillBranch("Top_pt", top_pt)
        self.out.fillBranch("Top_phi", top_phi)
        self.out.fillBranch("Top_eta", top_eta)
        self.out.fillBranch("Top_e", top_e)
        self.out.fillBranch("Top_M", top_M)
        
        self.out.fillBranch("Top_nu_pt", top_nu_pt)
        self.out.fillBranch("Top_nu_phi", top_nu_phi)
        self.out.fillBranch("Top_nu_eta", top_nu_eta)
        self.out.fillBranch("Top_nu_e", top_nu_e)
        self.out.fillBranch("Top_nu_M", top_nu_M)
        
        self.out.fillBranch("Top_bjet_index", top_bjet_index)
        self.out.fillBranch("Top_mu_index", top_mu_index)
        self.out.fillBranch("Top_el_index", top_el_index)
        
        self.out.fillBranch("Top_Jet_unboosted_pt",jet_unboosted_pt) 
        self.out.fillBranch("Top_Jet_unboosted_eta",jet_unboosted_eta)
        self.out.fillBranch("Top_Jet_unboosted_phi",jet_unboosted_phi)
        self.out.fillBranch("Top_Jet_unboosted_e",jet_unboosted_e)
        self.out.fillBranch("Top_Jet_unboosted_M",jet_unboosted_M)
        self.out.fillBranch("Top_Jet_has_promptLep",jet_has_pL)
        #add jet_has_promptLep
        #self.....("Top_promptLep", is_prompt_lep)
        
        self.out.fillBranch("Top_Lep_unboosted_pt",lep_unboosted_pt) 
        self.out.fillBranch("Top_Lep_unboosted_eta",lep_unboosted_eta)
        self.out.fillBranch("Top_Lep_unboosted_phi",lep_unboosted_phi)
        self.out.fillBranch("Top_Lep_unboosted_e",lep_unboosted_e)
        self.out.fillBranch("Top_Lep_unboosted_M",lep_unboosted_M)
        
        self.out.fillBranch("Top_pt_rel", top_pt_rel)
        self.out.fillBranch("Top_Is_dR_merg",is_dR_merg)
        self.out.fillBranch("Top_Costheta", costheta)
        self.out.fillBranch("Top_dR", top_dR)
        
         #self.out.fillBranch("Top_High_Truth",top_high_truth)
         #self.out.fillBranch("Top_Tau_High_Truth",tau_high_truth)
         #self.out.fillBranch("Top_Lep_MomId",lep_MomId)
        self.out.fillBranch("Muon_mindR", muon_mindR)
        self.out.fillBranch("Muon_mindR_jIndex", muon_mindR_jIndex)
        self.out.fillBranch("Electron_mindR", electron_mindR)
        self.out.fillBranch("Electron_mindR_jIndex", electron_mindR_jIndex)

        self.out.fillBranch("Top_LHE_Truth", top_lhe_truth)
        self.out.fillBranch("Lepton_Flavour", lepton_flavour)
        self.out.fillBranch("Lepton_LHE_Flavour", lepton_lhe_flavour)
        
        """Branches per good muons, electrons e jets"""
        
        self.out.fillBranch("nGoodMu", nGoodMu)
        self.out.fillBranch("GoodMu_pt", goodmu_pt)
        self.out.fillBranch("GoodMu_eta", goodmu_eta)
        self.out.fillBranch("GoodMu_phi", goodmu_phi)


        self.out.fillBranch("nGoodEl", nGoodEl)
        self.out.fillBranch("GoodEl_pt", goodel_pt)
        self.out.fillBranch("GoodEl_eta", goodel_eta)
        self.out.fillBranch("GoodEl_phi", goodel_phi)

        self.out.fillBranch("nGoodJet", nGoodJet)

#        self.out.fillBranch("GoodMu_mindR", goodmu_mindR)
#        self.out.fillBranch("GoodEl_mindR", goodel_mindR)

        self.out.fillBranch("Is_Jet_Standalone", is_jet_standalone_index)



        """Branches LHE"""

        self.out.fillBranch("LHEPart_Mu_dR", lhe_Mu_dR)
        self.out.fillBranch("LHEPart_Mu_pt", lhe_Mu_pt)
        self.out.fillBranch("LHEPart_Mu_eta", lhe_Mu_eta)
        self.out.fillBranch("LHEPart_Mu_phi", lhe_Mu_phi)

        self.out.fillBranch("LHEPart_El_dR", lhe_El_dR)
        self.out.fillBranch("LHEPart_El_pt", lhe_El_pt)
        self.out.fillBranch("LHEPart_El_eta", lhe_El_eta)
        self.out.fillBranch("LHEPart_El_phi", lhe_El_phi)

        self.out.fillBranch("LHEPart_Jet_dR", lhe_Jet_dR)
        self.out.fillBranch("LHEPart_Jet_pt", lhe_Jet_pt)
        self.out.fillBranch("LHEPart_Jet_eta", lhe_Jet_eta)
        self.out.fillBranch("LHEPart_Jet_phi", lhe_Jet_phi)

        """Promptness"""

        self.out.fillBranch("Is_Muon_Prompt", is_mu_prompt_index)
        self.out.fillBranch("Is_El_Prompt", is_el_prompt_index)

        return True

unpacking_MC = lambda: unpacking_vers2(1)
unpacking_Data = lambda: unpacking_vers2(0)

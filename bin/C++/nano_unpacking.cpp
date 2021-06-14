#include "TFile.h"
#include "TChain.h"
#include "TChainElement.h"
#include "TTree.h"
#include "TBranch.h"
#include "TH1.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TLorentzVector.h"
#include "RooGlobalFunc.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include <vector>
#include <assert.h>
#include <TMVA/Reader.h>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <cassert>
#include <sstream>
#include <string>
#include "TFileCollection.h"
#include "THashList.h"
#include "TBenchmark.h"
#include "TF1.h"
//#include "../../interface/DMTopVariables.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondTools/BTau/interface/BTagCalibrationReader.h"

using namespace std;


int main(int argc, char **argv)
{
    string path(argv[1]);    // List of root input files (.txt)

    string outFile(argv[2]); // Name of output file

    TFileCollection fc("FileCollection", "FileCollection", path.c_str());

    TString treePath = "Events";

    TChain chain(treePath);
    chain.AddFileInfoList(fc.GetList());

    /* ---------------- Add Sample Info --------------- */
    
    TObjArray *fileElements = chain.GetListOfFiles();
    TIter next(fileElements);
    TChainElement *chEl = 0;
    int nFiles = fc.GetNFiles();
    string filename[nFiles]; 
    int nEntries[nFiles];
    int l = 0;
    int N = 0;
    while (( chEl = (TChainElement*)next() )) {
      filename[l] = chEl->GetTitle();
      TFile f(chEl->GetTitle());
      TTree *T = (TTree*)f.Get("Events");
      nEntries[l] = T->GetEntries();
      l++;
    }
    int sum = 0;
    for(l=1;l<nFiles;l++){
      sum = nEntries[l-1];
      nEntries[l] = nEntries[l] + sum;
    }

    for(l=0;l<nFiles;l++){
      cout<<"Filename: "<<filename[l]<<endl;
      cout<<"# of Entries: "<<nEntries[l]<<endl;
    }
    
    /* ---------------- Input Variables --------------- */

    int sizeMax = 30;
    int sizeMaxTop = 300;

    Float_t MET;
    Float_t MET_phi;

    Float_t Jet_mass[sizeMax];
    Float_t Jet_pt[sizeMax];
    Float_t Jet_phi[sizeMax];
    Float_t Jet_eta[sizeMax];
    Float_t Jet_isDeep[sizeMax];         
    Int_t Jet_hadronFlavour[sizeMax]; 
    Int_t Jet_partonFlavour[sizeMax]; 
    Int_t Jet_Id[sizeMax];
    UInt_t Jet_size;

    Float_t Mu_mass[sizeMax];
    Float_t Mu_pt[sizeMax];
    Float_t Mu_phi[sizeMax];
    Float_t Mu_eta[sizeMax];
    Int_t Mu_charge[sizeMax];
    Float_t Mu_Dxy[sizeMax];
    Float_t Mu_Dxyerr[sizeMax];
    Float_t Mu_Dz[sizeMax];
    Float_t Mu_Dzerr[sizeMax];
    Bool_t Mu_isLoose[sizeMax];
    Bool_t Mu_isMedium[sizeMax];
    Bool_t Mu_isTight[sizeMax];
    Bool_t Mu_isGlobal[sizeMax];  
    Bool_t Mu_isTracker[sizeMax];
    Int_t Mu_nStations[sizeMax];
    Int_t Mu_nTrackerLayers[sizeMax];
    UChar_t Mu_genPFlav[sizeMax];
    UChar_t Mu_HighPtId[sizeMax]; // Care!!
    Float_t Mu_MiniIso[sizeMax];
    Float_t Mu_Iso04[sizeMax];
    UInt_t Mu_size;

    Float_t El_pt[sizeMax];  
    Float_t El_mass[sizeMax];
    Float_t El_phi[sizeMax];
    Float_t El_eta[sizeMax];
    Int_t El_charge[sizeMax];
    Float_t El_Dxy[sizeMax];
    Float_t El_Dxyerr[sizeMax];
    Float_t El_Dz[sizeMax];
    Float_t El_Dzerr[sizeMax];
    Int_t El_cutBased[sizeMax];
    UChar_t El_genPFlav[sizeMax];
    Float_t El_MiniIso[sizeMax];
    Float_t El_Iso03[sizeMax];
    Bool_t El_IsoL[sizeMax];
    Bool_t El_Iso90[sizeMax];
    Bool_t El_Iso80[sizeMax];
    Bool_t El_noIsoL[sizeMax];
    Bool_t El_noIso90[sizeMax];
    Bool_t El_noIso80[sizeMax];
    UInt_t El_size;

    Float_t Top_mass[sizeMaxTop];
    Float_t Top_pt[sizeMaxTop];
    Float_t Top_phi[sizeMaxTop];
    Float_t Top_eta[sizeMaxTop];
    Float_t Top_E[sizeMaxTop];
    Float_t lj_mass[sizeMaxTop];
    Float_t lj_pt[sizeMaxTop];
    Float_t lj_phi[sizeMaxTop];
    Float_t lj_eta[sizeMaxTop];
    Float_t lj_E[sizeMaxTop];
    Int_t el_idx[sizeMaxTop];
    Int_t mu_idx[sizeMaxTop];
    Int_t jet_idx[sizeMaxTop];
    Float_t Top_jet_unboosted_mass[sizeMaxTop];
    Float_t Top_jet_unboosted_pt[sizeMaxTop];
    Float_t Top_jet_unboosted_phi[sizeMaxTop];
    Float_t Top_jet_unboosted_eta[sizeMaxTop];
    Float_t Top_jet_unboosted_E[sizeMaxTop];
    Int_t Top_jet_hasPromptLep[sizeMaxTop];
    Float_t Top_lep_unboosted_mass[sizeMaxTop];
    Float_t Top_lep_unboosted_pt[sizeMaxTop];
    Float_t Top_lep_unboosted_phi[sizeMaxTop];
    Float_t Top_lep_unboosted_eta[sizeMaxTop];
    Float_t Top_lep_unboosted_E[sizeMaxTop];
    Float_t Top_relPt[sizeMaxTop];
    Float_t Top_cosTheta[sizeMaxTop];
    Float_t Top_dR[sizeMaxTop];
    Int_t Top_isMerged[sizeMaxTop];
    Int_t Top_Category[sizeMaxTop];
    Int_t Top_Tau_High_Truth[sizeMaxTop];
    Int_t Top_High_Truth;
    UInt_t nTop;


    /* ----------------------- Input Branches  -------------------- */

    chain.SetBranchAddress("MET_pt", &MET);
    chain.SetBranchAddress("MET_phi", &MET_phi);

    chain.SetBranchAddress("Jet_mass", &Jet_mass);
    chain.SetBranchAddress("Jet_pt", &Jet_pt);
    chain.SetBranchAddress("Jet_phi", &Jet_phi);
    chain.SetBranchAddress("Jet_eta", &Jet_eta);
    chain.SetBranchAddress("nJet", &Jet_size); 
    chain.SetBranchAddress("Jet_jetId", &Jet_Id); 
    chain.SetBranchAddress("Jet_partonFlavour", &Jet_partonFlavour); 
    chain.SetBranchAddress("Jet_hadronFlavour", &Jet_hadronFlavour); 
    chain.SetBranchAddress("Jet_btagDeepFlavB", &Jet_isDeep);

    chain.SetBranchAddress("Muon_pt", &Mu_pt);    
    chain.SetBranchAddress("Muon_mass", &Mu_mass); 
    chain.SetBranchAddress("Muon_phi", &Mu_phi); 
    chain.SetBranchAddress("Muon_eta", &Mu_eta);
    chain.SetBranchAddress("Muon_charge", &Mu_charge);
    chain.SetBranchAddress("Muon_dxy", &Mu_Dxy);
    chain.SetBranchAddress("Muon_dxyErr", &Mu_Dxyerr);
    chain.SetBranchAddress("Muon_dz", &Mu_Dz);
    chain.SetBranchAddress("Muon_dzErr", &Mu_Dzerr);
    chain.SetBranchAddress("Muon_looseId", &Mu_isLoose);
    chain.SetBranchAddress("Muon_mediumId", &Mu_isMedium);
    chain.SetBranchAddress("Muon_tightId", &Mu_isTight);
    chain.SetBranchAddress("Muon_isGlobal", &Mu_isGlobal);
    chain.SetBranchAddress("Muon_isTracker", &Mu_isTracker);
    chain.SetBranchAddress("Muon_nStations", &Mu_nStations);
    chain.SetBranchAddress("Muon_nTrackerLayers", &Mu_nTrackerLayers);
    chain.SetBranchAddress("Muon_genPartFlav", &Mu_genPFlav); 
    chain.SetBranchAddress("Muon_highPtId", &Mu_HighPtId); // Care!
    chain.SetBranchAddress("Muon_pfRelIso04_all", &Mu_Iso04);
    chain.SetBranchAddress("Muon_miniPFRelIso_all", &Mu_MiniIso);
    chain.SetBranchAddress("nMuon", &Mu_size); 

    chain.SetBranchAddress("Electron_pt", &El_pt);
    chain.SetBranchAddress("Electron_mass", &El_mass); 
    chain.SetBranchAddress("Electron_eta", &El_eta);
    chain.SetBranchAddress("Electron_phi", &El_phi);
    chain.SetBranchAddress("Electron_charge", &El_charge);
    chain.SetBranchAddress("Electron_dxy", &El_Dxy);
    chain.SetBranchAddress("Electron_dxyErr", &El_Dxyerr);
    chain.SetBranchAddress("Electron_dz", &El_Dz);
    chain.SetBranchAddress("Electron_dzErr", &El_Dzerr);
    chain.SetBranchAddress("Electron_cutBased", &El_cutBased);
    chain.SetBranchAddress("Electron_genPartFlav", &El_genPFlav);
    chain.SetBranchAddress("Electron_miniPFRelIso_all", &El_MiniIso);
    chain.SetBranchAddress("Electron_pfRelIso03_all", &El_Iso03);
    chain.SetBranchAddress("Electron_mvaFall17V2Iso_WPL", &El_IsoL);
    chain.SetBranchAddress("Electron_mvaFall17V2Iso_WP90", &El_Iso90);
    chain.SetBranchAddress("Electron_mvaFall17V2Iso_WP80", &El_Iso80);
    chain.SetBranchAddress("Electron_mvaFall17V2noIso_WPL", &El_noIsoL);
    chain.SetBranchAddress("Electron_mvaFall17V2noIso_WP90", &El_noIso90);
    chain.SetBranchAddress("Electron_mvaFall17V2noIso_WP80", &El_noIso80);
    chain.SetBranchAddress("nElectron", &El_size); 

    chain.SetBranchAddress("Top_nu_M", &Top_mass);
    chain.SetBranchAddress("Top_nu_pt", &Top_pt);
    chain.SetBranchAddress("Top_nu_phi", &Top_phi);
    chain.SetBranchAddress("Top_nu_eta", &Top_eta);
    chain.SetBranchAddress("Top_nu_e", &Top_E);
    chain.SetBranchAddress("Top_M", &lj_mass);
    chain.SetBranchAddress("Top_pt", &lj_pt);
    chain.SetBranchAddress("Top_phi", &lj_phi);
    chain.SetBranchAddress("Top_eta", &lj_eta);
    chain.SetBranchAddress("Top_e", &lj_E);
    chain.SetBranchAddress("Top_el_index", &el_idx); 
    chain.SetBranchAddress("Top_mu_index", &mu_idx); 
    chain.SetBranchAddress("Top_bjet_index", &jet_idx); 
    chain.SetBranchAddress("Top_Jet_unboosted_M", &Top_jet_unboosted_mass);
    chain.SetBranchAddress("Top_Jet_unboosted_pt", &Top_jet_unboosted_pt);
    chain.SetBranchAddress("Top_Jet_unboosted_eta", &Top_jet_unboosted_eta);
    chain.SetBranchAddress("Top_Jet_unboosted_phi", &Top_jet_unboosted_phi);
    chain.SetBranchAddress("Top_Jet_unboosted_e", &Top_jet_unboosted_E);
    chain.SetBranchAddress("Top_Jet_has_promptLep", &Top_jet_hasPromptLep);
    chain.SetBranchAddress("Top_Lep_unboosted_M", &Top_lep_unboosted_mass);
    chain.SetBranchAddress("Top_Lep_unboosted_pt", &Top_lep_unboosted_pt);
    chain.SetBranchAddress("Top_Lep_unboosted_eta", &Top_lep_unboosted_eta);
    chain.SetBranchAddress("Top_Lep_unboosted_phi", &Top_lep_unboosted_phi);
    chain.SetBranchAddress("Top_Lep_unboosted_e", &Top_lep_unboosted_E);
    chain.SetBranchAddress("Top_pt_rel", &Top_relPt);
    chain.SetBranchAddress("Top_Costheta", &Top_cosTheta);
    chain.SetBranchAddress("Top_dR", &Top_dR);
    chain.SetBranchAddress("Top_Is_dR_merg", &Top_isMerged);
    chain.SetBranchAddress("Top_High_Truth", &Top_Category);
    chain.SetBranchAddress("Top_Tau_High_Truth", &Top_Tau_High_Truth);
    chain.SetBranchAddress("nTop", &nTop);


    /* -------- Output Variables & Branches --------- */

    Float_t met_el_resolved = 0.;
    Float_t met_phi_el_resolved = 0.;

    Float_t jet_m_el_resolved = 0.;
    Float_t jet_pt_el_resolved = 0.;
    Float_t jet_eta_el_resolved = 0.;
    Float_t jet_phi_el_resolved = 0.;
    Int_t jet_Id_el_resolved = 0;
    Int_t jet_partFlav_el_resolved = 0;
    Int_t jet_hadFlav_el_resolved = 0;
    Float_t jet_isDeep_el_resolved = 0.;
    UInt_t nJet_el_resolved = 0;
    Int_t jet_idx_el_resolved = 0;

    Float_t el_pt_resolved = 0.;
    Float_t el_eta_resolved = 0.;
    Float_t el_phi_resolved = 0.;
    Int_t el_charge_resolved = 0;
    Float_t el_Dxy_resolved = 0.;
    Float_t el_DxyErr_resolved = 0.;
    Float_t el_Dz_resolved = 0.;
    Float_t el_DzErr_resolved = 0.;
    Int_t el_cutBased_resolved = 0;
    UChar_t el_genPFlav_resolved = 0;
    Float_t el_MiniIso_resolved = 0.;
    Float_t el_Iso03_resolved = 0.;
    Bool_t el_IsoL_resolved = 0;
    Bool_t el_Iso90_resolved = 0;
    Bool_t el_Iso80_resolved = 0;
    Bool_t el_noIsoL_resolved = 0;
    Bool_t el_noIso90_resolved = 0;
    Bool_t el_noIso80_resolved = 0;
    Float_t eljet_pt_resolved = 0.;
    UInt_t nElectron_resolved = 0;
    Int_t el_idx_resolved = 0;

    Float_t top_m_el_resolved = 0.;
    Float_t top_pt_el_resolved = 0.;
    Float_t top_eta_el_resolved = 0.;
    Float_t top_phi_el_resolved = 0.;
    Float_t top_E_el_resolved = 0.;
    Float_t lj_m_el_resolved = 0.;
    Float_t lj_pt_el_resolved = 0.;
    Float_t lj_eta_el_resolved = 0.;
    Float_t lj_phi_el_resolved = 0.;
    Float_t lj_E_el_resolved = 0.;
    Float_t top_mT_el_resolved = 0.;
    Float_t top_jetUnboost_m_el_resolved = 0.;
    Float_t top_jetUnboost_pt_el_resolved = 0.;
    Float_t top_jetUnboost_eta_el_resolved = 0.;
    Float_t top_jetUnboost_phi_el_resolved = 0.;
    Float_t top_jetUnboost_E_el_resolved = 0.;
    Int_t top_jet_hasPL_el_resolved = 0;
    Float_t top_lepUnboost_m_el_resolved = 0.;
    Float_t top_lepUnboost_pt_el_resolved = 0.;
    Float_t top_lepUnboost_eta_el_resolved = 0.;
    Float_t top_lepUnboost_phi_el_resolved = 0.;
    Float_t top_lepUnboost_E_el_resolved = 0.;
    Float_t top_relPt_el_resolved = 0.;
    Float_t top_costheta_el_resolved = 0.;
    Float_t top_dR_el_resolved = 0.;
    Int_t tau_high_truth_el_resolved = 0;
    Int_t top_category_el_resolved = 0;
    Int_t top_high_truth_el_resolved = 0;
    UInt_t nTop_el_resolved = 0;
    Int_t nEvent_el_resolved = 0;
    Int_t top_idx_el_resolved = 0;
    int sample_el_resolved = 0;

    Float_t met_el_merged = 0.;
    Float_t met_phi_el_merged = 0.;

    Float_t jet_m_el_merged = 0.;
    Float_t jet_pt_el_merged = 0.;
    Float_t jet_eta_el_merged = 0.;
    Float_t jet_phi_el_merged = 0.;
    Int_t jet_Id_el_merged = 0;
    Int_t jet_partFlav_el_merged = 0;
    Int_t jet_hadFlav_el_merged = 0;
    Float_t jet_isDeep_el_merged = 0.;
    UInt_t nJet_el_merged = 0;
    Int_t jet_idx_el_merged = 0;

    Float_t el_pt_merged = 0.;
    Float_t el_eta_merged = 0.;
    Float_t el_phi_merged = 0.;
    Int_t el_charge_merged = 0;
    Float_t el_Dxy_merged = 0.;
    Float_t el_DxyErr_merged = 0.;
    Float_t el_Dz_merged = 0.;
    Float_t el_DzErr_merged = 0.;
    Int_t el_cutBased_merged = 0;
    UChar_t el_genPFlav_merged = 0;
    Float_t el_MiniIso_merged = 0.;
    Float_t el_Iso03_merged = 0.;
    Bool_t el_IsoL_merged = 0;
    Bool_t el_Iso90_merged = 0;
    Bool_t el_Iso80_merged = 0;
    Bool_t el_noIsoL_merged = 0;
    Bool_t el_noIso90_merged = 0;
    Bool_t el_noIso80_merged = 0;
    Float_t eljet_pt_merged = 0.;
    UInt_t nElectron_merged = 0;
    Int_t el_idx_merged = 0;

    Float_t top_m_el_merged = 0.;
    Float_t top_pt_el_merged = 0.;
    Float_t top_eta_el_merged = 0.;
    Float_t top_phi_el_merged = 0.;
    Float_t top_E_el_merged = 0.;
    Float_t lj_m_el_merged = 0.;
    Float_t lj_pt_el_merged = 0.;
    Float_t lj_eta_el_merged = 0.;
    Float_t lj_phi_el_merged = 0.;
    Float_t lj_E_el_merged = 0.;
    Float_t top_mT_el_merged = 0.;
    Float_t top_jetUnboost_m_el_merged = 0.;
    Float_t top_jetUnboost_pt_el_merged = 0.;
    Float_t top_jetUnboost_eta_el_merged = 0.;
    Float_t top_jetUnboost_phi_el_merged = 0.;
    Float_t top_jetUnboost_E_el_merged = 0.;
    Int_t top_jet_hasPL_el_merged = 0;
    Float_t top_lepUnboost_m_el_merged = 0.;
    Float_t top_lepUnboost_pt_el_merged = 0.;
    Float_t top_lepUnboost_eta_el_merged = 0.;
    Float_t top_lepUnboost_phi_el_merged = 0.;
    Float_t top_lepUnboost_E_el_merged = 0.;
    Float_t top_relPt_el_merged = 0.;
    Float_t top_costheta_el_merged = 0.;
    Float_t top_dR_el_merged = 0.;
    Int_t tau_high_truth_el_merged = 0;
    Int_t top_category_el_merged = 0;
    Int_t top_high_truth_el_merged = 0;
    UInt_t nTop_el_merged = 0;
    Int_t nEvent_el_merged = 0;
    Int_t top_idx_el_merged = 0;
    int sample_el_merged = 0;


    Float_t met_mu_resolved = 0.;
    Float_t met_phi_mu_resolved = 0.;

    Float_t jet_m_mu_resolved = 0.;
    Float_t jet_pt_mu_resolved = 0.;
    Float_t jet_eta_mu_resolved = 0.;
    Float_t jet_phi_mu_resolved = 0.;
    Int_t jet_Id_mu_resolved = 0;
    Int_t jet_partFlav_mu_resolved = 0;
    Int_t jet_hadFlav_mu_resolved = 0;
    Float_t jet_isDeep_mu_resolved = 0.;
    UInt_t nJet_mu_resolved = 0;
    Int_t jet_idx_mu_resolved = 0;

    Float_t mu_pt_resolved = 0.;
    Float_t mu_eta_resolved = 0.;
    Float_t mu_phi_resolved = 0.;
    Int_t mu_charge_resolved = 0;
    Float_t mu_Dxy_resolved = 0.;
    Float_t mu_DxyErr_resolved = 0.;
    Float_t mu_Dz_resolved = 0.;
    Float_t mu_DzErr_resolved = 0.;
    Bool_t mu_isL_resolved = 0;
    Bool_t mu_isM_resolved = 0;
    Bool_t mu_isT_resolved = 0;
    Bool_t mu_isGlob_resolved = 0;
    Bool_t mu_isTrack_resolved = 0;
    Int_t mu_nStations_resolved = 0;
    Int_t mu_nTrackLayers_resolved = 0;
    UChar_t mu_HighPtId_resolved = 0;
    UChar_t mu_genPFlav_resolved = 0;
    Float_t mu_MiniIso_resolved = 0.;
    Float_t mu_Iso04_resolved = 0.;
    Float_t mujet_pt_resolved = 0.;
    UInt_t nMuon_resolved = 0;
    Int_t mu_idx_resolved = 0;

    Float_t top_m_mu_resolved = 0.;
    Float_t top_pt_mu_resolved = 0.;
    Float_t top_eta_mu_resolved = 0.;
    Float_t top_phi_mu_resolved = 0.;
    Float_t top_E_mu_resolved = 0.;
    Float_t lj_m_mu_resolved = 0.;
    Float_t lj_pt_mu_resolved = 0.;
    Float_t lj_eta_mu_resolved = 0.;
    Float_t lj_phi_mu_resolved = 0.;
    Float_t lj_E_mu_resolved = 0.;
    Float_t top_mT_mu_resolved = 0.;
    Float_t top_jetUnboost_m_mu_resolved = 0.;
    Float_t top_jetUnboost_pt_mu_resolved = 0.;
    Float_t top_jetUnboost_eta_mu_resolved = 0.;
    Float_t top_jetUnboost_phi_mu_resolved = 0.;
    Float_t top_jetUnboost_E_mu_resolved = 0.;
    Int_t top_jet_hasPL_mu_resolved = 0;
    Float_t top_lepUnboost_m_mu_resolved = 0.;
    Float_t top_lepUnboost_pt_mu_resolved = 0.;
    Float_t top_lepUnboost_eta_mu_resolved = 0.;
    Float_t top_lepUnboost_phi_mu_resolved = 0.;
    Float_t top_lepUnboost_E_mu_resolved = 0.;
    Float_t top_relPt_mu_resolved = 0.;
    Float_t top_costheta_mu_resolved = 0.;
    Float_t top_dR_mu_resolved = 0.;
    Int_t tau_high_truth_mu_resolved = 0;
    Int_t top_category_mu_resolved = 0;
    Int_t top_high_truth_mu_resolved = 0;
    UInt_t nTop_mu_resolved = 0;
    Int_t nEvent_mu_resolved = 0;
    Int_t top_idx_mu_resolved = 0;
    int sample_mu_resolved = 0;

    Float_t met_mu_merged = 0.;
    Float_t met_phi_mu_merged = 0.;

    Float_t jet_m_mu_merged = 0.;
    Float_t jet_pt_mu_merged = 0.;
    Float_t jet_eta_mu_merged = 0.;
    Float_t jet_phi_mu_merged = 0.;
    Int_t jet_Id_mu_merged = 0;
    Int_t jet_partFlav_mu_merged = 0;
    Int_t jet_hadFlav_mu_merged = 0;
    Float_t jet_isDeep_mu_merged = 0.;
    UInt_t nJet_mu_merged = 0;
    Int_t jet_idx_mu_merged = 0;

    Float_t mu_pt_merged = 0.;
    Float_t mu_eta_merged = 0.;
    Float_t mu_phi_merged = 0.;
    Int_t mu_charge_merged = 0;
    Float_t mu_Dxy_merged = 0.;
    Float_t mu_DxyErr_merged = 0.;
    Float_t mu_Dz_merged = 0.;
    Float_t mu_DzErr_merged = 0.;
    Bool_t mu_isL_merged = 0;
    Bool_t mu_isM_merged = 0;
    Bool_t mu_isT_merged = 0;
    Bool_t mu_isGlob_merged = 0;
    Bool_t mu_isTrack_merged = 0;
    Int_t mu_nStations_merged = 0;
    Int_t mu_nTrackLayers_merged = 0;
    UChar_t mu_HighPtId_merged = 0;
    UChar_t mu_genPFlav_merged = 0;
    Float_t mu_MiniIso_merged = 0.;
    Float_t mu_Iso04_merged = 0.;
    Float_t mujet_pt_merged = 0.;
    UInt_t nMuon_merged = 0;
    Int_t mu_idx_merged = 0;

    Float_t top_m_mu_merged = 0.;
    Float_t top_pt_mu_merged = 0.;
    Float_t top_eta_mu_merged = 0.;
    Float_t top_phi_mu_merged = 0.;
    Float_t top_E_mu_merged = 0.;
    Float_t lj_m_mu_merged = 0.;
    Float_t lj_pt_mu_merged = 0.;
    Float_t lj_eta_mu_merged = 0.;
    Float_t lj_phi_mu_merged = 0.;
    Float_t lj_E_mu_merged = 0.;
    Float_t top_mT_mu_merged = 0.;
    Float_t top_jetUnboost_m_mu_merged = 0.;
    Float_t top_jetUnboost_pt_mu_merged = 0.;
    Float_t top_jetUnboost_eta_mu_merged = 0.;
    Float_t top_jetUnboost_phi_mu_merged = 0.;
    Float_t top_jetUnboost_E_mu_merged = 0.;
    Int_t top_jet_hasPL_mu_merged = 0;
    Float_t top_lepUnboost_m_mu_merged = 0.;
    Float_t top_lepUnboost_pt_mu_merged = 0.;
    Float_t top_lepUnboost_eta_mu_merged = 0.;
    Float_t top_lepUnboost_phi_mu_merged = 0.;
    Float_t top_lepUnboost_E_mu_merged = 0.;
    Float_t top_relPt_mu_merged = 0.;
    Float_t top_costheta_mu_merged = 0.;
    Float_t top_dR_mu_merged = 0.;
    Int_t tau_high_truth_mu_merged = 0;
    Int_t top_category_mu_merged = 0;
    Int_t top_high_truth_mu_merged = 0;
    UInt_t nTop_mu_merged = 0;
    Int_t nEvent_mu_merged = 0;
    Int_t top_idx_mu_merged = 0;
    int sample_mu_merged = 0;


    TFile *f2 = new TFile((outFile).c_str(), "RECREATE");

/* Electron Resolved Tree */
    TTree *el_resolved = new TTree("el_resolved","el_resolved");

    el_resolved->Branch("MET",&met_el_resolved);
    el_resolved->Branch("MET_phi",&met_phi_el_resolved);

    el_resolved->Branch("Jet_Mass",&jet_m_el_resolved);
    el_resolved->Branch("Jet_Pt",&jet_pt_el_resolved);
    el_resolved->Branch("Jet_Eta",&jet_eta_el_resolved);
    el_resolved->Branch("Jet_Phi",&jet_phi_el_resolved);
    el_resolved->Branch("Jet_Id",&jet_Id_el_resolved);
    el_resolved->Branch("Jet_PartonFlavor",&jet_partFlav_el_resolved);
    el_resolved->Branch("Jet_HadronFlavor",&jet_hadFlav_el_resolved);
    el_resolved->Branch("Jet_DeepFlavB",&jet_isDeep_el_resolved);
    el_resolved->Branch("nJet",&nJet_el_resolved);
    el_resolved->Branch("Jet_index",&jet_idx_el_resolved);

    el_resolved->Branch("Electron_Pt",&el_pt_resolved);
    el_resolved->Branch("Electron_Eta",&el_eta_resolved);
    el_resolved->Branch("Electron_Phi",&el_phi_resolved);
    el_resolved->Branch("Electron_Charge",&el_charge_resolved);
    el_resolved->Branch("Electron_Dxy",&el_Dxy_resolved);
    el_resolved->Branch("Electron_DxyErr",&el_DxyErr_resolved);
    el_resolved->Branch("Electron_Dz",&el_Dz_resolved);
    el_resolved->Branch("Electron_DzErr",&el_DzErr_resolved);
    el_resolved->Branch("Electron_cutBased",&el_cutBased_resolved);
    el_resolved->Branch("Electron_genPartFlav",&el_genPFlav_resolved);
    el_resolved->Branch("Electron_MiniIso",&el_MiniIso_resolved);
    el_resolved->Branch("Electron_Iso03",&el_Iso03_resolved);
    el_resolved->Branch("Electron_mvaIsoL",&el_IsoL_resolved);
    el_resolved->Branch("Electron_mvaIso90",&el_Iso90_resolved);
    el_resolved->Branch("Electron_mvaIso80",&el_Iso80_resolved);
    el_resolved->Branch("Electron_mvanoIsoL",&el_noIsoL_resolved);
    el_resolved->Branch("Electron_mvanoIso90",&el_noIso90_resolved);
    el_resolved->Branch("Electron_mvanoIso80",&el_noIso80_resolved);
    el_resolved->Branch("Electron_Over_Jet_Pt",&eljet_pt_resolved);
    el_resolved->Branch("nElectron",&nElectron_resolved);
    el_resolved->Branch("Electron_index",&el_idx_resolved);

    el_resolved->Branch("Top_Mass",&top_m_el_resolved);
    el_resolved->Branch("Top_Pt",&top_pt_el_resolved);
    el_resolved->Branch("Top_Eta",&top_eta_el_resolved);
    el_resolved->Branch("Top_Phi",&top_phi_el_resolved);
    el_resolved->Branch("Top_E",&top_E_el_resolved);
    el_resolved->Branch("Top2_Mass",&lj_m_el_resolved);
    el_resolved->Branch("Top2_Pt",&lj_pt_el_resolved);
    el_resolved->Branch("Top2_Eta",&lj_eta_el_resolved);
    el_resolved->Branch("Top2_Phi",&lj_phi_el_resolved);
    el_resolved->Branch("Top2_E",&lj_E_el_resolved);
    el_resolved->Branch("Top_mT",&top_mT_el_resolved);
    el_resolved->Branch("Top_Jet_Unboosted_Mass",&top_jetUnboost_m_el_resolved);
    el_resolved->Branch("Top_Jet_Unboosted_Pt",&top_jetUnboost_pt_el_resolved);
    el_resolved->Branch("Top_Jet_Unboosted_Eta",&top_jetUnboost_eta_el_resolved);
    el_resolved->Branch("Top_Jet_Unboosted_Phi",&top_jetUnboost_phi_el_resolved);
    el_resolved->Branch("Top_Jet_Unboosted_E",&top_jetUnboost_E_el_resolved);
    el_resolved->Branch("Top_Jet_hasPromptLep",&top_jet_hasPL_el_resolved);
    el_resolved->Branch("Top_Lep_Unboosted_Mass",&top_lepUnboost_m_el_resolved);
    el_resolved->Branch("Top_Lep_Unboosted_Pt",&top_lepUnboost_pt_el_resolved);
    el_resolved->Branch("Top_Lep_Unboosted_Eta",&top_lepUnboost_eta_el_resolved);
    el_resolved->Branch("Top_Lep_Unboosted_Phi",&top_lepUnboost_phi_el_resolved);
    el_resolved->Branch("Top_Lep_Unboosted_E",&top_lepUnboost_E_el_resolved);
    el_resolved->Branch("Top_Relative_Pt",&top_relPt_el_resolved);
    el_resolved->Branch("Top_Costheta",&top_costheta_el_resolved);
    el_resolved->Branch("Top_dR",&top_dR_el_resolved);
    el_resolved->Branch("Tau_High_Truth",&tau_high_truth_el_resolved);
    el_resolved->Branch("Top_Category",&top_category_el_resolved);
    el_resolved->Branch("Top_High_Truth",&top_high_truth_el_resolved);
    el_resolved->Branch("nTop",&nTop_el_resolved);
    el_resolved->Branch("nEvent",&nEvent_el_resolved);
    el_resolved->Branch("Top_index",&top_idx_el_resolved);
    el_resolved->Branch("Sample",&sample_el_resolved);

/* Electron Merged Tree */
    TTree *el_merged = new TTree("el_merged","el_merged");

    el_merged->Branch("MET",&met_el_merged);
    el_merged->Branch("MET_phi",&met_phi_el_merged);

    el_merged->Branch("Jet_Mass",&jet_m_el_merged);
    el_merged->Branch("Jet_Pt",&jet_pt_el_merged);
    el_merged->Branch("Jet_Eta",&jet_eta_el_merged);
    el_merged->Branch("Jet_Phi",&jet_phi_el_merged);
    el_merged->Branch("Jet_Id",&jet_Id_el_merged);
    el_merged->Branch("Jet_PartonFlavor",&jet_partFlav_el_merged);
    el_merged->Branch("Jet_HadronFlavor",&jet_hadFlav_el_merged);
    el_merged->Branch("Jet_DeepFlavB",&jet_isDeep_el_merged);
    el_merged->Branch("nJet",&nJet_el_merged);
    el_merged->Branch("Jet_index",&jet_idx_el_merged);

    el_merged->Branch("Electron_Pt",&el_pt_merged);
    el_merged->Branch("Electron_Eta",&el_eta_merged);
    el_merged->Branch("Electron_Phi",&el_phi_merged);
    el_merged->Branch("Electron_Charge",&el_charge_merged);
    el_merged->Branch("Electron_Dxy",&el_Dxy_merged);
    el_merged->Branch("Electron_DxyErr",&el_DxyErr_merged);
    el_merged->Branch("Electron_Dz",&el_Dz_merged);
    el_merged->Branch("Electron_DzErr",&el_DzErr_merged);
    el_merged->Branch("Electron_cutBased",&el_cutBased_merged);
    el_merged->Branch("Electron_genPartFlav",&el_genPFlav_merged);
    el_merged->Branch("Electron_MiniIso",&el_MiniIso_merged);
    el_merged->Branch("Electron_Iso03",&el_Iso03_merged);
    el_merged->Branch("Electron_mvaIsoL",&el_IsoL_merged);
    el_merged->Branch("Electron_mvaIso90",&el_Iso90_merged);
    el_merged->Branch("Electron_mvaIso80",&el_Iso80_merged);
    el_merged->Branch("Electron_mvanoIsoL",&el_noIsoL_merged);
    el_merged->Branch("Electron_mvanoIso90",&el_noIso90_merged);
    el_merged->Branch("Electron_mvanoIso80",&el_noIso80_merged);
    el_merged->Branch("Electron_Over_Jet_Pt",&eljet_pt_merged);
    el_merged->Branch("nElectron",&nElectron_merged);
    el_merged->Branch("Electron_index",&el_idx_merged);

    el_merged->Branch("Top_Mass",&top_m_el_merged);
    el_merged->Branch("Top_Pt",&top_pt_el_merged);
    el_merged->Branch("Top_Eta",&top_eta_el_merged);
    el_merged->Branch("Top_Phi",&top_phi_el_merged);
    el_merged->Branch("Top_E",&top_E_el_merged);
    el_merged->Branch("Top2_Mass",&lj_m_el_merged);
    el_merged->Branch("Top2_Pt",&lj_pt_el_merged);
    el_merged->Branch("Top2_Eta",&lj_eta_el_merged);
    el_merged->Branch("Top2_Phi",&lj_phi_el_merged);
    el_merged->Branch("Top2_E",&lj_E_el_merged);
    el_merged->Branch("Top_mT",&top_mT_el_merged);
    el_merged->Branch("Top_Jet_Unboosted_Mass",&top_jetUnboost_m_el_merged);
    el_merged->Branch("Top_Jet_Unboosted_Pt",&top_jetUnboost_pt_el_merged);
    el_merged->Branch("Top_Jet_Unboosted_Eta",&top_jetUnboost_eta_el_merged);
    el_merged->Branch("Top_Jet_Unboosted_Phi",&top_jetUnboost_phi_el_merged);
    el_merged->Branch("Top_Jet_Unboosted_E",&top_jetUnboost_E_el_merged);
    el_merged->Branch("Top_Jet_hasPromptLep",&top_jet_hasPL_el_merged);
    el_merged->Branch("Top_Lep_Unboosted_Mass",&top_lepUnboost_m_el_merged);
    el_merged->Branch("Top_Lep_Unboosted_Pt",&top_lepUnboost_pt_el_merged);
    el_merged->Branch("Top_Lep_Unboosted_Eta",&top_lepUnboost_eta_el_merged);
    el_merged->Branch("Top_Lep_Unboosted_Phi",&top_lepUnboost_phi_el_merged);
    el_merged->Branch("Top_Lep_Unboosted_E",&top_lepUnboost_E_el_merged);
    el_merged->Branch("Top_Relative_Pt",&top_relPt_el_merged);
    el_merged->Branch("Top_Costheta",&top_costheta_el_merged);
    el_merged->Branch("Top_dR",&top_dR_el_merged);
    el_merged->Branch("Tau_High_Truth",&tau_high_truth_el_merged);
    el_merged->Branch("Top_Category",&top_category_el_merged);
    el_merged->Branch("Top_High_Truth",&top_high_truth_el_merged);
    el_merged->Branch("nTop",&nTop_el_merged);
    el_merged->Branch("nEvent",&nEvent_el_merged);
    el_merged->Branch("Top_index",&top_idx_el_merged);
    el_merged->Branch("Sample",&sample_el_merged);

/* Muon Resolved Tree */
    TTree *mu_resolved = new TTree("mu_resolved","mu_resolved");

    mu_resolved->Branch("MET",&met_mu_resolved);
    mu_resolved->Branch("MET_phi",&met_phi_mu_resolved);

    mu_resolved->Branch("Jet_Mass",&jet_m_mu_resolved);
    mu_resolved->Branch("Jet_Pt",&jet_pt_mu_resolved);
    mu_resolved->Branch("Jet_Eta",&jet_eta_mu_resolved);
    mu_resolved->Branch("Jet_Phi",&jet_phi_mu_resolved);
    mu_resolved->Branch("Jet_Id",&jet_Id_mu_resolved);
    mu_resolved->Branch("Jet_PartonFlavor",&jet_partFlav_mu_resolved);
    mu_resolved->Branch("Jet_HadronFlavor",&jet_hadFlav_mu_resolved);
    mu_resolved->Branch("Jet_DeepFlavB",&jet_isDeep_mu_resolved);
    mu_resolved->Branch("nJet",&nJet_mu_resolved);
    mu_resolved->Branch("Jet_index",&jet_idx_mu_resolved);

    mu_resolved->Branch("Muon_Pt",&mu_pt_resolved);
    mu_resolved->Branch("Muon_Eta",&mu_eta_resolved);
    mu_resolved->Branch("Muon_Phi",&mu_phi_resolved);
    mu_resolved->Branch("Muon_Charge",&mu_charge_resolved);
    mu_resolved->Branch("Muon_Dxy",&mu_Dxy_resolved);
    mu_resolved->Branch("Muon_DxyErr",&mu_DxyErr_resolved);
    mu_resolved->Branch("Muon_Dz",&mu_Dz_resolved);
    mu_resolved->Branch("Muon_DzErr",&mu_DzErr_resolved);
    mu_resolved->Branch("Muon_isLoose",&mu_isL_resolved);
    mu_resolved->Branch("Muon_isMedium",&mu_isM_resolved);
    mu_resolved->Branch("Muon_isTight",&mu_isT_resolved);
    mu_resolved->Branch("Muon_isGlobal",&mu_isGlob_resolved);
    mu_resolved->Branch("Muon_isTracker",&mu_isTrack_resolved);
    mu_resolved->Branch("Muon_nStations",&mu_nStations_resolved);
    mu_resolved->Branch("Muon_nTrackerLayers",&mu_nTrackLayers_resolved);
    mu_resolved->Branch("Muon_HighPtId",&mu_HighPtId_resolved);
    mu_resolved->Branch("Muon_genPartFlav",&mu_genPFlav_resolved);
    mu_resolved->Branch("Muon_MiniIso",&mu_MiniIso_resolved);
    mu_resolved->Branch("Muon_Iso04",&mu_Iso04_resolved);
    mu_resolved->Branch("Muon_Over_Jet_Pt",&mujet_pt_resolved);
    mu_resolved->Branch("nMuon",&nMuon_resolved);
    mu_resolved->Branch("Muon_index",&mu_idx_resolved);

    mu_resolved->Branch("Top_Mass",&top_m_mu_resolved);
    mu_resolved->Branch("Top_Pt",&top_pt_mu_resolved);
    mu_resolved->Branch("Top_Eta",&top_eta_mu_resolved);
    mu_resolved->Branch("Top_Phi",&top_phi_mu_resolved);
    mu_resolved->Branch("Top_E",&top_E_mu_resolved);
    mu_resolved->Branch("Top2_Mass",&lj_m_mu_resolved);
    mu_resolved->Branch("Top2_Pt",&lj_pt_mu_resolved);
    mu_resolved->Branch("Top2_Eta",&lj_eta_mu_resolved);
    mu_resolved->Branch("Top2_Phi",&lj_phi_mu_resolved);
    mu_resolved->Branch("Top2_E",&lj_E_mu_resolved);
    mu_resolved->Branch("Top_mT",&top_mT_mu_resolved);
    mu_resolved->Branch("Top_Jet_Unboosted_Mass",&top_jetUnboost_m_mu_resolved);
    mu_resolved->Branch("Top_Jet_Unboosted_Pt",&top_jetUnboost_pt_mu_resolved);
    mu_resolved->Branch("Top_Jet_Unboosted_Eta",&top_jetUnboost_eta_mu_resolved);
    mu_resolved->Branch("Top_Jet_Unboosted_Phi",&top_jetUnboost_phi_mu_resolved);
    mu_resolved->Branch("Top_Jet_Unboosted_E",&top_jetUnboost_E_mu_resolved);
    mu_resolved->Branch("Top_Jet_hasPromptLep",&top_jet_hasPL_mu_resolved);
    mu_resolved->Branch("Top_Lep_Unboosted_Mass",&top_lepUnboost_m_mu_resolved);
    mu_resolved->Branch("Top_Lep_Unboosted_Pt",&top_lepUnboost_pt_mu_resolved);
    mu_resolved->Branch("Top_Lep_Unboosted_Eta",&top_lepUnboost_eta_mu_resolved);
    mu_resolved->Branch("Top_Lep_Unboosted_Phi",&top_lepUnboost_phi_mu_resolved);
    mu_resolved->Branch("Top_Lep_Unboosted_E",&top_lepUnboost_E_mu_resolved);
    mu_resolved->Branch("Top_Relative_Pt",&top_relPt_mu_resolved);
    mu_resolved->Branch("Top_Costheta",&top_costheta_mu_resolved);
    mu_resolved->Branch("Top_dR",&top_dR_mu_resolved);
    mu_resolved->Branch("Tau_High_Truth",&tau_high_truth_mu_resolved);
    mu_resolved->Branch("Top_Category",&top_category_mu_resolved);
    mu_resolved->Branch("Top_High_Truth",&top_high_truth_mu_resolved);
    mu_resolved->Branch("nTop",&nTop_mu_resolved);
    mu_resolved->Branch("nEvent",&nEvent_mu_resolved);
    mu_resolved->Branch("Top_index",&top_idx_mu_resolved);
    mu_resolved->Branch("Sample",&sample_mu_resolved);

/* Muon Merged Tree */
    TTree *mu_merged = new TTree("mu_merged","mu_merged");

    mu_merged->Branch("MET",&met_mu_merged);
    mu_merged->Branch("MET_phi",&met_phi_mu_merged);

    mu_merged->Branch("Jet_Mass",&jet_m_mu_merged);
    mu_merged->Branch("Jet_Pt",&jet_pt_mu_merged);
    mu_merged->Branch("Jet_Eta",&jet_eta_mu_merged);
    mu_merged->Branch("Jet_Phi",&jet_phi_mu_merged);
    mu_merged->Branch("Jet_Id",&jet_Id_mu_merged);
    mu_merged->Branch("Jet_PartonFlavor",&jet_partFlav_mu_merged);
    mu_merged->Branch("Jet_HadronFlavor",&jet_hadFlav_mu_merged);
    mu_merged->Branch("Jet_DeepFlavB",&jet_isDeep_mu_merged);
    mu_merged->Branch("nJet",&nJet_mu_merged);
    mu_merged->Branch("Jet_index",&jet_idx_mu_merged);

    mu_merged->Branch("Muon_Pt",&mu_pt_merged);
    mu_merged->Branch("Muon_Eta",&mu_eta_merged);
    mu_merged->Branch("Muon_Phi",&mu_phi_merged);
    mu_merged->Branch("Muon_Charge",&mu_charge_merged);
    mu_merged->Branch("Muon_Dxy",&mu_Dxy_merged);
    mu_merged->Branch("Muon_DxyErr",&mu_DxyErr_merged);
    mu_merged->Branch("Muon_Dz",&mu_Dz_merged);
    mu_merged->Branch("Muon_DzErr",&mu_DzErr_merged);
    mu_merged->Branch("Muon_isLoose",&mu_isL_merged);
    mu_merged->Branch("Muon_isMedium",&mu_isM_merged);
    mu_merged->Branch("Muon_isTight",&mu_isT_merged);
    mu_merged->Branch("Muon_isGlobal",&mu_isGlob_merged);
    mu_merged->Branch("Muon_isTracker",&mu_isTrack_merged);
    mu_merged->Branch("Muon_nStations",&mu_nStations_merged);
    mu_merged->Branch("Muon_nTrackerLayers",&mu_nTrackLayers_merged);
    mu_merged->Branch("Muon_HighPtId",&mu_HighPtId_merged);
    mu_merged->Branch("Muon_genPartFlav",&mu_genPFlav_merged);
    mu_merged->Branch("Muon_MiniIso",&mu_MiniIso_merged);
    mu_merged->Branch("Muon_Iso04",&mu_Iso04_merged);
    mu_merged->Branch("Muon_Over_Jet_Pt",&mujet_pt_merged);
    mu_merged->Branch("nMuon",&nMuon_merged);
    mu_merged->Branch("Muon_index",&mu_idx_merged);

    mu_merged->Branch("Top_Mass",&top_m_mu_merged);
    mu_merged->Branch("Top_Pt",&top_pt_mu_merged);
    mu_merged->Branch("Top_Eta",&top_eta_mu_merged);
    mu_merged->Branch("Top_Phi",&top_phi_mu_merged);
    mu_merged->Branch("Top_E",&top_E_mu_merged);
    mu_merged->Branch("Top2_Mass",&lj_m_mu_merged);
    mu_merged->Branch("Top2_Pt",&lj_pt_mu_merged);
    mu_merged->Branch("Top2_Eta",&lj_eta_mu_merged);
    mu_merged->Branch("Top2_Phi",&lj_phi_mu_merged);
    mu_merged->Branch("Top2_E",&lj_E_mu_merged);
    mu_merged->Branch("Top_mT",&top_mT_mu_merged);
    mu_merged->Branch("Top_Jet_Unboosted_Mass",&top_jetUnboost_m_mu_merged);
    mu_merged->Branch("Top_Jet_Unboosted_Pt",&top_jetUnboost_pt_mu_merged);
    mu_merged->Branch("Top_Jet_Unboosted_Eta",&top_jetUnboost_eta_mu_merged);
    mu_merged->Branch("Top_Jet_Unboosted_Phi",&top_jetUnboost_phi_mu_merged);
    mu_merged->Branch("Top_Jet_Unboosted_E",&top_jetUnboost_E_mu_merged);
    mu_merged->Branch("Top_Jet_hasPromptLep",&top_jet_hasPL_mu_merged);
    mu_merged->Branch("Top_Lep_Unboosted_Mass",&top_lepUnboost_m_mu_merged);
    mu_merged->Branch("Top_Lep_Unboosted_Pt",&top_lepUnboost_pt_mu_merged);
    mu_merged->Branch("Top_Lep_Unboosted_Eta",&top_lepUnboost_eta_mu_merged);
    mu_merged->Branch("Top_Lep_Unboosted_Phi",&top_lepUnboost_phi_mu_merged);
    mu_merged->Branch("Top_Lep_Unboosted_E",&top_lepUnboost_E_mu_merged);
    mu_merged->Branch("Top_Relative_Pt",&top_relPt_mu_merged);
    mu_merged->Branch("Top_Costheta",&top_costheta_mu_merged);
    mu_merged->Branch("Top_dR",&top_dR_mu_merged);
    mu_merged->Branch("Tau_High_Truth",&tau_high_truth_mu_merged);
    mu_merged->Branch("Top_Category",&top_category_mu_merged);
    mu_merged->Branch("Top_High_Truth",&top_high_truth_mu_merged);
    mu_merged->Branch("nTop",&nTop_mu_merged);
    mu_merged->Branch("nEvent",&nEvent_mu_merged);
    mu_merged->Branch("Top_index",&top_idx_mu_merged);
    mu_merged->Branch("Sample",&sample_mu_merged);


/* ---------- Looping over the Entries ----------- */

    for (int i = 0; i < chain.GetEntries(); i++)
    {
        chain.GetEntry(i);

	if(i>0 && i%10000==0) {
	  cout << "Processed: " << i << "/" << chain.GetEntries() << " entries" << endl;
	}
	
	met_el_resolved = 0.;                 met_el_merged = 0.;
	met_phi_el_resolved = 0.;             met_phi_el_merged = 0.;
	jet_m_el_resolved = 0.;               jet_m_el_merged = 0.;
	jet_pt_el_resolved = 0.;              jet_pt_el_merged = 0.;
	jet_eta_el_resolved = 0.;             jet_eta_el_merged = 0.;
	jet_phi_el_resolved = 0.;             jet_phi_el_merged = 0.;
	jet_Id_el_resolved = 0;               jet_Id_el_merged = 0;
	jet_partFlav_el_resolved = 0;         jet_partFlav_el_merged = 0;
	jet_hadFlav_el_resolved = 0;          jet_hadFlav_el_merged = 0;
	jet_isDeep_el_resolved = 0.;          jet_isDeep_el_merged = 0.;
	nJet_el_resolved = 0;                 nJet_el_merged = 0;
	jet_idx_el_resolved = 0;              jet_idx_el_merged = 0;
	el_pt_resolved = 0.;                  el_pt_merged = 0.;
	el_phi_resolved = 0.;                 el_phi_merged = 0.;
	el_eta_resolved = 0.;                 el_eta_merged = 0.;
	el_charge_resolved = 0;               el_charge_merged = 0;
	el_Dxy_resolved = 0.;                 el_Dxy_merged = 0.;
	el_DxyErr_resolved = 0.;              el_DxyErr_merged = 0.;
	el_Dz_resolved = 0.;                  el_Dz_merged = 0.;
	el_DzErr_resolved = 0.;               el_DzErr_merged = 0.;
	el_cutBased_resolved = 0;             el_cutBased_merged = 0;
	el_genPFlav_resolved = 0;             el_genPFlav_merged = 0;
	el_MiniIso_resolved = 0.;             el_MiniIso_merged = 0.;
	el_Iso03_resolved = 0.;               el_Iso03_merged = 0.;
	el_IsoL_resolved = 0;                 el_IsoL_merged = 0;
	el_Iso90_resolved = 0;                el_Iso90_merged = 0;
	el_Iso80_resolved = 0;                el_Iso80_merged = 0;
	el_noIsoL_resolved = 0;               el_noIsoL_merged = 0;
	el_noIso90_resolved = 0;              el_noIso90_merged = 0;
	el_noIso80_resolved = 0;              el_noIso80_merged = 0;
	eljet_pt_resolved = 0.;               eljet_pt_merged = 0.;
	nElectron_resolved = 0;               nElectron_merged = 0;
	el_idx_resolved = 0;                  el_idx_merged = 0;
	top_m_el_resolved = 0.;               top_m_el_merged = 0.;
	top_pt_el_resolved = 0.;              top_pt_el_merged = 0.;
	top_eta_el_resolved = 0.;             top_eta_el_merged = 0.;
	top_phi_el_resolved = 0.;             top_phi_el_merged = 0.;
	top_E_el_resolved = 0.;               top_E_el_merged = 0.;
	lj_m_el_resolved = 0.;                lj_m_el_merged = 0.;
	lj_pt_el_resolved = 0.;               lj_pt_el_merged = 0.;
	lj_eta_el_resolved = 0.;              lj_eta_el_merged = 0.;
	lj_phi_el_resolved = 0.;              lj_phi_el_merged = 0.;
	lj_E_el_resolved = 0.;                lj_E_el_merged = 0.;
	top_mT_el_resolved = 0.;              top_mT_el_merged = 0.;
	top_jetUnboost_m_el_resolved = 0.;    top_jetUnboost_m_el_merged = 0.;
	top_jetUnboost_pt_el_resolved = 0.;   top_jetUnboost_pt_el_merged = 0.;
	top_jetUnboost_eta_el_resolved = 0.;  top_jetUnboost_eta_el_merged = 0.;
	top_jetUnboost_phi_el_resolved = 0.;  top_jetUnboost_phi_el_merged = 0.;
	top_jetUnboost_E_el_resolved = 0.;    top_jetUnboost_E_el_merged = 0.;
	top_jet_hasPL_el_resolved = 0;        top_jet_hasPL_el_merged = 0;
	top_lepUnboost_m_el_resolved = 0.;    top_lepUnboost_m_el_merged = 0.;
	top_lepUnboost_pt_el_resolved = 0.;   top_lepUnboost_pt_el_merged = 0.;
	top_lepUnboost_eta_el_resolved = 0.;  top_lepUnboost_eta_el_merged = 0.;
	top_lepUnboost_phi_el_resolved = 0.;  top_lepUnboost_phi_el_merged = 0.;
	top_lepUnboost_E_el_resolved = 0.;    top_lepUnboost_E_el_merged = 0.;
	top_relPt_el_resolved = 0.;           top_relPt_el_merged = 0.;
	top_costheta_el_resolved = 0.;        top_costheta_el_merged = 0.;
	top_dR_el_resolved = 0.;              top_dR_el_merged = 0.;
	tau_high_truth_el_resolved = 0;       tau_high_truth_el_merged = 0;
	top_category_el_resolved = 0;         top_category_el_merged = 0;
	top_high_truth_el_resolved = 0;       top_high_truth_el_merged = 0;
	nTop_el_resolved = 0;                 nTop_el_merged = 0;
	nEvent_el_resolved = 0;               nEvent_el_merged = 0;
	top_idx_el_resolved = 0;              top_idx_el_merged = 0;
	sample_el_resolved = 0;               sample_el_merged = 0;

	met_mu_resolved = 0.;                 met_mu_merged = 0.;
	met_phi_mu_resolved = 0.;             met_phi_mu_merged = 0.;
	jet_m_mu_resolved = 0.;               jet_m_mu_merged = 0.;
	jet_pt_mu_resolved = 0.;              jet_pt_mu_merged = 0.;
	jet_eta_mu_resolved = 0.;             jet_eta_mu_merged = 0.;
	jet_phi_mu_resolved = 0.;             jet_phi_mu_merged = 0.;
	jet_Id_mu_resolved = 0;               jet_Id_mu_merged = 0;
	jet_partFlav_mu_resolved = 0;         jet_partFlav_mu_merged = 0;
	jet_hadFlav_mu_resolved = 0;          jet_hadFlav_mu_merged = 0;
	jet_isDeep_mu_resolved = 0.;          jet_isDeep_mu_merged = 0.;
	nJet_mu_resolved = 0;                 nJet_mu_merged = 0;
	jet_idx_mu_resolved = 0;              jet_idx_mu_merged = 0;
	mu_pt_resolved = 0.;                  mu_pt_merged = 0.;
	mu_phi_resolved = 0.;                 mu_phi_merged = 0.;
	mu_eta_resolved = 0.;                 mu_eta_merged = 0.;
	mu_charge_resolved = 0;               mu_charge_merged = 0;
	mu_Dxy_resolved = 0.;                 mu_Dxy_merged = 0.;
	mu_DxyErr_resolved = 0.;              mu_DxyErr_merged = 0.;
	mu_Dz_resolved = 0.;                  mu_Dz_merged = 0.;
	mu_DzErr_resolved = 0.;               mu_DzErr_merged = 0.;
	mu_isL_resolved = 0;                  mu_isL_merged = 0;
	mu_isM_resolved = 0;                  mu_isM_merged = 0;
	mu_isT_resolved = 0;                  mu_isT_merged = 0;
	mu_isGlob_resolved = 0;               mu_isGlob_merged = 0;
	mu_isTrack_resolved = 0;              mu_isTrack_merged = 0;
	mu_nStations_resolved = 0;            mu_nStations_merged = 0;
	mu_nTrackLayers_resolved = 0;         mu_nTrackLayers_merged = 0;
	mu_HighPtId_resolved = 0;             mu_HighPtId_merged = 0;
	mu_genPFlav_resolved = 0;             mu_genPFlav_merged = 0;
	mu_MiniIso_resolved = 0.;             mu_MiniIso_merged = 0.;
	mu_Iso04_resolved = 0.;               mu_Iso04_merged = 0.;
	mujet_pt_resolved = 0.;               mujet_pt_merged = 0.;
	nMuon_resolved = 0;                   nMuon_merged = 0;
	mu_idx_resolved = 0;                  mu_idx_merged = 0;
	top_m_mu_resolved = 0.;               top_m_mu_merged = 0.;
	top_pt_mu_resolved = 0.;              top_pt_mu_merged = 0.;
	top_eta_mu_resolved = 0.;             top_eta_mu_merged = 0.;
	top_phi_mu_resolved = 0.;             top_phi_mu_merged = 0.;
	top_E_mu_resolved = 0.;               top_E_mu_merged = 0.;
	lj_m_mu_resolved = 0.;                lj_m_mu_merged = 0.;
	lj_pt_mu_resolved = 0.;               lj_pt_mu_merged = 0.;
	lj_eta_mu_resolved = 0.;              lj_eta_mu_merged = 0.;
	lj_phi_mu_resolved = 0.;              lj_phi_mu_merged = 0.;
	lj_E_mu_resolved = 0.;                lj_E_mu_merged = 0.;
	top_mT_mu_resolved = 0.;              top_mT_mu_merged = 0.;
	top_jetUnboost_m_mu_resolved = 0.;    top_jetUnboost_m_mu_merged = 0.;
	top_jetUnboost_pt_mu_resolved = 0.;   top_jetUnboost_pt_mu_merged = 0.;
	top_jetUnboost_eta_mu_resolved = 0.;  top_jetUnboost_eta_mu_merged = 0.;
	top_jetUnboost_phi_mu_resolved = 0.;  top_jetUnboost_phi_mu_merged = 0.;
	top_jetUnboost_E_mu_resolved = 0.;    top_jetUnboost_E_mu_merged = 0.;
	top_jet_hasPL_mu_resolved = 0;        top_jet_hasPL_mu_merged = 0;
	top_lepUnboost_m_mu_resolved = 0.;    top_lepUnboost_m_mu_merged = 0.;
	top_lepUnboost_pt_mu_resolved = 0.;   top_lepUnboost_pt_mu_merged = 0.;
	top_lepUnboost_eta_mu_resolved = 0.;  top_lepUnboost_eta_mu_merged = 0.;
	top_lepUnboost_phi_mu_resolved = 0.;  top_lepUnboost_phi_mu_merged = 0.;
	top_lepUnboost_E_mu_resolved = 0.;    top_lepUnboost_E_mu_merged = 0.;
	top_relPt_mu_resolved = 0.;           top_relPt_mu_merged = 0.;
	top_costheta_mu_resolved = 0.;        top_costheta_mu_merged = 0.;
	top_dR_mu_resolved = 0.;              top_dR_mu_merged = 0.;
	tau_high_truth_mu_resolved = 0;       tau_high_truth_mu_merged = 0;
	top_category_mu_resolved = 0;         top_category_mu_merged = 0;
	top_high_truth_mu_resolved = 0;       top_high_truth_mu_merged = 0;
	nTop_mu_resolved = 0;                 nTop_mu_merged = 0;
	nEvent_mu_resolved = 0;               nEvent_mu_merged = 0;
	top_idx_mu_resolved = 0;              top_idx_mu_merged = 0;
	sample_mu_resolved = 0;               sample_mu_merged = 0;
	  
	for(int k=0; k<(int)nTop; k++){ 

	    if(el_idx[k]!=-1 && Top_isMerged[k]==0){
	      
	        met_el_resolved = MET;
	        met_phi_el_resolved = MET_phi;

	        jet_m_el_resolved = Jet_mass[jet_idx[k]];
	        jet_pt_el_resolved = Jet_pt[jet_idx[k]];
		jet_eta_el_resolved = Jet_eta[jet_idx[k]];
		jet_phi_el_resolved = Jet_phi[jet_idx[k]];
		jet_Id_el_resolved = Jet_Id[jet_idx[k]];
		jet_partFlav_el_resolved = Jet_partonFlavour[jet_idx[k]];
		jet_hadFlav_el_resolved = Jet_hadronFlavour[jet_idx[k]];
		jet_isDeep_el_resolved = Jet_isDeep[jet_idx[k]];
		nJet_el_resolved = Jet_size;
		jet_idx_el_resolved = jet_idx[k];

		el_pt_resolved = El_pt[el_idx[k]];
		el_phi_resolved = El_phi[el_idx[k]];
		el_eta_resolved = El_eta[el_idx[k]];
		el_charge_resolved = El_charge[el_idx[k]];
		el_Dxy_resolved = El_Dxy[el_idx[k]];
		el_DxyErr_resolved = El_Dxyerr[el_idx[k]];
		el_Dz_resolved = El_Dz[el_idx[k]];
		el_DzErr_resolved = El_Dzerr[el_idx[k]];
		el_cutBased_resolved = El_cutBased[el_idx[k]];
		el_genPFlav_resolved = El_genPFlav[el_idx[k]];
		el_MiniIso_resolved = El_MiniIso[el_idx[k]];
		el_Iso03_resolved = El_Iso03[el_idx[k]];
		el_IsoL_resolved = El_IsoL[el_idx[k]];
		el_Iso90_resolved = El_Iso90[el_idx[k]];
		el_Iso80_resolved = El_Iso80[el_idx[k]];
		el_noIsoL_resolved = El_noIsoL[el_idx[k]];
		el_noIso90_resolved = El_noIso90[el_idx[k]];
		el_noIso80_resolved = El_noIso80[el_idx[k]];
		eljet_pt_resolved = El_pt[el_idx[k]]/Jet_pt[jet_idx[k]];
		nElectron_resolved = El_size;
		el_idx_resolved = el_idx[k];

		top_m_el_resolved = Top_mass[k];
		top_pt_el_resolved = Top_pt[k];
		top_eta_el_resolved = Top_eta[k];
		top_phi_el_resolved = Top_phi[k];
		top_E_el_resolved = Top_E[k];
		lj_m_el_resolved = lj_mass[k];
		lj_pt_el_resolved = lj_pt[k];
		lj_eta_el_resolved = lj_eta[k];
		lj_phi_el_resolved = lj_phi[k];
		lj_E_el_resolved = lj_E[k];
		top_mT_el_resolved = sqrt(2*lj_pt[k]*MET*(1-cos(deltaPhi(MET_phi,lj_phi[k]))));
		top_jetUnboost_m_el_resolved = Top_jet_unboosted_mass[k];
		top_jetUnboost_pt_el_resolved = Top_jet_unboosted_pt[k];
		top_jetUnboost_eta_el_resolved = Top_jet_unboosted_eta[k];
		top_jetUnboost_phi_el_resolved = Top_jet_unboosted_phi[k];
		top_jetUnboost_E_el_resolved = Top_jet_unboosted_E[k];
		top_jet_hasPL_el_resolved = Top_jet_hasPromptLep[k];
		top_lepUnboost_m_el_resolved = Top_lep_unboosted_mass[k];
		top_lepUnboost_pt_el_resolved = Top_lep_unboosted_pt[k];
		top_lepUnboost_eta_el_resolved = Top_lep_unboosted_eta[k];
		top_lepUnboost_phi_el_resolved = Top_lep_unboosted_phi[k];
		top_lepUnboost_E_el_resolved = Top_lep_unboosted_E[k];
		top_relPt_el_resolved = Top_relPt[k];
		top_costheta_el_resolved = Top_cosTheta[k];
		top_dR_el_resolved = Top_dR[k];
		tau_high_truth_el_resolved = Top_Tau_High_Truth[k];
		top_category_el_resolved = Top_Category[k];
		if(Top_Category[k]==0) Top_High_Truth=1;
		else Top_High_Truth=0;
		top_high_truth_el_resolved = Top_High_Truth;
		nTop_el_resolved = nTop;
		nEvent_el_resolved = i;
		top_idx_el_resolved = k;
		for(N=0;N<nFiles;N++){
		  stringstream ss;
		  if(i<nEntries[N]){
		    ss << filename[N].substr(79,4);
		    ss >> sample_el_resolved;
		    break;
		  }
		}
		
		el_resolved->Fill();

	    }  // Electron Resolved Category

	    if(el_idx[k]!=-1 && Top_isMerged[k]==1){
	      
	        met_el_merged = MET;
	        met_phi_el_merged = MET_phi;

	        jet_m_el_merged = Jet_mass[jet_idx[k]];
	        jet_pt_el_merged = Jet_pt[jet_idx[k]];
		jet_eta_el_merged = Jet_eta[jet_idx[k]];
		jet_phi_el_merged = Jet_phi[jet_idx[k]];
		jet_Id_el_merged = Jet_Id[jet_idx[k]];
		jet_partFlav_el_merged = Jet_partonFlavour[jet_idx[k]];
		jet_hadFlav_el_merged = Jet_hadronFlavour[jet_idx[k]];
		jet_isDeep_el_merged = Jet_isDeep[jet_idx[k]];
		nJet_el_merged = Jet_size;
		jet_idx_el_merged = jet_idx[k];

		el_pt_merged = El_pt[el_idx[k]];
		el_phi_merged = El_phi[el_idx[k]];
		el_eta_merged = El_eta[el_idx[k]];
		el_charge_merged = El_charge[el_idx[k]];
		el_Dxy_merged = El_Dxy[el_idx[k]];
		el_DxyErr_merged = El_Dxyerr[el_idx[k]];
		el_Dz_merged = El_Dz[el_idx[k]];
		el_DzErr_merged = El_Dzerr[el_idx[k]];
		el_cutBased_merged = El_cutBased[el_idx[k]];
		el_genPFlav_merged = El_genPFlav[el_idx[k]];
		el_MiniIso_merged = El_MiniIso[el_idx[k]];
		el_Iso03_merged = El_Iso03[el_idx[k]];
		el_IsoL_merged = El_IsoL[el_idx[k]];
		el_Iso90_merged = El_Iso90[el_idx[k]];
		el_Iso80_merged = El_Iso80[el_idx[k]];
		el_noIsoL_merged = El_noIsoL[el_idx[k]];
		el_noIso90_merged = El_noIso90[el_idx[k]];
		el_noIso80_merged = El_noIso80[el_idx[k]];
		eljet_pt_merged = El_pt[el_idx[k]]/Jet_pt[jet_idx[k]];
		nElectron_merged = El_size;
		el_idx_merged = el_idx[k];

		top_m_el_merged = Top_mass[k];
		top_pt_el_merged = Top_pt[k];
		top_eta_el_merged = Top_eta[k];
		top_phi_el_merged = Top_phi[k];
		top_E_el_merged = Top_E[k];
		lj_m_el_merged = lj_mass[k];
		lj_pt_el_merged = lj_pt[k];
		lj_eta_el_merged = lj_eta[k];
		lj_phi_el_merged = lj_phi[k];
		lj_E_el_merged = lj_E[k];
		top_mT_el_merged = sqrt(2*lj_pt[k]*MET*(1-cos(deltaPhi(MET_phi,lj_phi[k]))));
		top_jetUnboost_m_el_merged = Top_jet_unboosted_mass[k];
		top_jetUnboost_pt_el_merged = Top_jet_unboosted_pt[k];
		top_jetUnboost_eta_el_merged = Top_jet_unboosted_eta[k];
		top_jetUnboost_phi_el_merged = Top_jet_unboosted_phi[k];
		top_jetUnboost_E_el_merged = Top_jet_unboosted_E[k];
		top_jet_hasPL_el_merged = Top_jet_hasPromptLep[k];
		top_lepUnboost_m_el_merged = Top_lep_unboosted_mass[k];
		top_lepUnboost_pt_el_merged = Top_lep_unboosted_pt[k];
		top_lepUnboost_eta_el_merged = Top_lep_unboosted_eta[k];
		top_lepUnboost_phi_el_merged = Top_lep_unboosted_phi[k];
		top_lepUnboost_E_el_merged = Top_lep_unboosted_E[k];
		top_relPt_el_merged = Top_relPt[k];
		top_costheta_el_merged = Top_cosTheta[k];
		top_dR_el_merged = Top_dR[k];
		tau_high_truth_el_merged = Top_Tau_High_Truth[k];
		top_category_el_merged = Top_Category[k];
		if(Top_Category[k]==0) Top_High_Truth=1;
		else Top_High_Truth=0;
		top_high_truth_el_merged = Top_High_Truth;
		nTop_el_merged = nTop;
		nEvent_el_merged = i;
		top_idx_el_merged = k;
		for(N=0;N<nFiles;N++){
		  stringstream ss;
		  if(i<nEntries[N]){
		    ss << filename[N].substr(79,4);
		    ss >> sample_el_merged;
		    break;
		  }
		}
		
		el_merged->Fill();

	    }  // Electron Merged Category

	    if(mu_idx[k]!=-1 && Top_isMerged[k]==0){
	      
	        met_mu_resolved = MET;
	        met_phi_mu_resolved = MET_phi;

	        jet_m_mu_resolved = Jet_mass[jet_idx[k]];
	        jet_pt_mu_resolved = Jet_pt[jet_idx[k]];
		jet_eta_mu_resolved = Jet_eta[jet_idx[k]];
		jet_phi_mu_resolved = Jet_phi[jet_idx[k]];
		jet_Id_mu_resolved = Jet_Id[jet_idx[k]];
		jet_partFlav_mu_resolved = Jet_partonFlavour[jet_idx[k]];
		jet_hadFlav_mu_resolved = Jet_hadronFlavour[jet_idx[k]];
		jet_isDeep_mu_resolved = Jet_isDeep[jet_idx[k]];
		nJet_mu_resolved = Jet_size;
		jet_idx_mu_resolved = jet_idx[k];

		mu_pt_resolved = Mu_pt[mu_idx[k]];
		mu_phi_resolved = Mu_phi[mu_idx[k]];
	        mu_eta_resolved = Mu_eta[mu_idx[k]];
	        mu_charge_resolved = Mu_charge[mu_idx[k]];
	        mu_Dxy_resolved = Mu_Dxy[mu_idx[k]];
		mu_DxyErr_resolved = Mu_Dxyerr[mu_idx[k]];
	        mu_Dz_resolved = Mu_Dz[mu_idx[k]];
		mu_DzErr_resolved = Mu_Dzerr[mu_idx[k]];
	        mu_isL_resolved = Mu_isLoose[mu_idx[k]];
		mu_isM_resolved = Mu_isMedium[mu_idx[k]];
	        mu_isT_resolved = Mu_isTight[mu_idx[k]];
		mu_isGlob_resolved = Mu_isGlobal[mu_idx[k]];
	        mu_isTrack_resolved = Mu_isTracker[mu_idx[k]];
		mu_nStations_resolved = Mu_nStations[mu_idx[k]];
		mu_nTrackLayers_resolved = Mu_nTrackerLayers[mu_idx[k]];
	        mu_HighPtId_resolved = Mu_HighPtId[mu_idx[k]];
		mu_genPFlav_resolved = Mu_genPFlav[mu_idx[k]];
	        mu_MiniIso_resolved = Mu_MiniIso[mu_idx[k]];
		mu_Iso04_resolved = Mu_Iso04[mu_idx[k]];
		mujet_pt_resolved = Mu_pt[mu_idx[k]]/Jet_pt[jet_idx[k]];
		nMuon_resolved = Mu_size;
		mu_idx_resolved = mu_idx[k];

		top_m_mu_resolved = Top_mass[k];
		top_pt_mu_resolved = Top_pt[k];
		top_eta_mu_resolved = Top_eta[k];
		top_phi_mu_resolved = Top_phi[k];
		top_E_mu_resolved = Top_E[k];
		lj_m_mu_resolved = lj_mass[k];
		lj_pt_mu_resolved = lj_pt[k];
		lj_eta_mu_resolved = lj_eta[k];
		lj_phi_mu_resolved = lj_phi[k];
		lj_E_mu_resolved = lj_E[k];
		top_mT_mu_resolved = sqrt(2*lj_pt[k]*MET*(1-cos(deltaPhi(MET_phi,lj_phi[k]))));
		top_jetUnboost_m_mu_resolved = Top_jet_unboosted_mass[k];
		top_jetUnboost_pt_mu_resolved = Top_jet_unboosted_pt[k];
		top_jetUnboost_eta_mu_resolved = Top_jet_unboosted_eta[k];
		top_jetUnboost_phi_mu_resolved = Top_jet_unboosted_phi[k];
		top_jetUnboost_E_mu_resolved = Top_jet_unboosted_E[k];
		top_jet_hasPL_mu_resolved = Top_jet_hasPromptLep[k];
		top_lepUnboost_m_mu_resolved = Top_lep_unboosted_mass[k];
		top_lepUnboost_pt_mu_resolved = Top_lep_unboosted_pt[k];
		top_lepUnboost_eta_mu_resolved = Top_lep_unboosted_eta[k];
		top_lepUnboost_phi_mu_resolved = Top_lep_unboosted_phi[k];
		top_lepUnboost_E_mu_resolved = Top_lep_unboosted_E[k];
		top_relPt_mu_resolved = Top_relPt[k];
		top_costheta_mu_resolved = Top_cosTheta[k];
		top_dR_mu_resolved = Top_dR[k];
		tau_high_truth_mu_resolved = Top_Tau_High_Truth[k];
		top_category_mu_resolved = Top_Category[k];
		if(Top_Category[k]==0) Top_High_Truth=1;
		else Top_High_Truth=0;
		top_high_truth_mu_resolved = Top_High_Truth;
		nTop_mu_resolved = nTop;
		nEvent_mu_resolved = i;
		top_idx_mu_resolved = k;
		for(N=0;N<nFiles;N++){
		  stringstream ss;
		  if(i<nEntries[N]){
		    ss << filename[N].substr(79,4);
		    ss >> sample_mu_resolved;
		    break;
		  }
		}
		
		mu_resolved->Fill();

	    }  // Muon Resolved Category

	    if(mu_idx[k]!=-1 && Top_isMerged[k]==1){
	      
	        met_mu_merged = MET;
	        met_phi_mu_merged = MET_phi;

	        jet_m_mu_merged = Jet_mass[jet_idx[k]];
	        jet_pt_mu_merged = Jet_pt[jet_idx[k]];
		jet_eta_mu_merged = Jet_eta[jet_idx[k]];
		jet_phi_mu_merged = Jet_phi[jet_idx[k]];
		jet_Id_mu_merged = Jet_Id[jet_idx[k]];
		jet_partFlav_mu_merged = Jet_partonFlavour[jet_idx[k]];
		jet_hadFlav_mu_merged = Jet_hadronFlavour[jet_idx[k]];
		jet_isDeep_mu_merged = Jet_isDeep[jet_idx[k]];
		nJet_mu_merged = Jet_size;
		jet_idx_mu_merged = jet_idx[k];

		mu_pt_merged = Mu_pt[mu_idx[k]];
		mu_phi_merged = Mu_phi[mu_idx[k]];
	        mu_eta_merged = Mu_eta[mu_idx[k]];
	        mu_charge_merged = Mu_charge[mu_idx[k]];
	        mu_Dxy_merged = Mu_Dxy[mu_idx[k]];
		mu_DxyErr_merged = Mu_Dxyerr[mu_idx[k]];
	        mu_Dz_merged = Mu_Dz[mu_idx[k]];
		mu_DzErr_merged = Mu_Dzerr[mu_idx[k]];
	        mu_isL_merged = Mu_isLoose[mu_idx[k]];
		mu_isM_merged = Mu_isMedium[mu_idx[k]];
	        mu_isT_merged = Mu_isTight[mu_idx[k]];
		mu_isGlob_merged = Mu_isGlobal[mu_idx[k]];
	        mu_isTrack_merged = Mu_isTracker[mu_idx[k]];
		mu_nStations_merged = Mu_nStations[mu_idx[k]];
		mu_nTrackLayers_merged = Mu_nTrackerLayers[mu_idx[k]];
	        mu_HighPtId_merged = Mu_HighPtId[mu_idx[k]];
		mu_genPFlav_merged = Mu_genPFlav[mu_idx[k]];
	        mu_MiniIso_merged = Mu_MiniIso[mu_idx[k]];
		mu_Iso04_merged = Mu_Iso04[mu_idx[k]];
		mujet_pt_merged = Mu_pt[mu_idx[k]]/Jet_pt[jet_idx[k]];
		nMuon_merged = Mu_size;
		mu_idx_merged = mu_idx[k];

		top_m_mu_merged = Top_mass[k];
		top_pt_mu_merged = Top_pt[k];
		top_eta_mu_merged = Top_eta[k];
		top_phi_mu_merged = Top_phi[k];
		top_E_mu_merged = Top_E[k];
		lj_m_mu_merged = lj_mass[k];
		lj_pt_mu_merged = lj_pt[k];
		lj_eta_mu_merged = lj_eta[k];
		lj_phi_mu_merged = lj_phi[k];
		lj_E_mu_merged = lj_E[k];
		top_mT_mu_merged = sqrt(2*lj_pt[k]*MET*(1-cos(deltaPhi(MET_phi,lj_phi[k]))));
		top_jetUnboost_m_mu_merged = Top_jet_unboosted_mass[k];
		top_jetUnboost_pt_mu_merged = Top_jet_unboosted_pt[k];
		top_jetUnboost_eta_mu_merged = Top_jet_unboosted_eta[k];
		top_jetUnboost_phi_mu_merged = Top_jet_unboosted_phi[k];
		top_jetUnboost_E_mu_merged = Top_jet_unboosted_E[k];
		top_jet_hasPL_mu_merged = Top_jet_hasPromptLep[k];
		top_lepUnboost_m_mu_merged = Top_lep_unboosted_mass[k];
		top_lepUnboost_pt_mu_merged = Top_lep_unboosted_pt[k];
		top_lepUnboost_eta_mu_merged = Top_lep_unboosted_eta[k];
		top_lepUnboost_phi_mu_merged = Top_lep_unboosted_phi[k];
		top_lepUnboost_E_mu_merged = Top_lep_unboosted_E[k];
		top_relPt_mu_merged = Top_relPt[k];
		top_costheta_mu_merged = Top_cosTheta[k];
		top_dR_mu_merged = Top_dR[k];
		tau_high_truth_mu_merged = Top_Tau_High_Truth[k];
		top_category_mu_merged = Top_Category[k];
		if(Top_Category[k]==0) Top_High_Truth=1;
		else Top_High_Truth=0;
		top_high_truth_mu_merged = Top_High_Truth;
		nTop_mu_merged = nTop;
		nEvent_mu_merged = i;
		top_idx_mu_merged = k;
		for(N=0;N<nFiles;N++){
		  stringstream ss;
		  if(i<nEntries[N]){
		    ss << filename[N].substr(79,4);
		    ss >> sample_mu_merged;
		    break;
		  }
		}

		mu_merged->Fill();

	    }  // Muon Merged Category

	  } // Loop over Tops

    } // Loop of Entries

    el_resolved->Write();
    el_merged->Write();
    mu_resolved->Write();
    mu_merged->Write();

    f2->Close();

    return 1;
}

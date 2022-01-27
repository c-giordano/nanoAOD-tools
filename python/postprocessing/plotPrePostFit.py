#!/bin/env python
import optparse
from plots.plotUtils import *
usage = 'python plotPrePostFit.py -o fitfolder' #fit folder is the folder containing the fitDiagnostic.root file

signal = "WP_M6000W60_RH"
samples_CR0B = ["QCD", "DDFitWJetsTT_MttST", signal]
samples_SRT = ["QCD", "DDFitWJetsTT_MttST", signal]
samples_SRW = ["QCD", "DDFitWJetsTT_MttST", signal]
samples_SR2B = ["QCD", "DDFitWJetsTT_MttST", signal]

regions_mu = {
    "CR0B":("h_jets_best_Wprime_m_CR0B", "CR0B_muon", "CR0B_muon"),
    "SRT":("h_jets_best_Wprime_m_SRT", "SRT_muon", "SRT_muon"),
    "SRW":("h_jets_best_Wprime_m_SRW", "SRW_muon", "SRW_muon"),
    "SR2B":("h_jets_best_Wprime_m_SR2B", "SR2B_muon", "SR2B_muon"),
    }
regions_ele = {
    "CR0B":("h_jets_best_Wprime_m_CR0B", "CR0B_electron", "CR0B_electron"),
    "SRT":("h_jets_best_Wprime_m_SRT", "SRT_electron", "SRT_electron"),
    "SRW":("h_jets_best_Wprime_m_SRW", "SRW_electron", "SRW_electron"),
    "SR2B":("h_jets_best_Wprime_m_SR2B", "SR2B_electron", "SR2B_electron"),
    }

lep = ""
fitPhase = "prefit"
#fitPhase = "fit_b"
fitfolder = "/afs/cern.ch/work/a/adeiorio/CMSSW_10_2_5/src/Stat/Limits/test/26Jul21_dd_summedyears_CR_explin_v6"
fitfolder = "/eos/home-o/oiorio/Wprime/fitsetups/corrected_cr_2022"
histfolder = "/eos/home-o/oiorio/Wprime/nosynch/v18/plot_final_fit"

print('hello! Starting now')
#lep = "muon"
if lep == "muon":
    plot(histfolder, fitfolder, fitPhase, regions_mu["CR0B"], samples_CR0B)

#lep = "electron"
if lep == "electron":
    plot(histfolder, fitfolder, fitPhase, regions_ele["CR0B"], samples_CR0B)

lep = "muele"
if lep == "muele":    
    plot(histfolder, fitfolder, fitPhase, regions_mu["CR0B"], samples_CR0B)
    plot(histfolder, fitfolder, fitPhase, regions_ele["CR0B"], samples_CR0B)




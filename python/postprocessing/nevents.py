import os, commands
import optparse
import math
from ROOT import *

usage = 'python nevents.py'
parser = optparse.OptionParser(usage)
parser.add_option('-f', '--folder', dest='folder', type='string', default = 'v11', help='Default folder is v0')
#parser.add_option('-L', '--lep', dest='lep', type='string', default='muon', help='Default checks integrals of muon systematics')
(opt, args) = parser.parse_args()

folder = opt.folder
pathin = '/eos/user/a/adeiorio/Wprime/nosynch/' + folder + '/plot/'
#pathout = opt.pathout

gStyle.SetPalette(1)
gStyle.SetOptStat(0)
gROOT.SetBatch()        # don't pop up canvases

leptons = {
     "muon":["h_jets_best_Wprime_m_SR2B_I"],
#     "electron":["h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60", "h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_EQ_0_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60","h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60","h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_0_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"],
}

integrals = []
errors = []

samples = {
#     'DataMu_2016':'DataMuon', 'DataEle_2016':'DataElectron', 'DataHT_2016':'DataHT', 'ST_2016':'Single top', 'QCD_2016':'QCD', 'TT_Mtt_2016':'\\ttbar', 'WJets_2016':'\\wjets', 'WP_M2000W20_RH_2016':'\\PWpr 2\\tev(1\%)', 'WP_M3000W30_RH_2016':'\\PWpr 3\\tev(1\%)', 'WP_M4000W40_RH_2016':'\\PWpr 4\\tev(1\%)', 'WP_M4000W400_RH_2016':'\\PWpr 4\\tev(10\%)'
     'Data_2017':'Data', 'ST_2017':'Single top', 'QCD_2017':'QCD', 'TT_Mtt_2017':'\\ttbar', 'WJets_2017':'\\wjets',# 'WP_M2000W20_RH_2017':'\\PWpr 2\\tev(1\%)', 'WP_M3000W30_RH_2017':'\\PWpr 3\\tev(1\%)', 'WP_M4000W40_RH_2017':'\\PWpr 4\\tev(1\%)',  'WP_M5000W50_RH_2017':'\\PWpr 5\\tev(1\%)', 'WP_M6000W60_RH_2017':'\\PWpr 6\\tev(1\%)',# 'WP_M4000W400_RH_2017':'\\PWpr 4\\tev(10\%)',
#     'Data_2018':'DataMuon', 'ST_2018':'Single top', 'QCD_2018':'QCD', 'TT_Mtt_2018':'\\ttbar', 'WJets_2018':'\\wjets', 'WP_M2000W20_RH_2018':'\\PWpr 2\\tev(1\%)', 'WP_M3000W30_RH_2018':'\\PWpr 3\\tev(1\%)', 'WP_M4000W40_RH_2018':'\\PWpr 4\\tev(1\%)', 'WP_M4000W400_RH_2018':'\\PWpr 4\\tev(10\%)'
     }

def getSumError(_list):
     return math.sqrt(reduce(lambda x, y: x + y, list(map(lambda x: x**2, _list))))

def getSumSquared(_list):
     return reduce(lambda x, y: x + y, list(map(lambda x: x**2, _list)))

def getSignificance(_list):
     sign = []
     total = getSumSquared(_list)
     for el in _list:
          sign.append(100*(el**2/total))
#          print el, total 
     return sign

tex = True # False #
signif = False # True #
e = 0
for lep in leptons.keys():
     p = ""
     for hist in leptons[lep]:
          if lep == "muon":
               region = 'muon_'
          else:
               region = 'electron_'
          if hist == "h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_EQ_0_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60": 
               region += "SRT"
          elif hist == "h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60":
               region += "SRW"
          elif hist == "h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60":
               region += "SR2B"
          elif hist == "h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_0_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60":
               region += "CR0B"
          elif hist == "h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_EQ_0_AND_best_top_m_G_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60": 
               region += "SRT_I"
          elif hist == "h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_AND_best_top_m_G_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60":
               region += "SRW_I"
          elif hist == "h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_G_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60":
               region += "SR2B_I"
          elif hist == "h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_0_AND_best_top_m_G_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60":
               region += "CR0B_I"
          if(signif):
               infile = TFile.Open(pathin+"/Data_"+lep+".root")
               tmp = (TH1F)(infile.Get(hist))
               for i in range(1,tmp.GetNbinsX()+1):
                    errors_bin = []
                    total_bin = 0
                    st_bin = 0
                    for s, sname in samples.iteritems():
                         error = Double(0)
                         infile = TFile.Open(pathin+"/"+s+"_"+lep+".root")
                         tmp = (TH1F)(infile.Get(hist))
                         errors_bin.append(tmp.GetBinError(i))
                         total_bin += tmp.GetBinContent(i)
                         if s == "ST_tch":
                              st_bin = tmp.GetBinContent(i)
                    #print "Relative uncertainty %-20s %-8s, bin %-2i" %(hist, lep, i)
                    b = 100*st_bin/total_bin
                    if(b>100): 
                         p += " mcstat_"+region+"_ST_tch_bin"+str(i)
                    for s, el in zip(samples.keys(), errors_bin):
                         sign = 100*el/total_bin
                         if(sign>2 and s!="ST_tch_sd"): # and s!="DDQCD" and s!="ST_sch" and s!="VV" and s=="WJets"
                              e+=1
                              #print "%-10s %-4.2f %8s %2i %-0.2f " %(s, el, region, i, sign)
                              p += " mcstat_"+region+"_"+s+"_bin"+str(i)
               #print e
          if(tex):
               print "**********************************************"
               print "Region %s" %(region)
               print "\\begin{table}[]"
               print "\\begin{center}"
               print "\\caption{\label{tab:%s_%s} }" %(hist,lep)
               print "\\begin{tabular}{l|c c}"
               print "Process  & Integral $\pm$  Uncertainty & Abundancy \\\\ " 
               print "\\hline"
               integrals = []
               errors = []
               integrals_data = []
               errors_data = []
               snames = []
               for s, sname in samples.iteritems():
                    error = Double(0)
                    infile = TFile.Open(pathin + "/" + lep + "/" + s + "_" + lep + ".root")
                    tmp = (TH1F)(infile.Get(hist))
                    if not 'Data' in s:
                         integrals.append(tmp.IntegralAndError(1,tmp.GetNbinsX()+1, error))
                         errors.append(error)
                         snames.append(sname)
                         tmp.Reset("ICES")
                    else:
                         integrals_data.append(tmp.IntegralAndError(1,tmp.GetNbinsX()+1, error))
                         errors_data.append(error)
               for sname,integral,error in zip(snames, integrals, errors):
                    if not 'Data' in sname:
                         print "%-10s  & %-6i $\pm$  %-3i & %-3.2f \\\\ " %(sname, integral, error, integral/sum(integrals)*100)
               print "\\hline"
               print "Total MC  & %-6i $\pm$  %-3i \\\\ " %(sum(integrals),getSumError(errors))
               print "\\hline"
               print "Data  & %-6i $\pm$  %-3i \\\\ " %(sum(integrals_data),getSumError(errors_data))
               print "\\end{tabular}"
               print "\\end{center}"
               print "\\end{table}"

     if(signif):
          print p


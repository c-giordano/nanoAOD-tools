import os, commands
import optparse
from ROOT import *

usage = 'python systs_comparison.py'
parser = optparse.OptionParser(usage)
parser.add_option('--pathin', dest='pathin', type='string', default='Plot/fit/', help='')
parser.add_option('--pathout', dest='pathout', type='string', default='syst/', help='')
#parser.add_option('-L', '--lep', dest='lep', type='string', default='muon', help='Default checks integrals of muon systematics')
(opt, args) = parser.parse_args()

histos = []
#histos.append('h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_0_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60')
histos.append('h_jets_best_Wprime_m_CR0B')
histos.append('h_jets_best_Wprime_m_SR2B')
#h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60')


pathin = opt.pathin
pathout = opt.pathout

gStyle.SetPalette(1)
gStyle.SetOptStat(0)
gROOT.SetBatch()        # don't pop up canvases

leptons = [
"muon"
,"electron"
]

samples = [
#"QCD",
#"ST",
#"TT_Mtt",
#"WJets",
#"WP_M2000W20_RH",
#"WP_M6000W60_RH",
"DDFitWJetsTT_MttST"
]

logscale = True
scale = False
rebin = False
normalize = False # True #
systematics = {
     #"TT_Mtt":["jes", "jer", "pu" , "lep", "pdf_total", "q2", "btag", "mistag", "trig"],
     #"ST":["jes", "jer", "pu" , "lep", "pdf_total", "q2", "btag", "mistag", "trig"],
     #"WJets":["jes", "jer", "pu" , "lep", "pdf_total", "q2", "btag", "mistag", "trig"],
     "WP_M6000W60_RH":["jes", "jer", "pu" , "lep", "pdf_total", "btag", "mistag", "trig"],# "q2",
     #"QCD":["jes", "jer", "pu" , "lep", "pdf_total", "btag", "mistag", "trig"], # "q2",
     "DDFitWJetsTT_MttST":["TT_Mtt", "WJets", "ST", "TF_2020", "DD_2020", "Alt_2020", "AltTF_2020", "CR_2020"] #"jes", "jer", "pu" , "lep", "pdf_total", "q2", "btag", "mistag", "trig", 
 }
#systematics = {
     #"TT_Mtt":["jes", "jer", "pu" , "lep", "pdf_total", "q2", "btag", "mistag", "trig"],
     #"ST":["jes", "jer", "pu" , "lep", "pdf_total", "q2", "btag", "mistag", "trig"],
     #"WJets":["jes", "jer", "pu" , "lep", "pdf_total", "q2", "btag", "mistag", "trig"],
#     "WP_M2000W20_RH":["jes2016", "jes2017", "jes2018", "jer2016", "jer2017", "jer2018", "pu2016", "pu2017", "pu2018", "lep2016", "lep2017", "lep2018", "pdf_total2016", "pdf_total2017", "pdf_total2018", "q22016", "q22017", "q22018", "btag2016", "btag2017", "btag2018", "mistag2016", "mistag2017", "mistag2018", "trig2016", "trig2017", "trig2018"],
#     "QCD":["jes2016", "jes2017", "jes2018", "jer2016", "jer2017", "jer2018", "pu2016", "pu2017", "pu2018", "lep2016", "lep2017", "lep2018", "pdf_total2016", "pdf_total2017", "pdf_total2018", "q22016", "q22017", "q22018", "btag2016", "btag2017", "btag2018", "mistag2016", "mistag2017", "mistag2018", "trig2016", "trig2017", "trig2018"],
#     "DDFitWJetsTT_MttST":["TT_Mtt", "WJets", "ST", "TF_2020", "DD_2020", "Alt_2020"]
# }

year = '2020'

for lep in leptons:
     for s in samples:
          if not os.path.exists(pathout+lep+"/"+s+"_"+ year):
               os.system("mkdir -p "+pathout+lep+"/"+s+"_"+ year)
          for syst in systematics.get(s): #dictionary
               infile = []
               infile.append(TFile.Open(pathin+'/'+lep+'/'+s+"_" + year + "_"+lep+".root"))
               if lep == 'muon' and (syst == 'lep' or syst == 'trig'):
                    infile.append(TFile.Open(pathin+'/'+lep+'/'+s+"_" + year + "_"+lep+"_"+syst+"_muUp.root"))
                    infile.append(TFile.Open(pathin+'/'+lep+'/'+s+"_" + year + "_"+lep+"_"+syst+"_muDown.root"))
               elif lep == 'electron' and (syst == 'lep' or syst == 'trig'):
                    infile.append(TFile.Open(pathin+'/'+lep+'/'+s+"_" + year + "_"+lep+"_"+syst+"_eleUp.root"))
                    infile.append(TFile.Open(pathin+'/'+lep+'/'+s+"_" + year + "_"+lep+"_"+syst+"_eleDown.root"))
               elif lep == 'muon' and s == 'DDFitWJetsTT_MttST':
                    infile.append(TFile.Open(pathin+'/'+lep+'/'+s+"_" + year + "_"+lep+"_"+syst+"_muUp.root"))
                    infile.append(TFile.Open(pathin+'/'+lep+'/'+s+"_" + year + "_"+lep+"_"+syst+"_muDown.root"))
               elif lep == 'electron' and s == 'DDFitWJetsTT_MttST':
                    infile.append(TFile.Open(pathin+'/'+lep+'/'+s+"_" + year + "_"+lep+"_"+syst+"_eleUp.root"))
                    infile.append(TFile.Open(pathin+'/'+lep+'/'+s+"_" + year + "_"+lep+"_"+syst+"_eleDown.root"))
               else:
                    infile.append(TFile.Open(pathin+'/'+lep+'/'+s+"_" + year + "_"+lep+"_"+syst+"Up.root"))
                    infile.append(TFile.Open(pathin+'/'+lep+'/'+s+"_" + year + "_"+lep+"_"+syst+"Down.root"))
               for hist in histos:
                    print pathout+lep+"/"+s+"/"+hist+"_"+syst
                    h1 = TH1F()
                    h2 = TH1F()
                    h3 = TH1F()
                    c1 = TCanvas(str(hist),"c1",50,50,700,600)
                    leg = TLegend(0.7,0.7,0.9,0.9)
                    for inf in infile:
                         inf.cd()
                         tmp = (TH1F)(inf.Get(hist))
                         filename = (str)(inf.GetName())
          #          print "filename" , filename
                         if("Up" in filename):
                              h1 = tmp.Clone("nominal") 
                              if rebin:
                                   h1.Rebin(4)
                              h1.SetTitle(str(hist))
#               h1.SetName(str(hist))
                         elif("Down" in filename):
                              h2 = tmp.Clone("nominal") 
                              if rebin:
                                   h2.Rebin(4)
                              h2.SetTitle("down")
                         else:
                              h3 = tmp.Clone("nominal")
               #               print "i0ntegral ", h3.Integral()
                              if scale:
                                   h3.Scale(1./norm.GetBinContent(0))
               #               h3.SetName("nominal")
                              if rebin:
                                   h3.Rebin(4)
                              h3.SetTitle("nominal")
                         tmp.Reset("ICES")
                    c1.cd()
                    maximum = max(h1.GetMaximum(),h2.GetMaximum(),h3.GetMaximum())
                    minimum = min(h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum())
                    h1.SetMaximum(maximum*1.5)
                    h1.SetMinimum(0.0)
                    if(logscale):
                         h1.SetMaximum(maximum*150)
                         h1.SetMinimum(minimum/10)
                    h1.SetLineColor(kRed)
                    h1.GetXaxis().SetTitle("W' mass [GeV]")
                    if(normalize):
                         h1.GetYaxis().SetTitle("Fraction of Events/bin")
                         h1.DrawNormalized("E")
                    else:
                         h1.GetYaxis().SetTitle("Events/bin")
                         h1.Draw("E")
                    h1.SetTitle(syst)
                    print "int h1 up",h1.Integral()
                    h2.SetLineColor(kGreen)
                    if(normalize):
                         h2.DrawNormalized("ESAME")
                    else:
                         h2.Draw("ESAME")
                    print "int h2 down",h2.Integral()
                    h3.SetLineColor(kBlue)
                    if(normalize):
                         h3.DrawNormalized("ESAME")
                    else:
                         h3.Draw("HIST SAME")
                    print "int h3 nominal",h3.Integral()
                    leg.AddEntry(h1, "up", "l")
                    leg.AddEntry(h3, "nominal", "l")
                    leg.AddEntry(h2, "down", "l")
                    leg.Draw("SAME")
                    c1.cd()
                    if(logscale):
                         c1.SetLogy()
                    TGaxis.SetMaxDigits(3)
                    c1.RedrawAxis()
                    c1.Update()
#                    c1.Print(pathout+lep+"/"+s+"/"+hist+"_"+syst+".pdf")
                    c1.Print(pathout+lep+"/"+s+"_"+year+"/"+hist+"_"+syst+".png")
#                    c1.Print(pathout+lep+"/"+s+"/"+hist+"_"+syst+".root")
                    c1.Close()

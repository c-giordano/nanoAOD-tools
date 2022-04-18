import ROOT
import copy
import os
from array import array
folder = 'v18'
plotpath = '/eos/user/'+str(os.environ.get('USER')[0])+'/'+str(os.environ.get('USER'))+'/Wprime/nosynch/' + folder + '/plot_fit3Apr/'

ROOT.gROOT.SetBatch() # don't pop up canvases
ROOT.gStyle.SetOptStat(0)

histos = ['h_jets_best_Wprime_m_SR2B', 'h_jets_best_Wprime_m_SRT', 'h_jets_best_Wprime_m_SRW']
versus = ["Up", "Down"]
#years = ['2016', '2017', '2018']
years = ['2020']

sample = 'WP_M5000W50_RH'
systematics = {"jes2016":ROOT.kRed,"jes2017":ROOT.kRed+1,"jes2018":ROOT.kRed+2, "jer2016":ROOT.kBlue, "jer2017":ROOT.kBlue+1, "jer2018":ROOT.kBlue+2, "PF":ROOT.kOrange, "pu":ROOT.kYellow+4, "btag":ROOT.kCyan, "mistag":ROOT.kPink, "lep_ele":ROOT.kAzure, "trig_ele":ROOT.kMagenta, "pdf_total":ROOT.kGreen+2}
#systematics = {"jes2016":ROOT.kRed,"jes2017":ROOT.kRed+1,"jes2018":ROOT.kRed+2, "jer2016":ROOT.kBlue, "jer2017":ROOT.kBlue+1, "jer2018":ROOT.kBlue+2, "PF":ROOT.kOrange, "pu":ROOT.kYellow+4, "btag":ROOT.kCyan, "mistag":ROOT.kPink, "lep_mu":ROOT.kAzure, "trig_mu":ROOT.kMagenta, "pdf_total":ROOT.kGreen+2}

sample = 'DDFitWJetsTT_MttST'
#syst_base = {"jes2016":ROOT.kRed-1,"jes2017":ROOT.kRed-2,"jes2018":ROOT.kRed-3, "jer2016":ROOT.kBlue, "jer2017":ROOT.kBlue+1, "jer2018":ROOT.kBlue+2, "pdf_total":ROOT.kGreen-2, "ST_mu":ROOT.kBlue-1, "TT_Mtt_mu":ROOT.kMagenta, "WJets_mu":ROOT.kCyan, "LHETT_Mtt": ROOT.kCyan+2, "LHEWJets": ROOT.kCyan+3, "LHEST":ROOT.kCyan+4}


#sample = 'TT_Mtt'
#sample = 'QCD'
leps = ['electron']
leps = ['muon']

for h in histos:
    for year in years:
        for lep in leps:
            fnom = ROOT.TFile.Open(plotpath + lep + '/' + sample + '_' + year + '_' + lep + '.root')
            hnom = copy.deepcopy(fnom.Get(h))
            htot_up = hnom.Clone()
            htot_down = hnom.Clone()
            htot_up.Reset("ICES")
            htot_down.Reset("ICES")
            htot = {"Up": htot_up, "Down": htot_down}
            canvasname = sample + year + '_' + lep + '_' + h 
            c1 = ROOT.TCanvas(canvasname,"c1",50,50,700,600)
            c1.SetFillColor(0)
            c1.SetBorderMode(0)
            c1.SetFrameFillStyle(0)
            c1.SetFrameBorderMode(0)
            c1.SetLeftMargin( 0.12 )
            c1.SetRightMargin( 0.9 )
            c1.SetTopMargin( 1 )
            c1.SetBottomMargin(-1)
            c1.SetTickx(1)
            c1.SetTicky(1)
            bins = array('f', [1000., 1250., 1500., 1750., 2000., 2250., 2500., 2750., 3000., 3500., 4500., 6000.])
            nbins = len(bins)-1
            hsysts = []
            leg = ROOT.TLegend(0.35,0.54,0.91,0.89)
            leg.SetNColumns(2)
            leg.SetFillColor(0)
            leg.SetFillStyle(0)
            leg.SetTextFont(42)
            leg.SetBorderSize(0)
            leg.SetTextSize(0.02)
            f1 = ROOT.TLine(1000., 0., 6000., 0.)
            f1.SetLineColor(ROOT.kBlack)
            #f1.SetLineStyle(ROOT.kDashed)
            if "DDFit" in sample:
                if "ele" in lep:
                    systematics = {"jes2016":ROOT.kRed-1,"jes2017":ROOT.kRed-2,"jes2018":ROOT.kRed-3, "jer2016":ROOT.kBlue, "jer2017":ROOT.kBlue+1, "jer2018":ROOT.kBlue+2, "pdf_total":ROOT.kGreen-2, "ST_ele":ROOT.kBlue-1, "TT_Mtt_ele":ROOT.kMagenta, "WJets_ele":ROOT.kCyan, "LHETT_Mtt": ROOT.kCyan+2, "LHEWJets": ROOT.kCyan+3, "LHEST":ROOT.kCyan+4}
                    if h == "h_jets_best_Wprime_m_SR2B":
                        systematics["TF_SR2B_2020_ele"] = ROOT.kRed
                        systematics["Alt_SR2B_2020_ele"] = ROOT.kYellow+4
                        systematics["DD_SR2B_2020_ele"] = ROOT.kGreen+2 
                        systematics["CR_SR2B_2020_ele"] = ROOT.kMagenta+4
                        systematics["AltTF_SR2B_2020_ele"] = ROOT.kPink+4
                    elif h == "h_jets_best_Wprime_m_SRW":
                        systematics["TF_SRW_2020_ele"] = ROOT.kRed
                        systematics["Alt_SRW_2020_ele"] = ROOT.kYellow+4
                        systematics["DD_SRW_2020_ele"] = ROOT.kGreen+2 
                        systematics["CR_SRW_2020_ele"] = ROOT.kMagenta+4
                        systematics["AltTF_SRW_2020_ele"] = ROOT.kPink+4
                    elif h == "h_jets_best_Wprime_m_SRT":
                        systematics["TF_SRT_2020_ele"] = ROOT.kRed
                        systematics["Alt_SRT_2020_ele"] = ROOT.kYellow+4
                        systematics["DD_SRT_2020_ele"] = ROOT.kGreen+2 
                        systematics["CR_SRT_2020_ele"] = ROOT.kMagenta+4
                        systematics["AltTF_SRT_2020_ele"] = ROOT.kPink+4
                if "mu" in lep:
                    systematics = {"jes2016":ROOT.kRed-1,"jes2017":ROOT.kRed-2,"jes2018":ROOT.kRed-3, "jer2016":ROOT.kBlue, "jer2017":ROOT.kBlue+1, "jer2018":ROOT.kBlue+2, "pdf_total":ROOT.kGreen-2, "ST_mu":ROOT.kBlue-1, "TT_Mtt_mu":ROOT.kMagenta, "WJets_mu":ROOT.kCyan, "LHETT_Mtt": ROOT.kCyan+2, "LHEWJets": ROOT.kCyan+3, "LHEST":ROOT.kCyan+4}
                    if h == "h_jets_best_Wprime_m_SR2B":
                        systematics["TF_SR2B_2020_mu"] = ROOT.kRed
                        systematics["Alt_SR2B_2020_mu"] = ROOT.kYellow+4
                        systematics["DD_SR2B_2020_mu"] = ROOT.kGreen+2 
                        systematics["CR_SR2B_2020_mu"] = ROOT.kMagenta+4
                        systematics["AltTF_SR2B_2020_mu"] = ROOT.kPink+4
                    elif h == "h_jets_best_Wprime_m_SRW":
                        systematics["TF_SRW_2020_mu"] = ROOT.kRed
                        systematics["Alt_SRW_2020_mu"] = ROOT.kYellow+4
                        systematics["DD_SRW_2020_mu"] = ROOT.kGreen+2 
                        systematics["CR_SRW_2020_mu"] = ROOT.kMagenta+4
                        systematics["AltTF_SRW_2020_mu"] = ROOT.kPink+4
                    elif h == "h_jets_best_Wprime_m_SRT":
                        systematics["TF_SRT_2020_mu"] = ROOT.kRed
                        systematics["Alt_SRT_2020_mu"] = ROOT.kYellow+4
                        systematics["DD_SRT_2020_mu"] = ROOT.kGreen+2 
                        systematics["CR_SRT_2020_mu"] = ROOT.kMagenta+4
                        systematics["AltTF_SRT_2020_mu"] = ROOT.kPink+4

            for syst in systematics.keys():
                for vs in versus:
                    fsyst = ROOT.TFile.Open(plotpath + lep + '/' + sample + '_' + year + '_' + lep + '_' + syst + vs +'.root')
                    hsyst = copy.deepcopy(fsyst.Get(h)) 
                    hsyst.SetLineColor(systematics[syst])
                    hsyst.Add(hnom, -1)
                    hsyst.Divide(hnom)
                    htot[vs].Add(hsyst)
                    if vs == "Down":
                        hsyst.SetLineStyle(7)
                    c1.cd()
                    hsyst.SetTitle('; W\' mass [GeV] ; #frac{syst-nominal}{nominal}')
                    #hsyst.GetXaxis().SetLabel('W\' mass [GeV]')
                    #hsyst.GetYaxis().SetLabel('#frac{syst-nominal}{nominal}')
                    hsyst.GetYaxis().SetRangeUser(-1.0, 1.5)
                    leg.AddEntry(hsyst, syst+' '+vs, "l")
                    hsysts.append(hsyst)
                    hsyst.Draw("SAMEHIST")
            leg.Draw("SAME") 
            f1.Draw("SAME")
            latex = ROOT.TLatex()
            latex.SetTextSize(0.045)
            latex.SetTextAlign(12)
            if lep == 'electron':
                latex.DrawLatex(1500, 1.25, "e+jets")
            else:
                latex.DrawLatex(1500, 1.25, "#mu+jets")
            #htot_up.SetLineColor(ROOT.kBlack)
            #htot_down.SetLineColor(ROOT.kBlack)
            #htot_up.Draw("SAMEHIST")
            #htot_down.Draw("SAMEHIST")
            #c1.SetLogy()
            c1.Print('syst/' + canvasname + '.png')


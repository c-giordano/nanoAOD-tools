import ROOT
import copy
import os
from array import array
folder = 'v17'
plotpath = '/eos/user/'+str(os.environ.get('USER')[0])+'/'+str(os.environ.get('USER'))+'/Wprime/nosynch/' + folder + '/plot_merged_2017fix/'

ROOT.gROOT.SetBatch() # don't pop up canvases
ROOT.gStyle.SetOptStat(0)

histos = ['h_jets_best_Wprime_m_SR2B', 'h_jets_best_Wprime_m_SRT', 'h_jets_best_Wprime_m_SRW']
systematics = {"jes":ROOT.kRed, "jer":ROOT.kBlue, "PF":ROOT.kOrange, "pu":ROOT.kYellow+4, "btag":ROOT.kCyan, "mistag":ROOT.kPink, "lep":ROOT.kAzure, "trig":ROOT.kMagenta}#, "pdf_total":ROOT.kGreen+2}#, "q2":ROOT.kBlue}
#systematics = {"jes":ROOT.kRed, "jer":ROOT.kBlue, "PF":ROOT.kOrange, "pu":ROOT.kYellow+4, "btag":ROOT.kCyan, "mistag":ROOT.kPink, "lep":ROOT.kAzure, "trig":ROOT.kMagenta, "pdf_total":ROOT.kGreen+2}#, "q2":ROOT.kBlue}
#systematics = {"TF_2020":ROOT.kRed, "DD_2020":ROOT.kGreen+2, "Alt_2020":ROOT.kOrange, "AltTF_2020":ROOT.kPink, "ST":ROOT.kBlue, "TT_Mtt":ROOT.kMagenta, "WJets":ROOT.kCyan}
versus = ["Up", "Down"]
years = ['2016', '2017', '2018']
years = ['2020']
sample = 'WP_M5000W50_RH'
#sample = 'QCD'
#sample = 'DDFitWJetsTT_MttST'
#sample = 'TT_Mtt'
leps = ['electron']

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
            leg = ROOT.TLegend(0.35,0.62,0.91,0.85)
            leg.SetNColumns(2)
            leg.SetFillColor(0)
            leg.SetFillStyle(0)
            leg.SetTextFont(42)
            leg.SetBorderSize(0)
            leg.SetTextSize(0.03)
            f1 = ROOT.TLine(1000., 0., 6000., 0.)
            f1.SetLineColor(ROOT.kBlack)
            #f1.SetLineStyle(ROOT.kDashed)
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
                    hsyst.GetYaxis().SetRangeUser(-1.0, 1.0)
                    leg.AddEntry(hsyst, syst+' '+vs, "l")
                    hsysts.append(hsyst)
                    hsyst.Draw("SAMEHIST")
            leg.Draw("SAME") 
            f1.Draw("SAME")
            latex = ROOT.TLatex()
            latex.SetTextSize(0.045)
            latex.SetTextAlign(12)
            if lep == 'electron':
                latex.DrawLatex(1500, 0.75, "e+jets")
            else:
                latex.DrawLatex(1500, 0.75, "#mu+jets")
            #htot_up.SetLineColor(ROOT.kBlack)
            #htot_down.SetLineColor(ROOT.kBlack)
            #htot_up.Draw("SAMEHIST")
            #htot_down.Draw("SAMEHIST")
            #c1.SetLogy()
            c1.Print('syst/' + canvasname + '.png')


import ROOT,copy

noms={}
var1={}
var2={}

noms["WJets"]="localtest/v18/plot/muon/WJets_2018_muon.root"
var1["WJets"]="WJets_2018_muon.root"
var2["WJets"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot/muon/WJets_2018_muon.root"

regs=["SR2B","SRW","CR0B","SRT"]


c1=ROOT.TCanvas("c1")
c1.Draw()
regs=["SR2B"]
regs=["SRW","CR0B"]
regs=["SRW_II","CR0B_II"]
regs=["CR0B"]
histos=[]
for r in regs:
    for n in noms:
        c1.cd()
        h1n="h_jets_best_Wprime_m_"+r 
        h2n="h_jets_best_Wprime_m_"+r+"_I" 
        if("II" in r): h2n="h_jets_best_Wprime_m_"+r+"I" 
        hnom=ROOT.TH1F()
        hnom_I=ROOT.TH1F()
        h1=ROOT.TH1F()
        h1_I=ROOT.TH1F()
        h2=ROOT.TH1F()
        h2_I=ROOT.TH1F()
        print(h1n)
        print(ROOT.TFile(noms[n]))
        fnom=(ROOT.TFile(noms[n]))
        f1=(ROOT.TFile(var1[n]))
        f2=(ROOT.TFile(var2[n]))

        hnom=copy.deepcopy(fnom.Get(h1n).Clone())
        hnom_I=copy.deepcopy(fnom.Get(h2n).Clone())

        h1=copy.deepcopy(f1.Get(h1n).Clone())
        h1_I=copy.deepcopy(f1.Get(h2n).Clone())

        #        f2_I=(ROOT.TFile(var2[n]))
        #        


        h2=copy.deepcopy(f2.Get(h1n).Clone())
        h2_I=copy.deepcopy(f2.Get(h2n).Clone())

        hnom.SetLineColor(ROOT.kBlack)
        h1.SetLineColor(ROOT.kRed)
        h2.SetLineColor(ROOT.kRed)
        
        hnom.Integral()
        c1.SetLogy()
        hnom.Draw("histo")
        h1.Draw("same")
        #        r1 = ROOT.TRatioPlot(h1,hnom)
        r1 = ROOT.TRatioPlot(hnom,h1)
        r1.Draw()
        c1.SaveAs("nom_vs_Q2_"+n+"_"+r+".png")

        hnom.Draw("histo")
        h2.Draw("same")
        r1 = ROOT.TRatioPlot(hnom,h2)
        r1.Draw()
        c1.SaveAs("nom_vs_Q2_x2_"+n+"_"+r+".png")

        c1.SetLogy(0)
        hnom.Divide(hnom_I)
        hnom.Draw("histo")
        h1.Divide(h1_I)
        h1.Draw("same")
        r1 = ROOT.TRatioPlot(hnom,h1)
        r1.Draw()
        c1.SaveAs("nom_vs_Q2_TF_"+n+"_"+r+".png")

        hnom.Draw("histo")
        h2.Divide(h2_I)
        h2.Draw("same")
        r1 = ROOT.TRatioPlot(hnom,h2)
        r1.Draw()
        c1.SaveAs("nom_vs_Q2_x2_TF_"+n+"_"+r+".png")
        
        print f2
#        print h1,h2,h1_I,h2_I,hnom,hnom_I

#noms.append([""])

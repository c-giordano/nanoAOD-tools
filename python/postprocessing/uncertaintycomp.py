import ROOT,copy

noms={}
var1={}
var2={}


regs=["SR2B","SRW","CR0B","SRT"]

#noms["TTbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot/muon/TT_Mtt_2018_muon.root"
#var1["TTbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot/muon/TT_Mtt_2018_muon_btagUp.root"
#var2["TTbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot/muon/TT_Mtt_2018_muon_btagDown.root"

#noms["WJetsbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot/muon/WJets_2018_muon.root"
#var1["WJetsbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot/muon/WJets_2018_muon_btagUp.root"
#var2["WJetsbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot/muon/WJets_2018_muon_btagDown.root"



#total

noms["DDFitWJetsTT_MttSTjer"]="localtestnew/v18/plot_explin_fit/muon/DDFitWJetsTT_MttST_2020_muon.root"
var1["DDFitWJetsTT_MttSTjer"]="localtestnew/v18/plot_explin_fit/muon/DDFitWJetsTT_MttST_2020_muon_jerUp.root"
var2["DDFitWJetsTT_MttSTjer"]="localtestnew/v18/plot_explin_fit/muon/DDFitWJetsTT_MttST_2020_muon_jerDown.root"


#noms["DDFitWJetsTT_MttSTlep"]="localtestnew/v18/plot_explin_fit/muon/DDFitWJetsTT_MttST_2020_muon.root"
#var1["DDFitWJetsTT_MttSTlep"]="localtestnew/v18/plot_explin_fit/muon/DDFitWJetsTT_MttST_2020_muon_lepUp.root"
#var2["DDFitWJetsTT_MttSTlep"]="localtestnew/v18/plot_explin_fit/muon/DDFitWJetsTT_MttST_2020_muon_lepDown.root"


#noms["DDFitWJetsTT_MttSTpu"]="localtestnew/v18/plot_explin_fit/muon/DDFitWJetsTT_MttST_2020_muon.root"
#var1["DDFitWJetsTT_MttSTpu"]="localtestnew/v18/plot_explin_fit/muon/DDFitWJetsTT_MttST_2020_muon_puUp.root"
#var2["DDFitWJetsTT_MttSTpu"]="localtestnew/v18/plot_explin_fit/muon/DDFitWJetsTT_MttST_2020_muon_puDown.root"


#
#noms["WJetsTT_MttSTbtag"]="localtest/v18/plot_explin//muon/WJetsTT_MttST_2020_muon.root"
#var1["WJetsTT_MttSTbtag"]="localtest/v18/plot_explin//muon/WJetsTT_MttST_2020_muon_btagUp.root"
#var2["WJetsTT_MttSTbtag"]="localtest/v18/plot_explin//muon/WJetsTT_MttST_2020_muon_btagDown.root"

#noms["DDFitWJetsTT_MttSTtrig"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon.root"
#var1["DDFitWJetsTT_MttSTtrig"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_trigUp.root"
#var2["DDFitWJetsTT_MttSTtrig"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_trigDown.root"

#noms["DDFitWJetsTT_MttSTDD_2020"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon.root"
#var1["DDFitWJetsTT_MttSTDD_2020"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_DD_2020_muUp.root"
#var2["DDFitWJetsTT_MttSTDD_2020"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_DD_2020_muDown.root"

#noms["DDFitWJetsTT_MttSTTF_2020"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon.root"
#var1["DDFitWJetsTT_MttSTTF_2020"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_TF_2020_muUp.root"
#var2["DDFitWJetsTT_MttSTTF_2020"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_TF_2020_muDown.root"

#noms["DDFitWJetsTT_MttSTCR_2020"]="localtest/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon.root"
#var1["DDFitWJetsTT_MttSTCR_2020"]="localtest/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_CR_2020_muUp.root"
#var2["DDFitWJetsTT_MttSTCR_2020"]="localtest/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_CR_2020_muDown.root"

#noms["DDFitWJetsTT_MttSTjes"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon.root"
#var1["DDFitWJetsTT_MttSTjes"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_jesUp.root"
#var2["DDFitWJetsTT_MttSTjes"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_jesDown.root"

'''
###
noms["DDFitWJetsTT_MttSTbtag"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon.root"
var1["DDFitWJetsTT_MttSTbtag"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_btagUp.root"
var2["DDFitWJetsTT_MttSTbtag"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_btagDown.root"

noms["DDFitWJetsTT_MttSTTT_Mtt_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon.root"
var1["DDFitWJetsTT_MttSTTT_Mtt_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_TT_Mtt_muUp.root"
var2["DDFitWJetsTT_MttSTTT_Mtt_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_TT_Mtt_muDown.root"

noms["DDFitWJetsTT_MttSTWJets_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon.root"
var1["DDFitWJetsTT_MttSTWJets_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_WJets_muUp.root"
var2["DDFitWJetsTT_MttSTWJets_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_WJets_muDown.root"

noms["DDFitWJetsTT_MttSTST_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon.root"
var1["DDFitWJetsTT_MttSTST_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_ST_muUp.root"
var2["DDFitWJetsTT_MttSTST_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_ST_muDown.root"

noms["DDFitWJetsTT_MttSTAlt_2020_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon.root"
var1["DDFitWJetsTT_MttSTAlt_2020_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_Alt_2020_muUp.root"
var2["DDFitWJetsTT_MttSTAlt_2020_mu"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_Alt_2020_muDown.root"
####'''
#noms["DDFitWJetsTT_MttSTbtag"]="localtest/v18/plot_explin//muon/DDFitWJetsTT_MttST_2020_muon.root"
#var1["DDFitWJetsTT_MttSTbtag"]="localtest/v18/plot_explin//muon/DDFitWJetsTT_MttST_2020_muon_btagUp.root"
#var2["DDFitWJetsTT_MttSTbtag"]="localtest/v18/plot_explin//muon/DDFitWJetsTT_MttST_2020_muon_btagDown.root"

#noms["DDFitWJetsTT_MttSTjes"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon.root"
#var1["DDFitWJetsTT_MttSTjes"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_jesUp.root"
#var2["DDFitWJetsTT_MttSTjes"]="localtestnew/v18/plot_explin_fit//muon/DDFitWJetsTT_MttST_2020_muon_jesDown.root"


#
#noms["TT_Mttbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot_merged//muon/TT_Mtt_2020_muon.root"
#var1["TT_Mttbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot_merged//muon/TT_Mtt_2020_muon_btagUp.root"
#var2["TT_Mttbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot_merged//muon/TT_Mtt_2020_muon_btagDown.root"

#noms["TT_Mttbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot//muon/TT_Mtt_2020_muon.root"
#var1["TT_Mttbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot//muon/TT_Mtt_2020_muon_btagUp.root"
#var2["TT_Mttbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot//muon/TT_Mtt_2020_muon_btagDown.root"

#noms["TT_Mttbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot_merged//electron/TT_Mtt_2020_electron.root"
#var1["TT_Mttbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot_merged//electron/TT_Mtt_2020_electron_btagUp.root"
#var2["TT_Mttbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot_merged//electron/TT_Mtt_2020_electron_btagDown.root"

#noms["WJetsbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot_merged//muon/WJets_2020_muon.root"
#var1["WJetsbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot_merged//muon/WJets_2020_muon_btagUp.root"
#var2["WJetsbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot_merged//muon/WJets_2020_muon_btagDown.root"

#noms["STbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot/muon/ST_2018_muon.root"
#var1["STbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot/muon/ST_2018_muon_btagUp.root"
#var2["STbtag"]="/eos/home-o/oiorio/Wprime/nosynch/v18/plot/muon/ST_2018_muon_btagDown.root"
#


c1 = ROOT.TCanvas("c1")
c1.Draw()
regs=["SR2B"]
#regs=["SRW","CR0B"]
#regs=["SRW_II","CR0B_II"]
#regs=["CR0B"]

for r in regs:
    for n in noms:
        c1.cd()
        doDoubleRatios=(not "DDFit" in n)
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

        hnom=copy.deepcopy(fnom.Get(h1n).Clone("hnom"+n+r))
        h1=copy.deepcopy(f1.Get(h1n).Clone("hup"+n+r))
        h2=copy.deepcopy(f2.Get(h1n).Clone("hdown"+n+r))

        if(doDoubleRatios):
            hnom_I=copy.deepcopy(fnom.Get(h2n).Clone())
            h1_I=copy.deepcopy(f1.Get(h2n).Clone())
            h2_I=copy.deepcopy(f2.Get(h2n).Clone())

        hnom.SetLineColor(ROOT.kBlack)
        h1.SetLineColor(ROOT.kRed)
        h2.SetLineColor(ROOT.kGreen+2)
        maxdiffrel=0.2        
        for b in range(1,hnom.GetNbinsX()+1):
            hnom.SetBinError(b,0.001*hnom.GetBinContent(b))
            diffrelbin=0
            if(hnom.GetBinContent(b)!=0):
                diffrelbin=max(abs(1-h1.GetBinContent(b)/hnom.GetBinContent(b)),abs(1-h2.GetBinContent(b)/hnom.GetBinContent(b) ) )
            maxdiffrel=max(diffrelbin,maxdiffrel)
            if doDoubleRatios: 
                #hnom.SetBinError(b,0.001*hnom.GetBinContent(b))
                #h1.SetBinError(b,0.001*h1.GetBinContent(b))
                #h2.SetBinError(b,0.001*h2.GetBinContent(b))
                hnom.SetBinError(b,0)
                h1.SetBinError(b,0)
                h2.SetBinError(b,0)
               
            
        hnom.Integral()
        
        c1.SetLogy()
        hnom.Draw("histo")
        
        #r1 = ROOT.TRatioPlot(h1,h2)

        #r1 = ROOT.TRatioPlot(hnom,h1,"divsym")
        #r2 = ROOT.TRatioPlot(hnom,h2,"divsym")

        r1 = ROOT.TRatioPlot(h1,hnom,"divsym")
        r2 = ROOT.TRatioPlot(h2,hnom,"divsym")

        
        r2.Draw()
        g2 = r2.GetLowerRefGraph().Clone("g2")
        print(g2.GetN(), h1.GetNbinsX(),hnom.GetNbinsX(),h2.GetNbinsX())

        r1.Draw()
        print("maxdiffrel is ",maxdiffrel)
        #       r1.GetLowerRefGraph().SetLineColor(ROOT.kRed)
        r1.GetLowerRefGraph().SetMarkerColorAlpha(ROOT.kRed,0.9)
        r1.GetLowerRefGraph().SetLineColorAlpha(ROOT.kRed,0.9)
        r1.GetLowerRefGraph().GetYaxis().SetRangeUser(1-maxdiffrel*1.1,1+maxdiffrel*1.1)
        
        u=r1.GetUpperPad()
        u.SetLogy()
        d=r1.GetLowerPad()
        
        u.cd()
        h1.Draw("samehisto")
        h2.Draw("samehisto")
        d.cd()
        #d.GetYaxis().SetRangeUser(0,2)
        g2.SetMarkerStyle(0)
        g2.SetMarkerColorAlpha(ROOT.kGreen+2,0.9)
#        g2.SetLineColor(ROOT.kGreen+2)
        g2.SetLineColorAlpha(ROOT.kGreen+2,0.90)
        g2.Draw("P")
        
        c1.Print("nom_vs_syst_"+n+"_"+r+".png")
        c1.Clear()

        if(not doDoubleRatios): 
            f2.Close()
            f1.Close()
            fnom.Close()
            continue
        
      
        
        c1.SetLogy(0)
        
        
        
        print "checkpoint1"
        hnomf=copy.deepcopy(hnom)
        hnomf.Divide(hnom_I)
        hnomf.Draw("histo")
        print "checkpoint2"
        h1f=copy.deepcopy(h1)
        h2f=copy.deepcopy(h2)
        h1f.Divide(h1_I)
        h2f.Divide(h2_I)


        r3 = ROOT.TRatioPlot(hnomf,h1f)
        r4 = ROOT.TRatioPlot(hnomf,h2f)
        r4.Draw()
        g4 = r4.GetLowerRefGraph().Clone("g4")
        print "checkpoint3"
        r3.Draw()
#        r3.GetLowerRefGraph().SetLineColor(ROOT.kRed)
        r3.GetLowerRefGraph().SetLineColorAlpha(ROOT.kRed,1.0)
        r3.GetLowerRefGraph().SetMarkerColor(ROOT.kRed)
        r3.GetLowerRefGraph().GetYaxis().SetRangeUser(1-maxdiffrel,1+maxdiffrel)
        print "checkpoint4"
        u2=r3.GetUpperPad()
        u2.SetLogy()
        d2=r3.GetLowerPad()
        u2.cd()
        h1f.Draw("samehisto")
        h2f.Draw("samehisto")
        d2.cd()
        #d2.GetYaxis().SetRangeUser(0,2)
        g4.SetMarkerStyle(0)
        g4.SetMarkerColor(ROOT.kGreen+2)
#        g4.SetLineColor(ROOT.kGreen+2)
        g4.SetLineColorAlpha(ROOT.kGreen+2,1.0)
        g4.Draw("P")

        #        r1.Draw()
        c1.Print("nom_vs_syst_TF_"+n+"_"+r+".png")
        
        print f2
        f2.Close()
        f1.Close()
        fnom.Close()

#        print h1,h2,h1_I,h2_I,hnom,hnom_I

#noms.append([""])

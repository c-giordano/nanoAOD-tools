import ROOT
import math
import collections
import copy
from repos import namemap
from repos import wjets_veto_map as regions

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

fdir= "localhisto/test_new_nofitrange_v15/"
fdir= "localhisto/new_v15/"
fdir= "localhisto/new_tail_v16/"
fdir= '/eos/user/a/adeiorio/Wprime/nosynch/v17/plot_merged/'
fdir= '/eos/user/a/adeiorio/Wprime/nosynch/v17/plot_merged_explin_v3/'

years=["2020"]
#years=["2016","2017","2018"]
leptons=["muon","electron"]
postfix = ''
filesc=collections.OrderedDict()
#{"DDFitWJetsTT_MttST":ROOT.kViolet,"DDWJetsTT_MttST":ROOT.kGreen,"WJetsTT_MttST":ROOT.kRed,"tffile":ROOT.kBlue,"Data":ROOT.kBlack}
hsc={"DDFitWJetsTT_MttST":"DDFit","Data":"Data","WJetsTT_MttST":"MC","DDWJetsTT_MttST":"DDMC","tffile":"DDMC_MC"}

#filesc={"DDFitWJetsTT_MttST":ROOT.kViolet,"WJetsTT_MttST":ROOT.kRed,"Data":ROOT.kBlack}
filesc["Data"]=ROOT.kBlack
filesc["DDFitWJetsTT_MttST"]=ROOT.kViolet
#filesc["DDWJetsTT_MttST"]=ROOT.kRed
#filesc["WJetsTT_MttST"]=ROOT.kRed
#postfix="_DDvsData"
#filesc["WJetsTT_MttST"]=ROOT.kRed
#postfix="_MCvsData"

#filesc={"DDFitWJetsTT_MttST":ROOT.kViolet}
#hsc["DDFitUpWJetsTT_MttST"]="DDFitUp"
#hsc["DDFitDownWJetsTT_MttST"]="DDFitDown"

legnames={"DDFitWJetsTT_MttST":"DD: CR0B_I fit x TF #pm stat #pm syst ","Data":"Data CR0B","WJetsTT_MttST":"Pure MC: CR0B MC","tffile":"Pure MC: CR0B_I MC x TF","DDWJetsTT_MttST":"DD: CR0B_I subtraction x TF"}

regions_to_consider=["CR0B","CR1B","SR2B","SRT","SRWB",]
regions_blinded=["SR2B","SRT","SRW",]

nmultmc="WJetsTT_MttST_CR0B_over_CR0B_Imult_mc"

#fout=ROOT.TFile("histos.root")
c2 = ROOT.TCanvas("c2")
c1 = ROOT.TCanvas("c1")
#forregioname in namemap.iteritems():
for y in years:
    for l in leptons:
        for sr,cr in regions.iteritems():
            hname_sr=namemap[sr]
            hname_cr=namemap[cr]
            droption="ehisto "
            leg= ROOT.TLegend()
            legratio= ROOT.TLegend(0.45,0.73,0.87,0.87)
            histo_coll = {}
            for f,c in filesc.iteritems():
                if(sr in regions_blinded):
                    if f=="Data":
                        continue 
                if not  ("tffile" in f):
                    fnamee=(fdir+"/"+l+"/"+f+"_"+y+"_"+l+".root")
                    fil=ROOT.TFile(fnamee)
                else:
#                    fnamee=(f+"_"+y+"_"+l+".root").replace()
                    fil = ROOT.TFile(f+"_"+y+"_"+l+".root")
                hname=hname_sr
                if f=="WJetsTT_MttST":
                    hname=hname_sr
                if f=="tffile" :
                    hname=nmultmc.replace("CR0B",sr)
                h=fil.Get(hname)
                print "filename ",f," file ",fil," hname ",hname," histo ",h," color ",c," droption",droption
                h=fil.Get(hname).Clone(hsc[f])
                if("DDFit" in f):
                    filup=ROOT.TFile((fil.GetName()).replace(".root","_DD_"+y+"Up.root"))
                    fildown=ROOT.TFile(str(fil.GetName()).replace(".root","_DD_"+y+"Down.root"))
                    fil2up=ROOT.TFile((fil.GetName()).replace(".root","_WJetsUp.root"))
                    fil2down=ROOT.TFile(str(fil.GetName()).replace(".root","_WJetsDown.root"))
                    fil3up=ROOT.TFile((fil.GetName()).replace(".root","_TT_MttUp.root"))
                    fil3down=ROOT.TFile(str(fil.GetName()).replace(".root","_TT_MttDown.root"))
                    fil4up=ROOT.TFile((fil.GetName()).replace(".root","_STUp.root"))
                    fil4down=ROOT.TFile(str(fil.GetName()).replace(".root","_STDown.root"))
                    hup=filup.Get(hname).Clone(hsc[f]+"Up")
                    hdown=fildown.Get(hname).Clone(hsc[f]+"Down")
                    h2up=fil2up.Get(hname).Clone(hsc[f]+"WJetsUp")
                    h2down=fil2down.Get(hname).Clone(hsc[f]+"WJetsDown")
                    h3up=fil2up.Get(hname).Clone(hsc[f]+"TTUp")
                    h3down=fil2down.Get(hname).Clone(hsc[f]+"TTDown")
                    h4up=fil2up.Get(hname).Clone(hsc[f]+"STUp")
                    h4down=fil2down.Get(hname).Clone(hsc[f]+"STDown")
                h.SetLineColor(c)
                h.DrawNormalized(droption)
                #h.Draw(droption)
                if("DDFit" in f):
                    hup.SetLineColor(c-1)
                    hdown.SetLineColor(c-1)
                    h2up.SetLineColor(c-2)
                    h2down.SetLineColor(c-2)
                    h3up.SetLineColor(c-3)
                    h3down.SetLineColor(c-3)
                    h4up.SetLineColor(c-4)
                    h4down.SetLineColor(c-4)
                    hsumup=h.Clone("sumup")
                    hsumdown=h.Clone("sumdown")
                    for b in range(1,hsumup.GetNbinsX()+1):
                        b0=h.GetBinContent(b)
                        bincup= (hup.GetBinContent(b)-b0)**2
                        bincup= bincup+ (h2up.GetBinContent(b)-b0)**2
                        bincup= bincup+ (h3up.GetBinContent(b)-b0)**2
                        bincup= bincup+ (h4up.GetBinContent(b)-b0)**2

                        bincdown= (hdown.GetBinContent(b)-b0)**2
                        bincdown= bincdown +(h2down.GetBinContent(b)-b0)**2
                        bincdown= bincdown +(h3down.GetBinContent(b)-b0)**2
                        bincdown= bincdown +(h4down.GetBinContent(b)-b0)**2
                        h.SetBinError(b,(math.sqrt(bincup)+math.sqrt(bincdown))*0.5)
                        bincup=math.sqrt(bincup)+b0
                        bincdown=-math.sqrt(bincdown)+b0

                        hsumup.SetBinContent(b,bincup)
                        hsumdown.SetBinContent(b,bincdown)
                    h.DrawNormalized("esame")
                    hup.Scale(1/h.Integral())
                    hdown.Scale(1/h.Integral())
                    
                    h2up.Scale(1/h.Integral())
                    h2down.Scale(1/h.Integral())
                    h3up.Scale(1/h.Integral())
                    h3down.Scale(1/h.Integral())
                    h4up.Scale(1/h.Integral())
                    h4down.Scale(1/h.Integral())
                    hsumup.Scale(1/h.Integral())
                    hsumdown.Scale(1/h.Integral())
#                    hsumup.Draw("histo esame")
#                    hsumdown.Draw("histo esame")
#                    hup.DrawNormalized("histo same")
#                    hdown.DrawNormalized("histo same")
#                    h2up.DrawNormalized("histo same")
#                    h2down.DrawNormalized("histo same")
#                    h2up.DrawNormalized("histo same")
#                    h2down.DrawNormalized("histo same")
#                    h2up.DrawNormalized("histo same")
#                    h2down.DrawNormalized("histo same")
#                    h4up.Draw("histo same")
#                    h4down.Draw("histo same")
#                    h3up.Draw("histo same")
#                    h3down.Draw("histo same")
#                    h2up.Draw("histo same")
#                    h2down.Draw("histo same")
#                    hup.Draw("histo same")
#                    hdown.Draw("histo same")
                lname = legnames[f].replace("CR0B",sr)
                leg.AddEntry(h.GetName(),lname,"l")
                legratio.AddEntry(h.GetName(),lname,"l")
#                h.Draw(droption)
                histo_coll[f] = copy.deepcopy(h)
                droption="same ehist"
            leg.Draw()
            c1.SetLogy()
            extra=""
            if(sr in regions_blinded):
                extra="_no_data"
            c1.SaveAs("comparisons_"+sr+"_"+y+"_"+l+extra+postfix+".png")
            c2.cd()
            histo_coll["Data"].SetTitle(";W' mass [GeV]; Events")
            ratio = ROOT.TRatioPlot(histo_coll["Data"], histo_coll["DDFitWJetsTT_MttST"])
            #histo_coll["DDWJetsTT_MttST"].SetTitle(";W' mass [GeV]; Events")
            #ratio = ROOT.TRatioPlot(histo_coll["DDWJetsTT_MttST"], histo_coll["DDFitWJetsTT_MttST"])
            c2.SetLogy()
            ratio.Draw()
            legratio.Draw()
            #ratio.GetLowerRefYaxis().SetRangeUser(0,8)
            #ratio.GetLowerRefGraph().SetMaximum(4)
            c2.SetLogy()
            c2.Update()
            c2.Print("comparisons_"+sr+"_"+y+"_"+l+extra+postfix+"_ratio.png")

import os, commands
import sys
import optparse
import ROOT
import math
from variabile import variabile
from CMS_lumi import CMS_lumi
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from array import array

usage = 'python makeplot.py'
parser = optparse.OptionParser(usage)
parser.add_option('--merpart', dest='merpart', default = False, action='store_true', help='Default parts are not merged')
parser.add_option('--mertree', dest='mertree', default = False, action='store_true', help='Default make no file is merged')
parser.add_option('--lumi', dest='lumi', default = False, action='store_true', help='Default do not write the normalization weights')
parser.add_option('--sel', dest='sel', default = False, action='store_true', help='Default do not apply any selection')
parser.add_option('-p', '--plot', dest='plot', default = False, action='store_true', help='Default make no plots')
parser.add_option('-s', '--stack', dest='stack', default = False, action='store_true', help='Default make no stacks')
parser.add_option('-N', '--notstacked', dest='tostack', default = True, action='store_false', help='Default make plots stacked')
parser.add_option('-L', '--lep', dest='lep', type='string', default = 'muon', help='Default make muon analysis')
parser.add_option('-S', '--syst', dest='syst', type='string', default = 'all', help='Default all systematics added')
parser.add_option('-C', '--cut', dest='cut', type='string', default = 'lepton_eta>-10.', help='Default no cut')
parser.add_option('-y', '--year', dest='year', type='string', default = 'all', help='Default 2016, 2017 and 2018 are included')
parser.add_option('-f', '--folder', dest='folder', type='string', default = 'v6', help='Default folder is v0')
#parser.add_option('-T', '--topol', dest='topol', type='string', default = 'all', help='Default all njmt')
parser.add_option('-d', '--dat', dest='dat', type='string', default = 'all', help="")
(opt, args) = parser.parse_args()

folder = opt.folder

#filerepo = '/eos/user/a/apiccine/Wprime/nosynch/v13/'
filerepo = '/eos/user/'+str(os.environ.get('USER')[0])+'/'+str(os.environ.get('USER'))+'/Wprime/nosynch/' + folder + '/'
plotrepo = '/eos/user/'+str(os.environ.get('USER')[0])+'/'+str(os.environ.get('USER'))+'/Wprime/nosynch/' + folder + '/'#_topjet/'#/only_Wpjetbtag_ev1btag/'

ROOT.gROOT.SetBatch() # don't pop up canvases
if not os.path.exists(plotrepo + 'plot/muon'):
     os.makedirs(plotrepo + 'plot/muon')
if not os.path.exists(plotrepo + 'plot/electron'):
     os.makedirs(plotrepo + 'plot/electron')
if not os.path.exists(plotrepo + 'stack'):
     os.makedirs(plotrepo + 'stack')

def mergepart(dataset):
     samples = []
     if hasattr(dataset, 'components'): # How to check whether this exists or not
          samples = [sample for sample in dataset.components]# Method exists and was used.
     else:
          samples.append(dataset)
     for sample in samples:
          add = "hadd -f " + filerepo + sample.label + "/"  + sample.label + "_merged.root " + filerepo + sample.label + "/"  + sample.label + "_part*.root" 
          print add
          os.system(str(add))
          check = ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + "_merged.root ")
          print "Number of entries of the file %s are %s" %(filerepo + sample.label + "/"  + sample.label + "_merged.root", (check.Get("events_nominal")).GetEntries())
          #print "Number of entries of the file %s are %s" %(filerepo + sample.label + "/"  + sample.label + "_merged.root", (check.Get("events_all")).GetEntries())

def mergetree(sample):
     if not os.path.exists(filerepo + sample.label):
          os.makedirs(filerepo + sample.label)
     if hasattr(sample, 'components'): # How to check whether this exists or not
          add = "hadd -f " + filerepo + sample.label + "/"  + sample.label + ".root" 
          for comp in sample.components:
               add += " " + filerepo + comp.label + "/"  + comp.label + ".root" 
          print add
          os.system(str(add))

def lumi_writer(dataset, lumi):
     samples = []
     if hasattr(dataset, 'components'): # How to check whether this exists or not
          samples = [sample for sample in dataset.components]# Method exists and was used.
     else:
          samples.append(dataset)
     for sample in samples:
          if not ('Data' in sample.label or 'TT_dilep' in sample.label):
               infile =  ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + "_merged.root")
               tree = infile.Get('events_nominal')
               treejesup = infile.Get('events_jesUp')
               treejesdown = infile.Get('events_jesDown')
               treejerup = infile.Get('events_jerUp')
               treejerdown = infile.Get('events_jerDown')
               tree.SetBranchStatus('w_nominal', 0)
               tree.SetBranchStatus('w_PDF', 0)
               treejesup.SetBranchStatus('w_nominal', 0)
               treejesdown.SetBranchStatus('w_nominal', 0)
               treejerup.SetBranchStatus('w_nominal', 0)
               treejerdown.SetBranchStatus('w_nominal', 0)
               outfile = ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + ".root","RECREATE")
               tree_new = tree.CloneTree(0)
               treejesup_new = treejesup.CloneTree(0)
               treejesdown_new = treejesdown.CloneTree(0)
               treejerup_new = treejerup.CloneTree(0)
               treejerdown_new = treejerdown.CloneTree(0)
               tree.SetBranchStatus('w_nominal', 1)
               tree.SetBranchStatus('w_PDF', 1)
               treejesup.SetBranchStatus('w_nominal', 1)
               treejesdown.SetBranchStatus('w_nominal', 1)
               treejerup.SetBranchStatus('w_nominal', 1)
               treejerdown.SetBranchStatus('w_nominal', 1)
               print("Getting the histos from %s" %(infile))
               h_genw_tmp = ROOT.TH1F(infile.Get("h_genweight"))
               h_pdfw_tmp = ROOT.TH1F(infile.Get("h_PDFweight"))
               nbins = h_pdfw_tmp.GetXaxis().GetNbins()
               print("h_genweight first bin content is %f and h_PDFweight has %f bins" %(h_genw_tmp.GetBinContent(1), nbins))
               w_nom = array('f', [0.]) 
               w_nomjesup = array('f', [0.]) 
               w_nomjesdown = array('f', [0.]) 
               w_nomjerup = array('f', [0.]) 
               w_nomjerdown = array('f', [0.]) 
               w_PDF = array('f', [0.]*nbins)
               print(nbins)
               print(len(w_PDF))
               tree_new.Branch('w_nominal', w_nom, 'w_nominal/F')
               tree_new.Branch('w_PDF', w_PDF, 'w_PDF/F')
               treejesup_new.Branch('w_nominal', w_nomjesup, 'w_nominal/F')
               treejesdown_new.Branch('w_nominal', w_nomjesdown, 'w_nominal/F')
               treejerup_new.Branch('w_nominal', w_nomjerup, 'w_nominal/F')
               treejerdown_new.Branch('w_nominal', w_nomjerdown, 'w_nominal/F')
               for event in xrange(0, tree.GetEntries()):
                    tree.GetEntry(event)
                    if event%10000==1:
                         #print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                         sys.stdout.write("\rProcessing event {}     complete {} percent".format(event, 100*event/tree.GetEntries()))
                    w_nom[0] = tree.w_nominal * sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    for i in xrange(1, nbins):
                         w_PDF[i] = h_pdfw_tmp.GetBinContent(i+1)/h_genw_tmp.GetBinContent(2) 
                    tree_new.Fill()
               outfile.cd()
               tree_new.Write()
               infile.cd()
               for event in xrange(0, treejesup.GetEntries()):
                    treejesup.GetEntry(event)
                    if event%10000==1:
                         #print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                         sys.stdout.write("\rProcessing event {}     complete {} percent".format(event, 100*event/treejesup.GetEntries()))
                    w_nomjesup[0] = treejesup.w_nominal * sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    treejesup_new.Fill()
               outfile.cd()
               treejesup_new.Write()
               infile.cd()
               for event in xrange(0, treejesdown.GetEntries()):
                    treejesdown.GetEntry(event)
                    if event%10000==1:
                         #print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                         sys.stdout.write("\rProcessing event {}     complete {} percent".format(event, 100*event/treejesdown.GetEntries()))
                    w_nomjesdown[0] = treejesdown.w_nominal * sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    treejesdown_new.Fill()
               outfile.cd()
               treejesdown_new.Write()
               infile.cd()
               for event in xrange(0, treejerup.GetEntries()):
                    treejerup.GetEntry(event)
                    if event%10000==1:
                         #print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                         sys.stdout.write("\rProcessing event {}     complete {} percent".format(event, 100*event/treejerup.GetEntries()))
                    w_nomjerup[0] = treejerup.w_nominal * sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    treejerup_new.Fill()
               outfile.cd()
               treejerup_new.Write()
               infile.cd()
               for event in xrange(0, treejerdown.GetEntries()):
                    treejerdown.GetEntry(event)
                    if event%10000==1:
                         #print("Processing event %s     complete %s percent" %(event, 100*event/tree.GetEntries()))
                         sys.stdout.write("\rProcessing event {}     complete {} percent".format(event, 100*event/treejerdown.GetEntries()))
                    w_nomjerdown[0] = treejerdown.w_nominal * sample.sigma * lumi * 1000./float(h_genw_tmp.GetBinContent(1))
                    treejerdown_new.Fill()
               outfile.cd()
               treejerdown_new.Write()
               outfile.Close()
               print('\n')
          else:
               os.popen("mv " + filerepo + sample.label + "/"  + sample.label + "_merged.root " + filerepo + sample.label + "/"  + sample.label + ".root")

def cutToTag(cut):
    newstring = cut.replace("-", "neg").replace(">=","_GE_").replace(">","_G_").replace(" ","").replace("&&","_AND_").replace("||","_OR_").replace("<=","_LE_").replace("<","_L_").replace(".","p").replace("(","").replace(")","").replace("==","_EQ_").replace("!=","_NEQ_").replace("=","_EQ_").replace("*","_AND_").replace("+","_OR_")
    return newstring

def plot(lep, reg, variable, sample, cut_tag, syst):
     print "plotting ", variable._name, " for sample ", sample.label, " with cut ", cut_tag, " ", syst,
     ROOT.TH1.SetDefaultSumw2()
     f1 = ROOT.TFile.Open(filerepo + sample.label + "/"  + sample.label + ".root")
     treename = "events_nominal"
     if(cut_tag == ""):
          if variable._name=='WprAK8_tau2/WprAK8_tau1':
               histoname = "h_" + reg + "_WprAK8_tau21"
          elif variable._name== 'WprAK8_tau3/WprAK8_tau2':
               histoname =  "h_" + reg + "_WprAK8_tau32"
          else:
               histoname = "h_" + reg + "_" + variable._name
     else:
          if variable._name=='WprAK8_tau2/WprAK8_tau1':
               histoname = "h_" + reg + "_WprAK8_tau21_" + cut_tag
          elif variable._name== 'WprAK8_tau3/WprAK8_tau2':
               histoname =  "h_" + reg + "_WprAK8_tau32_" + cut_tag
          else:
               histoname = "h_" + reg + "_" + variable._name + "_" + cut_tag
     nbins = 0
     h1 = ROOT.TH1F()
     if variable._nbins == None:
          nbins = len(variable._xarray)-1
          h1 = ROOT.TH1F(histoname, variable._name + "_" + reg, nbins, variable._xarray)
     else:
          nbins = variable._nbins
          h1 = ROOT.TH1F(histoname, variable._name + "_" + reg, variable._nbins, variable._xmin, variable._xmax)
     h1.Sumw2()
     if 'muon' in lep: 
          cut = variable._taglio + '*isMu'
     elif 'electron' in lep:
          cut  = variable._taglio + '*isEle'
          if 'MC' in variable._name:
               cut = cut + "*(" + str(variable._name) + "!=-100.)"
     print str(cut)
     foutput = plotrepo + "plot/" + lep + "/" + sample.label + "_" + lep+".root"
     if not 'Data' in sample.label: 
          if(syst.startswith("jer") or syst.startswith("jes")):
               treename = "events_"+syst
               foutput = plotrepo + "plot/" + lep + "/" + sample.label + "_" + lep + "_" + syst + ".root"
          elif(syst == ""):
               foutput = plotrepo + "plot/" + lep + "/" + sample.label + "_" + lep + ".root"
          else:
               foutput = plotrepo + "plot/" + lep + "/" + sample.label + "_" + lep + "_" + syst + ".root"
               cut += '*'+syst
     #print treename
     f1.Get(treename).Project(histoname,variable._name,cut)
     #if not 'Data' in sample.label:
     #     h1.Scale((7.5)/35.89)
     #h1.SetBinContent(1, h1.GetBinContent(0) + h1.GetBinContent(1))
     #h1.SetBinError(1, math.sqrt(pow(h1.GetBinError(0),2) + pow(h1.GetBinError(1),2)))
     h1.SetBinContent(nbins, h1.GetBinContent(nbins) + h1.GetBinContent(nbins+1))
     h1.SetBinError(nbins, math.sqrt(pow(h1.GetBinError(nbins),2) + pow(h1.GetBinError(nbins+1),2)))
     for i in range(0, nbins+1):
          content = h1.GetBinContent(i)
          if(content<0.):
               h1.SetBinContent(i, 0.)
     fout = ROOT.TFile.Open(foutput, "UPDATE")
     fout.cd()
     h1.Write()
     fout.Close()
     f1.Close()

def makestack(lep_, reg_, variabile_, samples_, cut_tag_, syst_, lumi):
     os.system('set LD_PRELOAD=libtcmalloc.so')
     if variabile_._name=='WprAK8_tau2/WprAK8_tau1':
          variabile_._name = 'WprAK8_tau21' 
     elif variabile_._name== 'WprAK8_tau3/WprAK8_tau2':
          variabile_._name = 'WprAK8_tau32'
     infile = {}
     histo = []
     tmp = ROOT.TH1F()
     h = ROOT.TH1F()
     hdata = ROOT.TH1F()
     nbins = 0
     xmin = 0.
     xmax = 100.
     if variabile_._nbins == None:
          nbins = len(variabile_._xarray)-1
          hdata = ROOT.TH1F('h','h', nbins, variabile_._xarray)
          xmin = variabile_._xarray[0]
          xmax = variabile_._xarray[-1]
     else:
          nbins = variabile_._nbins
          hdata = ROOT.TH1F('h','h', variabile_._nbins, variabile_._xmin, variabile_._xmax)
          xmin = variabile_._xmin
          xmax = variabile_._xmax
     h_sig = []
     h_err = ROOT.TH1F()
     h_bkg_err = ROOT.TH1F()
     blind = False
     print "Variabile:", variabile_._name
     ROOT.gROOT.SetStyle('Plain')
     ROOT.gStyle.SetPalette(1)
     ROOT.gStyle.SetOptStat(0)
     ROOT.TH1.SetDefaultSumw2()
     if(cut_tag_ == ""):
          histoname = "h_" + reg_ + "_" + variabile_._name
          stackname = "stack_" + reg_ + "_" + variabile_._name
          canvasname = "stack_" + reg_ + "_" + variabile_._name + "_" + lep_ + "_" + str(samples_[0].year)
     else:
          histoname = "h_"+reg_+"_"+variabile_._name+"_"+cut_tag_
          stackname = "stack_"+reg_+"_"+variabile_._name+"_"+cut_tag_
          canvasname = "stack_"+reg_+"_"+variabile_._name+"_"+cut_tag_+"_"+lep_ + "_" + str(samples_[0].year)
     if("selection_AND_best_Wpjet_isbtag_AND_best_topjet_isbtag" in cut_tag_ ) or ("selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag" in cut_tag_ ) or  ("selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag" in cut_tag_ ):
          blind = True
     if("selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_" in cut_tag_ ):
          blind = False
     stack = ROOT.THStack(stackname, variabile_._name)
     leg_stack = ROOT.TLegend(0.33,0.62,0.91,0.87)
     signal = False

     print samples_
     for s in samples_:
          if('WP' in s.label):
               signal = True
          if(syst_ == ""):
               outfile = plotrepo + "stack_" + str(lep_).strip('[]') + ".root"
               infile[s.label] = ROOT.TFile.Open(plotrepo + "plot/" + lep + "/" + s.label + "_" + lep + ".root")
          else:
               outfile = plotrepo + "stack_"+syst_+"_"+str(lep_).strip('[]')+".root"
               infile[s.label] = ROOT.TFile.Open(plotrepo + "plot/" + lep + "/" + s.label + "_" + lep + "_" + syst_ + ".root")
     i = 0

     for s in samples_:
          infile[s.label].cd()
          print "opening file: ", infile[s.label].GetName()
          if('Data' in s.label):
               if ("GenPart" in variabile_._name) or ("MC_" in variabile_._name):
                    continue
          tmp = (ROOT.TH1F)(infile[s.label].Get(histoname))
          tmp.SetLineColor(ROOT.kBlack)
          tmp.SetName(s.leglabel)
          if('Data' in s.label):
               if ("GenPart" in variabile_._name) or ("MC_" in variabile_._name):
                    continue
               hdata.Add(ROOT.TH1F(tmp.Clone("")))
               hdata.SetMarkerStyle(20)
               hdata.SetMarkerSize(0.9)
               if(i == 0 and not blind): # trick to add Data flag to legend only once
                    leg_stack.AddEntry(hdata, "Data", "ep")
               i += 1
          elif('WP' in s.label):
               #tmp.SetLineStyle(9)
               if opt.tostack:
                    tmp.SetLineColor(s.color)
               else:
                    tmp.SetLineColor(s.color)
               #tmp.SetLineWidth(3)
               tmp.SetMarkerSize(0.)
               tmp.SetMarkerColor(s.color)
               h_sig.append(ROOT.TH1F(tmp.Clone("")))
          else:
               tmp.SetOption("HIST SAME")
               tmp.SetTitle("")
               if opt.tostack:
                    tmp.SetFillColor(s.color)
               else:
                    tmp.SetLineColor(s.color)
               histo.append(tmp.Clone(""))
               stack.Add(tmp.Clone(""))
          tmp.Reset("ICES")
     for hist in reversed(histo):
          if not ('Data' in hist.GetName()):
               leg_stack.AddEntry(hist, hist.GetName(), "f")
     #style options
     print "Is it blind? " + str(blind)
     leg_stack.SetNColumns(2)
     leg_stack.SetFillColor(0)
     leg_stack.SetFillStyle(0)
     leg_stack.SetTextFont(42)
     leg_stack.SetBorderSize(0)
     leg_stack.SetTextSize(0.05)
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
     c1.cd()

     pad1= ROOT.TPad("pad1", "pad1", 0, 0.31 , 1, 1)
     pad1.SetTopMargin(0.1)
     pad1.SetBottomMargin(0.02)
     pad1.SetLeftMargin(0.12)
     pad1.SetRightMargin(0.05)
     pad1.SetBorderMode(0)
     pad1.SetTickx(1)
     pad1.SetTicky(1)
     pad1.Draw()
     pad1.cd()
     if not blind:
          maximum = max(stack.GetMaximum(),hdata.GetMaximum())
     else:
          maximum = stack.GetMaximum()
     logscale = True # False #
     if(logscale):
          pad1.SetLogy()
          stack.SetMaximum(maximum*1000)
     else:
          stack.SetMaximum(maximum*1.6)
     stack.SetMinimum(0.01)
     if opt.tostack:
          stack.Draw("HIST")
     else:
          stack.Draw("HIST NOSTACK")
     if variabile_._nbins == None:
          ytitle = "Events / bin width"
     else:
          step = float(variabile_._xmax - variabile_._xmin)/float(variabile_._nbins)
          print str(step)
          if "GeV" in variabile_._title:
               if step.is_integer():
                    ytitle = "Events / %.0f GeV" %step
               else:
                    ytitle = "Events / %.2f GeV" %step
          else:
               if step.is_integer():
                    ytitle = "Events / %.0f units" %step
               else:
                    ytitle = "Events / %.2f units" %step
     stack.GetYaxis().SetTitle(ytitle)
     stack.GetYaxis().SetTitleFont(42)
     stack.GetXaxis().SetLabelOffset(1.8)
     stack.GetYaxis().SetTitleOffset(0.85)
     stack.GetXaxis().SetLabelSize(0.15)
     stack.GetYaxis().SetLabelSize(0.07)
     stack.GetYaxis().SetTitleSize(0.07)
     stack.SetTitle("")
     if(signal):
          for hsig in h_sig:
               #hsig.Scale(1000)
               hsig.Draw("same")
               leg_stack.AddEntry(hsig, hsig.GetName(), "l")
     h_err = stack.GetStack().Last().Clone("h_err")
     h_err.SetLineWidth(100)
     h_err.SetFillStyle(3154)
     h_err.SetMarkerSize(0)
     h_err.SetFillColor(ROOT.kGray+2)
     h_err.Draw("e2same0")
     leg_stack.AddEntry(h_err, "Stat. Unc.", "f")
     if not blind: 
          print(hdata.Integral())
          hdata.Draw("eSAMEpx0")
     else:
          hdata = stack.GetStack().Last().Clone("h_data")
     leg_stack.Draw("same")

     CMS_lumi.writeExtraText = 1
     CMS_lumi.extraText = ""
     if str(lep_).strip('[]') == "muon":
          lep_tag = "#mu+"
     elif str(lep_).strip('[]') == "electron":
          lep_tag = "e+"
          
     lumi_sqrtS = "%s fb^{-1}  (13 TeV)"%(lumi)
     
     iPeriod = 0
     iPos = 11
     CMS_lumi(pad1, lumi_sqrtS, iPos, lep_tag+str(reg_))
     hratio = stack.GetStack().Last()
     
     c1.cd()
     pad2= ROOT.TPad("pad2", "pad2", 0, 0.01 , 1, 0.30)
     pad2.SetTopMargin(0.05)
     pad2.SetBottomMargin(0.45)
     pad2.SetLeftMargin(0.12)
     pad2.SetRightMargin(0.05)
     ROOT.gStyle.SetHatchesSpacing(2)
     ROOT.gStyle.SetHatchesLineWidth(2)
     c1.cd()
     pad2.Draw()
     pad2.cd()
     ratio = hdata.Clone("ratio")
     ratio.SetLineColor(ROOT.kBlack)
     ratio.SetMaximum(2)
     ratio.SetMinimum(0)
     ratio.Sumw2()
     ratio.SetStats(0)
     
     ratio.Divide(hratio)
     ratio.SetMarkerStyle(20)
     ratio.SetMarkerSize(0.9)
     ratio.Draw("epx0e0")
     ratio.SetTitle("")
     
     h_bkg_err = hratio.Clone("h_err")
     h_bkg_err.Reset()
     h_bkg_err.Sumw2()
     for i in range(1,hratio.GetNbinsX()+1):
          h_bkg_err.SetBinContent(i,1)
          if(hratio.GetBinContent(i)):
               h_bkg_err.SetBinError(i, (hratio.GetBinError(i)/hratio.GetBinContent(i)))
          else:
               h_bkg_err.SetBinError(i, 10^(-99))
     h_bkg_err.SetLineWidth(100)

     h_bkg_err.SetMarkerSize(0)
     h_bkg_err.SetFillColor(ROOT.kGray+1)
     h_bkg_err.Draw("e20same")
     
     f1 = ROOT.TLine(xmin, 1., xmax,1.)
     f1.SetLineColor(ROOT.kBlack)
     f1.SetLineStyle(ROOT.kDashed)
     f1.Draw("same")
     
     ratio.GetYaxis().SetTitle("Data / MC")
     ratio.GetYaxis().SetNdivisions(503)
     ratio.GetXaxis().SetLabelFont(42)
     ratio.GetYaxis().SetLabelFont(42)
     ratio.GetXaxis().SetTitleFont(42)
     ratio.GetYaxis().SetTitleFont(42)
     ratio.GetXaxis().SetTitleOffset(1.1)
     ratio.GetYaxis().SetTitleOffset(0.35)
     ratio.GetXaxis().SetLabelSize(0.15)
     ratio.GetYaxis().SetLabelSize(0.15)
     ratio.GetXaxis().SetTitleSize(0.16)
     ratio.GetYaxis().SetTitleSize(0.16)
     ratio.GetYaxis().SetRangeUser(0.,2.0)
     ratio.GetXaxis().SetTitle(variabile_._title)
     ratio.GetXaxis().SetLabelOffset(0.04)
     ratio.GetYaxis().SetLabelOffset(0.02)
     ratio.Draw("epx0e0same")

     c1.cd()
     #ROOT.TGaxis.SetMaxDigits(3)
     c1.RedrawAxis()
     pad2.RedrawAxis()
     c1.Update()
     c1.Print(plotrepo + "stack/"+canvasname+".png")
     c1.Print(plotrepo + "stack/"+canvasname+".pdf")
     del histo
     tmp.Delete()
     h.Delete()
     del tmp
     del h
     del h_sig
     h_err.Delete()
     del h_err
     h_bkg_err.Delete()
     del h_bkg_err
     hratio.Delete()
     del hratio
     stack.Delete()
     del stack
     pad1.Delete()
     del pad1
     pad2.Delete()
     del pad2
     c1.Delete()
     del c1
     for s in samples_:
          infile[s.label].Close()
          infile[s.label].Delete()
     os.system('set LD_PRELOAD=libtcmalloc.so')

dataset_dict = {'2016':[],'2017':[],'2018':[]}
if(opt.dat!= 'all'):
     if not(opt.dat in sample_dict.keys()):
          print sample_dict.keys()
     dataset_names = map(str, opt.dat.strip('[]').split(','))
     #print dataset_names.keys()
     samples = []
     [samples.append(sample_dict[dataset_name]) for dataset_name in dataset_names]
     [dataset_dict[str(sample.year)].append(sample) for sample in samples]
else:
     dataset_dict = {
          '2016':[DataMu_2016, DataEle_2016, DataHT_2016, ST_2016, QCD_2016, TT_Mtt_2016, WJets_2016, WP_M2000W20_RH_2016, WP_M3000W30_RH_2016, WP_M4000W40_RH_2016, WP_M5000W50_RH_2016, WP_M6000W60_RH_2016],
          #'2016':[DataHTG_2016, DataMuG_2016, ST_2016, QCD_2016, TT_Mtt_2016, WJets_2016, WP_M2000W20_RH_2016, WP_M3000W30_RH_2016, WP_M4000W40_RH_2016, WP_M4000W400_RH_2016],
          #'2017':[DataMu_2017, DataEle_2017, DataHT_2017, ST_2017, QCD_2017, TT_Mtt_2017, WJets_2017, WP_M2000W20_RH_2017, WP_M3000W30_RH_2017, WP_M4000W40_RH_2017, WP_M4000W400_RH_2017],
          '2017':[DataMu_2017, DataEle_2017, DataPh_2017, DataHT_2017, ST_2017, QCD_2017, TT_Mtt_2017, WJets_2017, WP_M2000W20_RH_2017, WP_M3000W30_RH_2017, WP_M4000W40_RH_2017, WP_M5000W50_RH_2017, WP_M6000W60_RH_2017],
          '2018':[DataMu_2018, DataEle_2018, DataHT_2018, ST_2018, QCD_2018, TT_Mtt_2018, WJets_2018, WP_M2000W20_RH_2018, WP_M3000W30_RH_2018, WP_M4000W40_RH_2018, WP_M5000W50_RH_2018, WP_M6000W60_RH_2018],
     }
#print(dataset_dict.keys())

years = []
if(opt.year!='all'):
     years = map(str,opt.year.strip('[]').split(','))
else:
     years = ['2016','2017','2018']
print(years)

leptons = map(str,opt.lep.split(',')) 

cut = opt.cut #default cut must be obvious, for example lepton_eta>-10.
if opt.cut == "lepton_eta>-10." and not opt.sel:
     cut_dict = {'muon':"lepton_pt>55", #&&MET_pt>80",#&&best_topjet_isbtag==0&&best_Wpjet_isbtag==1&&nbjet_pt100==1", 
                 'electron':"lepton_pt>50&&abs(lepton_eta)<2.2"#&&MET_pt>80"#&&best_topjet_isbtag==0&&best_Wpjet_isbtag==1&&nbjet_pt100==1",
     }
     cut_tag = ""
else:
     if opt.sel:
          cut_dict = {'muon':"MET_pt>120&&lepton_pt>55&&leadingjet_pt>300&&subleadingjet_pt>150&&" + cut, 
                      'electron':"MET_pt>120&&lepton_pt>50&&leadingjet_pt>300&&subleadingjet_pt>150&&abs(lepton_eta)<2.2&&" + cut
          }
          #cut_dict = {'muon':"MET_pt>120&&lepton_pt>180&&leadingjets_pt>350&&best_top_pt>250&&" + cut, 
          #            'electron':"MET_pt>120&&lepton_pt>180&&leadingjets_pt>350&&best_top_pt>250&&" + cut
          #}
          if opt.cut != "lepton_eta>-10.":
               cut_tag = 'selection_AND_' + cutToTag(opt.cut) 
          else:
               cut_tag = 'selection' 
     else:
          cut_dict = {'muon':cut, 'electron':cut}
          cut_tag = cutToTag(opt.cut)

lumi = {'2016': 35.9, "2017": 41.53, "2018": 59.7}

#
systematics = []
if opt.syst!="all" and opt.syst!="noSyst":
     for syst in (opt.syst).split(","):
          systematics.append(syst)
elif opt.syst!="all" and opt.syst=="noSyst":
    systematics.append("") #di default per syst="" alla variabile si applica il peso standard incluso nella macro macro_plot.C
else:
     systematics = ["", "jesUp",  "jesDown",  "jerUp",  "jerDown", "PFUp", "PFDown", "puUp", "puDown", "btagUp", "btagDown", "mistagUp", "mistagDown", "lepUp", "lepDown", "trigUp", "trigDown", "pdf_totalUp", "pdf_totalDown", "q2Up", "q2Down"]

for year in years:
     for sample in dataset_dict[year]:
          if(opt.merpart):
               mergepart(sample)
          if(opt.lumi):
               lumi_writer(sample, lumi[year])
          if(opt.mertree):
               if not('WP' in sample.label):
                    mergetree(sample)

for year in years:
     for lep in leptons:
          dataset_new = dataset_dict[year]
          #if lep == 'muon' and sample_dict['DataEle_'+str(year)] in dataset_new:
               #dataset_new.remove(sample_dict['DataEle_'+str(year)])
          #elif lep == 'electron' and sample_dict['DataMu_'+str(year)] in dataset_new:
               #dataset_new.remove(sample_dict['DataMu_'+str(year)])
          variables = []
          wzero = 'w_nominal*PFSF*puSF*lepSF*trigSF*btagSF'
          cut = cut_dict[lep]
          variables.append(variabile('njet_pt100', 'no. of jets with p_{T} > 100 GeV',  wzero+'*('+cut+')', 8, 1.5, 9.5))
          variables.append(variabile('nbjet_pt100', 'no. of b jets with p_{T} > 100 GeV',  wzero+'*('+cut+')', 7, -0.5, 6.5))
          variables.append(variabile('leadingjet_pt', 'leading jet p_{T} [GeV]',  wzero+'*('+cut+')', None, None, None,  array('f', [300., 350., 400., 480., 560., 650., 740., 840., 940., 1050., 1200., 1350., 1500., 1650., 1800., 1950., 2100., 2300.])))
          variables.append(variabile('subleadingjet_pt', 'subleading jet p_{T} [GeV]',  wzero+'*('+cut+')', None, None, None,  array('f', [150., 180., 230, 280., 340., 400., 480., 560., 650., 740., 840., 940., 1050., 1200., 1350., 1500., 1650., 1800.])))

          for sample in dataset_new:
               if(opt.plot):
                    for syst in systematics:
                         for var in variables:
                              if (("GenPart" in var._name) or ("MC_" in var._name)) and "Data" in sample.label:
                                   continue
                              plot(lep, 'jets', var, sample, cut_tag, syst)
          if(opt.stack):
               #for syst in systematics:
               for var in variables:
                    os.system('set LD_PRELOAD=libtcmalloc.so')
                    makestack(lep, 'jets', var, dataset_new, cut_tag, "", lumi[str(year)])
                    os.system('set LD_PRELOAD=libtcmalloc.so')
          #if lep == 'muon':
               #dataset_new.append(sample_dict['DataEle_'+str(year)])
          #elif lep == 'electron':
               #dataset_new.append(sample_dict['DataMu_'+str(year)])
          

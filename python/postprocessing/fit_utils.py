### Decorrelate Q2 syst among the processes
import sys
import os, commands
import shutil
#from samples.toPlot import samples
import optparse
import ROOT
import copy

def shift(h, ib, shift, slabel, channel, v):
    corr = 1
    if(shift == "Down"): corr = -1
    oh = 0.
    eoh = 0.
   # nhName = ""
    oh = h.GetBinContent(ib)
    eoh = h.GetBinError(ib)
    oh += eoh * corr
    if(oh<0.): # per i WJets ci sono problemi di underflow... questo puo evitarlo
        oh=0
    #print "++ Bin 1: ", h.GetAt(ib)
    #print "++ W Bin 1: ", h.GetBinError(ib)
    nh = copy.deepcopy(h)
    nh.SetAt(oh, ib)
    #print "++ nh Bin 1: ", nh.GetBinContent(ib)
    #print "---- Old name: ",h.GetName()
    if ch == "electron": 
        nhName = h.GetName() + "_mcstat_" + varE[v] + "_" + slabel+"_bin"+str(ib)+"_"+shift
    elif ch == "muon": 
        nhName = h.GetName() + "_mcstat_" + var[v] + "_" + slabel+"_bin"+str(ib)+"_"+shift
    nh.SetName(nhName)
    print "---- New name: ",nh.GetName()
    #nh.GetSumw2().SetAt(X, ib)
    return nh

def smoothing(filename,h):
    fin = ROOT.TFile(filename, "UPDATE")
    tmp = ROOT.TH1F()
    fin.cd()
    tmp = fin.Get(h)
    tmp.Smooth(8)
    for i in range(tmp.GetNbinsX()+1):
        if(tmp.GetBinContent(i)<=0):
            tmp.SetBinContent(i,0.0000001)
    tmp.Write()
    fin.Close()

def scale(f, shift):
    prev_str = ""
    fin = ROOT.TFile(f,"UPDATE")
    tmp = ROOT.TH1F()
    for k, o in getall(fin):
        #    print o.ClassName(), k
        if(prev_str != k):
            fin.cd()
            tmp = fin.Get(k)
            tmp.Scale(1+shift)
            tmp.Write()
            tmp.Reset("ICES")
        prev_str = k
    fin.Close()

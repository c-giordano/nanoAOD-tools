import ROOT
import os
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import copy
import math

masses_narrow = [x for x in range(2000, 6100, 200)]
print masses_narrow

chiralities = []
chiralities.append("LHSMinter")
chiralities.append("RH")
chiralities.append("LRSMinter")

samples = []
nstep = 10
aLs = [float(x)/nstep for x in range(1, nstep)]
print(aLs)
aRs = [float(x)/nstep for x in range(1, nstep)]
print(aRs)

ROOT.TH1.SetDefaultSumw2()
folder = 'v18'
plotrepo = '/eos/user/'+str(os.environ.get('USER')[0])+'/'+str(os.environ.get('USER'))+'/Wprime/nosynch/' + folder + '/plot_merged'
histonames = ["h_jets_best_Wprime_m_SR2B", "h_jets_best_Wprime_m_SRT", "h_jets_best_Wprime_m_SRW", "h_jets_best_Wprime_m_CR0B"]

years = ['2020']

for year in years:
    for mass in masses_narrow:
        for lep in ['muon', 'electron']:
            h = ROOT.TH1F()
            for aL in aLs:
                #for aR in aRs:
                aR = math.sqrt(1 - aL**2)
                for hname in histonames:
                    fsch = ROOT.TFile.Open(plotrepo + lep + "/ST_sch_" + year + "_" + lep + ".root")
                    h.Add(fsch.Get(hname).Clone(), (1-aL**2)-(2*aL**2*aR**2)/(aL**2+aR**2))
                    flh = ROOT.TFile.Open(plotrepo + lep + '/WP_M'+str(mass) + 'W'+str(int(width)) + "_LHSMinter_" + year + "_" + lep + ".root")
                    h.Add(flh.Get(hname).Clone(), aL**2*(aL**2-aR**2)/(aL**2+aR**2))
                    flr = ROOT.TFile.Open(plotrepo + lep + '/WP_M'+str(mass) + 'W'+str(int(width)) + "_LRSMinter_" + year + "_" + lep + ".root")
                    h.Add(flr.Get(hname).Clone(), 4*aL**2*aR**2/(aL**2+aR**2))
                    frh = ROOT.TFile.Open(plotrepo + lep + '/WP_M'+str(mass) + 'W'+str(int(width)) + "_RH_" + year + "_" + lep + ".root")
                    h.Add(frh.Get(hname).Clone(), aR**2*(aR**2-aL**2)/(aL**2+aR**2))
                fout = plotrepo + lep + '/WP_M'+str(mass) + 'W'+str(int(width)) + "_aL_" + aL + "_" + year + "_" + lep + ".root"
                h.Write("", ROOT.TObject.kOverwrite)
                

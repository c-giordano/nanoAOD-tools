import ROOT
import array
import os
ROOT.gROOT.SetBatch()
infile = ROOT.TFile.Open("root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv7/Wprimetotb_M6000W600_RH_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/260000/E12988B6-429A-8543-8BCC-AA3C52D09028.root")

file_list = ["root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleMuon/NANOAOD/02Apr2020-v1/250000/606B900C-D8B7-294B-94DE-2A413E3EED3F.root", "root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleMuon/NANOAOD/02Apr2020-v1/30000/8C3F8917-63E3-AA41-9CD2-F6DB7247DA61.root", "root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleMuon/NANOAOD/02Apr2020-v1/30000/B3EBEFC9-97AF-F144-B7CD-BE350383BAE0.root", "root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleMuon/NANOAOD/02Apr2020-v1/30000/0B246ED0-3831-1F4C-87BF-057C43759F25.root", "root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleMuon/NANOAOD/02Apr2020-v1/30000/4A3643EB-147B-A34D-9F16-34F30878B1B7.root", "root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleMuon/NANOAOD/02Apr2020-v1/250000/4366DB9A-7E56-8845-8559-CDC570CE245E.root", "root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleMuon/NANOAOD/02Apr2020-v1/30000/FF16BFC3-E997-904E-9C11-C0BDC2E8B06C.root", "root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleMuon/NANOAOD/02Apr2020-v1/30000/B837A527-32CB-1240-94EE-69B6F5AC10BE.root"]

tree = ROOT.TChain('Events')
for infile in file_list: 
    print("Adding %s to the chain" %(infile))
    tree.Add(infile)

def plot(histo):
    plotpath = '/eos/user/'+str(os.environ.get('USER')[0])+'/'+str(os.environ.get('USER'))+'/Wprime/nosynch/highpt/plot1D/'
    c = ROOT.TCanvas('Wprimetotb_M6000W600_RH_2016_' + histo.GetName(), 'Wprimetotb_M6000W600_RH_2016_' + histo.GetName())
    c.Draw()
    maximum = histo.GetMaximum()
    histoname = histo.GetName()
    histo.SetMinimum(0.)
    histo.Draw()
    histo.SetMaximum(1.05)
    c.SetLogx()
    c.Print(plotpath + c.GetName() + '.png')
    c.Print(plotpath + c.GetName() + '.pdf')
    c.Print(plotpath + c.GetName() + '.root')

#def write(filename, num, den, eff):
def write(filename, eff):
    outfile = ROOT.TFile(filename, "UPDATE")
    outfile.cd()
    #num.Write()
    #den.Write()
    eff.Write()
    outfile.Close()

#tree = infile.Get("Events")

cut_str = ''
cut_str_highpt = ''
print(tree.GetEntries())
LHE = "abs(LHEPart_pdgId[4])==13"
#cut_str += LHE
#cut_str_highpt += LHE
print("Requiring a LHE muon")
print(cut_str, cut_str_highpt)
#print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
met = '(Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter)'
hlt = "&&(HLT_PFHT800 || HLT_PFHT900 || HLT_Mu50 || HLT_TkMu50 || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Photon175 || HLT_Ele27_WPTight_Gsf)"
cut_str += met + hlt
cut_str_highpt += met + hlt
print("MET Filters and HLT requirements")
print(cut_str, cut_str_highpt)
#print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
PV = '&&(PV_ndof>4 && abs(PV_z)<20 && sqrt(PV_x^2+PV_y^2)<2)'
cut_str += PV
cut_str_highpt += PV
print('Requiring good PV')
print(cut_str, cut_str_highpt)
#print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
muon_high = '&&(Muon_highPtId[0] == 2 && Muon_tkRelIso[0]<0.05 && abs(Muon_eta[0]) < 2.4)'
muon_tight = '&&(Muon_tightId[0] && Muon_miniPFRelIso_all[0]<0.1 && abs(Muon_eta[0]) < 2.4)'
cut_str += muon_tight
cut_str_highpt += muon_high
print('Requiring one tight/Highpt muon')
print(cut_str, cut_str_highpt)
#print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
#loose_mu = '&&(nMuon==1 || !(Muon_looseId[1] && Muon_pt[1] > 35 && Muon_miniPFRelIso_all[1] < 0.4 && abs(Muon_eta[1]) < 2.4))'
#loose_ele = '&&(nElectron==0 || !(Electron_mvaFall17V2noIso_WPL[0] && Electron_pt[0] > 35 && Electron_miniPFRelIso_all[0] < 0.4 && abs(Electron_eta[0]) < 2.4))'
#cut_str += loose_mu + loose_ele
#cut_str_highpt += loose_mu + loose_ele
#print('Vetoing additional leptons')
#print(cut_str, cut_str_highpt)
#print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
jets = '&&(Jet_jetId[0] >= 2 && Jet_jetId[1] >= 2 && abs(Jet_eta[0]) < 2.4 && abs(Jet_eta[1]) < 2.4 && Jet_pt[0] > 100 && Jet_pt[1] > 100)'
fatjets = '&&(nFatJet > 1)'
cut_str += jets + fatjets
cut_str_highpt += jets+ fatjets
print('Adding jets')
print(cut_str, cut_str_highpt)
#print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))
muonpt = '&&(Muon_pt[0] > 500)'
cut_str += muonpt
cut_str_highpt += muonpt
print('Requiring muon pt > 500 ')
print(cut_str, cut_str_highpt)
#print(int(tree.GetEntries(cut_str)), int(tree.GetEntries(cut_str_highpt)))

# plotting
edges = array.array('f', [30., 50., 60., 80., 100., 130., 200., 400., 1000.])
nbins = len(edges)-1
h_HLT_num_high = ROOT.TH1F("HLT_num_high", "HLT_num; lepton p_{T} [GeV]; Events / bin", nbins, edges)
h_HLT_den_high = ROOT.TH1F("HLT_den_high", "HLT_den; lepton p_{T} [GeV]; Events / bin", nbins, edges)
h_HLT_MC_Eff_high = ROOT.TH1F("h_HLT_MC_Eff_highpt", "h; lepton p_{T} [GeV]; #epsilon", nbins, edges)
h_HLT_num_tight = ROOT.TH1F("HLT_num_tight", "HLT_num; lepton p_{T} [GeV]; Events / bin", nbins, edges)
h_HLT_den_tight = ROOT.TH1F("HLT_den_tight", "HLT_den; lepton p_{T} [GeV]; Events / bin", nbins, edges)
h_HLT_MC_Eff_tight = ROOT.TH1F("h_HLT_MC_Eff_tight", "h; lepton p_{T} [GeV]; #epsilon", nbins, edges)
print(met + hlt + PV + jets + fatjets + muon_tight)
'''
tree.Project("HLT_num_tight", "Muon_pt[0]*Muon_tunepRelPt[0]", met + hlt + PV + jets + fatjets + muon_tight + muonpt)
tree.Project("HLT_den_tight", "Muon_pt[0]*Muon_tunepRelPt[0]", met + hlt + PV + jets + fatjets + muonpt + '&&(Muon_miniPFRelIso_all[0]<0.1 && abs(Muon_eta[0]) < 2.4)')
tree.Project("HLT_num_high", "Muon_pt[0]*Muon_tunepRelPt[0]", met + hlt + PV + jets + fatjets + muon_high + muonpt)
tree.Project("HLT_den_high", "Muon_pt[0]*Muon_tunepRelPt[0]", met + hlt + PV + jets + fatjets + muonpt + '&&(Muon_tkRelIso[0]<0.05 && abs(Muon_eta[0]) < 2.4)')

tree.Project("HLT_num_tight", "Muon_pt[0]", met + hlt + PV + jets + fatjets + muon_tight + muonpt)
tree.Project("HLT_den_tight", "Muon_pt[0]", met + hlt + PV + jets + fatjets + muonpt + '&&(Muon_miniPFRelIso_all[0]<0.1 && abs(Muon_eta[0]) < 2.4)')
tree.Project("HLT_num_high", "Muon_pt[0]", met + hlt + PV + jets + fatjets + muon_high + muonpt)
tree.Project("HLT_den_high", "Muon_pt[0]", met + hlt + PV + jets + fatjets + muonpt + '&&(Muon_tkRelIso[0]<0.05 && abs(Muon_eta[0]) < 2.4)')
#tree.Project("HLT_num", "Muon_pt[0]", met + hlt + PV + jets + fatjets + muon_tight)
#tree.Project("HLT_den", "Muon_pt[0]", met + hlt + PV + jets + fatjets + '&&(Muon_miniPFRelIso_all[0]<0.1 && abs(Muon_eta[0]) < 2.4)')
h_HLT_MC_Eff_tight.Divide(h_HLT_num_tight, h_HLT_den_tight, 1, 1)
h_HLT_MC_Eff_high.Divide(h_HLT_num_high, h_HLT_den_high, 1, 1)

plot(h_HLT_MC_Eff_tight)
plot(h_HLT_MC_Eff_high)

#write("Plot_with_tune.root", h_HLT_num_high, h_HLT_den_high, h_HLT_MC_Eff_high)
#write("Plot_with_tune.root", h_HLT_num_tight, h_HLT_den_tight, h_HLT_MC_Eff_tight)
write("Plot.root", h_HLT_num_high, h_HLT_den_high, h_HLT_MC_Eff_high)
write("Plot.root", h_HLT_num_tight, h_HLT_den_tight, h_HLT_MC_Eff_tight)
'''
h_tight = ROOT.TH1F("h_tight", "; lepton p_{T} [GeV]; Events / bin", 5, 500, 1000)
h_tight_tune = ROOT.TH1F("h_tight_tune", "; lepton p_{T} [GeV]; Events / bin", 5, 500, 1000)

tree.Project("h_tight", "Muon_pt[0]", met + hlt + PV + jets + fatjets + muon_tight + muonpt)
tree.Project("h_tight_tune", "Muon_pt[0]*Muon_tunepRelPt[0]", met + hlt + PV + jets + fatjets + muon_tight + muonpt)
print(h_tight.Integral())
print(h_tight_tune.Integral())

plot(h_tight)
plot(h_tight_tune)
write("Plot2.root", h_tight)
write("Plot2.root", h_tight_tune)




import ROOT
import os
#import json_reader as jr                                                                                                                                                                                                                                                                                         

path = os.path.dirname(os.path.abspath(__file__))

class sample:
    def __init__(self, color, style, fill, leglabel, label):
        self.color = color
        self.style = style
        self.fill = fill
        self.leglabel = leglabel
        self.label = label

tag_2016 = 'RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8'

###################################################################################################################################################################                                                                                                                                               
############################################################                                           ############################################################                                                                                                                                               
############################################################                    2016                   ############################################################                                                                                                                                               
############################################################                                           ############################################################                                                                                                                                               
###################################################################################################################################################################                                                                                                                                               

################################ TTbar ################################                                                                                                                                                                                                                                           
TT_incl_2016 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_incl_2016")
TT_incl_2016.sigma = 831.76 #pb                                                                                                                                                                                                                                                                                   
TT_incl_2016.year = 2016
TT_incl_2016.dataset = "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/"+tag_2016+"-v1/NANOAODSIM"

TT_Mtt700to1000_2016 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt700to1000_2016")
TT_Mtt700to1000_2016.sigma = 80.5 #pb                                                                                                                                                                                                                                                                             
TT_Mtt700to1000_2016.year = 2016
TT_Mtt700to1000_2016.dataset = "/TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#TT_Mtt700to1000_2016.files = jr.json_reader(path+"/TT_Mtt700to1000_2016.json")                                                                                                                                                                                                                                   

TT_Mtt1000toInf_2016 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt1000toInf_2016")
TT_Mtt1000toInf_2016.sigma = 21.3 #pb                                                                                                                                                                                                                                                                             
TT_Mtt1000toInf_2016.year = 2016
TT_Mtt1000toInf_2016.dataset = "/TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8/"+tag_2016+"-v1/NANOAODSIM"
#TT_Mtt1000toInf_2016.files = jr.json_reader(path+"/TT_Mtt1000toInf_2016.json")                                                                                                                                                                                                                                   

TT_Mtt_2016 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt_2016")
TT_Mtt_2016.year = 2016
TT_Mtt_2016.components = [TT_incl_2016, TT_Mtt700to1000_2016, TT_Mtt1000toInf_2016]

Tprime_tHq_600LH_2018 = sample(ROOT.kBlue,1,1,"T' 600 LH","Tprime_tHq_600LH_2018")
Tprime_tHq_600LH_2018.sigma = 1 #to be changed
Tprime_tHq_600LH_2018.year = 2018
Tprime_tHq_600LH_2018.dataset="/TprimeBToTH_M-600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_700LH_2018 = sample(ROOT.kBlue,1,1,"T' 700 LH","Tprime_tHq_700LH_2018")
Tprime_tHq_700LH_2018.sigma = 1 #to be changed
Tprime_tHq_700LH_2018.year = 2018
Tprime_tHq_700LH_2018.dataset="/TprimeBToTH_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_800LH_2018 = sample(ROOT.kBlue,1,1,"T' 800 LH","Tprime_tHq_800LH_2018")
Tprime_tHq_800LH_2018.sigma = 1 #to be changed
Tprime_tHq_800LH_2018.year = 2018
Tprime_tHq_800LH_2018.dataset="/TprimeBToTH_M-800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_900LH_2018 = sample(ROOT.kBlue,1,1,"T' 900 LH","Tprime_tHq_900LH_2018")
Tprime_tHq_900LH_2018.sigma = 1 #to be changed
Tprime_tHq_900LH_2018.year = 2018
Tprime_tHq_900LH_2018.dataset="/TprimeBToTH_M-900_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_1000LH_2018 = sample(ROOT.kBlue,1,1,"T' 1000 LH","Tprime_tHq_1000LH_2018")
Tprime_tHq_1000LH_2018.sigma = 1 #to be changed
Tprime_tHq_1000LH_2018.year = 2018
Tprime_tHq_1000LH_2018.dataset="/TprimeBToTH_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_1100LH_2018 = sample(ROOT.kBlue,1,1,"T' 1100 LH","Tprime_tHq_1100LH_2018")
Tprime_tHq_1100LH_2018.sigma = 1 #to be changed
Tprime_tHq_1100LH_2018.year = 2018
Tprime_tHq_1100LH_2018.dataset="/TprimeBToTH_M-1100_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_1200LH_2018 = sample(ROOT.kBlue,1,1,"T' 1200 LH","Tprime_tHq_1200LH_2018")
Tprime_tHq_1200LH_2018.sigma = 1 #to be changed
Tprime_tHq_1200LH_2018.year = 2018
Tprime_tHq_1200LH_2018.dataset="/TprimeBToTH_M-1200_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_1300LH_2018 = sample(ROOT.kBlue,1,1,"T' 1300 LH","Tprime_tHq_1300LH_2018")
Tprime_tHq_1300LH_2018.sigma = 1 #to be changed
Tprime_tHq_1300LH_2018.year = 2018
Tprime_tHq_1300LH_2018.dataset="/TprimeBToTH_M-1300_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_1400LH_2018 = sample(ROOT.kBlue,1,1,"T' 1400 LH","Tprime_tHq_1400LH_2018")
Tprime_tHq_1400LH_2018.sigma = 1 #to be changed
Tprime_tHq_1400LH_2018.year = 2018
Tprime_tHq_1400LH_2018.dataset="/TprimeBToTH_M-1400_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_1500LH_2018 = sample(ROOT.kBlue,1,1,"T' 1500 LH","Tprime_tHq_1500LH_2018")
Tprime_tHq_1500LH_2018.sigma = 1 #to be changed
Tprime_tHq_1500LH_2018.year = 2018
Tprime_tHq_1500LH_2018.dataset="/TprimeBToTH_M-1500_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_1600LH_2018 = sample(ROOT.kBlue,1,1,"T' 1600 LH","Tprime_tHq_1600LH_2018")
Tprime_tHq_1600LH_2018.sigma = 1 #to be changed
Tprime_tHq_1600LH_2018.year = 2018
Tprime_tHq_1600LH_2018.dataset="/TprimeBToTH_M-1600_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_1700LH_2018 = sample(ROOT.kBlue,1,1,"T' 1700 LH","Tprime_tHq_1700LH_2018")
Tprime_tHq_1700LH_2018.sigma = 1 #to be changed
Tprime_tHq_1700LH_2018.year = 2018
Tprime_tHq_1700LH_2018.dataset="/TprimeBToTH_M-1700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"

Tprime_tHq_1800LH_2018 = sample(ROOT.kBlue,1,1,"T' 1800 LH","Tprime_tHq_1800LH_2018")
Tprime_tHq_1800LH_2018.sigma = 1 #to be changed
Tprime_tHq_1800LH_2018.year = 2018
Tprime_tHq_1800LH_2018.dataset="/TprimeBToTH_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"



sample_dict = {'TT_Mtt_2016':TT_Mtt_2016, 'TT_Mtt700to1000_2016':TT_Mtt700to1000_2016, 'TT_Mtt1000toInf_2016':TT_Mtt1000toInf_2016, 'TT_incl_2016':TT_incl_2016,
"Tprime_tHq_600LH_2018":Tprime_tHq_600LH_2018,"Tprime_tHq_700LH_2018":Tprime_tHq_700LH_2018,"Tprime_tHq_800LH_2018":Tprime_tHq_800LH_2018,"Tprime_tHq_900LH_2018":Tprime_tHq_900LH_2018,
"Tprime_tHq_1000LH_2018":Tprime_tHq_1000LH_2018,"Tprime_tHq_1100LH_2018":Tprime_tHq_1100LH_2018,"Tprime_tHq_1200LH_2018":Tprime_tHq_1200LH_2018,"Tprime_tHq_1300LH_2018":Tprime_tHq_1300LH_2018,
"Tprime_tHq_1400LH_2018":Tprime_tHq_1400LH_2018,"Tprime_tHq_1500LH_2018":Tprime_tHq_1500LH_2018,"Tprime_tHq_1600LH_2018":Tprime_tHq_1600LH_2018,"Tprime_tHq_1700LH_2018":Tprime_tHq_1700LH_2018,
"Tprime_tHq_1800LH_2018":Tprime_tHq_1800LH_2018}

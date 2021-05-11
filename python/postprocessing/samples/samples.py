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


sample_dict = {'TT_Mtt_2016':TT_Mtt_2016, 'TT_Mtt700to1000_2016':TT_Mtt700to1000_2016, 'TT_Mtt1000toInf_2016':TT_Mtt1000toInf_2016, 'TT_incl_2016':TT_incl_2016}

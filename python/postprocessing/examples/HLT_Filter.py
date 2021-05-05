import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class HLT_Filter(Module):
    def __init__(self, year, runP):
        self.year = year
        self.runP = runP #
        pass
    def endJob(self):
        pass
    def beginJob(self):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        HLT = Object(event, "HLT")
        run = Object(event, "run")
        if self.year == '2016' and self.runP != 'H':
            if run.__getattr__('') > 274954:
                good_HLT = HLT.PFHT800 or HLT.PFHT900 or HLT.Mu50 or HLT.TkMu50 or HLT.Ele115_CaloIdVT_GsfTrkIdT or HLT.Photon175 or HLT.Ele27_WPTight_Gsf
        return good_HLT

def HLT_fun(year, runP):
    HLT_function = lambda : HLT_Filter(year, runP)
    return HLT_function

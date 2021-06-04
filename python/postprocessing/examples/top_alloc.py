import ROOT
import math
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *



class top_alloc(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        self.out.branch("nTop","i")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        electrons = Collection(event, "Electron")

       
        goodMu = list(filter(lambda x : x.pt>10, muons))
        goodJet = list(filter(lambda x :  x.pt>30, jets))
        goodEl = list(filter(lambda x : x.pt>10, electrons))


        if not ((len(goodMu)>0 or len(goodEl)>0) and len(goodJet)>0 ):          
            return False
        
        else:
            nTops = (len(goodJet)*(len(goodMu)+len(goodEl)))

        self.out.fillBranch("nTop", nTops)

        return True


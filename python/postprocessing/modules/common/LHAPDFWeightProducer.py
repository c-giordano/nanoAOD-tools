import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class LHAPDFWeightProducer(Module):
    def __init__(self,pdfnominal="NNPDF30_lo_as_0118",pdfreweights={"NNPDF30_lo_as_0118":"RMS"},names={"NNPDF30_lo_as_0118":"LHANNPDF"},getUnc=True,envelopePDFUncertainty=False,verbose=False):
        self.names = names
        self.pdfnominal=pdfnominal
        self.pdfreweights = pdfreweights
        self.getUnc=getUnc
        self.verbose = verbose
        self.envelopePDFUncertainty=envelopePDFUncertainty
        self._workers={}
        #Try to load module via python dictionaries
        try:
            ROOT.gSystem.Load("libPhysicsToolsNanoAODTools")
            dummy = ROOT.LHAPDFUncertaintiesCalculator
        #Load it via ROOT ACLIC. NB: this creates the object file in the CMSSW directory,
        #causing problems if many jobs are working from the same CMSSW directory
        except Exception as e:
            print "Could not load module via python, trying via ROOT", e
            if "/LHAPDFUncertaintiesCalculator_cc.so" not in ROOT.gSystem.GetLibraries():
                print "Load C++ Worker"
                ROOT.gROOT.ProcessLine(".L %s/src/PhysicsTools/NanoAODTools/src/LHAPDFWeightProducer.cc++" % os.environ['CMSSW_BASE'])
            dummy = ROOT.LHAPDFUncertaintiesCalculator

    def beginJob(self):
	pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pdf,method =self.pdfnominal, "RMS"
        for p,m in self.pdfreweights.iteritems():
            self._workers[p] = ROOT.LHAPDFUncertaintiesCalculator(self.pdfnominal,pdf,method,self.verbose)

        if(self.envelopePDFUncertainty): print("envelope not implemented yet!")
        """        if(len(self.pdfreweights)==1):

                pdf, method= p, m
        #not yet implmented: more than 1 pdf uncertainty calculation.
        if(len(self.pdfreweights)>1):
            print("WARNING! Multiple pdf uncertainty not yet implemented, will evaluate uncertainty only on the one matching nominal pdf ")
            nominalfound=False
            for p,m in self.pdfreweights.iteritems():
                if(p==self.pdfnominal): 
                    pdf, method= p, m
                    nominalfound=True
            if not nominalfound: 
                print("WARNING! Nominal pdf not found in the list of pdfs, using NNLOPDF_lo_as_118 - make sure this is what you want! ") 

        """         
        self.out = wrappedOutputTree
        for p in self.pdfreweights:
            self.out.branch(self.names[p], "F")
            if self.getUnc:
                self.out.branch(self.names[p]+"_pdfUnc", "F")
                self.out.branch(self.names[p]+"_pdfUp", "F")
                self.out.branch(self.names[p]+"_pdfDown", "F")
            
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""


        weights={}
        weights_unc={}
        weights_up={}
        weights_down = {}
        if hasattr(event,"Generator_x1"):
            x1=float(getattr(event,"Generator_x1"))
            x2=float(getattr(event,"Generator_x2"))
            id1=int(getattr(event,"Generator_id1"))
            id2=int(getattr(event,"Generator_id2"))
            scalePDF=float(getattr(event,"Generator_scalePDF"))

            pdf,method =self.pdfnominal, "RMS"

            for p,m in self.pdfreweights.iteritems():
                weights[p] = self._workers[p].getWeight(x1,x2,id1,id2,scalePDF,p)
                
                if(self.verbose):
                    print("pdf is = ",p)
                    print("central weight",weights[p])
                self.out.fillBranch(self.names[p],weights[p])
                if self.getUnc:
                    weights_unc[p] = self._workers[p].getUncertainty(x1,x2,id1,id2,scalePDF,p,self.verbose)
                    if(self.verbose): print("unc",weights_unc[p])
                    weights_up[p]= weights[p]+weights_unc[p]
                    weights_down[p]= weights[p]-weights_unc[p]

                    self.out.fillBranch(self.names[p]+"_pdfUnc",weights_unc[p])
                    self.out.fillBranch(self.names[p]+"_pdfUp",weights_up[p])
                    self.out.fillBranch(self.names[p]+"_pdfDown",weights_down[p])
                    
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

#def __init__(self,targetfile,pdfnominal="NNPDF30_lo_as_0118",pdfreweights={"NNPDF30_lo_as_0118":"RMS"},names={"NNPDF30_lo_as_0118":"LHANNPDF"},getUnc=True,envelopePDFUncertainty=False,verbose=False):
LHAPDFWeight_NNPDF = lambda : LHAPDFWeightProducer(pdfnominal="NNPDF30_lo_as_0118",pdfreweights={"NNPDF30_lo_as_0118":"RMS"},names={"NNPDF30_lo_as_0118":"LHANNPDF"},getUnc=True,envelopePDFUncertainty=False,verbose=True)


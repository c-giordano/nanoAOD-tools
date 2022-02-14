import math
import copy
from array import array
from ROOT import *
import sympy

def smoothFile(filedir,sample,syst,histos,nsmooth=10):
    f = ROOT.TFile(filedir+"/sample")
    

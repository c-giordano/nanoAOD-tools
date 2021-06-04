#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.examples.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.examples.MET_HLT_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.examples.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.examples.unpacking_vers2 import *
from PhysicsTools.NanoAODTools.postprocessing.examples.preselection_Tprime  import *
from PhysicsTools.NanoAODTools.postprocessing.examples.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.examples.top_alloc import *


metCorrector_tot = createJMECorrector(isMC=True, dataYear=2017, jesUncert='Total', redojec=True)
fatJetCorrector_tot = createJMECorrector(isMC=True, dataYear=2017, jesUncert='Total', redojec=True, jetType = 'AK8PFchs')
metCorrector = createJMECorrector(isMC=True, dataYear=2017, jesUncert='All', redojec=True)
fatJetCorrector = createJMECorrector(isMC=True, dataYear=2017, jesUncert='All', redojec=True, jetType = 'AK8PFchs')

p = PostProcessor('.', ['/../../home/iorio/public/tHq/signals/Tprime_tHq_1200.root'], '', modules=[MCweight_writer(), preselection_Tprime(), GenPart_MomFirstCp(flavour="11,12,13,14,15,16,5,6,24,23,25"), top_alloc(), unpacking_MC()], outputbranchsel=os.path.abspath('../scripts/keep_and_drop.txt'), histFileName="histOut.root", histDirName="plots", maxEntries=200000, provenance=True, fwkJobReport=True)
p.run()
print 'DONE'
#, PrefCorr(), metCorrector(), fatJetCorrector()

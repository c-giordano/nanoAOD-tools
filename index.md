# Welcome to CMSNAFW

The repository [CMSNAFW](https://github.com/CMSNAFW/nanoAOD-tools) is intended to provide a complete and working set of tools that allows to work with the NanoAOD format of the CMS Collaboration.

The framework makes use of the [NanoAOD-Tools](https://github.com/cms-nanoAOD/nanoAOD-tools) and it adds utils to run jobs on the [CRAB](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab) and [HTCondor](https://htcondor.readthedocs.io/en/latest/).

A useful set of slides that introduces to the NanoAOD format and to the NanoAOD-Tools framework can be found [here](https://docs.google.com/presentation/d/1vAA2NYoxtHY3nNmrXKSPITm6QOAJjv2d7mAcCxP7vR4/edit?usp=sharing)

The framework is conceived as a two-steps processing:
- CRAB step
- HTCondor step

## Step-by-step instruction
### Download and installation
Login to your machine (both lxplus and cmsui04). For cmsui you need to set the cms environment as reported [here](https://github.com/adeiorio/repo/blob/master/cmsui04_%40Naples.md#set-the-cms-enviroment)
```
cmsrel CMSSW_10_5_0
cd CMSSW_10_5_0/src
git clone https://github.com/CMSNAFW/nanoAOD-tools PhysicsTools/NanoAODTools
cd PhysicsTools/NanoAODTools
scramv1 b -j 4
```

### CRAB 
To run the CRAB step, **you need to modify and customise** some configuration files. 
1. First of all, you have to modify the file _script/keep_and_drop.txt_ to keep/drop branches you need or not.
2. Another requirement is to write the samples on which you would run in the file _python/postprocessing/samples/samples.py_ according to the convention already present. You also need to add the the samples you add to the dictionary, so you can use it as an argument of a python macro.
3. The last step is to personalise the _crab/submit_crab.py_ that will take care of writing all the files needed for the submission. It is also useful to interact with a crab job after it has been submitted or when it will be finished.
```
cd crab
python submit_crab.py -d TT_Mtt_2016 -s
```
In this step the PostProcessor method is run. **You need to customise** to your use case the modules in the _python/postprocessing/examples_ folder. 

### Condor
This represent the last step of the framework and it is located in _python/postprocessing_ folder. The wrapper _submit_condor.py_ allows you to submit a job taking as a input a file produced with the previous step or with a file stored on the CMS DAS database.
This macro prepares all the needed files for the submission. 
- The bash file _runner.sh_ takes care of setting the environment on the Condor machines and it run the _tree_skimmer.py_ macro
- **You need to write** your own tree_skimmer.py macro following the the example already present in this code repository.
```
cd python/postprocessing
python submit_condor.py -f v0 -d TT_Mtt_2016
```

### Makeplot
In the repository you can also find a macro to produce the histograms for your final fit from the output of the previous steps. This macro is _makeplot.py_, it is located in _python/postprocessing_ folder and it uses the class _variabile.py_ (stored in the same folder) and the official CMS macro for the plot style (_CMS\_lumi.py_).
**You need to customise** to your use case this macro to make it work correctly with your samples, input folder, years and categories.

- You can use this macro to merge all the parts files produced by Condor, apply the luminosity weights and merge the components of a samples:
```
python makeplot.py --merpart --lumi --mertree
```
This command should be used only ones. The parts files are not removed nor overwritten.

- Now you are ready to produce histograms and stack plots:
```
python makeplot.py -p -s --sel -S noSyst/all/name_syst -C "some requirement" 
```
The above is one of the most general uses of the makeplot. The option passed produce plots, stack plots, apply a default selection, histograms for systematic variations and apply additional requirements (producing an according text in the histogram) respectively.

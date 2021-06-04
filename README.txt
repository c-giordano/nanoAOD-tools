INSTRUCTIONS FOR ANALYSIS: Tprime -> tHq/tZq -> lnuqq

1. POSTPROCESSOR
   Input  ==> Raw nanoAOD file
   Output ==> Root file with top collection, input for ML step

   To run it, on crab/ folder:
      	python crab_script_local.py

   Modules used are in python/postprocessing/examples/
   List:
	MCweight_writer.py -> Writes MC weights
	preselection_Tprime.py -> Preselection for our final state
	GenPart_MomFirstCp.py -> Computes real mother particles (i.e. not considering scattering)
	top_alloc.py -> Allocation of Top candidates: Not needed anymore, either remove it or use it for top selection (i.e. el/mu/jet pt requirements etc.)
	unpacking_vers2.py -> Constructs the Top collection for each event

2. MACHINE LEARNING (BDT)
   Input  ==> Root output file from postprocessor
   Output ==> Same root file as input + Top_Score for each top

   To run the BDT, we first need to UNPACK (a) the original entries with several tops per entry, into a set of entries where each top is an individual event. Then, we train/run the BDT algorithm (b), and finally we need to REPACK (c) again all these entries as they originally were.

   a) Unpacking:
      Code is located in bin/C++/ directory (nano_unpacking.cpp). It takes the original tree or list of trees to unpack (listed in a txt file in the txt/ folder) and creates the output root file in a folder called MergedTrees/
      Example run:
      	    scram b -j 4  -> Compiles all codes & creates corresponding executables. NOTE: You might need to change the file "BuildFile.xml". 
  	    nano_unpacking txt/Tprime_1200_unpacking.txt MergedTrees/Tprime_1200_treeMerged.root

   b) BDT:
      Code is located in python/models/. The name is "MergedML.py", and to run it simply type:
      	   python MergedML.py
      It reads the configurations for training from "ML_config.py".
      The output will be a root file for each trained category (in our case it is 8 for the moment: high & low pt for electrons & muons in merged & resolved categories), that will contain the BDT score for each top. It will also output some plots to the png/ directory, as well as .json files containing the saved model for each trained category. NOTE: Check the direcories, you should put your own.

   c) Repacking:
      Code is located in bin/C++/ directory, named "repacking.final.cpp". It takes the output root files from the ML code and adds the Top_Score branch to the original root file output from the postprocessor.
      Example run:
      	    repacking_final txt/Tprime_1200_repack.txt ../crab/Tprime_tHq_1200_Skim.root

3. TREE SKIMMER
   Input  ==> Repacked output from postprocessor with Top_Score branch
   Output ==> Skimmed Tree

   Code is located in python/postprocessing/ directory. Example run:
   	python tree_skimmer_Tprime.py "Name+for+output" 0 "[Tprime_tHq_1200_Skim.root]" "Local"
   
*** IMPORTANT NOTE ***

There are a few things that have to be done/corrected:
   1.- Create a script that runs the Step 2 (BDT) with just one command
   2.- The Top_Score variable is not well integrated in the framework: It is not part of top collection and therefore connot be read as other branches in the tree skimmer. It can be read in the usual way (tree.GetEntry(i)), but we need to figuere out a way of making it a Top variable so that everything is well integrated within the framework.

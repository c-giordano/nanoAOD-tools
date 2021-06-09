#!/bin/bash                                                                                                                                       

# Inputs: 
    # 1[sampletype] --> 'S' for signal, 'B' for background
    # 2[runoption]  --> 'Yes' if model is trained, 'No' if it is not
    # 3-?[samples]  --> FOR SIG: Write all mass samples separated by blank space // FOR BKG: Dont put anything, uses default treelist_unpacking.txt

scram b -j 4

args=($@)
i=3
j=$#
max=$((j - 1))
sample=$3
while [ $i -le $max ]
do
    sample=$sample+${args[i]}
    i=$((i + 1))
done

echo "Step 1 ======> Unpacking original Tree/s"

if [ $1 == 'S' ]
    then
       nano_unpacking Txt/Tprime_$sample'_unpacking.txt' MergedTrees/Tprime_$sample'_treeMerged.root'
fi
if [ $1 == 'B' ]
    then
       nano_unpacking Txt/treelist_unpacking.txt MergedTrees/unpackedBkg_treeMerged.root
fi
if [ $1 != 'S' -a $1 != 'B' ]
    then
       echo "arg1 [sampletype] not a valid argument: it should be 'S' for signal or 'B' for background."
       exit 1
fi

echo "Step 2 ======> Adding BDT Score for each top"

if [ $2 == 'Yes' ]
    then
       python trainedModel.py $1 $sample
fi
if [ $2 == 'No' ]
    then
       exit 1
fi
if [ $2 != 'Yes' -a $2 != 'No' ]
    then
       echo "arg3 [runoption] not a valid argument: it should be 'Yes' if model trained, 'No' if not trained."
       exit 1
fi

echo "Step 3 ======> Repacking events into original Tree/s"

if [ $1 == 'S' ]
    then
       i=2
       while [ $i -le $max ]
       do
           echo "Repacking ${args[i]} sample."
	   repacking_final Txt/Tprime_${args[i]}_repacking.txt /home/diefer/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/Tprime_tHq_${args[i]}_Skim.root
	   i=$((i + 1))
       done
fi
if [ $1 == 'B' ]
    then
       repacking_final Txt/treelist_repacking.txt /home/diefer/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/crab/Prueba_Fondo.root
fi

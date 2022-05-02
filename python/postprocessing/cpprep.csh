#python full_analysis.py -m de -i localtest_anv17 -o localtest_anv17/  
#cp localtest_anv17/v18/plot_explin/muon/DD* localtest_anv17/v18/plot_merged/muon/
#cp localtest_anv17/v18/plot_explin/electron/DD* localtest_anv17/v18/plot_merged/electron/
#python full_analysis.py -m fe -i localtest_anv17 -o localtest_anv17/ --fitdir 19apr
cp localtest_anv17/v18/plot_fit19apr/muon/D* localtest_anv17/v18/plot_fit19apr/muon/QCD* localtest_anv17/v18/plot_fit_backgrounds/muon
cp localtest_anv17/v18/plot_fit19apr/electron/D* localtest_anv17/v18/plot_fit19apr/electron/QCD* localtest_anv17/v18/plot_fit_backgrounds/electron

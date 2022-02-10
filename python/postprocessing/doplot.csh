#!/bin/tcsh
set year = $1
set v = v18
set syst = 'all '
set extratext = '' #$2
set syst = 'noSyst'
#python makeplot.py -y $year -s -L muon --sel -f $v -C "deltaR_bestWAK4_closestAK8<0.4" -s $syst
#python makeplot.py -y $year -s -L electron --sel -f $v -C "deltaR_bestWAK4_closestAK8<0.4" -s $syst
#&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60
#set commcut = "&&best_top_m<250&&best_top_m>100"#&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&best_top_m<200&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&best_top_m>120&&best_top_m<200&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&best_top_m>120"
#

set commcut = "&&best_top_m>120&&best_top_m<220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60" #&&abs(best_topW_jets_deltaPhi)>2.5"
:<<EOF
# Plots for fit
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -S $syst -s 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -S $syst -s 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -S $syst -s 
#EOF
#:<<EOF
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -S $syst -s 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -S $syst -s 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -S $syst -s 
#EOF
#:<<EOF
#set commcut = "&&best_top_m<220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
#set commcut = ""
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst -s 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst -s 
#python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut -s $syst -d $extratext 
#python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst -d $extratext 
EOF

:<<EOF
#set commcut = "&&(best_top_m<120||best_top_m>220)&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = ""
# Plots for fit 
set commcut = "&&best_top_m>340&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>30"
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -s -S $syst  
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -s -S $syst  
#:<<EOF
set commcut = "&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -s -S $syst  
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -s -S $syst  
#EOF
#:<<EOF
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -s -S $syst  
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -s -S $syst  
#EOF
#set commcut = "&&best_top_m<200&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
#set commcut = ""
#EOF
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -s -S $syst  
#python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst  
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -s -S $syst  
#python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst  


set syst = 'noSyst'

:<<EOF
set commcut = "&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
#set commcut = ""
# Plots for fit 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -S $syst -d $extratext 
#
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -S $syst -d $extratext 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -S $syst -d $extratext 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -S $syst -d $extratext 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -S $syst -d $extratext 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -S $syst -d $extratext 
#EOF
#set commcut = "&&best_top_m<200&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
#set commcut = ""
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst -d $extratext 
#python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst -d $extratext 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst -d $extratext 
#python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst -d $extratext 
#EOF

set commcut = "&&best_top_m>120&&best_top_m<220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"

#:<<EOF
# Plots for fit 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -S $syst -d $extratext 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -S $syst -d $extratext 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -S $syst -d $extratext 
#:<<EOF
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -S $syst -d $extratext 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -S $syst -d $extratext 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -S $syst -d $extratext 
#EOF
#:<<EOF
#set commcut = "&&best_top_m<200&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
#set commcut = ""
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst -d $extratext 
#python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst -d $extratext 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst -d $extratext 
#python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst -d $extratext 
EOF

#:<<EOF
set syst = 'noSyst'
#python makeplot.py -y $year -L muon -f $v -s -S $syst -d $extratext 
#python makeplot.py -y $year -L electron -f $v -s -S $syst -d $extratext 
#python makeplot.py -y $year -L muon -f $v --sel --plot -S $syst -s # -d $extratext -C "lepton_pt>500"
python makeplot.py -y $year -L electron -f $v --sel --plot -S $syst -s # -d $extratext
EOF

set cut = ''
set cut = 'deltaR_bestWAK4_closestAK8<0.4'
:<<EOF
set cut = 'MET_phi>-3.14&&MET_phi<-2.36'
set cut = 'MET_phi>-2.36&&MET_phi<-1.57'
set cut = 'MET_phi>-1.57&&MET_phi<-0.79'
set cut = 'MET_phi>-0.79&&MET_phi<0'
set cut = 'MET_phi>0&&MET_phi<0.79'
set cut = 'MET_phi>0.79&&MET_phi<1.57'
set cut = 'MET_phi>1.57&&MET_phi<2.36'
set cut = 'MET_phi>2.36&&MET_phi<3.14'
set syst = 'noSyst'
python makeplot.py -y $year -L muon --sel -f $v -C $cut --plot -S $syst -s 
python makeplot.py -y $year -L electron --sel -f $v -C $cut --plot -S $syst -s 
EOF
#

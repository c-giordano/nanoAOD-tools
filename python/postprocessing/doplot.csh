set year = $1
set v = v17
set syst = 'all'
set syst = 'noSyst'
#python makeplot.py -y $year -s -L muon --sel -f $v -C "deltaR_bestWAK4_closestAK8<0.4" --plot -S $syst
#python makeplot.py -y $year -s -L electron --sel -f $v -C "deltaR_bestWAK4_closestAK8<0.4" --plot -S $syst
#&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60
#set commcut = "&&best_top_m<250&&best_top_m>100"#&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&best_top_m<200&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
set commcut = "&&best_top_m>120&&best_top_m<220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&best_top_m>120&&best_top_m<200&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&best_top_m>120"
#set commcut = ""

#:<<EOF
# Plots for fit 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -s -S $syst 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -s -S $syst 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -s -S $syst 
:<<EOF
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -S $syst 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -S $syst 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -S $syst 
EOF
#:<<EOF
#set commcut = "&&best_top_m<200&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
#set commcut = ""
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst 
#python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst 
#python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst 
#python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst 
#EOF

#:<<EOF
set commcut = "&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&(best_top_m<120||best_top_m>220)&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = ""
# Plots for fit 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -S $syst 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -S $syst 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -S $syst 
#EOF
:<<EOF
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -S $syst 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -S $syst 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -S $syst 
#EOF
#set commcut = "&&best_top_m<200&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
#set commcut = ""
EOF
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst 
#python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst 
#python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst 
#python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst 

:<<EOF
set commcut = "&&best_top_m<200&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
set commcut = "&&(best_top_m<120||best_top_m>220)&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = ""
# Plots for fit 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -S $syst 
#
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -S $syst 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -S $syst 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag"$commcut --plot -S $syst 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag==0"$commcut --plot -S $syst 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag&&best_Wpjet_isbtag"$commcut --plot -S $syst 
#EOF
#set commcut = "&&best_top_m<200&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
#set commcut = "&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
#set commcut = ""
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst 
python makeplot.py -y $year -L muon --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"$commcut --plot -S $syst 
python makeplot.py -y $year -L electron --sel -f $v -C "best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==1"$commcut --plot -S $syst 
EOF

:<<EOF
set syst = 'noSyst'
#python makeplot.py -y $year -L muon -f $v --plot -S $syst 
#python makeplot.py -y $year -L electron -f $v --plot -S $syst 
python makeplot.py -y $year -L muon -f $v --sel --plot $syst -s #-C "lepton_pt>500"
python makeplot.py -y $year -L electron -f $v --sel --plot $syst -s
EOF

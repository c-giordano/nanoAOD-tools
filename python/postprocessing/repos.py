#wjets_veto_threshold=400
wjets_veto_threshold=200

lepcut=""

namemap={}
'''
namemap["SR2B"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SR2B_I"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_G_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
#AND_best_top_m_G_120_AND_best_top_m_L_220
#AND_best_top_m_G_220

namemap["SR2B"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SR2B_I"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_G_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SR2B_II"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_G_60"

namemap["SRW"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SRW_I"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_AND_best_top_m_G_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"

#AND_best_top_m_G_120_AND_best_top_m_L_220
#AND_best_top_m_G_220
namemap["SRW"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SRW_I"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_AND_best_top_m_G_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"

namemap["SRW_II"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_G_60"

namemap["SRT"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_EQ_0_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SRT_I"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_EQ_0_AND_best_top_m_G_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"

#AND_best_top_m_G_120_AND_best_top_m_L_220
#AND_best_top_m_G_220

namemap["SRT"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_EQ_0_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SRT_I"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_EQ_0_AND_best_top_m_G_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"

namemap["SRT_II"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_EQ_0_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_G_60"

namemap["CR0B"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_0_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["CR0B_I"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_0_AND_best_top_m_G_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
#h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_1_AND_best_top_m_G_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60
namemap["CR0B_II"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_0_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_G_60"

namemap["CR1B"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_1_AND_best_top_m_G_120_AND_best_top_m_L_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["CR1B_I"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_1_AND_best_top_m_G_220_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["CR1B_II"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_1_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_G_60"

'''

namemap["SR2B"]="h_jets_best_Wprime_m_SR2B"
namemap["SR2B_I"]="h_jets_best_Wprime_m_SR2B_I"
#namemap["SR2B_I"]="h_jets_best_Wprime_m_selection_AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_G_340_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_G_30"

namemap["SRW"]="h_jets_best_Wprime_m_SRW"
namemap["SRW_I"]="h_jets_best_Wprime_m_SRW_I"

namemap["SRT"]="h_jets_best_Wprime_m_SRT"
namemap["SRT_I"]="h_jets_best_Wprime_m_SRT_I"

namemap["CR0B"]="h_jets_best_Wprime_m_CR0B"
namemap["CR0B_I"]="h_jets_best_Wprime_m_CR0B_I"


namemap["CR0B_mu"]="h_jets_best_Wprime_m_CR0B"
namemap["CR0B_I_mu"]="h_jets_best_Wprime_m_CR0B_I"

namemap["SR2B_IV"]="h_jets_best_Wprime_m_SR2B_IV"

namemap["SRW_II"]="h_jets_best_Wprime_m_SRW_II"
namemap["SRW_III"]="h_jets_best_Wprime_m_SRW_III"

namemap["SRT_II"]="h_jets_best_Wprime_m_SRT_II"
namemap["SRT_III"]="h_jets_best_Wprime_m_SRT_III"

namemap["CR0B_II"]="h_jets_best_Wprime_m_CR0B_II"
namemap["CR0B_III"]="h_jets_best_Wprime_m_CR0B_III"


namemap["CR0B_mu"]="h_jets_best_Wprime_m_CR0B"
namemap["CR0B_I_mu"]="h_jets_best_Wprime_m_CR0B_I"


#
wjets_veto_map = {"CR0B":"CR0B_I"}
wjets_veto_map = {"SR2B":"SR2B_I","SRW":"SRW_I","SRT":"SRT_I","CR0B":"CR0B_I"}
#wjets_veto_map = {"SR2B":"SR2B_I","SRW":"SRW_I","SRT":"SRT_I"}
#wjets_veto_map = {"SR2B":"SR2B_I"}
extra_map={"SRW_II":"SRW_III","SRT_II":"SRT_III","CR0B_II":"CR0B_III"}

histosr=[]
histocr=[]
for sr,cr in wjets_veto_map.iteritems():
    histosr.append(namemap[sr])
    histocr.append(namemap[cr])

extrasr=[]
extracr=[]
for sr,cr in extra_map.iteritems():
    extrasr.append(namemap[sr])
    extracr.append(namemap[cr])
#histocr.append(namemap["SR2B_I_old"])
#wjets_veto_map = {"SRT":"SRT_I"}

#wjets_veto_map = {"SR2B":"SR2B_I","SRW":"SRW_I","SRT":"SRT_I"}
#wjets_veto_map = {"SR2B":"SR2B_I","SRW":"SRW_I","SRT":"SRT_I"}
#wjets_veto_map = {"SR2B":"SR2B_I"}
#
ttbar_veto_map= {"SR2B":"SR2B_II","SRW":"SRW_II","SRT":"SRT_II","CR0B":"CR0B_II","CR1B":"CR1B_II"}
srcr_map = {"SR2B":"SRT","SR2B_I":"SRT_I","SRW":"CR1B","SRW_I":"CR1B_I"}
srcr_map_2 = {"SR2B":"SRW","SR2B_I":"SRW_I","SRW":"CR0B","SRW_I":"CR0B_I"}
srcr_map_3 = {"SR2B":"CR1B","SR2B_I":"CR1B_I"}
srcr_map_4 = {"SRT":"CR1B","SRT_I":"CR1B_I"}
srcr_map_4 = {"SRT":"CR1B","SRT_I":"CR1B_I"}



import os
import shutil

version = 'v17'
pathin = '/eos/user/a/adeiorio/Wprime/nosynch/' + version + '/plot_merged_explin_v3/'
#pathin = '/eos/user/a/adeiorio/Wprime/nosynch/' + version + '/plot_merged_bis/'
pathout = '/eos/user/a/adeiorio/Wprime/nosynch/' + version + '/plot_fit_ddsummed_explin_v3'

samples = ["DDFitWJetsTT_MttST"]
systs = ["PF", "pu", "lep", "trig", "jes", "jer", "btag", "mistag", "pdf_total", "TT_Mtt", "WJets", "ST"]
systs = ["TT_Mtt", "WJets", "ST"]
systs_peryear = ["TF", "DD", "Alt"]
#systs = ["PF", "pu", "lep", "trig", "jes", "jer", "btag", "mistag", "pdf_total", "TT_Mtt", "WJets", "ST", "TF", "DD"]
samples2 = ["QCD", "WP_M2000W20_RH", "WP_M3000W30_RH", "WP_M4000W40_RH", "WP_M5000W50_RH", "WP_M6000W60_RH"]
samples2 = []
systs2 = ["PF", "pu", "lep", "trig", "jes", "jer", "btag", "mistag", "pdf_total"]

versus = ['Up', 'Down']
leps = ['muon', 'electron']
#leps = ['muon']
years = ['2016', '2017', '2018']
if os.path.exists(pathout):
    #os.popen('rm -r '+ pathout + '/*')
    print 'ciao'
else:
    os.makedirs(pathout)
summedyears = True

for lep in leps:
    #os.makedirs(pathout + '/' + lep)
    if not summedyears:
        for year in years:
            filename = 'Data_' + year + '_' + lep + '.root'
            print('copying ', filename)
            #shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)
            for sample in samples:
                filename = sample + '_' + year + '_' + lep + '.root'
                print('copying ', filename)
                shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)
                for syst in systs:
                    for vs in versus:
                        filename = sample + '_' + year + '_' + lep + '_' + syst + vs + '.root'
                        print('copying ', filename)
                        shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)
                for syst in systs_peryear:
                    for vs in versus:
                        filename = sample + '_' + year + '_' + lep + '_' + syst + '_' + year + vs + '.root'
                        if lep == 'muon':
                            fileout = sample + '_' + year + '_' + lep + '_' + syst + '_mu_' + year + vs + '.root'
                        else:
                            fileout = sample + '_' + year + '_' + lep + '_' + syst + '_ele_' + year + vs + '.root'
                        print('copying ', filename)
                        shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + fileout)

            for sample in samples2:
                filename = sample + '_' + year + '_' + lep + '.root'
                print('copying ', filename)
                shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)
                for syst in systs2:
                    for vs in versus:
                        filename = sample + '_' + year + '_' + lep + '_' + syst + vs + '.root'
                        print('copying ', filename)
                        shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)

    else:
        systs = ["jes", "jer", "btag", "mistag", "pdf_total", "pu", "PF"]#, "q2"]
        systs_DD = ["TF_2020", "DD_2020", "Alt_2020", "TT_Mtt", "WJets", "ST"]
        systs_perlep = ["lep", "trig"]

        filename = 'Data_2020_' + lep + '.root'
        print('copying ', filename)
        shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)
        for sample in samples:
            filename = sample + '_2020_' + lep + '.root'
            print('copying ', filename)
            shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)
            for syst in systs_DD:
                for vs in versus:
                    filename = sample + '_2020_' + lep + '_' + syst + vs + '.root'
                    if lep == 'muon':
                        fileout = sample + '_2020_' + lep + '_' + syst + '_mu' + vs + '.root'
                    else:
                        fileout = sample + '_2020_' + lep + '_' + syst + '_ele' + vs + '.root'
                    print('copying ', filename)
                    shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + fileout)
        for sample in samples2:
            filename = sample + '_2020_' + lep + '.root'
            print('copying ', filename)
            shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)
            for syst in systs:
                for vs in versus:
                    filename = sample + '_2020_' + lep + '_' + syst + vs + '.root'
                    print('copying ', filename)
                    shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)
            for syst in systs_perlep:
                for vs in versus:
                    filename = sample + '_2020_' + lep + '_' + syst + vs + '.root'
                    if lep == 'muon':
                        fileout = sample + '_2020_' + lep + '_' + syst + '_mu' + vs + '.root'
                    else:
                        fileout = sample + '_2020_' + lep + '_' + syst + '_ele' + vs + '.root'
                    print('copying ', filename)
                    shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + fileout)


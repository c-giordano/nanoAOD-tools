import os

version = 'v18'
pathin = '/eos/user/a/adeiorio/Wprime/nosynch/' + version + '/plot'
pathout = '/eos/user/a/adeiorio/Wprime/nosynch/' + version + '/plot_merged'

systs_corr = ["jes", "btag", "mistag", "pdf_total", "q2", "pu", "PF", "lep", "trig"]
#systs_corr = ["PF", "lep", "trig"]
systs_uncorr = ["jer"]
#systs = ["PF", "pu", "lep", "trig", "jes", "jer", "btag", "mistag", "pdf_total", "TT_Mtt", "WJets", "ST", "TF", "DD"]
samples = ["WJets", "TT_Mtt", "ST", "QCD", "WP_M2000W20_RH", "WP_M3000W30_RH", "WP_M4000W40_RH", "WP_M5000W50_RH", "WP_M6000W60_RH"]
#systs2 = ["PF", "pu", "lep", "trig", "jes", "jer", "btag", "mistag", "pdf_total"]

versus = ['Up', 'Down']
leps = ['muon', 'electron']
#leps = ['muon']
years = ['2016', '2017', '2018']
if os.path.exists(pathout):
    os.popen('rm -r '+ pathout + '/*')
    print "ciao"
else:
    os.makedirs(pathout)

for lep in leps:
    os.makedirs(pathout + '/' + lep)
    command = 'hadd -f ' + pathout + '/' + lep + '/Data_2020_' + lep + '.root '
    for year in years:
        command += pathin + '/' + lep + '/Data*_' + year + '_' + lep + '.root '
    #print(command)
    os.system(command)

#sommare tutti gli anni
for lep in leps:
    for sample in samples:
        command = 'hadd -f ' + pathout + '/' + lep + '/' + sample + '_2020_' + lep + '.root '       
        for year in years:
            command += ' ' + pathin + '/' + lep + '/' + sample + '_' + year + '_' + lep + '.root'
        os.system(command)
        print ######### fine nominal #########
        if 'Data' in sample:
            continue 
        for syst in systs_corr:
            for vs in versus:
                command = 'hadd -f ' + pathout + '/' + lep + '/' + sample + '_2020_' +  lep + '_' + syst + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2016_' + lep + '_' + syst + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2017_' + lep + '_' + syst + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2018_' + lep + '_' + syst + vs +'.root'
                os.system(command)
        year = '2016'
        for syst in systs_uncorr:
            for vs in versus:
                command = 'hadd -f ' + pathout + '/' + lep + '/' + sample + '_2020_' +  lep + '_' + syst + year + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_' + year + '_' + lep + '_' + syst + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2017_' + lep + '.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2018_' + lep + '.root'
                os.system(command)
        print ######### fine 2016 #########
        year = '2017'
        for syst in systs_uncorr:
            for vs in versus:
                command = 'hadd -f ' + pathout + '/' + lep + '/' + sample + '_2020_' +  lep + '_' + syst + year + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2016_' + lep + '.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_' + year + '_' + lep + '_' + syst + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2018_' + lep + '.root'
                os.system(command)
        year = '2018'
        for syst in systs_uncorr:
            for vs in versus:
                command = 'hadd -f ' + pathout + '/' + lep + '/' + sample + '_2020_' +  lep + '_' + syst + year + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2016_' + lep + '.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2017_' + lep + '.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_' + year + '_' + lep + '_' + syst + vs +'.root'
                os.system(command)


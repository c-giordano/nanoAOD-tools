import os,optparse

usage = 'python doplot.py'
parser = optparse.OptionParser(usage)

parser.add_option('-l', '--lep', dest='leptons', default = 'muon,electron', type='string', help='lepton to run')
parser.add_option('-v', '--version', dest='version', default = 'v18', type='string', help='analysis version')
parser.add_option('-i', '--inputpath', dest='inputpath', default = '/eos/user/a/adeiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-o', '--outputpath', dest='outputpath', default = '/eos/user/o/oiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-n', '--dryrun', dest='dryrun', action= 'store_true' , default = False, help='if called not running the command')
parser.add_option('-d', '--samples', dest='samples', default = 'base', type='string', help='samples to run, default: all background, data and some signals')
parser.add_option('-M', '--missingSamplesFile', dest='missing', default = 'missingSamples.txt', type='string', help='missing samples file')
parser.add_option('--parallel', dest='parallel', type='int', default=1 , help='if called run on more than 1 plot simultaneously')
(opt, args) = parser.parse_args()


version = 'v17'


pathin = '/eos/user/o/oiorio/Wprime/nosynch/' + version + '/plot'
pathout = '/eos/user/o/oiorio/Wprime/nosynch/' + version + '/plot_merged_2017fix'

pathin = './newtest5/' + version + '/plot'
pathout = './newtest5/' + version + '/plot_merged_fix'

pathin = opt.inputpath 
pathout = opt.outputpath 

version = opt.version


pathin = opt.inputpath +"/"+version+"/plot"
pathout = opt.outputpath+"/"+version+"/plot_merged"
dryrun = opt.dryrun


#pathin= "/eos/user/o/oiorio/Wprime/nosynch/"+version+'/plot'
#pathout = './newtest5/' + version + '/plot_merged_fix_v2'


systs_corr = ["jes", "jer", "btag", "mistag", "pdf_total", "pu", "PF", "lep", "trig"]
#systs_corr = ["PF", "lep", "trig"]
systs_uncorr = []
#systs_corr = []
#systs = ["PF", "pu", "lep", "trig", "jes", "jer", "btag", "mistag", "pdf_total", "TT_Mtt", "WJets", "ST", "TF", "DD"]

import signalsampleslist

samples=[]
splitsamples = opt.samples.split(",")
if opt.samples=="base":
    samples.extend(["Data", "WJets", "TT_Mtt", "ST", "QCD", "WP_M2000W20_RH", "WP_M3000W30_RH", "WP_M4000W40_RH", "WP_M5000W50_RH", "WP_M6000W60_RH"])
if "WP_RH" in splitsamples:
    samples.extend(signalsampleslist.RH_samples)
    splitsamples.remove("WP_RH")
if "WP_LHSMinter" in splitsamples:
    samples.extend(signalsampleslist.LHSMinter_samples)
    splitsamples.remove("WP_LHSMinter")
if "WP_LRSMinter" in splitsamples:
    samples.extend(signalsampleslist.LRSMinter_samples)
    splitsamples.remove("WP_LRSMinter")

#print (splitsamples)
samples.extend(splitsamples)
#print (samples)


print "samples are ",  samples
missingSamplesFile=opt.missing
fmiss=file(missingSamplesFile)
missingSamplesList=(fmiss.read()).split()

for sample in samples:
    print "sample:", sample
    for missingSample in missingSamplesList:
        print "missing sample ", missingSample
        if sample in missingSample:
            
            print ("\nsample: "+sample+" has one of the years in missing samples list-skipping! List is: ")
            print (missingSamplesList)
            samples.remove(sample)
    
print ("\n\nsamples to run:\n\n",samples)
#exit()
#systs2 = ["PF", "pu", "lep", "trig", "jes", "jer", "btag", "mistag", "pdf_total"]



#systs_corr =["pdf_total"]
#samples=["WP_M6000W60_RH"]

versus = ['Up', 'Down']
leps = ['muon', 'electron']
leps = ['muon']
leps = ['electron','muon']
years = ['2016', '2017', '2018']
if os.path.exists(pathout):
#    os.popen('rm -r '+ pathout + '/*')
    print "path exists, not recreating it"
else:
    if(not dryrun):os.makedirs(pathout)

for lep in leps:
    if os.path.exists(pathout+"/"+lep):
        print "path for "+lep+" exists, not recreating it"
    else:
        if(not dryrun):os.makedirs(pathout + '/' + lep)
    command = 'hadd -f ' + pathout + '/' + lep + '/Data_2020_' + lep + '.root '
    commandrm = 'rm ' + pathin + '/' + lep + '/Data*_201*_' + lep + '_*.root '
    for year in years:
        command += pathin + '/' + lep + '/Data*_' + year + '_' + lep + '.root '
        print(commandrm)
        #os.system(commandrm)
    #print(command)
    if(not dryrun):os.system(command)

#sommare tutti gli anni
nparallel = opt.parallel
parallelize= (nparallel>1)
nplot=0
extrastring=''
for lep in leps:
    for sample in samples:
        if 'Data' in sample:
            continue 
        command = 'hadd -f ' + pathout + '/' + lep + '/' + sample + '_2020_' + lep + '.root ' 
        for year in years:
            command += ' ' + pathin + '/' + lep + '/' + sample + '_' + year + '_' + lep + '.root'
        nplot=nplot+1
        extrastring = '' if ( nplot%nparallel==0) else ' & ' 
        if(not dryrun): os.system(command + extrastring)
        print(command+extrastring)
        print ######### fine nominal #########
        for syst in systs_corr:
            for vs in versus:
                command = 'hadd -f ' + pathout + '/' + lep + '/' + sample + '_2020_' +  lep + '_' + syst + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2016_' + lep + '_' + syst + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2017_' + lep + '_' + syst + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2018_' + lep + '_' + syst + vs +'.root'
                nplot=nplot+1
                extrastring = '' if ( nplot%nparallel==0) else ' & ' 
                if(not dryrun): os.system(command + extrastring)
                print(command+extrastring)
        
        year = '2016'
        for syst in systs_uncorr:
            for vs in versus:
                command = 'hadd -f ' + pathout + '/' + lep + '/' + sample + '_2020_' +  lep + '_' + syst + year + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_' + year + '_' + lep + '_' + syst + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2017_' + lep + '.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2018_' + lep + '.root'
                nplot=nplot+1
                extrastring = '' if ( nplot%nparallel==0) else ' & ' 
                if(not dryrun): os.system(command + extrastring)
                print(command+extrastring)

        print ######### fine 2016 #########
        year = '2017'
        for syst in systs_uncorr:
            for vs in versus:
                command = 'hadd -f ' + pathout + '/' + lep + '/' + sample + '_2020_' +  lep + '_' + syst + year + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2016_' + lep + '.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_' + year + '_' + lep + '_' + syst + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2018_' + lep + '.root'
                nplot=nplot+1
                extrastring = '' if ( nplot%nparallel==0) else ' & ' 
                if(not dryrun): os.system(command + extrastring)
                print(command+extrastring)

        year = '2018'
        for syst in systs_uncorr:
            for vs in versus:
                command = 'hadd -f ' + pathout + '/' + lep + '/' + sample + '_2020_' +  lep + '_' + syst + year + vs +'.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2016_' + lep + '.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_2017_' + lep + '.root'
                command += ' ' + pathin + '/' + lep + '/' + sample + '_' + year + '_' + lep + '_' + syst + vs +'.root'
                nplot=nplot+1
                extrastring = '' if ( nplot%nparallel==0) else ' & ' 
                if(not dryrun): os.system(command + extrastring)
                print(command+extrastring)


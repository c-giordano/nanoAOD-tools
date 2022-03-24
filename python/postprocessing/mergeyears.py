import os,optparse
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *

usage = 'python mergeyears.py -i inputpath -o outpath -v version'
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

pathin = opt.inputpath 
pathout = opt.outputpath 

version = opt.version

pathin = opt.inputpath +"/"+version+"/plot"
pathout = opt.outputpath+"/"+version+"/plot_merged"
dryrun = opt.dryrun

systs_corr = ["jes", "jer", "btag", "mistag", "pdf_total", "pu", "PF", "lep", "trig"]
systs_corr.extend(["LHE"])
systs_uncorr = []

samples = []
splitsamples = opt.samples.split(",")
if opt.samples=="base":
    samples.extend(["Data", "WJets", "TT_Mtt", "ST", "QCD"])
if "WP_RH" in splitsamples:
    samples.extend(sample.label.replace('_2016', '') for sample in sample_dict['WP_RH_2016'].components)
    splitsamples.remove("WP_RH")
if "WP_LHSMinter" in splitsamples:
    samples.extend(sample.label.replace('_2016', '') for sample in sample_dict['WP_LHSMinter_2016'].components)
    splitsamples.remove("WP_LHSMinter")
if "WP_LRSMinter" in splitsamples:
    samples.extend(sample.label.replace('_2016', '') for sample in sample_dict['WP_LRSMinter_2016'].components)
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

versus = ['Up', 'Down']
leps = ['muon', 'electron']
years = ['2016', '2017', '2018']
if os.path.exists(pathout):
#    os.popen('rm -r '+ pathout + '/*')
    print "path exists, not recreating it"
else:
    if(not dryrun):os.makedirs(pathout)

for lep in leps:
    if not os.path.exists(pathout+"/"+lep):
        if(not dryrun):os.makedirs(pathout+"/"+lep)

for lep in leps:
    if not "Data" in sample:
        continue
    if os.path.exists(pathout+"/"+lep):
        print "path for "+lep+" exists, not recreating it"
    else:
        if(not dryrun):os.makedirs(pathout + '/' + lep)
    command = 'hadd -f ' + pathout + '/' + lep + '/Data_2020_' + lep + '.root '
    commandrm = 'rm ' + pathin + '/' + lep + '/Data*_201*_' + lep + '_*.root '
    for year in years:
        command += pathin + '/' + lep + '/Data*_' + year + '_' + lep + '.root '
        #print(commandrm)
        #os.system(commandrm)
    #print(command)
    if(not dryrun):os.system(command)

#sommare tutti gli anni
nparallel = opt.parallel
parallelize = (nparallel>1)
nplot = 0
extrastring = ''
systs_splitbysample={"LHE":["TT_Mtt","WJets","QCD","ST"]}
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
            splitbysample=""
            for vs in versus:
                if(syst in systs_splitbysample.keys()): 
                    splitbysample=sample
                    
                command = 'hadd -f ' + pathout + '/' + lep + '/' + sample + '_2020_' +  lep + '_' + syst+splitbysample + vs +'.root'
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

    #here we copythe nominal sample YY to the XXLHEUp/Down , e.g. WJets_TT_MTTLHEUp is put to nominal
print ("pcche")
nplot=0
for lep in leps:
    for syst in systs_splitbysample.keys():
        for sampsys in systs_splitbysample[syst]:
            for sample in samples:
                for vs in versus:
                    commandcp=""
                    if sample!=sampsys:
                        commandcp = 'cp ' + pathout + '/' + lep + '/' + sample + '_2020_' +  lep +'.root'
                        commandcp += ' ' + pathout + '/' + lep + '/' + sample + '_2020_' + lep + "_"+syst + sampsys+ vs+'.root'
                        nplot=nplot+1
                        extrastring = '' if ( nplot%nparallel==0) else ' & ' 
                        if(not dryrun): os.system(commandcp + extrastring)
                        print(commandcp+extrastring)

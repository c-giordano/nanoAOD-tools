import os
import shutil
import optparse
import copy
from symmetry import symmetry,nnpdfeval
from repos import histosr,histocr,extrasr,extracr
from fit_utils import shift,smoothing,scale
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *

pi = '/afs/cern.ch/work/o/oiorio/Wprimean/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/python/postprocessing/newtest5/v17_explin/'
po = '/afs/cern.ch/work/o/oiorio/Wprimean/CMSSW_10_5_0/src/PhysicsTools/NanoAODTools/python/postprocessing/newtest5/v17_explin_fit/'

usage = "python preparefit.py -l muon,electron -i pathinput -o pathoutput -v v17 -y 2016,2017,2018"
parser = optparse.OptionParser(usage)
parser.add_option('--years','-y', dest='years', default = '2016,2017,2018', type='string', help='years to run')
parser.add_option('-l', '--lep', dest='leptons', default = 'muon,electron', type='string', help='lepton to run')
parser.add_option('-v', '--version', dest='version', default = 'v18', type='string', help='analysis version')
parser.add_option('-i', '--inputpath', dest='inputpath', default = pi, type='string', help='file in , not working yet!')
parser.add_option('-o', '--outputpath', dest='outputpath', default = po, type='string', help='file in , not working yet!')
parser.add_option('-n', '--dryrun', dest='dryrun', action= 'store_true' , default = False, help='if called not running the command')
parser.add_option('-m', '--mode', dest='mode',default = 'sum symmetrize smooth pdfeval' , type='string', help='"sum" splits systs per years, "symmetrize" symmetrizes DD uncertainties, "smooth" smooths QCD histograms')
parser.add_option('--parallel', dest='parallel', type='int', default=1 , help='if called run on more than 1 plot simultaneously')
parser.add_option('-r', '--refresh', dest='refresh', action= 'store_true' , default = False, help='if called empty the output folders first')
parser.add_option('-e','--extraregions', dest='extraregions', action="store_true", default = False, help='use extra regions for later recorrection')
parser.add_option('-M', '--missingSamplesFile', dest='missing', default = 'missingSamples.txt', type='string', help='missing samples file')
parser.add_option('', '--splitregions', dest='splitregions', action= 'store_true' , default = False, help='split systs. for signal and control regions')
#parser.add_option('--cut','-c', dest='cuts', default = '', type='string', help='years to run')
(opt, args) = parser.parse_args()

extended = opt.extraregions
version = opt.version
pathin = opt.inputpath 
pathout = opt.outputpath
dryrun = opt.dryrun
missingSamplesFile=opt.missing
fmiss=file(missingSamplesFile)
missingSamplesList=(fmiss.read()).split()
leps = opt.leptons.split(',')
years = opt.years.split(',')
mode = opt.mode
splitddreg=opt.splitregions

signals = {}
signals['RH2016'] = [sample.label.replace('_2016', '') for sample in sample_dict['WP_RH_2016'].components]
signals['RH2017'] = [sample.label.replace('_2017', '') for sample in sample_dict['WP_RH_2017'].components]
signals['RH2018'] = [sample.label.replace('_2018', '') for sample in sample_dict['WP_RH_2018'].components]
signals['LHSMinter2016'] = [sample.label.replace('_2016', '') for sample in sample_dict['WP_LHSMinter_2016'].components]
signals['LHSMinter2017'] = [sample.label.replace('_2017', '') for sample in sample_dict['WP_LHSMinter_2017'].components]
signals['LHSMinter2018'] = [sample.label.replace('_2018', '') for sample in sample_dict['WP_LHSMinter_2018'].components]
#print(signals)

for s in signals['LHSMinter2016']:
    if (s+"_2016" in missingSamplesList) or (s+"_2017" in missingSamplesList) or (s+"_2018" in missingSamplesList):
        signals['LHSMinter2016'].remove(s)
        for lep in leps:
            os.system("rm "+pathout+"/"+lep+"/"+s+"*.root")
            print("removing "+pathout+"/"+lep+"/"+s+"*.root")

for s in signals['RH2016']:
    if (s+"_2016" in missingSamplesList) or (s+"_2017" in missingSamplesList) or (s+"_2018" in missingSamplesList):
        signals['RH2016'].remove(s)
        for lep in leps:
            os.system("rm "+pathout+"/"+lep+"/"+s+"*.root")
            print("removing "+pathout+"/"+lep+"/"+s+"*.root")

baseFit=False
#baseFit=True
if(baseFit):
    signals['LHSMinter2016']=[]
    signals['RH2016']=["WP_M"+str(x)+"000W"+str(x)+"0_RH" for x in range(2,7)]

listdd=["TF_2020", "DD_2020", "Alt_2020", "AltTF_2020"]
crlist=["CR_2020"]

#splitddreg=False
if(splitddreg):
    newlistdd=[]
    for l in listdd:
        newlistdd.append(l.replace("_2020","_SR2B_2020"))
        newlistdd.append(l.replace("_2020","_SRT_2020"))
        newlistdd.append(l.replace("_2020","_SRW_2020"))
        newlistdd.append(l.replace("_2020","_CR0B_2020"))
    listdd= copy.deepcopy(newlistdd)
    crlist=["CR_SR2B_2020" ,
            "CR_SRW_2020" ,
            "CR_SRT_2020" ,
            "CR_CR0B_2020" ]

allhistos = histosr#+histocr
if(extended):
    allistos = allhistos#+extrasr+extracr
if os.path.exists(pathout):
    if opt.refresh:
        os.popen('rm -r '+ pathout + '/*')
        print('folder ' + pathout + " cleared") 
else:
    os.makedirs(pathout)

summedyears = False
splityears = False
smooth = False
symmetrize = False
pdfeval = False
if 'sum' in mode: 
    summedyears = True
if 'splityears' in mode: 
    splityears = True
if 'smooth' in mode:
    smooth = True
if 'symmetrize' in mode:
    symmetrize = True
if 'pdfeval' in mode:
    pdfeval = True

###################################
# Definition of systs collections #
###################################
systs = ["jes2016", "jer2016", "jes2017", "jer2017", "jes2018", "jer2018", "btag", "mistag", "pdf_total", "pu", "PF", "LHETT_Mtt", "LHEWJets", "LHEST", "LHEQCD"]
systs_DD = listdd+["TT_Mtt", "WJets", "ST"]
#systs_DD_nolep = ["jes2016", "jer2016", "jes2017", "jer2017", "jes2018", "jer2018", "btag", "mistag", "pdf_total", "pu", "PF", "LHETT_Mtt", "LHEWJets", "LHEST", "LHEQCD"]
if extended: systs_DD.extend(crlist)
systs_perlep = ["lep", "trig"]
systs_smooth = systs + systs_perlep
systs_symmetrize = systs + systs_DD + systs_perlep

#####################################
# Definition of samples collections #
#####################################
samples_symmetrize = ["DDFitWJetsTT_MttST"]
samples_pdfeval = signals['LHSMinter2016']+signals['RH2016']

versus = ['Up', 'Down']

for lep in leps:
    if not os.path.exists(pathout+"/"+lep):os.makedirs(pathout + '/' + lep)
    os.system("cp " + pathin.replace("plot_merged", "") + "plot_explin/" + lep + "/DDFit* " + pathin + "/" +lep + "/" )
    if not summedyears:
        if splityears:
            for year in years:
                samples += signals['RH'+year] + signals['LHSMinter'+year]
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

                samples2 += signals['RH'+year] + signals['LHSMinter'+year]
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
        #systs = ["jes2016", "jer2016", "jes2017", "jer2017", "jes2018", "jer2018", "btag", "mistag", "pdf_total", "pu", "PF", "LHETT_Mtt", "LHEWJets", "LHEST", "LHEQCD"]
        #systs_DD = listdd+["TT_Mtt", "WJets", "ST"]
        #systs_DD_nolep = ["jes2016", "jer2016", "jes2017", "jer2017", "jes2018", "jer2018", "btag", "mistag", "pdf_total", "pu", "PF", "LHETT_Mtt", "LHEWJets", "LHEST", "LHEQCD"]
        #if extended: systs_DD.extend(crlist)
        #systs_perlep = ["lep", "trig"]

        filename = 'Data_2020_' + lep + '.root'
        print('copying ', filename)
        shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)

        samples = ["DDFitWJetsTT_MttST"]
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

        samples2 = ["QCD"] + samples 
        samples2 += signals['RH2016'] + signals['LHSMinter2016']
        #samples2 = ['WP_M5800W58_LHSMinter', 'WP_M6000W60_LHSMinter']
        #samples2 = ["DDFitWJetsTT_MttST"]
        for sample in samples2:
            filename = sample + '_2020_' + lep + '.root'
            print('copying ', filename)
            shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)
            print(systs)
            for syst in systs:
                for vs in versus:
                    filename = sample + '_2020_' + lep + '_' + syst + vs + '.root'
                    print('copying ', pathin + '/' + lep + '/' + filename, " in ", pathout +  '/' + lep + '/' + filename)
                    shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + filename)
            print(systs_perlep)
            for syst in systs_perlep:
                for vs in versus:
                    filename = sample + '_2020_' + lep + '_' + syst + vs + '.root'
                    if lep == 'muon':
                        fileout = sample + '_2020_' + lep + '_' + syst + '_mu' + vs + '.root'
                    else:
                        fileout = sample + '_2020_' + lep + '_' + syst + '_ele' + vs + '.root'
                    #print('copying ', filename)
                    print('copying ', pathin + '/' + lep + '/' + filename, " in ", pathout +  '/' + lep + '/' + fileout)
                    shutil.copyfile(pathin + '/' + lep + '/' + filename, pathout +  '/' + lep + '/' + fileout)
    if(smooth):
        #samples_smooth = ["DDFitWJetsTT_MttST"]
        samples_smooth = {"QCD":allhistos}
        for sample in samples_smooth:
            filename = sample + '_2020_' + lep + '.root'
            fileout = pathout+'/'+lep+'/'+filename
            print(" nominal fileout ",fileout)
            for h in samples_smooth[sample]:
                filename = sample + '_2020_' + lep + '.root'
                fileout = pathout+'/'+lep+'/'+filename
                print("sample ",sample , " syst nominal histo ",h, " fileout ",fileout)
                smoothing(fileout,h)
                for syst in systs_smooth:
                    print("sample ",sample , " syst " , syst, " histo ",h)
                    for vs in versus:
                        if(syst in systs):
                            filename = sample + '_2020_' + lep + '_' + syst + vs + '.root'
                        if(syst in systs_DD):
                            filename = sample + '_2020_' + lep + '_' + syst + vs + '.root'
                            if lep == 'muon':
                                filename = sample + '_2020_' + lep + '_' + syst + '_mu' + vs + '.root'
                            else:
                                filename = sample + '_2020_' + lep + '_' + syst + '_ele' + vs + '.root'
                                    
                        if(syst in systs_perlep):
                            for vs in versus:
                                filename = sample + '_2020_' + lep + '_' + syst + vs + '.root'
                                if lep == 'muon':
                                    filename = sample + '_2020_' + lep + '_' + syst + '_mu' + vs + '.root'
                                else:
                                    filename = sample + '_2020_' + lep + '_' + syst + '_ele' + vs + '.root'
                                                        
                        fileout = pathout+'/'+lep+'/'+filename
                        print("smoothing file ", fileout)
                        smoothing(fileout,h)
    
    if(symmetrize):
        print "symmetrizing"
        if extended: systs_symmetrize.extend(crlist)
        for sample in samples_symmetrize:
            #print "sample to smooth ",sample, " histograms:"
            filename = sample + '_2020_' + lep + '.root'
            filenameUp = sample + '_2020_' + lep + '.root'
            filenameDown = sample + '_2020_' + lep + '.root'
            
            fileout = pathout+'/'+lep+'/'+filename
            symmetry(histosr,fUp=fileout,fDown=fileout,fNom=fileout,version="cureZeros")
                                
            for syst in systs_symmetrize:
                print(" symmetrizing ",histosr , sample , syst)
                if(syst in systs):
                    filenameUp = sample + '_2020_' + lep + '_' + syst + "Up" + '.root'
                    filenameDown = sample + '_2020_' + lep + '_' + syst + "Down" + '.root'
                if(syst in systs_DD):
                    if lep == 'muon':
                        filenameUp = sample + '_2020_' + lep + '_' + syst + '_mu' + "Up" + '.root'
                        filenameDown = sample + '_2020_' + lep + '_' + syst + '_mu' + "Down" + '.root'
                    else:
                        filenameUp = sample + '_2020_' + lep + '_' + syst + '_ele' + "Up" + '.root'
                        filenameDown = sample + '_2020_' + lep + '_' + syst + '_ele' + "Down" + '.root'
                if(syst in systs_perlep):
                    if lep == 'muon':
                        filenameUp = sample + '_2020_' + lep + '_' + syst + '_mu' + "Up"+ '.root'
                        filenameDown = sample + '_2020_' + lep + '_' + syst + '_mu' + "Down" + '.root'
                    else:
                        filenameUp = sample + '_2020_' + lep + '_' + syst + '_ele' + "Up" + '.root'
                        filenameDown = sample + '_2020_' + lep + '_' + syst + '_ele' + "Down" + '.root'
                fileout = pathout+'/'+lep+'/'+filename
                fileoutUp = pathout+'/'+lep+'/'+filenameUp
                fileoutDown = pathout+'/'+lep+'/'+filenameDown
                symoption="switch"
                symoption=""
                if(("CR_CR" in syst) or ("CR_SR" in syst)):
                    symoption="switch"
                if(("TT_Mtt" in syst) or ("WJets" in syst) or ("ST" in syst ) or ("Alt" in syst)):# or ("TF" in syst) or ("DD" in syst) ):
                    symoption="switch"
                print("symmetry file,up,down ", fileoutUp,fileoutDown,fileout, " option ")
                symmetry(histosr,fUp=fileoutUp,fDown=fileoutDown,fNom=fileout,option = symoption)

    if(pdfeval):
        print "evaluating pdf"
        #samples_pdfeval = ['WP_M5800W58_LHSMinter', 'WP_M6000W60_LHSMinter']
        for sample in samples_pdfeval:
            #print "sample to smooth ",sample, " histograms:"
            filename = sample + '_2020_' + lep + '.root'
            filenameUp = sample + '_2020_' + lep + '_pdf_totalUp.root'
            filenameDown = sample + '_2020_' + lep + '_pdf_totalDown.root'
            filenameRMS  = sample + '_2020_' + lep + '_pdf_RMS.root'
            
            fileout = pathout+'/'+lep+'/'+filename
            fileoutUp = pathout+'/'+lep+'/'+filenameUp
            fileoutDown = pathout+'/'+lep+'/'+filenameDown
            fileoutRMS = pathout+'/'+lep+'/'+filenameRMS

            filein = pathin+'/'+lep+'/'+filename
            fileinUp = pathin+'/'+lep+'/'+filenameUp
            fileinDown = pathin+'/'+lep+'/'+filenameDown
            os.system("cp "+filein+" "+fileout)
            os.system("cp "+fileinUp+" "+fileoutUp)
            os.system("cp "+fileinDown+" "+fileoutDown)
            os.system("cp "+fileoutUp+" "+fileoutRMS)

            nnpdfeval(histosr,fUp=fileoutUp,fDown=fileoutDown,fNom=fileout,fRMS=fileoutRMS)


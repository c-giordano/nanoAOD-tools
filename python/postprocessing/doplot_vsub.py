import os,optparse,commands,subprocess

usage = 'python doplot.py'
parser = optparse.OptionParser(usage)
parser.add_option('--years','-y', dest='years', default = '2016,2017,2018', type='string', help='years to run')
parser.add_option('-S', '--syst', dest='syst', default = 'all', type='string', help='syst to run, options are: all,noSyst, or a specific systeamtic')
parser.add_option('-l', '--lep', dest='leptons', default = 'muon,electron', type='string', help='lepton to run')
parser.add_option('-v', '--version', dest='version', default = 'v17', type='string', help='analysis version')
parser.add_option('-i', '--inputpath', dest='inputpath', default = '/eos/user/a/adeiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-o', '--outputpath', dest='outputpath', default = '/eos/user/o/oiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-m', '--mode', dest='mode',default = 'fit' , type='string', help='type of plots to do: fit (only plot for mWprime) ')
parser.add_option('-n', '--dryrun', dest='dryrun', action= 'store_true' , default = False, help='if called not running the command')
parser.add_option('--parallel', dest='parallel', type='int', default=1 , help='if called run on more than 1 plot simultaneously')
#parser.add_option('--cut','-c', dest='cuts', default = '', type='string', help='years to run')

(opt, args) = parser.parse_args()

dryrun = opt.dryrun

inputpath=opt.inputpath
outputpath=opt.outputpath


nparallel = opt.parallel
parallelize= (nparallel>1)

version=opt.version
leptons=opt.leptons.split(',')
years=opt.years.split(',')

systlist=["all"]
if opt.syst=="all":
    systs=systlist
elif opt.syst=="noSyst":
    systs=["noSyst"]
else:
    systs=opt.syst.split(',')



regionCuts={"SR2B":"best_topjet_isbtag&&best_Wpjet_isbtag" }#cuts for the main SR/CR regions
#regionCuts["SRT"]="best_topjet_isbtag&&best_Wpjet_isbtag==0"
#regionCuts["SRW"]="best_topjet_isbtag==0&&best_Wpjet_isbtag"
#regionCuts["CR0B"]="best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"

centralCut="&&best_top_m>120&&best_top_m<220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
regionIcut="&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"

ctrlCuts={"SR2B":["&&best_top_m>120&&best_top_m<220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60",
                  "&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60",
                  "&&best_top_m>340&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>30" ]}#cuts for the BKG extraction cuts
ctrlCuts["CR0B"]=[centralCut,regionIcut]
ctrlCuts["SRW"]=[centralCut,regionIcut]
ctrlCuts["SRT"]=[centralCut,regionIcut]

nplot=0
extrastring=''
processes=[]
for r,rc in regionCuts.iteritems():
    for c,cc in ctrlCuts.iteritems():
        for ccc in cc:
            bigcut=rc+ccc
            for y in years:
                for l in leptons:
                    for s in systs:
                        print( "year ",y,"lepton",l ,"syst",s)
                        print ("big cut", bigcut)
                        if(parallelize):
                            nplot=nplot+1
                            extrastring = ' & '
                            if nplot%nparallel==0 or nplot%(len(years)*len(systs)*len(leptons))==0:
                                extrastring=';wait '
                        cmd='python makeplot.py -i '+inputpath+' -o '+outputpath+' -y '+y+' -L '+l + ' --sel -f '+version+' -C "'+bigcut+'" --plot -s -S '+s+' '+ extrastring
                        processes.append(subprocess.)
                        print ("command is ",cmd)
                        if not dryrun:
                            os.system(cmd)
                        

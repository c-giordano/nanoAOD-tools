import os,optparse,commands

usage = 'python doplot.py'
parser = optparse.OptionParser(usage)
parser.add_option('--years','-y', dest='years', default = '2016,2017,2018', type='string', help='years to run')
parser.add_option('-S', '--syst', dest='syst', default = 'all', type='string', help='syst to run, options are: all,noSyst, or a specific systeamtic')
parser.add_option('-l', '--lep', dest='leptons', default = 'muon,electron', type='string', help='lepton to run')
parser.add_option('-v', '--version', dest='version', default = 'v17', type='string', help='analysis version')
parser.add_option('-i', '--inputpath', dest='inputpath', default = '/eos/user/a/adeiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-o', '--outputpath', dest='outputpath', default = '/eos/user/o/oiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-n', '--dryrun', dest='dryrun', action= 'store_true' , default = False, help='if called not running the command')

parser.add_option('-m', '--mode', dest='mode',default = 'fit sr cr' , type='string', help='type of plots to do: fit (only plot for mWprime, no stack), plot (plot AN variables), stack (stack after plotting) ')
parser.add_option('--parallel', dest='parallel', type='int', default=1 , help='if called run on more than 1 plot simultaneously')
#parser.add_option('--cut','-c', dest='cuts', default = '', type='string', help='years to run')

(opt, args) = parser.parse_args()

dryrun = opt.dryrun

inputpath=opt.inputpath
outputpath=opt.outputpath


nparallel = opt.parallel
parallelize= (nparallel>1)

doFitPlot=("fit" in opt.mode)
doPlot=("plot" in opt.mode)
doStack=("stack" in opt.mode)

version=opt.version
leptons=opt.leptons.split(',')
years=opt.years.split(',')

systlist=["all"]
systlist = ["noSyst", "jesUp",  "jesDown",  "jerUp",  "jerDown", "PFUp", "PFDown", "puUp", "puDown", "btagUp", "btagDown", "mistagUp", "mistagDown", "lepUp", "lepDown", "trigUp", "trigDown", "pdf_totalUp", "pdf_totalDown", "q2Up", "q2Down"]
if opt.syst=="all":
    systs=systlist
elif opt.syst=="noSyst":
    systs=["noSyst"]
else:
    systs=opt.syst.split(',')


regionCuts={}#Cuts for the main regions

ctrlCuts={}#Cuts for the background extraction sub-regions
centralCut="&&best_top_m>120&&best_top_m<220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
regionIcut="&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"

if("sr" in opt.mode):
    regionCuts["SR2B"]="best_topjet_isbtag&&best_Wpjet_isbtag" #cuts for the main SR/CR regions
    regionCuts["SRT"]="best_topjet_isbtag&&best_Wpjet_isbtag==0"
    regionCuts["SRW"]="best_topjet_isbtag==0&&best_Wpjet_isbtag"
    ctrlCuts["SR2B"]=["&&best_top_m>120&&best_top_m<220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60",
                  "&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60",
                  "&&best_top_m>340&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>30" ]#cuts for the BKG extraction cuts

    ctrlCuts["SRW"]=[centralCut,regionIcut]
    ctrlCuts["SRT"]=[centralCut,regionIcut]

if("cr" in opt.mode):
    regionCuts["CR0B"]="best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"
    ctrlCuts["CR0B"]=[centralCut,regionIcut]

samples=""
signalsamples=[ "WP_M"+str(x)+"000W"+str(x)+"0_RH_2017" for x in xrange(2,7)]
samples=",".join(signalsamples)y
print("samples= ",samples)
if samples!="":
    samplescommand=" -d "+samples+" "
nplot=0
extrastring=''
#only plotting part
for r,rc in regionCuts.iteritems():
    cc =ctrlCuts[r]
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
                        nparallelcheck = min(nparallel, len(years)*len(systs)*len(leptons))
                        if nplot%nparallelcheck==0:
                            extrastring='; sleep 2'
                    cmd='python makeplot.py -i '+inputpath+' -o '+outputpath+' -y '+y+' -L '+l + samplescommand +' --sel -f '+version+' -C "'+bigcut+'" --plot -S '+s+' '+ extrastring
                    print ("command is ",cmd)
                    if (not dryrun) and doPlot or doFitPlot:
                        os.system(cmd)
                        
nplot=0
extrastring=''
#only stacking part
for r,rc in regionCuts.iteritems():
    cc =ctrlCuts[r]
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
                        nparallelcheck = min(nparallel, len(years)*len(systs)*len(leptons))
                        if nplot%nparallelcheck==0:
                            extrastring='; sleep 10'
                    cmd='python makeplot.py -i '+inputpath+' -o '+outputpath+' -y '+y+' -L '+l + ' --sel -f '+version+' -C "'+bigcut+'" -S '+s+' '+ extrastring
                    print ("command is ",cmd)
                    if (not dryrun) and doStack :
                        os.system(cmd)
                        

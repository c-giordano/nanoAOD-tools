import os,optparse,commands

usage = 'python doplot.py'
parser = optparse.OptionParser(usage)
parser.add_option('--years','-y', dest='years', default = '2016,2017,2018', type='string', help='years to run')
parser.add_option('-S', '--syst', dest='syst', default = 'all', type='string', help='syst to run, options are: all,noSyst, or a specific systeamtic')
parser.add_option('-l', '--lep', dest='leptons', default = 'muon,electron', type='string', help='lepton to run')
parser.add_option('-v', '--version', dest='version', default = 'v18', type='string', help='analysis version')
parser.add_option('-i', '--inputpath', dest='inputpath', default = '/eos/user/a/adeiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-o', '--outputpath', dest='outputpath', default = '/eos/user/o/oiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-n', '--dryrun', dest='dryrun', action= 'store_true' , default = False, help='if called not running the command')
parser.add_option('-t', '--tag', dest='tag', type='string', default = '', help="version of the signal region naming convention ")

parser.add_option('-m', '--mode', dest='mode',default = 'fit sr cr' , type='string', help='type of plots to do: fit (only plot for mWprime, no stack), plot (plot AN variables), stack (stack after plotting) ')
parser.add_option('--parallel', dest='parallel', type='int', default=1 , help='if called run on more than 1 plot simultaneously')


signalsamples=[ "WP_M"+str(x)+"000W"+str(x)+"0_RH_2017" for x in xrange(2,7)]
samples=""
#samples=",".join(signalsamples)
parser.add_option('-d', '--samples', dest='samples', default = samples, type='string', help='samples to run, default all')


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
doMerge=("mer" in opt.mode)

version=opt.version
leptons=opt.leptons.split(',')
years=opt.years.split(',')

systlist=["all"]
systlist = ["noSyst", "jesUp",  "jesDown",  "jerUp",  "jerDown", "PFUp", "PFDown", "puUp", "puDown", "btagUp", "btagDown", "mistagUp", "mistagDown", "lepUp", "lepDown", "trigUp", "trigDown", "pdf_totalUp", "pdf_totalDown"]
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
regionIIcut="&&best_top_m<220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
regionIIIcut="&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
tagRegions={}

tagversion=opt.tag


regionIcutSR2B="&&best_top_m>340&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>30" #cuts for the BKG extraction cuts

if("sr" in opt.mode):
    regionCuts["SR2B"]="best_topjet_isbtag&&best_Wpjet_isbtag" #cuts for the main SR/CR regions
    regionCuts["SRT"]="best_topjet_isbtag&&best_Wpjet_isbtag==0"
    regionCuts["SRW"]="best_topjet_isbtag==0&&best_Wpjet_isbtag"
    ctrlCuts["SR2B"]=[centralCut,regionIcut, regionIcutSR2B] #cuts for the BKG extraction cuts


    ctrlCuts["SRW"]=[centralCut,regionIcut,regionIIcut,regionIIIcut]
    ctrlCuts["SRT"]=[centralCut,regionIcut,regionIIcut,regionIIIcut]
    
    if tagversion=="v18":
        tagRegions[("SR2B",centralCut)]="SR2B"
        tagRegions[("SR2B",regionIcutSR2B)]="SR2B_I"
        tagRegions[("SR2B",regionIcut)]="SR2B_IV"

        tagRegions[("SRT",centralCut)]="SRT"
        tagRegions[("SRT",regionIcut)]="SRT_I"
        tagRegions[("SRT",regionIIcut)]="SRT_II"
        tagRegions[("SRT",regionIIIcut)]="SRT_III"
        
        tagRegions[("SRW",centralCut)]="SRW"
        tagRegions[("SRW",regionIcut)]="SRW_I"
        tagRegions[("SRW",regionIIcut)]="SRW_II"
        tagRegions[("SRW",regionIIIcut)]="SRW_III"


if("cr" in opt.mode):
    regionCuts["CR0B"]="best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"
    ctrlCuts["CR0B"]=[centralCut,regionIcut,regionIIcut,regionIIIcut]

    if tagversion=="v18":
        tagRegions[("CR0B",centralCut)]="CR0B"
        tagRegions[("CR0B",regionIcut)]="CR0B_I"
        tagRegions[("CR0B",regionIIcut)]="CR0B_II"
        tagRegions[("CR0B",regionIIIcut)]="CR0B_III"
        


#samplestorun = "WP_M5200W520_RH_2018"
samplestorun=opt.samples
print("samples= ",opt.samples)
#Need to automatize running components for the signal:
if(not doMerge and (doFitPlot or doPlot or doStack) and not samplestorun==""):
    listsamples=samplestorun.split(",") 
    import PhysicsTools.NanoAODTools.postprocessing.samples.samples as allsamples
    for l in listsamples:
        if("WP" in l):
            print("sample is: \n"+l)
            locsample= getattr(allsamples,l)
            print (" locsample label is: \n"+locsample.label)
            if hasattr(locsample,"components"):
                print(" has components: \n", locsample.components)
                comps =",".join([x.label for x in locsample.components])
                samplestorun.replace(l,comps)
                print(" to run: \n", comps)
                samplestorun = samplestorun.replace(l,comps)

#import sys
#sys.exit(100)
samplescommand=""
if samplestorun!="":
    samplescommand=" -d "+samplestorun+" "
nplot=0
extrastring=''
print "samples are ", opt.samples

print "to run",samplestorun



tagcommand=""
#only merging part
for y in years:
    if not (y in samplescommand or samplescommand==""):continue
    if(parallelize):
        nplot=nplot+1
        extrastring = ' & '
        nparallelcheck = min(nparallel, len(years) )
        if nplot%nparallelcheck==0:
            extrastring='; sleep 2'
    cmd='python makeplot.py -i '+inputpath+' -o '+inputpath+' -y '+y+' '+ samplescommand +' --sel -f '+version+' --merpart --lumi '+ extrastring
    print ("command is ",cmd)
    if (not dryrun) and doMerge:
        os.system(cmd)

nplot=0
extrastring=''
#only plotting part
for r,rc in regionCuts.iteritems():
    cc =ctrlCuts[r]
    for ccc in cc:
        bigcut=rc+ccc
        for y in years:
            if not (y in samplescommand or samplescommand==""):continue#            if not y in samplescommand:continue
            for l in leptons:
                for s in systs:
                    print( "year ",y,"lepton",l ,"syst",s)
                    print ("big cut", bigcut)
                    if tagversion!="":
                        tagcommand=" -t "+tagRegions[(r,ccc)]
                        print ("tagcommand is ", tagcommand)                      
                    if(parallelize):
                        nplot=nplot+1
                        extrastring = ' & '
                        nparallelcheck = min(nparallel, len(years)*len(systs)*len(leptons))
                        if nplot%nparallelcheck==0:
                            extrastring='; sleep 2'
                    cmd='python makeplot.py -i '+inputpath+' -o '+outputpath+' -y '+y+' -L '+l + samplescommand + tagcommand+' --sel -f '+version+' -C "'+bigcut+'" --plot -S '+s+' '+ extrastring
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
            if not (y in samplescommand or samplescommand==""):continue
#            if not y in samplescommand:continue
            for l in leptons:
                for s in systs:
                    print( "year ",y,"lepton",l ,"syst",s)
                    print ("big cut", bigcut)
                    if tagversion!="":
                        tagcommand=" -t "+tagRegions[(r,ccc)]
                        print ("tagcommand is ", tagcommand)                      
                    if(parallelize):
                        nplot=nplot+1
                        extrastring = ' & '
                        nparallelcheck = min(nparallel, len(years)*len(systs)*len(leptons))
                        if nplot%nparallelcheck==0:
                            extrastring='; sleep 10'
                    cmd='python makeplot.py -i '+inputpath+' -o '+outputpath+' -y '+y+' -L '+l + samplescommand + tagcommand + ' --sel -f '+version+' -C "'+bigcut+'" -S '+s+' '+ extrastring
                    print ("command is ",cmd)
                    if (not dryrun) and doStack :
                        os.system(cmd)
                        

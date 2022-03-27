import os,optparse,commands,time
from ROOT import TFile
#import ROOT
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
parser.add_option('', '--varset', dest='varset', type='string', default = '', help="variables set: S: signal, V: validation, A: AN")
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
doCheck=("check" in opt.mode)
doReplot=("rep" in opt.mode)

version=opt.version
leptons=opt.leptons.split(',')
years=opt.years.split(',')

validationvars=("V" in opt.varset)
signalvars=("S" in opt.varset)
plotAN=("A" in opt.varset)

varsetcommand=opt.varset
if varsetcommand!="":
    varsetcommand=" --varset "+opt.varset

systlist=["all"]
systlist = ["noSyst", "jesUp",  "jesDown",  "jerUp",  "jerDown", "PFUp", "PFDown", "puUp", "puDown", "btagUp", "btagDown", "mistagUp", "mistagDown", "lepUp", "lepDown", "trigUp", "trigDown", "pdf_totalUp", "pdf_totalDown"]
if opt.syst=="all":
    systs=systlist
elif opt.syst=="noSyst":
    systs=["noSyst"]
elif opt.syst=="extra":
    systs = ["mistagUp", "mistagDown","pdf_totalUp", "pdf_totalDown","LHEUp","LHEDown"]
else:
    systs=opt.syst.split(',')

regionCuts={}#Cuts for the main regions

ctrlCuts={}#Cuts for the background extraction sub-regions
centralCut= "&&best_top_m>120&&best_top_m<220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
regionIIcut="&&best_top_m>120&&best_top_m<220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
regionIcut=  "&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
regionIIIcut="&&best_top_m>220&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>60"
regionVcut="&&best_top_m<120&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD<60"
tagRegions={}

tagversion=opt.tag


regionIcutSR2B="&&best_top_m>340&&deltaR_bestWAK4_closestAK8<0.4&&WprAK8_mSD>30" #cuts for the BKG extraction cuts

if("sr" in opt.mode):
    regionCuts["SR2B"]="best_topjet_isbtag&&best_Wpjet_isbtag" #cuts for the main SR/CR regions
    regionCuts["SRT"]="best_topjet_isbtag&&best_Wpjet_isbtag==0"
    regionCuts["SRW"]="best_topjet_isbtag==0&&best_Wpjet_isbtag"
    ctrlCuts["SR2B"]=[centralCut,regionIcut, regionIcutSR2B,regionVcut] #cuts for the BKG extraction cuts
    ctrlCuts["SRW"]=[centralCut,regionIcut,regionIIcut,regionIIIcut,regionVcut]
    ctrlCuts["SRT"]=[centralCut,regionIcut,regionIIcut,regionIIIcut,regionVcut]
    
    if "v18" in tagversion:
        tagRegions[("SR2B",centralCut)]="SR2B"
        tagRegions[("SR2B",regionIcutSR2B)]="SR2B_I"
        tagRegions[("SR2B",regionIcut)]="SR2B_IV"
        tagRegions[("SR2B",regionVcut)]="SR2B_V"

        tagRegions[("SRT",centralCut)]="SRT"
        tagRegions[("SRT",regionIcut)]="SRT_I"
        tagRegions[("SRT",regionIIcut)]="SRT_II"
        tagRegions[("SRT",regionIIIcut)]="SRT_III"
        tagRegions[("SRT",regionVcut)]="SRT_V"
        
        tagRegions[("SRW",centralCut)]="SRW"
        tagRegions[("SRW",regionIcut)]="SRW_I"
        tagRegions[("SRW",regionIIcut)]="SRW_II"
        tagRegions[("SRW",regionIIIcut)]="SRW_III"
        tagRegions[("SRW",regionVcut)]="SRW_V"


if("cr" in opt.mode):
    regionCuts["CR0B"]="best_topjet_isbtag==0&&best_Wpjet_isbtag==0&&nbjet_pt100==0"
    ctrlCuts["CR0B"]=[centralCut,regionIcut,regionIIcut,regionIIIcut,regionVcut]

    if "v18" in tagversion:
        tagRegions[("CR0B",centralCut)]="CR0B"
        tagRegions[("CR0B",regionIcut)]="CR0B_I"
        tagRegions[("CR0B",regionIIcut)]="CR0B_II"
        tagRegions[("CR0B",regionIIIcut)]="CR0B_III"
        tagRegions[("CR0B",regionVcut)]="CR0B_V"
        


#samplestorun = "WP_M5200W520_RH_2018"
samplestorun=opt.samples
print("samples= ",opt.samples)
#Need to automatize running components for the signal:
if(not doMerge and (doFitPlot or doPlot or doStack or doCheck or doReplot) and not samplestorun==""):
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

print samplescommand

tagcommand=""
#only merging part
for y in years:
    if not doMerge: continue
    if not (y in samplescommand or samplescommand==""):continue
    if(parallelize):
        nplot=nplot+1
        extrastring = ' & '
        nparallelcheck = min(nparallel, len(years) )
        if nplot%nparallelcheck==0:
            extrastring='; sleep 2'
    cmd='python makeplot.py -i '+inputpath+' -o '+outputpath+' -y '+y+' '+ samplescommand +' --sel -f '+version+' --merpart --mertree --lumi '+ extrastring
    print ("command is ",cmd)
    if (not dryrun) and doMerge:
        os.system(cmd)

nplot=0
extrastring=''
#only plotting part
for r,rc in regionCuts.iteritems():
    if not (doPlot or doFitPlot):
        continue
    print "in regions"
    cc =ctrlCuts[r]
    for ccc in cc:
        print "in cuts"
        bigcut=rc+ccc
        for y in years:
            print "in years"
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
                    cmd='python makeplot.py -i '+inputpath+' -o '+outputpath+' -y '+y+' -L '+l + samplescommand + tagcommand + varsetcommand + ' --sel -f '+version+' -C "'+bigcut+'" --plot -S '+s+' '+ extrastring
                    print ("command is ",cmd)
                    if (not dryrun) and (doPlot or doFitPlot):
                        os.system(cmd)
                        
nplot=0
extrastring=''
#only stacking part
systStack="-S noSyst"
if opt.syst!="all":
    systStack=" -S "+opt.syst
for r,rc in regionCuts.iteritems():
    if not doStack:
        continue
    cc =ctrlCuts[r]
    for ccc in cc:
        bigcut=rc+ccc
        for y in years:
#            if not (y in samplescommand or samplescommand==""):continue
#            if not y in samplescommand:continue
            samplescommand_stack= " -d all "
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
                    cmd='python makeplot.py -i '+inputpath+' -o '+outputpath+' -y '+y+' -L '+l + samplescommand_stack + tagcommand + varsetcommand +' -s --sel -f '+version+' -C "'+bigcut+'" '+systStack +' ' +extrastring
#                    cmd='python makeplot.py -i '+inputpath+' -o '+outputpath+' -y '+y+' -L '+l + samplescommand_stack + tagcommand + varsetcommand +' -s --sel -f '+version+' -C "'+bigcut+'" -S '+s+' '+ extrastring
                    print ("command is ",cmd)
                    if (not dryrun) and doStack :
                        os.system(cmd)
                        

missinglist=[]
#check missing histos
if doCheck or doReplot:
    from pythondirs import find_histo_file,is_file_missing
    
if "," in samplestorun:
    salist=samplestorun.split(",")
else:
    salist=[samplestorun]    

bh="h_jets_best_Wprime_m_"
histosRegions= [bh + x for x in  list(tagRegions.values())]

for sa in salist:
    if not (doCheck or doReplot): continue
    for y in years:
        if not y in sa: continue
        for l in leptons:
            for s in systs:
                if("Data" in sa) and s!="noSyst": continue
                if(is_file_missing(sa,y)): continue
                sn=""
                if s!="noSyst":
                    sn= "_"+s
                print( "year ",y,"lepton",l ,"syst",s)
                filenamecheck=outputpath+"/"+version+"/plot/"+l+"/"+sa+"_"+l+sn+".root"
                print (" file to check: " +filenamecheck)
                if not os.path.exists(filenamecheck):
                    missinglist.append((sa,y,l,s))
                    continue
                else:
                    print (histosRegions)
                    missinghistos=find_histo_file(filenamecheck,histosRegions)[0]
                    if len(missinghistos)!=0:
                        missinglist.append((sa,y,l,s))
                        if(not doReplot):
                            print(" file "+filenamecheck+" will be purged ")
                            os.system(" rm "+filenamecheck+"")#need to be removed for good measure. Broken files can create issues when rerunning
                            time.sleep(0.2)
                            fmake = TFile(filenamecheck,"NEW")
                            fmake.Close()
                            time.sleep(0.2)

if(doCheck or doReplot):
    print "missinglist length: ",len(missinglist)
    print "missing list is \n\n", missinglist 
    
#time.sleep(3)

nplot=0
extrastring=''
#resubmitting missing plots
if doReplot:
    for r,rc in regionCuts.iteritems():
        cc =ctrlCuts[r]
        for ccc in cc:
            bigcut=rc+ccc
            for mis in missinglist:
                print "rerunning:  ",mis
                samplecommand= " -d "+mis[0]
                y = mis[1]
                l = mis[2]
                s = mis[3]
                print "samplescommand is ",samplecommand
                if tagversion!="":
                    tagcommand=" -t "+tagRegions[(r,ccc)]
                    print ("tagcommand is ", tagcommand)                      
                if(parallelize):
                    nplot=nplot+1
                    extrastring = ' & '
                    nparallelcheck = min(nparallel,int(len(missinglist)/nparallel))# Min () (Nparallel, len(years)*len(systs)*len(leptons))
                    print(nplot , " npa", nparallelcheck)
                    if nparallelcheck==0:
                        extrastring='; sleep 2'
                    else:
                        if nplot%nparallelcheck==0:
                            extrastring='; sleep 2'

                
                cmd='python makeplot.py -i '+inputpath+' -o '+outputpath+' -y '+y+' -L '+l + samplecommand + tagcommand+' --sel -f '+version+' -C "'+bigcut+'" --plot -S '+s+' '+ extrastring
                print cmd
                if not(opt.dryrun):
                    os.system(cmd)




import os,optparse,commands

usage = 'python full_analysis.py -m lpmdecf'
parser = optparse.OptionParser(usage)
parser.add_option('--years','-y', dest='years', default = '2016,2017,2018', type='string', help='years to run')
parser.add_option('-S', '--syst', dest='syst', default = 'all', type='string', help='syst to run, options are: all,noSyst, or a specific systeamtic')
parser.add_option('-l', '--lep', dest='leptons', default = 'muon,electron', type='string', help='lepton to run')
parser.add_option('-v', '--version', dest='version', default = 'v18', type='string', help='analysis version')
parser.add_option('-i', '--inputpath', dest='inputpath', default = '/eos/user/o/oiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-o', '--outputpath', dest='outputpath', default = '/eos/user/o/oiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-n', '--dryrun', dest='dryrun', action= 'store_true' , default = False, help='if called not running the command')
parser.add_option('', '--alt', dest='alt', action= 'store_true' , default = False, help='alternative fit from cr-corrected shape')


parser.add_option('--parallel', dest='parallel', type='int', default=10 , help='if called run on more than 1 plot simultaneously')

parser.add_option('-d', '--samples', dest='samples', default = '', type='string', help='samples to run, default all')
parser.add_option('', '--varset', dest='varset', type='string', default = '', help="variables set: S: signal, V: validation, A: AN")
parser.add_option('', '--nosplit', dest='nosplit', action= 'store_true' , default = False, help="if triggered doesn't spli data driven systs by region")

parser.add_option('-m', '--mode', dest='mode',default = '' , type='string', help='options: lpsmdecf. Determines the type of operations to do: l:lumimerge (merge and evaluate lumi), p:plot (plot fit variables), m:mergeyears (merge years into one plot), d:datadriven (evaluate background from data driven methods), f:fit (prepare fit with prefit routines)  ')


(opt, args) = parser.parse_args()

runs_dataset="" #this option by default runs the base samples, but not the extended signals
merge_dataset="" #this option by default merges the base samples, but not the extended signals

years=opt.years.split(",") 

if opt.samples!="":
    runs_dataset = "-d "
    merge_dataset = "-d "
    ss=opt.samples
    print (type(ss),ss)
    ssplit=opt.samples.strip("[]").split(",")
    if "base" in ssplit:
        testsigs=["WP_M2000W20_RH","WP_M3000W30_RH","WP_M4000W40_RH","WP_M5000W50_RH","WP_M6000W60_RH"]
        for dat in (["DataMu","DataPh","DataEle","DataHT","TT_Mtt","WJets","ST","QCD"]+testsigs):
            merge_dataset=merge_dataset+dat+","
            for y in years:
                if(y!="2017" and "DataPh" in dat ):continue
                runs_dataset=runs_dataset+dat+"_"+y+"," 
        ss=ss.replace("base,",",").replace("base","")
    if "WP_RH" in ssplit:
        runs_dataset =runs_dataset+"WP_RH_2016,WP_RH_2017,WP_RH_2018,"
        merge_dataset=merge_dataset+"WP_RH,"
        ss=ss.replace("WP_RH,",",").replace("WP_RH","")
    if "WP_LHSMinter" in ssplit:
        runs_dataset =runs_dataset+"WP_LHSMinter_2016,WP_LHSMinter_2017,WP_LHSMinter_2018,"
        merge_dataset=merge_dataset+"WP_LHSMinter,"
        ss=ss.replace("WP_LHSMinter,",",").replace("WP_LHSMinter","")
    if "WP_LRSMinter" in ssplit:
        runs_dataset =runs_dataset+"WP_LRSMinter_2016,WP_LRSMinter_2017,WP_LRSMinter_2018,"
        merge_dataset=merge_dataset+"WP_LRSMinter,"
        ss=ss.replace("WP_LRSMinter,",",").replace("WP_LRSMinter","")

    runs_dataset=runs_dataset+ss
    merge_dataset=merge_dataset+ss
    print runs_dataset
    
    while runs_dataset[-1]==",": 
#        print runs_dataset
        runs_dataset=runs_dataset[:-1]
#        print runs_dataset[-1]
    while merge_dataset[-1]==",": 
        merge_dataset=merge_dataset[:-1]
print merge_dataset


splitregoption=" --splitregions "
if opt.nosplit:
    splitregoption=""

corroption = "--addsystematic "
corrfolder=""
if opt.alt:
    corroption = " -O --addsystematic "
    #corrfolder= "_fit"

varsetcommand=opt.varset
if varsetcommand!="":
    varsetcommand=" --varset "+opt.varset



nparallel=str(opt.parallel)

####### 1
#in the first step, trees are merged
command_lumimerge="nohup python doplot.py -m mer -v "+opt.version+" -i "+opt.inputpath+" -o "+opt.outputpath+" -y "+opt.years+ " --parallel "+nparallel+" "+runs_dataset+"  >& "+opt.outputpath+"/"+opt.version+"/lumimerge.log &"

####### 2
#here plots for the sr and cr are done
command_plot="nohup python doplot.py -m fitsrcr -v "+opt.version+" -t "+opt.version+" -i "+opt.inputpath+" -o "+opt.outputpath+" -y "+opt.years+ " -S "+opt.syst+ " --parallel "+nparallel+varsetcommand+" "+runs_dataset+"  >& "+opt.outputpath+"/"+opt.version+"/plot.log &"

####### 3
#here we check whether the plot has really been produced
command_check="nohup python doplot.py -m checksrcr -v "+opt.version+" -t "+opt.version+" -i "+opt.inputpath+" -o "+opt.outputpath+" -y "+opt.years+ " -S "+opt.syst+ " --parallel "+nparallel+varsetcommand+" "+runs_dataset+"  >& "+opt.outputpath+"/"+opt.version+"/checkreplot.log "

command_replot="nohup python doplot.py -m repsrcr -v "+opt.version+" -t "+opt.version+" -i "+opt.inputpath+" -o "+opt.outputpath+" -y "+opt.years+ " -S "+opt.syst+ " --parallel "+nparallel+varsetcommand+" "+runs_dataset+"  >& "+opt.outputpath+"/"+opt.version+"/replot.log &"

####### 4
#here do the stacks plots for the sr and cr
command_stack="nohup python doplot.py -m stacksrcr -v "+opt.version+" -t "+opt.version+" -i "+opt.inputpath+" -o "+opt.outputpath+" -y "+opt.years+ " -S "+opt.syst+ " --parallel "+nparallel+varsetcommand+" "+runs_dataset+"  >& "+opt.outputpath+"/"+opt.version+"/plotstack.log &"

####### 5 (optional)
#mergeyears: this operation does merge the years together in the "outputpath"
command_mergeyears = "nohup python mergeyears.py -v "+opt.version+" -i "+opt.inputpath+" -o "+opt.outputpath+ " --parallel 10 "+merge_dataset+" >& "+opt.outputpath+"/"+opt.version+"/mergeyears.log &"

####### 6
#makedd: this makes the dd method apply. If "e" is specified, runs over the _II and _III regions as well to derive an extra correction
extrasamplesopt=""
if "e" in opt.mode: extrasamplesopt=" -e "
commands_makeddmu="nohup python makedd.py --pathin "+opt.inputpath+"/"+opt.version+"/plot_merged -y 2020 --plotpath plot_"+opt.version+" -c muon "+extrasamplesopt+splitregoption+"--pathout "+opt.outputpath+"/"+opt.version+"/plot_explin --runoptions N --resetMF >& "+opt.outputpath+"/"+opt.version+"/makeddmu.log; " 
commands_makeddmu=commands_makeddmu+"nohup python makedd.py --pathin "+opt.inputpath+"/"+opt.version+"/plot_merged -y 2020 --plotpath plot_"+opt.version+" -c muon "+extrasamplesopt+splitregoption+"--pathout "+opt.outputpath+"/"+opt.version+"/plot_explin --runoptions B --resetMF >& "+opt.outputpath+"/"+opt.version+"/makeddmu.log; " 
#commands_makeddmu=commands_makeddmu+"nohup python makedd.py --pathin "+opt.inputpath+"/"+opt.version+"/plot_merged -y 2020 --plotpath plot_"+opt.version+" -c muon "+extrasamplesopt+splitregoption+"--pathout "+opt.outputpath+"/"+opt.version+"/plot_explin --runoptions S --resetMF >& "+opt.outputpath+"/"+opt.version+"/makeddmu.log; " 
commands_makeddmucp= "cp "+opt.inputpath+"/"+opt.version+"/plot_merged/muon/WP*root "+opt.outputpath+"/"+opt.version+"/plot_explin/muon/ >& "+opt.outputpath+"/"+opt.version+"/makeddcpmu.log; "

commands_makeddel= "nohup python makedd.py --pathin "+opt.inputpath+"/"+opt.version+"/plot_merged -y 2020 --plotpath plot_"+opt.version+" -c electron "+extrasamplesopt+splitregoption+"--pathout "+opt.outputpath+"/"+opt.version+"/plot_explin --runoptions N --resetMF >& "+opt.outputpath+"/"+opt.version+"/makeddel.log; " 
commands_makeddel=commands_makeddel+"nohup python makedd.py --pathin "+opt.inputpath+"/"+opt.version+"/plot_merged -y 2020 --plotpath plot_"+opt.version+" -c electron "+extrasamplesopt+splitregoption+"--pathout "+opt.outputpath+"/"+opt.version+"/plot_explin --runoptions B --resetMF >& "+opt.outputpath+"/"+opt.version+"/makeddel.log; " 
commands_makeddelcp="cp "+opt.inputpath+"/"+opt.version+"/plot_merged/electron/WP*root "+opt.outputpath+"/"+opt.version+"/plot_explin/electron/ >& "+opt.outputpath+"/"+opt.version+"/makeddcpele.log"

####### 7
command_extraunc= "nohup python makecorrection.py "+corroption+splitregoption+"  -i "+opt.inputpath+"/"+opt.version+"/plot_explin"+corrfolder+"/ "+"  >& "+opt.outputpath+"/"+opt.version+"/extracr.log "
command_extraunc=command_extraunc+ "; nohup python splitregions.py "+corroption+splitregoption+" -i "+opt.inputpath+"/"+opt.version+"/plot_explin"+corrfolder+"/ "+"  >& "+opt.outputpath+"/"+opt.version+"/extrasplit.log "

####### 8
commands_preparefit = "nohup python preparefit.py -m 'sum symmetrize smooth pdfeval' "+extrasamplesopt+" -i "+ opt.inputpath+"/"+opt.version+"/plot_explin -o "+ opt.outputpath+"/"+opt.version+"/plot_explin_fit "+"  >& "+opt.outputpath+"/"+opt.version+"/fitprepare.log &"
commands_preparefit = "nohup python preparefit.py -m 'sum symmetrize pdfeval' "+extrasamplesopt+splitregoption+" -i "+ opt.inputpath+"/"+opt.version+"/plot_explin -o "+ opt.outputpath+"/"+opt.version+"/plot_explin_fit "+"  >& "+opt.outputpath+"/"+opt.version+"/fitprepare.log &"

if opt.mode=="":
    print("Note that no operating mode was given, will do nothing. Usage is: "+usage+" ; Check 'mode' options for more info.")

if opt.dryrun:
    print("Note that 'dryrun' mode is enabled. Will only print commands and not run them.")

if "l" in opt.mode:
    print("lumimerge command is: \n "+ command_lumimerge)
    if not opt.dryrun:
        os.system("rm missingSamples.txt")
        os.system(command_lumimerge)
if "p" in opt.mode:
    print("plot command is: \n "+ command_plot)
    if not opt.dryrun:
        os.system(command_plot)
if "s" in opt.mode:
    print("plot command is: \n "+ command_stack)
    if not opt.dryrun:
        os.system(command_stack)
if "r" in opt.mode:
    print("check command is: \n "+ command_check)
    if not opt.dryrun:
        os.system(command_check)
    print("replot command is: \n "+ command_replot)
    if not opt.dryrun:
        os.system(command_replot)

if "m" in opt.mode:
    if("p" in opt.mode):# if plotting is done, run from plotting directory
        command_mergeyears=command_mergeyears.replace(opt.inputpath,opt.outputpath)
    print ("mergeyears command is: \n "+command_mergeyears)
    if not opt.dryrun:
        os.system(command_mergeyears)
if "d" in opt.mode:
    print("makedd commands mu are: \n "+ commands_makeddmu)
    print("makedd commands el are: \n "+ commands_makeddel)
    if not opt.dryrun:
        os.system(commands_makeddmu)
        os.system(commands_makeddel)
    if "e" in opt.mode:
        command_extraunc= command_extraunc.replace(opt.inputpath,opt.outputpath)
        print("add control region uncertainty command: \n "+ command_extraunc)
        if not opt.dryrun:
            os.system(command_extraunc)

if opt.mode=="e": #if e alone: run only this one 
    print("add control region uncertainty command: \n "+ command_extraunc)
    if not opt.dryrun:
        os.system(command_extraunc)

if "c" in opt.mode:
    if("m" in opt.mode):#if merged is done, take it from the output
        commands_makeddmucp=commands_makeddmucp.replace(opt.inputpath,opt.outputpath)
        commands_makeddelcp=commands_makeddelcp.replace(opt.inputpath,opt.outputpath)

    commands_qcdmucp=commands_makeddmucp.replace("WP*","QCD*")
    commands_qcdelcp=commands_makeddelcp.replace("WP*","QCD*")
    print("makeddcp commands mu are: \n "+ commands_makeddmucp)
    print("makeddcp commands el are: \n "+ commands_makeddelcp)
    print("qcdddcp commands mu are: \n "+ commands_qcdmucp)
    print("qcdddcp commands el are: \n "+ commands_qcdelcp)
    if not opt.dryrun:
        os.system(commands_makeddmucp)
        os.system(commands_makeddelcp)
        os.system(commands_qcdelcp)
        os.system(commands_qcdmucp)


if "f" in opt.mode:
    if "de" in opt.mode:
        commands_preparefit= commands_preparefit.replace(opt.inputpath,opt.outputpath)

    print ("preparefit command is: \n "+ commands_preparefit)
    if not opt.dryrun:
        os.system(commands_preparefit)

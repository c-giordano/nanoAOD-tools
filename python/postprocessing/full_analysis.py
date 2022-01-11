import os,optparse,commands

usage = 'python full_analysis.py -m lpmdf'
parser = optparse.OptionParser(usage)
parser.add_option('--years','-y', dest='years', default = '2016,2017,2018', type='string', help='years to run')
parser.add_option('-S', '--syst', dest='syst', default = 'all', type='string', help='syst to run, options are: all,noSyst, or a specific systeamtic')
parser.add_option('-l', '--lep', dest='leptons', default = 'muon,electron', type='string', help='lepton to run')
parser.add_option('-v', '--version', dest='version', default = 'v18', type='string', help='analysis version')
parser.add_option('-i', '--inputpath', dest='inputpath', default = '/eos/user/o/oiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-o', '--outputpath', dest='outputpath', default = '/eos/user/o/oiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-n', '--dryrun', dest='dryrun', action= 'store_true' , default = False, help='if called not running the command')


parser.add_option('--parallel', dest='parallel', type='int', default=1 , help='if called run on more than 1 plot simultaneously')

parser.add_option('-d', '--samples', dest='samples', default = '', type='string', help='samples to run, default all')


parser.add_option('-m', '--mode', dest='mode',default = '' , type='string', help='options: lpmdf. Determines the type of operations to do: l:lumimerge (merge and evaluate lumi), p:plot (plot fit variables), m:mergeyears (merge years into one plot), d:datadriven (evaluate background from data driven methods), f:fit (prepare fit with prefit routines)  ')
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
        for dat in ["DataMu","DataEle","DataHT","TT_Mtt","WJets","ST","QCD"]:
            merge_dataset=merge_dataset+dat+","
            for y in years:
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
    while runs_dataset[-1]==",": 
#        print runs_dataset
        runs_dataset=runs_dataset[:-1]
#        print runs_dataset[-1]
    while merge_dataset[-1]==",": 
        merge_dataset=merge_dataset[:-1]

#in the first step, plots are taken from the 
command_lumimerge="nohup python doplot.py -m mer -v "+opt.version+" -i "+opt.inputpath+" -o "+opt.outputpath+" -y "+opt.years+ " --parallel 10 "+runs_dataset+"  >&"+opt.outputpath+"/"+opt.version+"/lumimerge.log &"

command_plot="nohup python doplot.py -m fitsrcr -v "+opt.version+" -t "+opt.version+" -i "+opt.inputpath+" -o "+opt.outputpath+" -y "+opt.years+ " -S "+opt.syst+ " --parallel 10 "+runs_dataset+"  >&"+opt.outputpath+"/"+opt.version+"/plot.log &"

#mergeyears: this operation does merge the years together in the "outputpath"
command_mergeyears = "nohup python mergeyears.py -v "+opt.version+" -i "+opt.outputpath+" -o "+opt.outputpath+ " --parallel 10 "+merge_dataset+" >& "+opt.outputpath+"/"+opt.version+"/mergeyears.log &"

commands_makeddmu="nohup python makedd.py --pathin "+opt.outputpath+"/"+opt.version+"/plot_merged -y 2020 --plotpath plot_"+opt.version+"-c muon --pathout "+opt.outputpath+"/"+opt.version+"/plot_explin --runoptions N --resetMF >& "+opt.outputpath+"/"+opt.version+"/makeddmu.log; " 
commands_makeddmu=commands_makeddmu+"nohup python makedd.py --pathin "+opt.outputpath+"/"+opt.version+"/plot_merged -y 2020 --plotpath plot_"+opt.version+"-c muon --pathout "+opt.outputpath+"/"+opt.version+"/plot_explin --runoptions B --resetMF >& "+opt.outputpath+"/"+opt.version+"/makeddmu.log; " 
#commands_makeddmu=commands_makeddmu+ "cp "+opt.outputpath+"/"+opt.version+"/plot_merged/muon/* "+opt.outputpath+"/"+opt.version+"/plot_explin/muon/ >& "+opt.outputpath+"/"+opt.version+"/makeddcpmu.log; "

commands_makeddel= "nohup python makedd.py --pathin "+opt.outputpath+"/"+opt.version+"/plot_merged -y 2020 --plotpath plot_"+opt.version+" -c electron --pathout "+opt.outputpath+"/"+opt.version+"/plot_explin --runoptions N --resetMF >& "+opt.outputpath+"/"+opt.version+"/makeddel.log; " 
commands_makeddel=commands_makeddel+"nohup python makedd.py --pathin "+opt.outputpath+"/"+opt.version+"/plot_merged -y 2020 --plotpath plot_"+opt.version+" -c electron --pathout "+opt.outputpath+"/"+opt.version+"/plot_explin --runoptions B --resetMF >& "+opt.outputpath+"/"+opt.version+"/makeddel.log; " 
#commands_makeddel= commands_makeddel+"cp "+opt.outputpath+"/"+opt.version+"/plot_merged/electron/* "+opt.outputpath+"/"+opt.version+"/plot_explin/electron/ >& "+opt.outputpath+"/"+opt.version+"/makeddcpele.log"

commands_preparefit = "nohup python preparefit.py -m 'sum symmetryze smooth pdfeval' -i "+ opt.outputpath+"/"+opt.version+"/plot_explin -o "+ opt.outputpath+"/"+opt.version+"/plot_explin_fit "+"  >&"+opt.outputpath+"/"+opt.version+"/fitprepare.log &"

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

if "m" in opt.mode:
    print ("mergeyears command is: \n "+command_mergeyears)
    if not opt.dryrun:
        os.system(command_mergeyears)
if "d" in opt.mode:
    print("makedd commands mu are: \n "+ commands_makeddmu)
    print("makedd commands el are: \n "+ commands_makeddel)
    if not opt.dryrun:
#        os.system(commands_makeddmu)
        os.system(commands_makeddel)
if "f" in opt.mode:
    print ("preparefit command is: \n "+ commands_preparefit)
    if not opt.dryrun:
        os.system(commands_preparefit)

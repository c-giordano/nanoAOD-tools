import os,optparse,commands,ROOT,math

usage = 'python doplot.py'
parser = optparse.OptionParser(usage)

parser.add_option('-l', '--lep', dest='leptons', default = 'muon,electron', type='string', help='lepton to run')
parser.add_option('-v', '--version', dest='version', default = 'v18', type='string', help='analysis version')
parser.add_option('-i', '--inputpath', dest='inputpath', default = '/eos/user/o/oiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-o', '--outputpath', dest='outputpath', default = '/eos/user/o/oiorio/Wprime/nosynch/', type='string', help='file in , not working yet!')
parser.add_option('-n', '--dryrun', dest='dryrun', action= 'store_true' , default = False, help='if called not running the command')
parser.add_option('-d', '--samples', dest='samples', default = '', type='string', help='samples to run, default: all background, data and some signals')
(opt, args) = parser.parse_args()


samples = ["Data","TT_Mtt","WJets","ST","QCD"]
samples = ["Data","TT_Mtt","WJets","ST","QCD"]

version = opt.version
pathin = opt.inputpath +"/"+version+"/plot_merged"
dryrun = opt.dryrun

leps = ['electron','muon']

names=["CR0B","CR0B_I","SR2B","SR2B_I","SRW","SRW_I","SRT","SRT_I"]

srcr={"CR0B":"CR0B_I","SR2B":"SR2B_I","SRW":"SRW_I","SRT":"SRT_I"}
#srcr={"SR2B":"SR2B_I"}

from repos import namemap 


fout=file("table_events.tex","w") 

so="\\begin{table} \n"
so+="\\centering \n"
so+=''' 
\\caption{Number of background events from the MC simulations and their realtive abundance in the main region and in the region I.}\\label{tab:background_prefit_rate}
\\begin{tabular}{l| c c | c c } 
'''
sobins=so
sotot=so

rebinfact=1
rebinfact=3
for lep in leps:
    for sr,cr in srcr.iteritems():
        print sr,cr
        head=' Lepton: '+str(lep)+'& \multicolumn{2}{c}{'+sr+'}  & \multicolumn{3}{|c}{'+sr+'\_I} \\\\ \n'
        head+='Process  & Integral $\pm$  Uncertainty & Abundance (\%) & Integral $\pm$  Uncertainty & Abundance (\%) & |N|/(Data-TotMC) \\\\ \n'
        headbins=' Lepton: '+str(lep)+'& \multicolumn{2}{c}{'+sr+'}  & \multicolumn{3}{|c}{'+sr+'\_I} \\\\ \n'
        headbins+='Process  & Integral $\pm$  Uncertainty & Abundance (\%) & Integral $\pm$  Uncertainty & Abundance (\%) & |N|/(Data-TotMC) \\\\ \n'
        so+=head
        sobins+=head
        sotot+=head

        totreg=0
        totregerr=0
        totregbins=[0]*30
        totregerrbins=[0]*30
        dataregion=0
        dataregionbins=[0]*30

        totreg_I=0
        totregerr_I=0
        totregbins_I=[0]*30
        totregerrbins_I=[0]*30
        dataregion_I=0
        dataregionbins_I=[0]*30
        #first loop: evaluating the total
        binrange=[]
        binranges=[""]*30
        for sample in samples:
            filename=pathin+"/"+lep+"/"+sample+"_2020_"+lep+".root"  
            filer=(ROOT.TFile(filename,"OPEN"))
            histonamesr=namemap[sr]
            histonamecr=namemap[cr]
            
            
#            print("histo name is "+histoname)
#            print("file name is "+filename)
            print (filer)
            histosr = filer.Get(histonamesr)
            histocr = filer.Get(histonamecr)
            if rebinfact>1:
                histosr.Rebin(rebinfact)
                histocr.Rebin(rebinfact)

            print(histosr)
            print (histosr.GetName())
            stot=histosr.Integral()
            stot_I=histocr.Integral()
            if sample=="Data":
                dataregion=stot
                dataregion_I=stot_I
                for b in range(1,histosr.GetNbinsX()+1):
                    bi=histosr.GetBinContent(b)
                    bi_I=histocr.GetBinContent(b)
                    dataregionbins[b]=bi
                    dataregionbins_I[b]=bi_I

                continue #Data does not enter the total

            stoterr=0
            stoterr_I=0
            binrange=range(1,histosr.GetNbinsX()+1)
            for b in range(1,histosr.GetNbinsX()+1):
                bi=histosr.GetBinContent(b)
                ebi=histosr.GetBinError(b)
                bi_I=histocr.GetBinContent(b)
                ebi_I=histocr.GetBinError(b)
                
                totregbins[b]+=bi
                totregerrbins[b]+=ebi*ebi
                totregerr+=ebi*ebi

                totregbins_I[b]+=bi_I
                totregerrbins_I[b]+=ebi_I*ebi_I
                totregerr_I+=ebi_I*ebi_I
                binranges[b]="["+"{:.0f}".format(histosr.GetBinLowEdge(b))+","+"{:.0f}".format(histosr.GetBinLowEdge(b+1))+"]"

            totreg+=stot
            totreg_I+=stot_I
        totregerr=math.sqrt(totregerr)
        totregerr_I=math.sqrt(totregerr_I)


        sotot+="Tot MC"+" & "+"{:.0f}".format(totreg)+" $\\pm$ "+ "{:.0f}".format(totregerr)+ " & " + "{:.0f}".format(totreg/totreg *100) + " & " 
        sotot +=" {:.0f}".format(totreg_I)+" $\\pm$ "+ "{:.0f}".format(totregerr_I)+ " & " + "{:.0f}".format(totreg_I/totreg_I *100) + " & \\\\ \n "  
        
        for b in binrange:
            totregerrbins[b]=math.sqrt(totregerrbins[b])
            totregerrbins_I[b]=math.sqrt(totregerrbins_I[b])
            sobins+="Tot MC, bin "+binranges[b]+" & "+"{:.0f}".format(totregbins[b])+" $\\pm$ "+ "{:.0f}".format(totregerrbins[b])+ " & " + "{:.0f}".format(totregbins[b]/totregbins[b] *100) + " & " 
            sobins +=" {:.0f}".format(totregbins_I[b])+" $\\pm$ "+ "{:.0f}".format(totregerrbins_I[b])+ " & " + "{:.0f}".format(totregbins_I[b]/totregbins_I[b] *100) + " & \\\\ \n "  
            


        for sample in samples:
            filename=pathin+"/"+lep+"/"+sample+"_2020_"+lep+".root"  
            filer=(ROOT.TFile(filename,"OPEN"))
            histonamesr=namemap[sr]
            histonamecr=namemap[cr]
            histosr = filer.Get(histonamesr)
            histocr = filer.Get(histonamecr)
            if rebinfact>1:
                histosr.Rebin(rebinfact)
                histocr.Rebin(rebinfact)
            stot=histosr.Integral()
            stot_I=histocr.Integral()
            stoterr=0
            stoterr_I=0
            stotbins=[0]*30
            stotbins_I=[0]*30
            stoterrbins=[0]*30
            stoterrbins_I=[0]*30
            for b in range(1,histosr.GetNbinsX()+1):
                bi=histosr.GetBinContent(b)
                ebi=histosr.GetBinError(b)
                bi_I=histocr.GetBinContent(b)
                ebi_I=histocr.GetBinError(b)

                stoterr+=ebi*ebi
                stoterr_I+=ebi_I*ebi_I
                
                
                stotbins[b]=bi
                stotbins_I[b]=bi_I
                stoterrbins[b]=ebi
                stoterrbins_I[b]=ebi_I

            stoterr=math.sqrt(stoterr)
            stoterr_I=math.sqrt(stoterr_I)
            if (sample!="Data"):
                sotot+=sample+" & "+"{:.0f}".format(stot)+" $\\pm$ "+ "{:.0f}".format(stoterr)+ " & " + "{:.0f}".format(stot/totreg *100) + " & " 
                sotot +=" {:.0f}".format(stot_I)+" $\\pm$ "+ "{:.0f}".format(stoterr_I)+ " & " + "{:.0f}".format(stot_I/totreg_I *100) + " & " +"{:.2f}".format(abs((dataregion_I-totreg_I)/stot_I)) +" \\\\ \n "  
            if (sample=="Data"):
                sotot+=sample+" & blinded  &  & " 
                sotot +=" {:.0f}".format(stot_I)+" $\\pm$ "+ "{:.0f}".format(stoterr_I)+ " & " + "{:.0f}".format(stot_I/totreg_I *100) + " & \\\\ \n "  
            
            for b in binrange:
                if (sample!="Data"):
                    ratio1="-"
                    ratio2="-"
                    ratio3="-"
                    if(totregbins[b]>0):
                        ratio1="{:.0f}".format(stotbins[b]/totregbins[b] *100)
                    if(totregbins_I[b]>0):
                        ratio2="{:.0f}".format(stotbins_I[b]/totregbins_I[b] *100)
                    if(stotbins_I[b]>0):
                        ratio3="{:.2f}".format(abs((dataregionbins_I[b]-totregbins_I[b])/stotbins_I[b]))

                    sobins+=sample+", bin "+binranges[b]+" & "+"{:.0f}".format(stotbins[b])+" $\\pm$ "+ "{:.0f}".format(stoterrbins[b])+ " & " + ratio1 + " & "                 
                    sobins +=" {:.0f}".format(stotbins_I[b])+" $\\pm$ "+ "{:.0f}".format(stoterrbins_I[b])+ " & " +ratio2+ " & " + ratio3 +" \\\\ \n "  
#                if sample=="Data":
                    
        #second loop: evaluating the partials

sotot=sotot+'''\end{tabular}
\end{table}


'''
sobins=sobins+'''\end{tabular}
\end{table}


'''


fout.write(sotot)
fout.write(sobins)

'''\begin{table}
%\resizebox{\textwidth}{!}{                                                                                                                                                       
\centering
\caption{Number of background events from the MC simulations and their realtive abundance in the main region and in the region I.}\label{tab:background_prefit_rate}
\begin{tabular}{l|c c | c c }
 & \multicolumn{2}{c}{CR0B}  & \multicolumn{2}{|c}{CR0B\_I} \\
Process  & Integral $\pm$  Uncertainty & Abundance (\%)  & Integral $\pm$  Uncertainty & Abundance (\%) \\
\hline
Single top  & 52     $\pm$  9   & 2.50 & 38     $\pm$  4   & 0.95 \\
\wjets      & 1667   $\pm$  9   & 79.94 & 3582   $\pm$  13  & 89.68 \\
\ttbar      & 299    $\pm$  18  & 14.38 & 316    $\pm$  17  & 7.93 \\
QCD         & 66     $\pm$  14  & 3.18 & 57     $\pm$  12  & 1.43 \\
\hline
 & \multicolumn{2}{c}{SRT}  & \multicolumn{2}{|c}{SRT\_I} \\
Process  & Integral $\pm$  Uncertainty & Abundance (\%)  & Integral $\pm$  Uncertainty & Abundance (\%) \\
\hline
Single top  & 120    $\pm$  10  & 14.13 & 60     $\pm$  9   & 10.75 \\
\wjets      & 92     $\pm$  2   & 10.79 & 189    $\pm$  2   & 33.76 \\
\ttbar      & 616    $\pm$  20  & 72.07 & 307    $\pm$  15  & 54.72 \\
QCD         & 25     $\pm$  9   & 3.01 & 4      $\pm$  2   & 0.77 \\
\hline
 & \multicolumn{2}{c}{SRW}  & \multicolumn{2}{|c}{SRW\_I} \\
Process  & Integral $\pm$  Uncertainty & Abundance (\%)  & Integral $\pm$  Uncertainty & Abundance (\%) \\
\hline
Single top  & 15     $\pm$  2   & 9.06 & 30     $\pm$  3   & 10.06 \\
\wjets      & 110    $\pm$  2   & 63.12 & 219    $\pm$  3   & 71.50 \\
\ttbar      & 46     $\pm$  5   & 26.75 & 47     $\pm$  6   & 15.62 \\
QCD         & 1      $\pm$  0   & 1.07 & 8      $\pm$  6   & 2.82 \\
\hline
 & \multicolumn{2}{c}{SRW}  & \multicolumn{2}{|c}{SRW\_I} \\
Process  & Integral $\pm$  Uncertainty & Abundance (\%)  & Integral $\pm$  Uncertainty & Abundance (\%) \\
\hline
Single top  & 74     $\pm$  7   & 24.62 & 129    $\pm$  7   & 40.36  \\
\wjets      & 8      $\pm$  0   & 2.95  & 74     $\pm$  1   & 23.23 \\
\ttbar      & 208    $\pm$  9   & 69.00 & 110    $\pm$  6   & 34.46 \\
QCD         & 10     $\pm$  6   & 3.43 & 6      $\pm$  3   & 1.95 \\
\end{tabular}%}                                                                                                                                                                   
\end{table}
'''

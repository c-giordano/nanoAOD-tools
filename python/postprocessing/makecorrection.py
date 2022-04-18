import os
import shutil
import optparse
import copy
import ROOT
from symmetry import symmetry,nnpdfeval
from repos import histosr,histocr
from fit_utils import shift,smoothing,scale

pi = "/eos/home-o/oiorio/Wprime/nosynch/v18/plot_explin/"
po = "/eos/home-o/oiorio/Wprime/nosynch/v18/plot_explin/"

usage = "python preparefit.py -l muon,electron -i pathinput -o pathoutput -v v17 -y 2016,2017,2018"
parser = optparse.OptionParser(usage)
parser.add_option('--years','-y', dest='years', default = '2016,2017,2018', type='string', help='years to run')
parser.add_option('-S', '--syst', dest='syst', default = 'all', type='string', help='syst to run, options are: all,noSyst, or a specific systeamtic')
parser.add_option('-l', '--lep', dest='leptons', default = 'muon,electron', type='string', help='lepton to run')
parser.add_option('-v', '--version', dest='version', default = 'v18', type='string', help='analysis version')
parser.add_option('-i', '--inputpath', dest='inputpath', default = pi, type='string', help='file in , not working yet!')
parser.add_option('-o', '--outputpath', dest='outputpath', default = po, type='string', help='file in , not working yet!')
parser.add_option('-n', '--dryrun', dest='dryrun', action= 'store_true' , default = False, help='if called not running the command')
parser.add_option('-m', '--mode', dest='mode',default = 'sum symmetrize smooth' , type='string', help='"sum" splits systs per years, "symmetrize" symmetrizes DD uncertainties, "smooth" smooths QCD histograms')
parser.add_option('--parallel', dest='parallel', type='int', default=1 , help='if called run on more than 1 plot simultaneously')
parser.add_option('-r', '--refresh', dest='refresh', action= 'store_true' , default = False, help='if called empty the output folders first')
parser.add_option('-O', '--overwrite', dest='overwrite', action= 'store_true' , default = False, help='overwrite original files with corrected ones, default false')
parser.add_option('', '--addsystematic', dest='addsystematic', action= 'store_true' , default = False, help='create alternative file with systematic variation')
parser.add_option('', '--splitregions', dest='splitregions', action= 'store_true' , default = False, help='split systs. for signal and control regions')
#parser.add_option('--cut','-c', dest='cuts', default = '', type='string', help='years to run')
(opt, args) = parser.parse_args()

version = opt.version
pathin = opt.inputpath
pathout = opt.outputpath
dryrun = opt.dryrun
leps = map(str,opt.leptons.split(','))

print leps

from repos import namemap, wjets_veto_map

pred = "DDFitWJetsTT_MttST"
data = "Data"
systs = ["noSyst","PF", "pu", "lep", "trig", "jes2016", "jer2016", "jes2017", "jer2017", "jes2018", "jer2018", "btag", "mistag", "pdf_total", "TT_Mtt", "WJets", "ST", "LHETT_Mtt", "LHEWJets", "LHEST"]
#systs=["noSyst"]
#systs.extend(["WJets","ST","TT_Mtt","AltTF_2020","Alt_2020","DD_2020","TF_2020"])
listdd=["TF_2020", "DD_2020", "Alt_2020", "AltTF_2020"]

splitddreg=opt.splitregions
#splitddreg=False
if(splitddreg):
    newlistdd=[]
    for l in listdd:
        newlistdd.append(l.replace("_2020","_SR2B_2020"))
        newlistdd.append(l.replace("_2020","_SRT_2020"))
        newlistdd.append(l.replace("_2020","_SRW_2020"))
        newlistdd.append(l.replace("_2020","_CR0B_2020"))
    listdd= copy.deepcopy(newlistdd)

#crlist=["CR_2020"]

systs.extend(["WJets","ST","TT_Mtt"]+listdd)
snames=[]
for s in systs:
    if s=="noSyst":
        snames.append("")
    else:
        snames.append("_"+s+"Up")
        snames.append("_"+s+"Down")
lepslabel={"muon":"mu","electron":"ele"}

#corrections={"CR0B":["CR0B_II","CR0B_II"],"SRT":["SRT_II","SRT_II"],"SRW":["SRW_II","SRW_II"]}
corrections={"CR0B":["CR0B_II","CR0B_II"],"SR2B":["SRT_II","SRT_II"],"SRT":["SRT_II","SRT_II"],"SRW":["CR0B_II","CR0B_II"]}
#corrections={"CR0B":["CR0B_II","CR0B_II"]}

splitddreg=False #DON'T CHANGE THIS! from here on out it's done in the splitregions.py, don't change it

for lep in leps:
    for s in snames:
        for c in corrections:
            if(s!="" and "_fit" in opt.inputpath):
                sn=s.replace ("Up","_"+lepslabel[lep]+"Up").replace("Down","_"+lepslabel[lep]+"Down")
                sn=s.replace ("Up","_"+lepslabel[lep]+"Up").replace("Down","_"+lepslabel[lep]+"Down")
            else: sn = s
            exss=""
            if splitddreg:
                exss=c+"_"
            fnamepred=pathin+"/"+lep+"/"+pred+"_2020_"+lep+sn+".root"
            fnamedata=pathin+"/"+lep+"/"+data+"_2020_"+lep+".root"
            fnameprednom=pathin+"/"+lep+"/"+pred+"_2020_"+lep+".root"
            fqcd=pathin+"/"+lep+"/QCD_2020_"+lep+".root"
            
            hname_tofix=namemap[c]
            hname_nom=namemap[corrections[c][0]]
            hname_den=namemap[corrections[c][1]]
            print(fnamedata,fnamepred,lep,s,sn,"\n",hname_tofix,hname_nom,hname_den)
            
            f_pred=ROOT.TFile(fnamepred)
            f_data=ROOT.TFile(fnamedata)
            f_qcd=ROOT.TFile(fqcd)
            f_prednom=ROOT.TFile(fnameprednom)
            updateopt="RECREATE"
            
            if(os.path.exists(fnamepred.replace(pred,pred+exss+"corr"))):updateopt="UPDATE"
            f_out=ROOT.TFile(fnamepred.replace(pred,pred+exss+"corr"),updateopt)

            print("fpred ",f_pred, " hnametotfix ",hname_tofix)
            h_tofix=f_pred.Get(hname_tofix)
            h_nom=f_data.Get(hname_nom)
            h_den=f_prednom.Get(hname_den)

            h_den_sub=f_qcd.Get(hname_den)
            print("tofix",h_tofix,"nom",h_nom,"den",h_den," den sub ",h_den_sub)

            h_den.Add(h_den_sub,-1)
            
            h_new=copy.deepcopy(h_tofix)
            h_new.SetName(hname_tofix+"new")
            h_temp=copy.deepcopy(h_tofix)
            h_temp.SetName(hname_tofix+"tmp")
            print(h_new.GetName(),h_temp.GetName(),h_tofix.GetName())

            #Getting the ratio
            h_temp.Reset("ICES")
            h_temp.Add(h_nom)
            h_temp.Divide(h_den)
            for b in range(1,h_temp.GetNbinsX()+1):
                if h_temp.GetBinContent(b)==0:
                    h_temp.SetBinContent(b,1)#dont' perform any operation if no info available
            if("SRW" in c):
                h_temp.Smooth()
#            if("SRW" in c):
#                h_temp.Smooth()
#            h_temp.SetBinContent(1,1)
#            h_temp.SetBinContent(2,1)
#            h_temp.SetBinContent(3,1)
            #Obtaining new histo with the correction
            h_new.Multiply(h_temp)
#            h_new.Scale(1/h_temp.Integral())
            #writing in the corr file
                
            f_out.cd()
            h_tofix.Write(h_new.GetName().replace("new","pred"), ROOT.TObject.kOverwrite)
            h_new.Write(h_new.GetName().replace("new",""), ROOT.TObject.kOverwrite)
            if splitddreg:
                updateopt2="RECREATE"
                if(os.path.exists(fnamepred.replace(pred,pred+"corr"))):updateopt2="UPDATE"
                f_out_tot=ROOT.TFile(fnamepred.replace(pred,pred+"corr"),updateopt2)
                f_out_tot.cd()
                h_tofix.Write(h_new.GetName().replace("new","pred"), ROOT.TObject.kOverwrite)
                h_new.Write(h_new.GetName().replace("new",""), ROOT.TObject.kOverwrite)
                f_out.cd()
                for c2 in corrections:
                    if c2==c:
                        continue
                    hname_nomc2=namemap[c2]  
                    h_tnomc2=f_pred.Get(hname_nomc2)
                    h_tnomc2.Write( ROOT.TObject.kOverwrite)
            f_out.Close()
            f_prednom.Close()
            f_data.Close()
            f_pred.Close()
clists=[""]

for lep in leps:
    
    for s in snames:
        for cl in clists:
            print (s, lep)
            if(s!="" and "_fit" in opt.inputpath):
                sn=s.replace ("Up","_"+lepslabel[lep]+"Up").replace("Down","_"+lepslabel[lep]+"Down")
            else: sn = s
            exss=""
            if splitddreg:
                exss=c+"_"
           
            fnamepred=pathin+"/"+lep+"/"+pred+"_2020_"+lep+sn+".root"
            fnamedata=pathin+"/"+lep+"/"+data+"_2020_"+lep+".root"
            fnameprednom=pathin+"/"+lep+"/"+pred+"_2020_"+lep+".root"
            if opt.addsystematic and not opt.overwrite:
                if(s==""):
                    nameup=fnamepred.replace(lep+".root",lep+"_CR_"+cl+"2020Up.root")
                    namedown=fnamepred.replace(lep+".root",lep+"_CR_"+cl+"2020Down.root")
                    os.system("cp "+fnamepred.replace(pred,pred+exss+"corr")+" "+nameup)
                    os.system("cp "+fnamepred.replace(pred,pred+exss+"corr")+" "+namedown)
                else:
                    continue

            if opt.overwrite:#addsystematic will not overrule the "overwrite" option
                print("firstcommand")
                if(cl==""):
                    print ("cp "+fnamepred+" "+fnamepred.replace(pred,pred+exss+"old"))
                    if not opt.dryrun:
                        os.system("cp "+fnamepred+" "+fnamepred.replace(pred,pred+exss+"old"))
                        os.system("sleep 0.1")
                        os.system("cp "+fnamepred.replace(pred,pred+exss+"corr")+" "+fnamepred)
                        print("secondcommand")
                    print ("cp "+fnamepred.replace(pred,pred+"corr")+" "+fnamepred)
                    if opt.addsystematic and s=="":#
                        os.system("sleep 0.1")
                        nameup=fnamepred.replace(lep+".root",lep+"_CR_"+cl+"2020Up.root")
                        namedown=fnamepred.replace(lep+".root",lep+"_CR_"+cl+"2020Down.root")
                        print ("cp "+fnamepred.replace(pred,pred+exss+"old")+" "+nameup)
                        print ("cp "+fnamepred.replace(pred,pred+exss+"old")+" "+namedown)
                        if not opt.dryrun:
                            os.system("cp "+fnamepred.replace(pred,pred+exss+"old")+" "+nameup)
                            os.system("cp "+fnamepred.replace(pred,pred+exss+"old")+" "+namedown)


            if(splitddreg):
                clist.extend(corrections)

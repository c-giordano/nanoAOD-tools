import ROOT,os

#from signal import SIGSEGV

fnamed = ROOT.TFile("localtest/v18/plot_merged/muon/Data_2020_muon.root")
hlistd=["h_jets_best_Wprime_m_CR0B_I","gibberish name"]

def writemissingf(missf,missing,foutname="missingPlot.txt"):
    print("zoombie")
    optf="w"
    if(os.path.exists(foutname)):
        optf="a"
    f=file(foutname,optf)
    f.write(missf)
    for m in missing:
        f.write(str(m))

def find_histo_file(fname, hlist): 
    tofind=hlist
    missing=[]
    present=[]
    ROOT.gEnv.SetValue("TFile.Recover",0)
    try:
        f = ROOT.TFile(fname,"READ")
    except:
        print("failed to open file! ")
        missing.extend(tofind)
        return missing,present

    try:
        if f.IsZombie():
            missing.extend(tofind)
            writemissingf(fname,missing)
            return missing,present
    except:
        print "uberZombie!",fname
        missing.extend(tofind)
        writemissingf(fname,missing)
        return missing,present
        #if not f.TestBit(ROOT.TFile.kRecovered):
        #:
    print "checkpoint 2"
    try:
        kl = f.GetListOfKeys()
    except:
        print "keys not found"
        missing.extend(tofind)
        return missing,present

    print "checkpoint 3"
        
    for t in tofind:
        found=False
        #        print "keylist ",[k.GetName() for k in kl ]
        if not (t in [k.GetName() for k in kl ]):
            missing.append(t)
            print t, " not in keylist!"
            continue
        else:
            try :
                h=f.Get((k.GetName()))
                if h!=0:
                    print("found it! ",t )
                    found =True
                    present.append(t)
                    continue
            except:
                print ("histo not found" )
                missing.append(t)

    return missing,present


def is_file_missing(sa,y,missingSamples="missingSamples.txt"):
    isMissing=False
    fmis= file(missingSamples,"r")
    for l in fmis.readlines():
        sn=sa+"_"+y
        if sn in l:
            isMissing=True
            print("missing files list is ",l, "\n found file ",sn, "in it, will skip. ")
            return isMissing

    return isMissing
#mp= find_histo_file(fnamed,hlistd)
#print "found ",mp[1]," missing ",mp[0]

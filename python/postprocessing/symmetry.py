import ROOT 

def symmetry(hists, fUp,fDown,fNom=None,version="shape"):
    if fNom is None:
        return
    filenom = ROOT.TFile()
    filenom = ROOT.TFile.Open(fNom,"UPDATE")
    hnom = ROOT.TH1F()
    fileup = ROOT.TFile.Open(fUp,"UPDATE")
    hup = ROOT.TH1F()
    filedown = ROOT.TFile.Open(fDown,"UPDATE")
    hdown = ROOT.TH1F()
    for h in hists:
        filedown.cd()
        hdown = (ROOT.TH1F)(filedown.Get(h))
        filenom.cd()
        hnom = (ROOT.TH1F)(filenom.Get(h))
        fileup.cd()
        hup = (ROOT.TH1F)(fileup.Get(h))
        if(version=="integral"):
            hup.Scale((hnom.Integral()+(hup.Integral()-hdown.Integral())/2)/hup.Integral())
            hdown.Scale((hnom.Integral()-(hup.Integral()-hdown.Integral())/2)/hdown.Integral())
#            print hdown.GetName(), " ", hdown.Integral()
#            print hup.GetName(), " ", hup.Integral()
        if(version=="shape"):
            for b in range(1,hup.GetNbinsX()+1):
                bnom = hnom.GetBinContent(b)
                bup= hup.GetBinContent(b)
                bdown=hdown.GetBinContent(b)
                
                bupnew=bnom+abs(bup-bdown)/2.0  
                bdownnew=max(0.00001,(bnom-abs(bup-bdown)/2.0))
                print "h name ", hnom.GetName()," bin ", b, " nom ",bnom, " up ", bup, " hdown ", bdown, " hupnew ", bupnew, " hdownnew ", bdownnew

                hup.SetBinContent(b,bupnew)
                hdown.SetBinContent(b,bdownnew)
        fileup.cd()
        hup.Write(h)
        filedown.cd()
        hdown.Write(h)
    filenom.Close()
    fileup.Close()
    filedown.Close()



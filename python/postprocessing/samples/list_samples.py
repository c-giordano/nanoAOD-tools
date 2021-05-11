import os


#os.system("voms-proxy-init -voms cms -rfc")
def dasgo(dataset, outfile):
    os.system("dasgoclient -query='file dataset=" + dataset + " ' --json >& " + outfile +".json" )

class dataset:
    pass

tag_2016 = 'RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7'

WJets_2016 = dataset()
WJets_2016.name = "WJets"
WJets_2016.year = "2016"
WJets_2016.tag = "WJetsToLNu"
WJets_2016.HTsteps = ["HT-200To400", "HT-400To600", "HT-600To800", "HT-800To1200", "HT-1200To2500", "HT-2500ToInf"] #strip("-") for outfile name
WJets_2016.suffix = "_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/"+tag_2016+"-v1/NANOAODSIM"

datasets = [WJets_2016]

for data in datasets:
    for step in data.HTsteps:
        dasgo("/"+data.tag+"_"+step+data.suffix, data.name+"_"+step.replace("-","")+"_"+data.year)
        print "Writing files of /"+data.tag+"_"+step+data.suffix
        #os.system("more " +  data.name+"_"+step.replace("-","")+"_"+data.year+".json")







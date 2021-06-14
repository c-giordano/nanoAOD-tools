#include "TFile.h"
#include "TChain.h"
#include "TChainElement.h"
#include "TTree.h"
#include "TBranch.h"
#include "TH1.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TLorentzVector.h"
#include "RooGlobalFunc.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include <vector>
#include <assert.h>
#include <TMVA/Reader.h>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <cassert>
#include <sstream>
#include "TFileCollection.h"
#include "THashList.h"
#include "TBenchmark.h"
#include "TF1.h"
//#include "../../interface/DMTopVariables.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondTools/BTau/interface/BTagCalibrationReader.h"

using namespace std;


int main(int argc, char **argv)
{
    string path(argv[1]);     // List of root input files (.txt)

    string origFile(argv[2]); // Name of file containing original Tree

    TFileCollection fc("FileCollection", "FileCollection", path.c_str());

    TString treePath = "scores";

    TChain chain(treePath);
    chain.AddFileInfoList(fc.GetList());

    /* --------- Creation of lower limits for Looping ----------- */
    
    TObjArray *fileElements = chain.GetListOfFiles();
    TIter next(fileElements);
    TChainElement *chEl = 0;
    Int_t nFiles = fc.GetNFiles();
    Int_t nEntries[nFiles];
    Int_t low_lim[nFiles];
    int j = 0;
    while (( chEl = (TChainElement*)next() )) {
      TFile f(chEl->GetTitle());
      TTree *T = (TTree*)f.Get("scores");
      nEntries[j] = T->GetEntries();
      j++;
    }
    int sum = 0;
    low_lim[0] = 0;
    for(j=1;j<nFiles;j++){
      sum += nEntries[j-1];
      low_lim[j] = sum;
    }
    
    /* -------- Input Variables & Branches --------- */
    
    UInt_t nTop;
    Int_t nEvent;
    Int_t top_idx;
    Float_t BDT_score;

    chain.SetBranchAddress("nTop", &nTop);
    chain.SetBranchAddress("nEvent", &nEvent);
    chain.SetBranchAddress("Top_index", &top_idx);
    chain.SetBranchAddress("BDT_Score", &BDT_score);


    /* -------- Output Variables & New Branch --------- */
    
    std::vector<Float_t> Top_Score;
    std::vector<Int_t> Top_Index;
    UInt_t Top_Number = 0;

    TFile *f2 = new TFile((origFile).c_str(),"update");

    TTree *tree = (TTree*)f2->Get("Events");

    TBranch *br = tree->Branch("Top_Score",&Top_Score);


    /* ---------- Looping over the Entries ----------- */

    int i=0, p=0, x=0;
    int up_lim = 0;
    int maxTop = 30; //chain.GetMaximum("nTop");
    bool goodTop;
    auto it = Top_Score.begin();
    auto it2 = Top_Index.begin();

    for(int l=chain.GetMinimum("nEvent"); l<=chain.GetMaximum("nEvent"); l++)
    {
	if(l>0 && l%1000==0) {
	  cout << "Processed: " << l-chain.GetMinimum("nEvent") << "/" << chain.GetMaximum("nEvent")-chain.GetMinimum("nEvent") << " entries" << endl;
	}

        Top_Score.clear();
        Top_Index.clear();
	Top_Number = 0;

	for(j=0; j<nFiles; j++){

	    up_lim = low_lim[j] + maxTop;
	    if(up_lim > chain.GetEntries()) up_lim = chain.GetEntries();
	
	    for (i=low_lim[j]; i<up_lim; i++)
	    {
		chain.GetEntry(i);

		if(nEvent==l){

		  Top_Score.push_back(BDT_score);
		  Top_Index.push_back(top_idx);
		  Top_Number = nTop;
    
		  low_lim[j] = i+1;
		}
	    } // Loop over particular top entries
    
	} // Loop over files

    /* ---------- Sort Scores & Add -1 to dR>2 ----------- */

	for(p=0; p<(int)Top_Number; p++){
	  goodTop = false;

	  for(x=0; x<(int)Top_Index.size(); x++){

	    if(p == Top_Index[x]){
	      goodTop = true;

	      if(p != x){

		it = Top_Score.begin();
		it2 = Top_Index.begin();
		Top_Score.insert(it+p, Top_Score[x]);
		Top_Index.insert(it2+p, Top_Index[x]);
		it = Top_Score.begin();
		it2 = Top_Index.begin();
		Top_Score.erase(it+x+1);
		Top_Index.erase(it2+x+1);
	      }
	    }
	  } //Loop over Top indices vector
	  
	  if(goodTop == false){

	    it = Top_Score.begin();
	    it2 = Top_Index.begin();
	    Top_Score.insert(it+p, -1);
	    Top_Index.insert(it2+p, -1);
	  }

	} // Loop over Tops
	
	br->Fill();

    } // Loop over original Entries
    
    tree->Write();
    f2->Close();

    return 1;
}

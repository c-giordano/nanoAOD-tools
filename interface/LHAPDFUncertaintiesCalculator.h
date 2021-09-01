#ifndef PhysicsTools_NanoAODTools_LHAPDFUncertaintiesCalculator_h
#define PhysicsTools_NanoAODTools_LHAPDFUncertaintiesCalculator_h

#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>

#include "LHAPDF/LHAPDF.h"

using namespace std;

class LHAPDFUncertaintiesCalculator {

public:
  LHAPDFUncertaintiesCalculator() {}

  LHAPDFUncertaintiesCalculator(string PDF, string nominalPDF="NNPDF30_lo_as_0118", string method="RMS", bool verbose=false);//Constructor from a single PDF set
  //  LHAPDFUncertaintiesCalculator(vector<string> PDFs,vector<string> methods, bool verbose=false);//Constructor from multiple PDFs
  ~LHAPDFUncertaintiesCalculator(){};//Destructor 
  void setNominalPDF(string PDF){pdf0_=LHAPDF::mkPDF(PDF,0);}//Change the nominal pdf, 
  
  float getWeight(float x1, float x2, int id1, int id2,float scalePDF,string newPDF="NNPDF30_lo_as_0118", bool verbose=false);
  
  float getUncertainty (float x1, float x2, int id1, int id2,float scalePDF, string newPDF="NNPDF_lo_as_118", bool verbose=false);
  //  vector<float> getUncertainties (float x1, float x2, int id1, int id2,float scalePDF, bool verbose=false);

private:
  string PDF_;
  string method_;
  bool verbose_;
  LHAPDF::PDF* pdf0_; // nominal pdf
  LHAPDF::PDFSet set_; // target set 
  vector<LHAPDF::PDF*> pdfs_; // target set replicas

  // not implemented yet: multiple pdf envelope calculation
  vector<string> PDFs_,methods_;
  vector<LHAPDF::PDFSet> sets_;
  // vector<vector <LHAPDF::PDF*> > pdfs_sets_; not implemented yet
};


#endif

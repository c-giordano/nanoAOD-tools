#include "PhysicsTools/NanoAODTools/interface/LHAPDFUncertaintiesCalculator.h"

LHAPDFUncertaintiesCalculator::LHAPDFUncertaintiesCalculator(string nominalPDF, string PDF, string method, bool verbose){
  PDF_=PDF;
  method_=method;
  verbose_=verbose;
 
  pdf0_ = LHAPDF::mkPDF(nominalPDF,0);//Default pdf set is taken as the one at initializaiton

  set_ = LHAPDF::PDFSet(PDF);
  pdfs_ = set_.mkPDFs();
  
   
}

size_t LHAPDFUncertaintiesCalculator::getNReplicas(){
  return (set_.size()-1);// n replicas besides the first
  
}

vector<float> LHAPDFUncertaintiesCalculator::getReplicasWeights(float x1, float x2, int id1, int id2,float scalePDF, string newPDF, bool verbose){


  float fx1_n=pdf0_->xfxQ(id1,x1,scalePDF);
  float fx2_n=pdf0_->xfxQ(id2,x2,scalePDF);

  vector<float> weights_pdfs;
  
  if (newPDF==PDF_){
    const size_t nmem_1=set_.size();
    const size_t npar_1=LHAPDF::countchar(set_.errorType(), '+');
    const size_t npdfmem_1 = nmem_1-2*npar_1;

    
    for (size_t imem = 1; imem < npdfmem_1; imem++) {
      weights_pdfs.push_back((pdfs_[imem]->xfxQ(id1,x1,scalePDF)*(pdfs_[imem]->xfxQ(id2,x2,scalePDF) ) ) /(fx1_n*fx2_n) );
      if(verbose){
	cout << " checking replica: weight "<<weights_pdfs[imem]<<endl;
      }
    }
  }
  return weights_pdfs;
}

float LHAPDFUncertaintiesCalculator::getWeight(float x1, float x2, int id1, int id2,float scalePDF, string newPDF, bool verbose){
  
  float newweight=1.;

  float fx1_n=pdf0_->xfxQ(id1,x1,scalePDF);
  float fx2_n=pdf0_->xfxQ(id2,x2,scalePDF);

  if (newPDF==PDF_){
    newweight=pdfs_.at(0)->xfxQ(id1,x1,scalePDF)*pdfs_.at(0)->xfxQ(id2,x2,scalePDF) /(fx1_n*fx2_n);  
  }
  return newweight;
}

float LHAPDFUncertaintiesCalculator::getUncertainty(float x1, float x2, int id1, int id2,float scalePDF, string newPDF, bool verbose){

  double mean=0;   
  double devst=0;
  double sigma=0;

  float fx1_n=pdf0_->xfxQ(id1,x1,scalePDF);
  float fx2_n=pdf0_->xfxQ(id2,x2,scalePDF);
  
  if (newPDF==PDF_){
    const size_t nmem_1=set_.size();
    const size_t npar_1=LHAPDF::countchar(set_.errorType(), '+');
    const size_t npdfmem_1 = nmem_1-2*npar_1;

    vector<float> weights_pdfs;
    
    for (size_t imem = 1; imem < npdfmem_1; imem++) {//Note: the 0th weight is the nominal one, will omit it 
      weights_pdfs.push_back((pdfs_[imem]->xfxQ(id1,x1,scalePDF)*(pdfs_[imem]->xfxQ(id2,x2,scalePDF) ) ) /(fx1_n*fx2_n) );
      mean+=weights_pdfs[imem];
      if(verbose){
	cout << " checking replica: weight "<<weights_pdfs[imem]<<endl;
	cout<<"val is "<<" sum "<<mean<<" tempmean "<<mean/(imem+1-1) <<endl; //Note: the -1 is for taking out the nominal central weight.
      }
    }
    mean=mean/(npdfmem_1-1);
    for (size_t imem = 1; imem < npdfmem_1; imem++) {
      devst= (weights_pdfs[imem]-mean)*(weights_pdfs[imem]-mean);
      if(verbose)cout<<"val is "<<" sum dev "<<devst<<" tempdevst "<< devst/(imem+1-1)<<" tempsigma "<<sqrt(devst/(imem+1-1-1)) <<endl;
    }    
    if(verbose )cout << " sum dev tot "<< devst<<" devst"<<devst/(npdfmem_1-1)<< " sigma "<< sqrt(devst/(npdfmem_1-1-1))<<endl;
    sigma=sqrt(devst/(npdfmem_1-1-1));
  }
  
  
  if(newPDF!=PDF_){
    if(sets_.size()==0){
      cout << "careful! PDF is not the one in memory!"<<endl;
	}
    else{
      for (size_t i = 0; i < PDFs_.size(); ++i){
	if (newPDF==PDFs_.at(i)){
	  cout << " not implemented yet!!! "<<endl;
	  return sigma;
	}
      } 
    }
  }
  return sigma;
}

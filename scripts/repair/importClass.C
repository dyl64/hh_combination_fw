#include "TROOT.h"
#include <RooCategory.h>
#include <RooAbsPdf.h>
#include <RooSimultaneous.h>
#include <RooRealVar.h>
#include "RooStats/AsymptoticCalculator.h"
#include "TFile.h"
#include "TSystem.h"
#include <RooArgList.h>
#include "TString.h"
using namespace RooFit;
using namespace RooStats;
using namespace std;


void importClass( const char* infile = NULL, const char* outfile = NULL) 
{
  cout << "Reading file " << infile << endl;

  gROOT->ProcessLine(".L HggTwoSidedCBPdf.cxx+");

  // Read into the Workspace
  TFile* f = new TFile( infile );
  RooWorkspace* ws = (RooWorkspace*) f->Get( "combination" );
  //ws->SetName("combined");

  RooAbsData* obsData = ws->data("obsData");
  obsData->Print();

  // Set the mu_* to be 1 and constant, they are floating for 
  // some studyies in the bbyy analysis.
  //if (ws->var("npbBSM")) {
  //  ws->var("npbBSM")->setRange(1.000,5.00);
  //}

  //if (ws->var("xsec_br")) {
  //  ws->var("xsec_br")->setRange(0.00,5.00);
  //}

  if (ws->var("mu")) {
    cout<<"has mu"<<endl;
    ws->var("mu")->setVal(1);
    ws->var("mu")->setConstant();
  }

  if (ws->var("mu_XS_VBF")) {
    cout<<"has mu_XS_VBF"<<endl;
    ws->var("mu_XS_VBF")->setVal(1);
    ws->var("mu_XS_VBF")->setConstant();
  }

  if (ws->var("mu_XS_ggF")) {
    cout<<"has mu_XS_ggF"<<endl;
    ws->var("mu_XS_ggF")->setVal(1);
    ws->var("mu_XS_ggF")->setConstant();
  }

  TString mcName = "mconfig";

  // Read into the ModelConfig
  ModelConfig* mc =(ModelConfig*) (ws->obj(mcName));
  //mc->SetName("ModelConfig");
  //ws->SetModelConfig 

  //ws->var("npbBSM")->SetName("mu"); 


  TString catName = "bbyy";

  //RooCategory* channelCat = new RooCategory(catName,"bbyy");
  RooCategory* channelCat = new RooCategory(*ws->cat("channellist"));
//  channelCat->SetName("channelList");
  //RooSimultaneous* simPdf = new RooSimultaneous("simPdf","RooSimultaneous Pdf", *channelCat);
  //RooSimultaneous* simPdf = new RooSimultaneous(*mc->GetPdf());

  channelCat->Print();

  //RooCategory* cat = (RooCategory*) &mc->GetPdf()->indexCat();
  //cat->Print();

  //RooRealVar* var = NULL;
  //TIterator* itr = channelCat->createIterator();
  //while (var = (RooRealVar*) itr->Next()) {
  //    string varName(var->GetName());
  //    cout<<"Name Category: "<<varName<<endl;

  //}

  mc->GetPdf()->Print();

  // Read into the model in the ModelConfig
//  RooAbsPdf* ModelPdf = (RooAbsPdf*) mc->GetPdf();
//  ModelPdf->Print();

//  channelCat->defineType(catName);
//  simPdf->addPdf(*ModelPdf,catName);

//  ws->import(*simPdf);
//  mc->SetPdf(*simPdf);

  RooRealVar *obsVar = ws->var("gg_mass");

  RooArgList obsList("obsList");
  obsList.add(*ws->var("gg_mass"));
  obsList.add(*channelCat);
  ws->factory("weightVar[1,-1e10,1e10]");
  obsList.add(*ws->var("weightVar"));
  RooRealVar* weight = ws->var("weightVar");
  weight->Print();
  obsList.add(*weight);

  ws->defineSet("Observables",obsList);
  mc->SetObservables(*ws->set("Observables"));

  ws->SetName("combined");
  mc->SetName("ModelConfig");

  // Generate the Asimov Dataset
  ws->var("gg_mass")->setBins(110);
  ws->var("npbBSM")->setVal(0);  //old name: npbBSM  //new name: mu_hh (for lambda samples)
  RooDataSet* asimovData = (RooDataSet*) RooStats::AsymptoticCalculator::GenerateAsimovData(*ws->pdf("CombinedPdf"),obsList);
  ws->import(*asimovData,Rename("asimovData"));

  asimovData->Print();

//  TIterator* iter = channelCat->typeIterator();
//  RooCatType* tt = NULL;
//
//  RooDataSet* obsdata1 =NULL;
//  RooDataSet* obsdata2 =NULL;
//  TString cat1Name;
//  TString cat2Name;
//  int i =1; 
//  while ((tt = (RooCatType*) iter->Next())) {
//  //  i = 1;
//    if (i==1) {
//      obsdata1 = (RooDataSet*) obsData->getSimData(tt->GetName());
//      //obsdata1->Print();
//      cat1Name = tt->GetName(); 
//      cout<<""<<tt->GetName()<<endl;
//    } 
//    if (i==2) {
//      obsdata2 = (RooDataSet*) obsData->getSimData(tt->GetName());
//      obsdata2->Print();
//      cat2Name = tt->GetName();
//      cout<<""<<tt->GetName()<<endl;
//    }
//    
//    i++; 
//  }
//  cout<<"test"<<endl;
//
//  RooDataSet* tempData1 = new RooDataSet("com1Data", "com1Data", obsList, Index(*channelCat),WeightVar("weightVar"),Import(cat1Name,*obsdata1));
//  cout<<"test1"<<endl;
//  RooDataSet* tempData2 = new RooDataSet("com2Data", "com2Data", obsList, Index(*channelCat),WeightVar("weightVar"),Import(cat2Name,*obsdata2));
//  cout<<"test2"<<endl;
//  RooDataSet* simData = NULL;
//  simData = tempData1;
//  simData->append(*tempData2);
//  ws->import(*simData,Rename("comData"));

  // ws->addClassDeclImportDir("/afs/cern.ch/work/l/liq/hhcombination/");
  ws->addClassDeclImportDir("./");
  ws->importClassCode();

  ws->writeToFile(outfile);

  //ws->Print();

  return;
}

/*
 * Mimic the behaviour in submodules/workspaceCombiner/src/fitUtil.cc:fitUtil::profileToData
*/
using namespace RooFit;
using namespace RooStats;

int profileToData(ModelConfig *mc, RooAbsData *data);

int fit() {
    //TFile* file = new TFile("../output/v140invfb_20210309/rescaled/nonres/bbyy/0_with_Asimov_POI_0_NP_fit.root");
    //TFile* file = new TFile("../input/20210309/bbyy/nonres/0.root");
    TFile* file = new TFile("/afs/cern.ch/user/n/nhehir/public/forRui/bbyy_ws/0_with_Asimov_POI_0_NP_fit.root");
    //TFile* file = new TFile("../output/v140invfb_20210309/regularised/nonres/bbyy/0.root");
    RooWorkspace *w = (RooWorkspace *)file->Get("combWS");

    if (!w) {
        cout << "workspace not found" << endl;
        return 0;
    }

    // get the modelConfig out of the file
    ModelConfig *mc = (ModelConfig *)w->obj("ModelConfig");
    // make sure ingredients are found
    if (!mc) {
        cout << "ModelConfig was not found" << endl;
        return 0;
    }

  RooArgSet* nuis = const_cast<RooArgSet*>(mc->GetNuisanceParameters()); nuis->sort();
  RooArgSet* gobs = const_cast<RooArgSet*>(mc->GetGlobalObservables()); gobs->sort();

  std::cout << "\t~~~~~~~~~~~~~~~~~~~~~~~~" << std::endl;
  std::cout << "\t~~~~~Simple Summary~~~~~" << std::endl;
  std::cout << "\t~~~~~~~~~~~~~~~~~~~~~~~~" << std::endl;
  printf("There are %d nuisances parameters:\n", mc->GetNuisanceParameters()->getSize());
  nuis->Print();
  std::cout << "\t~~~~~~~~~~~~~~~~~~~~~~~~" << std::endl;
  printf("There are %d global observables:\n", mc->GetGlobalObservables()->getSize());
  gobs->Print();
  std::cout << "\t~~~~~~~~~~~~~~~~~~~~~~~~" << std::endl;


    // get the modelConfig out of the file
    RooAbsData *data = w->data("combData");
    //RooAbsData *data = w->data("bbyy_data");

    // make sure ingredients are found
    if (!data ) {
        w->Print();
        cout << "data was not found" << endl;
        return 0;
    }


    //ModelConfig* mc, RooAbsData& realdata
    RooArgSet  poi( *mc->GetParametersOfInterest() );
    //poi.Print("v");
    RooRealVar* r = dynamic_cast<RooRealVar*>( poi.first() );
    //printf("There are %d pois:\n", poi.getSize());
    //poi.Print("v");
    //std::cout << "\t~~~~~~~~~~~~~~~~~~~~~~~~" << std::endl;

    double poiValue = 0; // 0, 1, -100(free fit)
    if ( poiValue<-99 ) {
        r->setConstant(false);
    } else {
        r->setConstant( true );
        r->setVal( poiValue );
    }

    profileToData(mc, data);
    std::cout << "REGTEST: Fit finished" << std::endl;
    return 0;
}

int profileToData(ModelConfig *mc, RooAbsData *data){
    RooAbsPdf *pdf=mc->GetPdf();
    RooWorkspace *w=mc->GetWS();
    RooArgSet funcs = w->allPdfs();

    unique_ptr<RooAbsReal> nll;
    nll.reset(pdf->createNLL(*data, Constrain(*mc->GetNuisanceParameters()), GlobalObservables(*mc->GetGlobalObservables())));

    RooMinimizer minim(*nll);
    minim.setVerbose();
    minim.setStrategy(2);
    minim.setPrintLevel(3);
    minim.setProfile(); /* print out time */
    minim.setEps(0.001/0.001);
    minim.setOffsetting(true);
    if(true) minim.optimizeConst(2);

    minim.setMinimizerType("Minuit2"); // Suggested by Nicolas M.
    minim.setMaxFunctionCalls(5000*mc->GetPdf()->getVariables()->getSize());//suggest by Stefan G.
    int status=minim.minimize("Minuit2");

    return status;
}

int printSummary(ModelConfig *m_mc, bool verbose)
{
  assert ( m_mc );
  RooStats::ModelConfig* m_mc;
  RooWorkspace* m_comb;
  RooAbsData* m_data;
  // RooRealVar* m_poi;
  RooArgSet m_poi;


  RooSimultaneous* m_pdf = dynamic_cast<RooSimultaneous*>(m_mc->GetPdf()); assert (m_pdf);
  RooCategory* m_cat = (RooCategory*)&m_pdf->indexCat();
  RooArgSet* m_gobs = dynamic_cast<const RooArgSet*>(m_mc->GetGlobalObservables()); assert(m_gobs);
  RooArgSet* m_nuis = const_cast<RooArgSet*>(m_mc->GetNuisanceParameters()); assert(m_nuis);
  int numChannels = m_cat->numBins(0);


  std::cout << "\t~~~~~~~~Begin Summary~~~~~~~~" << std::endl;
  std::cout << "\tThere are " << numChannels << " sub channels:" << std::endl;
  for ( int i= 0; i < numChannels; i++ ) {
    m_cat->setBin(i);
    TString channelname=m_cat->getLabel();
    RooAbsPdf* pdfi = m_pdf->getPdf(channelname);
    RooDataSet* datai = ( RooDataSet* )( m_dataList->FindObject( channelname ) );
    std::cout << "\t\tIndex: " << i << ", Pdf: " << pdfi->GetName() << ", Data: " << datai->GetName()  << ", SumEntries: " << datai->sumEntries() << std::endl;
  }
}

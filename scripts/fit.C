/*
 * Mimic the behaviour in submodules/workspaceCombiner/src/fitUtil.cc:fitUtil::profileToData
*/
using namespace RooFit;
using namespace RooStats;

int profileToData(ModelConfig *mc, RooAbsData *data);

int fit() {
    TFile* file = new TFile("../output/v140invfb_20210309/rescaled/nonres/bbyy/0_with_Asimov_POI_0_NP_fit.root");
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


using namespace std;
using namespace RooFit;
using namespace RooStats;

RooWorkspace* w = NULL;
ModelConfig* mc = NULL;
RooDataSet* data = NULL;
int global_status=0;

int maxRetries = 3;

RooNLLVar* createNLL(RooDataSet* _data, ModelConfig* mc)
{
  RooArgSet nuis = *mc->GetNuisanceParameters();
  RooNLLVar* nll = (RooNLLVar*)mc->GetPdf()->createNLL(*_data, Constrain(nuis));
  return nll;
}

int minimize(RooAbsReal* fcn)
{
  static int nrItr = 0;
   // cout << "Starting minimization. Using these global observables" << endl;
   // mc->GetGlobalObservables()->Print("v");


  int printLevel = ROOT::Math::MinimizerOptions::DefaultPrintLevel();
  RooFit::MsgLevel msglevel = RooMsgService::instance().globalKillBelow();
  if (printLevel < 0) RooMsgService::instance().setGlobalKillBelow(RooFit::FATAL);

  int strat = ROOT::Math::MinimizerOptions::DefaultStrategy();
  int save_strat = strat;
  RooMinimizer minim(*fcn);
  minim.setStrategy(strat);
  minim.setPrintLevel(printLevel);


  int status = minim.minimize(ROOT::Math::MinimizerOptions::DefaultMinimizerType().c_str(), ROOT::Math::MinimizerOptions::DefaultMinimizerAlgo().c_str());


//up the strategy
  if (status != 0 && status != 1 && strat < 2)
  {
    strat++;
    cout << "Fit failed with status " << status << ". Retrying with strategy " << strat << endl;
    minim.setStrategy(strat);
    status = minim.minimize(ROOT::Math::MinimizerOptions::DefaultMinimizerType().c_str(), ROOT::Math::MinimizerOptions::DefaultMinimizerAlgo().c_str());
  }

  if (status != 0 && status != 1 && strat < 2)
  {
    strat++;
    cout << "Fit failed with status " << status << ". Retrying with strategy " << strat << endl;
    minim.setStrategy(strat);
    status = minim.minimize(ROOT::Math::MinimizerOptions::DefaultMinimizerType().c_str(), ROOT::Math::MinimizerOptions::DefaultMinimizerAlgo().c_str());
  }

  //cout << "status is " << status << endl;

// //switch minuit version and try again
  if (status != 0 && status != 1)
  {
    string minType = ROOT::Math::MinimizerOptions::DefaultMinimizerType();
    string newMinType;
    if (minType == "Minuit2") newMinType = "Minuit";
    else newMinType = "Minuit2";
  
    cout << "Switching minuit type from " << minType << " to " << newMinType << endl;
  
    ROOT::Math::MinimizerOptions::SetDefaultMinimizer(newMinType.c_str());
    strat = ROOT::Math::MinimizerOptions::DefaultStrategy();
    minim.setStrategy(strat);

    status = minim.minimize(ROOT::Math::MinimizerOptions::DefaultMinimizerType().c_str(), ROOT::Math::MinimizerOptions::DefaultMinimizerAlgo().c_str());


    if (status != 0 && status != 1 && strat < 2)
    {
      strat++;
      cout << "Fit failed with status " << status << ". Retrying with strategy " << strat << endl;
      minim.setStrategy(strat);
      status = minim.minimize(ROOT::Math::MinimizerOptions::DefaultMinimizerType().c_str(), ROOT::Math::MinimizerOptions::DefaultMinimizerAlgo().c_str());
    }

    if (status != 0 && status != 1 && strat < 2)
    {
      strat++;
      cout << "Fit failed with status " << status << ". Retrying with strategy " << strat << endl;
      minim.setStrategy(strat);
      status = minim.minimize(ROOT::Math::MinimizerOptions::DefaultMinimizerType().c_str(), ROOT::Math::MinimizerOptions::DefaultMinimizerAlgo().c_str());
    }

    ROOT::Math::MinimizerOptions::SetDefaultMinimizer(minType.c_str());
  }

  if (status != 0 && status != 1)
  {
    nrItr++;
    if (nrItr > maxRetries)
    {
      nrItr = 0;
      global_status++;
      cout << "WARNING::Fit failure unresolved with status " << status << endl;
      return status;
    }
    else
    {
      if (nrItr == 0) // retry with mu=0 snapshot
      {
	w->loadSnapshot("conditionalNuis_0");
	return minimize(fcn);
      }
      else if (nrItr == 1) // retry with nominal snapshot
      {
	w->loadSnapshot("nominalNuis");
	return minimize(fcn);
      }
    }
  }

  if (printLevel < 0) RooMsgService::instance().setGlobalKillBelow(msglevel);
  ROOT::Math::MinimizerOptions::SetDefaultStrategy(save_strat);


  if (nrItr != 0) cout << "Successful fit" << endl;
  nrItr=0;
  return status;
}

int minimize(RooNLLVar* nll)
{
  RooAbsReal* fcn = (RooAbsReal*)nll;
  return minimize(fcn);
}

RooArgSet* findGlobalObservable (const RooAbsPdf& pdf, const RooArgSet& np, const RooArgSet& obs, const RooArgSet& gobs)
{
  RooArgSet* found= new RooArgSet;
  RooArgSet nptmp= np;
  RooArgSet* cons= pdf.getAllConstraints(obs,nptmp);
  for (RooFIter it= cons->fwdIterator(); RooAbsArg* p= it.next();) {
    found->add(*p->getObservables(gobs));
  }
  delete cons;
  return found;
}

bool keeplumi( TString s ){
  
  if( s.Contains("lumi", TString::ECaseCompare::kIgnoreCase) ){
    return true;
  }else{
    return false;
  }

}

///////////////////////

void fixnp_allforbbyy(){
  
  using namespace RooFit;
  using namespace RooStats;

  cout << "Load in libs" << endl;
  gROOT->ProcessLine(".L ExpGausExpPDF_cc.so");
  gROOT->ProcessLine(".L HggTwoSidedCBPdf_cc.so");
  gROOT->ProcessLine(".L RooNovosibirsk_nancy_cc.so");

  // ### only for bbyy non-resonant ###
  const char* fname = "/eos/atlas/atlascerngroupdisk/phys-higgs/HSG6/HH/combination/workspaces/to_be_processed_originals/bbyy/2018_08_10/nonres/0.root";
  cout << "Open ROOT file: " << fname << endl;
  TFile f( fname );

  cout << "Retrieve workspace modelconfig dataset" << endl;
  w = (RooWorkspace*) f.Get("combined");
  mc = (ModelConfig*) w->obj("ModelConfig");
  data = (RooDataSet*) w->data("obsData");

  // create nll
  cout << "Create NLL with obs data" << endl;
  RooNLLVar* obs_nll = createNLL(data, mc);

  // prefit
  cout << "Minize NLL with obs data to profile NPs" << endl;
  minimize( obs_nll );

  // fix them to their best fitted values to obsdata
/*
  const RooArgSet * nplist= mc->GetNuisanceParameters();
  RooArgSet* nplist_save = new RooArgSet(*nplist);
  RooArgSet* gobslist_save = new RooArgSet( *mc->GetGlobalObservables() );
  TIterator* itr = nplist->createIterator();
  RooRealVar* var;
  while((var = (RooRealVar*)itr->Next())){
    if( keeplumi( var->GetName() ) ){
	  // keep NP
	}else{
	  // set constant NP
      cout << "NP [" << var->GetName() << "]: fixed to " << var->getVal() << endl;
	  var->setConstant(1);
	  nplist_save->remove( *var );
      RooArgSet* gobslist_rm= findGlobalObservable (*mc->GetPdf(), RooArgSet(*var), *mc->GetObservables(), *gobslist_save );
	  gobslist_save->remove( *gobslist_rm );
      cout << "GOBS to remove "; gobslist_rm->Print();
	}
  }
*/
  RooArgSet* nplist_save = new RooArgSet;
  RooArgSet* gobslist_save = new RooArgSet;
  nplist_save->add( *w->var("lumi_2012") );
  gobslist_save->add( *w->var("RNDM_lumi_2012") );

  mc->SetNuisanceParameters( *nplist_save );
  mc->SetGlobalObservables( *gobslist_save );

  w->writeToFile( Form("FIX_allNPtoProfiled_%s", gSystem->BaseName(fname) ) );

}

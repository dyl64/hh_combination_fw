// NOTE: For bbyy non-resonant use fixnp_allforbbyy.C

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

/*
bool keeplumi( TString s ){
  
  if( s.Contains("lumi", TString::ECaseCompare::kIgnoreCase) ){
    return true;
  }else{
    return false;
  }

}
*/

///////////////////////

void fixnp_all_new(){
  
  using namespace RooFit;
  using namespace RooStats;

  cout << "Load in libs" << endl;
  gROOT->ProcessLine(".L ExpGausExpPDF_cc.so");
  gROOT->ProcessLine(".L HggTwoSidedCBPdf_cc.so");
  gROOT->ProcessLine(".L RooNovosibirsk_nancy_cc.so");

  // ### For bbyy non-resonant use fixnp_allforbbyy.C ###
  std::string model = "nonres";
  std::string channel = "bbbb";

  TString baseName = "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02";


  std::map<std::string, std::map<std::string, std::vector<int> > > point_map;

  std::vector<int> points_nonres = {0};
  std::vector<int> points_lambda = {-20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20};

  point_map["spin0"]["bbbb"] = {260, 270, 275, 280, 290, 300, 325, 350, 400, 450, 500, 550, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000};
  point_map["spin0"]["bbtautau"] = {260, 275, 300, 325, 350, 400, 450, 500, 550, 600, 700, 800, 900, 1000};
  point_map["spin0"]["bbyy"] = {260, 275, 300, 325, 350, 400, 450, 500, 550, 600, 700, 800, 900, 1000};
  point_map["spin0"]["WWyy"] = {260, 275, 300, 325, 350, 400, 450, 500};
  point_map["spin0"]["bbWW"] = {500, 550, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000};
  point_map["spin0"]["WWWW"] = {260, 275, 300, 325, 350, 400, 450, 500};

  point_map["spin2_c_1.0"]["bbbb"] = {260, 270, 280, 290, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000};
  point_map["spin2_c_1.0"]["bbtautau"] = {260, 300, 400, 500, 600, 700, 800, 900, 1000};
  point_map["spin2_c_1.0"]["bbWW"] = {500, 600, 700, 750, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000};

  point_map["spin2_c_2.0"]["bbbb"] = {260, 280, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 3000};
  point_map["spin2_c_2.0"]["bbtautau"] = {260, 275, 300, 325, 350, 400, 450, 500, 550, 600, 700, 800, 900, 1000};
  point_map["spin2_c_2.0"]["bbWW"] = {500, 600, 700, 750, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2250, 2500, 2750, 3000};
  
  
  
  std::vector<int> points;

  if (model == "nonres")
    points = points_nonres;
  else if (model == "lambda")
    points = points_lambda;
  else
    points = point_map[model][channel];


  for (int i=0; i<points.size(); i++) {
    
    const char* fname = Form("%s/%s/%s/%i.root", (const char*) baseName, (const char*) channel.c_str(), (const char*) model.c_str(), points[i]);
        
    cout << "Open ROOT file: " << fname << endl;
    TFile f( fname );
    
    cout << "Retrieve workspace modelconfig dataset" << endl;
    if (channel == "combined") {
      w = (RooWorkspace*) f.Get("combWS");
      mc = (ModelConfig*) w->obj("ModelConfig");
      data = (RooDataSet*) w->data("combData");
    }
    if (channel == "WWWW") {
      w = (RooWorkspace*) f.Get("combined");
      mc = (ModelConfig*) w->obj("ModelConfig");
      data = (RooDataSet*) w->data("obsData");
    }
    else if (channel == "bbyy" && model == "spin0") {
      w = (RooWorkspace*) f.Get("combination");
      mc = (ModelConfig*) w->obj("mconfig");
      data = (RooDataSet*) w->data("obsData");
    }
    else {
      w = (RooWorkspace*) f.Get("combined");
      mc = (ModelConfig*) w->obj("ModelConfig");
      data = (RooDataSet*) w->data("obsData");
    }
    
    // create nll
    cout << "Create NLL with obs data" << endl;
    RooNLLVar* obs_nll = createNLL(data, mc);
    
    // prefit
    cout << "Minize NLL with obs data to profile NPs" << endl;
    minimize( obs_nll );
    
    // fix them to their best fitted values to obsdata
    const RooArgSet * nplist= mc->GetNuisanceParameters();
    RooArgSet* nplist_save = new RooArgSet(*nplist);
    RooArgSet* gobslist_save = new RooArgSet( *mc->GetGlobalObservables() );
    TIterator* itr = nplist->createIterator();
    RooRealVar* var;
    int ctr_freenp = 0;
    while((var = (RooRealVar*)itr->Next())){
      
      //    if( keeplumi( var->GetName() ) ){
      //	  // keep NP
      //	}else{
      
      // leave free all bkg norm that are NOT constrained in the model
      // they are past of the stats model instead of syst
      // *** *** *** details *** *** ***
      // the first three in bbWW are QCD estmated in ABCD method and 2 SFs per cut applied later
      // #ATLAS_norm_QCD_inv_Rnp_NbNd_bbWW <— set range 1e-6, consider as strongly constrained
      // #ATLAS_norm_QCD_inv_mbbEff_bbWW <— set range 1e-6, consider as strongly constrained
      // #ATLAS_norm_Sigd0Eff_bbWW <— set range 1e-6, consider as strongly constrained
      // ATLAS_norm_QCD_bbWW
      // ATLAS_norm_ttbar_bbWW
      // ATLAS_norm_QCD_mBBcr_bbWW
      //
      // ATLAS_norm_Zbb_bbtautau
      // ATLAS_norm_ttbar_bbtautau
      //
      // ATLAS_sampleNorm_bkg_ZZ_WWWW
      //
      // c1_WWyy
      // c2_WWyy
      // nConBkgSR_WWyy
      //
      // nbkg_bb_bbyy
      // nbkg_bj_bbyy
      // slope_bb_bbyy
      // slope_bj_bbyy
      //
      // # bbbb bkg norm prefit and constrained with prior
      // alpha_r15_norm_NP0
      // alpha_r15_norm_NP1
      // alpha_r15_norm_NP2
      // alpha_r16_norm_NP0
      // alpha_r16_norm_NP1
      // alpha_r16_norm_NP2
      // *** end ***
      TString varnm( var->GetName() );
      if( varnm.Contains("ATLAS_norm_QCD") // bbWW
	  || varnm.Contains("ATLAS_norm_ttbar") // bbWW
	  || varnm.Contains("ATLAS_norm_QCD_mBBcr") // bbWW
	  || varnm.Contains("ATLAS_norm_Zbb") // bbtautau
	  || varnm.Contains("ATLAS_norm_ttbar") // bbtautau
	  || varnm.Contains("ATLAS_sampleNorm_bkg_ZZ") // WWWW
	  || varnm.Contains("c1") // WWyy
	  || varnm.Contains("c2") // WWyy
	  || varnm.Contains("nConBkgSR") // WWyy
	  || varnm.Contains("nbkg_") // bbyy
	  || varnm.Contains("slope_") // bbyy
	  ){
	if( varnm.Contains("Acc") ){ // bbtautau has NP like alpha_SysRatioHHSRTtbarAcc2Tag that contains "c2" ...
	}else{ // leave free in this case
	  cout << "FOUND free bkg norm factor [REMAIN FREE]: " << varnm << endl;
	  ctr_freenp += 1;
	  continue;
	}
      }
      
      // set constant NP
      cout << "NP [" << var->GetName() << "]: fixed to " << var->getVal() << endl;
      var->setConstant(1);
      nplist_save->remove( *var );
      RooArgSet* gobslist_rm= findGlobalObservable (*mc->GetPdf(), RooArgSet(*var), *mc->GetObservables(), *gobslist_save );
      gobslist_save->remove( *gobslist_rm );
      cout << "GOBS to remove "; gobslist_rm->Print();

    }

    // trick
    if( ctr_freenp == 0 ){ // if no free bkg norm left and no any others ... POI alone in the limit setting reports error
      RooRealVar* hf_lumi = w->var("Lumi"); // the histfactory lognormal Lumi
      hf_lumi->setRange( 1-2e-4, 1+2e-4 );
      hf_lumi->setConstant(0);
    }
    
    mc->SetNuisanceParameters( *nplist_save );
    mc->SetGlobalObservables( *gobslist_save );
    
    w->writeToFile( Form("%s/%s/%s_statOnly/%i.root", (const char*) baseName, (const char*) channel.c_str(), (const char*) model.c_str(), points[i]));
    
    f.Close();
  }
  
}

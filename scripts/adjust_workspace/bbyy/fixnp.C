void fixnp(){
  
  using namespace RooFit;
  using namespace RooStats;

  gROOT->ProcessLine(".L ../../../../lib/ExpGausExpPDF_cc.so");
  gROOT->ProcessLine(".L ../../../../lib/HggTwoSidedCBPdf_cc.so");
  gROOT->ProcessLine(".L ../../../../lib/RooNovosibirsk_nancy_cc.so");

  //const char* fname = "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw/test_input/vfinal_02/bbyy/nonres/processed_workspaces/0_allNPs.root";
  const char* fname = "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbyy/lambda/20.root";
  TFile f( fname );
  RooWorkspace* ws = (RooWorkspace*) f.Get("combined");
  ModelConfig* mc = (ModelConfig*) ws->obj("ModelConfig");

  // find NP
  RooRealVar* np = ws->var("dhhTh");
  RooRealVar* np_gobs = ws->var("RNDM_dhhTh");

  // set and fix NP
  np->Print("v");
  np->setVal(0);
  np->setConstant(1);

  // remove NP from nplist
  RooArgList nplist= *mc->GetNuisanceParameters();
  nplist.remove(*np);
  mc->SetNuisanceParameters(nplist);

  // remove NP globalobservable from gobslist
  RooArgSet gobslist= *mc->GetGlobalObservables();
  gobslist.remove(*np_gobs);
  mc->SetGlobalObservables(gobslist);

  // ws->writeToFile( "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbyy/nonres/0.root" );
  ws->writeToFile( "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/bbyy/lambda_temp/20.root" );

}

int modPOI( const char* infile, const char* outfile, const char* nmpoi = "SigXsecOverSM", TString proj = "" ){

  using namespace RooFit ;
  using namespace RooStats ;
  using namespace std ;

  cout << "reading file " << infile << endl;

  TFile f( infile );
  RooWorkspace* wkspc = (RooWorkspace*) f.Get( "combined" );

/*
m   acc*eff     acc_eff_relto260   acc_eff_relto300
260 0.007503872 1.0                -
270 0.007638304 1.0179150177401748 0.949848786311182
280 0.007772736 1.0358300354803494 0.966565857540788
290 0.007907168 1.053745053220524  0.9832829287703939
300 0.0080416   -                  1.0
*/

  cout << "Modifying POI and removing Lumi" << endl;
  if( proj == "use260_for270" )
    wkspc->factory(Form("EDIT::simPdfMOD(simPdf,%s=prod::CorrectAccEff(SigXsecOverSMMOD[0,-30,30],factor_interp[1.0179150177401748]))",nmpoi));
  if( proj == "use260_for280" )
    wkspc->factory(Form("EDIT::simPdfMOD(simPdf,%s=prod::CorrectAccEff(SigXsecOverSMMOD[0,-30,30],factor_interp[1.0358300354803494]))",nmpoi));
  if( proj == "use260_for290" )
    wkspc->factory(Form("EDIT::simPdfMOD(simPdf,%s=prod::CorrectAccEff(SigXsecOverSMMOD[0,-30,30],factor_interp[1.053745053220524]))",nmpoi));

  if( proj == "use300_for270" )
    wkspc->factory(Form("EDIT::simPdfMOD(simPdf,%s=prod::CorrectAccEff(SigXsecOverSMMOD[0,-30,30],factor_interp[0.949848786311182]))",nmpoi));
  if( proj == "use300_for280" )
    wkspc->factory(Form("EDIT::simPdfMOD(simPdf,%s=prod::CorrectAccEff(SigXsecOverSMMOD[0,-30,30],factor_interp[0.966565857540788]))",nmpoi));
  if( proj == "use300_for290" )
    wkspc->factory(Form("EDIT::simPdfMOD(simPdf,%s=prod::CorrectAccEff(SigXsecOverSMMOD[0,-30,30],factor_interp[0.9832829287703939]))",nmpoi));

  cout << "Registering POI and PDF" << endl;
  ModelConfig* mc = ((ModelConfig*)wkspc->obj("ModelConfig"));

  mc->SetParametersOfInterest( "SigXsecOverSMMOD" );
  mc->SetPdf( *wkspc->pdf("simPdfMOD") );

  wkspc->writeToFile( outfile );

  return 0;
}

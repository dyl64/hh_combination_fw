#include <iostream>

void renameDataSet() {


  using namespace std;
  using namespace RooFit;
  using namespace RooStats;
  
  const char* pathName = "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/input/workspaces/vfinal_02/WWWW/spin0";
  const char* fname = "260.root";

  TString wsname = "combWS";
  TString dataname_old = "combData";
  TString dataname_new = "obsData";

  cout << "Open ROOT file: " << fname << endl;
  TFile f( Form("%s/%s", pathName, fname) );

  cout << "Open workspace '" << wsname << "'" << endl;
  RooWorkspace* w = (RooWorkspace*) f.Get("combWS");
  RooDataSet* data = (RooDataSet*) w->data("combData");

  cout << "Changing dataset name: " << dataname_old << " --> " << dataname_new << endl;
  data->SetName("obsData");
  w->writeToFile(Form("%s/renamed_%s", pathName, fname));

}

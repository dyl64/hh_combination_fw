// CXX
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <limits>
#include <math.h>
#include <map>
#include <tuple>

// ROOT
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TMultiGraph.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TCanvas.h"
#include "TDatime.h"
#include "TGaxis.h"

#include "atlasstyle-00-03-05/AtlasStyle.C"
#include "atlasstyle-00-03-05/AtlasUtils.C"
using namespace std;


typedef std::map<int, std::tuple<double, double, double, double, double, double> > tuplemap;

tuplemap ReadInputFile (std::string inFileName, bool useNominalNPs, bool isNanCompatible);
tuplemap ReadInputFile_LimitsFromPaper (std::string inFileName, bool debug);
tuplemap ReadInputFile_bbyyLimitsFromPaper (std::string inFileName, TString model, bool debug);

// assumes xsec in pb, use scalefactor=1000 for pb->fb
std::map<double, double> ReadTheoryXsec (std::string inFileName, double scalefactor = 1.);   
void ATLASLabel (Double_t x, Double_t y, const char* text, Color_t color);
void ATLASLabelSplit(Double_t x, Double_t y, const char* text, Color_t color);
int StrToInt (std::string str);
std::vector<double> GetIntersectionsOfGraphs(TGraph* gr1, TGraph* gr2, double xMinStart = -999., double xMaxStart = -999., bool debug = false, TCanvas *c = nullptr, TMultiGraph* tmg = nullptr, TString cha ="", TString type = "obs");
std::vector<double> FindNullPos(TSpline3* spline, double min, double max);

void DrawTSpline(TString cha = "", TSpline3* spline_diff = nullptr, double xstart = 10.0, int npoints = 500, TCanvas *c = nullptr, TLegend* lg3 = nullptr, TMultiGraph* tmg = nullptr, double step = 0.01);
TGraph* ExtendTGraphByTSpline(TGraph *gr = nullptr);
TGraphAsymmErrors* ExtendTGraphAsymmErrorsByTSpline(TGraphAsymmErrors *gr = nullptr);


double s2f( std::string n ){
  TString s(n);
  if( s.Contains("nan", TString::kIgnoreCase) ){
    return -999;
  }
  else{
    return s.Atof();
  }
}

int NdotsToAdd(TGraph* gr, double Len)
{
  int ndots = gr->GetN();
  double step = gr->GetX()[1] - gr->GetX()[0]; 
  int NumAdd = int(Len/step);
  cout<<"Will add "<<NumAdd<<" points to TGraph or TGraphAsymmErrors"<<endl;

  return NumAdd;
}


void GenerateTGraphAsymmErrors(TGraphAsymmErrors *gr = nullptr)
{
  // 
  // here to judge if there is one exsiting file.
  // TSystem
   
  if (true) {
    //int ndots = gr->GetN();
   
    double Length = 1.0;
    //int n_points = ndots + NdotsToAdd(gr, Length);
    int n_points = 420;
    // is here 'w'?   
    TFile* f = new TFile("extend_lambda_limits_plot.root","RECREATE");
    TGraphAsymmErrors* extend = new TGraphAsymmErrors(n_points);  
    extend->SetName("nonres_lambda_theory_band");

    double xPoi = -50;
    double lambdaVal = 0;
    int binNum = 0;
    double YErrorHi = 0.0;
    double YErrorLo = 0.0;

    for (int n=0; n<n_points+1; n++) {
      xPoi = -21+n*0.1;
      if (xPoi == 0) continue;
      lambdaVal = 0.0711561 + xPoi*(-0.0476268) + xPoi*xPoi*0.00991164;

      YErrorHi = lambdaVal*0.10686;   
      YErrorLo = lambdaVal*0.10686;   
 
      if (xPoi>0)
        binNum = n -1;   
      else binNum = n;

      extend->SetPoint(binNum,xPoi,lambdaVal);
      extend->SetPointEXhigh(binNum,0);
      extend->SetPointEXlow (binNum,0);
      extend->SetPointEYhigh(binNum,YErrorHi);
      extend->SetPointEYlow (binNum,YErrorLo);
    }
    f->cd();
    extend->Write();
    f->Close();
  }
  else {
    printf("There is one root file saving the Theoritical Lambda Curve locally\n");
  }
} 


void PrintTGraphAsymmErrors(TGraphAsymmErrors* gr, bool debug=false)
{
  int npoints = gr->GetN();
  for (int i = 0; i < npoints; i++) {
    double X = gr->GetX()[i];
    double Y = gr->GetY()[i];
    //cout<<"X: "<<X<<" Y: "<<Y<<" YErrorHigh: "<<gr->GetErrorYhigh(i)<<" YErrorLow: "<<gr->GetErrorYlow(i)<<endl;
    if (debug)
      cout<<"fractional error Y_Error_Up: "<<gr->GetErrorYhigh(i)/Y<<" Y_Error_Low: "<<gr->GetErrorYlow(i)/Y<<endl;
  }
}


void PrintTGraph(TGraph* gr, bool debug=false)
{
  int npoints = gr->GetN();
  for (int i = 0; i < npoints; i++) {
    double X = gr->GetX()[i];
    double Y = gr->GetY()[i];
    if (debug)
      cout<<"X: "<<X<<" Y: "<<Y<<endl;
  }
}


void drawTSpline(TSpline3* sp)
{
    TCanvas*c3 = new TCanvas("c3","c3",800,600);
    c3->cd();
    sp->Draw();
    c3->Update();
    c3->SaveAs("spline.pdf");
}


TLegend * lg3 = nullptr;
TString ObsOrExp = "";


std::istream& skipline( std::istream& in )
{
  return in.ignore( std::numeric_limits< std::streamsize >::max(), '\n' );
}


int MakeLimitPlots_resonant_paper_newStyle() 
{
  SetAtlasStyle();

  lg3 =  new TLegend(0.315,0.69,0.615,0.74);

  // settings
  
  TString internal = "Internal"; // "Internal" "Preliminary" ""

  TString strModel = "spin-0"; // lambda spin-0 spin-2
  TString strCoupling = "c = 1.0";   // only relevant for spin-2
  TString strCMSenergy = "13 TeV";
  TString strLumi = "139";
  TString strOutfile = "";

  TString version = "v140invfb_20210531_obs2";
  std::string npCorrInfo = "NPnocorr"; // "nocorr" ""

  bool doHepData = false;
  TString hepdatafilename = ""; // will be strOutfile-HEPDATA.root
  TFile* hepdatafile = 0;
  TDirectory* _tmpdir = 0; // for tmp save pwd when swithing to hepdata root file saving operation

  // (savePlots,savePad1,savePad2)
  // false,...,... : no save
  // true,false,false: save spin0 or 2 or lambda with legend per plot
  // true,true,false : save spin0 or 2 or lambda plots without legend
  // true,false,true : save legend only (in eps, as pdf dose not work ...)
  bool debug = false;
  bool savePlots = true; // save plots to ./limit_plots
  bool savePad1 = false; // save pad1 (limit plot) only
  bool savePad2 = false; // save pad2 (legend) only
  bool useNominalNPs = false;  // nominal or profiled?
  bool drawObserved = true;  // draw observed limit curve in plot?
  bool extendTo3TeV = strModel.Contains("spin") && false;
  bool isNanCompatible = true; // take nan as -999 in limits
  bool is2ColumnLegend = strModel.Contains("spin") && true; // for spin0/2 separate plots and 2-col legends only!
  bool oneLegEntryPerChannel = false;
  
  bool conf = false;          // conf=true: 4b+bbtautau+bbyy, conf=false: all channels
  bool doLogScale = true;
  bool doLogScaleX = true;
  bool statOnly = (strModel=="lambda") && false;
  bool doExtend = (strModel=="lambda") && true; // extend range in lambda plot from -21 to 21 (to find crossing point between 4b and theory) [implemented by Qi] MUSTDO for 36.1/fb analyses lambda scan ONLY!
  bool calculateExclusions = (strModel=="lambda") && true; // show allowed lambda interval in lambda limit plots
  bool useUserXRange = true;
  bool doExtrapolationTo140fb = false;
  bool doExtrapolationTo440fb = false;
  

  std::map<TString, bool> printLimits;
  printLimits["bbbb"] = false;
  printLimits["bbtautau"] = false;
  printLimits["bbyy"] = false;
  printLimits["comb"] = false;


  std::map<TString, bool> useLimitsFromPaper;
  useLimitsFromPaper["bbbb"] = false;
  useLimitsFromPaper["bbtautau"] = false;
  if (statOnly)
    useLimitsFromPaper["bbyy"] = false;
  else
    useLimitsFromPaper["bbyy"] = false;


  double xmin, xmax;
  if (useUserXRange) {
    xmin = 250.0;
    xmax = 2000.;
  }


  TString PathOut = "./";

  if (conf && statOnly)
    drawObserved = false;
  

  //__________________________________________________________________________
  if (strModel.EqualTo("spin-0")) {
    if (conf) {
      if (statOnly) {
	strOutfile = PathOut+"limit_plots/limits_spin0_bbbb_bbtt_bbyy_comb_"+version+"_conf_statOnly_exp";
      }
      else {
	strOutfile = PathOut+"limit_plots/limits_spin0_bbbb_bbtt_bbyy_comb_"+version+"_conf_exp";
      }
    }
    else {
      if (statOnly) {
	strOutfile = PathOut+"limit_plots/limits_spin0_bbbb_bbtt_bbyy_comb_"+version+"_statOnly_exp";
      }
      else {
	strOutfile = PathOut+"limit_plots/limits_spin0_bbbb_bbtt_bbyy_pointExtension300_comb_"+version+"_exp";
      }
    }
  }
  else if (strModel.EqualTo("spin-2")) {
    if (strCoupling.EqualTo("c = 1.0")) {
      if (conf) {
	if (statOnly) {
	  strOutfile = PathOut+"limit_plots/limits_spin2_c10_bbbb_bbtt_comb_vfinal04_theoryPred_conf_statOnly_newCorr_exp";
	}
	else {
	  strOutfile = PathOut+"limit_plots/limits_spin2_c10_bbbb_bbtt_comb_vfinal04_theoryPred_conf_newCorr_exp";
	}
      }
      else {
	if (statOnly) {
	  strOutfile = PathOut+"limit_plots/limits_spin2_c10_bbbb_bbtt_bbWW_comb_vfinal04_theoryPred_paper_newStyle_statOnly_newCorr_exp";
	}
	else {
	  // strOutfile = PathOut+"limit_plots/limits_spin2_c10_bbbb_bbtt_bbWW_comb_vfinal04_theoryPred_paper_newStlye_newCorr_exp";
	  strOutfile = PathOut+"limit_plots/limits_spin2_c10_bbbb_bbtt_bbWW_comb_vfinal04_bbtautauInterpolation260-300_theoryPred_paper_newStlye_newCorr_260to360GeV_exp";
	}
      }
    }
    else if (strCoupling.EqualTo("c = 2.0")) {
      if (conf) {
	if (statOnly) {
	  strOutfile = PathOut+"limit_plots/limits_spin2_c20_bbbb_bbtt_comb_vfinal04_theoryPred_conf_statOnly_newCorr_exp";
	}
	else {
	  strOutfile = PathOut+"limit_plots/limits_spin2_c20_bbbb_bbtt_comb_vfinal04_theoryPred_conf_newCorr_exp";
	}
      }
      else {
	if (statOnly) {
	  strOutfile = PathOut+"limit_plots/limits_spin2_c20_bbbb_bbtt_bbWW_comb_vfinal04_theoryPred_paper_newStlye_newCorr_exp";
	}
	else {
	  strOutfile = PathOut+"limit_plots/limits_spin2_c20_bbbb_bbtt_bbWW_comb_vfinal04_theoryPred_paper_newStlye_newCorr_exp";
	}
      }
    }
  }
  else if (strModel.EqualTo("lambda")) {
    if (doExtrapolationTo140fb) {
      strOutfile = PathOut+"limit_plots/limits_lambda_140invfb_bbbb_bbtt_bbyy_comb_vfinal04_updatedScaling_4bJetNP1fix_newStlye_theory-NLO_newYscale_exp";
    }
    else if (doExtrapolationTo440fb) {
      strOutfile = PathOut+"limit_plots/limits_lambda_440invfb_bbbb_bbtt_bbyy_comb_vfinal04_updatedScaling_4bJetNP1fix_newStlye_theory-NLO_newYscale_exp";
    }
    else {
      if (conf) {
	if (statOnly) {
	  strOutfile = PathOut+"limit_plots/limits_lambda_bbbb_bbtt_bbyy_comb_vfinal04_conf_statOnly_theory-NLO_exp";
	}
	else {
	  strOutfile = PathOut+"limit_plots/limits_lambda_bbbb_bbtt_bbyy_comb_vfinal04_conf_theory-NLO_exp";  
	}
      }
      else {
	if (statOnly) {
	  strOutfile = PathOut+"limit_plots/limits_lambda_bbbb_bbtt_bbyy_comb_vfinal04_updatedScaling_newStlye_statOnly_theory-NLO_newYscale_exp";
	}
	else {
	  strOutfile = PathOut+"limit_plots/limits_lambda_bbbb_bbtt_bbyy_comb_vfinal04_updatedScaling_4bJetNP1fix_newStlye_theory-NLO_newYscale_exp";  
	}
      }
    }
  }

  if (drawObserved)
    strOutfile.Append("_obs");

  if (useNominalNPs)
    strOutfile.Append("_nomNP");
  else 
    strOutfile.Append("_profiledNP");
  
  if (npCorrInfo.length() != 0)
    strOutfile.Append("_"+npCorrInfo);

  if (extendTo3TeV)
    strOutfile.Append("_extendTo3TeV");
  
  if (extendTo3TeV && doLogScaleX)
    strOutfile.Append("_logScaleX");

  if (!doLogScale)
    strOutfile.Append("_linear");

  if (savePad1)
    strOutfile.Append("_limitsOnly");

  if (savePad2)
    strOutfile.Append("_legendOnly");

  //
  TDatime* datetime = new TDatime();
  int date = datetime->GetDate();
  date = date%1000000; //cut first two digits of the year away
  int time = datetime->GetTime();

  strOutfile.Append("_"+std::to_string(date)/*+"-"+std::to_string(time)*/);

  // HEPDATA
  if(doHepData){
    hepdatafilename = strOutfile+"-HEPDATA.root";
	std::cout << "Saving for HEPDATA inputs " << hepdatafile << std::endl;

    _tmpdir = gDirectory;
    hepdatafile = new TFile( hepdatafilename, "RECREATE" );
    _tmpdir->cd();
  }

  std::cout << "Making plot '" << strOutfile << "'" << std::endl;


  if (!useUserXRange && extendTo3TeV && doLogScaleX) {
    xmin = 260; //200.;
    xmax = 3000.;
  }

  double ymin, ymax;
  if (strModel.EqualTo("spin-0")) {
    if (extendTo3TeV) {
      ymin = 0.002;
      ymax = 50; //70.;
    }
    else {
      if (doLogScale) {
	if (conf) {
	  ymin = 0.001;
	  ymax = 1000.;
	}
	else {
	  ymin = 0.0003; //0.0001 //0.002
	  ymax = 30.; //50000.
	}
      }
      else {
	ymin = 0.0000002; //0.002
	ymax = 3.;
      }
    }
  }
  else if (strModel.EqualTo("spin-2")) {
    if (conf) {
      if (strCoupling.EqualTo("c = 1.0")) {
	ymin = 0.002;
	ymax = 100.;
      }
      else if (strCoupling.EqualTo("c = 2.0")) {
	if (statOnly) {
	  ymin = 0.003;
	  ymax = 100.;
	}
	else {
	  ymin = 0.001;
	  ymax = 400.;
	}
      }
    }
    else {
      if (strCoupling.EqualTo("c = 1.0")) {
	if (extendTo3TeV) {
	  ymin = 0.002; //0.001;  //0.0001
	  ymax = 50; //300.; //400.;
	}
	else {
	  ymin = 0.003;  //0.0001
	  ymax = 30.;  //3000.
	}
      }
      else if (strCoupling.EqualTo("c = 2.0")) {
	if (extendTo3TeV) {
	  ymin = 0.002;  //0.0001
	  ymax = 50; //300.; //400.;
	}
	else {
	  ymin = 0.003;  //0.0001
	  ymax = 30.;  //3000.
	}
      }
    }
  }
  else if (strModel.EqualTo("lambda")) {
    if (doLogScale) {
      if (statOnly) {
	ymin = 0.01;  //0.0001
	ymax = 4.;  //5000. //3000.
      }
      else {
	ymin = 0.01;  //0.0001
	ymax = 10.;  //5000. //3000.
      }
    }
    else {
      if (statOnly) {
	ymin = -1.; //0.;  //-3.;  //0.0001
	ymax = 3.; //3.5; //10.;  //5000. //3000.
      }
      else {
	ymin = -2.; //0.;  //-3.;  //0.0001
	ymax = 6.; //3.5; //10.;  //5000. //3000.
      }
    }
  }


  // std::string Path = "/eos/atlas/atlascerngroupdisk/phys-higgs/HSG6/HH/combination/workspaces/batches/2019_04_24_vfinal_04/";
  TString Path = "../../../output/"+version+"/";
  std::map<std::string, std::string> inFileNames;

  //spin-0
  if (strModel.EqualTo("spin-0")) {
    if (statOnly) {
      inFileNames["bbbb"] = Path+"limits/data-files/spin0_statOnly-bbbb.dat";
      inFileNames["bbtautau"] = Path+"limits/data-files/spin0_statOnly-bbtautau.dat";
      inFileNames["bbyy"] = Path+"limits/data-files/spin0_statOnly-bbyy.dat";
    }
    else {
      inFileNames["bbbb"] = Path+"limits/data-files/spin0-bbbb.dat";
      inFileNames["bbtautau"] = Path+"limits/data-files/spin0-bbtautau.dat";
      if (useLimitsFromPaper["bbyy"] == false)
	inFileNames["bbyy"] = Path+"limits/data-files/spin0-bbyy.dat";
      else
	inFileNames["bbyy"] = Path+"theory_inputs/limit_inputs.root";  
    }
    
    if (conf) {
      if (statOnly) {
	//inFileNames["comb_E_bbbb_bbtautau_bbyy"] = Path+"limits/data-files/spin0_statOnly-combined-E-bbbb_bbtautau_bbyy-fullcorr.dat";
	//inFileNames["comb_F_bbbb_bbtautau_bbyy"] = Path+"limits/data-files/spin0_statOnly-combined-F-bbbb_bbtautau_bbyy-fullcorr.dat";
      }
      else {
	//inFileNames["comb_E_bbbb_bbtautau_bbyy"] = Path+"limits/data-files/spin0-combined-E-bbbb_bbtautau_bbyy-fullcorr.dat";
	//inFileNames["comb_F_bbbb_bbtautau_bbyy"] = Path+"limits/data-files/spin0-combined-F-bbbb_bbtautau_bbyy-fullcorr.dat";
      }
    }
    else {
      inFileNames["comb_A_bbbb_bbtautau_bbyy"] = Path+"limits/data-files/spin0-combined-A-bbbb_bbtautau_bbyy-nocorr.dat";
      //inFileNames["comb_B_bbbb_bbtautau"] = Path+"limits/data-files/spin0-combined-A-bbbb_bbtautau-fullcorr.dat";
      //inFileNames["comb_C_bbbb"] = Path+"limits/data-files/spin0-combined-C-bbbb-nocorr.dat";
      //inFileNames["comb_D_bbtautau_bbyy"] = Path+"limits/data-files/spin0-combined-D-bbtautau_bbyy-nocorr.dat";
    }
    if (extendTo3TeV) {
      inFileNames["bbbb"] = Path+"limits/data-files/spin0-bbbb_allMassPoints.dat";
      inFileNames["comb_C_bbbb_bbtautau"] = Path+"limits/data-files/spin0-combined-D-bbbb_bbtautau-fullcorr.dat";
    }
  }
  
  // spin-2, c=1.0
  else if (strModel.EqualTo("spin-2") && strCoupling.EqualTo("c = 1.0")) {
    inFileNames["bbbb"] = Path+"limits/data-files/spin2_c_1.0-bbbb.dat";
    //inFileNames["bbtautau"] = Path+"limits/data-files/spin2_c_1.0-bbtautau.dat";
    inFileNames["bbtautau"] = Path+"limits/data-files/spin2_c_1.0_interpAvg-bbtautau.dat";
    if (extendTo3TeV) {
      inFileNames["bbbb"] = Path+"limits/data-files/spin2_c_1.0-bbbb_allMassPoints.dat";
    }
    if (!conf) {
      inFileNames["bbWW"] = Path+"limits/data-files/spin2_c_1.0-bbWW.dat";
      if (extendTo3TeV) {
	inFileNames["bbWW"] = Path+"limits/data-files/spin2_c_1.0-bbWW_allMassPoints.dat";
      }
    }
    
    if (conf) {
      if (statOnly) {
	inFileNames["bbbb"] = Path+"limits/data-files/spin2_c_1.0_statOnly-bbbb.dat";
	inFileNames["bbtautau"] = Path+"limits/data-files/spin2_c_1.0_statOnly-bbtautau.dat";
	inFileNames["comb_D_bbbb_bbtautau"] = Path+"limits/data-files/spin2_c_1.0_statOnly-combined-D-bbbb_bbtautau-fullcorr.dat";
	inFileNames["comb_E_bbbb_bbtautau"] = Path+"limits/data-files/spin2_c_1.0_statOnly-combined-E-bbbb_bbtautau-fullcorr.dat";
      }
      else {
	inFileNames["bbbb"] = Path+"limits/data-files/spin2_c_1.0-bbbb.dat";
	inFileNames["comb_D_bbbb_bbtautau"] = Path+"limits/data-files/spin2_c_1.0-combined-D-bbbb_bbtautau-fullcorr.dat";
	inFileNames["comb_E_bbbb_bbtautau"] = Path+"limits/data-files/spin2_c_1.0-combined-E-bbbb_bbtautau-fullcorr.dat";
      }
    }
    else {
      //inFileNames["comb_D_bbbb_bbtautau"] = Path+"limits/data-files/spin2_c_1.0-combined-D-bbbb_bbtautau-fullcorr.dat";
      inFileNames["comb_D_bbbb_bbtautau"] = Path+"limits/data-files/spin2_c_1.0_interpAvg-combined-D-bbbb_bbtautau-fullcorr.dat";
      inFileNames["comb_E_bbbb_bbtautau_bbWW"] = Path+"limits/data-files/spin2_c_1.0-combined-E-bbbb_bbtautau_bbWW-fullcorr.dat";
      if (extendTo3TeV) {
	inFileNames["comb_F_bbbb_bbWW"] = Path+"limits/data-files/spin2_c_1.0-combined-F-bbbb_bbWW-fullcorr.dat";
      }
    }
  }

  // spin-2, c=2.0
  else if (strModel.EqualTo("spin-2") && strCoupling.EqualTo("c = 2.0")) {
    inFileNames["bbbb"] = Path+"limits/data-files/spin2_c_2.0-bbbb.dat";
    inFileNames["bbtautau"] = Path+"limits/data-files/spin2_c_2.0-bbtautau.dat";
    if (extendTo3TeV) {
      inFileNames["bbbb"] = Path+"limits/data-files/spin2_c_2.0-bbbb_allMassPoints.dat";
    }
    if (!conf) {
      inFileNames["bbWW"] = Path+"limits/data-files/spin2_c_2.0-bbWW.dat";
      if (extendTo3TeV) {
	inFileNames["bbWW"] = Path+"limits/data-files/spin2_c_2.0-bbWW_allMassPoints.dat";
      }
    }
    
    if (conf) {
      if (statOnly) {
	inFileNames["bbbb"] = Path+"limits/data-files/spin2_c_2.0_statOnly-bbbb.dat";
	inFileNames["bbtautau"] = Path+"limits/data-files/spin2_c_2.0_statOnly-bbtautau.dat";
	inFileNames["comb_A_bbbb_bbtautau"] = Path+"limits/data-files/spin2_c_2.0_statOnly-combined-A-bbbb_bbtautau-fullcorr.dat";
	inFileNames["comb_B_bbbb_bbtautau"] = Path+"limits/data-files/spin2_c_2.0_statOnly-combined-B-bbbb_bbtautau-fullcorr.dat";
      }
      else {
	inFileNames["bbbb"] = Path+"limits/data-files/spin2_c_2.0-bbbb.dat";
	inFileNames["comb_A_bbbb_bbtautau"] = Path+"limits/data-files/spin2_c_2.0-combined-A-bbbb_bbtautau-fullcorr.dat";
	//inFileNames["comb_B_bbbb_bbtautau"] = Path+"limits/data-files/spin2_c_2.0-combined-B-bbbb_bbtautau-fullcorr.dat";
      }
    }
    else {
      inFileNames["comb_A_bbbb_bbtautau"] = Path+"limits/data-files/spin2_c_2.0-combined-A-bbbb_bbtautau-fullcorr.dat";
      inFileNames["comb_B_bbbb_bbtautau_bbWW"] = Path+"limits/data-files/spin2_c_2.0-combined-B-bbbb_bbtautau_bbWW-fullcorr.dat";
      if (extendTo3TeV) {
	inFileNames["comb_C_bbbb_bbWW"] = Path+"limits/data-files/spin2_c_2.0-combined-C-bbbb_bbWW-fullcorr.dat";
      }
    }
  }

  // lambda
  else if (strModel.EqualTo("lambda")) {
    if (doExtrapolationTo140fb) {
      inFileNames["bbtautau"] = Path+"limits/data-files/lambda_140invfb-bbtautau.dat";
      inFileNames["bbyy"] = Path+"limits/data-files/lambda_140invfb-bbyy.dat";
      inFileNames["comb_bbtautau_bbyy"] = Path+"limits/data-files/lambda_140invfb-combined-O-bbtautau_bbyy-fullcorr.dat";
    }
    else if (doExtrapolationTo440fb) {
      inFileNames["bbtautau"] = Path+"limits/data-files/lambda_440invfb-bbtautau.dat";
      inFileNames["bbyy"] = Path+"limits/data-files/lambda_440invfb-bbyy.dat";
      inFileNames["comb_bbtautau_bbyy"] = Path+"limits/data-files/lambda_440invfb-combined-O-bbtautau_bbyy-fullcorr.dat";
    }
    else {
      if (statOnly) {
	inFileNames["bbbb"] = Path+"limits/data-files/lambda_statOnly-bbbb.dat";
	inFileNames["bbtautau"] = Path+"limits/data-files/lambda_statOnly-bbtautau.dat";
	inFileNames["bbyy"] = Path+"limits/data-files/lambda_statOnly-bbyy.dat";
	inFileNames["comb_bbbb_bbtautau_bbyy"] = Path+"limits/data-files/lambda_statOnly-combined-F-bbbb_bbtautau_bbyy-fullcorr.dat";
	inFileNames["comb_bbbb_bbtautau_bbyy_fullSyst"] = Path+"limits/data-files/lambda-combined-F-bbbb_bbtautau_bbyy-fullcorr.dat";
      }
      else {
	inFileNames["bbbb"] = Path+"limits/data-files/lambda-bbbb.dat";
	inFileNames["bbtautau"] = Path+"limits/data-files/lambda-bbtautau.dat";
	if (useLimitsFromPaper["bbyy"] == false) {
	  inFileNames["bbyy"] = Path+"limits/data-files/lambda-bbyy.dat";
	}
	else {
	  inFileNames["bbyy"] = "./theory_inputs/limit_inputs.root";
	}
	// inFileNames["comb_bbbb_bbtautau_bbyy"] = Path+"limits/data-files/lambda-combined-F-bbbb_bbtautau_bbyy-fullcorr.dat";
	inFileNames["comb_bbbb_bbtautau_bbyy"] = Path+"limits/data-files/lambda-combined-F-bbbb_bbtautau_bbyy-fullcorr.dat";

	inFileNames["bbbb_statOnly"] = Path+"limits/data-files/lambda_statOnly-bbbb.dat";
	inFileNames["bbtautau_statOnly"] = Path+"limits/data-files/lambda_statOnly-bbtautau.dat";
	inFileNames["bbyy_statOnly"] = Path+"limits/data-files/lambda_statOnly-bbyy.dat";
	inFileNames["comb_bbbb_bbtautau_bbyy_statOnly"] = Path+"limits/data-files/lambda_statOnly-combined-F-bbbb_bbtautau_bbyy-fullcorr.dat";
      }
    }
  }
 
  std::map<std::string, std::tuple<int, const char*, bool> > coloursAndLegendNames;   
  // Arguments: 1: colour, 2: legend entry string, 3: create +-1/2 sigma bands

//  coloursAndLegendNames["bbbb"] = std::make_tuple(kMagenta+2, "b#bar{b}b#bar{b}", false);  //kRed
//  coloursAndLegendNames["bbtautau"] = std::make_tuple(kBlue-4, "b#bar{b}#tau^{+}#tau^{-}", false);  //kBlue
  coloursAndLegendNames["bbtautau"] = std::make_tuple(kMagenta+2, "b#bar{b}#tau^{+}#tau^{-}", false);  //kRed
  coloursAndLegendNames["bbbb"] = std::make_tuple(kBlue-4, "b#bar{b}b#bar{b}", false);  //kBlue
  coloursAndLegendNames["bbyy"] = std::make_tuple(kPink-2, "b#bar{b}#gamma#gamma", false);  //kOrange+4
  // coloursAndLegendNames["bbWW"] = std::make_tuple(kGreen+2, "b#bar{b}W^{+}W^{-}", false);  //kViolet-8
  // coloursAndLegendNames["WWyy"] = std::make_tuple(kCyan+1, "W^{+}W^{-}#gamma#gamma", false);  //kCyan+1
  // coloursAndLegendNames["WWWW"] = std::make_tuple(kOrange+5, "W^{+}W^{-}W^{+}W^{-}", false);  //kBlue-9
 
  //spin-0
  if (strModel.EqualTo("spin-0")) {
    coloursAndLegendNames["comb_A_bbbb_bbtautau_bbyy"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau+bb#gamma#gamma", true);
    //coloursAndLegendNames["comb_B_bbbb_bbtautau"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau", true);

    if (extendTo3TeV)
      coloursAndLegendNames["comb_D_bbbb_bbWW"] = std::make_tuple(kBlack, "bbbb+bbWW", true);
  }

  // spin-2
  if (strModel.EqualTo("spin-2")) {
    coloursAndLegendNames["comb_A_bbbb_bbtautau"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau", true);
    coloursAndLegendNames["comb_B_bbbb_bbtautau_bbWW"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau+bbWW", true);
    coloursAndLegendNames["comb_B_bbbb_bbtautau"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau", true);
    coloursAndLegendNames["comb_C_bbbb_bbWW"] = std::make_tuple(kBlack, "bbbb+bbWW", true);
    coloursAndLegendNames["comb_D_bbbb_bbtautau"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau", true);
    coloursAndLegendNames["comb_E_bbbb_bbtautau_bbWW"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau+bbWW", true);
    coloursAndLegendNames["comb_E_bbbb_bbtautau"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau", true);
    coloursAndLegendNames["comb_F_bbbb_bbWW"] = std::make_tuple(kBlack, "bbbb+bbWW", true);
  }

  // lambda
  if (strModel.EqualTo("lambda")) {
    if (doExtrapolationTo140fb || doExtrapolationTo440fb) {
      coloursAndLegendNames["comb_bbtautau_bbyy"] = std::make_tuple(kBlack, "bb#tau#tau+bb#gamma#gamma", true);
    }
    else {
      if (statOnly) {
	coloursAndLegendNames["bbbb_statOnly"] = std::make_tuple(kRed, "b#bar{b}b#bar{b}", false);
	coloursAndLegendNames["bbtautau_statOnly"] = std::make_tuple(kBlue, "b#bar{b}#tau^{+}#tau^{-}", false);
	coloursAndLegendNames["bbyy_statOnly"] = std::make_tuple(kSpring+4, "b#bar{b}#gamma#gamma", false);
	coloursAndLegendNames["comb_bbbb_bbtautau_bbyy"] = std::make_tuple(kBlack, "Comb.", true);
	coloursAndLegendNames["comb_bbbb_bbtautau_bbyy_fullSyst"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau+bb#gamma#gamma", false);
      }
      else {
	coloursAndLegendNames["comb_bbbb_bbtautau_bbyy"] = std::make_tuple(kBlack, "Comb.", true);
	coloursAndLegendNames["comb_bbbb_bbtautau_bbyy_fullSyst"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau+bb#gamma#gamma", true);
      }
    }
  }

  TString strXaxisTitle;
  TString strYaxisTitle;
  if (strModel.EqualTo("spin-0")) {
    strXaxisTitle = "m_{X} [GeV]";
    //strYaxisTitle = "95% CL upper limit on #sigma(pp #rightarrow S #rightarrow HH) [pb]";
    strYaxisTitle = "#sigma(pp #rightarrow X #rightarrow HH) [pb]";
  }
  else if (strModel.EqualTo("spin-2")) {
    strXaxisTitle = "m_{G_{KK}} [GeV]";
    //strYaxisTitle = "95% CL upper limit on #sigma(pp #rightarrow G_{KK} #rightarrow HH) [pb]";
    strYaxisTitle = "#sigma(pp #rightarrow G_{KK} #rightarrow HH) [pb]";
  }
  else if (strModel.EqualTo("lambda")) {
    //strXaxisTitle = "#kappa_{#lambda} = #lambda_{HHH} / #lambda_{SM}";
    strXaxisTitle = "#kappa_{#lambda}";
    //strYaxisTitle = "95% CL upper limit on #sigma_{ggF} (pp #rightarrow HH) [pb]";
    strYaxisTitle = "#sigma_{ggF} (pp #rightarrow HH) [pb]";
  }

  // Theory curve for lambda (NLO)
  TFile* file_lambda_NLO = nullptr;
  if (doExtend) {
    GenerateTGraphAsymmErrors(); 
    file_lambda_NLO =  new TFile("extend_lambda_limits_plot.root","READ");
  }
  else file_lambda_NLO = new TFile("./theory_inputs/limit_inputs.root", "READ");
  
  if (!file_lambda_NLO->IsOpen()) {
    std::cerr << "ERROR : Lambda NLO prediction input file could not be opened!" << std::endl;
  }


  TGraphAsymmErrors* gr_lambda_NLO = (TGraphAsymmErrors*) file_lambda_NLO->Get("nonres_lambda_theory_band");

  if (!doExtend)
    PrintTGraphAsymmErrors(gr_lambda_NLO, debug);

  int npoints_lambda_NLO = gr_lambda_NLO->GetN();
  double* lambda_NLO_x = gr_lambda_NLO->GetX();
  double* lambda_NLO_y = gr_lambda_NLO->GetY();

  // central theory values
  TGraph* gr_lambda_NLO_line = new TGraph(npoints_lambda_NLO, lambda_NLO_x, lambda_NLO_y);

  // rescaling lambda theory curve to updated SM xsec of 33.49 fb
  double scale = (33.49/(gr_lambda_NLO_line->Eval(1.0, 0, "S")*1000.));

  for (int k=0; k<npoints_lambda_NLO; k++) {
    gr_lambda_NLO_line->GetY()[k] *= scale;
    gr_lambda_NLO->GetY()[k] *= scale;
    gr_lambda_NLO->GetEYhigh()[k] =  gr_lambda_NLO->GetY()[k]*0.0729*scale;
    gr_lambda_NLO->GetEYlow()[k] =  gr_lambda_NLO->GetY()[k]*0.0841*scale;
  }

  // this is already after the abovescaling
  // theory up dn asked by Andreas before publishing
  double* lambda_NLO_y_high = gr_lambda_NLO->GetEYhigh ();
  double* lambda_NLO_y_low  = gr_lambda_NLO->GetEYlow ();
  TGraph* gr_lambda_NLO_line_yhigh = new TGraph(npoints_lambda_NLO, lambda_NLO_x, lambda_NLO_y_high);
  TGraph* gr_lambda_NLO_line_ylow  = new TGraph(npoints_lambda_NLO, lambda_NLO_x, lambda_NLO_y_low);
  for (int k=0; k<npoints_lambda_NLO; k++) {
    gr_lambda_NLO_line_yhigh->GetY()[k] = gr_lambda_NLO_line->GetY()[k] + gr_lambda_NLO_line_yhigh->GetY()[k];
	gr_lambda_NLO_line_ylow->GetY()[k]  = gr_lambda_NLO_line->GetY()[k] - gr_lambda_NLO_line_ylow->GetY()[k];
  }
  // test
  std::cout << "DDDDDDD" << endl;
  std::cout << gr_lambda_NLO_line->GetY()[20] << std::endl;
  std::cout << gr_lambda_NLO_line_yhigh->GetY()[20] << std::endl;
  std::cout << gr_lambda_NLO_line_ylow->GetY()[20] << std::endl;
  std::cout << "DDDDDDD" << endl;

  // Theory curve for spin-0
  std::map<double, double> map_theory_xsec_spin0 = ReadTheoryXsec("./theory_inputs/mH_vs_xs_ggFH_br_Htohh_hMSSM_tanb2_260to1000GeV.txt", 1.);

  double* theory_points_spin0 = new double[map_theory_xsec_spin0.size()];
  double* theory_xsec_spin0 = new double[map_theory_xsec_spin0.size()];

  int k=0;
  for (std::map<double, double>::iterator iterXsecSpin0 = map_theory_xsec_spin0.begin(); iterXsecSpin0 != map_theory_xsec_spin0.end(); ++iterXsecSpin0) {
    if (debug) 
      std::cout << "spin-0 prediction: mass = " << iterXsecSpin0->first << ",   xsec = " << iterXsecSpin0->second << std::endl;
    theory_points_spin0[k] = (double)iterXsecSpin0->first;
    theory_xsec_spin0[k] = iterXsecSpin0->second;
    k++;
  }

  TGraph* gr_theory_xsec_spin0 = new TGraph(map_theory_xsec_spin0.size(), theory_points_spin0, theory_xsec_spin0);


  // Theory curve for spin-2, c=1.0
  std::map<double, double> map_theory_xsec_spin2c10;
    if (extendTo3TeV)
      map_theory_xsec_spin2c10 = ReadTheoryXsec("./theory_inputs/xsecBR_c1_260to1800GeV.txt", 1.);
    else
      map_theory_xsec_spin2c10 = ReadTheoryXsec("./theory_inputs/xsecBR_c1_260to1000GeV.txt", 1.);

  double* theory_points_spin2c10 = new double[map_theory_xsec_spin2c10.size()];
  double* theory_xsec_spin2c10 = new double[map_theory_xsec_spin2c10.size()];

  k=0;
  for (std::map<double, double>::iterator iterXsecSpin2c10 = map_theory_xsec_spin2c10.begin(); iterXsecSpin2c10 != map_theory_xsec_spin2c10.end(); ++iterXsecSpin2c10) {
    if (debug) 
      std::cout << "spin-2 (c=1.0) prediction: mass = " << iterXsecSpin2c10->first << ",   xsec = " << iterXsecSpin2c10->second << std::endl;
    theory_points_spin2c10[k] = (double)iterXsecSpin2c10->first;
    theory_xsec_spin2c10[k] = iterXsecSpin2c10->second / 1000.;
    k++;
  }

  TGraph* gr_theory_xsec_spin2c10 = new TGraph(map_theory_xsec_spin2c10.size(), theory_points_spin2c10, theory_xsec_spin2c10);


  // Theory curve for spin-2, c=2.0
  std::map<double, double> map_theory_xsec_spin2c20;
  if (extendTo3TeV)
    map_theory_xsec_spin2c20 = ReadTheoryXsec("./theory_inputs/xsecBR_c2_260to2000GeV.txt", 1.);
  else
    map_theory_xsec_spin2c20 = ReadTheoryXsec("./theory_inputs/xsecBR_c2_260to1000GeV.txt", 1.);

  double* theory_points_spin2c20 = new double[map_theory_xsec_spin2c20.size()];
  double* theory_xsec_spin2c20 = new double[map_theory_xsec_spin2c20.size()];

  k=0;
  for (std::map<double, double>::iterator iterXsecSpin2c20 = map_theory_xsec_spin2c20.begin(); iterXsecSpin2c20 != map_theory_xsec_spin2c20.end(); ++iterXsecSpin2c20) {
    if (debug) 
      std::cout << "spin-2 (c=2.0) prediction: mass = " << iterXsecSpin2c20->first << ",   xsec = " << iterXsecSpin2c20->second << std::endl;
    theory_points_spin2c20[k] = (double)iterXsecSpin2c20->first;
    theory_xsec_spin2c20[k] = iterXsecSpin2c20->second / 1000.;
    k++;
  }

  TGraph* gr_theory_xsec_spin2c20 = new TGraph(map_theory_xsec_spin2c20.size(), theory_points_spin2c20, theory_xsec_spin2c20);



  std::map<std::string, std::map<int, std::tuple<double, double, double, double, double, double> > > massesAndLimits;
  for (std::map<std::string, std::string>::iterator it = inFileNames.begin(); it != inFileNames.end(); ++it) {
    if ((it->first) == "bbyy" && useLimitsFromPaper[it->first] == true)
      massesAndLimits[it->first] = ReadInputFile_bbyyLimitsFromPaper(it->second, strModel, debug);
    else if ((it->first).find("comb") == std::string::npos && useLimitsFromPaper[it->first] == true)
      massesAndLimits[it->first] = ReadInputFile_LimitsFromPaper(it->second, debug);
    else
      massesAndLimits[it->first] = ReadInputFile(it->second, useNominalNPs, isNanCompatible );
  }
  
  std::map<std::string,double*> masses;
  std::map<std::string,double*> err_masses;
  std::map<std::string,double*> xsec_m2s;
  std::map<std::string,double*> xsec_m1s;
  std::map<std::string,double*> xsec_exp;
  std::map<std::string,double*> xsec_p1s;
  std::map<std::string,double*> xsec_p2s;
  std::map<std::string,double*> xsec_obs;

 
  TCanvas* c1 = 0;
  if( strModel.EqualTo("lambda") ){
    c1 = new TCanvas("c1", "hh limits", 800/0.76, 700);
  }else{
    //c1 = new TCanvas("c1", "hh limits", 600, 500);
    c1 = new TCanvas("c1", "hh limits", 800/0.76, 700);
  }
  c1->cd();
  // if (doLogScale)
  //   c1->SetLogy();
  // c1->SetTickx();
  // c1->SetTicky();
  gPad->SetRightMargin(0.05);
  gPad->SetTopMargin(0.05);

  std::cout << "Before creation of pad1" << std::endl;
  TPad* pad1 = new TPad("pad1", "pad1", 0., 0., 0.76, 1.);
  pad1->Draw();
  pad1->cd();
  if (doLogScale)
    pad1->SetLogy();
  if (doLogScaleX)
    pad1->SetLogx();
  pad1->SetTicky();
  pad1->SetTicky();

  std::cout << "After switching cd to pad1" << std::endl;
  
  std::map<std::string, TGraph*> limitPlots_exp;
  std::map<std::string, TGraph*> limitPlots_obs;
  TGraphAsymmErrors* limit_plot_1s;
  TGraphAsymmErrors* limit_plot_2s;

  TMultiGraph* mg = new TMultiGraph();
  mg->SetName("limits");

  for (std::map<std::string, std::map<int, std::tuple<double, double, double, double, double, double> > >::iterator iter = massesAndLimits.begin(); iter != massesAndLimits.end(); ++iter) {  

    std::cout << "Storing values in arrays for channel " << iter->first << std::endl;
    
    int npoints = (iter->second).size();
    
    masses[iter->first] = new double[npoints];
    err_masses[iter->first] = new double[npoints];
    xsec_m2s[iter->first] = new double[npoints];
    xsec_m1s[iter->first] = new double[npoints];
    xsec_exp[iter->first] = new double[npoints];
    xsec_p1s[iter->first] = new double[npoints];
    xsec_p2s[iter->first] = new double[npoints];
    xsec_obs[iter->first] = new double[npoints];
    
    int i = 0;
    for (auto& mapLimits: iter->second) {
      masses[iter->first][i] = (double) (mapLimits.first);
      err_masses[iter->first][i] = 0.;
      xsec_m2s[iter->first][i] = std::get<0>(mapLimits.second);
      xsec_m1s[iter->first][i] = std::get<1>(mapLimits.second);
      xsec_exp[iter->first][i] = std::get<2>(mapLimits.second);
      xsec_p1s[iter->first][i] = std::get<3>(mapLimits.second);
      xsec_p2s[iter->first][i] = std::get<4>(mapLimits.second);
      xsec_obs[iter->first][i] = std::get<5>(mapLimits.second);

      if (printLimits[iter->first] == true || ((iter->first).find("comb") != std::string::npos && printLimits["comb"] == true)) {
	std::cout << "Mass = " << masses[iter->first][i] << std::endl;
	std::cout << "-2 sigma = " << xsec_m2s[iter->first][i] << std::endl;
	std::cout << "-1 sigma = " << xsec_m1s[iter->first][i] << std::endl;
	std::cout << "+1 sigma = " << xsec_p1s[iter->first][i] << std::endl;
	std::cout << "+2 sigma = " << xsec_p2s[iter->first][i] << std::endl;
	std::cout << "exp = " << xsec_exp[iter->first][i] << std::endl;
	std::cout << "obs = " << xsec_obs[iter->first][i] << std::endl;
      }

      i++;
    } 

    if (std::get<2>(coloursAndLegendNames[iter->first]) == true) {
      limit_plot_1s = new TGraphAsymmErrors(npoints, masses[iter->first], xsec_exp[iter->first], err_masses[iter->first], err_masses[iter->first], xsec_m1s[iter->first], xsec_p1s[iter->first]);
      limit_plot_2s = new TGraphAsymmErrors(npoints, masses[iter->first], xsec_exp[iter->first], err_masses[iter->first], err_masses[iter->first], xsec_m2s[iter->first], xsec_p2s[iter->first]);

	  limit_plot_1s->SetName((iter->first+"_1s").c_str() );
	  limit_plot_2s->SetName((iter->first+"_2s").c_str() );
 
      if (doExtend) { 
        limit_plot_2s = ExtendTGraphAsymmErrorsByTSpline(limit_plot_2s);     
        limit_plot_1s = ExtendTGraphAsymmErrorsByTSpline(limit_plot_1s);     
      }

      limit_plot_2s->SetLineColor(kYellow);
      limit_plot_2s->SetFillColor(kYellow);
      
      limit_plot_1s->SetLineColor(kGreen);
      limit_plot_1s->SetFillColor(kGreen);

      mg->Add(limit_plot_2s);
      mg->Add(limit_plot_1s);
    }

    limitPlots_exp[iter->first] = new TGraph(npoints, masses[iter->first], xsec_exp[iter->first]);
    limitPlots_obs[iter->first] = new TGraph(npoints, masses[iter->first], xsec_obs[iter->first]);
	limitPlots_exp[iter->first]->SetName( (iter->first+"_exp").c_str() );
	limitPlots_obs[iter->first]->SetName( (iter->first+"_obs").c_str() );

    if (doExtend) {
      limitPlots_exp[iter->first] = ExtendTGraphByTSpline(limitPlots_exp[iter->first]);
      limitPlots_obs[iter->first] = ExtendTGraphByTSpline(limitPlots_obs[iter->first]);
      cout<<endl<<"Channel: "<<iter->first<<endl; 
      
      if ((iter->first).find("bbtautau")!=string::npos&&(iter->first).find("comb")==string::npos) PrintTGraph(limitPlots_obs[iter->first], debug);
      //if (((iter->first).find("comb"))) PrintTGraph(limitPlots_obs[iter->first]);
    }

    if ((iter->first).find("statOnly") == std::string::npos)
      mg->Add(limitPlots_exp[iter->first]);

    if (!statOnly) {
      if (drawObserved && (iter->first).find("statOnly") == std::string::npos) {
	mg->Add(limitPlots_obs[iter->first]);
      }
    }
  }

  if (strModel.EqualTo("lambda")) {
    gr_lambda_NLO->SetLineColor(kOrange+7);  //kViolet-3
    gr_lambda_NLO->SetLineWidth(2);
    gr_lambda_NLO->SetFillColorAlpha(kOrange+7, 0.4);  //kViolet-3
    //gr_lambda_NLO->SetFillStyle(4050);
    mg->Add(gr_lambda_NLO);
    
    //mg->Add(gr_lambda_NLO_line);
    //gr_lambda_NLO_line->SetLineColor(kViolet-3);
    //gr_lambda_NLO_line->SetLineWidth(2);
    //gr_lambda_NLO_line->Draw("c same");
  }

  mg->Draw("a3 l");
  pad1->RedrawAxis();
  pad1->Update();
  pad1->Modified();
  
  mg->GetHistogram()->GetXaxis()->SetMoreLogLabels();
  // mg->GetHistogram()->GetXaxis()->ChangeLabel(120, -1, -1, -1, -1, -1, "3#times10^{3}");
  mg->GetHistogram()->GetXaxis()->SetTitleOffset(1.4);
  mg->GetHistogram()->GetYaxis()->SetTitleOffset(1.6);
  mg->GetHistogram()->GetXaxis()->SetTitleSize(0.045);  // 0.05
  mg->GetHistogram()->GetYaxis()->SetTitleSize(0.045);  // 0.05
  mg->GetHistogram()->GetXaxis()->SetTitle((const char*) strXaxisTitle);
  mg->GetHistogram()->GetYaxis()->SetTitle((const char*) strYaxisTitle);
  //  mg->GetHistogram()->GetXaxis()->SetLimits(-21,21);
  mg->GetHistogram()->GetYaxis()->SetRangeUser(ymin, ymax);
  if (useUserXRange || (extendTo3TeV && doLogScaleX))
  mg->GetHistogram()->GetXaxis()->SetRangeUser(xmin, xmax);
 
  gPad->RedrawAxis();

  if( doHepData ){
    std::cout << "HEPDATA : mg" << std::endl;
	_tmpdir = gDirectory;
	hepdatafile->cd();
	mg->Write();
	_tmpdir->cd();
  }

  //TLine * L0 = new TLine(-22,0,22,0);
  //L0->SetLineStyle(8);
  //  L0->Draw("same");
  


  //__________________________________________________________________
  int i=1;
  // expected limit plots
  for (std::map<std::string, TGraph*>::iterator iter_limitPlots = limitPlots_exp.begin(); iter_limitPlots != limitPlots_exp.end(); ++ iter_limitPlots) {
    
    if ((iter_limitPlots->first).find("statOnly") != std::string::npos)
      continue;
    if ((strModel.EqualTo("lambda")) && (statOnly) && (iter_limitPlots->first == "comb_bbbb_bbtautau_bbyy_fullSyst")) {
      iter_limitPlots->second->SetLineStyle(1);
      iter_limitPlots->second->SetLineWidth(2);
      iter_limitPlots->second->SetMarkerStyle(2); // set to 2 for points (pluses)   
      iter_limitPlots->second->SetLineColor(std::get<0>(coloursAndLegendNames[iter_limitPlots->first]));
      iter_limitPlots->second->SetMarkerColor(std::get<0>(coloursAndLegendNames[iter_limitPlots->first]));
    }
    else{
      iter_limitPlots->second->SetLineStyle(7);
      iter_limitPlots->second->SetLineWidth(2);
	  if( strModel.Contains("spin") ) iter_limitPlots->second->SetLineWidth(3); // only for resonant
      iter_limitPlots->second->SetMarkerStyle(2); // set to 2 for points (pluses)   
      iter_limitPlots->second->SetLineColor(std::get<0>(coloursAndLegendNames[iter_limitPlots->first]));
      iter_limitPlots->second->SetMarkerColor(std::get<0>(coloursAndLegendNames[iter_limitPlots->first]));
    }
    
    if (i==1) {
      std::cout << "Drawing exp " << iter_limitPlots->first << std::endl;
      iter_limitPlots->second->Draw("l");
    }
    else {
      std::cout << "Drawing exp " << iter_limitPlots->first << std::endl;
      iter_limitPlots->second->Draw("l same");
    }

    i++;
  }
  
  // observed limit plots
  if (!statOnly) {
    if (drawObserved) {
      for (std::map<std::string, TGraph*>::iterator iter_limitPlots_obs = limitPlots_obs.begin(); iter_limitPlots_obs != limitPlots_obs.end(); ++ iter_limitPlots_obs) {
	
	iter_limitPlots_obs->second->SetLineStyle(1);
	iter_limitPlots_obs->second->SetLineWidth(2);
	if( strModel.Contains("spin") ) iter_limitPlots_obs->second->SetLineWidth(3); // only for resonant
	iter_limitPlots_obs->second->SetMarkerStyle(20); // set to 2 for points (pluses)  
	iter_limitPlots_obs->second->SetMarkerSize(0.8*iter_limitPlots_obs->second->GetMarkerSize());
	iter_limitPlots_obs->second->SetLineColor(std::get<0>(coloursAndLegendNames[iter_limitPlots_obs->first]));
	iter_limitPlots_obs->second->SetMarkerColor(std::get<0>(coloursAndLegendNames[iter_limitPlots_obs->first]));
	
	if ((iter_limitPlots_obs->first).find("statOnly") != std::string::npos)
	  continue;
	else if ((iter_limitPlots_obs->first).find("comb") != std::string::npos) {
	  std::cout << "Drawing obs " << iter_limitPlots_obs->first << std::endl;
	  iter_limitPlots_obs->second->Draw("lp same");
	}
	else {
	  std::cout << "Drawing obs " << iter_limitPlots_obs->first << std::endl;
	  iter_limitPlots_obs->second->Draw("l same");  // add option "p" for points on data
	}
      }
    }
  }
  


  gr_theory_xsec_spin0->SetLineColor(kOrange+7);  //kViolet
  gr_theory_xsec_spin0->SetLineWidth(2);
  gr_theory_xsec_spin2c10->SetLineColor(kOrange+7);  //kViolet
  gr_theory_xsec_spin2c10->SetLineWidth(2);
  gr_theory_xsec_spin2c20->SetLineColor(kOrange+7);  //kViolet
  gr_theory_xsec_spin2c20->SetLineWidth(2);
  
  if (strModel.EqualTo("spin-0")) {
    //gr_theory_xsec_spin0->Draw("c same");
  }
  if (strModel.EqualTo("spin-2") && strCoupling.EqualTo("c = 1.0")) {
    gr_theory_xsec_spin2c10->Draw("c same");
  }
  if (strModel.EqualTo("spin-2") && strCoupling.EqualTo("c = 2.0")) {
    gr_theory_xsec_spin2c20->Draw("c same");
  }
  //________________________________________________________________________
    
    

  //________________________________________________________________________
  // calculate lambda exclusion (crossing points between lambda limits and theory prediction)
  map<TString,TGraph*> gr_limits_exp;
  map<TString,TGraph*> gr_limits_obs;
  map<TString,TGraph*> gr_limits_exp_stat;
  // only for statsonly col to add to fullsyst plot
  
  vector<TString> channel;

  for (std::map<std::string, TGraph*>::iterator iter_limitPlots_exp = limitPlots_exp.begin(); iter_limitPlots_exp != limitPlots_exp.end(); ++ iter_limitPlots_exp) {
    if (statOnly) {
      if (strModel.EqualTo("lambda")) {
	if ((iter_limitPlots_exp->first).find("fullSyst") == std::string::npos) {
	  gr_limits_exp[iter_limitPlots_exp->first] = iter_limitPlots_exp->second;
	  channel.push_back(iter_limitPlots_exp->first);
	}
      }
    }
    else {
      if (strModel.EqualTo("lambda")) {
      	if ((iter_limitPlots_exp->first).find("statOnly") != std::string::npos) {
      	  gr_limits_exp_stat[iter_limitPlots_exp->first] = iter_limitPlots_exp->second;
      	}
	else {
	  gr_limits_exp[iter_limitPlots_exp->first] = iter_limitPlots_exp->second;
      	  channel.push_back(iter_limitPlots_exp->first);
	}
      }
      else {
	gr_limits_exp[iter_limitPlots_exp->first] = iter_limitPlots_exp->second;
	channel.push_back(iter_limitPlots_exp->first);
      }
    }
  }
  
  for (std::map<std::string, TGraph*>::iterator iter_limitPlots_obs = limitPlots_obs.begin(); iter_limitPlots_obs != limitPlots_obs.end(); ++ iter_limitPlots_obs) {
    if (statOnly) {
      if (strModel.EqualTo("lambda")) {
	if ((iter_limitPlots_obs->first).find("fullSyst") == std::string::npos  && (iter_limitPlots_obs->first).find("fullSyst") == std::string::npos) {
	  gr_limits_obs[iter_limitPlots_obs->first] = iter_limitPlots_obs->second;
	}
      }
    }
    else {
	gr_limits_obs[iter_limitPlots_obs->first] = iter_limitPlots_obs->second;
    }
  }
  
  //channel.push_back("comb_C_bbbb_bbWW");

  std::vector<double> exclusionExpLow;
  std::vector<double> exclusionExpHigh;
  std::vector<double> exclusionObsLow;
  std::vector<double> exclusionObsHigh;
  // only for the statsonly col to add to fullsyst plots
  std::vector<double> exclusionExpLow_stat;
  std::vector<double> exclusionExpHigh_stat;
  
  map<TString, TGraph*> theory_curve;
  theory_curve["spin-0"] = gr_theory_xsec_spin0;
  theory_curve["spin-2-c1"] = gr_theory_xsec_spin2c10;
  theory_curve["spin-2-c2"] = gr_theory_xsec_spin2c20;
  theory_curve["lambda"] = gr_lambda_NLO_line; // gr_lambda_NLO_line_ylow; // gr_lambda_NLO_line_yhigh; // gr_lambda_NLO_line;

  TString modelStr("");

  if (strModel.EqualTo("spin-2")) {
    if  (strCoupling.EqualTo("c = 2.0")) modelStr = "spin-2-c2";
    else if (strCoupling.EqualTo("c = 1.0")) modelStr = "spin-2-c1";
  }
  else modelStr = strModel;

  map<TString, double> ExpLowLeft;
  map<TString, double> ExpLowRight;
  map<TString, double> ObsLowLeft;
  map<TString, double> ObsLowRight;
  map<TString, double> ExpHighLeft;
  map<TString, double> ExpHighRight;
  map<TString, double> ObsHighLeft;
  map<TString, double> ObsHighRight;


  if (strModel.EqualTo("lambda")) {
    if (doExtrapolationTo140fb || doExtrapolationTo440fb) {

      ExpLowLeft["bbbb"] = -15.0;
      ExpLowLeft["bbtautau"] = -10.0;
      ExpLowLeft["bbyy"] = -10.0;
      ExpLowLeft["comb_bbtautau_bbyy"] = -8.0;
      
      ExpLowRight["bbbb"] = -5.0;//-3.0;  //-10.0;
      ExpLowRight["bbtautau"] = -5.0;//-3.0; //-5.0;
      ExpLowRight["bbyy"] = -5.0;//-3.0; //-5.0;
      ExpLowRight["comb_bbtautau_bbyy"] = -3.0;
      
      ObsLowLeft["bbbb"] = -15.0;
      ObsLowLeft["bbtautau"] = -10.0;
      ObsLowLeft["bbyy"] = -10.0;
      ObsLowLeft["comb_bbtautau_bbyy"] = -8.0;
      
      ObsLowRight["bbbb"] = -5.0;
      ObsLowRight["bbtautau"] = -5.0;
      ObsLowRight["bbyy"] = -5.0;
      ObsLowRight["comb_bbtautau_bbyy"] = -3.0;
      
      ExpHighLeft["bbbb"] = 10.0;//10.0; //15.0;
      ExpHighLeft["bbtautau"] = 10.0;//10.0; //14.0;
      ExpHighLeft["bbyy"] = 10.0;//10.0;
      ExpHighLeft["comb_bbtautau_bbyy"] = 10.0;//10.0;
      
      ExpHighRight["bbbb"] = 20.;
      ExpHighRight["bbtautau"] = 20.0; //18.0;
      ExpHighRight["bbyy"] = 20.0; //15.0;
      ExpHighRight["comb_bbtautau_bbyy"] = 20.0; //15.0;
      
      ObsHighLeft["bbbb"] = 10.0;//10.0;
      ObsHighLeft["bbtautau"] = 10.0; //10.0;//14.0;
      ObsHighLeft["bbyy"] = 10.0; //10.0;
      ObsHighLeft["comb_bbtautau_bbyy"] = 10.0;//10.0;
      
      if (doExtend)
	ObsHighRight["bbbb"] = 22.0;
      else 
	ObsHighRight["bbbb"] = 20.0;
      ObsHighRight["bbtautau"] = 20.0;//18.0;
      ObsHighRight["bbyy"] = 20.0;//15.0;
      ObsHighRight["comb_bbtautau_bbyy"] = 20.0;//15.0;

    }
    else {

      ExpLowLeft["bbbb"] = -15.0;
      ExpLowLeft["bbtautau"] = -10.0;
      ExpLowLeft["bbyy"] = -10.0;
      ExpLowLeft["comb_bbbb_bbtautau_bbyy"] = -8.0;
      
      ExpLowRight["bbbb"] = -5.0;//-3.0;  //-10.0;
      ExpLowRight["bbtautau"] = -5.0;//-3.0; //-5.0;
      ExpLowRight["bbyy"] = -5.0;//-3.0; //-5.0;
      ExpLowRight["comb_bbbb_bbtautau_bbyy"] = -3.0;
      
      ObsLowLeft["bbbb"] = -15.0;
      ObsLowLeft["bbtautau"] = -10.0;
      ObsLowLeft["bbyy"] = -10.0;
      ObsLowLeft["comb_bbbb_bbtautau_bbyy"] = -8.0;
      
      ObsLowRight["bbbb"] = -5.0;
      ObsLowRight["bbtautau"] = -5.0;
      ObsLowRight["bbyy"] = -5.0;
      ObsLowRight["comb_bbbb_bbtautau_bbyy"] = -3.0;
      
      ExpHighLeft["bbbb"] = 10.0;//10.0; //15.0;
      ExpHighLeft["bbtautau"] = 10.0;//10.0; //14.0;
      ExpHighLeft["bbyy"] = 10.0;//10.0;
      ExpHighLeft["comb_bbbb_bbtautau_bbyy"] = 10.0;//10.0;
      
      ExpHighRight["bbbb"] = 20.;
      ExpHighRight["bbtautau"] = 20.0; //18.0;
      ExpHighRight["bbyy"] = 20.0; //15.0;
      ExpHighRight["comb_bbbb_bbtautau_bbyy"] = 20.0; //15.0;
      
      ObsHighLeft["bbbb"] = 10.0;//10.0;
      ObsHighLeft["bbtautau"] = 10.0; //10.0;//14.0;
      ObsHighLeft["bbyy"] = 10.0; //10.0;
      ObsHighLeft["comb_bbbb_bbtautau_bbyy"] = 10.0;//10.0;
      
      if (doExtend)
	ObsHighRight["bbbb"] = 22.0;
      else 
	ObsHighRight["bbbb"] = 20.0;
      ObsHighRight["bbtautau"] = 20.0;//18.0;
      ObsHighRight["bbyy"] = 20.0;//15.0;
      ObsHighRight["comb_bbbb_bbtautau_bbyy"] = 20.0;//15.0;

    }  
  }

  else if (strModel.EqualTo("spin-2")) {

    ExpLowLeft["bbbb"] = 260;
    ExpLowLeft["bbtautau"] = 260;
    ExpLowLeft["bbWW"] = 260;
    ExpLowLeft["comb_F_bbbb_bbWW"] = 260;
    ExpLowLeft["comb_E_bbbb_bbtautau_bbWW"] = 2000;
    ExpLowLeft["comb_D_bbbb_bbtautau"] = 2000;

    ExpLowRight["bbbb"] = 400;
    ExpLowRight["bbtautau"] = 400;
    ExpLowRight["bbWW"] = 400;
    ExpLowRight["comb_F_bbbb_bbWW"] = 400;
    ExpLowRight["comb_E_bbbb_bbtautau_bbWW"] = 2000;
    ExpLowRight["comb_D_bbbb_bbtautau"] = 2000;
    
    ObsLowLeft["bbbb"] = 260;
    ObsLowLeft["bbtautau"] = 260;
    ObsLowLeft["bbWW"] = 260;
    ObsLowLeft["comb_F_bbbb_bbWW"] = 260;
    ObsLowLeft["comb_E_bbbb_bbtautau_bbWW"] = 2000;
    ObsLowLeft["comb_D_bbbb_bbtautau"] = 2000;
    
    ObsLowRight["bbbb"] = 400;
    ObsLowRight["bbtautau"] = 400;
    ObsLowRight["bbWW"] = 400;
    ObsLowRight["comb_F_bbbb_bbWW"] = 400;
    ObsLowRight["comb_E_bbbb_bbtautau_bbWW"] = 2000;
    ObsLowRight["comb_D_bbbb_bbtautau"] = 2000;
    
    ExpHighLeft["bbbb"] = 1000;
    ExpHighLeft["bbtautau"] = 800;
    ExpHighLeft["bbWW"] = 800;
    ExpHighLeft["comb_F_bbbb_bbWW"] = 1000;
    ExpHighLeft["comb_E_bbbb_bbtautau_bbWW"] = 2000;
    ExpHighLeft["comb_D_bbbb_bbtautau"] = 2000;
    
    ExpHighRight["bbbb"] = 2000;
    ExpHighRight["bbtautau"] = 1000;
    ExpHighRight["bbWW"] = 1000;
    ExpHighRight["comb_F_bbbb_bbWW"] = 2000;
    ExpHighRight["comb_E_bbbb_bbtautau_bbWW"] = 2000;
    ExpHighRight["comb_D_bbbb_bbtautau"] = 2000;
    
    ObsHighLeft["bbbb"] = 1000;
    ObsHighLeft["bbtautau"] = 800;
    ObsHighLeft["bbWW"] = 800;
    ObsHighLeft["comb_F_bbbb_bbWW"] = 1000;
    ObsHighLeft["comb_E_bbbb_bbtautau_bbWW"] = 2000;
    ObsHighLeft["comb_D_bbbb_bbtautau"] = 2000;
    
    ObsHighRight["bbbb"] = 2000;
    ObsHighRight["bbtautau"] = 1000;
    ObsHighRight["bbWW"] = 1000;
    ObsHighRight["comb_F_bbbb_bbWW"] = 2000;
    ObsHighRight["comb_E_bbbb_bbtautau_bbWW"] = 2000;
    ObsHighRight["comb_D_bbbb_bbtautau"] = 2000;
    
  }


  if (calculateExclusions) {

    int numberChannelExclusions = 4;
    if (strModel.EqualTo("spin-2")) {
      numberChannelExclusions = 6;
    }


    double ybase = 0.35;
    double textsize = 0.04;
    double downstep = 0.09;
    
    // draw exclusions in lambda plot
    if (strModel.EqualTo("lambda")) {
      TLatex textExcl;
      textExcl.SetNDC();
      textExcl.SetTextSize(textsize);
      textExcl.SetTextFont(42);
      if (statOnly)
	textExcl.DrawLatex(0.19, ybase-0.03, "#splitline{Allowed #kappa_{#lambda} interval}{at 95% CL}");
      else
	textExcl.DrawLatex(0.19, ybase+0.1, "#splitline{Allowed #kappa_{#lambda} interval}{at 95% CL}");
      
      TLatex textObsExp;
      textObsExp.SetNDC();
      textObsExp.SetTextSize(textsize);
      textObsExp.SetTextFont(42);
      if (statOnly)
	textObsExp.DrawLatex(0.19, ybase-downstep/2-downstep, "Exp. stat.");
      else {
	textObsExp.DrawLatex(0.24, ybase+0.02, "Obs.               Exp.");
	textObsExp.DrawLatex(0.24, ybase+0.02-downstep/2, "                 (Exp. stat.)");
      }
    }
    
    for (int j = 0; j<channel.size() && j<numberChannelExclusions; j++) {
      TString cha = channel.at(j);
      cout<<"Channel Name: "<<cha<<endl;
      
      exclusionExpLow=GetIntersectionsOfGraphs(gr_limits_exp[cha],theory_curve[modelStr],ExpLowLeft[cha],ExpLowRight[cha],debug);
      exclusionExpHigh=GetIntersectionsOfGraphs(gr_limits_exp[cha],theory_curve[modelStr],ExpHighLeft[cha],ExpHighRight[cha],debug, c1,mg,cha,"Exp");
      exclusionObsLow=GetIntersectionsOfGraphs(gr_limits_obs[cha],theory_curve[modelStr],ObsLowLeft[cha],ObsLowRight[cha],debug);
      exclusionObsHigh=GetIntersectionsOfGraphs(gr_limits_obs[cha],theory_curve[modelStr],ObsHighLeft[cha],ObsHighRight[cha],debug,c1,mg,cha, "Obs");
      // only for the statsonly col to add to fullsyst plots
      if (!statOnly) {
	exclusionExpLow_stat=GetIntersectionsOfGraphs(gr_limits_exp_stat[cha+"_statOnly"],theory_curve[modelStr],ExpLowLeft[cha],ExpLowRight[cha],debug);
	exclusionExpHigh_stat=GetIntersectionsOfGraphs(gr_limits_exp_stat[cha+"_statOnly"],theory_curve[modelStr],ExpHighLeft[cha],ExpHighRight[cha],debug, c1,mg,cha,"Exp stat");
      }

      for (int i=0; i<exclusionExpLow.size(); i++)
	std::cout << cha << " - Exp exclusion low = " << exclusionExpLow[i] << std::endl;
      for (int i=0; i<exclusionExpHigh.size(); i++)
	std::cout << cha << " - Exp exclusion high = " << exclusionExpHigh[i] << std::endl;
      if (!statOnly) {
	for (int i=0; i<exclusionObsLow.size(); i++)
	  std::cout << cha << " - Obs exclusion low = " << exclusionObsLow[i] << std::endl;
	for (int i=0; i<exclusionObsHigh.size(); i++)
	  std::cout << cha << " - Obs exclusion high = " << exclusionObsHigh[i] << std::endl;
	
	// when statOnly=true, the printed exp limits correspond to real exp stat-only limits
	for (int i=0; i<exclusionExpLow_stat.size(); i++)
	  std::cout << cha << " - Exp exclusion low stat. = " << exclusionExpLow_stat[i] << std::endl;
	for (int i=0; i<exclusionExpHigh_stat.size(); i++)
	  std::cout << cha << " - Exp exclusion high stat. = " << exclusionExpHigh_stat[i] << std::endl;
      }
      
      
      
      // draw exclusions in lambda plot
      if (strModel.EqualTo("lambda")) {
	if (cha.Contains("comb")) {
	  
	  // TLatex chanName;
	  // chanName.SetNDC();
	  // chanName.SetTextSize(textsize);
	  // chanName.SetTextFont(42);
	  // chanName.DrawLatex(0.19, ybase-j*downstep, std::get<1>(coloursAndLegendNames[(const char*) cha]));
	  
	  const char* strObsExcl = Form("%.1f #minus %.1f", exclusionObsLow[0], exclusionObsHigh[0]);
	  const char* strExpExcl = Form("%.1f #minus %.1f", exclusionExpLow[0], exclusionExpHigh[0]);
	  // prepare exceptoinally statsonly in the plot of full syst, however strExpExcl still become statsonly when statOnly=true
	  const char* strExpExcl_stat = "";
	  if (!statOnly)
	    strExpExcl_stat = Form("(%.1f #minus %.1f)", exclusionExpLow_stat[0], exclusionExpHigh_stat[0]);
	  
	  if (!statOnly) {
	    TLatex obsExcl;
	    obsExcl.SetNDC();
	    obsExcl.SetTextSize(textsize);
	    obsExcl.SetTextFont(42);
	    // if (cha.EqualTo("bbbb"))
	    //   obsExcl.DrawLatex(0.27, ybase-j*downstep, strObsExcl);
	    // else
	    obsExcl.DrawLatex(0.19, ybase-downstep, strObsExcl);
	    
	    TLatex verticalBar;
	    verticalBar.SetNDC();
	    verticalBar.SetTextSize(textsize);
	    verticalBar.SetTextFont(42);
	    verticalBar.DrawLatex(0.363, ybase-downstep, "#lbar");
	  }
	  
	  TLatex expExcl;
	  expExcl.SetNDC();
	  expExcl.SetTextSize(textsize);
	  expExcl.SetTextFont(42);
	  if (statOnly) {
	    expExcl.DrawLatex(0.37, ybase-downstep/2-downstep, strExpExcl);
	  }
	  else {
	    // if (cha.EqualTo("bbbb")){
	    //   expExcl.DrawLatex(0.419, ybase-j*downstep, strExpExcl);
	    //   expExcl.DrawLatex(0.424, ybase-downstep/2-j*downstep, strExpExcl_stat);
	    // }
	    // else{
	    expExcl.DrawLatex(0.39, ybase-downstep, strExpExcl);
	    expExcl.DrawLatex(0.38, ybase-downstep/2-downstep, strExpExcl_stat);
	      //}
	  }
	}	
      }
      // end draw exclusions
      
      exclusionExpLow.clear();
      exclusionExpHigh.clear();
      exclusionObsLow.clear();
      exclusionObsHigh.clear();

      exclusionExpLow_stat.clear();
      exclusionExpHigh_stat.clear();
    }
  }
  
  // c1->cd();

  //______________________________________________________________________________
  //Legend
  TLegend* leg;
  TLegend* leg2;
  TLegend* leg3;

  if (strModel.EqualTo("spin-0")) {
    if (conf) {
      leg =  new TLegend(0., 0.16, 0.95, 0.95);
      leg2 = new TLegend(0.52, 0.70, 0.82, 0.91);
    }
    else {
      leg =  new TLegend(0., 0.16, 0.98, 0.95); //0.25, 0.57, 0.50, 0.92
      leg2 = new TLegend(0.2, 0.70, 0.45, 0.92);  //0.52, 0.57, 0.82, 0.92
    }
  }
  else if (strModel.EqualTo("spin-2")) {
    if (conf){
      leg =  new TLegend(0., 0.16, 0.95, 0.95);
      leg2 = new TLegend(0.52, 0.75, 0.82, 0.92);
    }
    else {
      leg =  new TLegend(0., 0.16, 0.95, 0.95);
      leg2 = new TLegend(0.52, 0.75, 0.82, 0.92);
    }
  }
  else if (strModel.EqualTo("lambda")) {
    if (doLogScale) {
      if (statOnly) {
        leg =  new TLegend(0., 0.16, 0.97, 0.95); //0.21, 0.75, 0.50, 0.92
	leg2 = new TLegend(0.50, 0.75, 0.80, 0.92); //0.50, 0.75, 0.80, 0.92
      } else {
        leg =  new TLegend(0., 0.16, 0.97, 0.95); //0.21, 0.735, 0.50, 0.92
	leg2 = new TLegend(0.50, 0.735, 0.80, 0.92); //0.50, 0.735, 0.80, 0.92
      }
    }
    else {
      if (statOnly) {
        leg =  new TLegend(0., 0.16, 0.95, 0.95); //0.21, 0.75, 0.50, 0.92
	leg2 = new TLegend(0.46, 0.75, 0.76, 0.92); //0.46, 0.75, 0.76, 0.92
      }
      else {
        leg =  new TLegend(0., 0.16, 0.95, 0.95); //0.21, 0.72, 0.50, 0.92
	leg2 = new TLegend(0.46, 0.75, 0.76, 0.92); //0.46, 0.75, 0.76, 0.92
      }
    }
  }

  if( strModel.EqualTo("spin-0") || strModel.EqualTo("spin-2") ){
    //if( is2ColumnLegend ){
	  leg3 = new TLegend(0.16, 0.16, 0.95, 0.95);
	  //}
  }
  else 
    leg3 = (TLegend*) leg->Clone("leg3");

  leg->SetFillStyle(0);
  leg->SetBorderSize(1);
  leg2->SetBorderSize(1);
  leg2->SetFillStyle(1);
  leg3->SetFillStyle(0);
  leg3->SetBorderSize(1);

  leg->SetTextFont(42); // default non-bold
  leg2->SetTextFont(42); // default non-bold
  leg3->SetTextFont(42); // default non-bold

  // Add Entry

  //dummy graph for generic exp and obs legend entry
  if (oneLegEntryPerChannel) {
    TGraph* dummy_gr_exp = new TGraph(1);
    dummy_gr_exp->SetLineStyle(7);
    dummy_gr_exp->SetLineWidth(2);
	if( strModel.Contains("spin") && savePad2 ) dummy_gr_exp->SetLineWidth(7);
	if( !statOnly ){
      leg->AddEntry(dummy_gr_exp, "Exp. 95\% CL limits", "l");
	}
	if( statOnly ){
      leg->AddEntry(dummy_gr_exp, "Exp. 95\% CL limits", "l");
	}
	if( strModel.Contains("spin") && savePad2 ){
      leg3->AddEntry(dummy_gr_exp, "#splitline{Exp. 95\% CL}{limits}", "l");
	}else{
      leg3->AddEntry(dummy_gr_exp, "Exp. 95\% CL limits", "l");
	}
    TGraph* dummy_gr_obs = new TGraph(1);
    dummy_gr_obs->SetLineStyle(1);
    dummy_gr_obs->SetLineWidth(2);
	if( strModel.Contains("spin") && savePad2 ) dummy_gr_obs->SetLineWidth(7);
    if (!statOnly && drawObserved) {
      leg->AddEntry(dummy_gr_obs, "Obs. 95\% CL limits", "l");

	  if( strModel.Contains("spin") && savePad2 ){
        leg3->AddEntry(dummy_gr_obs, "#splitline{Obs. 95\% CL}{limits}", "l");
	  }else{
        leg3->AddEntry(dummy_gr_obs, "Obs. 95\% CL limits", "l");
	  }
    }
  }

  // only make wider line as the legend is not ... by itself
  if( strModel.Contains("spin") && savePad2 ){
    std::cout << "ENH LEG" << std::endl;
    for (std::map<std::string, TGraph*>::iterator iter_limitPlots = limitPlots_exp.begin(); iter_limitPlots != limitPlots_exp.end(); ++ iter_limitPlots) {
	  iter_limitPlots->second->SetLineWidth(7);
	}
    for (std::map<std::string, TGraph*>::iterator iter_limitPlots = limitPlots_obs.begin(); iter_limitPlots != limitPlots_obs.end(); ++ iter_limitPlots) {
	  iter_limitPlots->second->SetLineWidth(7);
	}
  }

  for (std::map<std::string, TGraph*>::iterator iter_limitPlots = limitPlots_exp.begin(); iter_limitPlots != limitPlots_exp.end(); ++ iter_limitPlots) {

    if (iter_limitPlots->first.find("comb") == std::string::npos && iter_limitPlots->first.find("statOnly") == std::string::npos) {
      if (!oneLegEntryPerChannel) {
	leg->AddEntry(iter_limitPlots->second, Form("%s (exp.)", std::get<1>(coloursAndLegendNames[iter_limitPlots->first])), "l");
	leg3->AddEntry(iter_limitPlots->second, Form("%s (exp.)", std::get<1>(coloursAndLegendNames[iter_limitPlots->first])), "l");
      }
      else {
	// if (statOnly) {  // !!!! Changed on 19-03-2020 (correct?) !!!!
	  //leg->AddEntry(iter_limitPlots->second, Form("%s (exp.)", std::get<1>(coloursAndLegendNames[iter_limitPlots->first])), "l");
	  //leg3->AddEntry(iter_limitPlots->second, Form("%s (exp.)", std::get<1>(coloursAndLegendNames[iter_limitPlots->first])), "l");
	leg->AddEntry(iter_limitPlots->second, Form("%s", std::get<1>(coloursAndLegendNames[iter_limitPlots->first])), "l");
	leg3->AddEntry(iter_limitPlots->second, Form("%s", std::get<1>(coloursAndLegendNames[iter_limitPlots->first])), "l");
	  //}	
      }

      if (!statOnly) {
	if (drawObserved && iter_limitPlots->first.find("statOnly") == std::string::npos) {
	  if (oneLegEntryPerChannel) {
	    leg->AddEntry(limitPlots_obs[iter_limitPlots->first], Form("%s", std::get<1>(coloursAndLegendNames[iter_limitPlots->first])), "l");
	    leg3->AddEntry(limitPlots_obs[iter_limitPlots->first], Form("%s", std::get<1>(coloursAndLegendNames[iter_limitPlots->first])), "l");
	  }
	  else {
	    leg->AddEntry(limitPlots_obs[iter_limitPlots->first], Form("%s (obs.)", std::get<1>(coloursAndLegendNames[iter_limitPlots->first])), "l");
	    leg3->AddEntry(limitPlots_obs[iter_limitPlots->first], Form("%s (obs.)", std::get<1>(coloursAndLegendNames[iter_limitPlots->first])), "l");
	  }
	}
      }
    }
  }
  // the standalone legend is made with spin-0 if-control
  if (strModel.EqualTo("spin-0")) {
    if (conf) {
      // leg2
      leg->AddEntry(limitPlots_exp["comb_B_bbbb_bbtautau"], "Combined (exp.)", "l");
      leg3->AddEntry(limitPlots_exp["comb_B_bbbb_bbtautau"], "Comb. (exp.)", "l");
      if (drawObserved) {
	// leg2
	leg->AddEntry(limitPlots_obs["comb_B_bbbb_bbtautau"], "Combined (obs.)", "p l");
	leg3->AddEntry(limitPlots_obs["comb_B_bbbb_bbtautau"], "Comb. (obs.)", "p l");
	limitPlots_obs["comb_B_bbbb_bbtautau"]->SetMarkerSize(1.0);
	//limitPlots_obs["comb_F_bbbb_bbtautau_bbyy"]->SetMarkerSize(1.0);
      }
    }
    else {
      // leg2
      leg->AddEntry(limitPlots_exp["comb_B_bbbb_bbtautau"], "Combined (exp.)", "l");
      //leg3->AddEntry(limitPlots_exp["comb_E_bbbb_bbtautau_bbyy_WWyy_WWWW"], "Comb. (exp.)", "l"); // reduce exp. comb. as in individual channels
      //leg->AddEntry(limitPlots_exp["comb_E_bbbb_bbtautau_bbyy_WWyy"], "Combined (exp.)", "l");
      if (drawObserved) {
	// leg2
	leg->AddEntry(limitPlots_obs["comb_B_bbbb_bbtautau"], "Combined (obs.)", "p l");
	leg3->AddEntry(limitPlots_obs["comb_A_bbbb_bbtautau_bbyy"], "Comb. (obs.)", "p l");
	//leg->AddEntry(limitPlots_obs["comb_E_bbbb_bbtautau_bbyy_WWyy"], "Combined (obs.)", "p l");
        //limitPlots_obs["comb_B_bbbb_bbtautau"]->SetMarkerSize(1.0);
	//limitPlots_obs["comb_E_bbbb_bbtautau_bbyy_WWyy"]->SetMarkerSize(1.0);
      }
    }
  }
  else if (strModel.EqualTo("spin-2")) {
    if (conf) {
      if (strCoupling.EqualTo("c = 1.0")) {
        leg2->AddEntry(limitPlots_exp["comb_E_bbbb_bbtautau"], "Comb. (exp.)", "l");
        if (drawObserved) {
          leg2->AddEntry(limitPlots_obs["comb_E_bbbb_bbtautau"], "Comb. (obs.)", "pl");
          limitPlots_obs["comb_E_bbbb_bbtautau"]->SetMarkerSize(1.0);
          limitPlots_obs["comb_D_bbbb_bbtautau"]->SetMarkerSize(1.0);
        }
      }
      else if (strCoupling.EqualTo("c = 2.0")) {
        leg2->AddEntry(limitPlots_exp["comb_B_bbbb_bbtautau"], "Comb. (exp.)", "l");
        if (drawObserved) {
          leg2->AddEntry(limitPlots_obs["comb_B_bbbb_bbtautau"], "Comb. (obs.)", "pl");
          limitPlots_obs["comb_B_bbbb_bbtautau"]->SetMarkerSize(1.0);
          limitPlots_obs["comb_A_bbbb_bbtautau"]->SetMarkerSize(1.0);
        }
      }
    }
    else {
      leg2->AddEntry(limitPlots_exp["comb_E_bbbb_bbtautau_bbWW"], "Comb. (exp.)", "l");
      if (drawObserved)
	leg2->AddEntry(limitPlots_obs["comb_E_bbbb_bbtautau_bbWW"], "Comb. (obs.)", "l");
    }
  }
  else if (strModel.EqualTo("lambda")) {
    if (doExtrapolationTo140fb || doExtrapolationTo440fb) {
      leg->AddEntry(limitPlots_exp["comb_bbtautau_bbyy"], "Comb. (exp.)", "l");
      if (drawObserved) {
	limitPlots_obs["comb_bbtautau_bbyy"]->SetMarkerSize(0);
	//leg2
	leg->AddEntry(limitPlots_obs["comb_bbtautau_bbyy"], "Comb. (obs.)", "p l");
      }
    }
    else {
      //leg2
      if (!oneLegEntryPerChannel) {
	leg->AddEntry(limitPlots_exp["comb_bbbb_bbtautau_bbyy"], "Comb. (exp.)", "l");
      }
      if (statOnly) {
	//leg2
	//leg->AddEntry(limitPlots_exp["comb_bbbb_bbtautau_bbyy"], "Comb. (exp.)", "l");
	leg->AddEntry(limitPlots_exp["comb_bbbb_bbtautau_bbyy"], "Comb.", "l");
	//leg->AddEntry(limitPlots_exp["comb_bbbb_bbtautau_bbyy_fullSyst"], "#splitline{Comb. (exp.)}{full syst.}", "l");
	leg->AddEntry(limitPlots_exp["comb_bbbb_bbtautau_bbyy_fullSyst"], "#splitline{Exp. 95\% CL limits}{Comb. full syst.}", "l");
      }
      if (!statOnly) {
	if (drawObserved) {
	  limitPlots_obs["comb_bbbb_bbtautau_bbyy"]->SetMarkerSize(0);
	  //leg2
	  if (oneLegEntryPerChannel)
	    leg->AddEntry(limitPlots_obs["comb_bbbb_bbtautau_bbyy"], "Comb.", "p l");
	  else
	    leg->AddEntry(limitPlots_obs["comb_bbbb_bbtautau_bbyy"], "Comb. (obs.)", "p l");
	}
      }
    }
  }

  // leg2
  leg->AddEntry(limit_plot_1s, "Comb. #pm1#sigma (exp.)", "f");
  leg->AddEntry(limit_plot_2s, "Comb. #pm2#sigma (exp.)", "f");
  leg3->AddEntry(limit_plot_1s, "#splitline{Comb. #pm1#sigma}{(exp.)}", "f");
  leg3->AddEntry(limit_plot_2s, "#splitline{Comb. #pm2#sigma}{(exp.)}", "f");

  if (strModel.EqualTo("lambda")) {
    leg->AddEntry(gr_lambda_NLO, "Theory prediction", "lf"); 
    leg3->AddEntry(gr_lambda_NLO, "Theory prediction", "lf"); 
  }

  //if (strModel.EqualTo("spin-0"))
    // leg2
    // leg->AddEntry(gr_theory_xsec_spin0, "hMSSM (tan#beta = 2)", "l"); 
  if (strModel.EqualTo("spin-0") && savePad2) {
    // leg2
    leg->AddEntry(gr_theory_xsec_spin2c20, "Bulk RS", "l"); 
    leg3->AddEntry(gr_theory_xsec_spin2c20, "Bulk RS", "l"); 
  }
  if (strModel.EqualTo("spin-2") && strCoupling.EqualTo("c = 1.0")) {
    // leg2
    leg->AddEntry(gr_theory_xsec_spin2c10, "Bulk RS, k/#bar{M}_{Pl} = 1.0", "l"); 
    leg3->AddEntry(gr_theory_xsec_spin2c10, "Bulk RS, k/#bar{M}_{Pl} = 1.0", "l"); 
  }
  if (strModel.EqualTo("spin-2") && strCoupling.EqualTo("c = 2.0")) {
    // leg2
    leg->AddEntry(gr_theory_xsec_spin2c20, "Bulk RS, k/#bar{M}_{Pl} = 2.0", "l"); 
    leg3->AddEntry(gr_theory_xsec_spin2c20, "Bulk RS, k/#bar{M}_{Pl} = 2.0", "l"); 
  }

  pad1->Modified();
  c1->cd();

  ///TCanvas* c2 = new TCanvas("c2", "c2", 150, 500);
  TPad* pad2 = new TPad("pad2", "pad2", 0.75, 0., 1., 1.);
  pad2->Draw();
  pad2->cd();
  std::cout << "Switching to pad2" << std::endl;

  if (strModel.EqualTo("spin-0")) {
    leg->SetTextSize(0.075);
    leg2->SetTextSize(0.035);
    leg3->SetTextSize(0.075);
  }
  else if (strModel.EqualTo("spin-2")) {
    if (oneLegEntryPerChannel) {
      leg->SetTextSize(0.08);
      leg3->SetTextSize(0.08);
    }
    else {
      leg->SetTextSize(0.07);
      leg3->SetTextSize(0.07);
    }
  }
  else if (strModel.EqualTo("lambda")) {
    if (oneLegEntryPerChannel) {
      leg->SetTextSize(0.09);
      leg3->SetTextSize(0.09);
    }
    else {
      leg->SetTextSize(0.07);
      leg3->SetTextSize(0.07);
    }
  }

  // if( is2ColumnLegend ){
  //   leg->SetTextSize(0.031);
  //   leg->SetNColumns(2);
  // }

  leg->Draw();
  //if (!strModel.EqualTo("spin-0")) {
  //leg2->Draw();
  //}
  lg3->SetFillStyle(0);
  lg3->SetBorderSize(0);
  // lg3->Draw("same");

  pad2->RedrawAxis();
  pad2->Update();
  pad2->Modified();

  if(savePad2){
    //pad2->cd();
    //pad2->SaveAs(Form("%s.eps", (const char*) strOutfile));
    TCanvas* c2;
    if( is2ColumnLegend ) {
      c2 = new TCanvas("c2_wide","c2_wide", 600*0.76, 500 );
      leg3->SetTextSize(0.05);
      leg3->SetNColumns(2);
    }
    else
      c2 = new TCanvas("c2", "c2", 150, 500);

    c2->cd();
    leg3->Draw();
    if (savePlots){
      c2->SaveAs(Form("%s.pdf", (const char*) strOutfile));
	}
    c1->cd();
  }


  pad1->cd();
  std::cout << "Switching back to pad1" << std::endl;
  
  //______________________________________________________________________
  //Lines for paper, not conf note
  if (strModel.EqualTo("spin-0")) {
    TLine *line;
    if (extendTo3TeV)
      line = new TLine(500., ymin, 500., 20.);  //ymax=30 //ymax=8
    else
      line = new TLine(500., ymin, 500., 10.);
    line->SetLineStyle(1);
    line->SetLineWidth(2);
    if (!conf)
      // line->Draw();

    if (extendTo3TeV) {
      TLine *line3 = new TLine(1000., ymin, 1000., 3.);  //ymax=30 //ymax=8
      line3->SetLineStyle(1);
      line3->SetLineWidth(2);
      if (!conf)
	line3->Draw();
    }
  }
  else if (strModel.EqualTo("spin-2")) {
    TLine *line1 = new TLine(500., ymin, 500., 25.);
    line1->SetLineStyle(1);
    line1->SetLineWidth(2);
    if (!conf)
      line1->Draw();

    TLine *line2 = new TLine(1000., ymin, 1000., 3.);
    line2->SetLineStyle(1);
    line2->SetLineWidth(2);
    if (!conf && extendTo3TeV)
      line2->Draw();
  }


  if (strModel.EqualTo("lambda")) {
    TLine* L1;
    if (doLogScale)
      L1 = new TLine(1,-0.15,1,ymax); //ymax=3.2
    else
      L1 = new TLine(1,-0.15,1,ymax); //ymax=3.2
    L1->SetLineStyle(7);
    L1->SetLineColor(kGray+1);  //kMagenta-5
    L1->SetLineWidth(2);
    L1->Draw();
    
    TLatex latexSM;
    latexSM.SetTextSize(0.045);
    latexSM.SetTextColor(kGray+1);  //kMagenta-5
    latexSM.SetTextAlign(33);  //align at top
    latexSM.DrawLatex(0.50,2.5,"SM");
  }


  //______________________________________________
  //ATLAS logo
  if (strModel.EqualTo("lambda") && doLogScale)
    if( internal == "" ) // this mean "ATLAS" public
	{
      ATLASLabelSplit(0.68, 0.30, internal, kBlack);
	}else{ //internal or preliminary
      ATLASLabelSplit(0.68, 0.37, internal, kBlack);
	}
  else
    ATLASLabel(0.45, 0.88, internal, kBlack);
  
  TLatex L;
  L.SetNDC();
  L.SetTextSize(0.04);
  L.SetTextFont(42);
  if (strModel.EqualTo("lambda") && doLogScale)
    L.DrawLatex(0.68, 0.23, Form("#splitline{#sqrt{s} = %s}{%s fb^{-1}}", (const char*) strCMSenergy, (const char*) strLumi)); //y=0.28
  else
    L.DrawLatex(0.45, 0.83, Form("#sqrt{s} = %s,  %s fb^{-1}", (const char*) strCMSenergy, (const char*) strLumi));
  
  TLatex l;
  l.SetNDC();
  l.SetTextSize(0.05);
  l.SetTextFont(42);

  if (strModel.EqualTo("spin-0"))
    l.DrawLatex(0.75, 0.72, (const char*) strModel); // x=0.7, y=0.22
  else if (strModel.EqualTo("spin-2")) {
    strCoupling = strCoupling.ReplaceAll("c","k/#bar{M}_{Pl}");
    l.DrawLatex(0.7, 0.72, Form("#splitline{%s}{%s}", (const char*) strModel, (const char*) strCoupling));  // x=0.6, y=0.2
  }

  if (statOnly) {
    TLatex s;
    s.SetNDC();
    s.SetTextSize(0.05);
    s.SetTextFont(42);
    if (strModel.EqualTo("lambda")) {
      if (doLogScale){
	s.DrawLatex(0.68, 0.5, "Stat. only"); //x: 0.638, y: 0.69
	s.DrawLatex(0.68, 0.45, "dashed lines"); //x: 0.638, y: 0.69
	}
      else
	s.DrawLatex(0.7, 0.28, "Stat. only");
    }
  }

  pad1->RedrawAxis();
  pad1->Update();
  pad1->Modified();
  
  if (savePlots) {
    if(savePad1){
      pad1->cd();
      pad1->SaveAs(Form("%s.pdf", (const char*) strOutfile));
    }
    else if(savePad2){;}
    else{ // savePad2 save as eps and convert later by hand above (directly pdf does not work ...)
      c1->SaveAs(Form("%s.pdf", (const char*) strOutfile));
      c1->SaveAs(Form("%s.C", (const char*) strOutfile));
    }
    //    c1->SaveAs(Form("%s.eps", (const char*) strOutfile));
    //    c1->SaveAs(Form("%s.png", (const char*) strOutfile));
  }

  if( doHepData ){
    hepdatafile->Close();
  }

  return 0;
}


std::map<int, std::tuple<double, double, double, double, double, double> > ReadInputFile (std::string inFileName, bool useNominalNPs, bool isNanCompatible ) 
{
  std::cout << "Reading in file " << inFileName << std::endl;

  double xsec_m2s = 0.;
  double xsec_m1s = 0.;
  double xsec_exp = 0.;
  double xsec_p1s = 0.;
  double xsec_p2s = 0.;
  double xsec_obs = 0.;

  std::map<int, std::tuple<double, double, double, double, double, double> > massesAndScalings;

  int mass = 0;
  double scaling = 0.;
  double mu_m2s_NP_nominal = 0., mu_m1s_NP_nominal = 0., mu_exp_NP_nominal = 0., mu_p1s_NP_nominal = 0., mu_p2s_NP_nominal = 0., mu_obs_NP_nominal = 0.;
  double xsec_m2s_NP_nominal = 0., xsec_m1s_NP_nominal = 0., xsec_exp_NP_nominal = 0., xsec_p1s_NP_nominal = 0., xsec_p2s_NP_nominal = 0., xsec_obs_NP_nominal = 0.;
  double mu_m2s_NP_profiled = 0., mu_m1s_NP_profiled = 0., mu_exp_NP_profiled = 0., mu_p1s_NP_profiled = 0., mu_p2s_NP_profiled = 0., mu_obs_NP_profiled = 0.;
  double xsec_m2s_NP_profiled = 0., xsec_m1s_NP_profiled = 0., xsec_exp_NP_profiled = 0., xsec_p1s_NP_profiled = 0., xsec_p2s_NP_profiled = 0., xsec_obs_NP_profiled = 0.;
  
  // nan compatible solution: read in everything string
  std::string s_mu_m2s_NP_nominal = "", s_mu_m1s_NP_nominal = "", s_mu_exp_NP_nominal = "", s_mu_p1s_NP_nominal = "", s_mu_p2s_NP_nominal = "", s_mu_obs_NP_nominal = "";
  std::string s_xsec_m2s_NP_nominal = "", s_xsec_m1s_NP_nominal = "", s_xsec_exp_NP_nominal = "", s_xsec_p1s_NP_nominal = "", s_xsec_p2s_NP_nominal = "", s_xsec_obs_NP_nominal = "";
  std::string s_mu_m2s_NP_profiled = "", s_mu_m1s_NP_profiled = "", s_mu_exp_NP_profiled = "", s_mu_p1s_NP_profiled = "", s_mu_p2s_NP_profiled = "", s_mu_obs_NP_profiled = "";
  std::string s_xsec_m2s_NP_profiled = "", s_xsec_m1s_NP_profiled = "", s_xsec_exp_NP_profiled = "", s_xsec_p1s_NP_profiled = "", s_xsec_p2s_NP_profiled = "", s_xsec_obs_NP_profiled = "";
  //
  
  fstream file (inFileName, ios::in);
  if (!file.good()) {
    std::cerr << "ERROR : Function 'ReadInputFile': File '" << inFileName << "' could not be opened!" << std::endl;
  }
  
  std::string strMass = "";
  
  file >> skipline;
  while (!file.eof()) {
    if( isNanCompatible ){ // able to take nan
      file >> strMass >> scaling 
	   >> s_mu_m2s_NP_nominal >> s_mu_m1s_NP_nominal >> s_mu_exp_NP_nominal >> s_mu_p1s_NP_nominal >> s_mu_p2s_NP_nominal >> s_mu_obs_NP_nominal 
	   >> s_xsec_m2s_NP_nominal >> s_xsec_m1s_NP_nominal >> s_xsec_exp_NP_nominal >> s_xsec_p1s_NP_nominal >> s_xsec_p2s_NP_nominal >> s_xsec_obs_NP_nominal 
	   >> s_mu_m2s_NP_profiled >> s_mu_m1s_NP_profiled >> s_mu_exp_NP_profiled >> s_mu_p1s_NP_profiled >> s_mu_p2s_NP_profiled >> s_mu_obs_NP_profiled 
	   >> s_xsec_m2s_NP_profiled >> s_xsec_m1s_NP_profiled >> s_xsec_exp_NP_profiled >> s_xsec_p1s_NP_profiled >> s_xsec_p2s_NP_profiled >> s_xsec_obs_NP_profiled 
	   >> skipline;
    }
    else{ // normally
      file >> strMass >> scaling 
	   >> mu_m2s_NP_nominal >> mu_m1s_NP_nominal >> mu_exp_NP_nominal >> mu_p1s_NP_nominal >> mu_p2s_NP_nominal >> mu_obs_NP_nominal 
	   >> xsec_m2s_NP_nominal >> xsec_m1s_NP_nominal >> xsec_exp_NP_nominal >> xsec_p1s_NP_nominal >> xsec_p2s_NP_nominal >> xsec_obs_NP_nominal 
	   >> mu_m2s_NP_profiled >> mu_m1s_NP_profiled >> mu_exp_NP_profiled >> mu_p1s_NP_profiled >> mu_p2s_NP_profiled >> mu_obs_NP_profiled 
	   >> xsec_m2s_NP_profiled >> xsec_m1s_NP_profiled >> xsec_exp_NP_profiled >> xsec_p1s_NP_profiled >> xsec_p2s_NP_profiled >> xsec_obs_NP_profiled 
	   >> skipline;
    }
    
    mass = StrToInt(strMass);
    
    
    if( isNanCompatible ){
      mu_m2s_NP_nominal    = s2f( s_mu_m2s_NP_nominal   );
      mu_m1s_NP_nominal    = s2f( s_mu_m1s_NP_nominal   );
      mu_exp_NP_nominal    = s2f( s_mu_exp_NP_nominal   );
      mu_p1s_NP_nominal    = s2f( s_mu_p1s_NP_nominal   );
      mu_p2s_NP_nominal    = s2f( s_mu_p2s_NP_nominal   );
      mu_obs_NP_nominal    = s2f( s_mu_obs_NP_nominal   );
      xsec_m2s_NP_nominal  = s2f( s_xsec_m2s_NP_nominal );
      xsec_m1s_NP_nominal  = s2f( s_xsec_m1s_NP_nominal );
      xsec_exp_NP_nominal  = s2f( s_xsec_exp_NP_nominal );
      xsec_p1s_NP_nominal  = s2f( s_xsec_p1s_NP_nominal );
      xsec_p2s_NP_nominal  = s2f( s_xsec_p2s_NP_nominal );
      xsec_obs_NP_nominal  = s2f( s_xsec_obs_NP_nominal );
      mu_m2s_NP_profiled   = s2f( s_mu_m2s_NP_profiled  );
      mu_m1s_NP_profiled   = s2f( s_mu_m1s_NP_profiled  );
      mu_exp_NP_profiled   = s2f( s_mu_exp_NP_profiled  );
      mu_p1s_NP_profiled   = s2f( s_mu_p1s_NP_profiled  );
      mu_p2s_NP_profiled   = s2f( s_mu_p2s_NP_profiled  );
      mu_obs_NP_profiled   = s2f( s_mu_obs_NP_profiled  );
      xsec_m2s_NP_profiled = s2f( s_xsec_m2s_NP_profiled);
      xsec_m1s_NP_profiled = s2f( s_xsec_m1s_NP_profiled);
      xsec_exp_NP_profiled = s2f( s_xsec_exp_NP_profiled);
      xsec_p1s_NP_profiled = s2f( s_xsec_p1s_NP_profiled);
      xsec_p2s_NP_profiled = s2f( s_xsec_p2s_NP_profiled);
      xsec_obs_NP_profiled = s2f( s_xsec_obs_NP_profiled);
    }
    
    
    if (useNominalNPs) {
      xsec_m2s = xsec_m2s_NP_nominal;
      xsec_m1s = xsec_m1s_NP_nominal;
      xsec_exp = xsec_exp_NP_nominal;
      xsec_p1s = xsec_p1s_NP_nominal;
      xsec_p2s = xsec_p2s_NP_nominal;
    }
    else {
      xsec_m2s = xsec_m2s_NP_profiled;
      xsec_m1s = xsec_m1s_NP_profiled;
      xsec_exp = xsec_exp_NP_profiled;
      xsec_p1s = xsec_p1s_NP_profiled;
      xsec_p2s = xsec_p2s_NP_profiled;
    }
    xsec_obs = xsec_obs_NP_profiled;
    
    std::tuple<double, double, double, double, double, double> mu_exp_and_sdev (xsec_m2s, xsec_m1s, xsec_exp, xsec_p1s, xsec_p2s, xsec_obs);  
    massesAndScalings[mass] = mu_exp_and_sdev;
  }
  
  file.close();
  
  return massesAndScalings;
}


std::map<int, std::tuple<double, double, double, double, double, double> > ReadInputFile_LimitsFromPaper (std::string inFileName, bool debug) 
{
  std::cout << "Reading in limits from paper from file " << inFileName << std::endl;

  int mass = 0;
  double xsec_m2s = 0.;
  double xsec_m1s = 0.;
  double xsec_exp = 0.;
  double xsec_p1s = 0.;
  double xsec_p2s = 0.;
  double xsec_obs = 0.;

  std::map<int, std::tuple<double, double, double, double, double, double> > massesAndScalings;
  
  fstream file (inFileName, ios::in);
  if (!file.good()) {
    std::cerr << "ERROR : Function 'ReadInputFile': File '" << inFileName << "' could not be opened!" << std::endl;
  }
  
  std::string strMass = "";
  
  file >> skipline;
  while (!file.eof()) {
    file >> strMass >> xsec_m2s >> xsec_m1s >> xsec_exp >> xsec_p1s >> xsec_p2s >> xsec_obs;
    
    mass = StrToInt(strMass);

    if (debug) {
      std::cout << "mass = " << mass << std::endl;
      std::cout << "Values read in from input file:" << std::endl;
      std::cout << "xsec_m2s = " << xsec_m2s << std::endl;
      std::cout << "xsec_m1s = " << xsec_m1s << std::endl;
      std::cout << "xsec_exp = " << xsec_exp << std::endl;
      std::cout << "xsec_p1s = " << xsec_p1s << std::endl;
      std::cout << "xsec_p2s = " << xsec_p2s << std::endl;
      std::cout << "xsec_obs = " << xsec_obs << std::endl;
    } 
    
    xsec_m2s = xsec_exp - xsec_m2s;
    xsec_m1s = xsec_exp - xsec_m1s;
    xsec_p1s = xsec_p1s - xsec_exp;
    xsec_p2s = xsec_p2s - xsec_exp;
    
    if (debug) {
      std::cout << "Values with relative uncertainties: " << std::endl;
      std::cout << "xsec_m2s = " << xsec_m2s << std::endl;
      std::cout << "xsec_m1s = " << xsec_m1s << std::endl;
      std::cout << "xsec_exp = " << xsec_exp << std::endl;
      std::cout << "xsec_p1s = " << xsec_p1s << std::endl;
      std::cout << "xsec_p2s = " << xsec_p2s << std::endl;
      std::cout << "xsec_obs = " << xsec_obs << std::endl;
    } 
    
    std::tuple<double, double, double, double, double, double> mu_exp_and_sdev (xsec_m2s, xsec_m1s, xsec_exp, xsec_p1s, xsec_p2s, xsec_obs);  
    massesAndScalings[mass] = mu_exp_and_sdev;
  }
  
  file.close();
  
  return massesAndScalings;
}


std::map<int, std::tuple<double, double, double, double, double, double> > ReadInputFile_bbyyLimitsFromPaper (std::string inFileName, TString model, bool debug) 
{
  std::cout << "Reading in bbyy limits from paper from file " << inFileName << std::endl;

  int mass = 0;
  double xsec_m2s = 0.;
  double xsec_m1s = 0.;
  double xsec_exp = 0.;
  double xsec_p1s = 0.;
  double xsec_p2s = 0.;
  double xsec_obs = 0.;

  std::map<int, std::tuple<double, double, double, double, double, double> > massesAndScalings;
  
  TFile* file = new TFile(inFileName.c_str(), "READ");
  if (!file->IsOpen()) {
    std::cerr << "ERROR : Function 'ReadInputFile': File '" << inFileName << "' could not be opened!" << std::endl;
  }
  
  
  Int_t ntotal = 0;
  if (model.EqualTo("spin-0"))
    ntotal = ((TGraph*) file->Get("resonant_lm_expected"))->GetN() + ((TGraph*) file->Get("resonant_hm_expected"))->GetN();
  else if (model.EqualTo("lambda"))
    ntotal = ((TGraph*) file->Get("nonres_lambda_expected"))->GetN();


  TGraph* gr_exp = new TGraph(ntotal);
  TGraphAsymmErrors* gr_1sig = new TGraphAsymmErrors(ntotal);
  TGraphAsymmErrors* gr_2sig = new TGraphAsymmErrors(ntotal);
  TGraph* gr_obs = new TGraph(ntotal);

  if (model.EqualTo("spin-0")) {

    TGraph* gr_exp_lm;
    TGraph* gr_exp_hm;
    TGraph* gr_obs_lm;
    TGraph* gr_obs_hm;
    TGraphAsymmErrors* gr_1sig_lm; 
    TGraphAsymmErrors* gr_1sig_hm; 
    TGraphAsymmErrors* gr_2sig_lm;
    TGraphAsymmErrors* gr_2sig_hm;

    gr_exp_lm = (TGraph*) file->Get("resonant_lm_expected");
    gr_exp_hm = (TGraph*) file->Get("resonant_hm_expected");
    gr_1sig_lm = (TGraphAsymmErrors*) file->Get("resonant_lm_pm1sigma");
    gr_1sig_hm = (TGraphAsymmErrors*) file->Get("resonant_hm_pm1sigma");
    gr_2sig_lm = (TGraphAsymmErrors*) file->Get("resonant_lm_pm2sigma");
    gr_2sig_hm = (TGraphAsymmErrors*) file->Get("resonant_hm_pm2sigma");
    gr_obs_lm = (TGraph*) file->Get("resonant_lm_observed");
    gr_obs_hm = (TGraph*) file->Get("resonant_hm_observed");


    int npoints_lm = gr_exp_lm->GetN();
    int npoints_hm = gr_exp_hm->GetN();
    int npoints_total = npoints_lm + npoints_hm;


    for (int i=0; i<npoints_total; i++) {
      if (i < npoints_lm) {
	double exp_x=0., exp_y=0., obs_x=0., obs_y=0.;
	double p1sig=0., m1sig=0., p2sig=0., m2sig=0.;
	gr_exp_lm->GetPoint(i, exp_x, exp_y);
	gr_obs_lm->GetPoint(i, obs_x, obs_y);
	p1sig = gr_1sig_lm->GetErrorYhigh(i);
	m1sig = gr_1sig_lm->GetErrorYlow(i);
	p2sig = gr_2sig_lm->GetErrorYhigh(i);
	m2sig = gr_2sig_lm->GetErrorYlow(i);
	
	gr_exp->SetPoint(i, exp_x, exp_y);
	gr_obs->SetPoint(i, obs_x, obs_y);
	gr_1sig->SetPoint(i, exp_x, exp_y);
	gr_2sig->SetPoint(i, exp_x, exp_y);
	gr_1sig->SetPointError(i, 0., 0., m1sig, p1sig);
	gr_2sig->SetPointError(i, 0., 0., m2sig, p2sig);
      }
      else {
	double exp_x=0., exp_y=0., obs_x=0., obs_y=0.;
	double p1sig=0., m1sig=0., p2sig=0., m2sig=0.;
	gr_exp_hm->GetPoint(i-npoints_total+npoints_hm, exp_x, exp_y);
	gr_obs_hm->GetPoint(i-npoints_total+npoints_hm, obs_x, obs_y);
	p1sig = gr_1sig_hm->GetErrorYhigh(i-npoints_total+npoints_hm);
	m1sig = gr_1sig_hm->GetErrorYlow(i-npoints_total+npoints_hm);
	p2sig = gr_2sig_hm->GetErrorYhigh(i-npoints_total+npoints_hm);
	m2sig = gr_2sig_hm->GetErrorYlow(i-npoints_total+npoints_hm);
	
	gr_exp->SetPoint(i, exp_x, exp_y);
	gr_obs->SetPoint(i, obs_x, obs_y);
	gr_1sig->SetPoint(i, exp_x, exp_y);
	gr_2sig->SetPoint(i, exp_x, exp_y);
	gr_1sig->SetPointError(i, 0., 0., m1sig, p1sig);
	gr_2sig->SetPointError(i, 0., 0., m2sig, p2sig);
      }
    }
   
  }
  else if (model.EqualTo("lambda")) {
    gr_exp = (TGraph*) file->Get("nonres_lambda_expected");
    gr_1sig = (TGraphAsymmErrors*) file->Get("nonres_lambda_pm1sigma");
    gr_2sig = (TGraphAsymmErrors*) file->Get("nonres_lambda_pm2sigma");
    gr_obs = (TGraph*) file->Get("nonres_lambda_observed");
  }


  int npoints = gr_exp->GetN();
  double* masses = gr_exp->GetX();
  double* exp = gr_exp->GetY();
  double* p1sig = gr_1sig->GetEYhigh();
  double* m1sig = gr_1sig->GetEYlow();
  double* p2sig = gr_2sig->GetEYhigh();
  double* m2sig = gr_2sig->GetEYlow();
  double* obs = gr_obs->GetY();

  for (int i=0; i<npoints; i++) {
    
    mass = masses[i];    
    xsec_m2s = m2sig[i];
    xsec_m1s = m1sig[i];
    xsec_exp = exp[i];
    xsec_p1s = p1sig[i];
    xsec_p2s = p2sig[i];
    xsec_obs = obs[i];
    
    if (debug) {
      std::cout << "xsec_m2s = " << xsec_m2s << std::endl;
      std::cout << "xsec_m1s = " << xsec_m1s << std::endl;
      std::cout << "xsec_exp = " << xsec_exp << std::endl;
      std::cout << "xsec_p1s = " << xsec_p1s << std::endl;
      std::cout << "xsec_p2s = " << xsec_p2s << std::endl;
      std::cout << "xsec_obs = " << xsec_obs << std::endl;
    } 
    
    std::tuple<double, double, double, double, double, double> mu_exp_and_sdev (xsec_m2s, xsec_m1s, xsec_exp, xsec_p1s, xsec_p2s, xsec_obs);  
    massesAndScalings[mass] = mu_exp_and_sdev;
  }
  
  file->Close();
  
  return massesAndScalings;
}


std::map<double, double> ReadTheoryXsec (std::string inFileName, double scalefactor)
{
  std::cout << "Reading in theory cross sections from file " << inFileName << std::endl;

  double lambda = 0;
  double xsec = 0.;
  std::map<double, double> theoryXsec;
 
  fstream file (inFileName, ios::in);
  if (!file.good()) {
    std::cerr << "ERROR : Function 'ReadTheoryXsec': File '" << inFileName << "' could not be opened!" << std::endl;
  }
  
  // std::string strMass = "";
  
  file >> skipline;
  while (!file.eof()) {
    file >> lambda >> xsec >> skipline;
    
    // mass = StrToInt(strMass);
    xsec *= scalefactor;    
    theoryXsec[lambda] = xsec;
  }
  
  file.close();
  
  return theoryXsec;
}


void ATLASLabel (Double_t x, Double_t y, const char* text, Color_t color) 
{
  TLatex l; //l.SetTextAlign(12); l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextFont(72);
  l.SetTextColor(color);

  // double delx = 0.115*696*gPad->GetWh()/(472*gPad->GetWw());
  double delx = 0.15*696*gPad->GetWh()/(472*gPad->GetWw());
  double dely = 0.06;

  l.DrawLatex(x,y,"ATLAS");
  if (text) {
    TLatex p; 
    p.SetNDC();
    p.SetTextFont(42);
    p.SetTextColor(color);
    // p.DrawLatex(x+delx,y,text);
    p.DrawLatex(x+delx, y, text);
    //    p.DrawLatex(x,y,"#sqrt{s}=900GeV");
  }
}


void ATLASLabelSplit(Double_t x, Double_t y, const char* text, Color_t color) 
{
  TLatex l; //l.SetTextAlign(12); l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextFont(72);
  l.SetTextColor(color);

  double delx = 0.15*696*gPad->GetWh()/(472*gPad->GetWw());
  double dely = 0.05;

  l.DrawLatex(x,y,"ATLAS");
  if (text) {
    TLatex p; 
    p.SetNDC();
    p.SetTextFont(42);
    p.SetTextColor(color);
    p.DrawLatex(x,y-dely,text);
    //    p.DrawLatex(x,y,"#sqrt{s}=900GeV");
  }
}


int StrToInt (std::string str) 
{
  std::string strOut = "";
  std::string strSign = str.substr(0,1);
  std::string strValue = "";

  if ((str.length() > 1) && (strSign.compare("0") == 0)) {   
    strValue = str.substr(1);
    strOut = "-"+strValue;
  }
  else {
    strValue = str.substr(0);
    strOut = strValue;
  }

  int value = atoi(strOut.c_str());
  
  return value;
}


std::vector<double> GetIntersectionsOfGraphs(TGraph* gr1, TGraph* gr2, double xMinStart, double xMaxStart, bool debug, TCanvas* c = nullptr, TMultiGraph* tmg = nullptr, TString cha = "", TString type = "obs") 
{
  //cout<<"TGraph one name: "<<gr1->GetName()<<endl;
  int npoints_gr1 = gr1->GetN();
  int npoints_gr2 = gr2->GetN();

  double x_gr1[npoints_gr1];
  double y_gr1[npoints_gr1];
  double x_gr2[npoints_gr2];
  double y_gr2[npoints_gr2];

  for (int i=0; i<npoints_gr1; i++) {
    gr1->GetPoint(i, x_gr1[i], y_gr1[i]);
  }

  for (int i=0; i<npoints_gr2; i++) {
    gr2->GetPoint(i, x_gr2[i], y_gr2[i]);
  }

  double xmin_gr1 = x_gr1[0];
  double xmax_gr1 = x_gr1[npoints_gr1];

  double xmin_gr2 = x_gr2[0];
  double xmax_gr2 = x_gr2[npoints_gr2];

  double xmin_common_points = std::max(xmin_gr1, xmin_gr2);
  double xmax_common_points = std::min(xmax_gr1, xmax_gr2);
 
  if (xMinStart != -999. && xMaxStart != -999.) {
    xmin_common_points = xMinStart;
    xmax_common_points = xMaxStart;
  }

  int npoints = 4000;
  double step = (xmax_common_points - xmin_common_points) / npoints;

  TGraph* gr_diff = new TGraph(npoints);
  
  double x = xmin_common_points;
  for (int i=0; i<npoints; i++) {
    if (x <= xmax_common_points) {
      double diff = gr1->Eval(x, 0, "") - gr2->Eval(x, 0, "S");
      gr_diff->SetPoint(i, x, diff); //printf("X: %f  -  Y: %f\n",x,diff) ;
    }
    else {
      std::cout << "WARNING : Function 'GetIntersectionsOfGraphs': x is outside of the common range of the two graphs! Check evaluation of splines!" << std::endl;
    }
    x += step;
  }
  //printf("end of one channel\n\n");  

  TSpline3* spline_diff = new TSpline3("spline_diff", gr_diff);
  
  // ObsOrExp = type;

  // DrawTSpline(cha, spline_diff, xMinStart, npoints, c, lg3, tmg, step);
  // 

  //__________________________________________________________
  //for (int i=0; i <1000000; i++){
  //  if (fabs(spline_diff->Eval(20.000+i*0.000001)) < 0.0002)
  //  printf("%i -- Position number: %.9f \n",i,spline_diff->Eval(20.000+i*0.000001));
  //}
  //TCanvas *c2 = new TCanvas("","",800,600);
  //c2->cd();
  //spline_diff->Draw();
  //c2->Update();
  //c2->SaveAs("test.pdf");
  //delete c2;
  //__________________________________________________________

  std::vector<double> intersections = FindNullPos(spline_diff, xmin_common_points, xmax_common_points);

  return intersections;
}


std::vector<double> FindNullPos(TSpline3* spline, double min, double max) 
{
  std::vector<double> nullPos;
  double precision = 1e-8;
  double x = (min+max)/2.;
  double x_old = -999.;
  double a = min;
  double b = max;

  while (fabs(x-x_old) > precision) {
    if (spline->Eval(a) * spline->Eval(x) < 0.) {
      b = x;
    }
    else if (spline->Eval(x) * spline->Eval(b) < 0.) {
      a = x;
    }
    else if (spline->Eval(x) == 0.) {
      a = x;
      b = x;
    }
    
    x_old = x;
    x = (a+b)/2.;
  }

  nullPos.push_back(x);

  return nullPos;
}


void DrawTSpline(TString cha = "", TSpline3* spline_diff = nullptr, double xstart = 10.0, int npoints = 500, TCanvas *c = nullptr, TLegend* lg3 = nullptr, TMultiGraph* tmg = nullptr, double step = 0.01)
{
  int totalN = npoints+int(1.0/step);
  cout<<"Total bin: "<<totalN<<endl;

  TGraph* gr_extend = new TGraph(totalN);
  double x = xstart;
  for (int m = 0; m<totalN; m++) {
    gr_extend->SetPoint(m,x,spline_diff->Eval(x));
    x += step;
    if (spline_diff->Eval(x)<0) {
    }
  }

  double lower = TMath::MinElement(totalN,gr_extend->GetY());
  if (lower<0)
    lower = int(lower)-1;
  else lower = int(lower);

  if (!c) {
//    gr_extend->SetLineColor(kGreen);
//    gr_extend->SetLineWidth(1);
//
//    TMultiGraph* extend = new TMultiGraph();
//    extend->Add(gr_extend,"L");
//    extend->Add(gr1,"PL");
//    extend->Add(gr2,"PL");
//
//    TCanvas* c = new TCanvas("c","c",800,600);
//    c->cd();
//    extend->Draw("APL");
//    extend->GetXaxis()->SetLimits(-20,22);
//    extend->GetYaxis()->SetLabelOffset(0.03);
//    double height = 6.0;
//    cout<<"The lower margin: "<<lower<<endl;
//    extend->SetMaximum(height);
//    extend->SetMinimum(lower);
//    TLine* L20 = new TLine(xMaxStart,0,xMaxStart,height);
//    TLine* L15 = new TLine(xMinStart,0,xMinStart,height);
//    TLine* L0 = new TLine(-20,0,22,0);
//    L0->SetLineStyle(8);
//    L0->SetLineWidth(1);
//    L20 ->Draw("same");
//    L15 ->Draw("same");
//    L0 ->Draw("same");
//    c->Update();
//    c->SaveAs("test.pdf");
  }
  else if (c) {
    static int colorNum = 1;
    //    static int growselfL3Y2 = 0;
    gr_extend->SetLineColor(colorNum);
    gr_extend->SetLineWidth(2);
    gr_extend->SetLineStyle(8);

    //tmg->Add(gr_extend,"L");

    c->cd();

    colorNum +=1;
    TString chaName = "";
    if (cha.Contains("com")) chaName = "Combined";
    else if (cha.Contains("bbtautau")) chaName = "b#bar{b}#tau^{+}#tau^{-}";
    else if (cha.Contains("bbbb")) chaName = "b#bar{b}b#bar{b}";
    else if (cha.Contains("bbyy")) chaName = "b#bar{b}#gamma#gamma";
    else chaName = cha;

    lg3->SetY1(lg3->GetY1()-0.02);
    lg3->AddEntry(gr_extend,Form("%s (%s - Theo)",(const char*) ObsOrExp, (const char*) chaName),"L");
  }
}


TGraph* ExtendTGraphByTSpline(TGraph *gr = nullptr)
{
  static int ppp =1; 
  int npoints = gr->GetN();
  cout<<"How many points in the Input TGraph: "<<npoints<<endl;

  double step = 1.0;
  if (npoints>5) {
    step = gr->GetX()[1] - gr->GetX()[0];
  }  

  int AddNum = int(1.0/step);

  if (!ppp) {
   AddNum =10;
   step = 0.1;
  }
  else {
    AddNum =1;
    step =1.0;
  }

  ppp+=1;

  TGraph* extendTGraph = new TGraph(npoints+2*AddNum);
  extendTGraph->SetName( gr->GetName() );

  for (int i = 0; i < npoints; i++) {
    double X = gr->GetX()[i];
    double Y = gr->GetY()[i];
    extendTGraph->SetPoint(i+AddNum,X,Y); 
  }

  TSpline3* spline = new TSpline3("splineHi", gr);  

  for (int j = 0; j<AddNum; j++) {
    double Xm21 = spline->Eval(-21+step*j);
    double Xp21 = spline->Eval(20+step+step*j);
    extendTGraph->SetPoint(0+j,-21+step*j,Xm21);
    extendTGraph->SetPoint(AddNum+npoints+j,20+step+step*j,Xp21);
  }
  
  cout<<"How many points in the output TGraph: "<<extendTGraph->GetN()<<endl;

  return extendTGraph;
}


TGraphAsymmErrors* ExtendTGraphAsymmErrorsByTSpline(TGraphAsymmErrors *gr = nullptr)
{
  static int printTime = 1;

  int npoints = gr->GetN();
  cout<<"How many points in the Input TGraphAsymmErrors: "<<npoints<<endl;

  double step = 1.0;
  int AddNum = 0;

  if (npoints>5) {
    step = gr->GetX()[3] - gr->GetX()[2];
  }

  // hard code
  if (!printTime) { 
    step = 0.1; 
    AddNum = 10;
  }
  else {
    AddNum = 1; 
    step = 1.0;
  }

  cout<<"Step: "<<step<<" AddNum: "<<AddNum<<endl;

  int nPoints = npoints+2*AddNum;

  int npoints_lambda_NLO = gr->GetN();
  double* lambda_NLO_x = gr->GetX();
  double* lambda_NLO_y = gr->GetY();

  // TGraph needed by TSpline
  TGraph* grCentral = new TGraph(npoints, lambda_NLO_x, lambda_NLO_y);
  TGraph* grYHi = new TGraph(npoints);
  TGraph* grYLo = new TGraph(npoints);

  // New TGraph
  TGraphAsymmErrors* extendTGraph = new TGraphAsymmErrors(nPoints);
  extendTGraph->SetName( gr->GetName() );

  for (int i = 0; i < npoints; i++) {
    double X = gr->GetX()[i];
    double Y = gr->GetY()[i];
    double YErrorHi = gr->GetErrorYhigh(i);
    double YErrorLo = gr->GetErrorYlow(i);

    grYHi->SetPoint(i,X,YErrorHi);
    grYLo->SetPoint(i,X,YErrorLo);

    extendTGraph->SetPoint(i+AddNum,X,Y);
    extendTGraph->SetPointEXhigh(i+AddNum,0);
    extendTGraph->SetPointEXlow(i+AddNum,0);

    extendTGraph->SetPointEYhigh(i+AddNum,YErrorHi);
    extendTGraph->SetPointEYlow(i+AddNum,YErrorLo);
  }

  TSpline3* spline1 = new TSpline3("spline1", grCentral);
  TSpline3* spline2 = new TSpline3("spline2", grYHi);
  TSpline3* spline3 = new TSpline3("spline3", grYLo);
 
  if (printTime == 100) {   
    drawTSpline(spline3);
  }

  for (int n = 0; n<AddNum; n++) {
    double xlow = -21.0+step*n;
    double xhigh = 20.0+step*(n+1);
    int binlow = n;
    int binhigh = AddNum+npoints+n;

    double Ym21 = spline1->Eval(xlow);
    double YErrorHim21 = spline2->Eval(xlow);
    double YErrorLom21 = spline3->Eval(xlow);

    double Yp21 = spline1->Eval(xhigh);
    double YErrorHip21 = spline2->Eval(xhigh);
    double YErrorLop21 = spline3->Eval(xhigh);

    extendTGraph->SetPoint      (binlow,xlow,Ym21);
    extendTGraph->SetPointEXhigh(binlow,0);
    extendTGraph->SetPointEXlow (binlow,0);
    extendTGraph->SetPointEYhigh(binlow,YErrorHim21);
    extendTGraph->SetPointEYlow (binlow,YErrorLom21);

    extendTGraph->SetPoint      (binhigh,xhigh,Yp21);
    extendTGraph->SetPointEXhigh(binhigh,0);
    extendTGraph->SetPointEXlow (binhigh,0);
    extendTGraph->SetPointEYhigh(binhigh,YErrorHip21);
    extendTGraph->SetPointEYlow (binhigh,YErrorLop21);
  }

  if (printTime == 1) {
  //    PrintTGraphAsymmErrors(extendTGraph, debug);
  }
  printTime +=1;

  cout<<"How many points in the output TGraphAsymmErrors: "<<extendTGraph->GetN()<<endl;

  return extendTGraph;
}

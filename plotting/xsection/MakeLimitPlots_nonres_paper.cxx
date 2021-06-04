#include <iostream>
#include <string>
#include <fstream>
#include <limits>
#include <map>
#include <tuple>

#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TMultiGraph.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TDatime.h"

#include "./atlasstyle-00-03-05/AtlasStyle.C"
#include "./atlasstyle-00-03-05/AtlasUtils.C"

std::tuple<double, double, double, double, double, double> ReadInputFile (std::string inFile, bool useNominalNPs=false, bool debug=false, bool doSensitivityIncreasePlot=false, bool doResonantMassPoints=false, bool isNanCompatible=false );
std::tuple<double, double, double, double, double, double > ReadInputFile_LimitsFromPaper (std::string inFile, bool debug=false);
void ATLASLabel (Double_t x, Double_t y, const char* text, Color_t color);
void myTextBold(double_t x, double_t y, Color_t color, const char* text, double_t tsize);
void myText(double_t x, double_t y, const char* text, double_t tsize);
void myTextBoldNoNDC(double_t x, double_t y, const char* text, double_t tsize);
void myTextNoNDC(double_t x, double_t y, const char* text, double_t tsize);


std::istream& skipline( std::istream& in )
{
  return in.ignore( std::numeric_limits<std::streamsize>::max(), '\n' );
}

double s2f( std::string n ){
  TString s(n);
  if( s.Contains("nan", TString::kIgnoreCase) ){
    return -999;
  }else{
    return s.Atof();
  }
}

int MakeLimitPlots_nonres_paper(TString base_output = "../../../output/", TString version = "v140invfb_20210531_obs2") 
{
  SetAtlasStyle();

  TString internal = "Internal"; // "Internal" "Preliminary" ""
  bool debug = false;
  bool savePlots = true;
  bool useNominalNPs = false; // nominal or profiled?
  bool drawNumbers = true; // draw expected (and observed) limit values in plot? Set "drawObserved" to true in order to draw also observed limit values.
  bool drawObserved = true; // draw observed limit value in plot?
  bool doSensitivityIncreasePlot = false; // plot limits for individual channels combined step-by-step
  bool doResonantMassPoints = false;
  bool useLimitsFromPaper = false;
  bool conf = false;
  bool statOnly = false;
  
  bool doHepData = false; // IN FACT, no need of hepdata for non-resonant, as aux table records the numbers
  TString hepdatafilename = ""; // will be strOutfile-HEPDATA.root
  TFile* hepdatafile = 0;
  TDirectory* _tmpdir = 0; // for tmp save pwd when swithing to hepdata root file saving operation

  TString strModel = "non-resonant";
  TString strCMSenergy = "13 TeV";
  TString strLumi = "139";

  std::map<TString, bool> useLimitsFromPaperForIndidualChannels;
  useLimitsFromPaperForIndidualChannels["bbbb"] = false;
  useLimitsFromPaperForIndidualChannels["bbtautau"] = false;
  useLimitsFromPaperForIndidualChannels["bbyy"] = false;
  useLimitsFromPaperForIndidualChannels["WWWW"] = false;
  useLimitsFromPaperForIndidualChannels["WWyy"] = false;
  useLimitsFromPaperForIndidualChannels["bbWW"] = false;

  int mass = 400;

  double xmin = 1;
  double xmax = 1000.;

  if (doResonantMassPoints) {
    xmin = 0.1;
    xmax = 50000.;
  }
  else if (doSensitivityIncreasePlot) {
    xmin = 4.;
    xmax = 500.;
  }
  else if (conf) {
    xmin = 0.;
    xmax = 80.;
  }
  else if (statOnly) {
    xmin = 4.;
    xmax = 100000.;
  }

  //______________________________________________
  // construct the plot name
  //______________________________________________
  // appends .pdf, .eps and .png and creates one file for every format
  TString strOutfile = "./limit_plots/";  

  if (strModel.EqualTo("non-resonant")) { //liq add 
    if (conf) {
      if (statOnly) {
	strOutfile.Append(Form("limits_nonres_bbbb_bbtt_bbyy_comb_%s_statOnly_conf_exp", (const char*) version));
      }
      else {
        strOutfile.Append(Form("limits_nonres_bbbb_bbtt_bbyy_comb_%s_conf_exp", (const char*) version));
      }
    }
    else {
      if (statOnly) {
	strOutfile.Append(Form("limits_nonres_bbbb_bbtt_bbyy_comb_%s_statOnly_exp", (const char*) version));
      }
      else {
        strOutfile.Append(Form("limits_nonres_bbbb_bbtt_bbyy_comb_%s_exp", (const char*) version));
      }
    }
  } // liq
  else if (strModel.EqualTo("spin-0")) {
    strOutfile.Append(Form("limits_spin0_%i_bbbb_bbtt_bbyy_vfinal04_exp", mass));
  }

  if (useNominalNPs)
    strOutfile.Append("_nomNP");
  else 
    strOutfile.Append("_profiledNP");
  
  if (drawObserved)
    strOutfile.Append("_obs");

  if (doSensitivityIncreasePlot)
    strOutfile.Append("_sensitivityIncrease");

  TDatime* datetime = new TDatime();
  int date = datetime->GetDate();
  date = date%1000000; //cut first two digits of the year away
  int time = datetime->GetTime();
  std::cout << "Date: " << date << std::endl;

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
  //______________________________________________
  

  std::map<std::string, std::string> inFileNames;

  TString Path = base_output + "/" + version + "/";

  // non-resonant
  if (!doSensitivityIncreasePlot) {
    inFileNames["bbbb"] = Path+"limits/data-files/nonres-bbbb.dat";
    inFileNames["bbtautau"] = Path+"limits/data-files/nonres-bbtautau.dat";
    inFileNames["bbyy"] = Path+"limits/data-files/nonres-bbyy.dat";
    //inFileNames["WWWW"] = Path+"limits/data-files/nonres-WWWW.dat";
    inFileNames["combbig3"] = Path+"limits/data-files/nonres-combined-A-bbtautau_bbyy-nocorr.dat";
    inFileNames["combined"] = Path+"limits/data-files/nonres-combined-A-bbbb_bbtautau_bbyy-nocorr.dat";
  }
  else if (doSensitivityIncreasePlot && !doResonantMassPoints) {
    inFileNames["bbbb"] = "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw/test_output/vfinal_04/limits/data-files/nonres-bbbb.dat";
    inFileNames["bbtautau"] = "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw/test_output/vfinal_04/limits/data-files/nonres-bbtautau.dat";
    inFileNames["combined_bbbb_bbtautau"] = "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw/test_output/vfinal_04/limits/data-files/nonres-combined-A-bbbb_bbtautau-fullcorr.dat";
    inFileNames["combined_bbbb_bbtautau_bbyy"] = "/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw/test_output/vfinal_04/limits/data-files/nonres-combined-A-bbbb_bbtautau_bbyy-fullcorr.dat";
  }
  else {
    inFileNames["bbbb"] = Path+Form("limits/data-files/sensitivityStudySpin0/spin0-bbbb_%i.dat", mass);
    inFileNames["bbtautau"] = Path+Form("limits/data-files/sensitivityStudySpin0/spin0-bbtautau_%i.dat", mass);
    inFileNames["bbyy"] = Path+Form("limits/data-files/sensitivityStudySpin0/spin0-bbyy_%i.dat", mass);
    inFileNames["combined_bbbb_bbtautau"] = Path+Form("limits/data-files/sensitivityStudySpin0/spin0-combined-H3-bbbb_bbtautau-fullcorr_%i.dat", mass);
    inFileNames["combined_bbbb_bbyy"] = Path+Form("limits/data-files/sensitivityStudySpin0/spin0-combined-H3-bbbb_bbyy-fullcorr_%i.dat", mass);
    inFileNames["combined_bbtautau_bbyy"] = Path+Form("limits/data-files/sensitivityStudySpin0/spin0-combined-H3-bbtautau_bbyy-fullcorr_%i.dat", mass);
    inFileNames["combined_bbbb_bbtautau_bbyy"] = Path+Form("limits/data-files/sensitivityStudySpin0/spin0-combined-G3-bbbb_bbtautau_bbyy-fullcorr_%i.dat", mass);
  }

  std::map<std::string, std::string> inFileNames_statOnly;
  inFileNames_statOnly["bbbb"] = Path+"limits/data-files/nonres_statOnly-bbbb.dat";
  inFileNames_statOnly["bbtautau"] = Path+"limits/data-files/nonres_statOnly-bbtautau.dat";
  inFileNames_statOnly["bbyy"] = Path+"limits/data-files/nonres_statOnly-bbyy.dat";




  if (conf)
    inFileNames_statOnly["combined"] = Path+"limits/data-files/nonres_statOnly-combined-A-bbbb_bbtautau_bbyy-fullcorr.dat";
  else
    inFileNames_statOnly["combined"] = Path+"limits/data-files/nonres_statOnly-combined-A-bbbb_bbtautau_bbyy-nocorr.dat";

  std::map< std::string, std::tuple<int, const char*, bool> > coloursAndLegendNames;   
  // Arguments: 1: colour, 2: legend entry string, 3: create +-1/2 sigma bands

  coloursAndLegendNames["bbbb"] = std::make_tuple(kRed, "HH#rightarrow b#bar{b}b#bar{b}", true);
  coloursAndLegendNames["bbtautau"] = std::make_tuple(kBlue, "HH#rightarrow b#bar{b}#tau^{+}#tau^{-}", true);
  coloursAndLegendNames["bbyy"] = std::make_tuple(kOrange, "HH#rightarrow b#bar{b}#gamma#gamma", true); 
  coloursAndLegendNames["WWWW"] = std::make_tuple(kOrange, "HH#rightarrow Multilepton", true); 
  coloursAndLegendNames["WWyy"] = std::make_tuple(kOrange, "HH#rightarrow WW#gamma#gamma", true); 
  coloursAndLegendNames["bbWW"] = std::make_tuple(kOrange, "HH#rightarrow b#bar{b}WW", true); 
  coloursAndLegendNames["combbig3"] = std::make_tuple(kBlack, "b#bar{b}#tau^{+}#tau^{-} + b#bar{b}#gamma#gamma", true);
  coloursAndLegendNames["combined"] = std::make_tuple(kBlack, "All combined", true);

  //for sensitivity increase plots
  if (doSensitivityIncreasePlot && !doResonantMassPoints) {
    coloursAndLegendNames["combined_bbbb_bbtautau"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau", true);
    coloursAndLegendNames["combined_bbbb_bbtautau_bbyy"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau+bb#gamma#gamma", true);
    coloursAndLegendNames["combined_bbbb_bbtautau_bbyy_WWyy_bbWW_WWWW"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau+bb#gamma#gamma+b#bar{b}WW+WWWW+WW#gamma#gamma", true);
  }
  else if (doSensitivityIncreasePlot && doResonantMassPoints) {
    coloursAndLegendNames["combined_bbbb_bbtautau"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau", true);
    coloursAndLegendNames["combined_bbbb_bbyy"] = std::make_tuple(kBlack, "bbbb+bb#gamma#gamma", true);
    coloursAndLegendNames["combined_bbtautau_bbyy"] = std::make_tuple(kBlack, "bb#tau#tau+bb#gamma#gamma", true);
    coloursAndLegendNames["combined_bbbb_bbtautau_bbyy"] = std::make_tuple(kBlack, "bbbb+bb#tau#tau+bb#gamma#gamma", true);
  }

  TString strXaxisTitle = "";
  TString strYaxisTitle = "";
  if (strModel.EqualTo("non-resonant")) {
    strXaxisTitle = "95\% CL upper limit on #sigma_{ggF} (pp #rightarrow HH) normalised to #sigma^{SM}_{ggF}";
    //strXaxisTitle = "95\% CL upper limit on #sigma (pp #rightarrow HH) normalised to #sigma_{SM}";
  }
  else if (strModel.EqualTo("spin-0")) {
    strXaxisTitle = "#sigma (pp #rightarrow S #rightarrow HH) [pb]";
  }

  TCanvas* c1 = new TCanvas("c1", "hh limits", 800, 650);
  c1->SetLogx();
  c1->cd();
  if (!conf)
    c1->SetLogx();
  if (doSensitivityIncreasePlot)
    gPad->SetLeftMargin(0.27);
  else
    gPad->SetLeftMargin(0.22);

  gPad->SetRightMargin(0.05);
  gPad->SetTopMargin(0.05);
  gPad->SetBottomMargin(0.12);
  gStyle->SetOptStat(0);

  // for non-resonant
  std::vector<std::string> channelNames;
  if (!doSensitivityIncreasePlot) {
    channelNames.push_back("bbtautau");
    channelNames.push_back("bbbb");
    channelNames.push_back("bbyy");
    //channelNames.push_back("WWWW");
    channelNames.push_back("combbig3");
    channelNames.push_back("combined");
    assert(channelNames.size() == inFileNames.size());
  }
  else if (doSensitivityIncreasePlot && !doResonantMassPoints) {
    channelNames.push_back("bbbb");
    channelNames.push_back("bbtautau");
    channelNames.push_back("combined_bbbb_bbtautau");
    channelNames.push_back("combined_bbbb_bbtautau_bbyy");
  }
  else {
    channelNames.push_back("bbbb");
    channelNames.push_back("bbtautau");
    channelNames.push_back("bbyy");
    channelNames.push_back("combined_bbbb_bbtautau");
    channelNames.push_back("combined_bbbb_bbyy");
    channelNames.push_back("combined_bbtautau_bbyy");
    channelNames.push_back("combined_bbbb_bbtautau_bbyy");
  }

  std::map<TString, TString> channelRefs;
  channelRefs["bbbb"] = "[arXiv:1804.06174]";
  channelRefs["bbtautau"] = "[CERN-EP-2018-164]";
  channelRefs["bbyy"] = "[CERN-EP-2018-130]";
  channelRefs["WWWW"] = "[xxx]";
  channelRefs["WWyy"] = "[xxx]";
  channelRefs["bbWW"] = "[xxx]";

  int nChannels = inFileNames.size();
  std::cout << "nChannels = " << nChannels << std::endl;

  double* channelYPositions = new double[nChannels];
  double* err_channelYPositions = new double[nChannels];
  double* obs_Xerr = new double[nChannels];

  for (int i=0; i<channelNames.size(); i++) {
      if (inFileNames.find(channelNames[nChannels-i-1]) != inFileNames.end()) {
	channelYPositions[i] = i+0.5;
	err_channelYPositions[i] = 0.5;
	obs_Xerr[i] = 0.0;
      }
  }
 
  std::map<std::string, std::tuple<double, double, double, double, double, double> > limits;  // normalized to SM prediction
  for (std::map<std::string, std::string>::iterator it = inFileNames.begin(); it != inFileNames.end(); ++it) {
    if (useLimitsFromPaper)  
      limits[it->first] = ReadInputFile_LimitsFromPaper(it->second, debug);
    else if ((it->first).find("comb") == std::string::npos && useLimitsFromPaperForIndidualChannels[it->first] == true)   
      limits[it->first] = ReadInputFile_LimitsFromPaper(it->second, debug);
    else
      limits[it->first] = ReadInputFile(it->second, useNominalNPs, debug, doSensitivityIncreasePlot, doResonantMassPoints);
  }
  
  std::map<std::string, std::tuple<double, double, double, double, double, double> > limits_statOnly;  
  // normalized to SM prediction
  if (statOnly) {
    for (std::map<std::string, std::string>::iterator it_statOnly = inFileNames_statOnly.begin(); it_statOnly != inFileNames_statOnly.end(); ++it_statOnly) {
      limits_statOnly[it_statOnly->first] = ReadInputFile(it_statOnly->second, useNominalNPs, debug, doSensitivityIncreasePlot, doResonantMassPoints, true);
	  // isNanCompatible=true for nan compatible mode
    }
  }
  
  double* xsec_m2s = new double[nChannels];
  double* xsec_m1s = new double[nChannels];
  double* xsec_exp = new double[nChannels];
  double* xsec_p1s = new double[nChannels];
  double* xsec_p2s = new double[nChannels];
  double* xsec_obs = new double[nChannels];  

  double* xsec_m2s_statOnly = new double[nChannels];
  double* xsec_m1s_statOnly = new double[nChannels];
  double* xsec_exp_statOnly = new double[nChannels];
  double* xsec_p1s_statOnly = new double[nChannels];
  double* xsec_p2s_statOnly = new double[nChannels];
  double* xsec_obs_statOnly = new double[nChannels];
  // corresponds to xsec_obs_NP_profiled in limit data files

  double ymin = 0.0;
  int nybins = inFileNames.size()+3; //3
  double ymax = nybins;
 
 
  // just for title and Taxis 
  TH1F* hist = new TH1F("hist","hist",1,xmin,xmax);
  // hist->SetTitle("95% C.L. upper limits on #sigma (gg #rightarrow HH) normalized to #sigma_{SM} (gg #rightarrow HH)");
  hist->SetTitleSize(0.09);
  hist->SetMinimum(ymin);
  hist->SetMaximum(ymax);
  hist->SetTitle(0);
  hist->SetLineColor(kWhite);
  hist->GetYaxis()->Set(nybins,ymin,ymax);
  hist->GetYaxis()->SetNdivisions(110);
//  hist->GetYaxis()->SetTickSize(0);
  hist->GetYaxis()->SetTickLength(0.015);
  hist->GetXaxis()->SetTickLength(0.02);
  hist->GetXaxis()->SetTitle(strXaxisTitle);
  if (conf)
    hist->GetYaxis()->SetLabelSize(0.06);
  else
    hist->GetYaxis()->SetLabelSize(0.05);
  hist->GetXaxis()->SetLabelSize(0.04);
  hist->GetXaxis()->SetTitleSize(0.04); //0.047
  hist->GetXaxis()->SetNdivisions(510);
  if (conf)
    hist->GetXaxis()->SetTitleOffset(1.15);
  else
    hist->GetXaxis()->SetTitleOffset(1.25);

  c1->cd();
  for (int i = 0; i < channelNames.size(); i++) {
    hist->GetYaxis()->SetBinLabel(i+1, std::get<1>(coloursAndLegendNames[channelNames.at(nChannels-i-1)]));
    //hist->GetYaxis()->SetBinLabel(i+1, "L"); // looks like if latex elements enter, the extra pixels show up
//    hist->GetYaxis()->SetBinLabel(i+1, "");
  }
  
  //hist->GetYaxis()->LabelsOption("a");
  //hist->GetYaxis()->CenterLabels("kTRUE");
  hist->Draw("AXIS");

  //double allLebalX = -5;
  //for (int i = 0; i < channelNames.size(); i++) {
  //  cout<<"Label: "<<std::get<1>(coloursAndLegendNames[channelNames.at(nChannels-i-1)])<<endl;
  //  const char* labels= std::get<1>(coloursAndLegendNames[channelNames.at(nChannels-i-1)]);
  //  myTextNoNDC(allLebalX,i,labels, 0.05);
  //}

  double fiddly_minus_offset = -0.1;
  
  for (int i=0; i < nChannels; i++) {  
    if (debug) {
      std::cout << "i = " << i << std::endl;
      std::cout << "Storing values in arrays for channel " << channelNames[i] << std::endl;
    }
    
    xsec_m2s[nChannels-i-1] = std::get<0>(limits[channelNames[i]]);
    xsec_m1s[nChannels-i-1] = std::get<1>(limits[channelNames[i]]);
    xsec_exp[nChannels-i-1] = std::get<2>(limits[channelNames[i]]);
    xsec_p1s[nChannels-i-1] = std::get<3>(limits[channelNames[i]]);
    xsec_p2s[nChannels-i-1] = std::get<4>(limits[channelNames[i]]);
    xsec_obs[nChannels-i-1] = std::get<5>(limits[channelNames[i]]);

    if (statOnly) {
      xsec_m2s_statOnly[nChannels-i-1] = std::get<0>(limits_statOnly[channelNames[i]]);
      xsec_m1s_statOnly[nChannels-i-1] = std::get<1>(limits_statOnly[channelNames[i]]);
      xsec_exp_statOnly[nChannels-i-1] = std::get<2>(limits_statOnly[channelNames[i]]);
      xsec_p1s_statOnly[nChannels-i-1] = std::get<3>(limits_statOnly[channelNames[i]]);
      xsec_p2s_statOnly[nChannels-i-1] = std::get<4>(limits_statOnly[channelNames[i]]);
      xsec_obs_statOnly[nChannels-i-1] = std::get<5>(limits_statOnly[channelNames[i]]);
    }    

    if (debug) {
      std::cout << "xsec_m2s[nChannels-i-1] = " << xsec_m2s[nChannels-i-1] << std::endl;
      std::cout << "xsec_m1s[nChannels-i-1] = " << xsec_m1s[nChannels-i-1] << std::endl;
      std::cout << "xsec_exp[nChannels-i-1] = " << xsec_exp[nChannels-i-1] << std::endl;
      std::cout << "xsec_p1s[nChannels-i-1] = " << xsec_p1s[nChannels-i-1] << std::endl;
      std::cout << "xsec_p2s[nChannels-i-1] = " << xsec_p2s[nChannels-i-1] << std::endl;
      std::cout << "xsec_obs[nChannels-i-1] = " << xsec_obs[nChannels-i-1] << std::endl;

      if (statOnly) {
      std::cout << "xsec_m2s_statOnly[nChannels-i-1] = " << xsec_m2s_statOnly[nChannels-i-1] << std::endl;
      std::cout << "xsec_m1s_statOnly[nChannels-i-1] = " << xsec_m1s_statOnly[nChannels-i-1] << std::endl;
      std::cout << "xsec_exp_statOnly[nChannels-i-1] = " << xsec_exp_statOnly[nChannels-i-1] << std::endl;
      std::cout << "xsec_p1s_statOnly[nChannels-i-1] = " << xsec_p1s_statOnly[nChannels-i-1] << std::endl;
      std::cout << "xsec_p2s_statOnly[nChannels-i-1] = " << xsec_p2s_statOnly[nChannels-i-1] << std::endl;
      std::cout << "xsec_obs_statOnly[nChannels-i-1] = " << xsec_obs_statOnly[nChannels-i-1] << std::endl;
      }
    }
        
    TString stringExp = Form("%.2f", xsec_exp[nChannels-i-1]); // .1f -> .0f for paper
    TString stringExp_statOnly = "";
    if (statOnly)
      stringExp_statOnly = Form("%.0f", xsec_exp_statOnly[nChannels-i-1]); // .1f -> .0f for paper
	if (statOnly && (channelNames[i] == "combined") )
	  stringExp_statOnly = Form("%.1f", xsec_exp_statOnly[nChannels-i-1]);

    TString stringObs = Form("%.1f", xsec_obs[nChannels-i-1]);
    TString stringChannelRefs = "";
    if (useLimitsFromPaper) {
      if (channelNames[i] == "WWyy" || channelNames[i] == "bbyy") {
	stringExp = Form("%.0f", xsec_exp[nChannels-i-1]);
	stringObs = Form("%.0f", xsec_obs[nChannels-i-1]);
	if (statOnly)
	  stringExp_statOnly = Form("%.0f", xsec_exp_statOnly[nChannels-i-1]);
      }
    }

    if (channelNames[i] == "bbyy" && useLimitsFromPaperForIndidualChannels["bbyy"] == true) {
      stringExp = Form("%.0f", xsec_exp[nChannels-i-1]);
      stringObs = Form("%.0f", xsec_obs[nChannels-i-1]); 
	if (statOnly)
	  stringExp_statOnly = Form("%.0f", xsec_exp_statOnly[nChannels-i-1]);
    }

    if (!doSensitivityIncreasePlot && !doResonantMassPoints) {
      stringChannelRefs = channelRefs[channelNames[i]];
    }

    if (doSensitivityIncreasePlot && doResonantMassPoints) {
      stringExp = Form("%.3f", xsec_exp[nChannels-i-1]);
      stringObs = Form("%.3f", xsec_obs[nChannels-i-1]);
	if (statOnly)
	  stringExp_statOnly = Form("%.3f", xsec_exp_statOnly[nChannels-i-1]);
    }

	// use 3 digits, thus less sensitive channels, reduce digits
	if( channelNames[i] == "WWyy" || channelNames[i] == "WWWW" || channelNames[i] == "bbWW" ){
	// round to multiple of 10, i.e. 122 -> 120
	// except bbWW exp 304.7 and obs 305.2 !
	  if( channelNames[i] != "bbWW" ){
	    xsec_exp[nChannels-i-1] = round(xsec_exp[nChannels-i-1]/10)*10;
	    xsec_obs[nChannels-i-1] = round(xsec_obs[nChannels-i-1]/10)*10;
	  }
	  if( channelNames[i] != "WWWW" ){ // WWWW before rouding has only 2 digits before decimal point
	    xsec_exp_statOnly[nChannels-i-1] = round(xsec_exp_statOnly[nChannels-i-1]/10)*10;
   	  }
      stringExp = Form("%.0f", xsec_exp[nChannels-i-1]);
      stringExp_statOnly = Form("%.0f", xsec_exp_statOnly[nChannels-i-1]);
      stringObs = Form("%.0f", xsec_obs[nChannels-i-1]);
	}

    // The numbers in the plot
    // channel references
    if (useLimitsFromPaper) {
      if (channelNames[i] == "bbbb")
	myText(0.037, 0.125+(nChannels-i-1)*0.111, stringChannelRefs , 0.027);
      else
	myText(0.016, 0.125+(nChannels-i-1)*0.111, stringChannelRefs , 0.027);
    }

    if (drawNumbers && drawObserved) {
      if (statOnly) {
	if (conf) {
	  if (channelNames[i] == "combined") {
	    myTextNoNDC(54.6, nChannels-i-0.5, stringObs , 0.035);
	    myTextNoNDC(63, nChannels-i-0.5, stringExp , 0.035);
	    myTextNoNDC(72.5, nChannels-i-0.5, stringExp_statOnly , 0.035);
	  }
	  else {
	    myTextNoNDC(54, nChannels-i-0.5, stringObs , 0.035);
	    myTextNoNDC(63, nChannels-i-0.5, stringExp , 0.035);
	    myTextNoNDC(73, nChannels-i-0.5, stringExp_statOnly , 0.035);
	  }
	}
	// "usual" plot
	else {
	  if (channelNames[i] == "WWyy" || channelNames[i] == "bbWW") {
	    myTextNoNDC(2300, nChannels-i-0.5, stringObs , 0.035);
	    myTextNoNDC(6900, nChannels-i-0.5, stringExp , 0.035);
	    myTextNoNDC(30000, nChannels-i-0.5, stringExp_statOnly , 0.035);
	  }
	  else if (channelNames[i] == "WWWW") {
	    myTextNoNDC(2300, nChannels-i-0.5, stringObs , 0.035);
	    myTextNoNDC(6900, nChannels-i-0.5, stringExp , 0.035);
	    myTextNoNDC(33000, nChannels-i-0.5, stringExp_statOnly , 0.035);
	  }
	  else if (channelNames[i] == "combined") {
	    myTextNoNDC(2400, nChannels-i-0.5, stringObs , 0.035);
	    myTextNoNDC(7500, nChannels-i-0.5, stringExp , 0.035);
	    myTextNoNDC(32000, nChannels-i-0.5, stringExp_statOnly , 0.035);
	  }
	  else {
	    myTextNoNDC(2200, nChannels-i-0.5, stringObs , 0.035);
	    myTextNoNDC(7500, nChannels-i-0.5, stringExp , 0.035);
	    myTextNoNDC(33000, nChannels-i-0.5, stringExp_statOnly , 0.035);
	  }
	}
      }
      else if (doSensitivityIncreasePlot) {
	if ((channelNames[i] == "bbbb") || (channelNames[i] == "bbtautau")) {
	  myTextNoNDC(xmin+(0.44+fiddly_minus_offset)*((xmax/2.35)-xmin), (ymin/2)+(ymax-ymin)*0.053+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringObs , 0.04);
	  myTextNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+1.7*((xmax/3.5)-xmin), (ymin/2)+(ymax-ymin)*0.053+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringExp , 0.04);
	}
        else {
	  myTextNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/3.)-xmin), (ymin/2)+(ymax-ymin)*0.053+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringObs , 0.04);
	  myTextNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+1.7*((xmax/3.5)-xmin), (ymin/2)+(ymax-ymin)*0.053+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringExp , 0.04);
	}
      }
      else if (useLimitsFromPaper) {
	if (channelNames[i] == "WWyy") {
	  myTextNoNDC(xmin+(0.45+fiddly_minus_offset)*((xmax/30.)-xmin), (ymin/2)+(ymax-ymin)*0.02+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringObs , 0.04);
	  myTextNoNDC(xmin+(0.3+fiddly_minus_offset)*((xmax/30.)-xmin)+1.1*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.02+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringExp , 0.04);
	}
        else {
	  myTextNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin), (ymin/2)+(ymax-ymin)*0.02+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringObs , 0.04);
	  myTextNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+1.4*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.02+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringExp , 0.04);
	}
      }

      else {
	// modified since CONF, used for paper with only the three most sensitive channels (4b, bbtautau, bbyy)
	if (conf) {
	  if ((channelNames[i] == "WWyy") || (channelNames[i] == "bbWW")) {
	    myTextNoNDC(xmin+(0.442+fiddly_minus_offset)*((xmax/30.)-xmin),                        (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringObs , 0.04);
	    myTextNoNDC(xmin+(0.3+fiddly_minus_offset)*((xmax/30.)-xmin)+1.1535*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringExp , 0.04);
	  }
	  else if (channelNames[i] == "combined") {
	    //myTextNoNDC(xmin+(0.675+fiddly_minus_offset)*((xmax/30.)-xmin),                      (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringObs , 0.04);
	    //myTextNoNDC(xmin+(0.54+fiddly_minus_offset)*((xmax/30.)-xmin)+1.4*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringExp , 0.04);
	    myTextNoNDC(xmin+55.5+(0.7+fiddly_minus_offset)*((xmax/30.)-xmin),                      (ymin/2)+(ymax-ymin)*0.012+0.42+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringObs , 0.04);
	    myTextNoNDC(xmin+57+(0.54+fiddly_minus_offset)*((xmax/30.)-xmin)+1.4*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.012+0.42+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringExp , 0.04);
	  }
	  else {
	    //myTextNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin),                       (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringObs , 0.04);
	    //myTextNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+1.4*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringExp , 0.04);
	    myTextNoNDC(xmin+55+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin),                       (ymin/2)+(ymax-ymin)*0.012+0.42+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringObs , 0.04);
	    myTextNoNDC(xmin+57+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+1.4*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.012+0.42+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringExp , 0.04);
	  }
	}
	// not CONF, all 6 channels
	else {
	  if ((channelNames[i] == "WWyy") || (channelNames[i] == "bbWW") || (channelNames[i] == "WWWW")) {
	    myTextNoNDC(xmin+4.25*(0.442+fiddly_minus_offset)*((xmax/30.)-xmin),                        (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-0.6)/nybins*(ymax-ymin)), stringObs , 0.04);
	    myTextNoNDC(xmin+(0.3+fiddly_minus_offset)*((xmax/30.)-xmin)+2.85*1.1535*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-0.6)/nybins*(ymax-ymin)), stringExp , 0.04);
	  }
	  else if (channelNames[i] == "combined") {
	    myTextNoNDC(xmin+3.1*(0.675+fiddly_minus_offset)*((xmax/30.)-xmin),                      (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-0.6)/nybins*(ymax-ymin)), stringObs , 0.04);
	    myTextNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+3.5*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-0.6)/nybins*(ymax-ymin)), stringExp , 0.04);
	  }
	  else {
	    myTextNoNDC(xmin+3.5*(0.55+fiddly_minus_offset)*((xmax/30.)-xmin),                       (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-0.6)/nybins*(ymax-ymin)), stringObs , 0.04);
	    myTextNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+3.5*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.012+((double)(nChannels-i-0.6)/nybins*(ymax-ymin)), stringExp , 0.04);
	  } 
	}
      }
    }
    else if (drawNumbers && !drawObserved) {
      myTextNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+1.4*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.01+((double)(nChannels-i-1)/nybins*(ymax-ymin)), stringExp , 0.04);
    }

    if (debug) {
      std::cout << "Before creating new TGraphAsymmErrors: nChannels = " << nChannels << std::endl;
      std::cout << "Before creating new TGraphAsymmErrors: xsec_exp[nChannels-i] = " << xsec_exp[nChannels-i] << std::endl;
    }
  }
  
  if (drawNumbers && drawObserved) {
    if (statOnly) {
      if (conf) {
	//myTextBoldNoNDC(55,(ymin/2)+(ymax-ymin)*0.005+((double)(nChannels)/nybins*(ymax-ymin)), "Obs.", 0.035);
	//myTextBoldNoNDC(63,(ymin/2)+(ymax-ymin)*0.005+((double)(nChannels)/nybins*(ymax-ymin)), "Exp.", 0.035);
	//myTextBoldNoNDC(73,(ymin/2)+(ymax-ymin)*0.005+((double)(nChannels)/nybins*(ymax-ymin)), "Exp. stat.", 0.035);
	myTextBoldNoNDC(54,nChannels+0.05, "Obs.", 0.035);
	myTextBoldNoNDC(63,nChannels+0.05, "Exp.", 0.035);
	myTextBoldNoNDC(73,nChannels+0.05, "Exp. stat.", 0.035);
	//      myTextBoldNoNDC(xmin+(0.30 + fiddly_minus_offset)*((xmax/200.)-xmin),                        (ymin/2)+(ymax-ymin)*0.005+((double)(nChannels)/nybins*(ymax-ymin)), "obs.", 0.04);
	//      myTextBoldNoNDC(xmin+(0.25 + fiddly_minus_offset)*((xmax/200.)-xmin)+1.4*((xmax/190.)-xmin), (ymin/2)+(ymax-ymin)*0.005+((double)(nChannels)/nybins*(ymax-ymin)), "exp.", 0.04);
	//      myTextBoldNoNDC(xmin+(0.25 + fiddly_minus_offset)*((xmax/200.)-xmin)+1.4*((xmax/30.)-xmin),  (ymin/2)+(ymax-ymin)*0.005+((double)(nChannels)/nybins*(ymax-ymin)), "exp. stat.", 0.04);
      }
      else {
	myTextBoldNoNDC(2200,nChannels+0.05, "Obs.", 0.035);
	myTextBoldNoNDC(7000,nChannels+0.05, "Exp.", 0.035);
	myTextBoldNoNDC(30000,nChannels+0.05, "Exp. stat.", 0.035);
      }
    }
    else if (doSensitivityIncreasePlot) {
      myTextBoldNoNDC(xmin+(0.45+fiddly_minus_offset)*((xmax/2.35)-xmin), (ymin/2)+(ymax-ymin)*0.005+((double)(nChannels)/nybins*(ymax-ymin))+0.02, "Obs.", 0.04);
      myTextBoldNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+1.7*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.005+((double)(nChannels)/nybins*(ymax-ymin))+0.02, "Exp.", 0.04);
    }
    else {
      if (conf) {
	myTextBoldNoNDC(xmin+52+3.5*(0.55+fiddly_minus_offset)*((xmax/30.)-xmin), (ymin/2)+(ymax-ymin)*0.005+0.42+((double)(nChannels)/nybins*(ymax-ymin))+0.02, "Obs.", 0.04);
	myTextBoldNoNDC(xmin+40+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+3.5*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.005+0.42+((double)(nChannels)/nybins*(ymax-ymin))+0.02, "Exp.", 0.04);
      }
      else {
	myTextBoldNoNDC(xmin+3.5*(0.55+fiddly_minus_offset)*((xmax/30.)-xmin), (ymin/2)+(ymax-ymin)*0.005+((double)(nChannels)/nybins*(ymax-ymin))+0.02, "Obs.", 0.04);
	myTextBoldNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+3.5*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.005+((double)(nChannels)/nybins*(ymax-ymin))+0.02, "Exp.", 0.04);
      }
    }
  }
  else if (drawNumbers && !drawObserved) {
    myTextBoldNoNDC(xmin+(0.55+fiddly_minus_offset)*((xmax/30.)-xmin)+1.4*((xmax/10.)-xmin), (ymin/2)+(ymax-ymin)*0.005+((double)(nChannels)/nybins*(ymax-ymin)), "exp.", 0.05);
  }

  //gStyle->SetEndErrorSize(0.);

  // The real thing
  TMultiGraph* mg = new TMultiGraph();
  mg->SetName("limits");

  TGraphAsymmErrors* limit_graph_1s = new TGraphAsymmErrors(nChannels, xsec_exp, channelYPositions, xsec_m1s, xsec_p1s, err_channelYPositions, err_channelYPositions);
  TGraphAsymmErrors* limit_graph_2s = new TGraphAsymmErrors(nChannels, xsec_exp, channelYPositions, xsec_m2s, xsec_p2s, err_channelYPositions, err_channelYPositions);
  TGraphAsymmErrors* limit_obs = new TGraphAsymmErrors(nChannels, xsec_obs, channelYPositions, obs_Xerr, obs_Xerr, err_channelYPositions, err_channelYPositions);
  TGraphAsymmErrors* limit_exp = new TGraphAsymmErrors(nChannels, xsec_exp, channelYPositions, obs_Xerr, obs_Xerr, err_channelYPositions, err_channelYPositions);
  limit_graph_1s->SetName("exp_1s");
  limit_graph_2s->SetName("exp_2s");
  limit_obs->SetName("obs");
  limit_exp->SetName("exp");
  
  limit_graph_2s->SetLineColor(kYellow);
  limit_graph_2s->SetFillColor(kYellow);
  
  limit_graph_1s->SetLineColor(kGreen);
  limit_graph_1s->SetFillColor(kGreen);
  
  //limit_graph_2s->Draw("E2");
  //limit_graph_1s->Draw("SAME E2");

  limit_exp->SetLineStyle(2);
  limit_exp->SetLineWidth(2);
  limit_exp->SetMarkerSize(0);
  limit_exp->SetMarkerStyle(24);
  //limit_exp->Draw("same E0");

  mg->Add(limit_graph_2s,"E2");
  mg->Add(limit_graph_1s,"E2");
  mg->Add(limit_exp, "E");

  if (drawObserved) {
    limit_obs->SetMarkerColor(1);
    limit_obs->SetMarkerStyle(20);
    limit_obs->SetMarkerSize(1.2);
    limit_obs->SetLineWidth(2);
    mg->Add(limit_obs,"PE");
    //limit_obs->Draw("SAME p E");
  }
 
  mg->Draw("P");


  if( doHepData ){
    std::cout << "HEPDATA : mg" << std::endl;
	_tmpdir = gDirectory;
	hepdatafile->cd();
	mg->Write();
	_tmpdir->cd();
  }


  //mg->GetHistogram()->GetXaxis()->SetLimits(xmin,xmax);

  //xaxis->Draw("sameaxis");
  gPad->RedrawAxis();

  // The legend 
  TLegend* leg;
  if (doSensitivityIncreasePlot)
    leg = new TLegend(0.7, 0.76+0.002*nChannels, 0.99, 0.92);
  else if (useLimitsFromPaper)
    leg = new TLegend(0.67, 0.82+0.002*nChannels, 0.99, 0.93);
  else
    leg = new TLegend(0.64, 0.76+0.002*nChannels, 0.99, 0.92);

  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->SetTextFont(42); // default non-bold

  if (drawObserved)
    leg->AddEntry(limit_obs, "Observed", "p l");
  leg->AddEntry(limit_exp, "Expected", "l");
  leg->AddEntry(limit_graph_1s, "Expected #pm 1#sigma", "F");
  leg->AddEntry(limit_graph_2s, "Expected #pm 2#sigma", "F");   
  leg->Draw();
  
  TLine* line1 = new TLine(1., -0.5, 1., nChannels+0.5);
  line1->SetLineWidth(2);
  line1->SetLineStyle(2);
  line1->SetLineColor(kBlack);
  //line1->Draw("SAME L");

  TLine* lineUp = new TLine(xmin, nChannels+0.5, xmax, nChannels+0.5);
  lineUp->SetLineWidth(1);
  lineUp->SetLineColor(kBlack);
  //lineUp->Draw("SAME L");

  if (!doSensitivityIncreasePlot) {
    TLine* lineDown = new TLine(xmin, 2.0, xmax, 2.0);
    lineDown->SetLineWidth(2);
    lineDown->SetLineStyle(2);
    lineDown->SetLineColor(kBlack);
    lineDown->Draw("SAME L");
  }

  if (doSensitivityIncreasePlot)
    ATLASLabel(0.30, 0.87+0.002*nChannels, internal, kBlack);
  else
    ATLASLabel(0.27, 0.87+0.002*nChannels, internal, kBlack);

  TLatex L;
  L.SetNDC();
  if (useLimitsFromPaper)
    L.SetTextSize(0.04);
  else
     L.SetTextSize(0.035);
  L.SetTextFont(42);
  if (doSensitivityIncreasePlot)
    L.DrawLatex(0.30, 0.82+0.0025*nChannels, Form("#sqrt{s} = %s,  %s fb^{-1}", (const char*) strCMSenergy, (const char*) strLumi));
  else
    L.DrawLatex(0.27, 0.82+0.0025*nChannels, Form("#sqrt{s} = %s,  %s fb^{-1}", (const char*) strCMSenergy, (const char*) strLumi));

  TLatex l;
  l.SetNDC();
  l.SetTextSize(0.04);
  l.SetTextFont(42);
  // if (doSensitivityIncreasePlot && !doResonantMassPoints)
  // l.DrawLatex(0.29, 0.77+0.002*nChannels, (const char*) strModel);
  if (doSensitivityIncreasePlot && doResonantMassPoints)
    l.DrawLatex(0.29, 0.78+0.002*nChannels, Form("%s,  %i GeV", (const char*) strModel, mass));
  //else
    //l.DrawLatex(0.24, 0.72+0.002*nChannels, (const char*) strModel);

  TLatex a;
  a.SetNDC();
  a.SetTextFont(42);
  if (useLimitsFromPaper) {
    a.SetTextSize(0.03);
    a.DrawLatex(0.24, 0.78, "#sigma_{SM} (pp #rightarrow HH) = 33.49 fb");
  }
  else {
    a.SetTextSize(0.035);
    if (conf)
      a.DrawLatex(0.27, 0.778, "#sigma^{SM}_{ggF} (pp #rightarrow HH) = 33.5 fb");
    else
      a.DrawLatex(0.30, 0.778, "#sigma^{SM}_{ggF} (pp #rightarrow HH) = 31.05 fb");
      // a.DrawLatex(0.24, 0.807, "#sigma_{SM} (gg #rightarrow HH) = 33.41 fb");
      //a.DrawLatex(0.24, 0.807, "#sigma_{SM} (pp #rightarrow HH) = 33.41 fb");
  }
  
  TLatex A;
  A.SetNDC();
  A.SetTextFont(42);
  if (useLimitsFromPaper) {
    A.SetTextSize(0.03);
//    A.DrawLatex(0.52, 0.76, "#splitline{[Phys. Rev. Lett. 117 (2016) 012001]}{[Phys. Rev. Lett. 117 (2016) 079901]  (Err.)}");
  }
  else {
    A.SetTextSize(0.025);
//    if (conf)
//      A.DrawLatex(0.50, 0.76, "#splitline{[Phys. Rev. Lett. 117 (2016) 012001]}{[Phys. Rev. Lett. 117 (2016) 079901]  (Err.)}");
//    else
//      A.DrawLatex(0.47, 0.79, "#splitline{[Phys. Rev. Lett. 117 (2016) 012001]}{[Phys. Rev. Lett. 117 (2016) 079901]  (Err.)}");
  }

  c1->Update();

  if (savePlots) {
    c1->SaveAs(Form("%s.pdf", (const char*) strOutfile));
//    c1->SaveAs(Form("%s.eps", (const char*) strOutfile));
//    c1->SaveAs(Form("%s.png", (const char*) strOutfile));
  }

  if( doHepData ){
    hepdatafile->Close();
  }

  return 0;
}


std::tuple<double, double, double, double, double, double> ReadInputFile (std::string inFileName, bool useNominalNPs, bool debug, bool doSensitivityIncreasePlot, bool doResonantMassPoints, bool isNanCompatible ) {
  // returns limits normalized to SM
  std::cout << "Reading in file " << inFileName << std::endl;

  double SM_HH_xsec = 31.05;

  double xsec_m2s = 0.;
  double xsec_m1s = 0.;
  double xsec_exp = 0.;
  double xsec_p1s = 0.;
  double xsec_p2s = 0.;
  double xsec_obs = 0.;

  std::tuple<double, double, double, double, double, double> limits;

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
    std::cerr << "ERROR : Function 'ReadInputFile': File could not be opened: " << inFileName << std::endl;
    assert(0);
  }
  
  file >> skipline;
  while (!file.eof()) {
    if( isNanCompatible ){ // able to take nan
      file >> mass >> scaling 
	   >> s_mu_m2s_NP_nominal >> s_mu_m1s_NP_nominal >> s_mu_exp_NP_nominal >> s_mu_p1s_NP_nominal >> s_mu_p2s_NP_nominal >> s_mu_obs_NP_nominal 
	   >> s_xsec_m2s_NP_nominal >> s_xsec_m1s_NP_nominal >> s_xsec_exp_NP_nominal >> s_xsec_p1s_NP_nominal >> s_xsec_p2s_NP_nominal >> s_xsec_obs_NP_nominal 
	   >> s_mu_m2s_NP_profiled >> s_mu_m1s_NP_profiled >> s_mu_exp_NP_profiled >> s_mu_p1s_NP_profiled >> s_mu_p2s_NP_profiled >> s_mu_obs_NP_profiled 
	   >> s_xsec_m2s_NP_profiled >> s_xsec_m1s_NP_profiled >> s_xsec_exp_NP_profiled >> s_xsec_p1s_NP_profiled >> s_xsec_p2s_NP_profiled >> s_xsec_obs_NP_profiled 
	   >> skipline;
    }
    else{ // normally
      file >> mass >> scaling 
	   >> mu_m2s_NP_nominal >> mu_m1s_NP_nominal >> mu_exp_NP_nominal >> mu_p1s_NP_nominal >> mu_p2s_NP_nominal >> mu_obs_NP_nominal 
	   >> xsec_m2s_NP_nominal >> xsec_m1s_NP_nominal >> xsec_exp_NP_nominal >> xsec_p1s_NP_nominal >> xsec_p2s_NP_nominal >> xsec_obs_NP_nominal 
	   >> mu_m2s_NP_profiled >> mu_m1s_NP_profiled >> mu_exp_NP_profiled >> mu_p1s_NP_profiled >> mu_p2s_NP_profiled >> mu_obs_NP_profiled 
	   >> xsec_m2s_NP_profiled >> xsec_m1s_NP_profiled >> xsec_exp_NP_profiled >> xsec_p1s_NP_profiled >> xsec_p2s_NP_profiled >> xsec_obs_NP_profiled 
	   >> skipline;
    }
  }
  
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
    if (debug) {
      std::cout << "Nominal NP limits read in from file " << inFileName << std::endl;
      std::cout << "xsec_m2s_NP_nominal = " << xsec_m2s_NP_nominal << std::endl;
      std::cout << "xsec_m1s_NP_nominal = " << xsec_m1s_NP_nominal << std::endl;
      std::cout << "xsec_exp_NP_nominal = " << xsec_exp_NP_nominal << std::endl;
      std::cout << "xsec_p1s_NP_nominal = " << xsec_p1s_NP_nominal << std::endl;
      std::cout << "xsec_p2s_NP_nominal = " << xsec_p2s_NP_nominal << std::endl;
      std::cout << "xsec_obs_NP_profiled = " << xsec_obs_NP_profiled << std::endl;
    }  
    xsec_m2s = xsec_m2s_NP_nominal / (SM_HH_xsec/1000.);
    xsec_m1s = xsec_m1s_NP_nominal / (SM_HH_xsec/1000.);
    xsec_exp = xsec_exp_NP_nominal / (SM_HH_xsec/1000.);
    xsec_p1s = xsec_p1s_NP_nominal / (SM_HH_xsec/1000.);
    xsec_p2s = xsec_p2s_NP_nominal / (SM_HH_xsec/1000.);
    xsec_obs = xsec_obs_NP_profiled / (SM_HH_xsec/1000.);
  }  
  else {
    if (debug) {
      std::cout << "Profiled NP limits read in from file " << inFileName << std::endl;
      std::cout << "xsec_m2s_NP_profiled = " << xsec_m2s_NP_profiled << std::endl;
      std::cout << "xsec_m1s_NP_profiled = " << xsec_m1s_NP_profiled << std::endl;
      std::cout << "xsec_exp_NP_profiled = " << xsec_exp_NP_profiled << std::endl;
      std::cout << "xsec_p1s_NP_profiled = " << xsec_p1s_NP_profiled << std::endl;
      std::cout << "xsec_p2s_NP_profiled = " << xsec_p2s_NP_profiled << std::endl;
      std::cout << "xsec_obs_NP_profiled = " << xsec_obs_NP_profiled << std::endl;
    } 
    xsec_m2s = xsec_m2s_NP_profiled / (SM_HH_xsec/1000.);
    xsec_m1s = xsec_m1s_NP_profiled / (SM_HH_xsec/1000.);
    xsec_exp = xsec_exp_NP_profiled / (SM_HH_xsec/1000.);
    xsec_p1s = xsec_p1s_NP_profiled / (SM_HH_xsec/1000.);
    xsec_p2s = xsec_p2s_NP_profiled / (SM_HH_xsec/1000.);
    xsec_obs = xsec_obs_NP_profiled / (SM_HH_xsec/1000.);
  }  
		   
  if (debug) {
    std::cout << "Normalised to SM using sigma = " << SM_HH_xsec << std::endl;
    std::cout << "xsec_m2s = " << xsec_m2s << std::endl;
    std::cout << "xsec_m1s = " << xsec_m1s << std::endl;
    std::cout << "xsec_exp = " << xsec_exp << std::endl;
    std::cout << "xsec_p1s = " << xsec_p1s << std::endl;
    std::cout << "xsec_p2s = " << xsec_p2s << std::endl;
    std::cout << "xsec_obs = " << xsec_obs << std::endl;
  }  

  limits = std::make_tuple(xsec_m2s, xsec_m1s, xsec_exp, xsec_p1s, xsec_p2s, xsec_obs);  
  
  file.close();

  return limits;
}


std::tuple<double, double, double, double,  double, double> ReadInputFile_LimitsFromPaper (std::string inFileName, bool debug) 
{
  // returns limits normalized to SM
  std::cout << "Reading in file " << inFileName << std::endl;

  int mass = 0.;
  double xsec_m2s = 0.;
  double xsec_m1s = 0.;
  double xsec_exp = 0.;
  double xsec_p1s = 0.;
  double xsec_p2s = 0.;
  double xsec_obs = 0.;

  std::tuple<double, double, double, double,  double, double> limits;

  fstream file (inFileName, ios::in);
  if (!file.good()) {
    std::cerr << "ERROR : Function 'ReadInputFile': File could not be opened!" << std::endl;
  }
  
  file >> skipline;
  while (!file.eof()) {
    file >> mass >> xsec_m2s >> xsec_m1s >> xsec_exp >> xsec_p1s >> xsec_p2s >> xsec_obs;
  }    

  if (debug) {
    std::cout << "mass = " << mass << std::endl;
    std::cout << "xsec_m2s = " << xsec_m2s << std::endl;
    std::cout << "xsec_m1s = " << xsec_m1s << std::endl;
    std::cout << "xsec_exp = " << xsec_exp << std::endl;
    std::cout << "xsec_p1s = " << xsec_p1s << std::endl;
    std::cout << "xsec_p2s = " << xsec_p2s << std::endl;
    std::cout << "xsec_obs = " << xsec_obs << std::endl;
  }  

  limits = std::make_tuple(xsec_m2s, xsec_m1s, xsec_exp, xsec_p1s, xsec_p2s, xsec_obs);  
  
  file.close();

  return limits;
}


void ATLASLabel (Double_t x, Double_t y, const char* text, Color_t color) 
{
  TLatex l; //l.SetTextAlign(12); l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextFont(72);
  l.SetTextColor(color);

  double delx = 0.115*696*gPad->GetWh()/(472*gPad->GetWw());
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


void myTextBold(double_t x, double_t y, Color_t color, const char* text, double_t tsize) 
{
  TLatex l;
  l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextFont(62);
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}


void myText(double_t x, double_t y, const char* text, double_t tsize) 
{
  TLatex l;
  l.SetNDC();
  l.SetTextSize(tsize); 
  l.DrawLatex(x,y,text);
}


void myTextBoldNoNDC(double_t x, double_t y, const char* text, double_t tsize) 
{
  TLatex l;
  l.SetTextSize(tsize); 
  l.SetTextAlign(21); 
  //l.SetTextFont(62); // liq comment it 
  l.DrawLatex(x,y,text);
}


void myTextNoNDC(double_t x, double_t y, const char* text, double_t tsize) 
{
  TLatex l;
  l.SetTextSize(tsize); 
  l.SetTextAlign(22); 
  l.DrawLatex(x,y,text);
}


void limits_spin0_bbbb_bbtt_bbyy_pointExtension300_comb_v140invfb_20210531_obs2_exp_obs_profiledNP_NPnocorr_210603()
{
//=========Macro generated from canvas: c1/hh limits
//=========  (Thu Jun  3 00:42:29 2021) by ROOT version 6.22/00
   TCanvas *c1 = new TCanvas("c1", "hh limits",0,23,1052,700);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   c1->Range(0,0,1,1);
   c1->SetFillColor(0);
   c1->SetBorderMode(0);
   c1->SetBorderSize(2);
   c1->SetTickx(1);
   c1->SetTicky(1);
   c1->SetLeftMargin(0.16);
   c1->SetRightMargin(0.05);
   c1->SetTopMargin(0.05);
   c1->SetBottomMargin(0.16);
   c1->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: pad1
   TPad *pad1 = new TPad("pad1", "pad1",0,0,0.76,1);
   pad1->Draw();
   pad1->cd();
   pad1->Range(2.15198,-4.535537,3.372989,1.793577);
   pad1->SetFillColor(0);
   pad1->SetBorderMode(0);
   pad1->SetBorderSize(2);
   pad1->SetLogx();
   pad1->SetLogy();
   pad1->SetTickx(1);
   pad1->SetTicky(1);
   pad1->SetLeftMargin(0.16);
   pad1->SetRightMargin(0.05);
   pad1->SetTopMargin(0.05);
   pad1->SetBottomMargin(0.16);
   pad1->SetFrameBorderMode(0);
   pad1->SetFrameBorderMode(0);
   
   TMultiGraph *multigraph = new TMultiGraph();
   multigraph->SetName("limits");
   multigraph->SetTitle("");
   
   Double_t bbbb_exp_fx1[23] = {
   251,
   260,
   280,
   300,
   400,
   500,
   600,
   700,
   800,
   900,
   1000,
   1100,
   1200,
   1300,
   1400,
   1500,
   1600,
   1800,
   2000,
   2500,
   3000,
   4000,
   5000};
   Double_t bbbb_exp_fy1[23] = {
   1.224685,
   2.368036,
   1.703122,
   1.036457,
   0.1026937,
   0.03491513,
   0.01683126,
   0.009030204,
   0.005726297,
   0.003951046,
   0.002876262,
   0.002191062,
   0.001807308,
   0.001524607,
   0.00130761,
   0.0011457,
   0.00108486,
   0.000843732,
   0.000683482,
   0.000499624,
   0.000414398,
   0.000433745,
   0.000486189};
   TGraph *graph = new TGraph(23,bbbb_exp_fx1,bbbb_exp_fy1);
   graph->SetName("bbbb_exp");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#3333ff");
   graph->SetLineColor(ci);
   graph->SetLineStyle(7);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#3333ff");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(2);
   graph->SetMarkerSize(1.2);
   
   TH1F *Graph_bbbb_exp1 = new TH1F("Graph_bbbb_exp1","Graph",100,225.9,5474.9);
   Graph_bbbb_exp1->SetMinimum(0.0003729582);
   Graph_bbbb_exp1->SetMaximum(2.604798);
   Graph_bbbb_exp1->SetDirectory(0);
   Graph_bbbb_exp1->SetStats(0);
   Graph_bbbb_exp1->SetLineWidth(2);
   Graph_bbbb_exp1->SetMarkerStyle(20);
   Graph_bbbb_exp1->SetMarkerSize(1.2);
   Graph_bbbb_exp1->GetXaxis()->SetNdivisions(505);
   Graph_bbbb_exp1->GetXaxis()->SetLabelFont(42);
   Graph_bbbb_exp1->GetXaxis()->SetLabelOffset(0.01);
   Graph_bbbb_exp1->GetXaxis()->SetLabelSize(0.05);
   Graph_bbbb_exp1->GetXaxis()->SetTitleSize(0.05);
   Graph_bbbb_exp1->GetXaxis()->SetTitleOffset(1.4);
   Graph_bbbb_exp1->GetXaxis()->SetTitleFont(42);
   Graph_bbbb_exp1->GetYaxis()->SetNdivisions(505);
   Graph_bbbb_exp1->GetYaxis()->SetLabelFont(42);
   Graph_bbbb_exp1->GetYaxis()->SetLabelOffset(0.01);
   Graph_bbbb_exp1->GetYaxis()->SetLabelSize(0.05);
   Graph_bbbb_exp1->GetYaxis()->SetTitleSize(0.05);
   Graph_bbbb_exp1->GetYaxis()->SetTitleOffset(1.4);
   Graph_bbbb_exp1->GetYaxis()->SetTitleFont(42);
   Graph_bbbb_exp1->GetZaxis()->SetNdivisions(505);
   Graph_bbbb_exp1->GetZaxis()->SetLabelFont(42);
   Graph_bbbb_exp1->GetZaxis()->SetLabelOffset(0.01);
   Graph_bbbb_exp1->GetZaxis()->SetLabelSize(0.05);
   Graph_bbbb_exp1->GetZaxis()->SetTitleSize(0.05);
   Graph_bbbb_exp1->GetZaxis()->SetTitleOffset(1);
   Graph_bbbb_exp1->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_bbbb_exp1);
   
   multigraph->Add(graph,"");
   
   Double_t bbbb_obs_fx2[23] = {
   251,
   260,
   280,
   300,
   400,
   500,
   600,
   700,
   800,
   900,
   1000,
   1100,
   1200,
   1300,
   1400,
   1500,
   1600,
   1800,
   2000,
   2500,
   3000,
   4000,
   5000};
   Double_t bbbb_obs_fy2[23] = {
   1.586401,
   3.601968,
   2.977423,
   1.377719,
   0.0601435,
   0.03125205,
   0.009714861,
   0.007936791,
   0.004236008,
   0.004240867,
   0.002390892,
   0.005767605,
   0.003327874,
   0.001995374,
   0.002681759,
   0.002555168,
   0.001838778,
   0.001178751,
   0.001007897,
   0.000698318,
   0.000411118,
   0.000921648,
   0.000428007};
   graph = new TGraph(23,bbbb_obs_fx2,bbbb_obs_fy2);
   graph->SetName("bbbb_obs");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#3333ff");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#3333ff");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(20);
   graph->SetMarkerSize(0.96);
   
   TH1F *Graph_bbbb_obs2 = new TH1F("Graph_bbbb_obs2","Graph",100,225.9,5474.9);
   Graph_bbbb_obs2->SetMinimum(0.0003700062);
   Graph_bbbb_obs2->SetMaximum(3.962123);
   Graph_bbbb_obs2->SetDirectory(0);
   Graph_bbbb_obs2->SetStats(0);
   Graph_bbbb_obs2->SetLineWidth(2);
   Graph_bbbb_obs2->SetMarkerStyle(20);
   Graph_bbbb_obs2->SetMarkerSize(1.2);
   Graph_bbbb_obs2->GetXaxis()->SetNdivisions(505);
   Graph_bbbb_obs2->GetXaxis()->SetLabelFont(42);
   Graph_bbbb_obs2->GetXaxis()->SetLabelOffset(0.01);
   Graph_bbbb_obs2->GetXaxis()->SetLabelSize(0.05);
   Graph_bbbb_obs2->GetXaxis()->SetTitleSize(0.05);
   Graph_bbbb_obs2->GetXaxis()->SetTitleOffset(1.4);
   Graph_bbbb_obs2->GetXaxis()->SetTitleFont(42);
   Graph_bbbb_obs2->GetYaxis()->SetNdivisions(505);
   Graph_bbbb_obs2->GetYaxis()->SetLabelFont(42);
   Graph_bbbb_obs2->GetYaxis()->SetLabelOffset(0.01);
   Graph_bbbb_obs2->GetYaxis()->SetLabelSize(0.05);
   Graph_bbbb_obs2->GetYaxis()->SetTitleSize(0.05);
   Graph_bbbb_obs2->GetYaxis()->SetTitleOffset(1.4);
   Graph_bbbb_obs2->GetYaxis()->SetTitleFont(42);
   Graph_bbbb_obs2->GetZaxis()->SetNdivisions(505);
   Graph_bbbb_obs2->GetZaxis()->SetLabelFont(42);
   Graph_bbbb_obs2->GetZaxis()->SetLabelOffset(0.01);
   Graph_bbbb_obs2->GetZaxis()->SetLabelSize(0.05);
   Graph_bbbb_obs2->GetZaxis()->SetTitleSize(0.05);
   Graph_bbbb_obs2->GetZaxis()->SetTitleOffset(1);
   Graph_bbbb_obs2->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_bbbb_obs2);
   
   multigraph->Add(graph,"");
   
   Double_t bbtautau_exp_fx3[19] = {
   251,
   260,
   280,
   300,
   325,
   350,
   400,
   450,
   500,
   550,
   600,
   700,
   800,
   900,
   1000,
   1100,
   1200,
   1400,
   1600};
   Double_t bbtautau_exp_fy3[19] = {
   0.3444471,
   0.7377133,
   0.8291594,
   0.6494878,
   0.4645827,
   0.3522514,
   0.1444871,
   0.06835085,
   0.04269601,
   0.03270913,
   0.02628874,
   0.0193377,
   0.01481686,
   0.01320068,
   0.01183135,
   0.01253318,
   0.01329965,
   0.01899272,
   0.02828702};
   graph = new TGraph(19,bbtautau_exp_fx3,bbtautau_exp_fy3);
   graph->SetName("bbtautau_exp");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#990099");
   graph->SetLineColor(ci);
   graph->SetLineStyle(7);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#990099");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(2);
   graph->SetMarkerSize(1.2);
   
   TH1F *Graph_bbtautau_exp3 = new TH1F("Graph_bbtautau_exp3","Graph",100,116.1,1734.9);
   Graph_bbtautau_exp3->SetMinimum(0.01064822);
   Graph_bbtautau_exp3->SetMaximum(0.9108922);
   Graph_bbtautau_exp3->SetDirectory(0);
   Graph_bbtautau_exp3->SetStats(0);
   Graph_bbtautau_exp3->SetLineWidth(2);
   Graph_bbtautau_exp3->SetMarkerStyle(20);
   Graph_bbtautau_exp3->SetMarkerSize(1.2);
   Graph_bbtautau_exp3->GetXaxis()->SetNdivisions(505);
   Graph_bbtautau_exp3->GetXaxis()->SetLabelFont(42);
   Graph_bbtautau_exp3->GetXaxis()->SetLabelOffset(0.01);
   Graph_bbtautau_exp3->GetXaxis()->SetLabelSize(0.05);
   Graph_bbtautau_exp3->GetXaxis()->SetTitleSize(0.05);
   Graph_bbtautau_exp3->GetXaxis()->SetTitleOffset(1.4);
   Graph_bbtautau_exp3->GetXaxis()->SetTitleFont(42);
   Graph_bbtautau_exp3->GetYaxis()->SetNdivisions(505);
   Graph_bbtautau_exp3->GetYaxis()->SetLabelFont(42);
   Graph_bbtautau_exp3->GetYaxis()->SetLabelOffset(0.01);
   Graph_bbtautau_exp3->GetYaxis()->SetLabelSize(0.05);
   Graph_bbtautau_exp3->GetYaxis()->SetTitleSize(0.05);
   Graph_bbtautau_exp3->GetYaxis()->SetTitleOffset(1.4);
   Graph_bbtautau_exp3->GetYaxis()->SetTitleFont(42);
   Graph_bbtautau_exp3->GetZaxis()->SetNdivisions(505);
   Graph_bbtautau_exp3->GetZaxis()->SetLabelFont(42);
   Graph_bbtautau_exp3->GetZaxis()->SetLabelOffset(0.01);
   Graph_bbtautau_exp3->GetZaxis()->SetLabelSize(0.05);
   Graph_bbtautau_exp3->GetZaxis()->SetTitleSize(0.05);
   Graph_bbtautau_exp3->GetZaxis()->SetTitleOffset(1);
   Graph_bbtautau_exp3->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_bbtautau_exp3);
   
   multigraph->Add(graph,"");
   
   Double_t bbtautau_obs_fx4[19] = {
   251,
   260,
   280,
   300,
   325,
   350,
   400,
   450,
   500,
   550,
   600,
   700,
   800,
   900,
   1000,
   1100,
   1200,
   1400,
   1600};
   Double_t bbtautau_obs_fy4[19] = {
   0.6547361,
   0.9006836,
   0.4782721,
   0.5111473,
   0.3322476,
   0.2327375,
   0.07967997,
   0.04857658,
   0.04541521,
   0.0230327,
   0.02268862,
   0.02724668,
   0.03242683,
   0.03173564,
   0.02928594,
   0.02707365,
   0.0215234,
   0.02664377,
   0.02828096};
   graph = new TGraph(19,bbtautau_obs_fx4,bbtautau_obs_fy4);
   graph->SetName("bbtautau_obs");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#990099");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#990099");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(20);
   graph->SetMarkerSize(0.96);
   
   TH1F *Graph_bbtautau_obs4 = new TH1F("Graph_bbtautau_obs4","Graph",100,116.1,1734.9);
   Graph_bbtautau_obs4->SetMinimum(0.01937106);
   Graph_bbtautau_obs4->SetMaximum(0.9885997);
   Graph_bbtautau_obs4->SetDirectory(0);
   Graph_bbtautau_obs4->SetStats(0);
   Graph_bbtautau_obs4->SetLineWidth(2);
   Graph_bbtautau_obs4->SetMarkerStyle(20);
   Graph_bbtautau_obs4->SetMarkerSize(1.2);
   Graph_bbtautau_obs4->GetXaxis()->SetNdivisions(505);
   Graph_bbtautau_obs4->GetXaxis()->SetLabelFont(42);
   Graph_bbtautau_obs4->GetXaxis()->SetLabelOffset(0.01);
   Graph_bbtautau_obs4->GetXaxis()->SetLabelSize(0.05);
   Graph_bbtautau_obs4->GetXaxis()->SetTitleSize(0.05);
   Graph_bbtautau_obs4->GetXaxis()->SetTitleOffset(1.4);
   Graph_bbtautau_obs4->GetXaxis()->SetTitleFont(42);
   Graph_bbtautau_obs4->GetYaxis()->SetNdivisions(505);
   Graph_bbtautau_obs4->GetYaxis()->SetLabelFont(42);
   Graph_bbtautau_obs4->GetYaxis()->SetLabelOffset(0.01);
   Graph_bbtautau_obs4->GetYaxis()->SetLabelSize(0.05);
   Graph_bbtautau_obs4->GetYaxis()->SetTitleSize(0.05);
   Graph_bbtautau_obs4->GetYaxis()->SetTitleOffset(1.4);
   Graph_bbtautau_obs4->GetYaxis()->SetTitleFont(42);
   Graph_bbtautau_obs4->GetZaxis()->SetNdivisions(505);
   Graph_bbtautau_obs4->GetZaxis()->SetLabelFont(42);
   Graph_bbtautau_obs4->GetZaxis()->SetLabelOffset(0.01);
   Graph_bbtautau_obs4->GetZaxis()->SetLabelSize(0.05);
   Graph_bbtautau_obs4->GetZaxis()->SetTitleSize(0.05);
   Graph_bbtautau_obs4->GetZaxis()->SetTitleOffset(1);
   Graph_bbtautau_obs4->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_bbtautau_obs4);
   
   multigraph->Add(graph,"");
   
   Double_t bbyy_exp_fx5[22] = {
   251,
   260,
   270,
   280,
   290,
   300,
   312,
   325,
   337,
   350,
   375,
   400,
   425,
   450,
   475,
   500,
   550,
   600,
   700,
   800,
   900,
   1000};
   Double_t bbyy_exp_fy5[22] = {
   0.2118104,
   0.361997,
   0.3807887,
   0.3629264,
   0.3397812,
   0.3616979,
   0.3540393,
   0.3240646,
   0.2847944,
   0.2657133,
   0.2343459,
   0.1848576,
   0.1593137,
   0.1426355,
   0.1405925,
   0.1268645,
   0.0928402,
   0.07913617,
   0.07435386,
   0.06421386,
   0.04490186,
   0.0490436};
   graph = new TGraph(22,bbyy_exp_fx5,bbyy_exp_fy5);
   graph->SetName("bbyy_exp");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#ff3366");
   graph->SetLineColor(ci);
   graph->SetLineStyle(7);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#ff3366");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(2);
   graph->SetMarkerSize(1.2);
   
   TH1F *Graph_bbyy_exp5 = new TH1F("Graph_bbyy_exp5","Graph",100,176.1,1074.9);
   Graph_bbyy_exp5->SetMinimum(0.01131317);
   Graph_bbyy_exp5->SetMaximum(0.4143774);
   Graph_bbyy_exp5->SetDirectory(0);
   Graph_bbyy_exp5->SetStats(0);
   Graph_bbyy_exp5->SetLineWidth(2);
   Graph_bbyy_exp5->SetMarkerStyle(20);
   Graph_bbyy_exp5->SetMarkerSize(1.2);
   Graph_bbyy_exp5->GetXaxis()->SetNdivisions(505);
   Graph_bbyy_exp5->GetXaxis()->SetLabelFont(42);
   Graph_bbyy_exp5->GetXaxis()->SetLabelOffset(0.01);
   Graph_bbyy_exp5->GetXaxis()->SetLabelSize(0.05);
   Graph_bbyy_exp5->GetXaxis()->SetTitleSize(0.05);
   Graph_bbyy_exp5->GetXaxis()->SetTitleOffset(1.4);
   Graph_bbyy_exp5->GetXaxis()->SetTitleFont(42);
   Graph_bbyy_exp5->GetYaxis()->SetNdivisions(505);
   Graph_bbyy_exp5->GetYaxis()->SetLabelFont(42);
   Graph_bbyy_exp5->GetYaxis()->SetLabelOffset(0.01);
   Graph_bbyy_exp5->GetYaxis()->SetLabelSize(0.05);
   Graph_bbyy_exp5->GetYaxis()->SetTitleSize(0.05);
   Graph_bbyy_exp5->GetYaxis()->SetTitleOffset(1.4);
   Graph_bbyy_exp5->GetYaxis()->SetTitleFont(42);
   Graph_bbyy_exp5->GetZaxis()->SetNdivisions(505);
   Graph_bbyy_exp5->GetZaxis()->SetLabelFont(42);
   Graph_bbyy_exp5->GetZaxis()->SetLabelOffset(0.01);
   Graph_bbyy_exp5->GetZaxis()->SetLabelSize(0.05);
   Graph_bbyy_exp5->GetZaxis()->SetTitleSize(0.05);
   Graph_bbyy_exp5->GetZaxis()->SetTitleOffset(1);
   Graph_bbyy_exp5->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_bbyy_exp5);
   
   multigraph->Add(graph,"");
   
   Double_t bbyy_obs_fx6[22] = {
   251,
   260,
   270,
   280,
   290,
   300,
   312,
   325,
   337,
   350,
   375,
   400,
   425,
   450,
   475,
   500,
   550,
   600,
   700,
   800,
   900,
   1000};
   Double_t bbyy_obs_fy6[22] = {
   0.3737087,
   0.6192765,
   0.5753964,
   0.324553,
   0.2365402,
   0.3462419,
   0.3913949,
   0.2463755,
   0.2547474,
   0.3385101,
   0.4019956,
   0.1992617,
   0.1776417,
   0.1307587,
   0.1385703,
   0.1688778,
   0.08584362,
   0.07264196,
   0.04837601,
   0.0705693,
   0.07505447,
   0.05063947};
   graph = new TGraph(22,bbyy_obs_fx6,bbyy_obs_fy6);
   graph->SetName("bbyy_obs");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#ff3366");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#ff3366");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(20);
   graph->SetMarkerSize(0.96);
   
   TH1F *Graph_bbyy_obs6 = new TH1F("Graph_bbyy_obs6","Graph",100,176.1,1074.9);
   Graph_bbyy_obs6->SetMinimum(0.04353841);
   Graph_bbyy_obs6->SetMaximum(0.6763666);
   Graph_bbyy_obs6->SetDirectory(0);
   Graph_bbyy_obs6->SetStats(0);
   Graph_bbyy_obs6->SetLineWidth(2);
   Graph_bbyy_obs6->SetMarkerStyle(20);
   Graph_bbyy_obs6->SetMarkerSize(1.2);
   Graph_bbyy_obs6->GetXaxis()->SetNdivisions(505);
   Graph_bbyy_obs6->GetXaxis()->SetLabelFont(42);
   Graph_bbyy_obs6->GetXaxis()->SetLabelOffset(0.01);
   Graph_bbyy_obs6->GetXaxis()->SetLabelSize(0.05);
   Graph_bbyy_obs6->GetXaxis()->SetTitleSize(0.05);
   Graph_bbyy_obs6->GetXaxis()->SetTitleOffset(1.4);
   Graph_bbyy_obs6->GetXaxis()->SetTitleFont(42);
   Graph_bbyy_obs6->GetYaxis()->SetNdivisions(505);
   Graph_bbyy_obs6->GetYaxis()->SetLabelFont(42);
   Graph_bbyy_obs6->GetYaxis()->SetLabelOffset(0.01);
   Graph_bbyy_obs6->GetYaxis()->SetLabelSize(0.05);
   Graph_bbyy_obs6->GetYaxis()->SetTitleSize(0.05);
   Graph_bbyy_obs6->GetYaxis()->SetTitleOffset(1.4);
   Graph_bbyy_obs6->GetYaxis()->SetTitleFont(42);
   Graph_bbyy_obs6->GetZaxis()->SetNdivisions(505);
   Graph_bbyy_obs6->GetZaxis()->SetLabelFont(42);
   Graph_bbyy_obs6->GetZaxis()->SetLabelOffset(0.01);
   Graph_bbyy_obs6->GetZaxis()->SetLabelSize(0.05);
   Graph_bbyy_obs6->GetZaxis()->SetTitleSize(0.05);
   Graph_bbyy_obs6->GetZaxis()->SetTitleOffset(1);
   Graph_bbyy_obs6->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_bbyy_obs6);
   
   multigraph->Add(graph,"");
   
   Double_t comb_A_bbbb_bbtautau_bbyy_2s_fx3001[11] = {
   251,
   260,
   280,
   300,
   400,
   500,
   600,
   700,
   800,
   900,
   1000};
   Double_t comb_A_bbbb_bbtautau_bbyy_2s_fy3001[11] = {
   0.1688569,
   0.3119416,
   0.3140223,
   0.2853524,
   0.06863448,
   0.02440296,
   0.01283151,
   0.007685673,
   0.005099852,
   0.003649997,
   0.002734899};
   Double_t comb_A_bbbb_bbtautau_bbyy_2s_felx3001[11] = {
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0};
   Double_t comb_A_bbbb_bbtautau_bbyy_2s_fely3001[11] = {
   0.07822705,
   0.1445145,
   0.1454784,
   0.1321964,
   0.03179659,
   0.01130526,
   0.00594451,
   0.003560574,
   0.00236263,
   0.001690949,
   0.001267008};
   Double_t comb_A_bbbb_bbtautau_bbyy_2s_fehx3001[11] = {
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0};
   Double_t comb_A_bbbb_bbtautau_bbyy_2s_fehy3001[11] = {
   0.1845484,
   0.3292774,
   0.3455099,
   0.2944265,
   0.0772291,
   0.02675319,
   0.01524672,
   0.01005905,
   0.006771698,
   0.004947691,
   0.003728596};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(11,comb_A_bbbb_bbtautau_bbyy_2s_fx3001,comb_A_bbbb_bbtautau_bbyy_2s_fy3001,comb_A_bbbb_bbtautau_bbyy_2s_felx3001,comb_A_bbbb_bbtautau_bbyy_2s_fehx3001,comb_A_bbbb_bbtautau_bbyy_2s_fely3001,comb_A_bbbb_bbtautau_bbyy_2s_fehy3001);
   grae->SetName("comb_A_bbbb_bbtautau_bbyy_2s");
   grae->SetTitle("Graph");

   ci = TColor::GetColor("#ffff00");
   grae->SetFillColor(ci);
   grae->SetFillStyle(1000);

   ci = TColor::GetColor("#ffff00");
   grae->SetLineColor(ci);
   grae->SetMarkerStyle(20);
   grae->SetMarkerSize(1.2);
   
   TH1F *Graph_comb_A_bbbb_bbtautau_bbyy_2s3001 = new TH1F("Graph_comb_A_bbbb_bbtautau_bbyy_2s3001","Graph",100,176.1,1074.9);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->SetMinimum(0.001321102);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->SetMaximum(0.7253386);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->SetDirectory(0);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->SetStats(0);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->SetLineWidth(2);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->SetMarkerStyle(20);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->SetMarkerSize(1.2);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetXaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetXaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetXaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetXaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetXaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetXaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetXaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetYaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetYaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetYaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetYaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetYaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetYaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetYaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetZaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetZaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetZaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetZaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetZaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetZaxis()->SetTitleOffset(1);
   Graph_comb_A_bbbb_bbtautau_bbyy_2s3001->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_comb_A_bbbb_bbtautau_bbyy_2s3001);
   
   multigraph->Add(grae,"");
   
   Double_t comb_A_bbbb_bbtautau_bbyy_1s_fx3002[11] = {
   251,
   260,
   280,
   300,
   400,
   500,
   600,
   700,
   800,
   900,
   1000};
   Double_t comb_A_bbbb_bbtautau_bbyy_1s_fy3002[11] = {
   0.1688569,
   0.3119416,
   0.3140223,
   0.2853524,
   0.06863448,
   0.02440296,
   0.01283151,
   0.007685673,
   0.005099852,
   0.003649997,
   0.002734899};
   Double_t comb_A_bbbb_bbtautau_bbyy_1s_felx3002[11] = {
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0};
   Double_t comb_A_bbbb_bbtautau_bbyy_1s_fely3002[11] = {
   0.04718616,
   0.0871704,
   0.08775184,
   0.0797402,
   0.01917954,
   0.006819277,
   0.003585698,
   0.00214772,
   0.001425126,
   0.001019972,
   0.0007642527};
   Double_t comb_A_bbbb_bbtautau_bbyy_1s_fehx3002[11] = {
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0,
   0};
   Double_t comb_A_bbbb_bbtautau_bbyy_1s_fehy3002[11] = {
   0.07603071,
   0.1372741,
   0.1424996,
   0.1226943,
   0.03014584,
   0.01058571,
   0.005733112,
   0.003555641,
   0.002375271,
   0.001724362,
   0.001255681};
   grae = new TGraphAsymmErrors(11,comb_A_bbbb_bbtautau_bbyy_1s_fx3002,comb_A_bbbb_bbtautau_bbyy_1s_fy3002,comb_A_bbbb_bbtautau_bbyy_1s_felx3002,comb_A_bbbb_bbtautau_bbyy_1s_fehx3002,comb_A_bbbb_bbtautau_bbyy_1s_fely3002,comb_A_bbbb_bbtautau_bbyy_1s_fehy3002);
   grae->SetName("comb_A_bbbb_bbtautau_bbyy_1s");
   grae->SetTitle("Graph");

   ci = TColor::GetColor("#00ff00");
   grae->SetFillColor(ci);
   grae->SetFillStyle(1000);

   ci = TColor::GetColor("#00ff00");
   grae->SetLineColor(ci);
   grae->SetMarkerStyle(20);
   grae->SetMarkerSize(1.2);
   
   TH1F *Graph_comb_A_bbbb_bbtautau_bbyy_1s3002 = new TH1F("Graph_comb_A_bbbb_bbtautau_bbyy_1s3002","Graph",100,176.1,1074.9);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->SetMinimum(0.001773581);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->SetMaximum(0.5019769);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->SetDirectory(0);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->SetStats(0);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->SetLineWidth(2);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->SetMarkerStyle(20);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->SetMarkerSize(1.2);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetXaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetXaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetXaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetXaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetXaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetXaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetXaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetYaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetYaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetYaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetYaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetYaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetYaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetYaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetZaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetZaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetZaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetZaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetZaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetZaxis()->SetTitleOffset(1);
   Graph_comb_A_bbbb_bbtautau_bbyy_1s3002->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_comb_A_bbbb_bbtautau_bbyy_1s3002);
   
   multigraph->Add(grae,"");
   
   Double_t comb_A_bbbb_bbtautau_bbyy_exp_fx7[11] = {
   251,
   260,
   280,
   300,
   400,
   500,
   600,
   700,
   800,
   900,
   1000};
   Double_t comb_A_bbbb_bbtautau_bbyy_exp_fy7[11] = {
   0.1688569,
   0.3119416,
   0.3140223,
   0.2853524,
   0.06863448,
   0.02440296,
   0.01283151,
   0.007685673,
   0.005099852,
   0.003649997,
   0.002734899};
   graph = new TGraph(11,comb_A_bbbb_bbtautau_bbyy_exp_fx7,comb_A_bbbb_bbtautau_bbyy_exp_fy7);
   graph->SetName("comb_A_bbbb_bbtautau_bbyy_exp");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);
   graph->SetLineStyle(7);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(2);
   graph->SetMarkerSize(1.2);
   
   TH1F *Graph_comb_A_bbbb_bbtautau_bbyy_exp7 = new TH1F("Graph_comb_A_bbbb_bbtautau_bbyy_exp7","Graph",100,176.1,1074.9);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->SetMinimum(0.002461409);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->SetMaximum(0.345151);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->SetDirectory(0);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->SetStats(0);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->SetLineWidth(2);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->SetMarkerStyle(20);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->SetMarkerSize(1.2);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetXaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetXaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetXaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetXaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetXaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetXaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetXaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetYaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetYaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetYaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetYaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetYaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetYaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetYaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetZaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetZaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetZaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetZaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetZaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetZaxis()->SetTitleOffset(1);
   Graph_comb_A_bbbb_bbtautau_bbyy_exp7->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_comb_A_bbbb_bbtautau_bbyy_exp7);
   
   multigraph->Add(graph,"");
   
   Double_t comb_A_bbbb_bbtautau_bbyy_obs_fx8[11] = {
   251,
   260,
   280,
   300,
   400,
   500,
   600,
   700,
   800,
   900,
   1000};
   Double_t comb_A_bbbb_bbtautau_bbyy_obs_fy8[11] = {
   0.4009772,
   0.5701278,
   0.2516983,
   0.2730231,
   0.03799047,
   0.02550765,
   0.007488181,
   0.007713975,
   0.005893585,
   0.007290085,
   0.003870358};
   graph = new TGraph(11,comb_A_bbbb_bbtautau_bbyy_obs_fx8,comb_A_bbbb_bbtautau_bbyy_obs_fy8);
   graph->SetName("comb_A_bbbb_bbtautau_bbyy_obs");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(20);
   graph->SetMarkerSize(0.96);
   
   TH1F *Graph_comb_A_bbbb_bbtautau_bbyy_obs8 = new TH1F("Graph_comb_A_bbbb_bbtautau_bbyy_obs8","Graph",100,176.1,1074.9);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->SetMinimum(0.003483322);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->SetMaximum(0.6267535);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->SetDirectory(0);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->SetStats(0);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->SetLineWidth(2);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->SetMarkerStyle(20);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->SetMarkerSize(1.2);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetXaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetXaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetXaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetXaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetXaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetXaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetXaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetYaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetYaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetYaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetYaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetYaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetYaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetYaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetZaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetZaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetZaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetZaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetZaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetZaxis()->SetTitleOffset(1);
   Graph_comb_A_bbbb_bbtautau_bbyy_obs8->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_comb_A_bbbb_bbtautau_bbyy_obs8);
   
   multigraph->Add(graph,"");
   multigraph->Draw("a3 l");
   multigraph->GetXaxis()->SetLimits(13.55, 5237.45);
   multigraph->GetXaxis()->SetTitle("m_{S} [GeV]");
   multigraph->GetXaxis()->SetRange(5,39);
   multigraph->GetXaxis()->SetMoreLogLabels();
   multigraph->GetXaxis()->SetNdivisions(505);
   multigraph->GetXaxis()->SetLabelFont(42);
   multigraph->GetXaxis()->SetLabelOffset(0.01);
   multigraph->GetXaxis()->SetLabelSize(0.05);
   multigraph->GetXaxis()->SetTitleSize(0.045);
   multigraph->GetXaxis()->SetTitleOffset(1.4);
   multigraph->GetXaxis()->SetTitleFont(42);
   multigraph->GetYaxis()->SetTitle("#sigma(pp #rightarrow S #rightarrow HH) [pb]");
   multigraph->GetYaxis()->SetNdivisions(505);
   multigraph->GetYaxis()->SetLabelFont(42);
   multigraph->GetYaxis()->SetLabelOffset(0.01);
   multigraph->GetYaxis()->SetLabelSize(0.05);
   multigraph->GetYaxis()->SetTitleSize(0.045);
   multigraph->GetYaxis()->SetTitleOffset(1.6);
   multigraph->GetYaxis()->SetTitleFont(42);
   
   TH1F *limits_copy__1 = new TH1F("limits_copy__1","",100,13.55,5237.45);
   limits_copy__1->SetMinimum(0.0001383636);
   limits_copy__1->SetMaximum(6.442172);
   limits_copy__1->SetDirectory(0);
   limits_copy__1->SetStats(0);
   limits_copy__1->SetLineWidth(2);
   limits_copy__1->SetMarkerStyle(20);
   limits_copy__1->SetMarkerSize(1.2);
   limits_copy__1->GetXaxis()->SetNdivisions(505);
   limits_copy__1->GetXaxis()->SetLabelFont(42);
   limits_copy__1->GetXaxis()->SetLabelOffset(0.01);
   limits_copy__1->GetXaxis()->SetLabelSize(0.05);
   limits_copy__1->GetXaxis()->SetTitleSize(0.05);
   limits_copy__1->GetXaxis()->SetTitleOffset(1.4);
   limits_copy__1->GetXaxis()->SetTitleFont(42);
   limits_copy__1->GetYaxis()->SetNdivisions(505);
   limits_copy__1->GetYaxis()->SetLabelFont(42);
   limits_copy__1->GetYaxis()->SetLabelOffset(0.01);
   limits_copy__1->GetYaxis()->SetLabelSize(0.05);
   limits_copy__1->GetYaxis()->SetTitleSize(0.05);
   limits_copy__1->GetYaxis()->SetTitleOffset(1.4);
   limits_copy__1->GetYaxis()->SetTitleFont(42);
   limits_copy__1->GetZaxis()->SetNdivisions(505);
   limits_copy__1->GetZaxis()->SetLabelFont(42);
   limits_copy__1->GetZaxis()->SetLabelOffset(0.01);
   limits_copy__1->GetZaxis()->SetLabelSize(0.05);
   limits_copy__1->GetZaxis()->SetTitleSize(0.05);
   limits_copy__1->GetZaxis()->SetTitleOffset(1);
   limits_copy__1->GetZaxis()->SetTitleFont(42);
   limits_copy__1->Draw("sameaxis");
   
   TH1F *limits_copy__2 = new TH1F("limits_copy__2","",100,13.55,5237.45);
   limits_copy__2->SetMinimum(0.0003);
   limits_copy__2->SetMaximum(30);
   limits_copy__2->SetDirectory(0);
   limits_copy__2->SetStats(0);
   limits_copy__2->SetLineWidth(2);
   limits_copy__2->SetMarkerStyle(20);
   limits_copy__2->SetMarkerSize(1.2);
   limits_copy__2->GetXaxis()->SetTitle("m_{S} [GeV]");
   limits_copy__2->GetXaxis()->SetRange(5,39);
   limits_copy__2->GetXaxis()->SetMoreLogLabels();
   limits_copy__2->GetXaxis()->SetNdivisions(505);
   limits_copy__2->GetXaxis()->SetLabelFont(42);
   limits_copy__2->GetXaxis()->SetLabelOffset(0.01);
   limits_copy__2->GetXaxis()->SetLabelSize(0.05);
   limits_copy__2->GetXaxis()->SetTitleSize(0.045);
   limits_copy__2->GetXaxis()->SetTitleOffset(1.4);
   limits_copy__2->GetXaxis()->SetTitleFont(42);
   limits_copy__2->GetYaxis()->SetTitle("#sigma(pp #rightarrow S #rightarrow HH) [pb]");
   limits_copy__2->GetYaxis()->SetNdivisions(505);
   limits_copy__2->GetYaxis()->SetLabelFont(42);
   limits_copy__2->GetYaxis()->SetLabelOffset(0.01);
   limits_copy__2->GetYaxis()->SetLabelSize(0.05);
   limits_copy__2->GetYaxis()->SetTitleSize(0.045);
   limits_copy__2->GetYaxis()->SetTitleOffset(1.6);
   limits_copy__2->GetYaxis()->SetTitleFont(42);
   limits_copy__2->GetZaxis()->SetNdivisions(505);
   limits_copy__2->GetZaxis()->SetLabelFont(42);
   limits_copy__2->GetZaxis()->SetLabelOffset(0.01);
   limits_copy__2->GetZaxis()->SetLabelSize(0.05);
   limits_copy__2->GetZaxis()->SetTitleSize(0.05);
   limits_copy__2->GetZaxis()->SetTitleOffset(1);
   limits_copy__2->GetZaxis()->SetTitleFont(42);
   limits_copy__2->Draw("sameaxis");
   
   Double_t bbbb_exp_fx9[23] = {
   251,
   260,
   280,
   300,
   400,
   500,
   600,
   700,
   800,
   900,
   1000,
   1100,
   1200,
   1300,
   1400,
   1500,
   1600,
   1800,
   2000,
   2500,
   3000,
   4000,
   5000};
   Double_t bbbb_exp_fy9[23] = {
   1.224685,
   2.368036,
   1.703122,
   1.036457,
   0.1026937,
   0.03491513,
   0.01683126,
   0.009030204,
   0.005726297,
   0.003951046,
   0.002876262,
   0.002191062,
   0.001807308,
   0.001524607,
   0.00130761,
   0.0011457,
   0.00108486,
   0.000843732,
   0.000683482,
   0.000499624,
   0.000414398,
   0.000433745,
   0.000486189};
   graph = new TGraph(23,bbbb_exp_fx9,bbbb_exp_fy9);
   graph->SetName("bbbb_exp");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#3333ff");
   graph->SetLineColor(ci);
   graph->SetLineStyle(7);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#3333ff");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(2);
   graph->SetMarkerSize(1.2);
   
   TH1F *Graph_Graph_bbbb_exp19 = new TH1F("Graph_Graph_bbbb_exp19","Graph",100,225.9,5474.9);
   Graph_Graph_bbbb_exp19->SetMinimum(0.0003729582);
   Graph_Graph_bbbb_exp19->SetMaximum(2.604798);
   Graph_Graph_bbbb_exp19->SetDirectory(0);
   Graph_Graph_bbbb_exp19->SetStats(0);
   Graph_Graph_bbbb_exp19->SetLineWidth(2);
   Graph_Graph_bbbb_exp19->SetMarkerStyle(20);
   Graph_Graph_bbbb_exp19->SetMarkerSize(1.2);
   Graph_Graph_bbbb_exp19->GetXaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_exp19->GetXaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_exp19->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_exp19->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_exp19->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_exp19->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbbb_exp19->GetXaxis()->SetTitleFont(42);
   Graph_Graph_bbbb_exp19->GetYaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_exp19->GetYaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_exp19->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_exp19->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_exp19->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_exp19->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbbb_exp19->GetYaxis()->SetTitleFont(42);
   Graph_Graph_bbbb_exp19->GetZaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_exp19->GetZaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_exp19->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_exp19->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_exp19->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_exp19->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_bbbb_exp19->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_bbbb_exp19);
   
   graph->Draw("l");
   
   Double_t bbtautau_exp_fx10[19] = {
   251,
   260,
   280,
   300,
   325,
   350,
   400,
   450,
   500,
   550,
   600,
   700,
   800,
   900,
   1000,
   1100,
   1200,
   1400,
   1600};
   Double_t bbtautau_exp_fy10[19] = {
   0.3444471,
   0.7377133,
   0.8291594,
   0.6494878,
   0.4645827,
   0.3522514,
   0.1444871,
   0.06835085,
   0.04269601,
   0.03270913,
   0.02628874,
   0.0193377,
   0.01481686,
   0.01320068,
   0.01183135,
   0.01253318,
   0.01329965,
   0.01899272,
   0.02828702};
   graph = new TGraph(19,bbtautau_exp_fx10,bbtautau_exp_fy10);
   graph->SetName("bbtautau_exp");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#990099");
   graph->SetLineColor(ci);
   graph->SetLineStyle(7);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#990099");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(2);
   graph->SetMarkerSize(1.2);
   
   TH1F *Graph_Graph_bbtautau_exp310 = new TH1F("Graph_Graph_bbtautau_exp310","Graph",100,116.1,1734.9);
   Graph_Graph_bbtautau_exp310->SetMinimum(0.01064822);
   Graph_Graph_bbtautau_exp310->SetMaximum(0.9108922);
   Graph_Graph_bbtautau_exp310->SetDirectory(0);
   Graph_Graph_bbtautau_exp310->SetStats(0);
   Graph_Graph_bbtautau_exp310->SetLineWidth(2);
   Graph_Graph_bbtautau_exp310->SetMarkerStyle(20);
   Graph_Graph_bbtautau_exp310->SetMarkerSize(1.2);
   Graph_Graph_bbtautau_exp310->GetXaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_exp310->GetXaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_exp310->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_exp310->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_exp310->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_exp310->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbtautau_exp310->GetXaxis()->SetTitleFont(42);
   Graph_Graph_bbtautau_exp310->GetYaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_exp310->GetYaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_exp310->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_exp310->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_exp310->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_exp310->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbtautau_exp310->GetYaxis()->SetTitleFont(42);
   Graph_Graph_bbtautau_exp310->GetZaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_exp310->GetZaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_exp310->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_exp310->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_exp310->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_exp310->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_bbtautau_exp310->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_bbtautau_exp310);
   
   graph->Draw("l ");
   
   Double_t bbyy_exp_fx11[22] = {
   251,
   260,
   270,
   280,
   290,
   300,
   312,
   325,
   337,
   350,
   375,
   400,
   425,
   450,
   475,
   500,
   550,
   600,
   700,
   800,
   900,
   1000};
   Double_t bbyy_exp_fy11[22] = {
   0.2118104,
   0.361997,
   0.3807887,
   0.3629264,
   0.3397812,
   0.3616979,
   0.3540393,
   0.3240646,
   0.2847944,
   0.2657133,
   0.2343459,
   0.1848576,
   0.1593137,
   0.1426355,
   0.1405925,
   0.1268645,
   0.0928402,
   0.07913617,
   0.07435386,
   0.06421386,
   0.04490186,
   0.0490436};
   graph = new TGraph(22,bbyy_exp_fx11,bbyy_exp_fy11);
   graph->SetName("bbyy_exp");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#ff3366");
   graph->SetLineColor(ci);
   graph->SetLineStyle(7);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#ff3366");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(2);
   graph->SetMarkerSize(1.2);
   
   TH1F *Graph_Graph_bbyy_exp511 = new TH1F("Graph_Graph_bbyy_exp511","Graph",100,176.1,1074.9);
   Graph_Graph_bbyy_exp511->SetMinimum(0.01131317);
   Graph_Graph_bbyy_exp511->SetMaximum(0.4143774);
   Graph_Graph_bbyy_exp511->SetDirectory(0);
   Graph_Graph_bbyy_exp511->SetStats(0);
   Graph_Graph_bbyy_exp511->SetLineWidth(2);
   Graph_Graph_bbyy_exp511->SetMarkerStyle(20);
   Graph_Graph_bbyy_exp511->SetMarkerSize(1.2);
   Graph_Graph_bbyy_exp511->GetXaxis()->SetNdivisions(505);
   Graph_Graph_bbyy_exp511->GetXaxis()->SetLabelFont(42);
   Graph_Graph_bbyy_exp511->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbyy_exp511->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_bbyy_exp511->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_bbyy_exp511->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbyy_exp511->GetXaxis()->SetTitleFont(42);
   Graph_Graph_bbyy_exp511->GetYaxis()->SetNdivisions(505);
   Graph_Graph_bbyy_exp511->GetYaxis()->SetLabelFont(42);
   Graph_Graph_bbyy_exp511->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbyy_exp511->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_bbyy_exp511->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_bbyy_exp511->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbyy_exp511->GetYaxis()->SetTitleFont(42);
   Graph_Graph_bbyy_exp511->GetZaxis()->SetNdivisions(505);
   Graph_Graph_bbyy_exp511->GetZaxis()->SetLabelFont(42);
   Graph_Graph_bbyy_exp511->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbyy_exp511->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_bbyy_exp511->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_bbyy_exp511->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_bbyy_exp511->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_bbyy_exp511);
   
   graph->Draw("l ");
   
   Double_t comb_A_bbbb_bbtautau_bbyy_exp_fx12[11] = {
   251,
   260,
   280,
   300,
   400,
   500,
   600,
   700,
   800,
   900,
   1000};
   Double_t comb_A_bbbb_bbtautau_bbyy_exp_fy12[11] = {
   0.1688569,
   0.3119416,
   0.3140223,
   0.2853524,
   0.06863448,
   0.02440296,
   0.01283151,
   0.007685673,
   0.005099852,
   0.003649997,
   0.002734899};
   graph = new TGraph(11,comb_A_bbbb_bbtautau_bbyy_exp_fx12,comb_A_bbbb_bbtautau_bbyy_exp_fy12);
   graph->SetName("comb_A_bbbb_bbtautau_bbyy_exp");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);
   graph->SetLineStyle(7);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(2);
   graph->SetMarkerSize(1.2);
   
   TH1F *Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712 = new TH1F("Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712","Graph",100,176.1,1074.9);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->SetMinimum(0.002461409);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->SetMaximum(0.345151);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->SetDirectory(0);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->SetStats(0);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->SetLineWidth(2);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->SetMarkerStyle(20);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->SetMarkerSize(1.2);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetXaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetXaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetXaxis()->SetTitleFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetYaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetYaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetYaxis()->SetTitleFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetZaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetZaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_comb_A_bbbb_bbtautau_bbyy_exp712);
   
   graph->Draw("l ");
   
   Double_t bbbb_obs_fx13[23] = {
   251,
   260,
   280,
   300,
   400,
   500,
   600,
   700,
   800,
   900,
   1000,
   1100,
   1200,
   1300,
   1400,
   1500,
   1600,
   1800,
   2000,
   2500,
   3000,
   4000,
   5000};
   Double_t bbbb_obs_fy13[23] = {
   1.586401,
   3.601968,
   2.977423,
   1.377719,
   0.0601435,
   0.03125205,
   0.009714861,
   0.007936791,
   0.004236008,
   0.004240867,
   0.002390892,
   0.005767605,
   0.003327874,
   0.001995374,
   0.002681759,
   0.002555168,
   0.001838778,
   0.001178751,
   0.001007897,
   0.000698318,
   0.000411118,
   0.000921648,
   0.000428007};
   graph = new TGraph(23,bbbb_obs_fx13,bbbb_obs_fy13);
   graph->SetName("bbbb_obs");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#3333ff");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#3333ff");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(20);
   graph->SetMarkerSize(0.96);
   
   TH1F *Graph_Graph_bbbb_obs213 = new TH1F("Graph_Graph_bbbb_obs213","Graph",100,225.9,5474.9);
   Graph_Graph_bbbb_obs213->SetMinimum(0.0003700062);
   Graph_Graph_bbbb_obs213->SetMaximum(3.962123);
   Graph_Graph_bbbb_obs213->SetDirectory(0);
   Graph_Graph_bbbb_obs213->SetStats(0);
   Graph_Graph_bbbb_obs213->SetLineWidth(2);
   Graph_Graph_bbbb_obs213->SetMarkerStyle(20);
   Graph_Graph_bbbb_obs213->SetMarkerSize(1.2);
   Graph_Graph_bbbb_obs213->GetXaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_obs213->GetXaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_obs213->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_obs213->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_obs213->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_obs213->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbbb_obs213->GetXaxis()->SetTitleFont(42);
   Graph_Graph_bbbb_obs213->GetYaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_obs213->GetYaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_obs213->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_obs213->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_obs213->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_obs213->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbbb_obs213->GetYaxis()->SetTitleFont(42);
   Graph_Graph_bbbb_obs213->GetZaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_obs213->GetZaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_obs213->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_obs213->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_obs213->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_obs213->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_bbbb_obs213->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_bbbb_obs213);
   
   graph->Draw("l ");
   
   Double_t bbtautau_obs_fx14[19] = {
   251,
   260,
   280,
   300,
   325,
   350,
   400,
   450,
   500,
   550,
   600,
   700,
   800,
   900,
   1000,
   1100,
   1200,
   1400,
   1600};
   Double_t bbtautau_obs_fy14[19] = {
   0.6547361,
   0.9006836,
   0.4782721,
   0.5111473,
   0.3322476,
   0.2327375,
   0.07967997,
   0.04857658,
   0.04541521,
   0.0230327,
   0.02268862,
   0.02724668,
   0.03242683,
   0.03173564,
   0.02928594,
   0.02707365,
   0.0215234,
   0.02664377,
   0.02828096};
   graph = new TGraph(19,bbtautau_obs_fx14,bbtautau_obs_fy14);
   graph->SetName("bbtautau_obs");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#990099");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#990099");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(20);
   graph->SetMarkerSize(0.96);
   
   TH1F *Graph_Graph_bbtautau_obs414 = new TH1F("Graph_Graph_bbtautau_obs414","Graph",100,116.1,1734.9);
   Graph_Graph_bbtautau_obs414->SetMinimum(0.01937106);
   Graph_Graph_bbtautau_obs414->SetMaximum(0.9885997);
   Graph_Graph_bbtautau_obs414->SetDirectory(0);
   Graph_Graph_bbtautau_obs414->SetStats(0);
   Graph_Graph_bbtautau_obs414->SetLineWidth(2);
   Graph_Graph_bbtautau_obs414->SetMarkerStyle(20);
   Graph_Graph_bbtautau_obs414->SetMarkerSize(1.2);
   Graph_Graph_bbtautau_obs414->GetXaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_obs414->GetXaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_obs414->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_obs414->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_obs414->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_obs414->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbtautau_obs414->GetXaxis()->SetTitleFont(42);
   Graph_Graph_bbtautau_obs414->GetYaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_obs414->GetYaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_obs414->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_obs414->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_obs414->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_obs414->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbtautau_obs414->GetYaxis()->SetTitleFont(42);
   Graph_Graph_bbtautau_obs414->GetZaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_obs414->GetZaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_obs414->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_obs414->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_obs414->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_obs414->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_bbtautau_obs414->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_bbtautau_obs414);
   
   graph->Draw("l ");
   
   Double_t bbyy_obs_fx15[22] = {
   251,
   260,
   270,
   280,
   290,
   300,
   312,
   325,
   337,
   350,
   375,
   400,
   425,
   450,
   475,
   500,
   550,
   600,
   700,
   800,
   900,
   1000};
   Double_t bbyy_obs_fy15[22] = {
   0.3737087,
   0.6192765,
   0.5753964,
   0.324553,
   0.2365402,
   0.3462419,
   0.3913949,
   0.2463755,
   0.2547474,
   0.3385101,
   0.4019956,
   0.1992617,
   0.1776417,
   0.1307587,
   0.1385703,
   0.1688778,
   0.08584362,
   0.07264196,
   0.04837601,
   0.0705693,
   0.07505447,
   0.05063947};
   graph = new TGraph(22,bbyy_obs_fx15,bbyy_obs_fy15);
   graph->SetName("bbyy_obs");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);

   ci = TColor::GetColor("#ff3366");
   graph->SetLineColor(ci);
   graph->SetLineWidth(3);

   ci = TColor::GetColor("#ff3366");
   graph->SetMarkerColor(ci);
   graph->SetMarkerStyle(20);
   graph->SetMarkerSize(0.96);
   
   TH1F *Graph_Graph_bbyy_obs615 = new TH1F("Graph_Graph_bbyy_obs615","Graph",100,176.1,1074.9);
   Graph_Graph_bbyy_obs615->SetMinimum(0.04353841);
   Graph_Graph_bbyy_obs615->SetMaximum(0.6763666);
   Graph_Graph_bbyy_obs615->SetDirectory(0);
   Graph_Graph_bbyy_obs615->SetStats(0);
   Graph_Graph_bbyy_obs615->SetLineWidth(2);
   Graph_Graph_bbyy_obs615->SetMarkerStyle(20);
   Graph_Graph_bbyy_obs615->SetMarkerSize(1.2);
   Graph_Graph_bbyy_obs615->GetXaxis()->SetNdivisions(505);
   Graph_Graph_bbyy_obs615->GetXaxis()->SetLabelFont(42);
   Graph_Graph_bbyy_obs615->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbyy_obs615->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_bbyy_obs615->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_bbyy_obs615->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbyy_obs615->GetXaxis()->SetTitleFont(42);
   Graph_Graph_bbyy_obs615->GetYaxis()->SetNdivisions(505);
   Graph_Graph_bbyy_obs615->GetYaxis()->SetLabelFont(42);
   Graph_Graph_bbyy_obs615->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbyy_obs615->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_bbyy_obs615->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_bbyy_obs615->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbyy_obs615->GetYaxis()->SetTitleFont(42);
   Graph_Graph_bbyy_obs615->GetZaxis()->SetNdivisions(505);
   Graph_Graph_bbyy_obs615->GetZaxis()->SetLabelFont(42);
   Graph_Graph_bbyy_obs615->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbyy_obs615->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_bbyy_obs615->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_bbyy_obs615->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_bbyy_obs615->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_bbyy_obs615);
   
   graph->Draw("l ");
   
   Double_t comb_A_bbbb_bbtautau_bbyy_obs_fx16[11] = {
   251,
   260,
   280,
   300,
   400,
   500,
   600,
   700,
   800,
   900,
   1000};
   Double_t comb_A_bbbb_bbtautau_bbyy_obs_fy16[11] = {
   0.4009772,
   0.5701278,
   0.2516983,
   0.2730231,
   0.03799047,
   0.02550765,
   0.007488181,
   0.007713975,
   0.005893585,
   0.007290085,
   0.003870358};
   graph = new TGraph(11,comb_A_bbbb_bbtautau_bbyy_obs_fx16,comb_A_bbbb_bbtautau_bbyy_obs_fy16);
   graph->SetName("comb_A_bbbb_bbtautau_bbyy_obs");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(20);
   graph->SetMarkerSize(0.96);
   
   TH1F *Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816 = new TH1F("Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816","Graph",100,176.1,1074.9);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->SetMinimum(0.003483322);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->SetMaximum(0.6267535);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->SetDirectory(0);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->SetStats(0);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->SetLineWidth(2);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->SetMarkerStyle(20);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->SetMarkerSize(1.2);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetXaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetXaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetXaxis()->SetTitleFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetYaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetYaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetYaxis()->SetTitleFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetZaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetZaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_comb_A_bbbb_bbtautau_bbyy_obs816);
   
   graph->Draw("lp ");
   TLatex *   tex = new TLatex(0.45,0.88,"ATLAS");
tex->SetNDC();
   tex->SetTextFont(72);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.5921913,0.88,"Internal");
tex->SetNDC();
   tex->SetTextFont(42);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.45,0.83,"#sqrt{s} = 13 TeV,  139 fb^{-1}");
tex->SetNDC();
   tex->SetTextFont(42);
   tex->SetTextSize(0.04);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.75,0.72,"spin-0");
tex->SetNDC();
   tex->SetTextFont(42);
   tex->SetLineWidth(2);
   tex->Draw();
   
   TH1F *limits_copy__3 = new TH1F("limits_copy__3","",100,13.55,5237.45);
   limits_copy__3->SetMinimum(0.0003);
   limits_copy__3->SetMaximum(30);
   limits_copy__3->SetDirectory(0);
   limits_copy__3->SetStats(0);
   limits_copy__3->SetLineWidth(2);
   limits_copy__3->SetMarkerStyle(20);
   limits_copy__3->SetMarkerSize(1.2);
   limits_copy__3->GetXaxis()->SetTitle("m_{S} [GeV]");
   limits_copy__3->GetXaxis()->SetRange(5,39);
   limits_copy__3->GetXaxis()->SetMoreLogLabels();
   limits_copy__3->GetXaxis()->SetNdivisions(505);
   limits_copy__3->GetXaxis()->SetLabelFont(42);
   limits_copy__3->GetXaxis()->SetLabelOffset(0.01);
   limits_copy__3->GetXaxis()->SetLabelSize(0.05);
   limits_copy__3->GetXaxis()->SetTitleSize(0.045);
   limits_copy__3->GetXaxis()->SetTitleOffset(1.4);
   limits_copy__3->GetXaxis()->SetTitleFont(42);
   limits_copy__3->GetYaxis()->SetTitle("#sigma(pp #rightarrow S #rightarrow HH) [pb]");
   limits_copy__3->GetYaxis()->SetNdivisions(505);
   limits_copy__3->GetYaxis()->SetLabelFont(42);
   limits_copy__3->GetYaxis()->SetLabelOffset(0.01);
   limits_copy__3->GetYaxis()->SetLabelSize(0.05);
   limits_copy__3->GetYaxis()->SetTitleSize(0.045);
   limits_copy__3->GetYaxis()->SetTitleOffset(1.6);
   limits_copy__3->GetYaxis()->SetTitleFont(42);
   limits_copy__3->GetZaxis()->SetNdivisions(505);
   limits_copy__3->GetZaxis()->SetLabelFont(42);
   limits_copy__3->GetZaxis()->SetLabelOffset(0.01);
   limits_copy__3->GetZaxis()->SetLabelSize(0.05);
   limits_copy__3->GetZaxis()->SetTitleSize(0.05);
   limits_copy__3->GetZaxis()->SetTitleOffset(1);
   limits_copy__3->GetZaxis()->SetTitleFont(42);
   limits_copy__3->Draw("sameaxis");
   pad1->Modified();
   c1->cd();
  
// ------------>Primitives in pad: pad2
   TPad *pad2 = new TPad("pad2", "pad2",0.75,0,1,1);
   pad2->Draw();
   pad2->cd();
   pad2->Range(0,0,1,1);
   pad2->SetFillColor(0);
   pad2->SetBorderMode(0);
   pad2->SetBorderSize(2);
   pad2->SetTickx(1);
   pad2->SetTicky(1);
   pad2->SetLeftMargin(0.16);
   pad2->SetRightMargin(0.05);
   pad2->SetTopMargin(0.05);
   pad2->SetBottomMargin(0.16);
   pad2->SetFrameBorderMode(0);
   
   TLegend *leg = new TLegend(0,0.16,0.98,0.95,NULL,"brNDC");
   leg->SetBorderSize(1);
   leg->SetTextSize(0.075);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(1);
   leg->SetFillColor(0);
   leg->SetFillStyle(0);
   TLegendEntry *entry=leg->AddEntry("bbbb_exp","b#bar{b}b#bar{b} (exp.)","l");

   ci = TColor::GetColor("#3333ff");
   entry->SetLineColor(ci);
   entry->SetLineStyle(7);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("bbbb_obs","b#bar{b}b#bar{b} (obs.)","l");

   ci = TColor::GetColor("#3333ff");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("bbtautau_exp","b#bar{b}#tau^{+}#tau^{-} (exp.)","l");

   ci = TColor::GetColor("#990099");
   entry->SetLineColor(ci);
   entry->SetLineStyle(7);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("bbtautau_obs","b#bar{b}#tau^{+}#tau^{-} (obs.)","l");

   ci = TColor::GetColor("#990099");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("bbyy_exp","b#bar{b}#gamma#gamma (exp.)","l");

   ci = TColor::GetColor("#ff3366");
   entry->SetLineColor(ci);
   entry->SetLineStyle(7);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("bbyy_obs","b#bar{b}#gamma#gamma (obs.)","l");

   ci = TColor::GetColor("#ff3366");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("NULL","Combined (exp.)","l");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("NULL","Combined (obs.)","p l");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("comb_A_bbbb_bbtautau_bbyy_1s","Comb. #pm1#sigma (exp.)","f");

   ci = TColor::GetColor("#00ff00");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1000);

   ci = TColor::GetColor("#00ff00");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("comb_A_bbbb_bbtautau_bbyy_2s","Comb. #pm2#sigma (exp.)","f");

   ci = TColor::GetColor("#ffff00");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1000);

   ci = TColor::GetColor("#ffff00");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   leg->Draw();
   pad2->Modified();
   c1->cd();
   c1->Modified();
   c1->cd();
   c1->SetSelected(c1);
}

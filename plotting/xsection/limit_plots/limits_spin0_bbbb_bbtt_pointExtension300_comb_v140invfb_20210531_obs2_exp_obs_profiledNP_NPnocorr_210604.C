void limits_spin0_bbbb_bbtt_pointExtension300_comb_v140invfb_20210531_obs2_exp_obs_profiledNP_NPnocorr_210604()
{
//=========Macro generated from canvas: c1/hh limits
//=========  (Fri Jun  4 12:21:30 2021) by ROOT version 6.22/08
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
   pad1->Range(-147.7958,-4.535537,2166.59,1.793577);
   pad1->SetFillColor(0);
   pad1->SetBorderMode(0);
   pad1->SetBorderSize(2);
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
   3.607396,
   6.977636,
   5.024684,
   3.057476,
   0.302884,
   0.1031709,
   0.04971187,
   0.02669545,
   0.01691946,
   0.01168353,
   0.008499439,
   0.006465577,
   0.005302704,
   0.004499932,
   0.003857605,
   0.003384238,
   0.003205164,
   0.002498645,
   0.002022435,
   0.001485208,
   0.001230974,
   0.001286988,
   0.001447981};
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
   
   TH1F *Graph_bbbb_exp1 = new TH1F("Graph_bbbb_exp1","Graph",100,0,5474.9);
   Graph_bbbb_exp1->SetMinimum(0.001107877);
   Graph_bbbb_exp1->SetMaximum(7.675277);
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
   4.676847,
   10.61901,
   8.777929,
   4.061728,
   0.1773091,
   0.09213873,
   0.02864067,
   0.02339879,
   0.01248848,
   0.01250459,
   0.00704885,
   0.01700356,
   0.009811303,
   0.005882546,
   0.007906132,
   0.007532925,
   0.005420942,
   0.003475117,
   0.002971425,
   0.002058782,
   0.001213788,
   0.002717123,
   0.001262291};
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
   
   TH1F *Graph_bbbb_obs2 = new TH1F("Graph_bbbb_obs2","Graph",100,0,5474.9);
   Graph_bbbb_obs2->SetMinimum(0.001092409);
   Graph_bbbb_obs2->SetMaximum(11.68079);
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
   
   Double_t comb_A_bbbb_bbtautau_2s_fx3001[15] = {
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
   1400,
   1600};
   Double_t comb_A_bbbb_bbtautau_2s_fy3001[15] = {
   0.3417014,
   0.7324702,
   0.8136455,
   0.6242165,
   0.1257808,
   0.03841639,
   0.02221795,
   0.01480524,
   0.01050898,
   0.008229452,
   0.006525401,
   0.005469537,
   0.004797641,
   0.003733699,
   0.003160022};
   Double_t comb_A_bbbb_bbtautau_2s_felx3001[15] = {
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
   0,
   0,
   0,
   0,
   0};
   Double_t comb_A_bbbb_bbtautau_2s_fely3001[15] = {
   0.1583015,
   0.3393346,
   0.376941,
   0.2891834,
   0.05827099,
   0.01779732,
   0.010293,
   0.006858888,
   0.004868541,
   0.003812493,
   0.00302305,
   0.002533895,
   0.002222623,
   0.001729727,
   0.001463957};
   Double_t comb_A_bbbb_bbtautau_2s_fehx3001[15] = {
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
   0,
   0,
   0,
   0,
   0};
   Double_t comb_A_bbbb_bbtautau_2s_fehy3001[15] = {
   0.3531187,
   0.7289089,
   0.8306903,
   0.6246965,
   0.1279886,
   0.04031558,
   0.02311951,
   0.01529435,
   0.01101182,
   0.008933025,
   0.007234146,
   0.00668152,
   0.005604189,
   0.004526906,
   0.004925069};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(15,comb_A_bbbb_bbtautau_2s_fx3001,comb_A_bbbb_bbtautau_2s_fy3001,comb_A_bbbb_bbtautau_2s_felx3001,comb_A_bbbb_bbtautau_2s_fehx3001,comb_A_bbbb_bbtautau_2s_fely3001,comb_A_bbbb_bbtautau_2s_fehy3001);
   grae->SetName("comb_A_bbbb_bbtautau_2s");
   grae->SetTitle("Graph");

   ci = TColor::GetColor("#ffff00");
   grae->SetFillColor(ci);
   grae->SetFillStyle(1000);

   ci = TColor::GetColor("#ffff00");
   grae->SetLineColor(ci);
   grae->SetMarkerStyle(20);
   grae->SetMarkerSize(1.2);
   
   TH1F *Graph_comb_A_bbbb_bbtautau_2s3001 = new TH1F("Graph_comb_A_bbbb_bbtautau_2s3001","Graph",100,116.1,1734.9);
   Graph_comb_A_bbbb_bbtautau_2s3001->SetMinimum(0.001526459);
   Graph_comb_A_bbbb_bbtautau_2s3001->SetMaximum(1.8086);
   Graph_comb_A_bbbb_bbtautau_2s3001->SetDirectory(0);
   Graph_comb_A_bbbb_bbtautau_2s3001->SetStats(0);
   Graph_comb_A_bbbb_bbtautau_2s3001->SetLineWidth(2);
   Graph_comb_A_bbbb_bbtautau_2s3001->SetMarkerStyle(20);
   Graph_comb_A_bbbb_bbtautau_2s3001->SetMarkerSize(1.2);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetXaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetXaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetXaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetXaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetXaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetXaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetXaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetYaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetYaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetYaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetYaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetYaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetYaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetYaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetZaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetZaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetZaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetZaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetZaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetZaxis()->SetTitleOffset(1);
   Graph_comb_A_bbbb_bbtautau_2s3001->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_comb_A_bbbb_bbtautau_2s3001);
   
   multigraph->Add(grae,"");
   
   Double_t comb_A_bbbb_bbtautau_1s_fx3002[15] = {
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
   1400,
   1600};
   Double_t comb_A_bbbb_bbtautau_1s_fy3002[15] = {
   0.3417014,
   0.7324702,
   0.8136455,
   0.6242165,
   0.1257808,
   0.03841639,
   0.02221795,
   0.01480524,
   0.01050898,
   0.008229452,
   0.006525401,
   0.005469537,
   0.004797641,
   0.003733699,
   0.003160022};
   Double_t comb_A_bbbb_bbtautau_1s_felx3002[15] = {
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
   0,
   0,
   0,
   0,
   0};
   Double_t comb_A_bbbb_bbtautau_1s_fely3002[15] = {
   0.09548663,
   0.2046849,
   0.2273689,
   0.1744339,
   0.03514876,
   0.01073525,
   0.006208687,
   0.004137246,
   0.002936679,
   0.002299676,
   0.001823488,
   0.001528433,
   0.001340675,
   0.001043362,
   0.0008830512};
   Double_t comb_A_bbbb_bbtautau_1s_fehx3002[15] = {
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
   0,
   0,
   0,
   0,
   0};
   Double_t comb_A_bbbb_bbtautau_1s_fehy3002[15] = {
   0.1476645,
   0.3093847,
   0.3500431,
   0.2627456,
   0.05399474,
   0.01683094,
   0.009668892,
   0.006346127,
   0.004530985,
   0.003572582,
   0.002866728,
   0.002494306,
   0.002164125,
   0.001766371,
   0.001778459};
   grae = new TGraphAsymmErrors(15,comb_A_bbbb_bbtautau_1s_fx3002,comb_A_bbbb_bbtautau_1s_fy3002,comb_A_bbbb_bbtautau_1s_felx3002,comb_A_bbbb_bbtautau_1s_fehx3002,comb_A_bbbb_bbtautau_1s_fely3002,comb_A_bbbb_bbtautau_1s_fehy3002);
   grae->SetName("comb_A_bbbb_bbtautau_1s");
   grae->SetTitle("Graph");

   ci = TColor::GetColor("#00ff00");
   grae->SetFillColor(ci);
   grae->SetFillStyle(1000);

   ci = TColor::GetColor("#00ff00");
   grae->SetLineColor(ci);
   grae->SetMarkerStyle(20);
   grae->SetMarkerSize(1.2);
   
   TH1F *Graph_comb_A_bbbb_bbtautau_1s3002 = new TH1F("Graph_comb_A_bbbb_bbtautau_1s3002","Graph",100,116.1,1734.9);
   Graph_comb_A_bbbb_bbtautau_1s3002->SetMinimum(0.002049274);
   Graph_comb_A_bbbb_bbtautau_1s3002->SetMaximum(1.27983);
   Graph_comb_A_bbbb_bbtautau_1s3002->SetDirectory(0);
   Graph_comb_A_bbbb_bbtautau_1s3002->SetStats(0);
   Graph_comb_A_bbbb_bbtautau_1s3002->SetLineWidth(2);
   Graph_comb_A_bbbb_bbtautau_1s3002->SetMarkerStyle(20);
   Graph_comb_A_bbbb_bbtautau_1s3002->SetMarkerSize(1.2);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetXaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetXaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetXaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetXaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetXaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetXaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetXaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetYaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetYaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetYaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetYaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetYaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetYaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetYaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetZaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetZaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetZaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetZaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetZaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetZaxis()->SetTitleOffset(1);
   Graph_comb_A_bbbb_bbtautau_1s3002->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_comb_A_bbbb_bbtautau_1s3002);
   
   multigraph->Add(grae,"");
   
   Double_t comb_A_bbbb_bbtautau_exp_fx5[15] = {
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
   1400,
   1600};
   Double_t comb_A_bbbb_bbtautau_exp_fy5[15] = {
   0.3417014,
   0.7324702,
   0.8136455,
   0.6242165,
   0.1257808,
   0.03841639,
   0.02221795,
   0.01480524,
   0.01050898,
   0.008229452,
   0.006525401,
   0.005469537,
   0.004797641,
   0.003733699,
   0.003160022};
   graph = new TGraph(15,comb_A_bbbb_bbtautau_exp_fx5,comb_A_bbbb_bbtautau_exp_fy5);
   graph->SetName("comb_A_bbbb_bbtautau_exp");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);
   graph->SetLineStyle(7);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(2);
   graph->SetMarkerSize(1.2);
   
   TH1F *Graph_comb_A_bbbb_bbtautau_exp5 = new TH1F("Graph_comb_A_bbbb_bbtautau_exp5","Graph",100,116.1,1734.9);
   Graph_comb_A_bbbb_bbtautau_exp5->SetMinimum(0.00284402);
   Graph_comb_A_bbbb_bbtautau_exp5->SetMaximum(0.894694);
   Graph_comb_A_bbbb_bbtautau_exp5->SetDirectory(0);
   Graph_comb_A_bbbb_bbtautau_exp5->SetStats(0);
   Graph_comb_A_bbbb_bbtautau_exp5->SetLineWidth(2);
   Graph_comb_A_bbbb_bbtautau_exp5->SetMarkerStyle(20);
   Graph_comb_A_bbbb_bbtautau_exp5->SetMarkerSize(1.2);
   Graph_comb_A_bbbb_bbtautau_exp5->GetXaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_exp5->GetXaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_exp5->GetXaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_exp5->GetXaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_exp5->GetXaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_exp5->GetXaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_exp5->GetXaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_exp5->GetYaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_exp5->GetYaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_exp5->GetYaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_exp5->GetYaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_exp5->GetYaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_exp5->GetYaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_exp5->GetYaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_exp5->GetZaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_exp5->GetZaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_exp5->GetZaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_exp5->GetZaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_exp5->GetZaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_exp5->GetZaxis()->SetTitleOffset(1);
   Graph_comb_A_bbbb_bbtautau_exp5->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_comb_A_bbbb_bbtautau_exp5);
   
   multigraph->Add(graph,"");
   
   Double_t comb_A_bbbb_bbtautau_obs_fx6[15] = {
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
   1400,
   1600};
   Double_t comb_A_bbbb_bbtautau_obs_fy6[15] = {
   0.6645857,
   0.9306523,
   0.52651,
   0.5409974,
   0.06116032,
   0.03907029,
   0.01476881,
   0.01808779,
   0.01715156,
   0.01720975,
   0.01450556,
   0.01755806,
   0.01007051,
   0.008126498,
   0.00528068};
   graph = new TGraph(15,comb_A_bbbb_bbtautau_obs_fx6,comb_A_bbbb_bbtautau_obs_fy6);
   graph->SetName("comb_A_bbbb_bbtautau_obs");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(20);
   graph->SetMarkerSize(0.96);
   
   TH1F *Graph_comb_A_bbbb_bbtautau_obs6 = new TH1F("Graph_comb_A_bbbb_bbtautau_obs6","Graph",100,116.1,1734.9);
   Graph_comb_A_bbbb_bbtautau_obs6->SetMinimum(0.004752612);
   Graph_comb_A_bbbb_bbtautau_obs6->SetMaximum(1.02319);
   Graph_comb_A_bbbb_bbtautau_obs6->SetDirectory(0);
   Graph_comb_A_bbbb_bbtautau_obs6->SetStats(0);
   Graph_comb_A_bbbb_bbtautau_obs6->SetLineWidth(2);
   Graph_comb_A_bbbb_bbtautau_obs6->SetMarkerStyle(20);
   Graph_comb_A_bbbb_bbtautau_obs6->SetMarkerSize(1.2);
   Graph_comb_A_bbbb_bbtautau_obs6->GetXaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_obs6->GetXaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_obs6->GetXaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_obs6->GetXaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_obs6->GetXaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_obs6->GetXaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_obs6->GetXaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_obs6->GetYaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_obs6->GetYaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_obs6->GetYaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_obs6->GetYaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_obs6->GetYaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_obs6->GetYaxis()->SetTitleOffset(1.4);
   Graph_comb_A_bbbb_bbtautau_obs6->GetYaxis()->SetTitleFont(42);
   Graph_comb_A_bbbb_bbtautau_obs6->GetZaxis()->SetNdivisions(505);
   Graph_comb_A_bbbb_bbtautau_obs6->GetZaxis()->SetLabelFont(42);
   Graph_comb_A_bbbb_bbtautau_obs6->GetZaxis()->SetLabelOffset(0.01);
   Graph_comb_A_bbbb_bbtautau_obs6->GetZaxis()->SetLabelSize(0.05);
   Graph_comb_A_bbbb_bbtautau_obs6->GetZaxis()->SetTitleSize(0.05);
   Graph_comb_A_bbbb_bbtautau_obs6->GetZaxis()->SetTitleOffset(1);
   Graph_comb_A_bbbb_bbtautau_obs6->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_comb_A_bbbb_bbtautau_obs6);
   
   multigraph->Add(graph,"");
   multigraph->Draw("a3 l");
   multigraph->GetXaxis()->SetLimits(13.55, 5237.45);
   multigraph->GetXaxis()->SetTitle("m_{X} [GeV]");
   multigraph->GetXaxis()->SetRange(5,39);
   multigraph->GetXaxis()->SetMoreLogLabels();
   multigraph->GetXaxis()->SetNdivisions(505);
   multigraph->GetXaxis()->SetLabelFont(42);
   multigraph->GetXaxis()->SetLabelOffset(0.01);
   multigraph->GetXaxis()->SetLabelSize(0.05);
   multigraph->GetXaxis()->SetTitleSize(0.045);
   multigraph->GetXaxis()->SetTitleOffset(1.4);
   multigraph->GetXaxis()->SetTitleFont(42);
   multigraph->GetYaxis()->SetTitle("#sigma(pp #rightarrow X #rightarrow HH) [pb]");
   multigraph->GetYaxis()->SetNdivisions(505);
   multigraph->GetYaxis()->SetLabelFont(42);
   multigraph->GetYaxis()->SetLabelOffset(0.01);
   multigraph->GetYaxis()->SetLabelSize(0.05);
   multigraph->GetYaxis()->SetTitleSize(0.045);
   multigraph->GetYaxis()->SetTitleOffset(1.6);
   multigraph->GetYaxis()->SetTitleFont(42);
   
   TH1F *limits_copy__1 = new TH1F("limits_copy__1","",100,13.55,5237.45);
   limits_copy__1->SetMinimum(0.0004085493);
   limits_copy__1->SetMaximum(18.99091);
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
   limits_copy__2->GetXaxis()->SetTitle("m_{X} [GeV]");
   limits_copy__2->GetXaxis()->SetRange(5,39);
   limits_copy__2->GetXaxis()->SetMoreLogLabels();
   limits_copy__2->GetXaxis()->SetNdivisions(505);
   limits_copy__2->GetXaxis()->SetLabelFont(42);
   limits_copy__2->GetXaxis()->SetLabelOffset(0.01);
   limits_copy__2->GetXaxis()->SetLabelSize(0.05);
   limits_copy__2->GetXaxis()->SetTitleSize(0.045);
   limits_copy__2->GetXaxis()->SetTitleOffset(1.4);
   limits_copy__2->GetXaxis()->SetTitleFont(42);
   limits_copy__2->GetYaxis()->SetTitle("#sigma(pp #rightarrow X #rightarrow HH) [pb]");
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
   
   Double_t bbbb_exp_fx7[23] = {
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
   Double_t bbbb_exp_fy7[23] = {
   3.607396,
   6.977636,
   5.024684,
   3.057476,
   0.302884,
   0.1031709,
   0.04971187,
   0.02669545,
   0.01691946,
   0.01168353,
   0.008499439,
   0.006465577,
   0.005302704,
   0.004499932,
   0.003857605,
   0.003384238,
   0.003205164,
   0.002498645,
   0.002022435,
   0.001485208,
   0.001230974,
   0.001286988,
   0.001447981};
   graph = new TGraph(23,bbbb_exp_fx7,bbbb_exp_fy7);
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
   
   TH1F *Graph_Graph_bbbb_exp17 = new TH1F("Graph_Graph_bbbb_exp17","Graph",100,0,5474.9);
   Graph_Graph_bbbb_exp17->SetMinimum(0.001107877);
   Graph_Graph_bbbb_exp17->SetMaximum(7.675277);
   Graph_Graph_bbbb_exp17->SetDirectory(0);
   Graph_Graph_bbbb_exp17->SetStats(0);
   Graph_Graph_bbbb_exp17->SetLineWidth(2);
   Graph_Graph_bbbb_exp17->SetMarkerStyle(20);
   Graph_Graph_bbbb_exp17->SetMarkerSize(1.2);
   Graph_Graph_bbbb_exp17->GetXaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_exp17->GetXaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_exp17->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_exp17->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_exp17->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_exp17->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbbb_exp17->GetXaxis()->SetTitleFont(42);
   Graph_Graph_bbbb_exp17->GetYaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_exp17->GetYaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_exp17->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_exp17->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_exp17->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_exp17->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbbb_exp17->GetYaxis()->SetTitleFont(42);
   Graph_Graph_bbbb_exp17->GetZaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_exp17->GetZaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_exp17->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_exp17->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_exp17->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_exp17->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_bbbb_exp17->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_bbbb_exp17);
   
   graph->Draw("l");
   
   Double_t bbtautau_exp_fx8[19] = {
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
   Double_t bbtautau_exp_fy8[19] = {
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
   graph = new TGraph(19,bbtautau_exp_fx8,bbtautau_exp_fy8);
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
   
   TH1F *Graph_Graph_bbtautau_exp38 = new TH1F("Graph_Graph_bbtautau_exp38","Graph",100,116.1,1734.9);
   Graph_Graph_bbtautau_exp38->SetMinimum(0.01064822);
   Graph_Graph_bbtautau_exp38->SetMaximum(0.9108922);
   Graph_Graph_bbtautau_exp38->SetDirectory(0);
   Graph_Graph_bbtautau_exp38->SetStats(0);
   Graph_Graph_bbtautau_exp38->SetLineWidth(2);
   Graph_Graph_bbtautau_exp38->SetMarkerStyle(20);
   Graph_Graph_bbtautau_exp38->SetMarkerSize(1.2);
   Graph_Graph_bbtautau_exp38->GetXaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_exp38->GetXaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_exp38->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_exp38->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_exp38->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_exp38->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbtautau_exp38->GetXaxis()->SetTitleFont(42);
   Graph_Graph_bbtautau_exp38->GetYaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_exp38->GetYaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_exp38->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_exp38->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_exp38->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_exp38->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbtautau_exp38->GetYaxis()->SetTitleFont(42);
   Graph_Graph_bbtautau_exp38->GetZaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_exp38->GetZaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_exp38->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_exp38->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_exp38->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_exp38->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_bbtautau_exp38->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_bbtautau_exp38);
   
   graph->Draw("l ");
   
   Double_t comb_A_bbbb_bbtautau_exp_fx9[15] = {
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
   1400,
   1600};
   Double_t comb_A_bbbb_bbtautau_exp_fy9[15] = {
   0.3417014,
   0.7324702,
   0.8136455,
   0.6242165,
   0.1257808,
   0.03841639,
   0.02221795,
   0.01480524,
   0.01050898,
   0.008229452,
   0.006525401,
   0.005469537,
   0.004797641,
   0.003733699,
   0.003160022};
   graph = new TGraph(15,comb_A_bbbb_bbtautau_exp_fx9,comb_A_bbbb_bbtautau_exp_fy9);
   graph->SetName("comb_A_bbbb_bbtautau_exp");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);
   graph->SetLineStyle(7);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(2);
   graph->SetMarkerSize(1.2);
   
   TH1F *Graph_Graph_comb_A_bbbb_bbtautau_exp59 = new TH1F("Graph_Graph_comb_A_bbbb_bbtautau_exp59","Graph",100,116.1,1734.9);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->SetMinimum(0.00284402);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->SetMaximum(0.894694);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->SetDirectory(0);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->SetStats(0);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->SetLineWidth(2);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->SetMarkerStyle(20);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->SetMarkerSize(1.2);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetXaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetXaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetXaxis()->SetTitleFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetYaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetYaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetYaxis()->SetTitleFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetZaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetZaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_comb_A_bbbb_bbtautau_exp59->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_comb_A_bbbb_bbtautau_exp59);
   
   graph->Draw("l ");
   
   Double_t bbbb_obs_fx10[23] = {
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
   Double_t bbbb_obs_fy10[23] = {
   4.676847,
   10.61901,
   8.777929,
   4.061728,
   0.1773091,
   0.09213873,
   0.02864067,
   0.02339879,
   0.01248848,
   0.01250459,
   0.00704885,
   0.01700356,
   0.009811303,
   0.005882546,
   0.007906132,
   0.007532925,
   0.005420942,
   0.003475117,
   0.002971425,
   0.002058782,
   0.001213788,
   0.002717123,
   0.001262291};
   graph = new TGraph(23,bbbb_obs_fx10,bbbb_obs_fy10);
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
   
   TH1F *Graph_Graph_bbbb_obs210 = new TH1F("Graph_Graph_bbbb_obs210","Graph",100,0,5474.9);
   Graph_Graph_bbbb_obs210->SetMinimum(0.001092409);
   Graph_Graph_bbbb_obs210->SetMaximum(11.68079);
   Graph_Graph_bbbb_obs210->SetDirectory(0);
   Graph_Graph_bbbb_obs210->SetStats(0);
   Graph_Graph_bbbb_obs210->SetLineWidth(2);
   Graph_Graph_bbbb_obs210->SetMarkerStyle(20);
   Graph_Graph_bbbb_obs210->SetMarkerSize(1.2);
   Graph_Graph_bbbb_obs210->GetXaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_obs210->GetXaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_obs210->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_obs210->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_obs210->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_obs210->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbbb_obs210->GetXaxis()->SetTitleFont(42);
   Graph_Graph_bbbb_obs210->GetYaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_obs210->GetYaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_obs210->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_obs210->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_obs210->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_obs210->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbbb_obs210->GetYaxis()->SetTitleFont(42);
   Graph_Graph_bbbb_obs210->GetZaxis()->SetNdivisions(505);
   Graph_Graph_bbbb_obs210->GetZaxis()->SetLabelFont(42);
   Graph_Graph_bbbb_obs210->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbbb_obs210->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_bbbb_obs210->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_bbbb_obs210->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_bbbb_obs210->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_bbbb_obs210);
   
   graph->Draw("l ");
   
   Double_t bbtautau_obs_fx11[19] = {
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
   Double_t bbtautau_obs_fy11[19] = {
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
   graph = new TGraph(19,bbtautau_obs_fx11,bbtautau_obs_fy11);
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
   
   TH1F *Graph_Graph_bbtautau_obs411 = new TH1F("Graph_Graph_bbtautau_obs411","Graph",100,116.1,1734.9);
   Graph_Graph_bbtautau_obs411->SetMinimum(0.01937106);
   Graph_Graph_bbtautau_obs411->SetMaximum(0.9885997);
   Graph_Graph_bbtautau_obs411->SetDirectory(0);
   Graph_Graph_bbtautau_obs411->SetStats(0);
   Graph_Graph_bbtautau_obs411->SetLineWidth(2);
   Graph_Graph_bbtautau_obs411->SetMarkerStyle(20);
   Graph_Graph_bbtautau_obs411->SetMarkerSize(1.2);
   Graph_Graph_bbtautau_obs411->GetXaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_obs411->GetXaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_obs411->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_obs411->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_obs411->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_obs411->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbtautau_obs411->GetXaxis()->SetTitleFont(42);
   Graph_Graph_bbtautau_obs411->GetYaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_obs411->GetYaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_obs411->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_obs411->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_obs411->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_obs411->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_bbtautau_obs411->GetYaxis()->SetTitleFont(42);
   Graph_Graph_bbtautau_obs411->GetZaxis()->SetNdivisions(505);
   Graph_Graph_bbtautau_obs411->GetZaxis()->SetLabelFont(42);
   Graph_Graph_bbtautau_obs411->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_bbtautau_obs411->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_bbtautau_obs411->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_bbtautau_obs411->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_bbtautau_obs411->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_bbtautau_obs411);
   
   graph->Draw("l ");
   
   Double_t comb_A_bbbb_bbtautau_obs_fx12[15] = {
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
   1400,
   1600};
   Double_t comb_A_bbbb_bbtautau_obs_fy12[15] = {
   0.6645857,
   0.9306523,
   0.52651,
   0.5409974,
   0.06116032,
   0.03907029,
   0.01476881,
   0.01808779,
   0.01715156,
   0.01720975,
   0.01450556,
   0.01755806,
   0.01007051,
   0.008126498,
   0.00528068};
   graph = new TGraph(15,comb_A_bbbb_bbtautau_obs_fx12,comb_A_bbbb_bbtautau_obs_fy12);
   graph->SetName("comb_A_bbbb_bbtautau_obs");
   graph->SetTitle("Graph");
   graph->SetFillStyle(1000);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(20);
   graph->SetMarkerSize(0.96);
   
   TH1F *Graph_Graph_comb_A_bbbb_bbtautau_obs612 = new TH1F("Graph_Graph_comb_A_bbbb_bbtautau_obs612","Graph",100,116.1,1734.9);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->SetMinimum(0.004752612);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->SetMaximum(1.02319);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->SetDirectory(0);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->SetStats(0);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->SetLineWidth(2);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->SetMarkerStyle(20);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->SetMarkerSize(1.2);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetXaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetXaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetXaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetXaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetXaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetXaxis()->SetTitleOffset(1.4);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetXaxis()->SetTitleFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetYaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetYaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetYaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetYaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetYaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetYaxis()->SetTitleOffset(1.4);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetYaxis()->SetTitleFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetZaxis()->SetNdivisions(505);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetZaxis()->SetLabelFont(42);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetZaxis()->SetLabelOffset(0.01);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetZaxis()->SetLabelSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetZaxis()->SetTitleSize(0.05);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetZaxis()->SetTitleOffset(1);
   Graph_Graph_comb_A_bbbb_bbtautau_obs612->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph_comb_A_bbbb_bbtautau_obs612);
   
   graph->Draw("lp ");
   TLatex *   tex = new TLatex(0.45,0.88,"ATLAS");
tex->SetNDC();
   tex->SetTextFont(72);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.5924019,0.88,"Internal");
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
   limits_copy__3->GetXaxis()->SetTitle("m_{X} [GeV]");
   limits_copy__3->GetXaxis()->SetRange(5,39);
   limits_copy__3->GetXaxis()->SetMoreLogLabels();
   limits_copy__3->GetXaxis()->SetNdivisions(505);
   limits_copy__3->GetXaxis()->SetLabelFont(42);
   limits_copy__3->GetXaxis()->SetLabelOffset(0.01);
   limits_copy__3->GetXaxis()->SetLabelSize(0.05);
   limits_copy__3->GetXaxis()->SetTitleSize(0.045);
   limits_copy__3->GetXaxis()->SetTitleOffset(1.4);
   limits_copy__3->GetXaxis()->SetTitleFont(42);
   limits_copy__3->GetYaxis()->SetTitle("#sigma(pp #rightarrow X #rightarrow HH) [pb]");
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
   entry=leg->AddEntry("NULL","Combined (exp.)","l");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("comb_A_bbbb_bbtautau_1s","Comb. #pm1#sigma (exp.)","f");

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
   entry=leg->AddEntry("comb_A_bbbb_bbtautau_2s","Comb. #pm2#sigma (exp.)","f");

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

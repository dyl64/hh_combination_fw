from quickstats.components import AnalysisBase
from pdb import set_trace

##filename = "../../FullRun2Workspaces/original/PUBHL2022/v12/bbyy/WS-yybb-nonresonant_BDT_h026_v10_3000ifb_kl1p0_mu/WS-yybb-nonresonant_BDT_h026_v10_3000ifb_kl1p0_mu.root"
#filename = "../../FullRun2Workspaces/original/PUBHL2022/v12/bbyy/WS-yybb-nonresonant_BDT_h026_v10_3000ifb_kl1p0_mu/WS-yybb-nonresonant_BDT_h026_v10_3000ifb_kl1p0_mu.root"
#data_name = "combData"
#poi_name = "mu_XS_HH"
#
#
#filename = "../../FullRun2Workspaces/original/PUBHL2022/v12/bbtautau/baseline/3000ifb.root"
#data_name = "asimovData"
#poi_name = "SigXsecOverSM"
#
#filename = "../../../workspaceCombiner/bbtautau.root"
#filename = "../../../workspaceCombiner/bbyy.root"
#filename = "output/20220919_proj_all/lumi3000ifb/theo_exp_baseline/SM/rescaled/nonres/bbbb/0.root"
#data_name = "combData"
#poi_name = "xsec_br"


filename = "../../FullRun2Workspaces/original/PUBHL2022/20220919_proj_all/lumi3000ifb/theo_exp_baseline/bbbb/nonres/0_kl.root"
data_name = "asimovData"
poi_name = "mu_HH"

analysis = AnalysisBase(filename, data_name=data_name, poi_name=poi_name, verbosity="DEBUG")
analysis.setup_parameters(fix_param="k2V=1", profile_param="mu_HH=-10000_10000")

mu = 0
do_minos = True
scan_str= 'sm2'
analysis.generate_standard_asimov(asimov_types=[-2], asimov_names=[f"asimovData_1_NP_Nominal_{scan_str}"])
analysis.set_data(f"asimovData_1_NP_Nominal_{scan_str}")
fit_result = analysis.nll_fit(poi_val=mu, mode=1, do_minos=do_minos)
print(fit_result)

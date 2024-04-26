import numpy as np
import json
import argparse

SYST_BLOCKS = {
    "nominal": [],
    "fix_all": ["ATLAS_*", "THEO_*", "gamma_*"],
    "all_syst": ["gamma_*"],
    "stat_only": ["ATLAS_*", "THEO_*"],
    "bbbb": ["ATLAS_bbbb_*"],
    "bbtautau": ["ATLAS_bbtautau_*"],
    "met": ["ATLAS_MET_*"],
    "theory": ["THEO_*"],
    "ftag": ["ATLAS_FTAG_*", "ATLAS_FT_*"],
    "jet": ["ATLAS_JET_*"],
    "tau": ["ATLAS_TAUS_*"],
    # "e_gamma": ["ATLAS_EG_*", "ATLAS_EL_*"], # used for merging e_gamma_photon
    # "ml": ["ATLAS_ml_*"], # used for merging ml_muon
    # "prw": ["ATLAS_PU_PRW_DATASF"], # used for merging prw_lumi
    # upper error larger than nominal, so merge
    # "bbll": ["ATLAS_bbll_*"],  # merged to bbllyy
    # "bbyy": ["ATLAS_bbyy_*"],  # merged to bbllyy
    # "photon": ["ATLAS_PH_*"],  # merged to e_gamma_photon
    # "muon": ["ATLAS_MUON_*"],  # merged to ml_muon
    # "lumi": ["ATLAS_LUMI_*"],  # merged to prw_lumi
    # merged alternatives
    "e_gamma_photon": ["ATLAS_EG_*", "ATLAS_EL_*", "ATLAS_PH_*"],
    "bbllyy": ["ATLAS_bbll_*", "ATLAS_bbyy_*"],
    "ml_muon": ["ATLAS_ml_*", "ATLAS_MUON_*"],
    "prw_lumi": ["ATLAS_PU_PRW_DATASF", "ATLAS_LUMI_*"],
}
TABLE_TITLES = {
    "nominal": "None (nominal fit)",
    "fix_all": "Total syst.",
    "all_syst": "MC stat.",
    "stat_only": "No MC stat.",
    "bbbb": r"\bbbb",
    "bbtautau": r"\bbtt",
    "met": r"$E_\mathrm{T}^\mathrm{miss}$",
    "theory": "Theory",
    "ftag": "FTAG CP",
    "jet": "Jet CP",
    "tau": "Tau CP",
    "e_gamma_photon": r"$e/\gamma$ CP",
    "bbllyy": r"\bbll and \bbtt",
    "ml_muon": "Muon CP and \ml",
    "prw_lumi": "Pile-up reweighting",
}


def get_parser():
    p = argparse.ArgumentParser(
        description="Run fits for hh4b analysis", allow_abbrev=False
    )
    p.add_argument(
        "-i",
        "--in_dir",
        dest="in_dir",
        default=None,
        required=True,
        help="Directory where TRExFitter workspaces are stored",
    )
    p.add_argument(
        "-o",
        "--out_dir",
        dest="out_dir",
        default=None,
        required=True,
        help="Directory where fit outputs will be saved",
    )
    return p


def get_err(filename):
    with open(filename, "r") as f:
        results = json.load(f)
    return results["pois"]["errorlo_postfit"][0], results["pois"]["errorhi_postfit"][0]


def run_fits(in_dir, out_dir):
    # run nominal fit and get total uncertainty
    nominal_fit = (
        "quickstats likelihood_fit "
        f"-i {in_dir}/HH_combined.root "
        "-d asimovData_muhat_NP_Profile "
        "--snapshot asimovData_muhat_NP_Profile "
        "-r mu=1_-10_10 "
        '-f "ATLAS_KAPPA_REWEIGHTING_*" '
        "--num_cpu 6 "
        "--save --minos --pois mu"
    )
    final_cmd = ""
    for block in SYST_BLOCKS:
        # run fit with groups of NPs fixed
        to_fix = ",".join(SYST_BLOCKS[block])
        out_name = f"{out_dir}/{block}.json"
        cmd = nominal_fit + f" --outname {out_name}"
        if to_fix != "":
            cmd += f' -f "{to_fix}"'
        print(cmd)
        final_cmd += cmd + ";"
    print(final_cmd)


def get_table_start():
    return (
        r"\begin{table}[ht]""\n"
        r"    \centering""\n"
        r"    \caption{""\n"
        r"        Impact of systematic uncertainties grouped by similar sources of uncertainty.""\n"
        r"        The uncertainty on the POI $\mu_{\HH}$ is evaluated with Minos.""\n"
        r"    }""\n"
        r"    \resizebox{\columnwidth}{!}{""\n"
        r"    \begin{tabular}{lcc""\n"
        r"        S[table-format=4.4, round-mode = figures, round-precision = 4]""\n"
        r"        S[table-format=4.4, round-mode = figures, round-precision = 4]""\n"
        r"        S[table-format=4.4, round-mode = figures, round-precision = 4]""\n"
        r"        }""\n"
        r"    \toprule""\n"
        r"    {Group} & {Nuisance parameters fixed} & {POI uncertainty (68\%)} & {Lower bound} & {Upper bound} \\""\n"
        r"            &                             &                          & {impact (\%)} & {impact (\%)} \\""\n"
        r"    \midrule""\n"
    )


def get_table_end():
    return (
        r"    \bottomrule""\n"
        r"    \end{tabular}""\n"
        r"    }""\n"
        r"    \label{tab:systematics_impact}""\n"
        r"\end{table}""\n"
    )


def compare_uncertainties(results_path):
    # prepare final table
    table = get_table_start()
    err_nom_lo, err_nom_hi = get_err(f"{results_path}/nominal.json")
    for block in SYST_BLOCKS:
        err_block_lo, err_block_hi = get_err(f"{results_path}/{block}.json")
        # subtract in quadrature, see https://twiki.cern.ch/twiki/pub/AtlasProtected/ATLASStatisticsFAQ/pllguide_draft.pdf
        err_syst_lo = (
            100 * np.sqrt(err_nom_lo**2 - err_block_lo**2) / abs(err_nom_lo)
        )
        err_syst_hi = (
            100 * np.sqrt(err_nom_hi**2 - err_block_hi**2) / abs(err_block_hi)
        )
        print(
            block,
            "uncertainty:",
            f"(errlo = {err_block_lo:.4f}, errhi = {err_block_hi:.4f})",
            "impact_lo",
            f"{err_syst_lo:.4f}",
            "impact_hi",
            f"{err_syst_hi:.4f}",
        )
        NPs = r"\texttt{" + ", ".join(SYST_BLOCKS[block]).replace("_", r"\_") + r"}"
        if block == "nominal":
            table += f"        {TABLE_TITLES[block]} & N/A & [{err_block_lo:.4f}, {err_block_hi:.4f}] & 100.0 & 100.0 \\\\\n"
        else:
            table += f"        {TABLE_TITLES[block]} & {NPs} & [{err_block_lo:.4f}, {err_block_hi:.4f}] & {err_syst_lo:.4f} & {err_syst_hi:.4f} \\\\\n"
        if block == "fix_all":
            table += r"    \midrule""\n"
    table += get_table_end()
    print(table)


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    # required arguments
    INPUT_WS_PATH, OUTPUTPATH = args.in_dir, args.out_dir
    run_fits(INPUT_WS_PATH, OUTPUTPATH)
    compare_uncertainties(OUTPUTPATH)

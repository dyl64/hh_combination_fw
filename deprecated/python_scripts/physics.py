#!/usr/bin/env python


# - Numerical data taken from
# - CERN Yellow Report:
# - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR


# - mH = 125.09 GeV
br_h_WW     = 0.2152
br_h_bb     = 0.5809
br_h_tautau = 0.06256
br_h_yy     = 2.270e-03

br_hh_bbbb     = br_h_bb*br_h_bb
br_hh_bbtautau = br_h_bb*br_h_tautau*2.0
br_hh_bbyy     = br_h_bb*br_h_yy*2.0
br_hh_WWyy     = br_h_WW*br_h_yy*2.0
br_hh_bbWW     = br_h_bb*br_h_WW*2.0
br_hh_WWWW     = br_h_WW*br_h_WW

br_h = {
        'bb'     : br_h_bb,
        'tautau' : br_h_tautau,
        'yy'     : br_h_yy,
        'WW'     : br_h_WW
       }


br_hh = {
         'bbbb'     : br_hh_bbbb,
         'bbtautau' : br_hh_bbtautau,
         'bbyy'     : br_hh_bbyy,
         'WWyy'     : br_hh_WWyy,
         'bbWW'     : br_hh_bbWW,
         'WWWW'     : br_hh_WWWW
        }

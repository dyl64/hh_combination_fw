// https://gitlab.cern.ch/atlas-phys/exot/CommonStatTools/-/blob/master/getGlobalP0.C
// Rui Zhang 6.2020
// rui.zhang@cern.ch

/// \file
/// Functions to compute the global significance

#include <iostream>
#include <TMath.h>
#include <RooStats/RooStatsUtils.h>

/// Compute the global p0
/// \param[in] maximumSignificance maximum local significance, in number of gaussian sigmas
/// \param[in] nCrossings number of crossings
/// \param[in] debugLevel (0 = verbose, 1 = debug, 2 = warning, 3 = error, 4 = fatal, 5 = silent)
/// \param[out] p0 global p-value of the background-only hypothesis
///
/// See ATL-PHYS-PUB-2011-011 for details.
void global_pvalue(Double_t p0, UInt_t nCrossings, Double_t z_ref = 0) // z_ref in sigma
{
   // reference: https://cds.cern.ch/record/1375842/files/ATL-PHYS-PUB-2011-011.pdf
   // CMS: https://cds.cern.ch/record/1406347/files/HIG-11-032-pas.pdf
   // p (global) = p0 (local) + N*exp( - (q0 - q_ref)/2.)
   // q0: test-statistics for local max significance, q0=Z0*Z0 asymptotically
   // q_ref: reference point, eg. 1sigma := z_ref*z_ref
   // N: up-crossing points at reference point q_ref (down corssing if looking at p-value plot)

   const Double_t maximumSignificance = RooStats::PValueToSignificance (p0);
//    const Double_t p0 = RooStats::SignificanceToPValue(maximumSignificance);
   const Double_t q0 = TMath::Power(maximumSignificance, 2);

   const Double_t pglobal = ((Double_t)nCrossings) * TMath::Exp(-(q0 - z_ref*z_ref) / 2.) + p0;
   const Double_t pglobal_error = TMath::Sqrt((Double_t)nCrossings) * TMath::Exp(-(q0 - z_ref*z_ref) / 2.);
//    std::cout << TMath::Sqrt((Double_t)nCrossings) << " * exp (-(" << q0 << " - " << z_ref <<" **2 ) / 2) = " << pglobal_error << std::endl;

   const Double_t nsigglobal = RooStats::PValueToSignificance(pglobal);
   const Double_t nsigglobal_error_up = nsigglobal - RooStats::PValueToSignificance(pglobal+pglobal_error);
   const Double_t nsigglobal_error_dn = RooStats::PValueToSignificance(pglobal-pglobal_error) - nsigglobal;

    std::cout << " N crossing :  " << nCrossings << " z_ref: " << z_ref << std::endl;
    std::cout << " Local p-value :  " << p0 << " significance: " << maximumSignificance << std::endl;
    std::cout << " Global p-value:  " << pglobal <<" +/- " << pglobal_error << " significance: " << nsigglobal <<" + " << nsigglobal_error_up << " - " << nsigglobal_error_dn << std::endl;

}

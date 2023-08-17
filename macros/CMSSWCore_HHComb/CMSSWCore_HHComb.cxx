#ifndef __CMSSWCore_HHComb_CXX__
#define __CMSSWCore_HHComb_CXX__

#include "CloseCoutSentry.cc"
#include "VerticalInterpHistPdf.cc"
#include "RooSimultaneousOpt.cc"
#include "CMSHistSum.cc"
#include "RooSpline1D.cc"
#include "RooBernsteinFast.cc"
#include "HZZ2L2QRooPdfs.cc"
#include "RooMultiPdf.cxx"
#include "FastTemplate_Old.cc"
#include "SimpleCacheSentry.cc"
#include "CachingNLL.cc"
#include "CachingMultiPdf.cc"
#include "CascadeMinimizer.cc"
#include "vectorized.cc"
#include "VectorizedHistFactoryPdfs.cc"
#include "VectorizedGaussian.cc"
#include "CMSHistFunc.cc"
#include "CMSHistFuncWrapper.cc"
#include "CMSHistErrorPropagator.cc"
#include "ToyMCSamplerOpt.cc"
#include "Significance.cc"
#include "Logger.cc"
#include "utils.cc"
#include "ProfilingTools.cc"
#include "Combine.cc"
#include "AsimovUtils.cc"
#include "AsymptoticLimits.cc"
#include "ProfiledLikelihoodRatioTestStatExt.cc"
#include "SimpleGaussianConstraint.cc"
#include "SimpleConstraintGroup.cc"
#include "SimplePoissonConstraint.cc"
#include "SimpleProdPdf.cc"
#include "VectorizedSimplePdfs.cc"
#include "VectorizedCB.cc"
#include "HGGRooPdfs.cc"
#include "RooCheapProduct.cc"
#include "ProcessNormalization.cc"

#include "TObject.h"
class CMSSWCore_HHComb: public TObject {
    public:
    protected:
    private:
        ClassDef(CMSSWCore_HHComb,1)
    };

ClassImp(CMSSWCore_HHComb)
    
    
#ifdef __CINT__

#pragma link off all functions;
#pragma link off all globals;
#pragma link off all classes;

#pragma link C++ nestedclasses;
#pragma link C++ nestedtypedefs;

#pragma link C++ namespace vectorized;

#pragma link C++ class VerticalInterpHistPdf+;
#pragma link C++ class FastHisto+;
#pragma link C++ class FastHisto2D+;
#pragma link C++ class FastHisto3D+;    
#pragma link C++ class FastVerticalInterpHistPdf+;
#pragma link C++ class FastVerticalInterpHistPdfBase+;
#pragma link C++ class FastVerticalInterpHistPdf2D+;
#pragma link C++ class FastVerticalInterpHistPdf3D+;
#pragma link C++ class FastVerticalInterpHistPdf2D2+;
#pragma link C++ class FastVerticalInterpHistPdf2+;
#pragma link C++ class FastVerticalInterpHistPdf2Base+;
#pragma link C++ class RooSimultaneousOpt+;
#pragma link C++ class CMSHistSum+;
#pragma link C++ class RooSpline1D+;
#pragma link C++ class RooMultiPdf+;
#pragma link C++ class FastTemplate+;
#pragma link C++ class SimpleCacheSentry+;
#pragma link C++ class CachingSimNLL+;
#pragma link C++ class CascadeMinimizer+;
#pragma link C++ class CachingPiecewiseInterpolation+;
#pragma link C++ class Logger+;
#pragma link C++ class VectorizedGaussian+;
#pragma link C++ class VectorizedExponential+;
#pragma link C++ class CMSHistFuncWrapper+;
#pragma link C++ class Significance+;
#pragma link C++ class CloseCoutSentry+;
#pragma link C++ class SimpleGaussianConstraint+;
#pragma link C++ class SimpleConstraintGroup+;
#pragma link C++ class CMSHistErrorPropagator+;
#pragma link C++ class CMSHistFunc+;
#pragma link C++ class CachingMultiPdf+;
#pragma link C++ class SimplePoissonConstraint+;
#pragma link C++ class SimpleProdPdf+;
#pragma link C++ class ToyMCSamplerOpt+;
#pragma link C++ class VectorizedCBShape+;
#pragma link C++ class RooPower+;
#pragma link C++ class RooCheapProduct+;
#pragma link C++ class ProcessNormalization+;
#pragma link C++ class RooBernsteinFast<1>+;
#pragma link C++ class RooBernsteinFast<2>+;
#pragma link C++ class RooBernsteinFast<3>+;
#pragma link C++ class RooBernsteinFast<4>+;
#pragma link C++ class RooBernsteinFast<5>+;
#pragma link C++ class RooBernsteinFast<6>+;
#pragma link C++ class RooBernsteinFast<7>+;
#pragma link C++ class RooDoubleCB+;
#pragma link C++ class RooCB+;
#pragma link C++ class RooFermi+;
#pragma link C++ class RooRelBW+;
#pragma link C++ class RooRelBWUF+;
#pragma link C++ class RooRelBWUFParamWidth+;
#pragma link C++ class RooRelBWHighMass+;
#pragma link C++ class RooRelBW1+;
#pragma link C++ class Triangle+;
#pragma link C++ class RooLevelledExp+;
#endif
    
    
#endif

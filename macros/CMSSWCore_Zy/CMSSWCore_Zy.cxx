#ifndef __CMSSWCore_Zy_CXX__
#define __CMSSWCore_Zy_CXX__

#include "ProcessNormalization.cxx"
#include "RooMultiPdf.cxx"
#include "RooGaussStepBernstein.cxx"
#include "Accumulators.h"
#include "CMSHggFormula.cxx"
#include "CMSHistErrorPropagator.cxx"
#include "CMSHistFunc.cxx"
#include "CMSHistFuncWrapper.cxx"
#include "CMSHistV.h"
#include "FastTemplate_Old.cxx"
#include "GBRMath.cxx"
#include "HGGRooPdfs.cxx"
#include "RooBernsteinFast.cxx"
#include "RooCheapProduct.cxx"
#include "RooDoubleCBFast.cxx"
#include "SimpleCacheSentry.cxx"
#include "SimpleProdPdf.cxx"
#include "VerticalInterpPdf.cxx"
#include "vectorized.cxx"

#include "TObject.h"
class CMSSWCore_Zy: public TObject {
    public:
    protected:
    private:
        ClassDef(CMSSWCore_Zy,1)
    };

ClassImp(CMSSWCore_Zy)
    
    
#ifdef __CINT__

#pragma link off all functions;
#pragma link off all globals;
#pragma link off all classes;

#pragma link C++ nestedclasses;
#pragma link C++ nestedtypedefs;

#pragma link C++ namespace vectorized;

#pragma link C++ class CMSHggFormulaA1+;
#pragma link C++ class CMSHggFormulaA2+;
#pragma link C++ class CMSHggFormulaB1+;
#pragma link C++ class CMSHggFormulaB2+;
#pragma link C++ class CMSHggFormulaC1+;
#pragma link C++ class CMSHggFormulaD1+;
#pragma link C++ class CMSHggFormulaD2+;
#pragma link C++ class CMSHistErrorPropagator+;
#pragma link C++ class CMSHistFunc+;
#pragma link C++ class CMSHistFuncWrapper+;
#pragma link C++ class FastTemplate+;
#pragma link C++ class RooPower+;
#pragma link C++ class ProcessNormalization+;
#pragma link C++ class RooBernsteinFast+;
#pragma link C++ class RooCheapProduct+;
#pragma link C++ class RooDoubleCBFast+;
#pragma link C++ class RooMultiPdf+;
#pragma link C++ class RooGaussStepBernstein+;
#pragma link C++ class SimpleCacheSentry+;
#pragma link C++ class SimpleProdPdf+;
#pragma link C++ class VerticalInterpPdf+;
#pragma link C++ class ProcessNormalization+;  
#pragma link C++ class RooMultiPdf+;
#pragma link C++ class RooGaussStepBernstein+;
    
#endif
    
    
#endif

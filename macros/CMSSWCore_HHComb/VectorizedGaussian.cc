#include "VectorizedGaussian.h"
#include "RooMath.h"
#include "vectorized.h"
#include <RooRealVar.h>
#include <stdexcept>

VectorizedGaussian::VectorizedGaussian(const RooGaussian &gaus, const RooAbsData &data, bool includeZeroWeights)
{
    RooArgSet obs(*data.get());
    if (obs.getSize() != 1) throw std::invalid_argument("Multi-dimensional dataset?");
    RooRealVar *x = dynamic_cast<RooRealVar*>(obs.first());

    Worker w(gaus);
    if (obs.contains(w.xvar())) {
        x_ = dynamic_cast<const RooRealVar*>(& w.xvar());
        mean_ = & w.meanvar();
        sigma_ = & w.sigvar();
    } else if (obs.contains(w.meanvar())) {
        x_ = dynamic_cast<const RooRealVar*>(& w.meanvar());
        mean_ = & w.xvar();
        sigma_ = & w.sigvar();
    } else {
        throw std::invalid_argument("Dataset is not the mean or x of the gaussian");
    }

    xvals_.reserve(data.numEntries());
    for (unsigned int i = 0, n = data.numEntries(); i < n; ++i) {
        obs.assignValueOnly(*data.get(i), true);
        if (data.weight() || includeZeroWeights) xvals_.push_back(x->getVal());        
    }
    work_.resize(xvals_.size());
    work2_.resize(xvals_.size());
}

void VectorizedGaussian::fill(std::vector<Double_t> &out) const {
    // calculate normalizatio integral
    // cannot use constexpr sqrt outside gcc:
    // https://stackoverflow.com/questions/27744079/is-it-a-conforming-compiler-extension-to-treat-non-constexpr-standard-library-fu
    constexpr double root2{1.4142135623730951455}; // std::sqrt(2.)
    constexpr double rootPiBy2{1.2533141373155001208}; // std::sqrt(M_PI/2.0)
    Double_t xscale = root2*sigma_->getVal();
    Double_t mean = mean_->getVal();
    Double_t norm = rootPiBy2*sigma_->getVal()*(RooMath::erf((x_->getMax()-mean)/xscale)-RooMath::erf((x_->getMin()-mean)/xscale));
    out.resize(xvals_.size());
    vectorized::gaussians(xvals_.size(), mean, sigma_->getVal(), norm, &xvals_[0], &out[0], &work_[0], &work2_[0]);
}

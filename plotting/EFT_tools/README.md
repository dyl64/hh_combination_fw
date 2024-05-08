# Intro

This folder contains tools for EFT studies.
Part of the code is taken from the bbyy EFT repository where it was developed for the legavy Run 2 analysis.

``HEFT_coeffs_updated/`` : HEFT coefficients, affected by the POWHEG bug on triangle diagrams : https://link.springer.com/article/10.1007/JHEP10(2023)086

``HEFT_coeffs_updated_bugfix/`` : HEFT coefficients with the fix of the POWHEG bug on triangle diagrams

# Plotting

``plot_shape.py`` and ``plot_xs.py`` read the coefficients and return the xs (1D, 2D) or mHH shape as function of any POI.
Command line options (run with ``--help``) describe how to configure it

# Getting a basis for HEFT

``get_basis_scalings.py`` computes the scaling functions for any set of active POIs and any chosen basis (provided that the resulting matrix is invertable).
In order to run it you need to set:

- the list of samples ``basis_samples`` : this is the list of names of the samples.
- ``sample_def`` a dictionary that defines the values of the couplings simulated for each sample. If you follow a convention "POIname1_poival1_POIname2_poival2[..]" the values can be automatically deduced by the `auto_deduce_pois`` function. Note that the conversion of ``poival`` interprets ``p`` as ``.`` and ``n`` as ``-``. POIs non specifically declared in the name are assumed to be at the SM value.
- The list of active POIs (the ones to vary inside the model). These must be a subset (or identical to) of the 5 HEFT points listed in ``all_pois`` (use the same names)

The code uses the fact that a given sample s is given by s = c x a, where a is a vector containing the various parts of the amplitude (e.g. box diagram square, box-triangle interference, etc - in practice, each item of the HEFT polynomial that has 23 terms) and c is the vector of the scaling (each element of c constains a combination of pois that encodes the dependence on the HEFT coefficients, for example ctth^4, ctthh^2, etc. ) . s can be interpreted as a total xs or a differential one in any variable.

By simulating N samples, one can write a matrix M so that
S = M x a , where S = [s0, s1, .. sN] are the samples of the basis, a is the vector of the amplitues described above, and each element Mij is the evaluation of the corresponding element of c with the specific couplings of the sample si.
Therefore by inverting the matrix a = Minv x S and this can be replaced in the expression of s giving s = c x Minv x S, where the functional dependence is encoded in the product c x Minv to be applied on S.

The code prints the value of these scaling functions (one for each element of the basis) that can be accessed via ``coeffs``.

NOTE : it is possible to use more samples than the minimum required, and combine them with a pseudo-inverse matrix.
The code enables this possibility, but whether there is an advantage in using more samples muts be studied and it is not guaranteed to increase the statistical precision.

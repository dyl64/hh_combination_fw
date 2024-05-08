# Author : L. Cadamuro (IJCLab)
# 08/05/2024

from HEFT_poly import poly
from HEFT_poly import read_coeffs_ATLAS
from HEFT_poly import ci_func_vector
import sympy

## maybe wrong? 11 elements, from bbtt ws txt file
# basis_samples = [
#     'cgghh_0p0_ctthh_0p0',
#     'ctthh_n0p2',
#     'ctthh_0p7',
#     'cgghh_n0p3',
#     'cgghh_0p4',
#     'chhh_n2p5',
#     'chhh_9p0',
#     'cgghh_0p4_ctthh_n0p2',
#     'ctthh_n0p2_chhh_n2p5',
#     'ctthh_1p0_chhh_n10p0',
#     'cgghh_0p4_chhh_n2p5',
# ]

basis_samples = [
    'cgghh_0p0_ctthh_0p0',
    'cgghh_0p4',
    'cgghh_0p4_chhh_n2p5',
    'cgghh_0p4_ctthh_n0p2',
    'cgghh_n0p3',
    'chhh_9p0',
    'chhh_n2p5',
    'ctthh_0p7',
    'ctthh_1p0_chhh_n10p0',
    'ctthh_n0p2',
]

#bbtt
# RooFormulaVar::SigXsecOverSM_cgghh0p0ctthh0p0_kappa [ actualVars=(kappaL,kappa2V,kappat,cgghh,ctthh,chhh,cH,cHbox,den_mu) formula="(-8.3333333333*x[3]*x[3]-0.7142857143*x[3]*x[5]-12.5*x[3]*x[4]+1.5476190476*x[3]-0.0357142857*x[5]*x[5]-0.7873376623*x[5]*x[4]+0.2321428571*x[5]-7.1428571429*x[4]*x[4]+4.3587662338*x[4]+0.8035714286)" ] = -6.5
# RooFormulaVar::SigXsecOverSM_cgghh0p4_kappa         [ actualVars=(kappaL,kappa2V,kappat,cgghh,ctthh,chhh,cH,cHbox,den_mu) formula="(3.5714285714*x[3]*x[3]+0.7142857143*x[3]*x[5]+12.5*x[3]*x[4]+0.3571428571*x[3])" ] = 4.64286
# RooFormulaVar::SigXsecOverSM_cgghh0p4chhhn2p5_kappa [ actualVars=(kappaL,kappa2V,kappat,cgghh,ctthh,chhh,cH,cHbox,den_mu) formula="(-0.7142857143*x[3]*x[5]+0.7142857143*x[3])" ] = 0
# RooFormulaVar::SigXsecOverSM_cgghh0p4ctthhn0p2_kappa[ actualVars=(kappaL,kappa2V,kappat,cgghh,ctthh,chhh,cH,cHbox,den_mu) formula="(-12.5*x[3]*x[4])" ] = 0
# RooFormulaVar::SigXsecOverSM_cgghhn0p3_kappa        [ actualVars=(kappaL,kappa2V,kappat,cgghh,ctthh,chhh,cH,cHbox,den_mu) formula="(4.7619047619*x[3]*x[3]-1.9047619048*x[3])" ] = 2.85714
# RooFormulaVar::SigXsecOverSM_chhh9p0_kappa          [ actualVars=(kappaL,kappa2V,kappat,cgghh,ctthh,chhh,cH,cHbox,den_mu) formula="(0.0108695652*x[5]*x[5]+0.0815217391*x[5]*x[4]+0.0163043478*x[5]-0.0815217391*x[4]-0.027173913)" ] = 0
# RooFormulaVar::SigXsecOverSM_chhhn2p5_kappa         [ actualVars=(kappaL,kappa2V,kappat,cgghh,ctthh,chhh,cH,cHbox,den_mu) formula="(0.7142857143*x[3]*x[5]-0.7142857143*x[3]+0.0248447205*x[5]*x[5]+0.4720496894*x[5]*x[4]-0.248447205*x[5]-0.4720496894*x[4]+0.2236024845)" ] = 0
# RooFormulaVar::SigXsecOverSM_ctthh0p7_kappa         [ actualVars=(kappaL,kappa2V,kappat,cgghh,ctthh,chhh,cH,cHbox,den_mu) formula="(0.1731601732*x[5]*x[4]+1.5873015873*x[4]*x[4]+0.1443001443*x[4])" ] = 0
# RooFormulaVar::SigXsecOverSM_ctthh1p0chhhn10p0_kappa[ actualVars=(kappaL,kappa2V,kappat,cgghh,ctthh,chhh,cH,cHbox,den_mu) formula="(-0.0909090909*x[5]*x[4]+0.0909090909*x[4])" ] = 0
# RooFormulaVar::SigXsecOverSM_ctthhn0p2_kappa        [ actualVars=(kappaL,kappa2V,kappat,cgghh,ctthh,chhh,cH,cHbox,den_mu) formula="(12.5*x[3]*x[4]+0.1515151515*x[5]*x[4]+5.5555555556*x[4]*x[4]-4.0404040404*x[4])" ] = 0


active_pois = ['cgghh', 'ctthh', 'chhh']

##############################################################

def auto_deduce_pois(sname):
    t = sname.split('_')
    res = {}
    if len(t) % 2 != 0:
        raise RuntimeError("token number not even, cannot parse")    
    for i in range(0, len(t), 2):
        pname = t[i]
        s = t[i+1]
        s = s.replace('p', '.')
        s = s.replace('n', '-')
        v = float(s)
        res[pname] = v
    # print(res)
    return res

## default definitions
all_pois = ['cgghh', 'ctthh', 'chhh', 'cggh', 'ctth']
default_vals = {
    'cgghh' : 0.,
    'ctthh' : 0.,
    'chhh'  : 1.,
    'cggh'  : 0.,
    'ctth'  : 1.,
}

# sample_def is a dictionaty that containts the value of the pois for this specific value
# for simplicity it is auto-deduced below, but it can be supplied by hand

sample_def = {s : auto_deduce_pois(s) for s in basis_samples}
# in case of undef names, add defaults
sample_def = {s : {**default_vals, **d} for s,d in sample_def.items()}

## printout values
for s in basis_samples:
    print(' ******** sample : ', s)
    for p in all_pois:
        pref = '  [active] ' if p in active_pois else '           '
        print ('  : {} {:<5} {}'.format(pref, p, sample_def[s][p]))

## now compute the theo xs of each sample using the HEFT poly

# coeff_file_name = 'HEFT_coeffs_updated/muR_muF_1/HEFT_dA_and_A_with_Binning_250_1050_41_Variable_Bins_1200_1400_muR_muF_1.txt'
# print(f'[INFO] will read coefficients from {coeff_file_name}')
# mhh_bins_files, coeffs, Ais = read_coeffs_ATLAS(coeff_file_name, 23)

def get_xs(poi_def_dict, Ais):
    # print(poi_def_dict)
    poi_dict = {**poi_def_dict}
    poi_dict['A'] = Ais
    s = poly(**poi_dict)
    return s

# xs_vals = {s : get_xs(sample_def[s], Ais) for s in basis_samples}

## build the coupling matrix

# first, reduce the ci func vector to only active pois
def contains_active_pois(s, active_pois):
    c = ['{{{}}}'.format(a) in s for a in active_pois]
    return any(c)

def set_of_active_pois_from_list(s, poilist):
    c = ['{{{}}}'.format(a) in s for a in poilist]
    activelist = [x  for i, x in enumerate(poilist) if c[i]]
    activelist.sort()
    activelist = tuple(activelist)
    return activelist

def set_of_active_pois_with_power_from_list(s, poilist):
    """ return a tuple containing all the pois within poilist that are in the expression s and the nr of occurrences """
    activelist = set_of_active_pois_from_list(s, poilist)
    res = []
    for al in activelist:
        smatch = '{{{}}}'.format(al)
        n = s.count(smatch)
        elem = (al, n)
        res.append(elem)
    res.sort()
    res = tuple(res)
    return res
    # c = ['{{{}}}'.format(a) in s for a in poilist]
    # activelist = [x  for i, x in enumerate(poilist) if c[i]]
    # activelist.sort()
    # activelist = tuple(activelist)
    return activelist

active_combs = [set_of_active_pois_with_power_from_list(c, active_pois) for c in ci_func_vector]
unique_combs = list(set(active_combs))
combs_idxs = {comb : [i for i,x in enumerate(active_combs) if x == comb] for comb in unique_combs}

# combs_idx meaning : for a given combiation of couplings == al element of the polynonial, tell whcih elements of the full polynomial correspond

# now select a subset of the polynomial elements
ci_to_keep = []
for combdef, combidxs in combs_idxs.items():
    # if combdef == (): # must also keep the empty element because it is a constant to be propagated
        # continue
    ci_to_keep.append(combidxs[0])

## ci to keep are the idx in the ci_func_vector of the only elements that are relevant
## THIS MUST MATCH THE LENGTH OF THE BASIS!!    

print('Number of unique coefficients : ', len(ci_to_keep))
print('Number of samples in basis', len(basis_samples))

if len(ci_to_keep) > len(basis_samples):
    print('ERROR : sizes of base and required elements do not match')
    raise RuntimeError('SAMPLE BASIS LENGTH NOT ENOUGH FOR THE CHOSEN SET OF POIS')

# setup sympy
alg_samples_vec = [sympy.symbols('s%i' %i) for i in range(len(basis_samples))] # the input samples
alg_poi_list = [sympy.symbols(s) for s in active_pois] # the pois
# alg_ampl_list = [sympy.symbols('a%i' % i) for i in range(len(ci_to_keep))] # the elements of the amplitude
alg_ampl_vec = []
for ici in ci_to_keep:
    s = ci_func_vector[ici]
    poistr = {p:p for p in all_pois}
    s = s.format(**poistr)
    ssymb = sympy.sympify(s)
    alg_ampl_vec.append(ssymb)

nrows = len(basis_samples)
ncols = len(ci_to_keep)
M_tofill = [[None]*ncols for i in range(nrows)]

# nsam = len(basis_samples)
# M = [[None] * nelem for _ in range(nelem)]
# # fill each element of M with the expected poi 

for isample, sample in enumerate(basis_samples): # rows
    sdef = sample_def[sample]
    for icoupl in range(len(ci_to_keep)): # cols
        expr = alg_ampl_vec[icoupl]
        evalexpr = expr.evalf(subs={**sdef})
        M_tofill[isample][icoupl] = evalexpr

### S = M x C
# S : sample vec
# M : matrix
# C : coupling vec

# --> C = Minv x S
# --> s = M x C = Minv x S x C
# where s is the point I want to model and S is the basis

M = sympy.Matrix(M_tofill)
S = sympy.Matrix(alg_samples_vec)
C = sympy.Matrix(alg_ampl_vec)

Minv = M.pinv()
coeffs = C.transpose()*Minv

print('... ... functions found are listed below')
for ic, c in enumerate(coeffs):
    print('--->', basis_samples[ic])
    print(c)
    print('\n')
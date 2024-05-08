import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--pois', default=None,
                        metavar="KEY=VALUE",
                        nargs='+',
                        help="Values of the pois corresponding to this point (not scanned), passed as poi=value. "
                             "Do not put spaces before or after the = sign. "
                             "Separate multiple entries just with a space. Example: "
                             "--pois ctth=1 cgghh=2. "
                             "All parameters not explicitely set are assumed to be at SM value"
                    )
parser.add_argument('--smeft', dest='do_heft', default=True, help="Do calculations for SMEFT (default is for HEFT)", action='store_false')
parser.add_argument('--oname', dest='oname', default=None, help="output name (if not passed, built from values of the pois)")
args = parser.parse_args()

if args.do_heft:
    print('[INFO] Making plot for HEFT')
    pois = ['chhh', 'ctth', 'cgghh', 'cggh', 'ctthh']
    SM_vals = {
        'chhh'  : 1.0,
        'ctth'  : 1.0,
        'cgghh' : 0.0,
        'cggh'  : 0.0,
        'ctthh' : 0.0
    }

    poi_names = {
        'chhh'  : '$c_{hhh}$',
        'ctth'  : '$c_{tth}$',
        'cgghh' : '$c_{gghh}$',
        'cggh'  : '$c_{ggh}$',
        'ctthh' : '$c_{tthh}$',
    }

    import sys
    sys.path.append("../") # needed to import the packages from the directory above
    from HEFT_poly import poly
    from HEFT_poly import read_coeffs_ATLAS

    # coeff_file_name = 'NLO-Ais-13TeV.txt'
    coeff_file_name = 'HEFT_coeffs_updated/muR_muF_1/HEFT_dA_and_A_with_Binning_250_1050_41_Variable_Bins_1200_1400_muR_muF_1.txt'
    print(f'[INFO] will read coefficients from {coeff_file_name}')
    mhh_bins_files, coeffs, Ais = read_coeffs_ATLAS(coeff_file_name, 23)

    mHH_bins = [
        250.,   270.,   290.,   310.,   330.,   350.,   370.,   390.,
        410.,   430.,   450.,   470.,   490.,   510.,   530.,   550.,
        570.,   590.,   610.,   630.,   650.,   670.,   690.,   710.,
        730.,   750.,   770.,   790.,   810.,   830.,   850.,   870.,
        890.,   910.,   930.,   950.,   970.,   990.,  1010.,  1030.,
        1050.,  1200.,  1400.]


else:
    print('[INFO] Making plot for SMEFT')
    pois = ['cdp', 'cp', 'ctp', 'ctG', 'cpg']
    SM_vals = {
        'cdp'  : 0,
        'cp'   : 0,
        'ctp'  : 0,
        'ctG'  : 0,
        'cpg'  : 0, 
    }

    poi_names     = {
        'cdp'   : r'$c_{H,box}$', ## cannot make \Box or \square here
        'cp'    : r'$C_{H}$',
        'ctp'   : r'$c_{tH}$',
        'ctG'   : r'$c_{tG}$',
        'cpg'   : r'$c_{HG}$',
    }

    import sys
    sys.path.append("../") # needed to import the packages from the directory above
    from ..SMEFT_poly import poly
    from ..SMEFT_poly import read_coeffs_ATLAS

    coeff_file_name = 'Weights_20_GeV_Bins.txt'
    print(f'[INFO] reading coefficients from {coeff_file_name}')
    mhh_bins_files, coeffs, Ais = read_coeffs_ATLAS(coeff_file_name, 21)

    mHH_bins = [
        250., 270.,290.,310.,330.,350.,370.,390.,
        410.,430.,450.,470.,490.,
        510.,530.,550.,570.,590.,
        610.,630.,650.,670.,690.,
        710.,730.,750.,770.,790.,
        810.,830.,850.,870.,890.,
        910.,930.,950.,970.,990.,
        1010.,1030.
    ]
    mHH_bins = [x - 10. for x in mHH_bins] # because the values from the coeffs are expressed as center, so shfit it by 1/2 bin width


poi_setup = dict(SM_vals)
if args.pois:
    for elem in args.pois:
        poi, val = elem.split('=')
        if not poi in pois:
            raise RuntimeError("cannot parse {} : POI name {} not understood".format(elem, poi))
        val = float(val)
        poi_setup[poi] = val

print('[INFO] : setup of the poi used')
for poi in pois:
    print('       : {:<5} = {:.2f}'.format(poi, poi_setup[poi]))

normed_bins = [poly(**{**poi_setup, 'A' : coeffs[i]}) for i in range(len(mhh_bins_files))]

# make plot
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.hist(mhh_bins_files, bins=mHH_bins, weights=normed_bins)
poilist = ['{} : {:.1f}'.format(name, value) for name, value in poi_setup.items()]
ax.set_title(', '.join(poilist))
ax.set_xlabel('$m_{HH} [GeV]$')
ax.set_ylabel('$\sigma$')
poilist2 = ['{}_{:.1f}'.format(name, value) for name, value in poi_setup.items()]
oname = args.oname if args.oname else '_'.join(poilist2)+'.pdf'
fig.savefig(oname)
print('[INFO] : figure saved as', oname)

# bw = 20.
# print(mhh_bins_files)


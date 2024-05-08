### simple script to plot total xs from the coefficients

import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--xpoi', required=True, help="scanned poi (reported on x-axis of the plot)")
parser.add_argument('--xmin', type=float, default=-10,  help="min range of scanned x poi")
parser.add_argument('--xmax', type=float, default=10,   help="max range of scanned x poi")
parser.add_argument('--nptx', type=int,   default=100,  help="number of points on the x axis")

parser.add_argument('--ypoi', default=None,  help="scanned poi (reported on y-axis of the plot). If not specified, the code makes a 1D scan")
parser.add_argument('--ymin', type=float, default=-10,  help="min range of scanned y poi")
parser.add_argument('--ymax', type=float, default=10,   help="max range of scanned y poi")
parser.add_argument('--npty', type=int,   default=100,  help="number of points on the y axis")

parser.add_argument('--smeft', dest='do_heft', default=True, help="Do calculations for SMEFT (default is for HEFT)", action='store_false')
parser.add_argument('--other-pois', default=None,
                        metavar="KEY=VALUE",
                        nargs='+',
                        help="Values of the other pois (not scanned), passed as poi=value. "
                             "Do not put spaces before or after the = sign. "
                             "Separate multiple entries just with a space. Example: "
                             "--other-pois ctth=1 cgghh=2. "
                             "All parameters not explicitely set are assumed to be at SM value"
                    )
parser.add_argument('--output', default=None, help="output file name. Use {xpoi} and {ypoi} to replace it with poi (defaults to xs_{xpoi}[_{ypoi}].pdf)")
parser.add_argument('--add-bin-sum', dest='add_bin_sum', default=False, help="Overlay the xs value obtained from the sum of the individual mHH bins (for 1D plots only)", action='store_true')
args = parser.parse_args()

is2D = args.ypoi is not None

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


fixed_pois = list(pois)
fixed_pois.remove(args.xpoi)
if is2D: fixed_pois.remove(args.ypoi)
fixed_pois = {x : SM_vals[x] for x in fixed_pois} # convert to dictionary with SM values

# override values if needed
if args.other_pois:
    for elem in args.other_pois:
        poi, val = elem.split('=')
        if not poi in pois:
            raise RuntimeError("cannot parse {} : POI name {} not understood".format(elem, poi))
        if poi == args.xpoi:
            print(f'[WARNING] POI named {poi} is declared as the scanned x POI, so its declaration as {elem} with --other-pois will be ignored')
            continue
        if is2D and poi == args.ypoi:
            print(f'[WARNING] POI named {poi} is declared as the scanned y POI, so its declaration as {elem} with --other-pois will be ignored')
            continue
        val = float(val)
        fixed_pois[poi] = val

# log info
if is2D:
    print(f'\n[INFO] : 2D scan . Scanning POI x : {args.xpoi} [{args.xmin}, {args.xmax}, {args.nptx} pts], y : {args.ypoi} [{args.ymin}, {args.ymax}, {args.npty} pts]')
else:
    print(f'\n[INFO] : 1D scan . Scanning POI x : {args.xpoi} [{args.xmin}, {args.xmax}, {args.nptx} pts]')
print(f'       : the other POIs are set to the following values:')
for poi in pois:
    if poi != args.xpoi and poi != args.ypoi:
        print('       : {:<5} = {:.2f}'.format(poi, fixed_pois[poi]))

# generate the grid
points = np.linspace(args.xmin, args.xmax, args.nptx)
if is2D:
    ygrid = np.linspace(args.ymin, args.ymax, args.npty)
    def dstack_product(x, y): # makes carthesian product as a single array : https://stackoverflow.com/questions/11144513/cartesian-product-of-x-and-y-array-points-into-single-array-of-2d-points
        return np.dstack(np.meshgrid(x, y)).reshape(-1, 2)
    points = dstack_product(points, ygrid)
    if len(points) != args.nptx*args.npty:
        raise RuntimeError('.. error when combining grid - should never happen')

xs = []
for p in points:
    if is2D:
        xval = p[0]
        yval = p[1]
        poi_dict = {**fixed_pois, args.xpoi : xval, args.ypoi : yval}
    else:
        xval = p
        poi_dict = {**fixed_pois, args.xpoi : xval}
    poi_dict['A'] = Ais    
    s = poly(**poi_dict)
    xs.append(s)

# make the plot
fig, ax = plt.subplots()
if is2D:
    x_data = [p[0] for p in points]
    y_data = [p[1] for p in points]
    z_data = xs
    import pandas as pd # use pandas pivot function to format data for heatmap
    df = pd.DataFrame({'x' : x_data, 'y' : y_data, 'z' : z_data})
    table = df.pivot('y', 'x', 'z')
    import seaborn as sns
    from matplotlib.colors import LogNorm
    # ax = sns.heatmap(table, cmap="Blues", norm=LogNorm(), cbar_kws={'label': r'Total cross section [fb]'})
    ax = sns.heatmap(table, cmap="Blues", cbar_kws={'label': r'Total cross section [fb]'})
    ax.set_xlabel(poi_names[args.xpoi])
    ax.set_ylabel(poi_names[args.ypoi])
    ax.invert_yaxis()
    # from matplotlib.ticker import FormatStrFormatter
    # majorFormatter = FormatStrFormatter('%0.1f')
    # ax.xaxis.set_major_formatter(majorFormatter)
    # ax.yaxis.set_major_formatter(majorFormatter)

else:
    xs = np.asarray(xs)
    ax.plot(points, xs, '-o', lw=1, ms=1.5, c='black', label='Tot. xs')
    ax.set_xlabel(poi_names[args.xpoi])
    ax.set_ylabel('Total cross section [fb]')
    # ax.set_yscale('log')

    if args.add_bin_sum:
        xs_sumbins = []
        for p in points:
            sumbin = sum([poly(**{**fixed_pois, args.xpoi : p, 'A' : coeffs[i]}) for i in range(len(mhh_bins_files))])
            xs_sumbins.append(sumbin)
        ax.plot(points, xs_sumbins, '-o', lw=1, ms=0.75, c='red', label='Sum(bins) xs')
        ax.legend(loc='best')

if args.other_pois:
    ax.set_title(', '.join(args.other_pois))

oname = args.output if args.output else 'xs_{xpoi}.pdf' if not is2D else 'xs_{xpoi}_{ypoi}.pdf'
oname = oname.format(xpoi = args.xpoi, ypoi=args.ypoi)
fig.tight_layout()
print(f'[INFO] Saving figure as {oname}')
fig.savefig(oname)
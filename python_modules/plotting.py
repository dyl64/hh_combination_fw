#!/usr/bin/env python

import sys
import os
import glob
import numpy as np
import matplotlib
from matplotlib.ticker import AutoMinorLocator
from matplotlib.font_manager import FontProperties
from matplotlib import patches as mpatches
import matplotlib.pyplot as plt
import aux_utils as utils
#matplotlib.use('Agg')

font0 = FontProperties()

################################
### --- Figure cosmetics --- ###
################################

fig_type_to_xlabel = {  'nonres'      : r'Non-resonant', 
                         'spin0'       : r'$m_{S}$ [GeV]',
                         'spin2_c_1.0' : r'$m_{G^{*}_{KK}}$ [GeV]',
                         'spin2_c_2.0' : r'$m_{G^{*}_{KK}}$ [GeV]'
                      }

fig_type_to_ylabel = {
                          'nonres':       r'95% CL Limit on $\sigma( pp \rightarrow hh$) [pb]',
                          'spin0':        r'95% CL Limit on $\sigma( pp \rightarrow S \rightarrow hh$ [pb]',
                          'spin2_c_1.0':  r'95% CL Limit on $\sigma( pp \rightarrow G^{*}_{KK} \rightarrow hh$ [pb]',
                          'spin2_c_2.0':  r'95% CL Limit on $\sigma( pp \rightarrow G^{*}_{KK} \rightarrow hh$ [pb]'
                       }

fig_type_to_legend = {
                         'nonres'      :  r"pp $\rightarrow hh$ (exp)",
                         'spin0'       :  r"pp $\rightarrow S \rightarrow hh$ (exp)",
                         'spin2_c_1.0' : r"pp $\rightarrow G^{*}_{KK} \rightarrow hh $ (exp)",
                         'spin2_c_2.0' : r"pp $\rightarrow G^{*}_{KK} \rightarrow hh $ (exp)"
                     }

fig_channel_to_color = {
                            'bbbb'     : 'firebrick',
                            'bbtautau' : 'navy',
                            'bbyy'     : 'darkgreen',
                            'WWyy'     : 'olive',
                            'bbWW'     : 'magenta',
                            'combined' : 'darkorange',
                       }

fig_channel_to_latex = {
                            'bbbb'     : r'$bbbb$',
                            'bbtautau' : r'$bb\tau\tau$',
                            'bbyy'     : r'$bb\gamma\gamma$',
                            'WWyy'     : r'$WW \gamma \gamma$',
                            'bbWW'     : r'$bbWW$',
                            'combined' : 'combined',
                       }

fig_scheme_to_linestyle = {
                            'fullcorr' : r'-',
                            'nocorr'   : r':',
                           }


fig_nConstituents_to_color = {
                                2 : 'sandybrown',
                                3 : 'coral',
                                4 : 'darkorange',
                                5 : 'chocolate'
                             }

#########################
### --- Functions --- ###
#########################

def create_plot_options(datafile_dir, type, rest, comparison=False, label_correlation_scheme=False, verbose=True):

    plot_options = []

    for i, r in enumerate(rest):
        datafile_name = "{0}-{1}.dat".format(type, r)
        datafile_path = os.path.join(datafile_dir, datafile_name)
        info = extract_info_from_datafile_name(datafile_path)
        if comparison:
            curve_options = create_curve_options(info, index=i, label_correlation_scheme=label_correlation_scheme, verbose=verbose)
        else:
            curve_options = create_curve_options(info, label_correlation_scheme=label_correlation_scheme, verbose=verbose)
        plot_options.append(curve_options)

    return plot_options


def create_scheme_legend(scheme):

    if scheme == 'fullcorr':
        legend = "with complete correlation"
    if scheme == 'nocorr':
        legend = "without any correlation"

    return legend
          

def create_constituents_legend(constituents_underscore):
    splitted      = constituents_underscore.split('_')
    nConstituents = len(splitted)
    constituents_legend = "(" + ",".join([fig_channel_to_latex[x]  for x in splitted]) + ")"
    return constituents_legend
    

def create_curve_options(info, index=-1, alpha=0.8, label_correlation_scheme=False, verbose=False):

    curve_options = {}
    curve_options['datafile']    = info['datafile_path']
    curve_options['color']       = fig_channel_to_color[info['channel']]
    curve_options['legend']      = fig_channel_to_latex[info['channel']]
    curve_options['alpha']       = alpha
    curve_options['short_label'] = fig_channel_to_latex[info['channel']]

    if 'combined' == info['channel']:
        curve_options['linestyle'] = fig_scheme_to_linestyle[info['scheme']]
        constituents_legend = create_constituents_legend(info['constituents_underscore'])
        scheme_legend       = create_scheme_legend(info['scheme'])
        scheme = info['scheme']
        curve_options['constituents_legend'] = constituents_legend
        curve_options['color']       = fig_nConstituents_to_color[info['nConstituents']]
        curve_options['short_label']   = constituents_legend
        curve_options['scheme']        = scheme
        if verbose:
            curve_options['scheme_legend'] = scheme_legend
            curve_options['legend'] += " {0} {1}".format(constituents_legend, scheme_legend)
        else:
            curve_options['legend'] += " {0}".format(constituents_legend)

    if not index == -1:
        curve_options['color']   = "C{0}".format(index)


    return curve_options


def extract_info_from_datafile_name(datafile_path):

    filename = os.path.basename(datafile_path)
    basename = filename.split('.dat')[0]
    splitted = basename.split('-')

    type     = splitted[0]
    channel  = splitted[1]

    info = {}

    if len(splitted) == 2:
        pass
    elif len(splitted) == 5:
        region       = splitted[2]
        constituents = splitted[3]
        scheme       = splitted[4]
        info['region']                  = region
        info['constituents_underscore'] = constituents
        info['nConstituents']           = len(constituents.split('_'))
        info['scheme']         = scheme
    #else:
    #    raise Exception('Unknown datafile name pattern: {0}, length: {1}'.format(filename,
    #        len(splitted)))

    info['datafile_path']  = datafile_path
    info['type']           = type
    info['channel']        = channel

    return info


def autoplotdir(datafile_dir, figure_dir):

    datafiles = glob.glob( os.path.join(datafile_dir,  '*.dat' ))
    for datafile in datafiles:
        
        filename = os.path.basename(datafile)
        basename = filename.split('.dat')[0]
        splitted = basename.split('-')
        type     = splitted[0]
        channel  = splitted[1]

        types    = ['spin0', 'nonres', 'spin2_c_1.0']
        channels = ['bbbbb', 'bbtautau', 'WWyy', 'bbWW', 'bbyy']

        if not type in types:
            continue
        if not channel in channels:
            continue

        figure_filename = "{}_{}".format(type, channel)
        figure_path = os.path.join(figure_dir, figure_filename)

        if type == "nonres":
            isSM = True
            xrange = []
            yrange = []
        else:
            isSM = False
            xrange = [290.0, 3000.0]
            yrange = [1e-3, 1.0e1]
        

        plot_single_exp_limit(datafile,
                              figure_path,
                              xlabel = fig_type_to_xlabel[type],
                              ylabel = fig_type_to_ylabel[type],
                              xrange = xrange,
                              yrange = yrange,
                              title  = fig_type_to_legend[type] + ', ' + fig_channel_to_latex[channel],
                              legend_text = fig_type_to_legend[type],
                              isSM=isSM
                              )


#######################
# - read_pts_from_file()
def read_pts_from_file(inp_datafile, delimiter=' '):
    """Read in a datafile with numpy.genfromtxt().
       Returns a structured numpy array."""

    pts = np.genfromtxt(inp_datafile, delimiter=delimiter, names=True)

    return pts


##################################
# - convert_namedtuple_to_structured_array
#def convert_namedtuple_to_structured_array( list_of_namedtuple  ):
#
#    a = np.array(list(zip(*list_of_namedtuple)))
#
#    f = a[:,0]
#    d = a[:,1:]
#
#    print(d)
#    print(f)
#    
#    structured_array  = np.array(d, dtype='float32')
#    structured_array  = np.array(d, dtype=[(name, 'float32') for name in f])

#    print(structured_array)
#    print(structured_array['mass'])

#    return structured_array


#########################
# - plot_single_exp_limit
def plot_single_exp_limit(inp_datafile, out_figure,
                      xlabel = r'$m_{X}$ [GeV]',
                      ylabel = r'95% CL Limit on $\sigma( pp \rightarrow X \rightarrow hh)$ [pb]',
                      xrange = [290.0, 3000.0],
                      yrange = [1e-3,   1e1],
                      legend_text = r"pp $\rightarrow X \rightarrow hh$ (exp)",
                      title = '',
                      text = 'ATLAS (internal)',
                      text_posx = 0.07,
                      text_posy = 0.95, 
                      ylog=True,
                      xlog=False,
                      isSM=False):
    """
    Creates a limit plot featuring a single limit.

    Arguments:
    - inp_datafile: Path to the datafile containing the mass and limits vales
    - out_figure: Output figure name.
    Arguments with default values:
    - xlabel: 
    - ylabel:
    - xrange:
    - yrange:
    - legend_text:
    - title:
    - text:
    - text_posx:
    - text_posy:
    - ylog:
      
    Returns matplotlib.pyplot figure and axis handles."""

    print("Trying to create {}".format(out_figure))

    # - Create output folder if it doesn't exist
    output_folder = os.path.dirname(out_figure)
    utils.mkdir_p(output_folder)

    pts = read_pts_from_file(inp_datafile)

    f, a = plt.subplots()
    
    if not isSM:
        a.fill_between(pts['mass'], pts['xsec_exp']-pts['xsec_m2s'], pts['xsec_exp']+pts['xsec_p2s'], facecolor='gold', interpolate=True)
        a.fill_between(pts['mass'], pts['xsec_exp']-pts['xsec_m1s'], pts['xsec_exp']+pts['xsec_p1s'], facecolor='green' , interpolate=True)

    a.plot(pts['mass'], pts['xsec_exp'], color='k', linestyle='--', marker='+', label=legend_text)

    if xrange:
        a.set_xlim(xrange)
    if yrange:
        a.set_ylim(yrange)

    # - Minor ticks
    minorLocator = AutoMinorLocator()
    a.xaxis.set_minor_locator(minorLocator)

    if ylog:
        a.set_yscale("log")

    if xlog:
        a.set_xscale("log")


    a.set_xlabel(xlabel)
    a.set_ylabel(ylabel)

    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)

    a.text(text_posx, text_posy,  text,
        verticalalignment='top', horizontalalignment='left',
        transform=a.transAxes, fontsize=15)

    a.set_title(title)

    f.savefig(out_figure+'.png', bbox_inches='tight')
    f.savefig(out_figure+'.pdf', bbox_inches='tight')

    return f,a

def singlept_comparison(
                        type,
                        channels,
                        xrange = [0.1, 400.0],
                        xlog=False,
                        xlabel='',
                        title='',
                        normalisation=1.0,
                        elinewidth=6.0,
                        markersize=7.0,
                        out_figure = False,
                        ATLAS_label_pos=(0.03, 0.92),
                        show_obs=False,
                        colorize=False
                        ):


    f, a = plt.subplots(nrows=1, ncols=1)


    nChannels = len(channels)
    y = np.arange(nChannels)

    #labels = [for ch['label'] in channels]
    #a.set_xlim(xrange)
    a.set_xlim(xrange)

    if xlog:
        a.set_xscale("log")

    a.set_xlabel(xlabel)

    ytick_labels = []
    x_exp = []
    x_obs = []
    x_exp_1sigerr_min = []
    x_exp_1sigerr_max = []
    x_exp_2sigerr_min = []
    x_exp_2sigerr_max = []

    xsec_exp_col = "xsec_exp_{}".format(type)
    xsec_obs_col = "xsec_obs_{}".format(type)
    xsec_exp_err_1sigerr_min_col = "xsec_m1s_{}".format(type)
    xsec_exp_err_1sigerr_max_col = "xsec_p1s_{}".format(type)
    xsec_exp_err_2sigerr_min_col = "xsec_m2s_{}".format(type)
    xsec_exp_err_2sigerr_max_col = "xsec_p2s_{}".format(type)




    for ch in channels:
        pts = read_pts_from_file(ch['datafile'])
        x_exp.append(pts[xsec_exp_col]/normalisation)
        x_obs.append(pts[xsec_obs_col]/normalisation)
        x_exp_1sigerr_min.append(pts[xsec_exp_err_1sigerr_min_col]/normalisation) 
        x_exp_1sigerr_max.append(pts[xsec_exp_err_1sigerr_max_col]/normalisation) 
        x_exp_2sigerr_min.append(pts[xsec_exp_err_2sigerr_min_col]/normalisation) 
        x_exp_2sigerr_max.append(pts[xsec_exp_err_2sigerr_max_col]/normalisation) 


        if show_obs:
            ytick_label = "{0}\nexp: {1:.1f}\nobs: {2:.1f} ".format(ch['short_label'],
                                                                    pts[xsec_exp_col]/normalisation,
                                                                    pts[xsec_obs_col]/normalisation)
        else:
            ytick_label = "{0}\nexp: {1:.1f}".format(ch['short_label'], pts[xsec_exp_col]/normalisation)


        if 'scheme_legend' in ch:
                ytick_label = "{0}\nexp: {1:.1f}\n{2}".format(ch['short_label'],
                    pts[xsec_exp_col]/normalisation, ch['scheme_legend'])



        ytick_labels.append(ytick_label)

    a.plot(x_exp, y, 
            linestyle='',
            marker='o',
            markerfacecolor='none',
            markeredgecolor='k',
            markersize=markersize)
    a.errorbar(x_exp, y, xerr=[x_exp_2sigerr_min, x_exp_2sigerr_max],
              linestyle='',
              ecolor='gold',
              elinewidth=elinewidth)
    a.errorbar(x_exp, y, xerr=[x_exp_1sigerr_min, x_exp_1sigerr_max],
               linestyle='',
               ecolor='green',
               elinewidth=elinewidth)

    if show_obs:
        a.plot(x_obs, y, 
                linestyle='',
                marker='o',
                markerfacecolor='k',
                markeredgecolor='k',
                markersize=markersize)
    

    plt.yticks(y, ytick_labels, rotation='horizontal')


    if colorize:
        colors = []
        for ch in channels:
            colors.append(ch['color'])

        for ytick, color in zip(a.get_yticklabels(), colors):
                ytick.set_color(color)
        

#   handles, labels = a.get_legend_handles_labels()
#   a.legend(handles, labels, bbox_to_anchor=(1, 1), loc='upper left', ncol=1)

    a.set_title(title)

    if ATLAS_label_pos:
        text_ATLAS_full_info(a, x_pos=ATLAS_label_pos[0], y_pos=ATLAS_label_pos[1])

    if out_figure:
        f.savefig(out_figure+'.png', bbox_inches='tight')
        f.savefig(out_figure+'.pdf', bbox_inches='tight')


    return f,a


#########################
# - plot_multiple_channels
def plot_multiple_channels(x, y, channels,
                           out_figure=False,
                           xlabel = r'$m_{X}$ [GeV]',
                           ylabel = r'95% CL Limit on $\sigma( pp \rightarrow X \rightarrow hh)$ [pb]',
                           xrange = [290.0, 3000.0],
                           yrange = [1e-3,  1e1],
                           title = '',
                           ylog=True,
                           normalise_to_reference=False,
                           ATLAS_label_pos=(0.5, 0.92),
                           legend_pos=(0.7, 0.92),
                           make_legend=True,
                           run_label=False,
                           ):
    """ 
    Creates a limit plot featuring multiple limit curves.

    Arguments:
    - channels: List containing dictionaries, one dictionary for each channel.
                Dictionary stores information need to create the figure:
                - datafile
                - color
                - legend
                - linewidth
                - linestyle
                - marker
    - out_figure: Output figure name.
    Arguments with defeault values:

    """


    f, a = plt.subplots()

    a.set_xlim(xrange)
    a.set_ylim(yrange)

    if ylog:
        a.set_yscale("log")

    a.set_xlabel(xlabel)
    a.set_ylabel(ylabel)


    if normalise_to_reference:
        ref_pts = read_pts_from_file(normalise_to_reference)

    for ch in channels:
        pts = read_pts_from_file(ch['datafile'])

        plot_cosmetics_fill_blanksettings(ch)

        if normalise_to_reference:
               a.plot(pts[x],
               pts[y]/ref_pts['xsec_exp'],
               color=ch['color'],
               linewidth=ch['linewidth'],
               linestyle=ch['linestyle'],
               marker=ch['marker'],
               label=ch['legend'],
               alpha=ch['alpha'])

        else:
            a.plot(pts[x],
                   pts[y],
                   color=ch['color'],
                   linewidth=ch['linewidth'],
                   linestyle=ch['linestyle'],
                   marker=ch['marker'],
                   label=ch['legend'],
                   alpha=ch['alpha'])

    handles, labels = a.get_legend_handles_labels()

    if make_legend:
        a.legend(handles, labels, bbox_to_anchor=legend_pos, loc='upper left', ncol=1)

    a.set_title(title)


    if ATLAS_label_pos:
        text_ATLAS_full_info(a, x_pos=ATLAS_label_pos[0], y_pos=ATLAS_label_pos[1])


    if out_figure:
        f.savefig(out_figure+'.png', bbox_inches='tight')
        f.savefig(out_figure+'.pdf', bbox_inches='tight')


    return f, a

def plot_cosmetics_fill_blanksettings(settings):

    fill_dict_if_missing(settings, 'color',     'k')
    fill_dict_if_missing(settings, 'linewidth', 2.0)
    fill_dict_if_missing(settings, 'linestyle', '-')
    fill_dict_if_missing(settings, 'marker',    'o')
    fill_dict_if_missing(settings, 'legend',    'blank legend')
    fill_dict_if_missing(settings, 'alpha',     1.0)


def fill_dict_if_missing(dict, key, value):
    if not key in dict:
        dict[key] = value

######################################

def make_ATLAS_label(a, version='wip', fontsize=17, x_pos=0.03, y_pos=0.92, x_shift=0.15):

    #font = font0.copy()
    #font.set_style('italic')
    #font.set_weight('bold')

    label_ATLAS = r'ATLAS'
    if version == 'wip':
        label_version = "(work in progress)"

    if version == 'int':
        label_version = "Internal"

    a.text(x_pos, y_pos, label_ATLAS, fontsize=fontsize, fontweight='bold', style='italic', transform=a.transAxes)
    a.text(x_pos+x_shift, y_pos, label_version, fontsize=fontsize, transform=a.transAxes)



def make_run_label(a,
                  run_version = 'run2',
                  fontsize=16,
                  x_pos=0.03,
                  y_pos=0.85):

    if run_version == 'run2':
        run_label = r'$\sqrt{s} = 13$ TeV, $\mathcal{L} = 36.1$  $\mathrm{fb}^{-1}$'

    a.text(x_pos, y_pos, run_label, fontsize=fontsize, transform=a.transAxes)

######################################

def text_ATLAS(a, x_pos, y_pos, label="ATLAS", style="italic", fontweight="bold", fontsize=16,
        coordinate='axes'):

    if coordinate == 'axes':
        transform = a.transAxes
    elif coordinate == 'data':
        transform = a.transData

    a.text(x_pos, y_pos, label, style=style, fontweight=fontweight, fontsize=fontsize,
            transform=transform)

def text_ATLAS_label(a, x_pos, y_pos, fontsize=20, x_shift=0.25, version_text="Internal", coordinate='axes'):

    text_ATLAS(a, x_pos, y_pos, fontsize=fontsize, coordinate=coordinate)
    
    if coordinate == 'axes':
        transform = a.transAxes
    elif coordinate == 'data':
        transform = a.transData

    a.text(x_pos+x_shift, y_pos, version_text, fontsize=fontsize, transform=transform)


def text_collider_setup(a, x_pos, y_pos, sqrt_s='13 TeV', lumi='36.1 fb$^{-1}$', coordinate='axes'):

    collider_setup_text = r"$\sqrt{{s}} =$ {}, {}".format(sqrt_s, lumi)
    if coordinate == 'axes':
        transform = a.transAxes
    elif coordinate == 'data':
        transform = a.transData

    a.text(x_pos, y_pos, collider_setup_text, transform=transform)


def text_ATLAS_full_info(a, x_pos, y_pos, version_x_shift=0.13, collider_x_shift=0.00,
        collider_y_shift=-0.06, version_text="Internal",
        sqrt_s='13 TeV', lumi='36.1 fb$^{-1}$', fontsize=14, coordinate='axes'):

    text_ATLAS_label(a, x_pos, y_pos, fontsize=fontsize, x_shift=version_x_shift, coordinate=coordinate)
    text_collider_setup(a, x_pos+collider_x_shift, y_pos+collider_y_shift, sqrt_s, lumi, coordinate=coordinate)


def top_caption(f, a, mH, legend_handles, legend_loc=(0.57,0.99), legend_fontsize=7.5, model_description="Singlet model"):
    caption_box = mpatches.Rectangle((0.0, 1.0), 1.0, 0.2, clip_on=False, transform=a.transAxes,  edgecolor='k', facecolor='white', linewidth=1.0)
    a.add_artist(caption_box)
    text_ATLAS_full_info(a, 0.016, 1.12, fontsize=14, collider_y_shift=-0.08, version_x_shift=0.12)
    a.text(0.32, 1.12, model_description, fontweight='bold', fontsize=14, transform=a.transAxes)
    a.text(0.33, 1.045, r"$m_{{H}}$ = {:.0f} GeV".format(mH), fontsize=14, transform=a.transAxes)
    leg = a.legend(handles=legend_handles, ncol=2, columnspacing=1, loc=legend_loc, fontsize=legend_fontsize, frameon=False)

def hMSSM_top_caption(f, a, legend_handles, legend_loc=(0.57,0.99), legend_fontsize=7.5, model_description="Singlet model"):
    caption_box = mpatches.Rectangle((0.0, 1.0), 1.0, 0.2, clip_on=False, transform=a.transAxes,  edgecolor='k', facecolor='white', linewidth=1.0)
    a.add_artist(caption_box)
    text_ATLAS_full_info(a, 0.020, 1.12, fontsize=14, collider_y_shift=-0.08, version_x_shift=0.12)
    a.text(0.40, 1.10, model_description, fontweight='bold', fontsize=14, transform=a.transAxes)
    leg = a.legend(handles=legend_handles, ncol=2, columnspacing=1, loc=legend_loc, fontsize=legend_fontsize, frameon=False)

#!/usr/bin/env python

import plotting as stp
import os
import aux_utils as utils

#data_folder   = '/.data/englert/projects/hh_combination/software/RooStatTools/limits/data-files/WWyy_should_working/'
#figure_folder = '/.data/englert/projects/hh_combination/software/RooStatTools/figures/WWyy_should_working/'

#data_folder = '/.data/englert/projects/hh_combination/software/RooStatTools/limits/data-files/2017_10_22_WWyy_fixed/'
#figure_folder = '/.data/englert/projects/hh_combination/software/RooStatTools/figures/2017_10_22_WWyy_fixed/'


tag = "Beta"
data_folder   = os.path.join('/.data/englert/projects/hh_combination/software/RooStatTools/limits/data-files/', tag)
figure_folder = os.path.join('/.data/englert/projects/hh_combination/software/RooStatTools/figures/', tag)

utils.mkdir_p(figure_folder)

br_h_bb = { 125.00 : 0.5824,
            125.09 : 0.5809 }

print('Making limit plots')

#######################################
##### ----- Single channels ----- #####
#######################################

print('Single channels')

##################################
##### ----- bb tautau ----- ######
##################################

print('hh -> bb tautau')

#############################################################################
### --- bbtautau, spin-0 [pb]

print(" - spin-0")

bbtautau_spin0_datafile = os.path.join(data_folder,   'spin0_bbtautau.dat')
bbtautau_spin0_figure   = os.path.join(figure_folder, 'spin0_bbtautau')

stp.plot_single_exp_limit(bbtautau_spin0_datafile,
                          bbtautau_spin0_figure,
                          xlabel = r'$m_{S}$ [GeV]',
                          ylabel = r'95% CL Limit on $\sigma( pp \rightarrow S \rightarrow hh$ [pb]',
                          xrange = [250.0, 1050.0],
                          yrange = [1e-3,   1.0e1],
                          title = r"$pp \rightarrow S \rightarrow hh$ upper limits in the $b\bar{b} \tau \tau$ channel",
                          legend_text = r"pp $\rightarrow S \rightarrow hh$ (exp)"
                          )


#############################################################################
### --- bbtautau, spin-2 [pb]

print(" - spin-2")

bbtautau_spin2_c_10_datafile = os.path.join(data_folder,   'spin2_c_1.0_bbtautau.dat')
bbtautau_spin2_c_10_figure   = os.path.join(figure_folder, 'spin2_c_1.0_bbtautau')

stp.plot_single_exp_limit(bbtautau_spin2_c_10_datafile,
                          bbtautau_spin2_c_10_figure,
                          xlabel = r'$m_{G^{*}_{KK}}$ [GeV]',
                          ylabel = r'95% CL Limit on $\sigma( pp \rightarrow G^{*}_{KK} \rightarrow hh$ [pb]',
                          xrange = [250.0, 1050.0],
                          yrange = [1e-3,   1.0e1],
                          title = r"$pp \rightarrow G^{*}_{KK} \rightarrow hh$ upper limits in the $b\bar{b} \tau \tau$ channel",
                          legend_text = r"pp $\rightarrow G^{*}_{KK} \rightarrow hh $ (exp)"
                          )

##############################
##### ----- bb bb ----- ######
##############################

print('hh -> bb bb')

#############################################################################
### --- bbbb, spin-0 [pb], scaled

print(" - spin-0")

bbbb_spin0_datafile = os.path.join(data_folder,   'spin0_bbbb.dat')
bbbb_spin0_figure   = os.path.join(figure_folder, 'spin0_bbbb')

stp.plot_single_exp_limit(bbbb_spin0_datafile,
                          bbbb_spin0_figure,
                          xlabel = r'$m_{S}$ [GeV]',
                          ylabel = r'95% CL Limit on $\sigma( pp \rightarrow S \rightarrow hh$ [pb]',
                          xrange = [250.0, 1600.0],
                          yrange = [1e-3,   1.0e1],
                          title = r"$pp \rightarrow S \rightarrow hh$ upper limits in the $b\bar{b}b\bar{b}$ channel",
                          legend_text = r"pp $\rightarrow S \rightarrow hh$ (exp)"
                          )


#############################################################################
### --- bbbb, spin-0, Br(h->bb)**2 applied, in [fb]
### --- To compare with Internal Note


bbbb_spin0_br_h_bb_fb_datafile = os.path.join(data_folder,   'spin0_bbbb_br_h_bb_fb.dat')
bbbb_spin0_br_h_bb_fb_figure   = os.path.join(figure_folder, 'spin0_bbbb_br_h_bb_fb')

stp.plot_single_exp_limit(bbbb_spin0_br_h_bb_fb_datafile,
                          bbbb_spin0_br_h_bb_fb_figure,
                          xlabel = r'$m_{S}$ [GeV]',
                          ylabel = r'95% CL Limit on $\sigma( pp \rightarrow S \rightarrow hh \rightarrow b\bar{b}b\bar{b})$ [fb]',
                          xrange = [200.0, 3100.0],
                          yrange = [0.8,   1.1e4],
                          title = r"$pp \rightarrow S \rightarrow hh \rightarrow b\bar{b} b\bar{b}$ upper limits",
                          legend_text = r"pp $\rightarrow S \rightarrow hh \rightarrow b\bar{b}b\bar{b}$ (exp)",
                          xlog=True
                          )

#############################################################################
### --- bbbb, spin-2 [pb]

print(" - spin-2")

bbbb_spin2_c_10_datafile = os.path.join(data_folder,   'spin2_c_1.0_bbbb.dat')
bbbb_spin2_c_10_figure   = os.path.join(figure_folder, 'spin2_c_1.0_bbbb')

stp.plot_single_exp_limit(bbbb_spin2_c_10_datafile,
                          bbbb_spin2_c_10_figure,
                          xlabel = r'$m_{G^{*}_{KK}}$ [GeV]',
                          ylabel = r'95% CL Limit on $\sigma( pp \rightarrow G^{*}_{KK} \rightarrow hh$ [pb]',
                          xrange = [200.0, 3000.0],
                          yrange = [1e-3,   1.0e1],
                          legend_text = r"pp $\rightarrow G^{*}_{KK} \rightarrow hh$ (exp)"
                          )

bbbb_spin2_c_10_br_h_bb_fb_datafile = os.path.join(data_folder,   'spin2_c_1.0_bbbb_br_h_bb_fb.dat')
bbbb_spin2_c_10_br_h_bb_fb_figure   = os.path.join(figure_folder, 'spin2_c_1.0_bbbb_br_h_bb_fb')

stp.plot_single_exp_limit(bbbb_spin2_c_10_br_h_bb_fb_datafile,
                          bbbb_spin2_c_10_br_h_bb_fb_figure,
                          xlabel = r'$m_{G^{*}_{KK}}$ [GeV]',
                          ylabel = r'95% CL Limit on $\sigma( pp \rightarrow G^{*}_{KK} \rightarrow hh \rightarrow b\bar{b}b\bar{b})$ [fb]',
                          xrange = [200.0, 3100.0],
                          yrange = [0.8,   1.1e4],
                          title = r"$pp \rightarrow G^{*}_{KK} \rightarrow hh \rightarrow b\bar{b}b\bar{b}$ upper limits",
                          legend_text = r"pp $\rightarrow G^{*}_{KK} \rightarrow hh \rightarrow b\bar{b}b\bar{b}$ (exp)",
                          xlog=True
                          )

##############################
##### ----- WW yy ----- ######
##############################

print('hh -> WW yy')

#############################################################################
### --- WWyy, spin-0 [pb]

print(' - spin-0')

WWyy_spin0_datafile = os.path.join(data_folder,   'spin0_WWyy.dat')
WWyy_spin0_figure   = os.path.join(figure_folder, 'spin0_WWyy')

stp.plot_single_exp_limit(WWyy_spin0_datafile,
                          WWyy_spin0_figure,
                          xlabel = r'$m_{S}$ [GeV]',
                          ylabel = r'95% CL Limit on $\sigma( pp \rightarrow S \rightarrow hh$ [pb]',
                          xrange = [250.0, 650.0],
                          yrange = [1e-2,   1.0e2],
                          title = r"$pp \rightarrow S \rightarrow hh$ upper limits in the $WW \gamma \gamma$ channel",
                          legend_text = r"pp $\rightarrow S \rightarrow hh$ (exp)"
                          )

########################
### --- Combined --- ###
########################


doCombination = False
if doCombination:

    print('hh combination')
    
    #############################################################################
    ### --- Combined spin-0 [pb]
    
    print(' - spin-0')
    
    combined_spin0_datafile = os.path.join(data_folder,   'spin0_combined_nocorr.dat')
    combined_spin0_figure   = os.path.join(figure_folder, 'spin0_combined_nocorr')
    
    stp.plot_single_exp_limit(combined_spin0_datafile,
                              combined_spin0_figure,
                              xlabel = r'$m_{S}$ [GeV]',
                              ylabel = r'95% CL Limit on $\sigma( pp \rightarrow S \rightarrow hh$ [pb]',
                              xrange = [250.0, 1050.0],
                              yrange = [1e-3,   1.0e1],
                              title = r"$pp \rightarrow S \rightarrow hh$ upper limits from $bbbb$ and $bb\tau\tau$ combination",
                              legend_text = r"pp $\rightarrow S \rightarrow hh$ (exp)"
                              )
    
    combined_spin0_datafile = os.path.join(data_folder,   'spin0_combined_fullcorr.dat')
    combined_spin0_figure   = os.path.join(figure_folder, 'spin0_combined_fullcorr')
    
    stp.plot_single_exp_limit(combined_spin0_datafile,
                              combined_spin0_figure,
                              xlabel = r'$m_{S}$ [GeV]',
                              ylabel = r'95% CL Limit on $\sigma( pp \rightarrow S \rightarrow hh$ [pb]',
                              xrange = [250.0, 1050.0],
                              yrange = [1e-3,   1.0e1],
                              title = r"$pp \rightarrow S \rightarrow hh$ upper limits from $bbbb$ and $bb\tau\tau$ combination",
                              legend_text = r"pp $\rightarrow S \rightarrow hh$ (exp)"
                              )
    
    #############################################################################
    ### --- Combined spin-2 [pb]
    
    print(' - spin-2')
    
    combined_spin2_c_10_datafile = os.path.join(data_folder,   'spin2_c_1.0_combined_fullcorr.dat')
    combined_spin2_c_10_figure   = os.path.join(figure_folder, 'spin2_c_1.0_combined_fullcorr')
    
    stp.plot_single_exp_limit(combined_spin2_c_10_datafile,
                              combined_spin2_c_10_figure,
                              xlabel = r'$m_{S}$ [GeV]',
                              ylabel = r'95% CL Limit on $\sigma( pp \rightarrow G^{*}_{KK} \rightarrow hh$ [pb]',
                              xrange = [250.0, 1050.0],
                              yrange = [1e-3,   1.0e1],
                              title = r"$pp \rightarrow G^{*}_{KK} \rightarrow hh$ upper limits from $bbbb$ and $bb\tau\tau$ combination",
                              legend_text = r"pp $\rightarrow G^{*}_{KK} \rightarrow hh$ (exp)"
                              )
    
    combined_spin2_c_10_datafile = os.path.join(data_folder,   'spin2_c_1.0_combined_nocorr.dat')
    combined_spin2_c_10_figure   = os.path.join(figure_folder, 'spin2_c_1.0_combined_nocorr')
    
    stp.plot_single_exp_limit(combined_spin2_c_10_datafile,
                              combined_spin2_c_10_figure,
                              xlabel = r'$m_{S}$ [GeV]',
                              ylabel = r'95% CL Limit on $\sigma( pp \rightarrow G^{*}_{KK} \rightarrow hh$ [pb]',
                              xrange = [250.0, 1050.0],
                              yrange = [1e-3,   1.0e1],
                              title = r"$pp \rightarrow G^{*}_{KK} \rightarrow hh$ upper limits from $bbbb$ and $bb\tau\tau$ combination",
                              legend_text = r"pp $\rightarrow G^{*}_{KK} \rightarrow hh$ (exp)"
                              )

########################################
##### ----- Multiple channels ----- ####
########################################

print("Multiple channels")

### --- Spin-0

print(" - spin-0")

multi_channel_spin0_fig         = os.path.join(figure_folder, 'spin0_multiple')
multi_channel_spin0_fig_zoomed  = os.path.join(figure_folder, 'spin0_multiple_zoomed')
bbbb_spin0_datafile             = os.path.join(data_folder,   'spin0_bbbb.dat')
bbtautau_spin0_datafile         = os.path.join(data_folder,   'spin0_bbtautau.dat')
WWyy_spin0_datafile             = os.path.join(data_folder,   'spin0_WWyy.dat')
combination_spin0_datafile_with_corr = os.path.join(data_folder, 'spin0_combined_fullcorr.dat')
combination_spin0_datafile_wout_corr = os.path.join(data_folder, 'spin0_combined_nocorr.dat')
bbWW_spin0_datafile                  = os.path.join(data_folder, 'spin0_bbWW.dat')

channels = [
              {'datafile': bbbb_spin0_datafile, 
                  'color': 'firebrick',
                   'name': 'bbbb',
                 'legend': r"$b\bar{b}b\bar{b}$ (exp)"},
              {'datafile': WWyy_spin0_datafile,
                  'color': 'olive',
                   'name': 'WWyy',
                 'legend': r"$WW\gamma\gamma$ (exp)"},
              {'datafile': bbWW_spin0_datafile,
                  'color': 'magenta',
                   'name': 'bbWW',
                 'legend': r"$b\bar{b}WW$ (exp), missing scaling"},
              {'datafile': bbtautau_spin0_datafile,
                  'color': 'navy',
                   'name': 'bbtautau',
                 'legend': r"$b\bar{b}\tau\tau$ (exp)"},
               {'datafile': combination_spin0_datafile_with_corr,
                   'color': 'darkorange',
                    'name': 'combination',
                   'alpha': 0.5,
                  'legend': r"$bbbb$, $bb\tau\tau, WW\gamma\gamma$ comb. (exp), with corr"},
                {'datafile': combination_spin0_datafile_wout_corr,
                    'color': 'springgreen',
                     'name': 'combination',
                    'alpha': 0.5,
                   'legend': r"$bbbb$, $bb\tau\tau, WW\gamma\gamma$ comb. (exp), wout corr"}
           ]

stp.plot_multiple_channels(channels, multi_channel_spin0_fig,
                           xlabel = r'$m_{S}$ [GeV]',
                           ylabel = r'95% CL Limit on $\sigma( pp \rightarrow S \rightarrow hh)$ [pb]',
                           xrange = [250.0, 3100.0],
                           yrange = [4e-3,  20e0],
                          )

stp.plot_multiple_channels(channels, multi_channel_spin0_fig_zoomed,
                           xlabel = r'$m_{S}$ [GeV]',
                           ylabel = r'95% CL Limit on $\sigma( pp \rightarrow S \rightarrow hh)$ [pb]',
                           xrange = [200.0, 1100.0],
                           yrange = [4e-3,  20e0],
                          )


### --- Spin-2

print(" - spin-2")

multi_channel_spin2_c_10_fig    = os.path.join(figure_folder, 'spin2_c_1.0_multiple')
bbbb_spin2_c_10_datafile        = os.path.join(data_folder,   'spin2_c_1.0_bbbb.dat')
bbtautau_spin2_c_10_datafile    = os.path.join(data_folder,   'spin2_c_1.0_bbtautau.dat')
combination_spin2_c_10_datafile = os.path.join(data_folder,   'spin2_c_1.0_combined_fullcorr.dat')

channels = [
              {'datafile': bbbb_spin2_c_10_datafile, 
                  'color': 'firebrick',
                   'name': 'bbbb',
                 'legend': r"$b\bar{b}b\bar{b}$ (exp)"},
              {'datafile': bbtautau_spin2_c_10_datafile,
                  'color': 'navy',
                   'name': 'bbtautau',
                 'legend': r"$b\bar{b}\tau\tau$ (exp)"},
              {'datafile': combination_spin2_c_10_datafile,
                  'color': 'darkorange',
                   'name': 'combination',
                 'legend': r"$bbbb$ & $bb\tau\tau$ comb. (exp)"}
           ]

stp.plot_multiple_channels(channels, multi_channel_spin2_c_10_fig,
                           xlabel = r'$m_{G^{*}_{KK}}$ [GeV]',
                           ylabel = r'95% CL Limit on $\sigma( pp \rightarrow G^{*}_{KK} \rightarrow hh)$ [pb]',
                           xrange = [250.0, 1250.0],
                           yrange = [1e-3,  1e1],
                          )

################################################
### --- Comparison of with and wout corr --- ###
################################################


print("Correlation scheme comparison")

spin2_c_10_fig_with_wout_corr_logscale    = os.path.join(figure_folder, 'spin2_c_1.0_with_wout_corr_log')
spin2_c_10_fig_with_wout_corr_linscale    = os.path.join(figure_folder, 'spin2_c_1.0_with_wout_corr_lin')
combination_spin2_c_10_datafile_wout_corr = os.path.join(data_folder,   'spin2_c_1.0_combined_fullcorr.dat') 
combination_spin2_c_10_datafile_with_corr = os.path.join(data_folder,   'spin2_c_1.0_combined_nocorr.dat') 

channels = [
              {'datafile': combination_spin2_c_10_datafile_with_corr,
                  'color': 'navy',
                   'name': 'combination with corr NP',
                 'legend': r"combination with corr NP (exp)"},
              {'datafile': combination_spin2_c_10_datafile_wout_corr,
                  'color': 'firebrick',
                   'name': 'combination wout corr NP',
                 'legend': r"combination wout corr NP(exp)"}
           ]

stp.plot_multiple_channels(channels, spin2_c_10_fig_with_wout_corr_logscale,
                           xlabel = r'$m_{G^{*}_{KK}}$ [GeV]',
                           ylabel = r'95% CL Limit on $\sigma( pp \rightarrow G^{*}_{KK} \rightarrow hh)$ [pb]',
                           xrange = [250.0, 1050.0],
                           yrange = [1e-2,  1e1],
                          )

stp.plot_multiple_channels(channels, spin2_c_10_fig_with_wout_corr_linscale,
                           xlabel = r'$m_{G^{*}_{KK}}$ [GeV]',
                           ylabel = r'95% CL Limit on $\sigma( pp \rightarrow G^{*}_{KK} \rightarrow hh)$ [pb]',
                           xrange = [250.0, 1050.0],
                           yrange = [-0.2,  2.0],
                           ylog=False
                          )
# ------------

spin0_fig_with_wout_corr_logscale    = os.path.join(figure_folder, 'spin0_with_wout_corr_log')
spin0_fig_with_wout_corr_linscale    = os.path.join(figure_folder, 'spin0_with_wout_corr_lin')
combination_spin0_datafile_wout_corr = os.path.join(data_folder,   'spin0_combined_nocorr.dat') 
combination_spin0_datafile_with_corr = os.path.join(data_folder,   'spin0_combined_fullcorr.dat') 

channels = [
              {'datafile': combination_spin0_datafile_with_corr,
                  'color': 'navy',
                   'name': 'combination with corr NP',
                 'legend': r"combination with corr NP (exp)"},
              {'datafile': combination_spin0_datafile_wout_corr,
                  'color': 'firebrick',
                   'name': 'combination wout corr NP',
                 'legend': r"combination wout corr NP(exp)"}
           ]

stp.plot_multiple_channels(channels, spin0_fig_with_wout_corr_logscale,
                           xlabel = r'$m_{S}$ [GeV]',
                           ylabel = r'95% CL Limit on $\sigma( pp \rightarrow S \rightarrow hh)$ [pb]',
                           xrange = [250.0, 1050.0],
                           yrange = [1e-2,  1e1],
                          )

stp.plot_multiple_channels(channels, spin0_fig_with_wout_corr_linscale,
                           xlabel = r'$m_{S}$ [GeV]',
                           ylabel = r'95% CL Limit on $\sigma( pp \rightarrow S \rightarrow hh)$ [pb]',
                           xrange = [250.0, 1050.0],
                           yrange = [-0.2,  3.0],
                           ylog=False
                          )

#!/usr/bin/env python

import root_plot as rplot
import ROOT

output_basename = '/.data/englert/projects/hh_combination/software/hh_combination_fw/results/exclusion_plots/hMSSM_exclusion'

frame_x_min = 180
frame_x_max = 550
frame_y_min = 1
frame_y_max = 4

plot_settings = {
                  'bbtautau': {
                                'priority'   : 2,
                                'fillcolor'  : ROOT.kBlue,
                                'linecolor'  : ROOT.kBlue,
                                'alpha'      : 0.2,
                                'linestyle'  : ROOT.kSolid,
                                'legend'     : 'bb#tau#tau',
                                'doDrawFill' : True,
                                'doDrawLine' : True,
                                'file_path'  : '/.data/englert/projects/hh_combination/software/hh_combination_fw/results/exclusion_plots/xs_ggFH_br_H_hh_over_limit_bbtautau_exp_tgraph.root',
                              },
                  'bbbb': {
                                'priority'   : 3,
                                'fillcolor'  : ROOT.kRed,
                                'linecolor'  : ROOT.kRed,
                                'alpha'      : 0.2,
                                'linestyle'  : ROOT.kSolid,
                                'legend'     : 'bbbb',
                                'doDrawFill' : True,
                                'doDrawLine' : True,
                                'file_path'  : '/.data/englert/projects/hh_combination/software/hh_combination_fw/results/exclusion_plots/xs_ggFH_br_H_hh_over_limit_bbbb_exp_tgraph.root'
                              },
                  'combined': {
                                'priority'   : 1,
                                'fillcolor'  : ROOT.kOrange,
                                'linecolor'  : ROOT.kOrange,
                                'alpha'      : 0.2,
                                'linestyle'  : ROOT.kSolid,
                                'legend'     : 'combined',
                                'doDrawFill' : True,
                                'doDrawLine' : True,
                                'file_path'  : '/.data/englert/projects/hh_combination/software/hh_combination_fw/results/exclusion_plots/xs_ggFH_br_H_hh_over_limit_combined_exp_tgraph.root'
                              },
                  'mH':       {
                                'priority'   : 10,
                                'fillcolor'  : ROOT.kGray+1,
                                'linecolor'  : ROOT.kGray+1,
                                'alpha'      : 1.0,
                                'linestyle'  : ROOT.kDashed,
                                'legend'     : 'm_{H} [GeV]',
                                'doDrawFill' : False,
                                'doDrawLine' : True,
                                'file_path'  : '/.data/englert/projects/hh_combination/software/hh_combination_fw/results/exclusion_plots/tgr_mH.root'
                              },
                }


y_max = 4.0

#############################################################################


# - General style settings
rplot.setup_style()

# - Get frame
frame = rplot.get_frame(x1=frame_x_min, x2=frame_x_max, y1=frame_y_min, y2=frame_y_max)

# - Get canvas
canvas = rplot.create_canvas()

frame.Draw()

# - Plot contours
for contour_line, options in sorted(plot_settings.iteritems(), key=lambda (k,v): v['priority']):

    tf, tgraphs = rplot.get_objects(options['file_path'])
    plot_settings[contour_line]['tgraph'] = tgraphs[0]

    for tgraph in tgraphs:
        options['tgraph'] = tgraph
        rplot.draw_tgraph_contour(**options)
    tf.Close()

# - mH contours
mHs = range(200, 525, 25)
mH_labels = rplot.mH_labels(mHs, y_pos=3.5)

# - Create TPave (top information box) 
legpave = rplot.draw_TPave()

#legline = rplot.draw_TLine(180, y_max, 500, y_max)

# - ATLAS info label
ATLAS_label = rplot.draw_ATLAS_label()

# - Add legends
legend = rplot.draw_legend(plot_settings)

# - Save output
canvas.SaveAs(output_basename+'.pdf')
canvas.SaveAs(output_basename+'.png')

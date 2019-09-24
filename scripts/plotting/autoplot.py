#!/usr/bin/env python

import os

import plotting as rsplt

tag = "Epsilon"
data_dir   = "/.data/englert/projects/hh_combination/workspaces/{0}/limits/data-files".format(tag)
figure_dir = "/.data/englert/projects/hh_combination/workspaces/{0}/figures/".format(tag)

rsplt.autoplotdir(data_dir, figure_dir)

#!/usr/bin/env python

import os

hh_combination_fw_path = os.environ['hh_combination_fw_path']

##############################
### --- Custom schemes --- ###
##############################

fullcorr_scheme_bbbb_bbtautau_WWyy_bbWW = { 
                                            'bbbb':      'fullcorr',
                                            'bbtautau':  'fullcorr',
                                            'WWyy':      'fullcorr',
                                            'bbWW':      'fullcorr'
                                          }

fullcorr_scheme_bbbb_bbtautau_WWyy = { 
                                            'bbbb':      'fullcorr',
                                            'bbtautau':  'fullcorr',
                                            'WWyy':      'fullcorr',
                                          }

fullcorr_scheme_A = { 
                      'bbbb':      'fullcorr',
                      'bbtautau':  'fullcorr',
                      'WWyy':      'fullcorr'
                    }


fullcorr_scheme_B = { 
                      'bbbb':      'fullcorr',
                      'bbtautau':  'fullcorr',
                    }

nocorr_scheme_A = { 
                      'bbbb':      'nocorr',
                      'bbtautau':  'nocorr',
                      'WWyy':      'nocorr'
                   }

nocorr_scheme_B = { 
                      'bbbb':      'nocorr',
                      'bbtautau':  'nocorr',
                  }


#########################
### --- Functions --- ###
#########################

def get_same_scheme_for_all_channels(channels, scheme='fullcorr'):
    scheme_setup = {}
    for ch in channels:
        scheme_setup[ch] = scheme
    return scheme_setup
        

def get_scheme_file_path(ch, scheme_file_version):
    scheme_file_path = os.path.join(hh_combination_fw_path,
                                    'workspaceCombiner/schemes',
                                     ch,
                                     "{}.xml".format(scheme_file_version),
                                    )

    return scheme_file_path

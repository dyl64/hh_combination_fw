#!/usr/bin/env python

import os
import sys


def main():
    
    inpath = '/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/output/vfinal_04/limits/data-files'

    infileNames = ['lambda_statOnly-combined-A-bbbb_bbtautau-fullcorr.dat',
                   'lambda_statOnly-combined-B-bbbb_bbtautau-fullcorr.dat',
                   'lambda_statOnly-combined-C-bbbb_bbtautau-fullcorr.dat',
                   'lambda_statOnly-combined-D-bbbb_bbtautau-fullcorr.dat']

    outfileName = 'lambda_statOnly-combined-F-bbbb_bbtautau-fullcorr.dat'

    print "Merging files:"
    print infileNames
    print "Outfile name = {}".format(os.path.join(inpath, outfileName))

    
    outfile = open(os.path.join(inpath, outfileName), 'w')

    filenumber = 1
    for infileName in infileNames:
        with open(os.path.join(inpath, infileName), 'r') as infile:
            linenumber = 1
            for line in infile:
                if linenumber == 1 and not filenumber == 1:
                    linenumber += 1
                    continue
                else:
                    outfile.write(line)

                linenumber += 1
        filenumber += 1
    
    outfile.close()



if __name__ == '__main__':
    main()

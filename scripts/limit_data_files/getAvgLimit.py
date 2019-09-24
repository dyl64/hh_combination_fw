#!/usr/bin/env python

import os
import sys
import math
import collections
import itertools
import operator


#read-in content of input file and store lines in list
def GetFileContent(inpath, infileName):

    fileContent = []

    with open(os.path.join(inpath, infileName), 'r') as f:
        fileContent = f.readlines()

    return fileContent


#save values of single lines in dictionary with first element (mass) as key
def GetLineContent(lines):

    lineContent = {}

    for line in lines:
        elements = line.split()
        key = elements[0]
        del elements[0]
        #numbers = [float(x) for x in elements]
        values = [x for x in elements]
        lineContent[key] = values[:]

    return lineContent



def main():

    inpath = '/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2/output/vfinal_04/limits/data-files'
    
    # spin-0
    #infileName1 = 'spin0_interp275-bbtautau.dat'
    #infileName2 = 'spin0_interp300-bbtautau.dat'
    #infileName1 = 'spin0_interp275-combined-E-bbbb_bbtautau_bbyy_WWyy_WWWW-fullcorr.dat'
    #infileName2 = 'spin0_interp300-combined-E-bbbb_bbtautau_bbyy_WWyy_WWWW-fullcorr.dat'

    #outfileName = 'spin0_interpAvg-bbtautau.dat'
    #outfileName = 'spin0_interpAvg-combined-E-bbbb_bbtautau_bbyy_WWyy_WWWW-fullcorr.dat'


    # spin-2, c=1
    #infileName1 = 'spin2_c_1.0_interp260-bbtautau.dat'
    #infileName2 = 'spin2_c_1.0_interp300-bbtautau.dat'
    infileName1 = 'spin2_c_1.0_interp260-combined-D-bbbb_bbtautau-fullcorr.dat'
    infileName2 = 'spin2_c_1.0_interp300-combined-D-bbbb_bbtautau-fullcorr.dat'

    #outfileName = 'spin2_c_1.0_interpAvg-bbtautau.dat'
    outfileName = 'spin2_c_1.0_interpAvg-combined-D-bbbb_bbtautau-fullcorr.dat'


    print "Averaging limits of common mass points..."
    print "Input file 1: {0}".format(os.path.join(inpath, infileName1))
    print "Input file 2: {0}".format(os.path.join(inpath, infileName2))


    contentFile1 = GetFileContent(inpath, infileName1)
    contentFile2 = GetFileContent(inpath, infileName2)

    parameterNames = contentFile1[0]
    parameterNames = parameterNames.rstrip()

    
    contentFile1.pop(0)
    contentFile2.pop(0)

    dict1 = GetLineContent(contentFile1)
    dict2 = GetLineContent(contentFile2)
    
    commonPoints = []
    
    for key in dict1.keys():
        if dict2.has_key(key):
            commonPoints.append(key)

    print "Common points: {0}".format(sorted(commonPoints, key=lambda x: int(x)))


    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

    avgLimits = {}

    for key in commonPoints:
        limits1 = dict1[key]
        limits2 = dict2[key]

        if compare(dict1[key], dict2[key]):
            continue

        avgLimits[key] = [[limits1[0]]]
        avgLimits[key].append([abs((((float(limits1[3])-float(x)) + (float(limits2[3])-float(y)))/2) - ((float(limits1[3])+float(limits2[3]))/2)) for x,y in zip(limits1[1:3], limits2[1:3])])
        avgLimits[key].append([(float(limits1[3])+float(limits2[3]))/2])
        avgLimits[key].append([abs((((float(limits1[3])+float(x)) + (float(limits2[3])+float(y)))/2) - ((float(limits1[3])+float(limits2[3]))/2)) for x,y in zip(limits1[4:6], limits2[4:6])])
        avgLimits[key].append([(float(limits1[6])+float(limits2[6]))/2])
        avgLimits[key].append([abs((((float(limits1[9])-float(x)) + (float(limits2[9])-float(y)))/2) - ((float(limits1[9])+float(limits2[9]))/2)) for x,y in zip(limits1[7:9], limits2[7:9])])
        avgLimits[key].append([(float(limits1[9])+float(limits2[9]))/2])
        avgLimits[key].append([abs((((float(limits1[9])+float(x)) + (float(limits2[9])+float(y)))/2) - ((float(limits1[9])+float(limits2[9]))/2)) for x,y in zip(limits1[10:12], limits2[10:12])])
        avgLimits[key].append([(float(limits1[12])+float(limits2[12]))/2])
        avgLimits[key].append([abs((((float(limits1[15])-float(x)) + (float(limits2[15])-float(y)))/2) - ((float(limits1[15])+float(limits2[15]))/2)) for x,y in zip(limits1[13:15], limits2[13:15])])
        avgLimits[key].append([(float(limits1[15])+float(limits2[15]))/2])
        avgLimits[key].append([abs((((float(limits1[15])+float(x)) + (float(limits2[15])+float(y)))/2) - ((float(limits1[15])+float(limits2[15]))/2)) for x,y in zip(limits1[16:18], limits2[16:18])])
        avgLimits[key].append([(float(limits1[18])+float(limits2[18]))/2])
        avgLimits[key].append([abs((((float(limits1[21])-float(x)) + (float(limits2[21])-float(y)))/2) - ((float(limits1[21])+float(limits2[21]))/2)) for x,y in zip(limits1[19:21], limits2[19:21])])
        avgLimits[key].append([(float(limits1[21])+float(limits2[21]))/2])
        avgLimits[key].append([abs((((float(limits1[21])+float(x)) + (float(limits2[21])+float(y)))/2) - ((float(limits1[21])+float(limits2[21]))/2)) for x,y in zip(limits1[22:24], limits2[22:24])])
        avgLimits[key].append([(float(limits1[24])+float(limits2[24]))/2])
        if len(limits1) > 25 and len(limits2) > 25:   # for normalization to SM in non-resonant
            avgLimits[key].append([(float(x)+float(y))/2 for x,y in zip(limits1[25:], limits2[25:])])


        avgLimits[key] = list(itertools.chain.from_iterable(avgLimits[key]))

        del dict1[key]
        del dict2[key]


    avgLimits.update(dict1)
    avgLimits.update(dict2)


    limitList = []
    for key in avgLimits.keys():
        pointList = [int(key)]
        for x in avgLimits[key]:
            pointList.append(x)
        limitList.append(pointList)


    limitList.sort(key=lambda x: x[0])


    print "Writing results to output file {0}".format(os.path.join(inpath, outfileName))
    
    with open(os.path.join(inpath, outfileName), 'w') as outfile:
        outfile.write(parameterNames+"\n")
        for line in limitList:
            outfile.write(" ".join(str(l) for l in line)+"\n")

    print "Done!"



if __name__ == '__main__':
    main()

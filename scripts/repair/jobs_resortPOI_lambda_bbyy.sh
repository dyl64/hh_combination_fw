#!/bin/bash


FRAMEWORKPATH="/afs/cern.ch/user/f/fbeisieg/work/HHcombination/hh_combination_fw_FullRun2"
SCRIPTPATH="./submodules/RooStatTools/python_modules/resortPOIs.py"
FILEPATH="./input/workspaces/vfinal_03/bbyy/lambda_temp2"

lambda="0"

for i in $(seq -20 20); do
    if (($i < 0)); then
	lambda="0${i#-}"
    else
	lambda="$i"
    fi

    INFILE=${FRAMEWORKPATH}/${FILEPATH}/${lambda}.root
    if [ -f $INFILE ]; then
    
	echo "Running POI re-sorting for lambda = ${lambda}"
        #python ./submodules/RooStatTools/python_modules/resortPOIs.py ./test_input/vfinal_02/bbyy/lambda/${lambda}.root ./test_input/vfinal_02/bbyy/lambda/${lambda}_resorted.root mu_hh
	python ${FRAMEWORKPATH}/${SCRIPTPATH} ${INFILE} ${FRAMEWORKPATH}/${FILEPATH}/${lambda}_resorted.root mu_hh
	
	echo "Removing ${FRAMEWORKPATH}/${FILEPATH}/${lambda}.root"
	rm -rf ${INFILE}
	echo "Renaming ${FRAMEWORKPATH}/${FILEPATH}/${lambda}_resorted.root to ${FRAMEWORKPATH}/${FILEPATH}/${lambda}.root"
	mv ${FRAMEWORKPATH}/${FILEPATH}/${lambda}_resorted.root ${FRAMEWORKPATH}/${FILEPATH}/${lambda}.root
	
    fi

done
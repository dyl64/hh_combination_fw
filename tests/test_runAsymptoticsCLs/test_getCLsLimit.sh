#!/usr/bin/env bash

echo "Testing RooStatTools/bin/getCLsLimit."

GETCLSLIMIT_BIN=${ROOSTATPATH}/bin/getCLsLimit
INPUT_WS="${hh_combination_fw_path}/tests/reference_workspaces/bbbb/spin0/500.root"
OUTPUT_LIMITS="${hh_combination_fw_path}/tests/test_runAsymptoticsCLs/bbbb_500_limits.root"
LOG="${hh_combination_fw_path}/tests/test_runAsymptoticsCLs/bbbb_500_limits_root.log"
EXP_OR_OBS="exp"
DOBETTERBANDS="false"
DATANAME=obsData
WORKSPACENAME=combined
MODELCONFIGNAME=ModelConfig
ASIMOVDATANAME=_

${GETCLSLIMIT_BIN} ${INPUT_WS} ${OUTPUT_LIMITS} ${EXP_OR_OBS} ${DOBETTERBANDS} ${WORKSPACENAME} ${MODELCONFIGNAME} ${DATANAME} ${ASIMOVDATANAME} $CL > ${LOG}

OUTPUT_LIMITS="${hh_combination_fw_path}/tests/test_runAsymptoticsCLs/bbbb_500_limits.dat"
LOG="${hh_combination_fw_path}/tests/test_runAsymptoticsCLs/bbbb_500_limits_dat.log"

${GETCLSLIMIT_BIN} ${INPUT_WS} ${OUTPUT_LIMITS} ${EXP_OR_OBS} ${DOBETTERBANDS} ${WORKSPACENAME} ${MODELCONFIGNAME} ${DATANAME} ${ASIMOVDATANAME} $CL > ${LOG}

echo "Test should be finished now."

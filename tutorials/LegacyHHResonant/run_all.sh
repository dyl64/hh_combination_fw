if [ "$#" -ge 1 ];
then
	OUTDIR=$1
else
	OUTDIR=${PWD}/output_$(date +'%d_%m_%Y')
fi

INPUTDIR=/eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/

HHComb process_channels -i /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/FullRun2Workspaces/original/LegacyRun2/20230915/ -o $OUTDIR -c bbbb,bbtautau,bbyy -n spin0 --file_expr '<mX[F]>' --config $hh_combination_fw_path/configs/task_options/Legacy2022/spin0_v3.yaml --unblind --tasks modification,limit,significance

## correlated case
HHComb combine_channels -i $OUTDIR -n spin0 -s $hh_combination_fw_path/configs/correlation_schemes/Legacy2022/spin0_v2.json -c bbbb,bbtautau,bbyy --file_expr '<mX[F]>' --config $hh_combination_fw_path/configs/task_options/Legacy2022/spin0_v3.yaml --unblind --tasks combination,limit,significance

## uncorrelated case
HHComb combine_channels -i $OUTDIR -n spin0 -c bbbb,bbtautau,bbyy --file_expr '<mX[F]>' --config $hh_combination_fw_path/configs/task_options/Legacy2022/spin0_v3.yaml --unblind --tasks combination,limit,significance
The scripts under this folder are BSM limits scan scripts which is used to get the upper limits v.s. ratio of br_h_bb and br_h_yy, which is model independent and can be applied to hMSSM, MSSM benchmarks and the 2HDM. The latest results is stored under the scripts folder as well named `summary*.txt`.

Quick start to run the BSM scan:
1) Go to the scripts folder and source the setup file, `source setup.sh`
2) run the reparamterize script `python reparam.py`, set the input folder to the one that contain the workspaces after rescale, set the output folder as you like, it will create a several BSM output folder under it. 
3) run the combination script, `python combination.py`

Note that Step 2 and 3 are usually very fast, only take few minutes to finish

4) After checking all the combined workspace is created successfully, run the scan job script `python fit.py`. It will submit the scan job to the condor, one scan job will contain several scan points.
5) After all the scanning jobs are finished, run the script that summarize the fit results, `python get_fit_results.py`
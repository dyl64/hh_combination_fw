1. create workspaces for each lambda value from original generic workspace:

   	  python scripts/repair/set_bbyy_lambda.py


2. add missing variables "channellist" and weightVar" to generated workspaces:

       	  ./scripts/repair/jobs.sh   (uses scripts/repair/importClass.C)


3. resort POI list in workspaces (important to have "mu_hh" as first POI for later rescaling since combination framework always uses the first POI):

   	  ./scripts/repair/jobs_resortPOI_lambda_bbyy.sh


4. run normal pipeline:

       	  python scripts/pipeline/processChannels_DPG.py

# Model scan

## hMSSM 

1. Use the [`ModelTools`][ModelTools] package to create the list of parameter points you'd like to be evaluated.
    For hMSSM we can run the `submodules/ModelTools/scripts/generate_hMSSM_space.sh` script,
    that calls `submodules/ModelTools/bin/converthMSSMTuple2ASCII`. The latter binary is basically a
    wrapper around [LHCHXSWGMSSMNeutral][LHCHXSWGMSSMNeutral].
    The shell script creates a list of parameters points with the required properties (masses,
    cross-section, branching ratio etc.) written out as columns in an ASCII file to the folder
    `submodules/ModelTools/ascii/`
2. Once we have our input (the list of parameter space points) prepared, you should specify job
   settings in `scripts/hMSSM_scan/setup_scan.py`.
   This script handles the following:
    - appends each parameter space point with the available neigbouring mass points.
    - distributes the list of parameter scan points across the number of jobs specified.
    - submit the jobs to the cluster with a job scheduler of our choice (SGE in our case).
3. Once the jobs are finished, merge the result of each job with
   `scripts/hMSSM_scan/pool_processed_scan_pts.py`.

### Job success inspections and resubmission

To see which jobs have processed all the assigned points run:
- [`./scripts/hMSSM_scan/get_failed_jobs.py`](../scripts/hMSSM_scan/get_failed_jobs.py)

To automatically gather all failed jobs and resubmit a new batch with the reamining points:
- [`./scripts/hMSSM_scan/resubmit_failed_jobs.py`](../scripts/hMSSM_scan/resubmit_failed_jobs.py)


[ModelTools]: ./submodules/ModelTools/
[LHCHXSWGMSSMNeutral]: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHXSWGMSSMNeutral

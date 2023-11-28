This is the code for BSM exclusion region plotting

For the hMSSM and MSSM benchmarks, the ROOT file containing the prediction from the LHCHWG need to be downloaded, it can be found in https://zenodo.org/records/6334713.

For the singlet model, a Singlet prediction framework needs to be downloaded, it can be found in: https://gitlab.cern.ch/atlas-physics/HDBS/HBSM/recomendationsrealewksinglet.

Then the scripts can be run by simply type `python limit_<model>.py`. Currently the Singlet have 275 and 500 mass point. Mh125eft scripts contain the Mh125eft and Mh125eftlc models, it can be switched by setting the `islc` to `False` or `True`.
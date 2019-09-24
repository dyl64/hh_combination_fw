# `hh_combination_fw` combination details

## Correlation scheme

The correlation scheme is defined by the combination `.xml` file, which is the configuration file of
the [`workspaceCombiner`][workspaceCombiner].

Correlated nuisance parameters will be the ones which have identical names across the different
channels.

The different versions of the correlation scheme `.xml` file snippets for each channel can be found in the
[./workspaceCombiner/schemes/](../workspaceCombiner/schemes/) folder. These `.xml` snippets are used to
build up a combination `.xml` file, which serves as the config file for the combination.

Please see the relevant section of the [workspaceCombiner TWiki][workspaceCombiner_combination] for
more details. 

**For analysis contacts:**
If the NP naming convention has been changed relative to the previous iteration of the workspaces,
please refer to the [manual][how_to_update] on how to update these.

## POI scaling factors

The scaling factors are used to normalise the POIs of the different channels, in order to have a
standardised definition of POI, which is:
- in case of the non-resonant production: &sigma;(pp->hh), without considering the further decay
    of 'h'.
- in case of the resonant production:     &sigma;(pp->X->hh), similarly without any further decay.

The scaling factors are stored in the  [python_modules/scalings.py](../python_modules/scalings.py) file.

**For analysis contacts:**
If the scaling factors have been changed relative to the previous interation of the workspaces, 
please refer to the [manual][how_to_update] on how to update these.


[how_to_update]: ./for_analysis_contacts.md
[workspaceCombiner_combination]: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/WorkspaceCombiner#Workspace_combination
[workspaceCombiner]: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/WorkspaceCombiner

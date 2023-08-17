# Instructions for channel analysis contacts

## Update scaling factors

If you wish to update the scalings factors used to normalise the POIs

1. Open the [./python_modules/scalings.py](./python_modules/scalings.py) file.
2. Create a new entry in the appropriate scalings dictionary, with a version number (key of the
   python dictionary) that is an integer larger the previous existing one.
3. Please also leave a comment above the version number writing the date of creation of the new
   workspaces.

Thank you!

## Update NPs

If the name of the NPs has been changed please create a new file under the channel directory in
[./workspaceCombiner/schemes/](./workspaceCombiner/schemes/).

For the value of `NewName` please use the [standardised naming convention of systematics][NP_naming_convention]

Thank you!

[NP_naming_convention]: https://indico.cern.ch/event/630646/contributions/2548335/attachments/1443117/2225302/XiaohuSUN-CombHH-2017-04-11-HHdomain-EDIT.pdf


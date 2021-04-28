## Semi-automated Nuisance Parameter suggestions

Setup environment:
```
source /eos/atlas/atlascerngroupdisk/phys-hdbs/diHiggs/combination/anaconda3/setup.sh
```

<details><summary>Error when running bbyy workspace </summary>
<p>
If you saw
```
cling::DynamicLibraryManager::loadLibrary(): libopenblasp-r0-5bebc122.3.13.dev.so: cannot open shared object file: No such file or directory
ERROR: Shared library for the macro RooTwoSidedCBShape is incompatible with the current pyROOT version. Please recompile by typing "quickstats compile".
```
Contact analysis contacts (rui.zhang@cern.ch, stefano.manzoni@cern.ch) to run the following commands which requires write permission in HHcomb eos space.
```
quickstats compile
```
</p>
</details>

### Example commands

```
python NPrenaming.py --path ../../../input/20210309/ -c bbbb -p spin0  -m 400 -w w
python NPrenaming.py --path ../../../input/20210309/ -c bbbb -p spin0  -m 1600 -w combined
python NPrenaming.py --path ../../../input/20210309/ -c bbtautau -p spin0  -m 1600 -w combined
python NPrenaming.py --path ../../../input/20210309/ -c bbyy
```

# Troubleshooting

This note aims to collect all the issues we encountered during the development of the combination
framework and their respective solutions. Should you run into these problems yourself, we provide
solutions and workarounds to these nuances.



## `RooGenericPdf`, `RooFormulaVar` (non)indexed syntax

### Symptom(s)

Variables in formulas using the non-indexed syntax are not appended by the channel postfix (e.g.
`_WWyy`) in the combination step.

~~~~
[#0] ERROR:Eval -- RooFormula::eval(conBkgPdf_WWyy): Formula doesn’t compile: exp(c1*m_yy+c2*m_yy*m_yy)
~~~~

### Solution

`RooFormulaVar` and `RooGenericPdf` should use the indexed syntax, e.g. `(”’@0+@1’, x, y”)`.
See [workspaceCombiner prerequisites](workspaceCombiner_prerequisites)

[workspaceCombiner_prerequisites]: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/WorkspaceCombiner#Prerequisites_for_input_workspac



## bb&gamma;&gamma; workspace doesn't give a limit

### Description

`runAsmpyoticsCLs` is unable to provide a sensible limit.

### Solution

Need to fix all `mu` variables to 1 and to constant (`mu`, `mu_XS_VBF`, `mu_XS_ggF`)
See [`./scripts/repair/correct_bbyy.py`](../scripts/repair/correct_bbyy.py)



## bb&gamma;&gamma; toy limits (Qi Li)

### Description

In the bb&gamma;&gamma; nonres worksapce, the `ModelConfig` is changed. The change is on the list of the observable.
Another two variables - `weightVar` and `Channellist` - are added to the Observables. Using the package
to throw toys will encounter error that a variable "weight" is missing

### Solution

Adding them to the workspace can solve this problem. The modified workspace is placed in
`/eos/atlas/atlascerngroupdisk/phys-higgs/HSG6/HH/combination/workspaces/bbyy_liq_2018_01_22`. 



## Custom classes in the workspaces

Some examples for custom classes:
-`HggTwoSidedCBPdf`
- `RooNovosobirsk`
- `ExpGaussExpPDF`

### Problem: Custom classes dropped

#### Description

There is a custom class inside the workspace which is dropped after the rescaling step (editing the
workspace with workspaceCombiner).

#### Symptom(s)

~~~~
Class::Init:0: RuntimeWarning: no dictionary for class HggTwoSidedCBPdf is available Error in
<TBufferFile::ReadObject>: trying to read an emulated class (HggTwoSidedCBPdf) to store in a
compiled pointer (TObject)
~~~~

#### Solution

##### pyROOT

Create `HggTwoSidedCBPdf cxx.so`, with ROOT CINT:
~~~~
.L HggTwoSidedCBPdf.cxx+
~~~~

In your python script insert the following in the beginning:

~~~~
import ROOT
ROOT.gSystem.Load("HggTwoSidedCBPdf_cxx.so")
~~~~



##### Compiled C++

You need to create:
- `HggTwoSidedCBPdfinkDef.h`
- Dictionary objects with `ROOTCINT`

Have a look here:
https://gitlab.cern.ch/denglert/RooStatTools/blob/master/src/Makefile


### Problem: `.wscode...` hidden directory created

#### Description

The custom class libraries are compiled and loaded on the fly, during which hidden folders are
created. This can pose an issue during scans where there multiple combinations/rescalings, polluting
the folder and thaking additional time.


#### Solution

- For `RooStatTools`:
    - Add load directive to `python_modules/ROOT_setup.py`

- For `workspaceCombiner`:
    - Add `.cxx` to `./src`
    - Add `.h` to `./interface`
    - Add a pragma link e.g. `#pragma link C++ class ExpGausExpPDF+;` to `./interface/manager_LinkDef.h`


## Multiple rescaling of a workspace (pitfall!)

### Symptom(s)

Multiple rescaling of the workspace doesn't yield a sensible limit.

### Solution

In the occasion you need to perform a rescaling on a POI that has been already rescaled before,
be cautious and change the `oldpoi_equivalent_name/OLDPOIEQUIVALENTNAME` inside
[rescale.xml](../workspaceCombiner/cfg/template/rescale.xml) something other than what is already in
the rescaled workspace. Failure to do so will result in overwriting the already existing expression
that rescaled the original POI in the workspace, so you'll be rescaling the original POI not the
already rescaled one.

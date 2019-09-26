# Setup instructions

1. **Setup `workspaceCombiner`**.

    Download and install [workspaceCombiner][workspaceCombiner].

    Please refer to the [installation manual][workspaceCombiner_install] on how to setup this package.

    If you are using custom external classes in the `RooStat.Workspace`s (e.g. `ExpGausExpPDF`,
    `HggTwoSidedCBPdf` in case of bb&gamma;&gamma;) you will need to compile and links these with
    [workspaceCombiner][workspaceCombiner].

    Place the
    - `.h` header files in `./interface` directory
    - `.cxx` source files in `./src` directory 
    and
    - Add a pragma link e.g. `#pragma link C++ class ExpGausExpPDF+;` to `./interface/manager_LinkDef.h`
    within the [workspaceCombiner][workspaceCombiner] package, and the (re)compile the binary.

    Failure of doing so will result in compiling this libraries on the file polluting your work area
    with hidden folders named e.g `.wscode.e61c755a-b4e8-11e8-9717-839d8a89beef.combWS`, see
    relevant part of the
    [troubleshooting documentation](./troubleshooting.md#problem-wscode-hidden-directory-created).

2.  **Checkout the [`hh_combination_fw`][hh_combination_fw] `git` repository.**

    You can check out the [`hh_combination_fw`][hh_combination_fw] `git` repository, including the submodules with:

    ~~~~
    git clone --recursive ssh://git@gitlab.cern.ch:7999/atlas-physics/HDBS/DiHiggs/combination/hh_combination_fw.git
    ~~~~

3.  **Setting up the framework**

    In order to run, the framework needs two local setup scripts, one in the root directory of framwork itself and one in the RooStatTools submodule. In addition, the framework need to know the path of the local copy of the
    WSCombiner. All this is done automatically by sourcing the framework setup script from the root directory of `hh_combination_fw`, which needs to be setup once before the first usage:

    ~~~~
    source setup_framework.sh
    ~~~~

    The framework should be set up correctly now and you can continue with step 5. In case of problems in step 5 or 6, please remove
    - `./setup_local.sh`
    - `./submodules/RooStatTools/setup_local.sh`
    
    and follow step 4.

4.  **Specify the absolute paths to the dependencies (only if step 3 was not successful)**

    The `hh_combination_fw` needs the path to `workspaceCombiner` package,
    which you should specify in a `setup_local.sh` bash script at two locations:
    - `./setup_local.sh`
    - `./submodules/RooStatTools/setup_local.sh`.

    These bash scripts will be sourced by [`setup.sh`](./setup.sh), before you build the package.

    The `ROOT` setup script should also be placed in `setup_local.sh`.
    For the combination, it is recommended to use the HSG7 ROOT from cvmfs:

    `root 6.04.16-HiggsComb-x86_64-slc6-gcc49-opt`.

    Example contents of `setup_local.sh`:

    ~~~~
    #!/usr/bin/env bash
    
    # - Set the path to `workspaceCombiner` package here (you need to build it before)
    # - See: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/WorkspaceCombiner
    if [[ -z ${WORKSPACECOMBINER_SET} ]]; then
        export WORKSPACECOMBINER_SET=0
        export WORKSPACECOMBINER_PATH="PATH_TO_WSCOMBINER"
        echo "WORKSPACECOMBINER_SET is false, setting workspaceCombiner."
        echo "WORKSPACECOMBINER_PATH: ${WORKSPACECOMBINER_PATH}"
    	WORKSPACECOMBINER_SETUP_SCRIPT=${WORKSPACECOMBINER_PATH}/setup.sh
    	source_if_exists ${WORKSPACECOMBINER_SETUP_SCRIPT}
        export WORKSPACECOMBINER_LIB="${WORKSPACECOMBINER_PATH}/lib/"
        export LD_LIBRARY_PATH=${WORKSPACECOMBINER_LIB}:${LD_LIBRARY_PATH}
    fi
    
    # - Source HSG7, ROOT 6 version from cvmfs
    if [[ -z ${ROOT_SET} ]]; then
       echo "ROOT not set up yet, sourcing ${ROOT}"
       export ROOT_SET=0
       setupATLAS
       lsetup "root 6.04.16-HiggsComb-x86_64-slc6-gcc49-opt"
    fi
    ~~~~

    **What you should modify is:**
    - `WORKSPACECOMBINER_PATH` to your local installation path of `workspaceCombiner`
    - `ROOT`, to the path to the ROOT source script, if you are NOT on lxplus.
    
    Note:
    - that the function `source_if_exists` is specified in the main `setup.sh` script.
    - `[[ -z ${WORKSPACECOMBINER_SET} ]]` are source guards which avoids setting the environment variables twice.

5. **Source the `setup.sh` script**

    Standing in the root directory of `hh_combination_fw`, setup all the necessary environment
    variables with: 

    ~~~~
    source setup.sh
    ~~~~

    Review the std output here, and look for possible `file not found` errors!

6. **Build the project.**

    Now you should be able to build the framework with:

    ~~~~
    make
    ~~~~

    If by any chance you get and error at this stage complaining about `.depend_cpp`, similar to this:
    ~~~~
    make[2]: Entering directory `/.data/englert/projects/hh_combination/software/hhcomb_test/submodules/RooStatTools/src'
    Makefile:32: .depend_cpp: No such file or directory
    ~~~~
    just create an empty file with `touch .depend_cpp`.
    and try `make` again.


[hh_combination_fw]: https://gitlab.cern.ch/atlas-physics/HDBS/DiHiggs/combination/hh_combination_fw
[workspaceCombiner]: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/WorkspaceCombiner
[workspaceCombiner_install]: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/WorkspaceCombiner#Installation

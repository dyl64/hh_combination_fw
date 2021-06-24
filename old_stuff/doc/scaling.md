# Rescaling of POI

## Description of the process

Let's start with writing explicitly how the number of signal events in the region of interest is
determined:

&mu;<sub>reference signal</sub> &sigma;<sub>ref</sub> Br &epsilon; A = (# number of signal events)

where
- &mu;<sub>reference signal</sub> plays to role of the signal normalisation parameter, and it is the parameter of interest
(POI) of our statistical model
- &sigma;<sub>ref</sub> is the reference production cross-section, i.e. the cross-section of the signal Monte Carlo sample,
- Br accounts for any branching fractions,
- A &epsilon; is the acceptance * efficiency of the analysis.



When running a statistical analysis to get an upper limit, we get an upper limit on the number of
signal events, and therefore the POI (i.e &mu;<sub>reference signal</sub>) as well. In this case the
upper limit on the signal events is determined by the background and therefore is a fixed value:

&mu;<sup>U.L.</sup><sub>reference signal</sub> &sigma;<sub>ref</sub> Br &epsilon; A = (# number of signal events)<sup>U.L.</sup>

Expressing &mu;<sub>reference signal</sub><sup>U.L.</sup>:

&mu;<sub>reference signal</sub><sup>U.L.</sup> = (# number of signal events)<sup>U.L.</sup> / ( &sigma;<sub>ref</sub> Br &epsilon; A  )

Note that this is relative to the reference cross-section, branching ratios, acceptance x efficiency.
If we wish to express the upper limit on the production cross-section, we have to multiply
&mu;<sub>reference signal</sub> by the reference cross-section:

&sigma;<sup>U.L</sup> = &mu;<sup>U.L.</sup><sub>reference signal</sub> &sigma;<sub>ref</sub>

We can scale the workspace so that our normalisation parameter &mu; absorbs this reference
cross-section, and the &mu; that we get can be interpreted as the production cross-section.
To do this we apply the following rescaling:

&mu;<sub>new</sub> / &sigma;<sub>ref</sub> = &mu;<sub>reference signal</sub>

So the new POI is:

&mu;<sub>new</sub> = &mu;<sub>reference signal</sub> &sigma;<sub>ref</sub> = &sigma;

## Technical implementation


In the `workspaceCombiner/cfg/template/rescale.xml` template file we have:

~~~~
  <!-- Rescaling. -->
  <Item Name="expr::mu_old('@0/SCALING', NEWPOINAME[0.0,-1.0,20.0])"/>
~~~~

so `mu_old` is equal to `NEWPOI/SCALING` that is &mu;<sub>new</sub>/&sigma;<sub>ref</sub>.

Later we relate `mu_old` with the `OLDPOI` by making them equal:

~~~~
  <!-- PDF -->
  <Item Name="EDIT::NEWPDF(OLDPDF,
	      OLDPOINAME=mu_old,
	      )"/>
~~~~


Here the `SCALING` is replaced by the appropriate scaling parameter when we create the rescaling
config file:

~~~~
    create_rescale_config_file(wsc_rescale_config_template,
                               rescale_cfg_file_path,
                               regularised_ws_path,
                               rescaled_ws_path,
                               new_poiname,
                               scaling)
~~~~

the replacement happends inside `create_rescale_config_file()`:

~~~~
def create_rescale_config_file(template,
                               cfg_file,
                               input_ws,
                              output_ws,
                            newpoi_name,
                               scaling):
    ...
    utils.replace_single_token_in_a_file(cfg_file, 'SCALING',        scaling)
~~~~

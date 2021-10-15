How to run p-value

An example command:
submodules/RooStatTools/bin/runSigCalc ../output/v140invfb_20210531_obs2/rescaled/spin0/bbbb/1000_with_Asimov_POI_0_NP_fit.root  pvalue combWS ModelConfig combData > pvalue/bbbb_1000.log &

Run plotting in a docker
This image provides consistent setup for kl plots, result plots, Accxeff plots.
p-value plots should work (didn't test) despite that the global signifiance will crash.
```
docker build . -f Image/Dockerfile -t plotting
docker run -it -v $(pwd):/workarea plotting /bin/bash
```

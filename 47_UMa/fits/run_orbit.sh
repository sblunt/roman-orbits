#!/bin/bash

radvel fit -s 47UMa_radvel.py
radvel mcmc -s 47UMa_radvel.py --nwalkers=70
radvel derive -s 47UMa_radvel.py 
radvel plot -t rv derived corner trend -s 47UMa_radvel.py
radvel ic -t nplanets e trend jit -s 47UMa_radvel.py
radvel report -s 47UMa_radvel.py

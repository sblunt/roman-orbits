#!/bin/bash

radvel fit -s 39091_radvel.py
radvel mcmc -s 39091_radvel.py --nwalkers=100
radvel derive -s 39091_radvel.py 
radvel plot -t rv derived corner trend -s 39091_radvel.py
radvel ic -t nplanets e trend jit -s 39091_radvel.py
# radvel report -s 39091_radvel.py
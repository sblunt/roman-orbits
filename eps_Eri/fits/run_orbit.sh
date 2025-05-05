#!/bin/bash

radvel fit -s 22049_radvel.py
radvel mcmc -s 22049_radvel.py --nwalkers=70
radvel derive -s 22049_radvel.py 
radvel plot -t rv derived corner trend -s 22049_radvel.py
radvel ic -t nplanets e trend jit -s 22049_radvel.py
# radvel report -s 22049_radvel.py
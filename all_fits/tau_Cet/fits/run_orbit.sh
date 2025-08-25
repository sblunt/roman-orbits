#!/bin/bash

radvel fit -s 10700_radvel.py
radvel mcmc -s 10700_radvel.py --nwalkers=150
radvel derive -s 10700_radvel.py 
radvel plot -t rv derived corner trend -s 10700_radvel.py
radvel ic -t nplanets e trend jit -s 10700_radvel.py
# radvel report -s 10700_radvel.py
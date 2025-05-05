#!/bin/bash

radvel fit -s 9826_radvel.py
radvel mcmc -s 9826_radvel.py --nwalkers=100
radvel derive -s 9826_radvel.py 
radvel plot -t rv derived corner trend -s 9826_radvel.py
radvel ic -t nplanets e trend jit -s 9826_radvel.py
# radvel report -s 9826_radvel.py
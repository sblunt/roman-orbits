#!/bin/bash

radvel fit -s 192310_radvel.py
radvel mcmc -s 192310_radvel.py --nwalkers=100
radvel derive -s 192310_radvel.py 
radvel plot -t rv derived corner trend -s 192310_radvel.py
radvel ic -t nplanets e trend jit -s 192310_radvel.py
# radvel report -s 192310_radvel.py
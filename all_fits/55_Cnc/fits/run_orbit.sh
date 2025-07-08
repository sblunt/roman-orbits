#!/bin/bash

radvel fit -s 55Cnc_radvel.py
radvel mcmc -s 55Cnc_radvel.py --nsteps=20000 --nwalkers=200
radvel derive -s 55Cnc_radvel.py 
radvel plot -t rv derived corner trend -s 55Cnc_radvel.py
radvel ic -t nplanets e trend jit -s 55Cnc_radvel.py
radvel report -s 55Cnc_radvel.py

#!/bin/bash

radvel fit -s radvel_setup.py
radvel mcmc -s radvel_setup.py --nwalkers=64
radvel derive -s radvel_setup.py 
radvel plot -t rv derived corner trend -s radvel_setup.py
radvel ic -t nplanets e trend jit -s radvel_setup.py
radvel report -s radvel_setup.py

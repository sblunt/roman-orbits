#!/bin/bash

radvel fit -s GJ687_radvel.py
radvel mcmc -s GJ687_radvel.py --nwalkers=200
radvel derive -s GJ687_radvel.py 
radvel plot -t rv derived corner trend -s GJ687_radvel.py
radvel ic -t nplanets e trend jit -s GJ687_radvel.py
radvel report -s GJ687_radvel.py

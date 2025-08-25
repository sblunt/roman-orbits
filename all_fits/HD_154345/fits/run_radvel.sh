#!/bin/bash

radvel fit -s HD154345_radvel.py
radvel mcmc -s HD154345_radvel.py --nwalkers=64
radvel derive -s HD154345_radvel.py 
radvel plot -t rv derived corner trend -s HD154345_radvel.py
radvel ic -t nplanets e trend jit -s HD154345_radvel.py
radvel report -s HD154345_radvel.py

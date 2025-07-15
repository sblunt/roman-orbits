#!/bin/bash

radvel fit -s HD160691_radvel.py
radvel mcmc -s HD160691_radvel.py --nwalkers=128
radvel derive -s HD160691_radvel.py 
radvel plot -t rv derived corner trend -s HD160691_radvel.py
radvel ic -t nplanets e trend jit -s HD160691_radvel.py
radvel report -s HD160691_radvel.py

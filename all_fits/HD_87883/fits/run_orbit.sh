#!/bin/bash

radvel fit -s HD87883_radvel.py
radvel mcmc -s HD87883_radvel.py --nwalkers=64
radvel derive -s HD87883_radvel.py 
radvel plot -t rv derived corner trend -s HD87883_radvel.py
radvel ic -t nplanets e trend jit -s HD87883_radvel.py
radvel report -s HD87883_radvel.py

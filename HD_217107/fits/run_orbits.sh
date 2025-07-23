#!/bin/bash

radvel fit -s HD217107_radvel.py
radvel mcmc -s HD217107_radvel.py 
radvel derive -s HD217107_radvel.py 
radvel plot -t rv derived corner trend -s HD217107_radvel.py
radvel ic -t nplanets e trend jit -s HD217107_radvel.py
radvel report -s HD217107_radvel.py
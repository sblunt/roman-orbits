#!/bin/bash

radvel fit -s HD190360_radvel.py
radvel mcmc -s HD190360_radvel.py 
radvel derive -s HD190360_radvel.py 
radvel plot -t rv derived corner trend -s HD190360_radvel.py
radvel ic -t nplanets e trend jit -s HD190360_radvel.py
radvel report -s HD190360_radvel.py

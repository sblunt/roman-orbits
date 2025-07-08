#!/bin/bash

radvel fit -s 14Her_radvel.py
radvel mcmc -s 14Her_radvel.py
radvel derive -s 14Her_radvel.py 
radvel plot -t rv derived corner trend -s 14Her_radvel.py
radvel ic -t nplanets e trend jit -s 14Her_radvel.py
radvel report -s 14Her_radvel.py

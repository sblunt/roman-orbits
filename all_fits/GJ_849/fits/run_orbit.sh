#!/bin/bash

radvel fit -s GJ849_radvel.py
radvel mcmc -s GJ849_radvel.py 
radvel derive -s GJ849_radvel.py 
radvel plot -t rv derived corner trend -s GJ849_radvel.py
radvel ic -t nplanets e trend jit -s GJ849_radvel.py
radvel report -s GJ849_radvel.py

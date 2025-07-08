#!/bin/bash

radvel fit -s HD134987_radvel.py
radvel mcmc -s HD134987_radvel.py
radvel derive -s HD134987_radvel.py 
radvel plot -t rv derived corner trend -s HD134987_radvel.py
radvel ic -t nplanets e trend jit -s HD134987_radvel.py
radvel report -s HD134987_radvel.py

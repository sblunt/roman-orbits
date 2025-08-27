#!/bin/bash

radvel fit -s HD217107_radvel.py -d results
radvel plot -t rv -s HD217107_radvel.py -d results
radvel mcmc -s HD217107_radvel.py -d results --nsteps 10000
radvel derive -s HD217107_radvel.py -d results
radvel plot -t trend rv corner derived -s HD217107_radvel.py -d results

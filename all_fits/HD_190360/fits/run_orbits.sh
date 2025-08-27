radvel fit -s HD190360_radvel.py -d results
radvel mcmc -s HD190360_radvel.py  -d results --nsteps 6000
radvel derive -s HD190360_radvel.py -d results
radvel plot -t rv trend derived corner -s HD190360_radvel.py -d results
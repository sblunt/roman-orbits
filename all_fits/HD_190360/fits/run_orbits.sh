radvel fit -s HD190360_radvel.py -d results
radvel mcmc -s HD190360_radvel.py  -d results --nensembles 8 --burnGR 1.05
radvel derive -s HD190360_radvel.py -d results
radvel plot -t rv derived corner trend -s HD190360_radvel.py -d results
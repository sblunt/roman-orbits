radvel fit -s 22049_radvel.py -d results
radvel plot -t rv -s 22049_radvel.py -d results
radvel mcmc -s 22049_radvel.py -d results --maxGR 1.003
radvel derive -s 22049_radvel.py -d results
radvel plot -t rv trend derived corner -s 22049_radvel.py -d results
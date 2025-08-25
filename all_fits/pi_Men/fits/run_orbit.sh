radvel fit -s 39091_radvel.py -d results
radvel plot -t rv -s 39091_radvel.py -d results
radvel mcmc -s 39091_radvel.py -d results
radvel derive -s 39091_radvel.py -d results
radvel plot -t rv trend derived corner -s 39091_radvel.py -d results
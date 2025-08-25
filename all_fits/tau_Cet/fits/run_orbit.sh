radvel fit -s 10700_radvel.py -d results
radvel plot -t rv -s 10700_radvel.py -d results
radvel mcmc -s 10700_radvel.py -d results
radvel derive -s 10700_radvel.py -d results
radvel plot -t rv trend derived corner -s 10700_radvel.py -d results
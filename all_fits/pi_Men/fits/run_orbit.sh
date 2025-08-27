radvel fit -s 39091_radvel.py -d results
radvel plot -t rv -s 39091_radvel.py -d results
radvel mcmc -s 39091_radvel.py -d results --nsteps 4000
radvel derive -s 39091_radvel.py -d results
radvel plot -t  trend derived corner rv -s 39091_radvel.py -d results
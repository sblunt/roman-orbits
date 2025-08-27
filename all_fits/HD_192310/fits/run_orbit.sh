radvel fit -s 192310_radvel.py -d results
radvel plot -t rv -s 192310_radvel.py -d results
radvel mcmc -s 192310_radvel.py -d results --nsteps 4000
radvel derive -s 192310_radvel.py -d results
radvel plot -t rv trend derived corner -s 192310_radvel.py -d results
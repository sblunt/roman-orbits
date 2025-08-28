radvel fit -s HD160691_radvel.py -d results
radvel plot -t rv -s HD160691_radvel.py -d results
radvel mcmc -s HD160691_radvel.py -d results --nsteps 15000
radvel derive -s HD160691_radvel.py -d results
radvel plot -t rv trend derived corner -s HD160691_radvel.py -d results
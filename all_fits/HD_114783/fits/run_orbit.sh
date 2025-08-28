# radvel fit -s HD114783_radvel.py -d results
# radvel plot -t rv -s HD114783_radvel.py -d results
# radvel mcmc -s HD114783_radvel.py -d results --nsteps 5000
radvel derive -s HD114783_radvel.py -d results
radvel plot -t rv trend derived corner -s HD114783_radvel.py -d results
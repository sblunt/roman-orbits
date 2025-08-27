radvel fit -s HD154345_radvel.py -d results
radvel plot -t rv -s HD154345_radvel.py -d results
radvel mcmc -s HD154345_radvel.py -d results --nsteps 5000
radvel derive -s HD154345_radvel.py -d results
radvel plot -t rv trend derived corner -s HD154345_radvel.py -d results
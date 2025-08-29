radvel fit -s 55Cnc_radvel.py -d results
radvel plot -t rv -s 55Cnc_radvel.py -d results
radvel mcmc -s 55Cnc_radvel.py -d results --nwalkers 100 --nsteps 20000
radvel derive -s 55Cnc_radvel.py -d results
radvel plot -t rv trend derived corner -s 55Cnc_radvel.py -d results
radvel fit -s 9826_radvel.py -d results
radvel plot -t rv -s 9826_radvel.py -d results
radvel mcmc -s 9826_radvel.py -d results --maxGR 1.003 --nsteps 10000
radvel derive -s 9826_radvel.py -d results
radvel plot -t rv trend derived corner -s 9826_radvel.py -d results
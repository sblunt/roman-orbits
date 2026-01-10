radvel fit -s HD219134_radvel.py -d results
radvel plot -t rv -s HD219134_radvel.py -d results
radvel mcmc -s HD219134_radvel.py -d results
radvel derive -s HD219134_radvel.py -d results
radvel plot -t rv trend derived corner -s HD219134_radvel.py -d results
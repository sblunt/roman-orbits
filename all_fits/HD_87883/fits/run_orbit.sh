radvel fit -s HD87883_radvel.py -d results
radvel plot -t rv -s HD87883_radvel.py -d results
radvel mcmc -s HD87883_radvel.py -d results
radvel derive -s HD87883_radvel.py -d results
radvel plot -t rv trend derived corner -s HD87883_radvel.py -d results
radvel fit -s /roman_orbits/all_fits/HD_134987/fits/HD134987_radvel.py -d /roman_orbits/all_fits/HD_134987/fits/results
radvel mcmc -s /roman_orbits/all_fits/HD_134987/fits/HD134987_radvel.py --nsteps 12000 -d /roman_orbits/all_fits/HD_134987/fits/results
radvel derive -s /roman_orbits/all_fits/HD_134987/fits/HD134987_radvel.py -d /roman_orbits/all_fits/HD_134987/fits/results
radvel plot -t rv trend derived corner -s HD134987_radvel.py -d /roman_orbits/all_fits/HD_134987/fits/results
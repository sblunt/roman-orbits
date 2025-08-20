radvel fit -s /roman_orbits/all_fits/HD_134987/fits/HD134987_radvel.py -d /roman_orbits/all_fits/HD_134987/fits/results
radvel mcmc -s /roman_orbits/all_fits/HD_134987/fits/HD134987_radvel.py --nensembles 8 --burnGR 1.01 --burnAfactor 200 -d /roman_orbits/all_fits/HD_134987/fits/results
radvel derive -s /roman_orbits/all_fits/HD_134987/fits/HD134987_radvel.py -d /roman_orbits/all_fits/HD_134987/fits/results
radvel plot -t rv derived corner trend -s HD134987_radvel.py -d /roman_orbits/all_fits/HD_134987/fits/results
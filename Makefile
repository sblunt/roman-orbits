docker:
	docker build . --tag roman-orbits
	docker run roman-orbits pip3 install -r /roman_orbits/requirements.txt --root-user-action 
	docker run -it roman-orbits:latest bash
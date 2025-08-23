docker:
	docker build . --tag roman-orbits:latest --cache-to type=inline --memory="8g" --cache-from roman-orbits:latest
	docker run -v .:/roman_orbits -it --rm roman-orbits:latest bash
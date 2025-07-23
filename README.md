# roman-orbits
Collection of data and orbit fits for stars of interest to the Roman coronagraph

Progress spreadsheet: https://docs.google.com/spreadsheets/d/1Uga6Lc0byhLyxEZvPCrVjI--WwV_y-GT5HVC6B65uro/edit?usp=sharing
Video tutorial: https://www.youtube.com/watch?v=J8cNtCHYPOY

NOTE: Targets from spreadsheet are from [plandb database](https://plandb.sioslab.com/), accessed March 16 2025. Targets from that spreadsheet with Vmag too low or otherwise unsuitable are in second spreadsheet tab ("killed").

DOCKER SETUP INSTRUCTIONS:

1. Set an environment variable called ROMAN_ORBITS that points to the root of this repository. E.g.:

    $ export ROMAN_ORBITS=/home/sblunt/GitHub/roman-orbits

(Add that line to your .bashrc, .profile, or some other such file to avoid having to define this variable every time.)

2. [Install docker on your machine](https://docs.sevenbridges.com/docs/install-docker), if it isn't already installed.

3. Start a docker container running:

    $ make docker

4. That's it! If everything works correctly, you should now be inside a docker container, and can run orbit fits
within a standardized environment.


## Sanity Checks:

- Examine trend files. Do chains look converged?
- Make sure time offsets have been accounted for in file combinations
- Parameters consistent with Exoplanet Archive?
- Previous fit? Compare output if so

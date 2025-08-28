import pandas as pd
import numpy as np
import radvel
import os

# Define global planetary system and dataset parameters
starname = "HD95735"
nplanets = 1  # number of planets in the system
instnames = [ "HIRES-post", "APF", "SOPHIE"]
ntels = len(instnames)  # number of instruments with unique velocity zero-points
fitting_basis = "per tc secosw sesinw k"  # Fitting basis, see radvel.basis.BASIS_NAMES for available basis names
bjd0 = 2450000.0
planet_letters = {1: "b", 2: "c"}

# Define prior centers (initial guesses) in a basis of your choice (need not be in the fitting basis)
anybasis_params = radvel.Parameters(
    nplanets, basis="per tp e w k"
)  # initialize Parameters object

anybasis_params["per2"] = radvel.Parameter(value=12.9532)  # period of 1st planet
anybasis_params["tp2"] = radvel.Parameter(value=57190.42978287143)  # time of periastron of 1st planet
anybasis_params["e2"] = radvel.Parameter(value=0.101)  # eccentricity of 'per tp secosw sesinw k'1st planet
anybasis_params["w2"] = radvel.Parameter(value=-1.7928782287003768)  # argument of periastron of the star's orbit for 1st planet
anybasis_params["k2"] = radvel.Parameter(value=1.59)  # velocity semi-amplitude for 1st planet

anybasis_params["per1"] = radvel.Parameter(value=3190)  # period of 2nd planet
anybasis_params["tp1"] = radvel.Parameter(value=2456792.79)  # time of periastron of 2nd planet
anybasis_params["e1"] = radvel.Parameter(value=0.14)  # eccentricity of 'per tp secosw sesinw k' 2nd planet
anybasis_params["w1"] = radvel.Parameter(value=0.1) # RAD (?) # argument of periastron of the star's orbit for 2nd planet
anybasis_params["k1"] = radvel.Parameter(value=1.56)  # velocity semi-amplitude for 2nd planet


####################################

# need to update


anybasis_params["dvdt"] = radvel.Parameter(value=0.0)  # slope
anybasis_params["curv"] = radvel.Parameter(value=0.0)  # curvature

anybasis_params["gamma_SOPHIE"] = radvel.Parameter(-84283.79)
anybasis_params["gamma_HIRES-post"] = radvel.Parameter(-0.93)
anybasis_params["gamma_APF"] = radvel.Parameter(-1.46)

anybasis_params["jit_SOPHIE"] = radvel.Parameter(value=5)
anybasis_params["jit_HIRES-post"] = radvel.Parameter(value=5)
anybasis_params["jit_APF"] = radvel.Parameter(value=5)

#######################################

# Convert input orbital parameters into the fitting basis
params = anybasis_params.basis.to_any_basis(anybasis_params, fitting_basis)

params["dvdt"].vary = False
params["curv"].vary = False

# Load radial velocity data, in this example the data is contained in an hdf file,
# the resulting dataframe or must have 'time', 'mnvel', 'errvel', and 'tel' keys
# the velocities are expected to be in m/s
this_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(this_dir)  # assumes the data dir and fits dir are in same parent dir
path = os.path.join(parent_dir, "data", "HD95735_rv_combined_binned.txt")

data = pd.read_csv(
    path,
    header=None,
    skiprows=1,
    delim_whitespace=True,
    names=("time", "mnvel", "errvel", "tel"),
)

# Define prior shapes and widths here.

## need to change ?
priors = [
    radvel.prior.EccentricityPrior(nplanets),  # Keeps eccentricity < 1
    radvel.prior.PositiveKPrior(nplanets),  # Keeps K > 0
    radvel.prior.HardBounds("jit_SOPHIE", 0.0, 100.0),
    radvel.prior.HardBounds("jit_HIRES-post", 0.0, 100.0),
    radvel.prior.HardBounds("jit_APF", 0.0, 100.0)
]

# abscissa for slope and curvature terms (should be near mid-point of time baseline)
time_base = np.mean([np.min(data.time), np.max(data.time)])


# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=0.386, mstar_err=0.039)  # numbers from Diaz et al. 2019

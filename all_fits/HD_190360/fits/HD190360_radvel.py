import pandas as pd
import numpy as np
import radvel

# Define global planetary system and dataset parameters
starname = "HD190360"
nplanets = 2  # number of planets in the system
instnames = ["ELODIE", "AFOE", "SOPHIE", "Hamilton", "HIRES-pre", "HIRES-post", "APF"]
ntels = len(instnames)  # number of instruments with unique velocity zero-points
fitting_basis = "per tc secosw sesinw k"  # Fitting basis, see radvel.basis.BASIS_NAMES for available basis names
bjd0 = 2450000.0
planet_letters = {1: "b", 2: "c"}

# Define prior centers (initial guesses) in a basis of your choice (need not be in the fitting basis)
anybasis_params = radvel.Parameters(
    nplanets, basis="per tp e w k"
)  # initialize Parameters object

anybasis_params["per1"] = radvel.Parameter(value=2887.7)  # period of 1st planet
anybasis_params["tp1"] = radvel.Parameter(
    value=2459286
)  # time of periastron of 1st planet
anybasis_params["e1"] = radvel.Parameter(
    value=0.3291
)  # eccentricity of 'per tp secosw sesinw k'1st planet
anybasis_params["w1"] = radvel.Parameter(
    value=0.201
)  # argument of periastron of the star's orbit for 1st planet
anybasis_params["k1"] = radvel.Parameter(
    value=22.74
)  # velocity semi-amplitude for 1st planet
anybasis_params["per2"] = radvel.Parameter(value=17.11695)  # period of 2nd planet
anybasis_params["tp2"] = radvel.Parameter(
    value=2458993.34
)  # time of periastron of 2nd planet
anybasis_params["e2"] = radvel.Parameter(
    value=0.164
)  # eccentricity of 'per tp secosw sesinw k' 2nd planet
anybasis_params["w2"] = radvel.Parameter(
    value=5.723
)  # argument of periastron of the star's orbit for 2nd planet
anybasis_params["k2"] = radvel.Parameter(
    value=5.49
)  # velocity semi-amplitude for 2nd planet

anybasis_params["dvdt"] = radvel.Parameter(value=0.0)  # slope
anybasis_params["curv"] = radvel.Parameter(value=0.0)  # curvature

anybasis_params["gamma_ELODIE"] = radvel.Parameter(-45347.5)  # velocity zero-point
anybasis_params["gamma_AFOE"] = radvel.Parameter(-45349.9)
anybasis_params["gamma_SOPHIE"] = radvel.Parameter(-45214.67)
anybasis_params["gamma_Hamilton"] = radvel.Parameter(-3.77)
anybasis_params["gamma_HIRES-pre"] = radvel.Parameter(-1.56)
anybasis_params["gamma_HIRES-post"] = radvel.Parameter(-2.51)
anybasis_params["gamma_APF"] = radvel.Parameter(1.13)

anybasis_params["jit_ELODIE"] = radvel.Parameter(value=3.2)  # jitter
anybasis_params["jit_AFOE"] = radvel.Parameter(value=7.6)
anybasis_params["jit_SOPHIE"] = radvel.Parameter(value=2.01)
anybasis_params["jit_Hamilton"] = radvel.Parameter(value=5.34)
anybasis_params["jit_HIRES-pre"] = radvel.Parameter(value=3.03)
anybasis_params["jit_HIRES-post"] = radvel.Parameter(value=2.65)
anybasis_params["jit_APF"] = radvel.Parameter(value=2.2)


# Convert input orbital parameters into the fitting basis
params = anybasis_params.basis.to_any_basis(anybasis_params, fitting_basis)

params["dvdt"].vary = False
params["curv"].vary = False

# Load radial velocity data, in this example the data is contained in an hdf file,
# the resulting dataframe or must have 'time', 'mnvel', 'errvel', and 'tel' keys
# the velocities are expected to be in m/s
path = "/roman_orbits/all_fits/HD_190360/data/HD190360_rv_combined_binned.txt"
data = pd.read_csv(
    path,
    header=None,
    skiprows=1,
    delim_whitespace=True,
    names=("time", "mnvel", "errvel", "tel"),
)

# Define prior shapes and widths here.
priors = [
    radvel.prior.EccentricityPrior(nplanets),  # Keeps eccentricity < 1
    radvel.prior.PositiveKPrior(nplanets),  # Keeps K > 0
    radvel.prior.HardBounds("jit_ELODIE", 0.0, 10.0),
    radvel.prior.HardBounds("jit_AFOE", 0.0, 50.0),
    radvel.prior.HardBounds("jit_SOPHIE", 0.0, 10.0),
    radvel.prior.HardBounds("jit_Hamilton", 0.0, 10.0),
    radvel.prior.HardBounds("jit_HIRES-pre", 0.0, 10.0),
    radvel.prior.HardBounds("jit_HIRES-post", 0.0, 10.0),
    radvel.prior.HardBounds("jit_APF", 0.0, 10.0),
]

# abscissa for slope and curvature terms (should be near mid-point of time baseline)
time_base = np.mean([np.min(data.time), np.max(data.time)])


# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=0.986, mstar_err=0.039)  # numbers from Rosenthal et al. 2021

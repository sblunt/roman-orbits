import pandas as pd
import numpy as np
import radvel

# Load Data
data = pd.read_csv("../data/all_rvs.csv")

# Define global planetary system
starname = "HD87883"
nplanets = 1
instnames = list(np.unique(data["tel"]))
ntels = len(instnames)
fitting_basis = 'per tc secosw sesinw k'
bjd0 = 2440000.
planet_letters = {1:'b'}

anybasis_params = radvel.Parameters(
    nplanets,
    basis = 'per tp e w k',
)

# Parameters retrieved from the Feng et al. 2022 fit 
# https://exoplanetarchive.ipac.caltech.edu/overview/HD%2087883
anybasis_params['per1'] = radvel.Parameter(value = 3309.22)
anybasis_params['tp1'] = radvel.Parameter(value = 2450345.19)
anybasis_params['e1'] = radvel.Parameter(value = 0.707)
anybasis_params['w1'] = radvel.Parameter(value = 289.351 * np.pi / 180.)
anybasis_params['k1'] = radvel.Parameter(value = 51.435)

anybasis_params['dvdt'] = radvel.Parameter(value = 0.0)
anybasis_params['curv'] = radvel.Parameter(value = 0.0)

# Adding instrument rv offset and jitter parameters (assuming 5 m/s for all for now)
# Check this. I have split up each published data set by publication.
# So there are multiple hires_j's, for example, one per publication.
for inst in instnames:
    anybasis_params['gamma_{}'.format(inst)] = radvel.Parameter(value = 0)
for inst in instnames:
    anybasis_params['jit_{}'.format(inst)] = radvel.Parameter(value = 5)

params = anybasis_params.basis.to_any_basis(anybasis_params, fitting_basis)

params['dvdt'].vary = False
params['curv'].vary = False

priors = [
    radvel.prior.EccentricityPrior(nplanets),
    radvel.prior.PositiveKPrior(nplanets),
]
# Adding instrument-specific hardbounds priors for jitter
# Setting all hardbounds to 0 to 10 m/s for now
for inst in instnames:
    priors.append(
        radvel.prior.HardBounds(
            'jit_{}'.format(inst),
            0.0,
            25.0,
        )
    )

time_base = np.mean([np.amin(data.time), np.amax(data.time)])

# Parameters retrieved from the Feng et al. 2022 fit 
# https://exoplanetarchive.ipac.caltech.edu/overview/HD%2087883
stellar = dict(mstar = 0.810, mstar_err = 0.091)

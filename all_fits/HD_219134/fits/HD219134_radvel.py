import pandas as pd
import numpy as np
import radvel

# Load Data
data = pd.read_csv("../data/all_rvs_binned.csv")

# Define global planetary system
starname = "HD219134"
nplanets = 6
instnames = list(np.unique(data["tel"]))
ntels = len(instnames)
fitting_basis = 'per tc secosw sesinw k'
bjd0 = 2440000.
planet_letters = {
    1:'b',
    2:'c',
    3:'d',
    4:'f',
    5:'g',
    6:'h',
}

anybasis_params = radvel.Parameters(
    nplanets,
    basis = 'per tp e w k',
)

# https://exoplanetarchive.ipac.caltech.edu/overview/HD%20219134

# Parameters retrieved from the Rosenthal 2021 fit unless otherwise noted
# b
anybasis_params['per1'] = radvel.Parameter(value = 3.092947)
anybasis_params['tp1'] = radvel.Parameter(value = 2449999.5) # Vogt 2015 fit
anybasis_params['e1'] = radvel.Parameter(value = 0.0630)
anybasis_params['w1'] = radvel.Parameter(value = 9.70 * np.pi / 180.)
anybasis_params['k1'] = radvel.Parameter(value = 2.13)

# c
anybasis_params['per2'] = radvel.Parameter(value = 6.76406)
anybasis_params['tp2'] = radvel.Parameter(value = 2449998.5) # Vogt 2015 fit
anybasis_params['e2'] = radvel.Parameter(value = 0.16)
anybasis_params['w2'] = radvel.Parameter(value = 6.30 * np.pi / 180.)
anybasis_params['k2'] = radvel.Parameter(value = 1.44)

# d
anybasis_params['per3'] = radvel.Parameter(value = 46.734)
anybasis_params['tp3'] = radvel.Parameter(value = 2449964.) # Vogt 2015 fit
anybasis_params['e3'] = radvel.Parameter(value = 0.0770)
anybasis_params['w3'] = radvel.Parameter(value = 340. * np.pi / 180.)
anybasis_params['k3'] = radvel.Parameter(value = 3.43)

# f: This is the controversial planet
anybasis_params['per4'] = radvel.Parameter(value = 22.7945)
anybasis_params['tp4'] = radvel.Parameter(value = 2449983.) # Vogt 2015 fit
anybasis_params['e4'] = radvel.Parameter(value = 0.0720)
anybasis_params['w4'] = radvel.Parameter(value = 10. * np.pi / 180.)
anybasis_params['k4'] = radvel.Parameter(value = 2.05)

# g: All parameters from Vogt 2015
anybasis_params['per5'] = radvel.Parameter(value = 94.2)
anybasis_params['tp5'] = radvel.Parameter(value = 2449972.)
anybasis_params['e5'] = radvel.Parameter(value = 0.)
anybasis_params['w5'] = radvel.Parameter(value = 0. * np.pi / 180.)
anybasis_params['k5'] = radvel.Parameter(value = 1.8)

# h
anybasis_params['per6'] = radvel.Parameter(value = 2104.)
anybasis_params['tp6'] = radvel.Parameter(value = 2448725.) # Vogt 2015 fit
anybasis_params['e6'] = radvel.Parameter(value = 0.025)
anybasis_params['w6'] = radvel.Parameter(value = 0.0 * np.pi / 180.)
anybasis_params['k6'] = radvel.Parameter(value = 5.73)

anybasis_params['dvdt'] = radvel.Parameter(value = 0.0)
anybasis_params['curv'] = radvel.Parameter(value = 0.0)

# Adding instrument rv offset and jitter parameters (assuming 5 m/s for all for now)
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
for inst in instnames:
    priors.append(
        radvel.prior.HardBounds(
            'jit_{}'.format(inst),
            0.0,
            1000
        )
    )

time_base = np.mean([np.amin(data.time), np.amax(data.time)])

# Parameters retrieved from the Seager 2021 fit 
stellar = dict(mstar = 0.81, mstar_err = 0.03)

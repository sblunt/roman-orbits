import pandas as pd
import numpy as np
import radvel

# Load Data
data = pd.read_csv("../data/all_rvs_binned.csv")

# Define global planetary system
starname = "HD160691"
nplanets = 4
instnames = list(np.unique(data["tel"]))
ntels = len(instnames)
fitting_basis = 'per tc secosw sesinw k'
bjd0 = 2440000.
planet_letters = {
    1:'b',
    2:'d',
    3:'e',
    4:'c',
}

anybasis_params = radvel.Parameters(
    nplanets,
    basis = 'per tp e w k',
)

# https://exoplanetarchive.ipac.caltech.edu/overview/HD%20160691

# Parameters retrieved from the Benedict et al. 2022 fit (in the paper)
anybasis_params['per1'] = radvel.Parameter(value = 645.0)
anybasis_params['tp1'] = radvel.Parameter(value = 2452396)
anybasis_params['e1'] = radvel.Parameter(value = 0.036)
anybasis_params['w1'] = radvel.Parameter(value = 39. * np.pi / 180.)
anybasis_params['k1'] = radvel.Parameter(value = 36.1)

# Parameters retrieved from the Gozdziewski et al. 2007 fit
anybasis_params['per2'] = radvel.Parameter(value = 9.6392)
anybasis_params['tp2'] = radvel.Parameter(value = 2400052)
anybasis_params['e2'] = radvel.Parameter(value = 0.16)
anybasis_params['w2'] = radvel.Parameter(value = 197. * np.pi / 180.)
anybasis_params['k2'] = radvel.Parameter(value = 2.94)

anybasis_params['per3'] = radvel.Parameter(value = 307.9)
anybasis_params['tp3'] = radvel.Parameter(value = 2452720.)
anybasis_params['e3'] = radvel.Parameter(value = 0.091)
anybasis_params['w3'] = radvel.Parameter(value = 193. * np.pi / 180.)
anybasis_params['k3'] = radvel.Parameter(value = 12.23)

anybasis_params['per4'] = radvel.Parameter(value = 3947.)
anybasis_params['tp4'] = radvel.Parameter(value = 2453264.)
anybasis_params['e4'] = radvel.Parameter(value = 0.022)
anybasis_params['w4'] = radvel.Parameter(value = 84. * np.pi / 180.)
anybasis_params['k4'] = radvel.Parameter(value = 22.18)

anybasis_params['dvdt'] = radvel.Parameter(value = 0.0)
anybasis_params['curv'] = radvel.Parameter(value = 0.0)

# Adding instrument rv offset and jitter parameters
for inst in instnames:
    anybasis_params['gamma_{}'.format(inst)] = radvel.Parameter(value=np.mean(data.mnvel.values[data.tel==inst]))
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
            0.1,
            2000.,
        )
    )

time_base = np.mean([np.amin(data.time), np.amax(data.time)])

# Parameters retrieved from the Benedict et al. 2002 fit 
stellar = dict(mstar = 1.13, mstar_err = 0.02)

import pandas as pd
import numpy as np
import radvel
from radvel.orbit import timeperi_to_timetrans

# Load Data
data = pd.read_csv("../data/all_rvs_binned.csv")

three_planet = True # if True, only fit for the inner two transiting planets & outer long-period planet

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
    basis = 'per tc e w k',
)

# https://exoplanetarchive.ipac.caltech.edu/overview/HD%20219134

#
# b: 
anybasis_params['per1'] = radvel.Parameter(value = 3.092920) # Seager et al 21
anybasis_params['tc1'] = radvel.Parameter(value = 2458765.95501) # Seager et al 21
anybasis_params['e1'] = radvel.Parameter(value = 0.06) # Rosenthal+ 21
anybasis_params['w1'] = radvel.Parameter(value = 9.7 * np.pi/180) # Rosenthal+ 21
anybasis_params['k1'] = radvel.Parameter(value = 1.9) # Rosenthal+ 21

# c: Seager et al 21
anybasis_params['per2'] = radvel.Parameter(value = 6.765149) # Seager et al 21
anybasis_params['tc2'] = radvel.Parameter(value = 2458766.16927) # Seager et al 21
anybasis_params['e2'] = radvel.Parameter(value = 0.16) # Rosenthal+ 21
anybasis_params['w2'] = radvel.Parameter(value = 6.30 * np.pi / 180.) # Rosenthal+ 21
anybasis_params['k2'] = radvel.Parameter(value = 1.44) # Rosenthal+ 21

# f: This is the controversial planet (params from Vogt+ 15): controversy
# comes from identical period in S-indices (reported by Johsnon+ 2016).
# I (Sarah) think it's fine to fit for this even if it is stellar activity. 
# Could stand to think about this more, but I doubt it affects the outer planet
# params
tc4 = timeperi_to_timetrans(2449983, 22.805, 0.0720,  10. * np.pi / 180.)
anybasis_params['per4'] = radvel.Parameter(value = 22.805)
anybasis_params['tc4'] = radvel.Parameter(value = tc4)
anybasis_params['e4'] = radvel.Parameter(value = 0.01)
anybasis_params['w4'] = radvel.Parameter(value = 10. * np.pi / 180.)
anybasis_params['k4'] = radvel.Parameter(value = 2.3)

# d: Vogt+ 15
tc3 = timeperi_to_timetrans(2449964, 46.71, 0, 0)
anybasis_params['per3'] = radvel.Parameter(value = 46.71)
anybasis_params['tc3'] = radvel.Parameter(value = tc3)
anybasis_params['e3'] = radvel.Parameter(value = 0.01)
anybasis_params['w3'] = radvel.Parameter(value = 10. * np.pi / 180.)
anybasis_params['k3'] = radvel.Parameter(value = 4.4)

# g: Vogt+ 15
tc5 = timeperi_to_timetrans(2449972, 94.2, 0,0)
anybasis_params['per5'] = radvel.Parameter(value = 94.2)
anybasis_params['tc5'] = radvel.Parameter(value = tc5)
anybasis_params['e5'] = radvel.Parameter(value = 0.01)
anybasis_params['w5'] = radvel.Parameter(value = 10 * np.pi / 180.)
anybasis_params['k5'] = radvel.Parameter(value = 1.8)

# h: Vogt+ 15
tc6 = timeperi_to_timetrans(2448725., 22047, 0, 0)
anybasis_params['per6'] = radvel.Parameter(value = 2247.)
anybasis_params['tc6'] = radvel.Parameter(value = tc6)
anybasis_params['e6'] = radvel.Parameter(value = 0.025)
anybasis_params['w6'] = radvel.Parameter(value = 0.0 * np.pi / 180.)
anybasis_params['k6'] = radvel.Parameter(value = 5.73)

anybasis_params['dvdt'] = radvel.Parameter(value = 0.0)
anybasis_params['curv'] = radvel.Parameter(value = 0.0)

# Adding instrument rv offset and jitter parameters
for inst in instnames:
    anybasis_params['gamma_{}'.format(inst)] = radvel.Parameter(value = np.mean(data.mnvel[data.tel == inst]))
for inst in instnames:
    anybasis_params['jit_{}'.format(inst)] = radvel.Parameter(value = 5)


params = anybasis_params.basis.to_any_basis(anybasis_params, fitting_basis)

params['dvdt'].vary = False
params['curv'].vary = False

priors = [
    radvel.prior.EccentricityPrior(nplanets),
    radvel.prior.PositiveKPrior(nplanets),
    radvel.prior.Gaussian('per1', 3.092920,0.000011),
    radvel.prior.Gaussian('tc1', 2458765.95501, 0.00047),
    radvel.prior.Gaussian('per2',6.765149, 0.000036),
    radvel.prior.Gaussian('tc2',2458766.16927, 0.00069)
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

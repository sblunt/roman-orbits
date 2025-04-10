#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-04-08 15:12
Author: calebharada

192310_radvel.py

    Description: RadVel setup file for HD 192310
"""

import pandas as pd
import numpy as np
import radvel

DATA_PATH = '../data/192310_rv_main_binned.txt'


# Define planetary system parameters
starname = 'HD 192310'
nplanets = 2
planet_letters = {1:'b', 2:'c'}

# Load RV data
data = pd.read_csv(DATA_PATH, header=None, skiprows=1, delim_whitespace=True,
                   names=('time','mnvel','errvel','tel'))

# Define dataset parameters
instnames = list(np.unique(data['tel']))
ntels = len(instnames)

# define radvel parameters
fitting_basis = 'per tc secosw sesinw k'
bjd0 = 2440000.

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define prior centers (initial guesses) 

# initialize Parameters object
anybasis_params = radvel.Parameters(nplanets,basis='per tp e w k')    

# planet 1
anybasis_params['per1'] = radvel.Parameter(value=74.39)  # period 
anybasis_params['tp1'] = radvel.Parameter(value=2455164.3)  # time of peri
anybasis_params['e1'] = radvel.Parameter(value=0.30)  # eccentricity 
anybasis_params['w1'] = radvel.Parameter(value=0.26)  # arg of peri 
anybasis_params['k1'] = radvel.Parameter(value=4.07)  # RV semi-amp

# planet 2
anybasis_params['per2'] = radvel.Parameter(value=525.8)  # period 
anybasis_params['tp2'] = radvel.Parameter(value=2440000)  # time of peri
anybasis_params['e2'] = radvel.Parameter(value=0.32)  # eccentricity 
anybasis_params['w2'] = radvel.Parameter(value=1.9)  # arg of peri 
anybasis_params['k2'] = radvel.Parameter(value=2.27)  # RV semi-amp

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# slope and curvature
anybasis_params['dvdt'] = radvel.Parameter(value=0.0)
anybasis_params['curv'] = radvel.Parameter(value=0.0)

# velocity zero-point and jitter
for tel in instnames:
    anybasis_params['jit_' + tel] = radvel.Parameter(value=10.0)  # jitter
    anybasis_params['gamma_' + tel] = radvel.Parameter(
        value=data.loc[data['tel']==tel, 'mnvel'].mean()
        )   # velocity zero-point
    
# Convert input orbital parameters into the fitting basis
params = anybasis_params.basis.to_any_basis(anybasis_params,fitting_basis)

# Set the 'vary' attributes of each of the parameters in the fitting basis. 
# A parameter's 'vary' attribute should be set to False if you wish to hold it
# fixed during the fitting process. By default, all 'vary' parameters
# are set to True.
#params['secosw1'].vary = False
#params['sesinw1'].vary = False
#params['tc1'].vary = False
#params['per1'].vary = False
#params['k1'].vary = False
#params['secosw2'].vary = False
#params['sesinw2'].vary = False
#params['tc2'].vary = False
#params['per2'].vary = False
#params['k2'].vary = False
#params['secosw3'].vary = False
#params['sesinw3'].vary = False
#params['tc3'].vary = False
#params['per3'].vary = False
#params['k3'].vary = False
params['dvdt'].vary = False
params['curv'].vary = False

# Define prior shapes and widths here.
priors = [
    radvel.prior.EccentricityPrior(nplanets),    # Keeps eccentricity < 1
    radvel.prior.PositiveKPrior(nplanets),       # Keeps K > 0
]
for tel in instnames:
    priors.append(radvel.prior.HardBounds('jit_' + tel, 0.0, 30.0))

# abscissa for slope and curvature terms 
# (should be near mid-point of time baseline)
time_base = np.mean([np.min(data.time), np.max(data.time)])  

# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=0.85, mstar_err= 0.02)   # from Howard et al. 2011


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-04-07 15:11
Author: calebharada

10700_radvel.py

    Description: RadVel setup file for HD 10700 (tau Cet)
"""

import pandas as pd
import numpy as np
import radvel

DATA_PATH = '../data/10700_rv_main_binned.txt'


# Define planetary system parameters
starname = 'tau Cet (HD 10700)'
nplanets = 4
planet_letters = {1:'e', 2:'f', 3:'g', 4:'h'}

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
anybasis_params['per1'] = radvel.Parameter(value=162.87)  # period 
anybasis_params['tp1'] = radvel.Parameter(value=2450000)  # time of peri
anybasis_params['e1'] = radvel.Parameter(value=0.18)  # eccentricity 
anybasis_params['w1'] = radvel.Parameter(value=0.39)  # arg of peri 
anybasis_params['k1'] = radvel.Parameter(value=0.55)  # RV semi-amp

# planet 2
anybasis_params['per2'] = radvel.Parameter(value=636.13)  # period 
anybasis_params['tp2'] = radvel.Parameter(value=2450000)  # time of peri
anybasis_params['e2'] = radvel.Parameter(value=0.16)  # eccentricity 
anybasis_params['w2'] = radvel.Parameter(value=2.09)  # arg of peri 
anybasis_params['k2'] = radvel.Parameter(value=0.35)  # RV semi-amp

# planet 3
anybasis_params['per3'] = radvel.Parameter(value=20.00)  # period 
anybasis_params['tp3'] = radvel.Parameter(value=2450000)  # time of peri
anybasis_params['e3'] = radvel.Parameter(value=0.06)  # eccentricity 
anybasis_params['w3'] = radvel.Parameter(value=6.90)  # arg of peri 
anybasis_params['k3'] = radvel.Parameter(value=0.49)  # RV semi-amp

# planet 4
anybasis_params['per4'] = radvel.Parameter(value=49.41)  # period 
anybasis_params['tp4'] = radvel.Parameter(value=2450000)  # time of peri
anybasis_params['e4'] = radvel.Parameter(value=0.23)  # eccentricity 
anybasis_params['w4'] = radvel.Parameter(value=0.13)  # arg of peri 
anybasis_params['k4'] = radvel.Parameter(value=0.39)  # RV semi-amp

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
    priors.append(radvel.prior.HardBounds('jit_' + tel, 0.0, 20.0))

# abscissa for slope and curvature terms 
# (should be near mid-point of time baseline)
time_base = np.mean([np.min(data.time), np.max(data.time)])  

# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=0.783, mstar_err= 0.012)   # from Feng et al. 2017


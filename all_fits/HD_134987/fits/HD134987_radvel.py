#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 15:12:56 2024

@author: zhexingli
"""

# Setup file for HD 134987 Radvel fitting

# Required packages for setup
import pandas as pd
import numpy as np
import radvel

# Define global planetary system and dataset parameters
starname = 'HD134987'
nplanets = 2    # number of planets in the system
instnames = ['UCLES','HIRES-pre','HIRES-post','HARPS-pre','HARPS-post']    # UCLES data from another source
ntels = len(instnames)       # number of instruments with unique velocity zero-points
fitting_basis = 'per tc secosw sesinw k'    # Fitting basis, see radvel.basis.BASIS_NAMES for available basis names
bjd0 = 2450000.
planet_letters = {1:'b',2:'c'}

# Define prior centers (initial guesses) in a basis of your choice (need not be in the fitting basis)
anybasis_params = radvel.Parameters(nplanets,basis='per tp e w k')    # initialize Parameters object

anybasis_params['per1'] = radvel.Parameter(value=258.249)    # 1st planet
anybasis_params['tp1'] = radvel.Parameter(value=2459110.9)    
anybasis_params['e1'] = radvel.Parameter(value=0.2318)
anybasis_params['w1'] = radvel.Parameter(value=6.198)      
anybasis_params['k1'] = radvel.Parameter(value=50.05)         
anybasis_params['per2'] = radvel.Parameter(value=6294)    # 2nd planet
anybasis_params['tp2'] = radvel.Parameter(value=2458492)    
anybasis_params['e2'] = radvel.Parameter(value=0.106)          
anybasis_params['w2'] = radvel.Parameter(value=5.093)      
anybasis_params['k2'] = radvel.Parameter(value=11.01)         

anybasis_params['dvdt'] = radvel.Parameter(value=0.0)        # slope
anybasis_params['curv'] = radvel.Parameter(value=0.0)         # curvature

anybasis_params['gamma_UCLES'] = radvel.Parameter(-20.63)      # velocity zero-point 
anybasis_params['gamma_HIRES-pre'] = radvel.Parameter(-0.59)
anybasis_params['gamma_HIRES-post'] = radvel.Parameter(-1.3)
anybasis_params['gamma_HARPS-pre'] = radvel.Parameter(-28.23)
anybasis_params['gamma_HARPS-post'] = radvel.Parameter(-11.8)

anybasis_params['jit_UCLES'] = radvel.Parameter(value=2.18)        # stellar jitter
anybasis_params['jit_HIRES-pre'] = radvel.Parameter(value=3.62)
anybasis_params['jit_HIRES-post'] = radvel.Parameter(value=2.31)
anybasis_params['jit_HARPS-pre'] = radvel.Parameter(value=1.75)
anybasis_params['jit_HARPS-post'] = radvel.Parameter(value=1.7)

# Convert input orbital parameters into the fitting basis
params = anybasis_params.basis.to_any_basis(anybasis_params,fitting_basis)

# Set the 'vary' attributes of each of the parameters in the fitting basis. A parameter's 'vary' attribute should
# be set to False if you wish to hold it fixed during the fitting process. By default, all 'vary' parameters
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
params['dvdt'].vary = False
params['curv'].vary = False

# Load radial velocity data, in this example the data is contained in an hdf file,
# the resulting dataframe or must have 'time', 'mnvel', 'errvel', and 'tel' keys
# the velocities are expected to be in m/s
path = '/roman_orbits/all_fits/HD_134987/data/HD134987_rv_master_binned.txt'
data = pd.read_csv(path,header=None,skiprows=1,delim_whitespace=True,names=('time','mnvel','errvel','tel'))

# Define prior shapes and widths here.
priors = [
    radvel.prior.EccentricityPrior(nplanets),           # Keeps eccentricity < 1
    radvel.prior.PositiveKPrior(nplanets),             # Keeps K > 0
    #radvel.prior.Gaussian('per1', params['per1'].value, 5.0), # Gaussian prior on tp1 with center at tc1 and width 0.01 days
    #radvel.prior.Gaussian('per2', params['per2'].value, 0.005),
    #radvel.prior.Gaussian('tc1', params['tc1'].value, 20.0),
    #radvel.prior.Gaussian('tc2', params['tc2'].value, 3.0),
    #radvel.prior.Gaussian('k1', params['k1'].value, 1.0),
    #radvel.prior.Gaussian('k2', params['k2'].value, 0.5),
    radvel.prior.HardBounds('jit_UCLES', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HIRES-pre', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HIRES-post', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HARPS-pre', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HARPS-post', 0.0, 10.0)
]

# abscissa for slope and curvature terms (should be near mid-point of time baseline)
time_base = np.mean([np.min(data.time), np.max(data.time)])  


# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=1.093, mstar_err= 0.047)   # stellar parameters from Rosenthal et al. 2021



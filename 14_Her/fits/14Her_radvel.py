#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 17:10:09 2024

@author: zhexingli
"""

# Setup file for 14 Her Radvel fitting

# Required packages for setup
import pandas as pd
import numpy as np
import radvel

# Define global planetary system and dataset parameters
starname = '14Her'
nplanets = 2    # number of planets in the system
instnames = ['ELODIE','HJS','HIRES-pre','HIRES-post','APF']
ntels = len(instnames)       # number of instruments with unique velocity zero-points
fitting_basis = 'per tc secosw sesinw k'    # Fitting basis, see radvel.basis.BASIS_NAMES for available basis names
bjd0 = 2450000.
planet_letters = {1:'b',2:'c'}

# Define prior centers (initial guesses) in a basis of your choice (need not be in the fitting basis)
anybasis_params = radvel.Parameters(nplanets,basis='per tc e w k')    # initialize Parameters object

anybasis_params['per1'] = radvel.Parameter(value=1766.75)    # period of b planet
anybasis_params['tc1'] = radvel.Parameter(value=2456836.1)    # time of periastron of 1st planet
anybasis_params['e1'] = radvel.Parameter(value=0.3651)          # eccentricity of 'per tp secosw sesinw k'1st planet
anybasis_params['w1'] = radvel.Parameter(value=0.3956)      # argument of periastron of the star's orbit for 1st planet
anybasis_params['k1'] = radvel.Parameter(value=89.44)         # velocity semi-amplitude for 1st planet
anybasis_params['per2'] = radvel.Parameter(value=19328)    # period of c planet
anybasis_params['tc2'] = radvel.Parameter(value=2454799)
anybasis_params['e2'] = radvel.Parameter(value=0.362)
anybasis_params['w2'] = radvel.Parameter(value=6.00)
anybasis_params['k2'] = radvel.Parameter(value=43.3)

anybasis_params['dvdt'] = radvel.Parameter(value=0.0)        # slope
anybasis_params['curv'] = radvel.Parameter(value=0.0)         # curvature

anybasis_params['gamma_ELODIE'] = radvel.Parameter(-13874.9)      # velocity zero-point     
anybasis_params['gamma_HJS'] = radvel.Parameter(-29.9)   
anybasis_params['gamma_HIRES-pre'] = radvel.Parameter(5.2)      
anybasis_params['gamma_HIRES-post'] = radvel.Parameter(-3.1)      
anybasis_params['gamma_APF'] = radvel.Parameter(45.8)

anybasis_params['jit_ELODIE'] = radvel.Parameter(value=5.0)        # jitter        
anybasis_params['jit_HJS'] = radvel.Parameter(value=0.1)
anybasis_params['jit_HIRES-pre'] = radvel.Parameter(value=3.0)        
anybasis_params['jit_HIRES-post'] = radvel.Parameter(value=3.0)        
anybasis_params['jit_APF'] = radvel.Parameter(value=3.0)


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
path = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/09-14Her/14Her_rv_master_binned.txt'
data = pd.read_csv(path,header=None,skiprows=1,delim_whitespace=True,names=('time','mnvel','errvel','tel'))

# Define prior shapes and widths here.
priors = [
    radvel.prior.EccentricityPrior(nplanets),           # Keeps eccentricity < 1
    radvel.prior.PositiveKPrior(nplanets),             # Keeps K > 0
    #radvel.prior.HardBounds('jit_ELODIE', 0.0, 10.0),
    #radvel.prior.HardBounds('jit_HJS', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HIRES-pre', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HIRES-post', 0.0, 10.0),
    radvel.prior.HardBounds('jit_APF', 0.0, 10.0)
]

# abscissa for slope and curvature terms (should be near mid-point of time baseline)
time_base = np.mean([np.min(data.time), np.max(data.time)])  


# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=0.969, mstar_err= 0.042)    # numbers from Rosenthal et al. 2021



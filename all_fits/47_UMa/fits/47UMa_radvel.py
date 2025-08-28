#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:17:52 2024

@author: zhexingli
"""

# Setup file for 47 UMa Radvel fitting

# Required packages for setup
import pandas as pd
import numpy as np
import radvel

# Define global planetary system and dataset parameters
starname = '47UMa'
nplanets = 3    # number of planets in the system
instnames = ['ELODIE','HJS','HRS','Hamilton','HIRES-post','APF']
ntels = len(instnames)       # number of instruments with unique velocity zero-points
fitting_basis = 'per tc secosw sesinw k'    # Fitting basis, see radvel.basis.BASIS_NAMES for available basis names
bjd0 = 2440000.
planet_letters = {1:'b',2:'c',3:'d'}

# Define prior centers (initial guesses) in a basis of your choice (need not be in the fitting basis)
anybasis_params = radvel.Parameters(nplanets,basis='per tp e w k')    # initialize Parameters object

anybasis_params['per1'] = radvel.Parameter(value=1075.71)    # period of 1st planet
anybasis_params['tp1'] = radvel.Parameter(value=2458378)    # time of periastron of 1st planet
anybasis_params['e1'] = radvel.Parameter(value=0.0305)          # eccentricity of 'per tp secosw sesinw k'1st planet
anybasis_params['w1'] = radvel.Parameter(value=5.853)      # argument of periastron of the star's orbit for 1st planet
anybasis_params['k1'] = radvel.Parameter(value=47.28)         # velocity semi-amplitude for 1st planet
anybasis_params['per2'] = radvel.Parameter(value=2290.3)    # period of 2nd planet
anybasis_params['tp2'] = radvel.Parameter(value=2457882)    # time of periastron of 2nd planet
anybasis_params['e2'] = radvel.Parameter(value=0.26)          # eccentricity of 'per tp secosw sesinw k' 2nd planet
anybasis_params['w2'] = radvel.Parameter(value=1.47)      # argument of periastron of the star's orbit for 2nd planet
anybasis_params['k2'] = radvel.Parameter(value=7.63)         # velocity semi-amplitude for 2nd planet
anybasis_params['per3'] = radvel.Parameter(value=16218)    # period of 3rd planet
anybasis_params['tp3'] = radvel.Parameter(value=2451347)    # time of periastron of 3rd planet
anybasis_params['e3'] = radvel.Parameter(value=0.371)          # eccentricity of 'per tp secosw sesinw k' 3rd planet
anybasis_params['w3'] = radvel.Parameter(value=1.12)      # argument of periastron of the star's orbit for 3rd planet
anybasis_params['k3'] = radvel.Parameter(value=11.87)         # velocity semi-amplitude for 3rd planet

anybasis_params['dvdt'] = radvel.Parameter(value=0.0)        # slope
anybasis_params['curv'] = radvel.Parameter(value=0.0)         # curvature

anybasis_params['gamma_ELODIE'] = radvel.Parameter(11212.7)      # velocity zero-point
anybasis_params['gamma_HJS'] = radvel.Parameter(11.7)      
anybasis_params['gamma_HRS'] = radvel.Parameter(26.9)   
anybasis_params['gamma_Hamilton'] = radvel.Parameter(-2.12)      
anybasis_params['gamma_HIRES-post'] = radvel.Parameter(7.8)      
anybasis_params['gamma_APF'] = radvel.Parameter(25.1)   

anybasis_params['jit_ELODIE'] = radvel.Parameter(value=5.0)        # jitter
anybasis_params['jit_HJS'] = radvel.Parameter(value=5.0)        
anybasis_params['jit_HRS'] = radvel.Parameter(value=5.0)
anybasis_params['jit_Hamilton'] = radvel.Parameter(value=5.0)        
anybasis_params['jit_HIRES-post'] = radvel.Parameter(value=5.0)        
anybasis_params['jit_APF'] = radvel.Parameter(value=5.0)


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
#params['secosw3'].vary = False
#params['sesinw3'].vary = False
#params['tc3'].vary = False
#params['per3'].vary = False
#params['k3'].vary = False
params['dvdt'].vary = False
params['curv'].vary = False

# Load radial velocity data, in this example the data is contained in an hdf file,
# the resulting dataframe or must have 'time', 'mnvel', 'errvel', and 'tel' keys
# the velocities are expected to be in m/s
path = '/roman_orbits/all_fits/47_UMa/data/47UMa_rv_master_binned.txt'

data = pd.read_csv(path,header=None,skiprows=1,delim_whitespace=True,names=('time','mnvel','errvel','tel'))


# Define prior shapes and widths here.
priors = [
    radvel.prior.EccentricityPrior(nplanets),           # Keeps eccentricity < 1
    radvel.prior.PositiveKPrior(nplanets),             # Keeps K > 0
    radvel.prior.HardBounds('jit_ELODIE', 0.0, 200.0),
    radvel.prior.HardBounds('jit_HJS', 0.0, 200.0),
    radvel.prior.HardBounds('jit_HRS', 0.0, 200.0),
    radvel.prior.HardBounds('jit_Hamilton', 0.0, 200.0),
    radvel.prior.HardBounds('jit_HIRES-post', 0.0, 200.0),
    radvel.prior.HardBounds('jit_APF', 0.0, 200.0)
]

# abscissa for slope and curvature terms (should be near mid-point of time baseline)
time_base = np.mean([np.min(data.time), np.max(data.time)])  


# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=1.005, mstar_err= 0.047)   # stellar parameters from Rosenthal et al. 2021



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 17:22:46 2024

@author: zhexingli
"""

# Setup file for GJ 849 Radvel fitting

# Required packages for setup
import pandas as pd
import numpy as np
import radvel

# Define global planetary system and dataset parameters
starname = 'GJ849'
nplanets = 2    # number of planets in the system
instnames = ['HARPS-pre','HARPS-post','HARPS-N','HIRES-pre','HIRES-post','CARMENES']
ntels = len(instnames)       # number of instruments with unique velocity zero-points
fitting_basis = 'per tc secosw sesinw k'    # Fitting basis, see radvel.basis.BASIS_NAMES for available basis names
bjd0 = 2450000.
planet_letters = {1:'b',2:'c'}

# Define prior centers (initial guesses) in a basis of your choice (need not be in the fitting basis)
anybasis_params = radvel.Parameters(nplanets,basis='per tp e w k')    # initialize Parameters object

anybasis_params['per1'] = radvel.Parameter(value=1917.2)    # period of 1st planet
anybasis_params['tp1'] = radvel.Parameter(value=2455848)    # time of periastron of 1st planet
anybasis_params['e1'] = radvel.Parameter(value=0.028)          # eccentricity of 'per tp secosw sesinw k'1st planet
anybasis_params['w1'] = radvel.Parameter(value=1.71)      # argument of periastron of the star's orbit for 1st planet
anybasis_params['k1'] = radvel.Parameter(value=24.92)         # velocity semi-amplitude for 1st planet
anybasis_params['per2'] = radvel.Parameter(value=5768)    # period of 2nd planet
anybasis_params['tp2'] = radvel.Parameter(value=2460488)    # time of periastron of 2nd planet
anybasis_params['e2'] = radvel.Parameter(value=0.054)          # eccentricity of 'per tp secosw sesinw k' 2nd planet
anybasis_params['w2'] = radvel.Parameter(value=3.653)      # argument of periastron of the star's orbit for 2nd planet
anybasis_params['k2'] = radvel.Parameter(value=18.04)         # velocity semi-amplitude for 2nd planet

anybasis_params['dvdt'] = radvel.Parameter(value=0.0)        # slope
anybasis_params['curv'] = radvel.Parameter(value=0.0)         # curvature

anybasis_params['gamma_HARPS-pre'] = radvel.Parameter(22.06)      # velocity zero-point
anybasis_params['gamma_HARPS-post'] = radvel.Parameter(10.0)      
anybasis_params['gamma_HARPS-N'] = radvel.Parameter(-6.5)   
anybasis_params['gamma_HIRES-pre'] = radvel.Parameter(10.0)      
anybasis_params['gamma_HIRES-post'] = radvel.Parameter(5.21)      
anybasis_params['gamma_CARMENES'] = radvel.Parameter(-3.1)

anybasis_params['jit_HARPS-pre'] = radvel.Parameter(value=1.93)        # jitter
anybasis_params['jit_HARPS-post'] = radvel.Parameter(value=4.03)        
anybasis_params['jit_HARPS-N'] = radvel.Parameter(value=3.39)
anybasis_params['jit_HIRES-pre'] = radvel.Parameter(value=3.0)        
anybasis_params['jit_HIRES-post'] = radvel.Parameter(value=4.36)        
anybasis_params['jit_CARMENES'] = radvel.Parameter(value=2.4)


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
path1 = 'path/GJ849_HARPSpre_bin.txt'
path2 = 'path/GJ849_HARPSpost_bin.txt'
path3 = 'path/GJ849_HARPSN_bin.txt'
path4 = 'path/GJ849_HIRESpre_bin.txt'
path5 = 'path/GJ849_HIRESpost_bin.txt'
path6 = 'path/GJ849_CARMENES_bin.txt'

data1 = pd.read_csv(path1,header=None,skiprows=1,delim_whitespace=True,names=('time','mnvel','errvel','tel'))
data2 = pd.read_csv(path2,header=None,skiprows=1,delim_whitespace=True,names=('time','mnvel','errvel','tel'))
data3 = pd.read_csv(path3,header=None,skiprows=1,delim_whitespace=True,names=('time','mnvel','errvel','tel'))
data4 = pd.read_csv(path4,header=None,skiprows=1,delim_whitespace=True,names=('time','mnvel','errvel','tel'))
data5 = pd.read_csv(path5,header=None,skiprows=1,delim_whitespace=True,names=('time','mnvel','errvel','tel'))
data6 = pd.read_csv(path6,header=None,skiprows=1,delim_whitespace=True,names=('time','mnvel','errvel','tel'))

dataframe = [data1,data2,data3,data4,data5,data6]
data = pd.concat(dataframe,ignore_index=True)


# Define prior shapes and widths here.
priors = [
    radvel.prior.EccentricityPrior(nplanets),           # Keeps eccentricity < 1
    radvel.prior.PositiveKPrior(nplanets),             # Keeps K > 0
    radvel.prior.HardBounds('jit_HARPS-pre', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HARPS-post', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HARPS-N', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HIRES-pre', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HIRES-post', 0.0, 10.0),
    radvel.prior.HardBounds('jit_CARMENES', 0.0, 10.0)
]

# abscissa for slope and curvature terms (should be near mid-point of time baseline)
time_base = np.mean([np.min(data.time), np.max(data.time)])  


# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=0.496, mstar_err= 0.009)    # numbers from Rosenthal et al. 2021


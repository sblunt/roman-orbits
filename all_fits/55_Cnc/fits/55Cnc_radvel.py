#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 18:53:34 2024

@author: zhexingli
"""

# Setup file for 55 Cnc Radvel fitting

# Required packages for setup
import pandas as pd
import numpy as np
import radvel

# Define global planetary system and dataset parameters
starname = '55Cnc'
nplanets = 5   # number of planets in the system
instnames = ['HJS','HRS','ELODIE','Hamilton','HIRES-pre','HIRES-post','APF',\
             'HARPS','HARPS-N','SOPHIE']
#instnames = ['HJS','HRS','ELODIE','Hamilton','HIRES-pre','HIRES-post','APF','HARPS-N','SOPHIE']
ntels = len(instnames)       # number of instruments with unique velocity zero-points
fitting_basis = 'per tc secosw sesinw k'    # Fitting basis, see radvel.basis.BASIS_NAMES for available basis names
bjd0 = 2450000.
planet_letters = {1:'b',2:'c',3:'d',4:'e',5:'f'}

# Define prior centers (initial guesses) in a basis of your choice (need not be in the fitting basis)
anybasis_params = radvel.Parameters(nplanets,basis='per tc e w k')    # initialize Parameters object

anybasis_params['per1'] = radvel.Parameter(value=14.651622)    # period of b planet
anybasis_params['tc1'] = radvel.Parameter(value=2458909.441)    # time of periastron of 1st planet
anybasis_params['e1'] = radvel.Parameter(value=0.0046)          # eccentricity of 'per tp secosw sesinw k'1st planet
anybasis_params['w1'] = radvel.Parameter(value=2.4)      # argument of periastron of the star's orbit for 1st planet
anybasis_params['k1'] = radvel.Parameter(value=71.31)         # velocity semi-amplitude for 1st planet
anybasis_params['per2'] = radvel.Parameter(value=44.3939)    # c planet
anybasis_params['tc2'] = radvel.Parameter(value=2458910.52)    
anybasis_params['e2'] = radvel.Parameter(value=0.008)         
anybasis_params['w2'] = radvel.Parameter(value=5.083)     
anybasis_params['k2'] = radvel.Parameter(value=9.68)        
anybasis_params['per3'] = radvel.Parameter(value=5046)   # d planet
anybasis_params['tc3'] = radvel.Parameter(value=2456235)   
anybasis_params['e3'] = radvel.Parameter(value=0.09)          
anybasis_params['w3'] = radvel.Parameter(value=4.872)     
anybasis_params['k3'] = radvel.Parameter(value=43.24)
anybasis_params['per4'] = radvel.Parameter(value=0.736546)   # e planet
anybasis_params['tc4'] = radvel.Parameter(value=2458916.353)   
anybasis_params['e4'] = radvel.Parameter(value=0.033)          
anybasis_params['w4'] = radvel.Parameter(value=0.8)     
anybasis_params['k4'] = radvel.Parameter(value=6.62)
anybasis_params['per5'] = radvel.Parameter(value=261.06)   # f planet
anybasis_params['tc5'] = radvel.Parameter(value=2458891)   
anybasis_params['e5'] = radvel.Parameter(value=0.086)          
anybasis_params['w5'] = radvel.Parameter(value=3.683)     
anybasis_params['k5'] = radvel.Parameter(value=5.14)

anybasis_params['dvdt'] = radvel.Parameter(value=0.0)        # slope
anybasis_params['curv'] = radvel.Parameter(value=0.0)         # curvature

anybasis_params['gamma_HJS'] = radvel.Parameter(-22574.2)      # velocity zero-point
anybasis_params['gamma_HRS'] = radvel.Parameter(28396)   
anybasis_params['gamma_ELODIE'] = radvel.Parameter(27267.3)
anybasis_params['gamma_Hamilton'] = radvel.Parameter(-3.08)      
anybasis_params['gamma_HIRES-pre'] = radvel.Parameter(-31.15)   
anybasis_params['gamma_HIRES-post'] = radvel.Parameter(-24.07)   
anybasis_params['gamma_APF'] = radvel.Parameter(21.88)
anybasis_params['gamma_HARPS'] = radvel.Parameter(27454.)
anybasis_params['gamma_HARPS-N'] = radvel.Parameter(27465.5)
anybasis_params['gamma_SOPHIE'] = radvel.Parameter(27435.1) 

anybasis_params['jit_HJS'] = radvel.Parameter(value=5.0)     # jitter   
anybasis_params['jit_HRS'] = radvel.Parameter(value=5.0)
anybasis_params['jit_ELODIE'] = radvel.Parameter(value=10.0)
anybasis_params['jit_Hamilton'] = radvel.Parameter(value=5.0)
anybasis_params['jit_HIRES-pre'] = radvel.Parameter(value=5.0)        
anybasis_params['jit_HIRES-post'] = radvel.Parameter(value=5.0)        
anybasis_params['jit_APF'] = radvel.Parameter(value=5.0)
anybasis_params['jit_HARPS'] = radvel.Parameter(value=5.0)
anybasis_params['jit_HARPS-N'] = radvel.Parameter(value=5.0)
anybasis_params['jit_SOPHIE'] = radvel.Parameter(value=5.0)


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
path = '/roman_orbits/all_fits/55_Cnc/data/55Cnc_rv_master_binned.txt'

data = pd.read_csv(path,header=None,skiprows=1,delim_whitespace=True,names=('time','mnvel','errvel','tel'))


# Define prior shapes and widths here.
priors = [
    radvel.prior.EccentricityPrior(nplanets),           # Keeps eccentricity < 1
    radvel.prior.PositiveKPrior(nplanets),             # Keeps K > 0
    #radvel.prior.Gaussian('per1', params['per1'].value, 0.000053),
    #radvel.prior.Gaussian('k1', params['k1'].value, 0.23),
    #radvel.prior.Gaussian('per2', params['per2'].value, 0.0038),
    #radvel.prior.Gaussian('k2', params['k2'].value, 0.25),
    #radvel.prior.Gaussian('per3', params['per3'].value, 77),
    #radvel.prior.Gaussian('k3', params['k3'].value, 2.7),
    #radvel.prior.Gaussian('per4', params['per4'].value, 0.0000015),
    #radvel.prior.Gaussian('k4', params['k4'].value, 0.24),
    #radvel.prior.Gaussian('per5', params['per5'].value, 0.24),
    #radvel.prior.Gaussian('k5', params['k5'].value, 0.27),
    radvel.prior.HardBounds('jit_HJS', 0.1, 100),
    radvel.prior.HardBounds('jit_HRS', 0.1, 100),
    #radvel.prior.HardBounds('jit_ELODIE', 0.1, 100),
    radvel.prior.HardBounds('jit_Hamilton', 0.1, 100),
    radvel.prior.HardBounds('jit_HIRES-pre', 0.1, 100),
    radvel.prior.HardBounds('jit_HIRES-post', 0.1, 100),
    radvel.prior.HardBounds('jit_APF', 0.1, 100),
    #radvel.prior.HardBounds('jit_HARPS', 0.1, 100)
    radvel.prior.HardBounds('jit_HARPS-N', 0.1, 100),
    radvel.prior.HardBounds('jit_SOPHIE', 0.1, 100),
    radvel.prior.HardBounds('jit_HARPS', 0.1, 100)
]

# abscissa for slope and curvature terms (should be near mid-point of time baseline)
time_base = np.mean([np.min(data.time), np.max(data.time)])  


# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=0.975, mstar_err= 0.045)   # stellar parameters from Rosenthal et al. 2021



"""
Created on April 8 2025

@author: stevengiacalone
"""

# Setup file for HD 217107 Radvel fitting

# Required packages for setup
import pandas as pd
import numpy as np
import radvel

# Define global planetary system and dataset parameters
starname = 'HD217107'
nplanets = 2   # number of planets in the system
instnames = ['Hamilton','HIRES-pre','HIRES-post','APF',\
             'HJS','CORALIE']
#instnames = ['HJS','HRS','ELODIE','Hamilton','HIRES-pre','HIRES-post','APF','HARPS-N','SOPHIE']
ntels = len(instnames)       # number of instruments with unique velocity zero-points
fitting_basis = 'per tc secosw sesinw k'    # Fitting basis, see radvel.basis.BASIS_NAMES for available basis names
bjd0 = 2450000.
planet_letters = {1:'b',2:'c'}

# Define prior centers (initial guesses) in a basis of your choice (need not be in the fitting basis)
anybasis_params = radvel.Parameters(nplanets,basis='per tc e w k')    # initialize Parameters object

anybasis_params['per1'] = radvel.Parameter(value=7.1268744)    # period of b planet
anybasis_params['tc1'] = radvel.Parameter(value=2456306.847)    # time of periastron of 1st planet
anybasis_params['e1'] = radvel.Parameter(value=0.1279)          # eccentricity of 'per tp secosw sesinw k'1st planet
anybasis_params['w1'] = radvel.Parameter(value=0.75)      # argument of periastron of the star's orbit for 1st planet
anybasis_params['k1'] = radvel.Parameter(value=141.91)         # velocity semi-amplitude for 1st planet
anybasis_params['per2'] = radvel.Parameter(value=5141)    # c planet
anybasis_params['tc2'] = radvel.Parameter(value=2460064)    
anybasis_params['e2'] = radvel.Parameter(value=0.3928)         
anybasis_params['w2'] = radvel.Parameter(value=0.85)     
anybasis_params['k2'] = radvel.Parameter(value=53.08)        

anybasis_params['dvdt'] = radvel.Parameter(value=0.0)        # slope
anybasis_params['curv'] = radvel.Parameter(value=0.0)         # curvature
   
anybasis_params['gamma_Hamilton'] = radvel.Parameter(0.075)     # velocity zero-point 
anybasis_params['gamma_HIRES-pre'] = radvel.Parameter(10.296)   
anybasis_params['gamma_HIRES-post'] = radvel.Parameter(-1.938)   
anybasis_params['gamma_APF'] = radvel.Parameter(-3.056)
anybasis_params['gamma_HJS'] = radvel.Parameter(0.004)   
anybasis_params['gamma_CORALIE'] = radvel.Parameter(-13410)

anybasis_params['jit_Hamilton'] = radvel.Parameter(value=5.0) # jitter   
anybasis_params['jit_HIRES-pre'] = radvel.Parameter(value=5.0)        
anybasis_params['jit_HIRES-post'] = radvel.Parameter(value=5.0)        
anybasis_params['jit_APF'] = radvel.Parameter(value=5.0)
anybasis_params['jit_HJS'] = radvel.Parameter(value=5.0)  
anybasis_params['jit_CORALIE'] = radvel.Parameter(value=5.0)


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
path = '../data/HD217107_rv_master_binned.txt'

data = pd.read_csv(path,header=None,skiprows=1,delim_whitespace=True,names=('time','mnvel','errvel','tel'))


# Define prior shapes and widths here.
priors = [
    radvel.prior.EccentricityPrior(nplanets),           # Keeps eccentricity < 1
    radvel.prior.PositiveKPrior(nplanets),             # Keeps K > 0
    #radvel.prior.Gaussian('per1', params['per1'].value, 0.000053),
    #radvel.prior.Gaussian('k1', params['k1'].value, 0.23),
    #radvel.prior.Gaussian('per2', params['per2'].value, 0.0038),
    #radvel.prior.Gaussian('k2', params['k2'].value, 0.25),
    radvel.prior.HardBounds('jit_Hamilton', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HIRES-pre', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HIRES-post', 0.0, 10.0),
    radvel.prior.HardBounds('jit_APF', 0.0, 10.0),
    radvel.prior.HardBounds('jit_HJS', 0.0, 10.0),
    radvel.prior.HardBounds('jit_CORALIE', 0.0, 10.0)
]

# abscissa for slope and curvature terms (should be near mid-point of time baseline)
time_base = np.mean([np.min(data.time), np.max(data.time)])  


# optional argument that can contain stellar mass in solar units (mstar) and
# uncertainty (mstar_err). If not set, mstar will be set to nan.
stellar = dict(mstar=1.0596, mstar_err=0.0447)   # stellar parameters from Rosenthal et al. 2021
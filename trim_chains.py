import pandas as pd

# load in radvel chains and trim off the first X percent
trim_percent = 0.1 # (as a fraction)

n_walkers = 50
n_ensembles = 8
thin = 10

chains_path = '/roman_orbits/all_fits/HD_190360/fits/results/HD190360_radvel_chains'

chains = pd.read_csv(f'{chains_path}.csv.bz2', compression='bz2')

n_params = chains.shape[1]

trimmed_chains = pd.DataFrame()

for par_name in chains.columns:
    param_vals = chains[par_name].values
    param_chains = param_vals.reshape((n_walkers, n_ensembles, -1))
    n_steps = param_chains.shape[-1]
    param_chains_trimmed = param_chains[:,:,int(trim_percent*n_steps):]
    trimmed_chains[par_name] = param_chains_trimmed.flatten()
trimmed_chains.to_csv(f'{chains_path}.csv.bz2', compression='bz2')
chains.to_csv(f'{chains_path}_untrimmed.csv.bz2', compression='bz2')
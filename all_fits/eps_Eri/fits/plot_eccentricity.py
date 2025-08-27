import pandas as pd
import matplotlib.pyplot as plt

chains_path = 'results/22049_radvel_chains'

chains = pd.read_csv(f'{chains_path}.csv.bz2', compression='bz2')

ecc = chains['secosw1']**2 + chains['sesinw1']**2

plt.figure()
plt.hist(ecc, bins=50)
plt.xlabel('ecc')
plt.ylabel('n samples')
plt.savefig('ecc.png',dpi=250)
Include "raw" data here-- i.e. files grabbed directly from papers, vizier, etc.
We should also include scripts here that read all of these files, concatenate them,
and make files that are readable by the orbit-fitting codes we want to use. The idea
is to reduce "hand-copying" of data (which tends to introduce mistakes) as much 
as possible.

### Data Sources:
1. ELODIE data, in the "ELODIE_rv_raw.txt" file, taken from Vizier (Naef et al. 2004) (https://ui.adsabs.harvard.edu/abs/2004A%26A...414..351N/abstract).
2. HJS data, in the "HJS_rv_raw.txt" file, taken from Vizier (Wittenmyer et al. 2007) (https://ui.adsabs.harvard.edu/abs/2007ApJ...654..625W/abstract).
3. Keck-HIRES data, including both pre- and post-upgrade data, in the "CLS_rv_raw.txt" file, taken from Table 6 of Rosenthal et al. 2021 (https://iopscience.iop.org/article/10.3847/1538-4365/abe23c/meta#apjsabe23ct6).
4. APF-Levy data, in the "CLS_rv_raw.txt" file, taken from Table 6 of Rosenthal et al. 2021 (https://iopscience.iop.org/article/10.3847/1538-4365/abe23c/meta#apjsabe23ct6).

Master data files generated by "14Her_DataSetup.py" are concatenated data including all sources, cleaned and formatted for radvel as input.

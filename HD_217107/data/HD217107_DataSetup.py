"""
Created on April 7 2025

@author: stevengiacalone
"""

import pandas as pd
import radvel

path1 = 'CLS_rv_raw.csv'
path2 = 'HJS_rv_raw.csv'
path3 = 'CORALIE_rv_raw.csv'

# set nightly binning option
binning = 1   # nightly bin, 1 for yes, 2 for no

# CLS data
data1 = pd.read_csv(path1, usecols=[3,4,5,8])

data1_ham = data1[data1['tel'] == 'lick']   # Hamilton data
data1_ham['tel'] = 'Hamilton'

data1_pre = data1[data1['tel'] == 'k']   # HIRES-pre data
data1_pre['tel'] = 'HIRES-pre'

data1_post = data1[data1['tel'] == 'j']   # HIRES-post data
data1_post['tel'] = 'HIRES-post'

data1_apf = data1[data1['tel'] == 'apf']   # APF data
data1_apf['tel'] = 'APF'

# HJS data
data2_hjs = pd.read_csv(path2, usecols=[3,4,5,2])

# CORALIE data
data3_cor = pd.read_csv(path3, usecols=[0,1,2])
data3_cor["mnvel"] *= 1e3
data3_cor["errvel"] *= 1e3
data3_cor['tel'] = "CORALIE"

# data concatenation and optionally do nightly bin of all data sources
dataframe = [data1_ham,data1_pre,data1_post,data1_apf,data2_hjs,data3_cor]
data_all = pd.concat(dataframe,ignore_index=True)
savepath='./'
data_all.to_csv(savepath+'HD217107_rv_master_unbinned.txt',sep='\t',index=False, header=True)

# nightly bin
if binning == 1:
    time, mnvel, errvel, tel = radvel.utils.bintels(data_all['time'].values,\
                               data_all['mnvel'].values,data_all['errvel'].values,\
                               data_all['tel'])
    bin_dict = {'time':time, 'mnvel':mnvel, 'errvel':errvel, 'tel':tel}

    data_all_bin = pd.DataFrame(data=bin_dict)
    data_all_bin.to_csv(savepath+'HD217107_rv_master_binned.txt',sep='\t',index=False, header=True)
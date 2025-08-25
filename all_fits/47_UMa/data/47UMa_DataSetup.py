#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 11:55:32 2024

@author: zhexingli
"""

# data setup file that concatenates all the rv data together into one master 
# data file, with binning option

# For 47 UMa

import pandas as pd
import radvel

path1 = 'ELODIE_rv_raw.txt'
path2 = 'HJS_rv_raw.txt'
path3 = 'HRS_rv_raw.txt'
path4 = 'CLS_rv_raw.txt'

# set nightly binning option
binning = 1   # nightly bin, 1 for yes, 2 for no

# ELODIE data
data1 = pd.read_csv(path1,header=None,skiprows=12,sep='\s+',\
                    usecols=[0,1,2],names=('time','mnvel','errvel'))
data1['mnvel'] *= 1000
data1['errvel'] *= 1000
data1['tel'] = 'ELODIE'

# HJS data
data2 = pd.read_csv(path2,header=None,skiprows=11,delim_whitespace=True,\
                    usecols=[2,3,4],names=('time','mnvel','errvel'))
data2['tel'] = 'HJS'

# HRS data
data3 = pd.read_csv(path3,header=None,skiprows=11,delim_whitespace=True,\
                    usecols=[2,3,4],names=('time','mnvel','errvel'))
data3['tel'] = 'HRS'

# CLS data, including Hamilton, APF, and HIRES-post
data4 = pd.read_csv(path4,header=None,skiprows=30,delim_whitespace=True,\
                    usecols=[2,4,5,6],names=('tel','time','mnvel','errvel'))
data4_ham = data4[data4['tel'] == 'lick']   # Lick Hamilton data
data4_ham['tel'] = 'Hamilton'
data4_apf = data4[data4['tel'] == 'apf']   # APF Levy data
data4_apf['tel'] = 'APF'
data4_hires = data4[data4['tel'] == 'j']   # Keck HIRES-post data
data4_hires['tel'] = 'HIRES-post'

# data concatenation and optionally do nightly bin of all data sources
dataframe = [data1,data2,data3,data4_ham,data4_apf,data4_hires]
data_all = pd.concat(dataframe,ignore_index=True)
data_all.to_csv('47UMa_rv_master_unbinned.txt',sep='\t',index=False, header=True)

# nightly bin
if binning == 1:
    time, mnvel, errvel, tel = radvel.utils.bintels(data_all['time'].values,\
                               data_all['mnvel'].values,data_all['errvel'].values,\
                               data_all['tel'])
    bin_dict = {'time':time, 'mnvel':mnvel, 'errvel':errvel, 'tel':tel}

    data_all_bin = pd.DataFrame(data=bin_dict)
    data_all_bin.to_csv('47UMa_rv_master_binned.txt',sep='\t',index=False, header=True)


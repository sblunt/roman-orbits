#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 15:05:56 2024

@author: zhexingli
"""

# data setup file that concatenates all the rv data together into one master 
# data file, with binning option

# For HD 134987

import pandas as pd
import radvel

path1 = 'path/UCLES_rv_raw.txt'
path2 = 'path/HIRES_rv_raw.txt'
path3 = 'path/HARPS_rv_raw.txt'
savepath = 'path/'

# set nightly binning option
binning = 1   # nightly bin, 1 for yes, 2 for no

# UCLES data
data1 = pd.read_csv(path1,header=None,skiprows=22,delim_whitespace=True,\
                    names=('time','mnvel','errvel'))
data1['tel'] = 'UCLES'

# HIRES data
data2 = pd.read_csv(path2,header=None,skiprows=30,delim_whitespace=True,\
                    usecols=[2,4,5,6],names=('tel','time','mnvel','errvel'))
data2_pre = data2[data2['tel'] == 'k']   # pre-upgrade data
data2_pre['tel'] = 'HIRES-pre'
data2_post = data2[data2['tel'] == 'j']   # post-upgrade data
data2_post['tel'] = 'HIRES-post'

# HARPS data
data3 = pd.read_csv(path3,header=None,skiprows=2,delim_whitespace=True,\
                    usecols=[3,4,5],names=('time','mnvel','errvel'))
data3_pre = data3[data3['time'] < 2457174.5]   # pre-upgrade data
data3_pre['tel'] = 'HARPS-pre'
data3_post = data3[data3['time'] > 2457174.5]   # post-upgrade data
data3_post['tel'] = 'HARPS-post'

# data concatenation and optionally do nightly bin of all data sources
dataframe = [data1,data2_pre,data2_post,data3_pre,data3_post]
data_all = pd.concat(dataframe,ignore_index=True)
data_all.to_csv(savepath+'HD134987_rv_master_unbinned.txt',sep='\t',index=False, header=True)

# nightly bin
if binning == 1:
    time, mnvel, errvel, tel = radvel.utils.bintels(data_all['time'].values,\
                               data_all['mnvel'].values,data_all['errvel'].values,\
                               data_all['tel'])
    bin_dict = {'time':time, 'mnvel':mnvel, 'errvel':errvel, 'tel':tel}

    data_all_bin = pd.DataFrame(data=bin_dict)
    data_all_bin.to_csv(savepath+'HD134987_rv_master_binned.txt',sep='\t',index=False, header=True)


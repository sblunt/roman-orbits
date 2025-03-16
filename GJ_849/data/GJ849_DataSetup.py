#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 12:12:20 2024

@author: zhexingli
"""

# data setup file that concatenates all the rv data together into one master 
# data file, with binning option

# For GJ 849

import pandas as pd
import radvel

path1 = 'path/HARPS_rv_raw.txt'
path2 = 'path/HARPS-N_rv_raw.txt'
path3 = 'path/HIRES_rv_raw.txt'
path4 = 'path/CARMENES_rv_raw.csv'
savepath = 'path/'

# set nightly binning option
binning = 1   # nightly bin, 1 for yes, 2 for no

# HARPS pre and post data
data1 = pd.read_csv(path1,header=None,skiprows=2,sep='\s+',\
                    usecols=[3,4,5],names=('time','mnvel','errvel'))
data1_pre = data1[data1['time'] < 2457174.5]   # pre-upgrade data
data1_pre['tel'] = 'HARPS-pre'
data1_post = data1[data1['time'] > 2457174.5]   # post-upgrade data
data1_post['tel'] = 'HARPS-post'

# HARPS-N data
data2 = pd.read_csv(path2,header=None,skiprows=30,delim_whitespace=True,\
                    usecols=[1,2,3],names=('time','mnvel','errvel'))
data2['time'] += 2400000
data2['tel'] = 'HARPS-N'

# HIRES data
data3 = pd.read_csv(path3,header=None,skiprows=30,delim_whitespace=True,\
                    usecols=[2,4,5,6],names=('tel','time','mnvel','errvel'))
data3_pre = data3[data3['tel'] == 'k']   # pre-upgrade data
data3_pre['tel'] = 'HIRES-pre'
data3_post = data3[data3['tel'] == 'j']   # post-upgrade data
data3_post['tel'] = 'HIRES-post'

# CARMENES data
data4 = pd.read_csv(path4,header=None,skiprows=1,delimiter=',',\
                    usecols=[0,3,4],names=('time','mnvel','errvel'))
data4['tel'] = 'CARMENES'
data4 = data4.dropna(axis=0, how='any').reset_index(drop=True)   # there's 1 row with nan value

# data concatenation and optionally do nightly bin of all data sources
dataframe = [data1_pre,data1_post,data2,data3_pre,data3_post,data4]
data_all = pd.concat(dataframe,ignore_index=True)
data_all.to_csv(savepath+'GJ849_rv_master_unbinned.txt',sep='\t',index=False, header=True)

# nightly bin
if binning == 1:
    time, mnvel, errvel, tel = radvel.utils.bintels(data_all['time'].values,\
                               data_all['mnvel'].values,data_all['errvel'].values,\
                               data_all['tel'])
    bin_dict = {'time':time, 'mnvel':mnvel, 'errvel':errvel, 'tel':tel}

    data_all_bin = pd.DataFrame(data=bin_dict)
    data_all_bin.to_csv(savepath+'GJ849_rv_master_binned.txt',sep='\t',index=False, header=True)






#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 17:00:24 2024

@author: zhexingli
"""

# data setup file that concatenates all the rv data together into one master 
# data file, with binning option

# For 14 Her

import pandas as pd
import radvel

path1 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/09-14Her/ELODIE_rv_raw.txt'
path2 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/09-14Her/HJS_rv_raw.txt'
path3 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/09-14Her/CLS_rv_raw.txt'
savepath = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/09-14Her/'

# set nightly binning option
binning = 1   # nightly bin, 1 for yes, 2 for no

# ELODIE data
data1 = pd.read_csv(path1,header=None,skiprows=27,delim_whitespace=True,\
                    usecols=[0,1,2],names=('time','mnvel','errvel'))
data1['mnvel'] *= 1000
data1['errvel'] *= 1000
data1['tel'] = 'ELODIE'

# HJS data
data2 = pd.read_csv(path2,header=None,skiprows=26,delim_whitespace=True,\
                    usecols=[2,3,4],names=('time','mnvel','errvel'))
data2['tel'] = 'HJS'

# CLS data
data3 = pd.read_csv(path3,header=None,skiprows=29,delim_whitespace=True,\
                    usecols=[2,4,5,6], names=('tel','time','mnvel','errvel'))

data3_pre = data3[data3['tel'] == 'k']   # HIRES-pre data
data3_pre['tel'] = 'HIRES-pre'

data3_post = data3[data3['tel'] == 'j']   # HIRES-post data
data3_post['tel'] = 'HIRES-post'

data3_apf = data3[data3['tel'] == 'apf']   # APF data
data3_apf['tel'] = 'APF'

# data concatenation and optionally do nightly bin of all data sources
dataframe = [data1,data2,data3_pre,data3_post,data3_apf]
data_all = pd.concat(dataframe,ignore_index=True)
data_all.to_csv(savepath+'14Her_rv_master_unbinned.txt',sep='\t',index=False, header=True)

# nightly bin
if binning == 1:
    time, mnvel, errvel, tel = radvel.utils.bintels(data_all['time'].values,\
                               data_all['mnvel'].values,data_all['errvel'].values,\
                               data_all['tel'])
    bin_dict = {'time':time, 'mnvel':mnvel, 'errvel':errvel, 'tel':tel}

    data_all_bin = pd.DataFrame(data=bin_dict)
    data_all_bin.to_csv(savepath+'14Her_rv_master_binned.txt',sep='\t',index=False, header=True)


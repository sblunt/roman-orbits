#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:42:04 2024

@author: zhexingli
"""

# data setup file that concatenates all the rv data together into one master 
# data file, with binning option

# For GJ 687

import pandas as pd
import radvel

path1 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/04-GJ687/HRS_rv_raw.txt'
path2 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/04-GJ687/HIRES_rv_raw.txt'
path3 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/04-GJ687/APF_rv_raw.txt'
path4 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/04-GJ687/CARMENES_rv_raw.csv'
savepath = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/04-GJ687/'

# set nightly binning option
binning = 1   # nightly bin, 1 for yes, 2 for no

# HRS data
data1 = pd.read_csv(path1,header=None,skiprows=1,delim_whitespace=True,\
                    names=('time','mnvel','errvel'))
data1['tel'] = 'HRS'

# HIRES data
data2 = pd.read_csv(path2,header=None,skiprows=29,delim_whitespace=True,\
                    usecols=[2,4,5,6],names=('tel','time','mnvel','errvel'))
data2_pre = data2[data2['tel'] == 'k']   # HIRES-pre data
data2_pre['tel'] = 'HIRES-pre'
data2_post = data2[data2['tel'] == 'j']   # HIRES-post data
data2_post['tel'] = 'HIRES-post'

# APF data
data3 = pd.read_csv(path3,header=None,skiprows=25,delim_whitespace=True,\
                    usecols=[1,2,3,4],names=('time','mnvel','errvel','tel'))

# CARMENES data
data4 = pd.read_csv(path4,header=None,skiprows=1,delimiter=',',\
                    usecols=[0,3,4],names=('time','mnvel','errvel'))
data4['tel'] = 'CARMENES'
data4 = data4.drop([3]).reset_index(drop=True)   # remove one outlier

# data concatenation and optionally do nightly bin of all data sources
dataframe = [data1,data2_pre,data2_post,data3,data4]
data_all = pd.concat(dataframe,ignore_index=True)
data_all.to_csv(savepath+'GJ687_rv_master_unbinned.txt',sep='\t',index=False, header=True)

# nightly bin
if binning == 1:
    time, mnvel, errvel, tel = radvel.utils.bintels(data_all['time'].values,\
                               data_all['mnvel'].values,data_all['errvel'].values,\
                               data_all['tel'])
    bin_dict = {'time':time, 'mnvel':mnvel, 'errvel':errvel, 'tel':tel}

    data_all_bin = pd.DataFrame(data=bin_dict)
    data_all_bin.to_csv(savepath+'GJ687_rv_master_binned.txt',sep='\t',index=False, header=True)



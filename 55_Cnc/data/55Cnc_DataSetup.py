#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 18:22:54 2024

@author: zhexingli
"""

# data setup file that concatenates all the rv data together into one master 
# data file, with binning option

# For 55 Cnc

import pandas as pd
import radvel

path1 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/05-55Cnc/McDonald_rv_raw.txt'
path2 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/05-55Cnc/ELODIE_rv_raw.txt'
path3 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/05-55Cnc/CLS_rv_raw.txt'
path4 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/05-55Cnc/HARPS_rv_raw.txt'
path5 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/05-55Cnc/HARPS-N_rv_raw.txt'
path6 = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/05-55Cnc/SOPHIE_rv_raw.txt'
savepath = '/Users/zhexingli/Desktop/UCR/01-RESEARCH/PROJECTS/WFIRST/Refinement/RealSims/05-55Cnc/'

# set nightly binning option
binning = 1   # nightly bin, 1 for yes, 2 for no

# McDonald data
data1 = pd.read_csv(path1,header=None,skiprows=25,delim_whitespace=True,\
                    names=('time','mnvel','errvel','tel'))
data1['time'] += 2400000

data1_hjs = data1[data1['tel'] == 'HJST/Tull']   # HJS data
data1_hjs['tel'] = 'HJS'

data1_hrs = data1[data1['tel'] == 'HET/HRS']   # HRS data
data1_hrs['tel'] = 'HRS'

# ELODIE data
data2 = pd.read_csv(path2,header=None,skiprows=21,delim_whitespace=True,\
                    names=('time','mnvel','errvel'))
data2['tel'] = 'ELODIE'

# CLS data
data3 = pd.read_csv(path3,header=None,skiprows=29,delim_whitespace=True,\
                    usecols=[2,4,5,6], names=('tel','time','mnvel','errvel'))
    
data3_ham = data3[data3['tel'] == 'lick']   # Hamilton data
data3_ham['tel'] = 'Hamilton'

data3_pre = data3[data3['tel'] == 'k']   # HIRES-pre data
data3_pre['tel'] = 'HIRES-pre'

data3_post = data3[data3['tel'] == 'j']   # HIRES-post data
data3_post['tel'] = 'HIRES-post'

data3_apf = data3[data3['tel'] == 'apf']   # APF data
data3_apf['tel'] = 'APF'

# HARPS data
data4 = pd.read_csv(path4,header=None,skiprows=26,delim_whitespace=True,\
                    usecols=[0,1,2], names=('time','mnvel','errvel'))
data4['time'] += 2400000
data4['tel'] = 'HARPS'

# HARPS-N data
data5 = pd.read_csv(path5,header=None,skiprows=26,delim_whitespace=True,\
                    usecols=[0,1,2], names=('time','mnvel','errvel'))
data5['time'] += 2400000
data5['tel'] = 'HARPS-N'

# SOPHIE data
data6 = pd.read_csv(path6,header=None,skiprows=26,delim_whitespace=True,\
                    usecols=[0,1,2], names=('time','mnvel','errvel'))
data6['time'] += 2400000
data6['tel'] = 'SOPHIE'

# data concatenation and optionally do nightly bin of all data sources
dataframe = [data1_hjs,data1_hrs,data2,data3_ham,data3_pre,data3_post,data3_apf,\
             data4,data5,data6]
data_all = pd.concat(dataframe,ignore_index=True)
data_all.to_csv(savepath+'55Cnc_rv_master_unbinned.txt',sep='\t',index=False, header=True)

# nightly bin
if binning == 1:
    time, mnvel, errvel, tel = radvel.utils.bintels(data_all['time'].values,\
                               data_all['mnvel'].values,data_all['errvel'].values,\
                               data_all['tel'])
    bin_dict = {'time':time, 'mnvel':mnvel, 'errvel':errvel, 'tel':tel}

    data_all_bin = pd.DataFrame(data=bin_dict)
    data_all_bin.to_csv(savepath+'55Cnc_rv_master_binned.txt',sep='\t',index=False, header=True)



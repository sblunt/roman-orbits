#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-04-09 16:02
Author: calebharada

39091_DataSetup.py

    Description: combines RV datasets for HD 39091 (pi Men)
"""

import radvel
import pandas as pd

SYSTEM_HD = 39091
STD_COL_NAMES = ['time', 'mnvel', 'errvel', 'tel']


def data_setup():
    """Main data setup function. 

    Calls other functions to read in RV data and combines each data set
    into a single table. Saves an unbinned and binned RV data file.
    """

    # create new DF and add each data source
    combined_data = pd.DataFrame(columns=STD_COL_NAMES)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # add HAPRS (ESO)
    combined_data = pd.concat([combined_data, 
        get_RVBank_HARPS(f'{SYSTEM_HD}_RVBank_HARPS.csv')],
        ignore_index=True )
    # add UCLES (AAT)
    combined_data = pd.concat([combined_data, 
        get_Laliotis23_UCLES(f'{SYSTEM_HD}_Laliotis23_UCLES.csv')],
        ignore_index=True )
    # add PFS (Magellan)
    combined_data = pd.concat([combined_data, 
        get_Laliotis23_PFS(f'{SYSTEM_HD}_Laliotis23_PFS-Post.csv')],
        ignore_index=True )
    # add ESPRESSO (VLT)
    combined_data = pd.concat([combined_data, 
        get_Damasso20_ESPRESSO(f'{SYSTEM_HD}_Damasso20_ESPRESSO.txt')],
        ignore_index=True )
    # add CORALIE (LET)
    combined_data = pd.concat([combined_data, 
        get_Damasso20_CORALIE(f'{SYSTEM_HD}_Damasso20_CORALIE.txt')],
        ignore_index=True )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # save compiled data file
    combined_data.to_csv(f'{SYSTEM_HD}_rv_main_unbinned.txt', sep='\t',
                         index=False, header=True)

    # nightly bin
    time, mnvel, errvel, tel = radvel.utils.bintels(
        combined_data['time'].values,
        combined_data['mnvel'].values,
        combined_data['errvel'].values,
        combined_data['tel'])
    bin_dict = {'time':time, 'mnvel':mnvel, 'errvel':errvel, 'tel':tel}

    # save binned data file
    data_all_bin = pd.DataFrame(data=bin_dict)
    data_all_bin.to_csv(f'{SYSTEM_HD}_rv_main_binned.txt', sep='\t',
                        index=False, header=True)

    return


def get_RVBank_HARPS(data_file):
    """Read in a data file from the HARPS RVBank

    Args:
        data_file (str): path to .csv file

    Returns:
        pd.DataFrame: RV dataframe
    """

    # load file
    raw = pd.read_csv(data_file, index_col=0)
    
    # new df
    new = pd.DataFrame()
    
    # separate pre-upgrade (Trifonov et al. 2020)
    harps_pre_msk = raw['BJD'] <= 2_457_163 
    harps_pre_data = raw.loc[harps_pre_msk, 
                            ['BJD', 'RV_mlc_nzp', 'e_RV_mlc_nzp']]
    harps_pre_data['tel'] = 'HARPS-pre'
    harps_pre_data = harps_pre_data.rename(
        columns={'BJD':'time', 'RV_mlc_nzp':'mnvel', 'e_RV_mlc_nzp':'errvel'})
    new = pd.concat([new, harps_pre_data])
    
    # separate post-upgrade (Trifonov et al. 2020)
    harps_post_msk = raw['BJD'] >= 2_457_173 
    harps_post_data = raw.loc[harps_post_msk, 
                            ['BJD', 'RV_mlc_nzp', 'e_RV_mlc_nzp']]
    harps_post_data['tel'] = 'HARPS-post'
    harps_post_data = harps_post_data.rename(
        columns={'BJD':'time', 'RV_mlc_nzp':'mnvel', 'e_RV_mlc_nzp':'errvel'})
    new = pd.concat([new, harps_post_data])

    # order columns
    new = new[STD_COL_NAMES]
    
    return new


def get_Laliotis23_UCLES(data_file):
    """Read in UCLES data file from the Laliotis et al (2023)

    Args:
        data_file (str): path to .csv file

    Returns:
        pd.DataFrame: RV dataframe
    """    
     # load file
    raw = pd.read_csv(data_file, usecols=[1,2,3],
                      skiprows=1, names=['time', 'mnvel', 'errvel'])
    
    # new df
    new = raw.copy()
    
    # add tel
    new['tel'] = 'UCLES'
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_Laliotis23_PFS(data_file):
    """Read in PFS data file from the Laliotis et al (2023)

    Args:
        data_file (str): path to .csv file

    Returns:
        pd.DataFrame: RV dataframe
    """    
     # load file
    raw = pd.read_csv(data_file, usecols=[1,2,3],
                      skiprows=1, names=['time', 'mnvel', 'errvel'])
    
    # new df
    new = raw.copy()
    
    # add tel
    new['tel'] = 'PFS-post'
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_Damasso20_ESPRESSO(data_file):
    """Read in ESPRESSO/VLT RV data file from Damasso et al. (2020)

    Args:
        data_file (str): path to .txt file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, delim_whitespace=True, skiprows=43,
                      names=['time', 'mnvel', 'errvel'], usecols=[0,1,2])
     
    # new df
    new = raw.copy()
    
    # get relevant columns
    new['tel'] = 'ESPRESSO'

    new['time'] += 2450000
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_Damasso20_CORALIE(data_file):
    """Read in CORALIE/LET RV data file from Damasso et al. (2020)

    Args:
        data_file (str): path to .txt file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, delim_whitespace=True, skiprows=38,
                      names=['time', 'mnvel', 'errvel', 'tel'], 
                      usecols=[0,1,2,3])
     
    # new df
    new = raw.copy()

    new['time'] += 2450000
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


########################################################################
########################################################################
# execute script

if __name__ == '__main__':
    data_setup()

########################################################################
########################################################################



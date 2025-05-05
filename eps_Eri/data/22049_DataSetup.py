#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-04-07 18:08
Author: calebharada

22049_DataSetup.py

    Description: combines RV datasets for HD 22049 (eps Eri)
"""

import radvel
import pandas as pd

SYSTEM_HD = 22049
STD_COL_NAMES = ['time', 'mnvel', 'errvel', 'tel']


def data_setup():
    """Main data setup function. 

    Calls other functions to read in RV data and combines each data set
    into a single table. Saves an unbinned and binned RV data file.
    """

    # create new DF and add each data source
    combined_data = pd.DataFrame(columns=STD_COL_NAMES)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # add HIRES (Keck)
    combined_data = pd.concat([combined_data, 
        get_EBPS_HIRES(f'{SYSTEM_HD}_EBPS_HIRES.vels')],
        ignore_index=True)
     # add HAPRS (ESO)
    combined_data = pd.concat([combined_data, 
        get_RVBank_HARPS(f'{SYSTEM_HD}_RVBank_HARPS.csv')],
        ignore_index=True )
    # add Levy (APF)
    combined_data = pd.concat([combined_data, 
        get_CLS21_APF(f'{SYSTEM_HD}_CLS21_APF.csv')],
        ignore_index=True )
    # add Hamilton (Lick)
    combined_data = pd.concat([combined_data, 
        get_CLS21_Hamilton(f'{SYSTEM_HD}_CLS21_Hamilton.csv')],
        ignore_index=True )
    # add Tull (McDonald)
    combined_data = pd.concat([combined_data, 
        get_Benedict06_Tull(f'{SYSTEM_HD}_Benedict06_Tull.rdb')],
        ignore_index=True )
    # add CES-LC (La Silla)
    combined_data = pd.concat([combined_data, 
        get_Zechmeister19_CES_LC(f'{SYSTEM_HD}_Zechmeister13_CES-LC.txt')],
        ignore_index=True )
    # add CES-VLC (La Silla)
    combined_data = pd.concat([combined_data, 
        get_Zechmeister19_CES_VLC(f'{SYSTEM_HD}_Zechmeister13_CES-VLC.txt')],
        ignore_index=True )
    # add EXPRES (LDT)
    combined_data = pd.concat([combined_data, 
        get_Roettenbacher22_EXPRES(f'{SYSTEM_HD}_Roettenbacher22_EXPRES.txt')],
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


def get_EBPS_HIRES(data_file):
    """Read in a .vels data file from the EBPS HIRES RV archive

    Args:
        data_file (str): path to .vels file

    Returns:
        pd.DataFrame: RV dataframe
    """

    # load file
    raw = pd.read_csv(data_file, sep='\s+', header=None, 
                      usecols=[0,1,2], names=['time', 'mnvel', 'errvel'])

    # new df
    new = pd.DataFrame()
    
    # separate PRE-upgrade (before Aug 18, 2004 = JD 2453236)
    hires_pre_msk = raw['time'] < 2_453_236
    hires_pre_data = raw.loc[
        hires_pre_msk, ['time', 'mnvel', 'errvel']]
    hires_pre_data['tel'] = 'HIRES-pre'
    new = pd.concat([new, hires_pre_data])
    
    # separate POST-upgrade (after Aug 18, 2004 = JD 2453236)
    hires_post_msk = raw['time'] >= 2_453_236
    hires_post_data = raw.loc[
        hires_post_msk, ['time', 'mnvel', 'errvel']]
    hires_post_data['tel'] = 'HIRES-post'
    new = pd.concat([new, hires_post_data])
    
    # order columns
    new = new[STD_COL_NAMES]

    return new


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


def get_CLS21_APF(data_file):
    """Read in an APF data file from CLS

    Args:
        data_file (str): path to .csv file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, header=0,
                      names=['time', 'mnvel', 'errvel'], usecols=[4,5,6])
    
    # new df
    new = raw.copy()
    
    # get relevant columns
    new['tel'] = 'Levy'
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_CLS21_Hamilton(data_file):
    """Read in an Hamilton/Lick data file from CLS

    Args:
        data_file (str): path to .csv file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, header=0,
                      names=['time', 'mnvel', 'errvel'], usecols=[4,5,6])
    
    # new df
    new = raw.copy()
    
    # get relevant columns
    new['tel'] = 'Hamilton'
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_Benedict06_Tull(data_file):
    """Read in Tull/McDonald RV data file from Benedict+06

    Args:
        data_file (str): path to .txt file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, delim_whitespace=True, skiprows=2,
                      names=['time', 'mnvel', 'errvel'], usecols=[0,1,2])
     
    # new df
    new = raw.copy()
    
    # get relevant columns
    new['tel'] = 'Tull'

    # MJD to JD
    new['time'] += 2400000.5
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_Zechmeister19_CES_LC(data_file):
    """Read in CES-LC RV data file from Zechmeister+19

    Args:
        data_file (str): path to .txt file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, delim_whitespace=True, skiprows=3,
                      names=['time', 'mnvel', 'errvel'], usecols=[0,1,2])
     
    # new df
    new = raw.copy()
    
    # get relevant columns
    new['tel'] = 'CES-LC'
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_Zechmeister19_CES_VLC(data_file):
    """Read in CES-VLC RV data file from Zechmeister+19

    Args:
        data_file (str): path to .txt file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, delim_whitespace=True, skiprows=3,
                      names=['time', 'mnvel', 'errvel'], usecols=[0,1,2])
     
    # new df
    new = raw.copy()
    
    # get relevant columns
    new['tel'] = 'CES-VLC'
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_Roettenbacher22_EXPRES(data_file):
    """Read in EXPRES data file from Roettenbacher+2022

    Args:
        data_file (str): path to .txt file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, delim_whitespace=True, skiprows=37,
                      names=['time', 'mnvel', 'errvel'], usecols=[0,1,2])
     
    # new df
    new = raw.copy()
    
    # get relevant columns
    new['tel'] = 'EXPRES'

    # RJD to JD
    new['time'] += 2400000
    
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



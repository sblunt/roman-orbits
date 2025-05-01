#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-04-09 10:56
Author: calebharada

9826_DataSetup.py

    Description: combines RV datasets for HD 9826 (ups And)
"""

import radvel
import pandas as pd

SYSTEM_HD = 9826
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
        get_CLS21_HIRES(f'{SYSTEM_HD}_CLS21_HIRES-Pre.csv')],
        ignore_index=True)
    # add Levy (APF)
    combined_data = pd.concat([combined_data, 
        get_CLS21_APF(f'{SYSTEM_HD}_CLS21_APF.csv')],
        ignore_index=True )
    # add Hamilton (Lick)
    combined_data = pd.concat([combined_data, 
        get_CLS21_Hamilton(f'{SYSTEM_HD}_CLS21_Hamilton.csv')],
        ignore_index=True )
    # add AFOE (Whipple)
    combined_data = pd.concat([combined_data, 
        get_Butler99_AFOE(f'{SYSTEM_HD}_Butler99_AFOE.rdb')],
        ignore_index=True )
    # add HRS (HET)
    combined_data = pd.concat([combined_data, 
        get_McArthur10_HRS(f'{SYSTEM_HD}_McArthur2010_HET.txt')],
        ignore_index=True )
    # get ELODIE (OHP)
    combined_data = pd.concat([combined_data, 
        get_Naef04_ELODIE(f'{SYSTEM_HD}_Naef04_ELODIE.txt')],
        ignore_index=True )
    # get HJS (McDonald)
    combined_data = pd.concat([combined_data, 
        get_Wittenmyer07_HJS(f'{SYSTEM_HD}_Wittenmyer07_HJS.txt')],
        ignore_index=True )
    # get SOPHIE (OHP)
    combined_data = pd.concat([combined_data, 
        get_ElodieArchive_SOPHIE(f'{SYSTEM_HD}_ElodieArchive_SOPHIE.txt')],
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


def get_CLS21_HIRES(data_file):
    """Read in an HIRES data file from CLS

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
    new['tel'] = 'HIRES-pre'
    
    # reorder columns
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


def get_Butler99_AFOE(data_file):
    """Read in AFOE/Whipple RV data file from Butler+99

    Args:
        data_file (str): path to .rdb file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, delim_whitespace=True, skiprows=2,
                      names=['time', 'mnvel', 'errvel'], usecols=[0,1,2])
     
    # new df
    new = raw.copy()
    
    # get relevant columns
    new['tel'] = 'AFOE'

    # MJD to JD
    new['time'] += 2400000.
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_McArthur10_HRS(data_file):
    """Read in HRS/HET RV data file from McArthur+2010

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
    new['tel'] = 'HRS'
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_Naef04_ELODIE(data_file):
    """Read in ELODIE/OHP RV data file from Naef+2004

    Args:
        data_file (str): path to .txt file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, delim_whitespace=True, skiprows=41,
                      names=['time', 'mnvel', 'errvel'], usecols=[0,1,2])
     
    # new df
    new = raw.copy()
    
    # get relevant columns
    new['tel'] = 'ELODIE'

    # convert to m/s
    new['mnvel'] *= 1000
    new['errvel'] *= 1000
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_Wittenmyer07_HJS(data_file):
    """Read in HJS/McDonald RV data file from Wittenmyer+2007

    Args:
        data_file (str): path to .txt file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, delim_whitespace=True, skiprows=40,
                      names=['time', 'mnvel', 'errvel'], usecols=[2,3,4])
     
    # new df
    new = raw.copy()
    
    # get relevant columns
    new['tel'] = 'HJS'
    
    # reorder columns
    new = new[STD_COL_NAMES]

    return new


def get_ElodieArchive_SOPHIE(data_file):
    """Read in SOPHIE/OHP RV data file from the Elodie Archive website

    Args:
        data_file (str): path to .txt file

    Returns:
        pd.DataFrame: RV dataframe
    """
    # load file
    raw = pd.read_csv(data_file, comment='#', skiprows=26,
                      names=['mnvel', 'errvel', 'time'], usecols=[6,7,17])
     
    # new df
    new = raw.copy()
    
    # get relevant columns
    new['tel'] = 'SOPHIE'

    # remove nans
    new = new[new['errvel'].notna()]

    # convert to m/s
    new['mnvel'] *= 1000
    new['errvel'] *= 1000
    
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



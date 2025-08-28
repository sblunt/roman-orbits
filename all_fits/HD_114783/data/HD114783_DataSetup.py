import pandas as pd
import radvel
import os

# assumes the CLS and HARPS data files are in the same directory as this file
this_dir = os.path.dirname(__file__)
path1 = os.path.join(this_dir, "CLS_rv_raw.txt")
path2 = os.path.join(this_dir, "HARPS_rv_raw.txt")

# set nightly binning option
binning = 1  # nightly bin, 1 for yes, 2 for no

############
# CLS data #    including Hamilton, HIRES, and APF data
############ 
data1 = pd.read_csv(
    path1,
    header=None,
    skiprows=30,
    delim_whitespace=True,
    usecols=[2, 4, 5, 6],
    names=("tel", "time", "mnvel", "errvel"),
)
data1_ham = data1[data1["tel"] == "lick"]  # Lick Hamilton data
data1_ham["tel"] = "Hamilton"
data1_pre = data1[data1["tel"] == "k"]  # Keck HIRES-pre data
data1_pre["tel"] = "HIRES-pre"
data1_post = data1[data1["tel"] == "j"]  # Keck HIRES-post data
data1_post["tel"] = "HIRES-post"
data1_apf = data1[data1["tel"] == "apf"]  # APF Levy data
data1_apf["tel"] = "APF"

#################
# HARPS pre and #
#   post data   #
#################
data2 = pd.read_csv(
    path2, 
    header=None,
    skiprows=2,
    sep='\s+',
    usecols=[3,4,5],
    names=('time','mnvel','errvel')
)
data2_pre = data2[data2['time'] < 2457174.5]   # pre-upgrade data
data2_pre['tel'] = 'HARPS-pre'
data2_post = data2[data2['time'] > 2457174.5]   # post-upgrade data
data2_post['tel'] = 'HARPS-post'


# data concatenation and optionally do nightly bin of all data sources
dataframe = [data1_ham, data1_pre, data1_post, data1_apf, data2_pre, data2_post]
data_all = pd.concat(dataframe, ignore_index=True)
data_all.to_csv(
    "HD114783_rv_combined_unbinned.txt",
    sep="\t",
    index=False,
    header=True,
)

# nightly bin
if binning == 1:
    time, mnvel, errvel, tel = radvel.utils.bintels(
        data_all["time"].values,
        data_all["mnvel"].values,
        data_all["errvel"].values,
        data_all["tel"],
    )
    bin_dict = {"time": time, "mnvel": mnvel, "errvel": errvel, "tel": tel}

    data_all_bin = pd.DataFrame(data=bin_dict)
    data_all_bin.to_csv(
        "HD114783_rv_combined_binned.txt", sep="\t", index=False, header=True
    )

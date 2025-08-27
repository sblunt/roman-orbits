
import pandas as pd
import radvel
import numpy as np

path1 = "/Users/macuser/Roman/rv_orbits/roman-orbits/all_fits/HD_95735/data/CLS_rv_raw.txt"
path2 = "/Users/macuser/Roman/rv_orbits/roman-orbits/all_fits/HD_95735/data/SOPHIE_rv_raw.txt"

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


###############
# SOPHIE data #
###############
data2 = pd.read_csv(
    path2,
    header=None,
    skiprows=17,
    delim_whitespace=True,
    usecols=[2,3,6,7],
    names=('mnvel', 'errvel', 'mjd', 'time'),
)
# convert mjd to bjd for observations with nan bjd
for i, (bjd, mjd) in enumerate(zip(data2['time'].values, data2['mjd'].values)):
     if np.isnan(bjd):
         data2['time'].iloc[i] = mjd + 2400000
# drop unneccesary labels
data2 = data2.drop(columns='mjd')
# drop observations with nan errvel
data2 = data2.drop(index=np.where(np.isnan(data2['errvel']))[0])
# convert RV measurements in km/s to m/s
data2["mnvel"] *= 1000  
data2["errvel"] *= 1000 
# add instrument name 
data2["tel"] = "SOPHIE"


########################################################################################
# data concatenation and optionally do nightly bin of all data sources
dataframe = [data2, data1_ham, data1_pre, data1_post, data1_apf]
data_all = pd.concat(dataframe, ignore_index=True)
data_all.to_csv(
    "HD95735_rv_combined_unbinned.txt",
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
        "HD95735_rv_combined_binned.txt", sep="\t", index=False, header=True
    )

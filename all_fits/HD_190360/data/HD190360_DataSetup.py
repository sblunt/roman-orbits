import pandas as pd
import radvel

path1 = "ELODIE_rv_raw.txt"
path2 = "SOPHIE_rv_raw.txt"
path3 = "CLS_rv_raw.txt"

# set nightly binning option
binning = 1  # nightly bin, 1 for yes, 2 for no

# ELODIE and AFOE data
data1 = pd.read_csv(
    path1,
    header=None,
    skiprows=27,
    delim_whitespace=True,
    names=("time", "mnvel", "errvel", "tel"),
)
data1["mnvel"] *= 1000
data1["errvel"] *= 1000
data1_el = data1[data1["tel"] == 1]
data1_af = data1[data1["tel"] == 2]
data1_el["tel"] = "ELODIE"
data1_af["tel"] = "AFOE"

# SOPHIE data
data2 = pd.read_csv(
    path2,
    header=None,
    skiprows=1,
    delim_whitespace=True,
    names=("time", "mnvel", "errvel"),
)

data2["time"] += 2400000
data2["mnvel"] *= 1000
data2["errvel"] *= 1000
data2["tel"] = "SOPHIE"

# CLS data, including Hamilton, HIRES, and APF data
data3 = pd.read_csv(
    path3,
    header=None,
    skiprows=30,
    delim_whitespace=True,
    usecols=[2, 4, 5, 6],
    names=("tel", "time", "mnvel", "errvel"),
)
data3_ham = data3[data3["tel"] == "lick"]  # Lick Hamilton data
data3_ham["tel"] = "Hamilton"
data3_pre = data3[data3["tel"] == "k"]  # Keck HIRES-pre data
data3_pre["tel"] = "HIRES-pre"
data3_post = data3[data3["tel"] == "j"]  # Keck HIRES-post data
data3_post["tel"] = "HIRES-post"
data3_apf = data3[data3["tel"] == "apf"]  # APF Levy data
data3_apf["tel"] = "APF"

# data concatenation and optionally do nightly bin of all data sources
dataframe = [data1_el, data1_af, data2, data3_ham, data3_pre, data3_post, data3_apf]
data_all = pd.concat(dataframe, ignore_index=True)
data_all.to_csv(
    "HD190360_rv_combined_unbinned.txt",
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
        "HD190360_rv_combined_binned.txt", sep="\t", index=False, header=True
    )

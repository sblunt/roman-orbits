import pandas as pd
from astropy.table import Table
from copy import deepcopy
import toml, os
from pprint import pprint
import radvel

#running_from_top_dir = True

instruments = toml.load("instruments.toml")

#if running_from_top_dir:
#
#    subfolders = sorted([f.path for f in os.scandir(".") if f.is_dir()])
#
#    print("Choose system to compile RVs for.")
#    print("(the sub-direcotry 'data' must have a valid sources.toml file).")
#    print("0:\tTerminate Program")
#    for idx, f in enumerate(subfolders):
#        print("{}:\t{}".format(idx + 1, f))
#    whichdir = int(input("> "))
#
#    if whichdir == 0:
#        exit()
#    assert whichdir <= len(subfolders) + 1, (
#        "Chosen number is not valid."
#    )
#
#    cd_path = "./{}/data".format(subfolders[whichdir - 1])
#    os.chdir(cd_path)
#
#    #print(os.getcwd())

# Indices 0-3 are the RadVel standard column names
# Indices 4-5 are the components of the "tel" column (inst-source)
standard_names = [
    "time", # 0
    "mnvel", # 1
    "errvel", # 2
    "tel", # 3
    "inst", # 4 - The instrument
    "source", # 5 - The data source
]

sources = toml.load("sources.toml")

for k, v in sources.items():
    
    if v["is_survey"]:
        sdata = Table.read(v["fname"], format = v["format"]).to_pandas()
        # Locate only the rows that contain the desired system
        data = sdata[sdata[v["system_col"]["col"]] == v["system_col"]["name"]].copy()
    else:
        data = Table.read(v["fname"], format = v["format"]).to_pandas()
    # Incorporate JD offset
    data[v["jd_name"]] = data[v["jd_name"]] + v["jd_offset"]
    # Rename columns to standard names (t, rv, e_rv)
    data.rename(
        columns = {
            v["jd_name"] : standard_names[0],
            v["rv_name"] : standard_names[1],
            v["e_rv_name"] : standard_names[2],
        },
        inplace = True,
    )
    # Check to see if the data is actually in km/s
    if ("rv_in_km" in v.keys()):
        if v["rv_in_km"]:
            data[standard_names[1]] = data[standard_names[1]] * 1000
            data[standard_names[2]] = data[standard_names[2]] * 1000
    # Now to deal with the instrument nightmare
    # First, create a placeholder column of nans for the "tel" column
    data[standard_names[3]] = [None] * len(data)
    # Check if there is inst_col or inst_all in the keys:
    if "inst_new" in v.keys():
        instcol = [v["inst_new"]] * len(data)
        data[standard_names[4]] = instcol

    elif "inst_col" in v.keys():
        # Now make sure all the goddamn instrument names are STRINGS
        data[v["inst_col"]["col"]] = data[v["inst_col"]["col"]].astype(str)
        instcolname = v["inst_col"]["col"]
        instreplace = v["inst_col"]["names"]
        # Add the data source name into the instrument name
        for kk, vv in instreplace.items():
            instreplace[kk] = vv # + "-" + str(k)
        data.replace(
            {instcolname : instreplace},
            inplace = True,
        )
        data.rename(
            columns = {
                instcolname : standard_names[4],
            },
            inplace = True,
        )

    data[standard_names[5]] = [str(k)] * len(data)

    # Save in the sources dictionary
    v['data'] = deepcopy(data)
    
# Compile all data sources into one simplified RV table

dataframes = []

# Adding notes for the data source is now in the data's instrument
for k, v, in sources.items():
    copyframe = v['data'][standard_names].copy()
    #copyframe["source"] = [k] * len(copyframe)
    dataframes.append(copyframe)

alldata = pd.concat(dataframes, ignore_index = True).sort_values(by = standard_names[0]).copy()

# Ok, we're implementing this. We now need to run through the instrument.toml file
# and split out any data that may come from instruments that underwent upgrades
# (e.g. hires -> hiresj & hiresk)

for k, v in instruments.items():
    if not v['divide']:
        continue
    kidxs = alldata.index[alldata[standard_names[4]] == k].tolist()
    if len(kidxs) == 0:
        continue
    for idx in kidxs:
        # Iterate through the keys and values within v (these are the different
        # upgrade periods)
        pointjd = alldata[standard_names[0]][idx]
        for kk, vv, in v.items():
            if kk == "divide":
                continue
            if type(vv) is not dict:
                continue
            if ("jd_min" not in vv.keys()) or ("jd_max" not in vv.keys()):
                print("WARNING: {}.{} is missing either jd_min or jd_max, its points have not been treated properly".format(k, kk))
                continue
            if (pointjd >= vv['jd_min']) and (pointjd < vv['jd_max']):
                alldata.at[idx, standard_names[4]] = kk

# Ok, so the Lick Hamilton spectrograph data is an absolute pain in my ass.
# I could implement something in here that checks all the lick data from all
# sources... but I'm just going to have all data except the Lick 25 yr data 
# get ignored in the sources.toml file because otherwise I'm gonna lose my mind

# In the instruments.toml, there are periods where RV data should be ignored.
# For example, data taken during the HARPS 2015 fiber upgrade gets labeled
# "ignoreharps01". So, get the indices of each data point in all the data
# that has an "ignore" in the instrument name and remove it.

ignoredata = alldata[alldata[standard_names[4]].str.contains("ignore", na = False)].copy()
alldata = alldata[~alldata[standard_names[4]].str.contains("ignore", na = False)].reset_index(drop = True).copy()

if len(ignoredata) > 0:
    ignoredata.to_csv("ignored_points.csv", index = False)
    print("Ignored {} data points (see ignored_points.csv)".format(len(ignoredata)))

# Now, since there are multiple RV data sources, we need to remove duplicate
# data points.
# First, we will check if there are two adjacent data points within 0.001 of a 
# day (1.44 minutes) of each other.
# If there are indeed two data points within 1.44 minutes of each other, then we
# need to check they are from the same spectrograph.
# If they are from the same spectrograph, the data point with the smaller RV error
# will be selected.

duplicate_points = []
deleted_points_list = []

for i in range(len(alldata) - 1):
    point1 = alldata.iloc[i]
    point2 = alldata.iloc[i + 1]

    t1 = point1["time"]
    t2 = point2["time"]

    e_rv1 = point1["errvel"]
    e_rv2 = point2["errvel"]

    inst1 = str(point1["inst"]).strip()#.split("-")[0])
    inst2 = str(point2["inst"]).strip()#.split("-")[0])

    #print("1: {}    2: {}    Match? {}".format(inst1, inst2, inst1==inst2))

    dt = t2 - t1

    if (dt < 0.001) and (inst1 == inst2):
        if e_rv1 < e_rv2:
            # Remove the lower accuracy point 2
            duplicate_points.append(i + 1)
            deleted_points_list.append(point2)
        else:
            # Remove the lower accuracy point 1
            duplicate_points.append(i)
            deleted_points_list.append(point1)

deleted_points = pd.DataFrame(deleted_points_list)

if len(duplicate_points) > 0:
    deleted_points.to_csv("duplicate_points.csv", index = False)
    print("Deleted {} duplicate data points (see duplicate_points.csv)".format(len(duplicate_points)))
    finaldata = alldata.drop(index = duplicate_points).reset_index(drop = True)
else:
    finaldata = alldata

# Now, the last thing we need to do is to smash the "source" column strings
# onto the end of the instrument strings
finaldata[standard_names[3]] = finaldata[standard_names[4]].astype(str) + "-" + finaldata[standard_names[5]].astype(str)

print("Final set of RVs consists of {} unique data points.".format(len(finaldata)))


# Sarah: we don't want to fit RVs from the same instrument but different pubs differently,
# so change the separation Nick implemented above here (super clunky but oh well)
finaldata = finaldata.rename(columns={"tel":"inst", "inst":"tel"})

finaldata.to_csv("all_rvs_unbinned.csv", index = False)

time, mnvel, errvel, tel = radvel.utils.bintels(finaldata['time'].values,\
                            finaldata['mnvel'].values,finaldata['errvel'].values,\
                            finaldata['tel'])
bin_dict = {'time':time, 'mnvel':mnvel, 'errvel':errvel, 'tel':tel}

data_all_bin = pd.DataFrame(data=bin_dict)
data_all_bin.to_csv('all_rvs_binned.csv', index=False, header=True)
# HD219134 - Nick Schragal

This folder contains two sub-folders:

## `data`

Inside this folder are the raw data and the script necessary to prepare it into a final table for radvel to injest.

Important files to note:
- `all_rvs.csv` - This is the final set of radial velocities that is injested by the radvel fitting script.
- `[Source Name]_DataSetup.py` - This is the script that generates the final set of radial velocities `all_rvs.csv`. This script depends on the files `instruments.toml` and `sources.toml`.
- `instruments.toml` - This configuration file was born out of frustration regarding certain datasets having upgrades done which may have altered their RV offsets but not having these upgrades indicated in the raw data. A further elaboration on the format of this file can be found below
- `sources.toml` - This configuration file describes key aspects of the raw data sources used in preparation of this data. A further elaboration on this file can be found below.
- `vizier_query.py` - This is a leftover script used to query datasets publically available on Vizier.
- The remaining files are iterations of the raw data files (some have had their formats converted).

## `fits`

Inside this folder are the scripts needed to run the orbit fits.

- `[Source Name]_radvel.py` - This is the radvel setup script for the source.
- `run_orbit.sh` - This is the bash script that will run the radvel commands to fit an orbit to the source's data (`all_rvs.csv`)

NOTE: As currently configured and with the latest version of radvel, the `run_orbit.sh` script will fail during plotting. This is because radvel only defines 9 default colors to use in plotting, while there are more than 9 data sources present if you use the present `all_rvs.csv`. This can be fixed by *modifying the radvel source code* (yeah, I know it sucks, but it must be done):
1. Navigate to the folder containing the radvel installation you are using. (By this, I mean the directory level that contains `setup.py`, the README, and the `pyproject.toml`)
2. Now navigate into `./radvel/plot` and open `__init__.py`
3. Around line 43 there will be a line that reads
```
default_colors = ['orange', 'purple', 'magenta', 'pink', 'green', 'grey', 'red', 'blue', 'yellow']
```
4. Comment out this line and replace it with the following:
```
cmap = pl.get_cmap('tab20')
colors = [cmap(i) for i in range(cmap.N)]  # Get all colors in the colormap
default_colors = [matplotlib.colors.rgb2hex(color) for color in colors]  # Convert to hex
```
5. Save and close. The plotting routine should now run to completion.

The code above replaces the default color map with a color map derived from matplotlib's `tab20` color map. It contains 20 colors, enough for 20 data sources.

If you have any questions regarding the contents of these folders, please don't hesitate to contact Nick Schragal. I don't know what I was on when I wrote all this, but it somehow works despite it being horrendous.

## Elaborations on `instruments.toml` and `sources.toml`

### `instruments.toml`

This .toml file exists to describe upgrades made to spectrographs where their RV offsets may have been altered by the upgrade. To explain the formatting, let's take HARPS as an example. In this file you will find the following:
```
# ESO's HARPS Spectrograph

[harps]
divide = true

# Data points from the commissioning of HARPS until the 2015 Fiber Upgrade
[harps.harps0]
jd_min = 0
jd_max = 2457157

# Some data was taken during the fiber upgrade. The spectrograph was not
# stable during this period, do not use this data.
[harps.ignoreharps01]
jd_min = 2457157
jd_max = 2457177

# Data points from the completion of the 2015 Fiber Upgrade to the
# beginning of the 2023 Cryostat Intervention
[harps.harps1]
jd_min = 2457177
jd_max = 2460263

# Some data may have been taken during the cryostat intervention.
# The spectrograph likely would not have been stable during this period,
# so do not use this data.
[harps.ignoreharps12]
jd_min = 2460263
jd_max = 2460277

# Data points after the 2023 cryostat intervention
[harps.harps2]
jd_min = 2460277
jd_max = inf
```
At the top, the name of the instrument is given as a dictionary entry `[harps]` with one sub-entry `divide = true`. This indicates that HARPS data should be split up according to date taken. In python dictionary parlance, this small section formats to 
```
{
    "harps":{
        "divide": True,
        },
}
```

Second, the divisions are defined. Let's take the first for example `[harps.harps0]`. This is the first time block for the HARPS instrument before the 2015 fiber upgrade. Any HARPS data taken between the start and end times (in JD) here will be labeled as `harps0` data. In the case of HARPS, there are 5 time blocks here. In python dictionary parlance (just considering the harps0 block), our dictionary now looks like
```
{
    "harps":{
        "divide":True,
        "harps0":{
            jd_min: 0,
            jd_max: 2457157,
        },
    },
}
```

Finally, you'll notice there are two time blocks in the HARPS data that have "ignore" as a substring within their name. This is used by the data preparation script to indicate that any data taken during this block of time for this instrument should not be used. In the case of these time blocks for HARPS, data might have been taken during these interventions in the spectrograph.

### `sources.toml`

This .toml file exists to describe the data sources used for this source. Let's take a look at the example of the data description for the California Legacy Survey (CLS):

```
[callegacy]
fname = "californialegacyrvs.txt"
format = "ascii.cds"
jd_name = "BJD"
rv_name = "RVel"
e_rv_name = "e_RVel"
jd_offset = 0
is_survey = true
inst_col.col = "Inst"

[callegacy.inst_col.names]
k = "hiresk"
j = "hiresj"
apf = "apf"
lick = "ignore"

[callegacy.system_col]
col = "Name"
name = "87883"
```

First, the name of the data source is the first key in the dictionary `[callegacy]`. Below this are the following keys:
- `fname` - The name of the raw data file corresponding to this data source (this is a relative path, relative to the `./data` directory)
- `format` - A string that can be used in the `format` argument for astropy.Table.read() that describes the format of the raw data file indicated by `fname`. In this example, the file is a CDS-formatted table.
- `jd_name` - The name of the column in the raw data table that corresponds to the time (in units of days, e.g. JD, MJD, BJD, etc.) the observation was made. In this case, `BJD` is the column for time.
- `rv_name` - The name of the column in the raw data that corresponds to the measured radial velocity (in m/s).
- `e_rv_name` - The name of the column in the raw data that corresponds to the error on the radial velocity measurement (in m/s)
- `jd_offset` - The time indicated by the column specified by `jd_name` may not be a true Julian Date. This number describes the offset and is added to all quantities in the raw data's `jd_name` column. For example, if times in the raw data were reported in MJD, then this quantity would be 2400000.5
- `is_survey` - Indicates whether or not this source is a "survey", meaning that there are RV measurements from multiple sources present in the raw data.
- `inst_col.col` - Tha name of the column in the raw data the represents which instrument the data was taken with. See below for elaboration on `inst_col.names`

Next, you will find `[callegacy.inst_col.names]`. CLS has data from multiple spectrographs, this section describes a mapping between the names in the CLS raw data to standard names. For example, any data marked in the CLS raw data with a `k` in the instrument column is HIRES data from its "k" period (pre-upgrade) and is thus renamed to `hiresk` by the data setup script.

Finally, you will find `[callegacy.system_col]`. This section is present because the CLS raw data contains data from multiple different sources. This section describes what column the script should search in (`col`) and what designator it should search for (`name`) to locate the data for this source.
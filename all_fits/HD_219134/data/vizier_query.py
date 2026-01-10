from astropy.table import Table
from astroquery.vizier import Vizier

vizier = Vizier()
vizier.ROW_LIMIT = 100000000000
overwrite = True

query_butler = True
query_motalebi = True
query_johnson = True
query_bonfanti = True
query_hirsch = True
query_lick25 = True

# Butler et al. 2017 - LCES HIRES
if query_butler:
    table_name = "J/AJ/153/208/table1"
    constraints = {
        "Name" : "HD219134",
    }

    result = vizier.query_constraints(
        catalog = table_name,
        **constraints,
    )

    table = Table(result[0])

    table.write("butler2017.csv", format = "ascii.csv", overwrite = overwrite)

# Motalebi et al. 2015
if query_motalebi:
    table_name = "J/A+A/584/A72/table6"
    constraints = {
    #    "HD" : ,
    }

    result = vizier.query_constraints(
        catalog = table_name,
        **constraints,
    )

    table = Table(result[0])

    table.write("motalebi2015.csv", format = "ascii.csv", overwrite = overwrite)

# Johnson et al. 2016 HJST Table
if query_johnson:
    table_name = "J/ApJ/821/74/table1"
    constraints = {
        "e_dRV" : ">0",
    }

    result = vizier.query_constraints(
        catalog = table_name,
        **constraints,
    )

    table = Table(result[0])

    table.write("johnson2016hj.csv", format = "ascii.csv", overwrite = overwrite)

# Johnson et al. 2016 HIRES Table
if query_johnson:
    table_name = "J/ApJ/821/74/table2"
    constraints = {
        "e_dRV" : ">0",
    }

    result = vizier.query_constraints(
        catalog = table_name,
        **constraints,
    )

    table = Table(result[0])

    table.write("johnson2016hr.csv", format = "ascii.csv", overwrite = overwrite)

# Bonfanti & Gillon 2020
if query_bonfanti:
    table_name = "J/A+A/635/A6/rv1"
    constraints = {
    #    "e_dRV" : ">0",
    }

    result = vizier.query_constraints(
        catalog = table_name,
        **constraints,
    )

    table = Table(result[0])

    table.write("bonfanti2020.csv", format = "ascii.csv", overwrite = overwrite)

# Hirsch et al. 2021 - APF, HIRES J & K, Lick
if query_hirsch:
    table_name = "J/AJ/161/134/table3"
    constraints = {
        "HD" : 219134,
    }

    result = vizier.query_constraints(
        catalog = table_name,
        **constraints,
    )

    table = Table(result[0])

    table.write("hirsch2021.csv", format = "ascii.csv", overwrite = overwrite)

if query_lick25:
    table_name = "J/ApJS/210/5/table2"
    constraints = {
        "Name" : "219134",
    }

    result = vizier.query_constraints(
        catalog = table_name,
        **constraints,
    )

    table = Table(result[0])

    table.write("lick25.csv", format = "ascii.csv", overwrite = True)

from astropy.table import Table
from astroquery.vizier import Vizier

vizier = Vizier()
vizier.ROW_LIMIT = 100000000000
overwrite = True

query_butler = True
query_hirsch = True
query_lick25 = True

# Butler et al. 2017 - LCES HIRES
if query_butler:
    table_name = "J/AJ/153/208/table1"
    constraints = {
        "Name" : "HD87883",
    }

    result = vizier.query_constraints(
        catalog = table_name,
        **constraints,
    )

    table = Table(result[0])

    table.write("butler2017.csv", format = "ascii.csv", overwrite = overwrite)

# Hirsch et al. 2021 - APF, HIRES J & K, Lick
if query_hirsch:
    table_name = "J/AJ/161/134/table3"
    constraints = {
        "HD" : 87883,
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
        "Name" : "87883",
    }

    result = vizier.query_constraints(
        catalog = table_name,
        **constraints,
    )

    table = Table(result[0])

    table.write("lick25.csv", format = "ascii.csv", overwrite = overwrite)

import pandas as pd
import numpy as np

ninds = pd.read_csv("ninds.csv")
aff = pd.read_csv("affiliations.csv", header = 1)

ninds = ninds.rename(index=str, columns={"organization city":"city", "organization state":"state"},)
aff = aff.rename(index=str, columns={"aff_city": "city", "aff_state": "state"})
aff = aff.rename(index=str,columns={"scopus idx": "scopus_idx"})


ninds["city"], aff["city"] = ninds["city"].str.lower(), aff["city"].str.lower()
ninds["state"], aff["state"] = ninds["state"].str.lower(), aff["state"].str.lower()

aff_cs = aff[["scopus_idx","city","state"]]


ninds_scopus = pd.merge(ninds, aff_cs, on =["scopus_idx"], how='right' )
ninds_scopus["city_match"] = np.where(ninds_scopus["city_x"] == ninds_scopus["city_y"], 1,0)
ninds_scopus["state_match"] = np.where(ninds_scopus["state_x"] == ninds_scopus["state_y"], 1,0)
ninds_scopus["keep"] = np.where((ninds_scopus["city_match"] == 1) | (ninds_scopus["state_match"] == 1), 1, 0)
ninds_keep = ninds_scopus[ninds_scopus["keep"] == 1]





# ninds = ninds.rename(index=str, columns={"organization state":"state"},)
# aff = aff.rename(index=str, columns={"aff_state": "state"})
# aff = aff.rename(index=str,columns={"scopus idx": "scopus_idx"})
#
# ninds["city"], aff["city"] = ninds["city"].str.lower(), aff["city"].str.lower()
#
# ninds_city, aff_city = ninds[["scopus_idx","state"]], aff[["scopus_idx","city"]]
#
# ninds_city, aff_city = ninds_city.sort_values("city"), aff_city.sort_values("city")
#
#
# # test = pd.merge(ninds_city, aff_city, on =["scopus_idx","city"], how='outer' )
# test = pd.merge(ninds_city, aff_city, on =["scopus_idx"], how='right' )
# test["city_match"] = np.where(test["city_x"] == test["city_y"], 1,0)





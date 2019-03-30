import pandas as pd
import numpy as np

ninds = pd.read_csv("ninds.csv")
aff = pd.read_csv("clean_affiliations.csv")

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

# ninds_keep.to_csv("check_ninds.csv")

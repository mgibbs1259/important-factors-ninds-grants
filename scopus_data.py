import glob
import os
import time
import re

import pandas as pd
import numpy as np
# import scopus
# from scopus import AuthorSearch
# from scopus import AuthorRetrieval
# from scopus import ContentAffiliationRetrieval


# Create function to return name as first_middle last format
def name_split(pi):
    if "," not in pi:
        pass
    else:
        nih_pi_split = pi.split(', ')
        if len(nih_pi_split[1].split()) > 1:
            last = nih_pi_split[0].title()
            middle = nih_pi_split[1].lstrip().split(' ')[1].title()[0]
            first = nih_pi_split[1].lstrip().split(' ')[0].title()
        else:
            last = nih_pi_split[0].title()
            middle = ""
            first = nih_pi_split[1].lstrip().title()
        first_middle = first + " " + middle
        return [first_middle, last]


# Get ninds pi
ninds_df = pd.read_csv("data/ninds_data.csv")
ninds_df.columns = map(str.lower, ninds_df.columns)
ninds_pi = ninds_df.loc[:, "contact pi / project leader"]


# Apply function to ninds pi
#scopus_pi = ninds_pi.apply(name_split)


# Get unique names from nih_data
#scopus_search = scopus_pi.unique()
#print(scopus_search)

# Scopus DATA

#scopus_series_list = []

# for i in range(0, len(nih_pi)):
#
#     # Use AuthorSearch
#     try:
#         scopus_authors = AuthorSearch('AUTHLAST(' + scopus_search_names.iloc[i][1].title() + ') and AUTHFIRST(' + scopus_search_names.iloc[i][0].title() + ')', refresh = True)
#         df = pd.DataFrame(scopus_authors.authors)
#
#         df = df.iloc[0, :]
#         print(df)
#
#         # Get Scopus ID
#         eid = df["eid"].values
#         scopus_id = eid[0][7:]
#
#         # Use AuthorRetrieval
#         au = AuthorRetrieval(scopus_id)
#
#         # Get Current Affiliation ID
#         aff_current_ID = au.affiliation_current
#         # Use ContentAffiliationRetrieval
#         aff_current = ContentAffiliationRetrieval(aff_current_ID)
#
#         # Create Scopus dictionary
#         scopus_dict = {'name': ascopus_search_names.iloc[i][0].title() + ' ' + scopus_search_names.iloc[i][1].title(), 'scopus_id': scopus_id,
#                        'document_count': au.document_count, 'citation_count': au.citation_count,
#                        'h_index': au.h_index, 'begin_publication_range': au.publication_range[0],
#                        'end_publication_range': au.publication_range[1], 'aff_current_name': aff_current.affiliation_name,
#                        'aff_current_city': aff_current.city, 'aff_current_state': aff_current.state,
#                        'aff_current_auth_count': aff_current.author_count, 'aff_current_doc_count': aff_current.document_count}
#
#
#         # Create Scopus series
#         scopus_series = pd.Series(scopus_dict)
#         print(scopus_series)
#         scopus_series_list.append(scopus_series)
#         time.sleep(2)
#
#        # Out as csv
#
#     except:
#         pass
#



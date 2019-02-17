import glob
import os
import time
import re

import pandas as pd
import numpy as np
import scopus
from scopus import AuthorSearch
from scopus import AuthorRetrieval
from scopus import ContentAffiliationRetrieval


# NIH data

# Create nih dataframe
files_list = glob.glob("data/*.csv")
nih_data = pd.concat(map(lambda file: pd.read_csv(file, encoding = "cp1252"), files_list))
nih_data = nih_data.apply(lambda x: x.astype(str).str.lower())
nih_data.columns = map(str.lower, nih_data.columns)
nih_data.columns = nih_data.columns.str.replace(' ', '_')
nih_data.columns = nih_data.columns.str.replace('(','')
nih_data.columns = nih_data.columns.str.replace(')','')

# Get Contact PI/Project Leader
nih_pi = nih_data['contact_pi_/_project_leader']


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
        # print(first_middle, last)
        return [first_middle, last]


scopus_search_names = nih_pi.apply(name_split)
nih_data_with_scopus_idx = pd.merge(nih_data, pd.DataFrame(scopus_search_names), left_index=True, right_index=True)
# nih_data_with_scopus_idx["contact_pi_/_project_leader_y"] = nih_data_with_scopus_idx["contact_pi_/_project_leader_y"].rename(idx=str, columns={"contact_pi_/_project_leader_y": "scopus_idx"})
# nih_data_with_scopus_idx = nih_data.join(pd.DataFrame(scopus_search_names))
print(nih_data_with_scopus_idx.head())

# Scopus data

scopus_series_list = []


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
#
#     except:
#         pass
#



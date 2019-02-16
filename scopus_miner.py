import pandas as pd
import numpy as np
import scopus
from scopus import AuthorSearch
from scopus import AuthorRetrieval
from scopus import ContentAffiliationRetrieval


# Use AuthorSearch
scopus_authors = AuthorSearch('AUTHLAST(Han) and AUTHFIRST(Chun)', refresh = True)
df = pd.DataFrame(scopus_authors.authors)
df = df[df['affiliation'] == 'Cornell University']


# Parse eid to get Scopus ID
eid = df["eid"].values
scopus_id = eid[0][7:]


# Use AuthorRetrieval
au = AuthorRetrieval(scopus_id)
scopus_id = {'scopus_id': scopus_id}
document_count = {'document_count': au.document_count}
citation_count = {'citation_count': au.citation_count}
h_index = {'h_index': au.h_index}
begin_publication_range = {'begin_publication_range': au.publication_range[0]}
end_publication_range = {'end_publication_range': au.publication_range[1]}


# Use affiliation IDs to get institution name
aff_current_ID = au.affiliation_current


# Use ContentAffiliationRetrieval
aff_current = ContentAffiliationRetrieval(aff_current_ID)
aff_current_name = {'aff_current_name': aff_current.affiliation_name}
aff_current_city = {'aff_current_city': aff_current.city}
aff_current_state = {'aff_current_state': aff_current.state}
aff_current_auth_count = {'aff_current_auth_count': aff_current.author_count}
aff_current_doc_count = {'aff_current_doc_count': aff_current.document_count}


# Create dataframe
df = pd.DataFrame.from_dict([scopus_id, document_count, citation_count, h_index, begin_publication_range,
                             end_publication_range, aff_current_name, aff_current_city, aff_current_state,
                             aff_current_auth_count, aff_current_doc_count])

print(df)
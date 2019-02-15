import scopus
from scopus import AuthorSearch
from scopus import AuthorRetrieval
import pandas as pd

s = AuthorSearch('AUTHLAST(Han) and AUTHFIRST(Chun)', refresh = True)
df = (pd.DataFrame(s.authors))

df = df[df['affiliation'] == 'Cornell University']

print(df)

au = AuthorRetrieval(df.loc['affiliation_id'])
print(au.citation_count)
print(au.document_count)
print(au.h_index)
print(au.publication_range)
print(pd.DataFrame(au.journal_history).head())
print(au.get_coauthors)

print(df)
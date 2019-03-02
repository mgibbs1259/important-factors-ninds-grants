import pandas as pd
import numpy as np
import scopus
from scopus import AuthorSearch
from scopus import AuthorRetrieval
from scopus import ContentAffiliationRetrieval


# Create format name function - FIX
def format_name(pi):
    if ',' not in pi:
        pass
    else:
        nih_pi_split = pi.split(', ')
        if len(nih_pi_split[1].split()) > 1:
            last = nih_pi_split[0].title()
            middle = nih_pi_split[1].lstrip().split(' ')[1].title()[0]
            first = nih_pi_split[1].lstrip().split(' ')[0].title()
        else:
            last = nih_pi_split[0].title()
            middle = ''
            first = nih_pi_split[1].lstrip().title()
        first_middle = first + ' ' + middle
        return first_middle, last


# Get ninds pi
ninds_df = pd.read_csv('data/ninds_data.csv')
ninds_df.columns = map(str.lower, ninds_df.columns)
ninds_pi = ninds_df.loc[:, 'contact pi / project leader']


# Apply format name function to ninds pi
scopus_pi = pd.Series(ninds_pi.apply(format_name))


# Add scopus pi column to ninds data, purpose is joining dfs later on
# ninds_df['scopus idx'] = scopus_pi
# ninds_df.to_csv('ninds_scopus_idx_data.csv')

# Get unique names from scopus pi
scopus_search = scopus_pi.unique()
# print(len(scopus_search))
# 15499 scopus search names

print(scopus_search[0:25])

# Get Scopus data

scopus_df = pd.DataFrame()
coauthors_df = pd.DataFrame()
journals_df = pd.DataFrame()
affiliations_df = pd.DataFrame()

# Range - 0 to 4900, 4901 to 9800, 9801 to 14700, 14701 to last
for i in range(0, 25):

    try:
        # Use AuthorSearch
        scopus_authors = AuthorSearch('AUTHLAST(' + scopus_search[i][1] + ') and AUTHFIRST(' + scopus_search[i][0] + ')', refresh = True)
        scopus_authors_df = pd.DataFrame(scopus_authors.authors)
        scopus_author_df = scopus_authors_df.iloc[0, :]
        print(scopus_author_df)

        # Get Scopus ID
        eid = scopus_author_df['eid']
        scopus_id = eid[7:]

        # Use AuthorRetrieval
        au = AuthorRetrieval(scopus_id)

        # Get Current Affiliation ID
        aff_current_ID = scopus_author_df['affiliation_id']

        # Use ContentAffiliationRetrieval
        aff_current = ContentAffiliationRetrieval(aff_current_ID)

        # Create Scopus dictionary
        scopus_dict = {'scopus idx': [scopus_search[i] for n in range(0, 1)], 'name': scopus_search[i][0] + ' ' + scopus_search[i][1],
                       'scopus_id': scopus_id, 'document_count': au.document_count, 'coauthor_count': au.coauthor_count, 'citation_count': au.citation_count,
                       'h_index': au.h_index, 'begin_publication_range': au.publication_range[0],
                       'end_publication_range': au.publication_range[1], 'aff_current_name': scopus_author_df['affiliation'],
                       'aff_current_city': scopus_author_df['city'], 'aff_current_state': aff_current.state,
                       'aff_current_auth_count': scopus_author_df['country'], 'aff_current_doc_count': aff_current.document_count}

        # Append scopus dict to scopus df
        scopus_dict_df = pd.DataFrame.from_dict(scopus_dict)
        scopus_df = scopus_df.append(scopus_dict_df)


        # Get coauthors
        coauth = pd.DataFrame(au.get_coauthors())
        auth_coauth = [scopus_search[i] for n in range(coauth.shape[0] + 1)]
        coauth['scopus_idx'] = pd.Series(auth_coauth)

        # Append coauthors to coauthors df
        coauthors_df = coauthors_df.append(coauth)

        # Get journals
        journals = pd.DataFrame(au.get_documents())
        auth_journals = [scopus_search[i] for n in range(journals.shape[0] + 1)]
        journals['scopus_idx'] = pd.Series(auth_journals)

        # Append coauthors to coauthors df
        journals_df = journals_df.append(journals)

        # Get former affiliations
        former_aff = au.affiliation_history
        for aff in former_aff:
            aff_ret = ContentAffiliationRetrieval(aff)
            former_aff_dict = {'scopus idx': [scopus_search[i] for n in range(0, 1)], 'aff_name': aff_ret.affiliation_name,
                                   'aff_city': aff_ret.city, 'aff_state': aff_ret.state, 'aff_country': aff_ret.country,
                                   'aff_author_count': aff_ret.author_count, 'aff_document_count': aff_ret.document_count}
            former_aff_dict_df = pd.DataFrame.from_dict(former_aff_dict)
            affiliations_df = affiliations_df.append(former_aff_dict_df)

    except:
        print('error')
        # Create empty Scopus dictionary
        empty_scopus_dict = {'scopus idx': [scopus_search[i] for n in range(0, 1)], 'name': scopus_search[i][0] + ' ' + scopus_search[i][1],
                              'scopus_id': 'NA', 'document_count': 'NA', 'coauthor_count': 'NA', 'citation_count': 'NA',
                              'h_index': 'NA', 'begin_publication_range': 'NA',
                              'end_publication_range': 'NA', 'aff_current_name': 'NA',
                              'aff_current_city': 'NA', 'aff_current_state': 'NA',
                              'aff_current_auth_count': 'NA', 'aff_current_doc_count': 'NA'}
        
        # Append empty scopus dict to scopus df
        empty_scopus_dict_df = pd.DataFrame.from_dict(empty_scopus_dict)
        scopus_df.append(empty_scopus_dict_df)

scopus_df.to_csv('scopus_data_0_25.csv')
coauthors_df.to_csv('coauthors_data_0_25.csv')
journals_df.to_csv('journals_data_0_25.csv')
affiliations_df.to_csv('affiliations_data_0_25.csv')


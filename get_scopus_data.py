import pandas as pd
import numpy as np
import scopus
from scopus import AuthorSearch
from scopus import AuthorRetrieval
from scopus import ContentAffiliationRetrieval


# Create format name function
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
ninds_df = pd.read_csv('data/ninds_data/ninds_data.csv')
ninds_df.columns = map(str.lower, ninds_df.columns)
ninds_pi = ninds_df.loc[:, 'contact pi / project leader']

# Apply format name function to ninds pi
scopus_pi = pd.Series(ninds_pi.apply(format_name))

# Add scopus pi column to ninds data, purpose is joining dfs later on
# ninds_df['scopus idx'] = scopus_pi
# ninds_df.to_csv('ninds_scopus_idx_data.csv')


# Get unique names from scopus pi
# scopus_search = scopus_pi.unique()
# print(len(scopus_search))
# 15499 scopus search names
# scopus search is a list with the format: [('Sandra M', 'Aamodt') ('Ralph D', 'Aarons') ('Creed W', 'Abell') ...,]

# use scopus search to run for missing
missing = pd.read_csv("scopus_missing.csv")
missing = missing.drop([0]) #only for scopus_missing.csv-- first row is nan
def reformat_missing(pi):
    first_middle = pi.split(', ')[0].replace("'","").replace("(","")
    last = pi.split(', ')[1].replace("'","").replace(")","")
    return first_middle, last
scopus_search = pd.Series(missing.iloc[:,1].apply(reformat_missing))

scopus_df = pd.DataFrame()
coauthors_df = pd.DataFrame()
journals_df = pd.DataFrame()
affiliations_df = pd.DataFrame()


for i in range(15000, 15500):

    try:
        # Use AuthorSearch
        scopus_authors = AuthorSearch('AUTHLAST(' + scopus_search[i][1] + ') and AUTHFIRST(' + scopus_search[i][0] + ')', refresh = True)
        scopus_authors_df = pd.DataFrame(scopus_authors.authors)
        scopus_author_df = scopus_authors_df.iloc[0, :]

        # Get scopus ID
        eid = scopus_author_df['eid']
        scopus_id = eid[7:]

        # Use AuthorRetrieval
        au = AuthorRetrieval(scopus_id)

        # Get current affiliation ID
        aff_current_ID = scopus_author_df['affiliation_id']

        # Use ContentAffiliationRetrieval
        aff_current = ContentAffiliationRetrieval(aff_current_ID)

        # Create scopus dictionary
        scopus_dict = {'scopus idx': [scopus_search[i] for n in range(0, 1)],
                       'name': scopus_search[i][0] + ' ' + scopus_search[i][1],
                       'scopus_id': scopus_id,
                       'begin_publication_range': au.publication_range[0],
                       'end_publication_range': au.publication_range[1],
                       'document_count': au.document_count,
                       'coauthor_count': au.coauthor_count,
                       'citation_count': au.citation_count,
                       'h_index': au.h_index,
                       'cited_by_count': au.cited_by_count,
                       'aff_current_name_from_affid': aff_current.affiliation_name,
                       'aff_current_city_from_affid': aff_current.city,
                       'aff_current_state_from_affid': aff_current.state,
                       'aff_current_country_from_affid': aff_current.country,
                       'aff_current_auth_count': aff_current.author_count,
                       'aff_current_doc_count': aff_current.document_count}

        # Append scopus dict to scopus df
        scopus_dict_df = pd.DataFrame.from_dict(scopus_dict)
        scopus_df = scopus_df.append(scopus_dict_df)

        # Get journals
        journals = pd.DataFrame(au.get_documents())
        auth_journals = [scopus_search[i] for n in range(journals.shape[0] + 1)]
        journals['scopus_idx'] = pd.Series(auth_journals)

        # Append coauthors to coauthors df
        journals_df = journals_df.append(journals)

        # Get coauthors
        coauth = pd.DataFrame(au.get_coauthors())
        auth_coauth = [scopus_search[i] for n in range(coauth.shape[0] + 1)]
        coauth['scopus_idx'] = pd.Series(auth_coauth)

        # Append coauthors to coauthors df
        coauthors_df = coauthors_df.append(coauth)

        # Get former affiliations
        former_aff = au.affiliation_history
        for aff in former_aff:
            aff_ret = ContentAffiliationRetrieval(aff)
            former_aff_dict = {'scopus idx': [scopus_search[i] for n in range(0, 1)],
                               'aff_name': aff_ret.affiliation_name,
                               'aff_city': aff_ret.city,
                               'aff_state': aff_ret.state,
                               'aff_country': aff_ret.country,
                               'aff_author_count': aff_ret.author_count,
                               'aff_document_count': aff_ret.document_count}
            former_aff_dict_df = pd.DataFrame.from_dict(former_aff_dict)
            affiliations_df = affiliations_df.append(former_aff_dict_df)
        print(i)

    except:
        print('error' + ' ' + str(i))


scopus_df.to_csv('scopus_data_15000_15500.csv')
journals_df.to_csv('journals_data_15000_15500.csv')
coauthors_df.to_csv('coauthors_data_15000_15500.csv')
affiliations_df.to_csv('affiliations_data_15000_15500.csv')



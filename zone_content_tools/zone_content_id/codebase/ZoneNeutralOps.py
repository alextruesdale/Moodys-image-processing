"""Module container for functions that are zone-neutral."""

from re import finditer
import numpy as np
import pandas as pd
import re
import os

def file_to_df(file_in):
    """Read .csv file into dataframe."""

    working_df = pd.read_csv(file_in, sep=',', encoding='iso-8859-1')
    working_df = working_df.drop(['Unnamed: 0'], axis=1)
    working_df = working_df[pd.notnull(working_df['text'])]
    working_df.set_index('zone_num', inplace=True)
    working_df['zone_num'] = working_df.index

    return working_df

def test_consec_years(row):
    """Search for consecutive year strings in row values."""

    current_zone = row['text']
    zone_next = row['zone_next']

    test_string = r'.*19\d{1,2}.{0,4}19\d{0,2}\s+.*'
    # print_test = r'.{0,60}19\d{1,2}.{0,4}19\d{0,2}\s+.{1,160}'

    if re.match(test_string, current_zone) or re.match(test_string, zone_next):
        value_out = 1
    else:
        value_out = 0

    return value_out

def update_and_output(zones_small, account_df_out, balance_df_out, stock_bond_df_out, reference_df_out):
    """Update original .csv file and save as new .csv file."""

    working_df = file_to_df(zones_small)
    account_column = account_df_out[['inc_table']]
    balance_column = balance_df_out[['bal_sheet']]
    stock_bond_columns = stock_bond_df_out[['stock_rec', 'bonds_rec']]
    reference_column = reference_df_out[['ref_on_stocks', 'ref_on_bonds']]

    working_df = working_df.join(account_column)
    working_df = working_df.join(balance_column)
    working_df = working_df.join(stock_bond_columns)
    working_df = working_df.join(reference_column)

    working_df = working_df[['file_name', 'manual', 'manual_yr', 'fiche', 'fiche_num',
                             'zone_num', 'CoName', 'CoNum', 'Hist', 'Dir', 'inc_table',
                             'bal_sheet', 'stock_rec', 'bonds_rec', 'ref_on_stocks',
                             'ref_on_bonds', 'text']]

    save_name = 'ZoneClassificationsUpdate.csv'
    out_path = os.getcwd()[:-8] + save_name
    working_df.to_csv(out_path, index=False)

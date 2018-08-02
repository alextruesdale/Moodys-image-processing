"""Perform operations to find Stock / Bond Table zones."""

import StockBondOps as sbo
import ZoneNeutralOps as zno
import numpy as np
import pandas as pd
import os

pd.options.mode.chained_assignment = None
# pd.set_option('display.max_colwidth', -1)
# pd.set_option('display.max_rows', None)

class stock_bond_overhead(object):

    """
    Container class to construct testing dataframe looking for stock or bond table strings /
    zones. Calls methods from similarly-named Ops module. Filters resulting dummy columns
    in data to define 'stock or bond table' zones with a 1 or 0 score.

    Attributes:

    zones_full:
    zones_small:
    working_df:
    sub_working_df:

    clean_starts_data: returned data from id_clean_starts()
        clean_starts:
        clean_starts_indices:

    confident_rows_indices:
    output_dataframe:
    """

    def __init__(self, zones_full, zones_small):

        self.zones_full = zones_full
        self.zones_small = zones_small
        self.working_df = zno.file_to_df(self.zones_small)
        self.sub_working_df = self.test_stock_bond()

        self.clean_starts_data = self.id_clean_starts()
        self.clean_starts_stocks = self.clean_starts_data[0]
        self.clean_starts_bonds = self.clean_starts_data[1]
        self.clean_starts_indices_stocks = self.clean_starts_data[2]
        self.clean_starts_indices_bonds = self.clean_starts_data[3]

        self.output_dataframe = self.update_original()

    def test_stock_bond(self):
        """Search zone content for 'year(s) ended' string."""

        sub_working_df = self.working_df[['file_name', 'text']]
        sub_working_df['zone_next'] = sub_working_df['text']
        sub_working_df.zone_next = sub_working_df.zone_next.shift(-1)
        sub_working_df = sub_working_df.fillna(value='')

        # sub_working_df['consec_years'] = sub_working_df.apply(zno.test_consec_years, axis=1)
        sub_working_df['stock_records'] = sub_working_df.text.apply(sbo.test_stock_records)
        sub_working_df['bonds_records'] = sub_working_df.text.apply(sbo.test_bond_records)

        return sub_working_df

    def id_clean_starts(self):
        """Identify well-defined income accounts / statements starts."""

        clean_starts_stocks = self.sub_working_df.loc[(self.sub_working_df['stock_records'] == 1)]
        clean_starts_bonds =  self.sub_working_df.loc[(self.sub_working_df['bonds_records'] == 1)]

        clean_starts_indices_stocks = clean_starts_stocks.index.values
        clean_starts_indices_bonds = clean_starts_bonds.index.values

        return (clean_starts_stocks, clean_starts_bonds, clean_starts_indices_stocks,
                clean_starts_indices_bonds)

    def update_original(self):
        """Add dummy column denoting Income Statements."""

        self.working_df['stock_rec'] = 0
        for index in self.clean_starts_indices_stocks:
            self.working_df.set_value(index, 'stock_rec', 1)

        self.working_df['bonds_rec'] = 0
        for index in self.clean_starts_indices_bonds:
            self.working_df.set_value(index, 'bonds_rec', 1)

        output_dataframe = self.working_df[['file_name', 'manual', 'manual_yr', 'fiche', 'fiche_num',
                                            'zone_num', 'CoName', 'CoNum', 'Hist', 'Dir', 'stock_rec',
                                            'bonds_rec', 'text']]

        return output_dataframe

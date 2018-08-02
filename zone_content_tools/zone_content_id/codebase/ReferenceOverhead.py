"""Perform operations to find Reference Notes zones."""

import ReferenceOps as ro
import ZoneNeutralOps as zno
import numpy as np
import pandas as pd
import os

pd.options.mode.chained_assignment = None
# pd.set_option('display.max_colwidth', -1)
# pd.set_option('display.max_rows', None)

class reference_overhead(object):

    """
    Container class to construct testing dataframe looking for Reference Notes strings /
    zones. Calls methods from similarly-named Ops module. Filters resulting dummy columns
    in data to define 'Reference Notes' zones with a 1 or 0 score.

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
        self.clean_starts = self.clean_starts_data[0]
        self.clean_starts_indices = self.clean_starts_data[1]
        self.non_clean_start_indices = self.clean_starts_data[2]

        self.on_stocks_clean_indices = self.on_stocks()
        self.on_bonds_clean_indices = self.on_bonds()

        self.output_dataframe = self.update_original()

    def test_stock_bond(self):
        """Search zone content for 'year(s) ended' string."""

        sub_working_df = self.working_df[['file_name', 'text']]
        sub_working_df['zone_next'] = sub_working_df['text']
        sub_working_df['zone_next_next'] = sub_working_df['text']
        sub_working_df.zone_next_next = sub_working_df.zone_next_next.shift(-2)
        sub_working_df = sub_working_df.fillna(value='')

        # sub_working_df['consec_years'] = sub_working_df.apply(zno.test_consec_years, axis=1)
        sub_working_df['caps_reference'] = sub_working_df.text.apply(ro.test_caps_reference)

        return sub_working_df

    def id_clean_starts(self):
        """Identify well-defined income accounts / statements starts."""

        clean_starts = self.sub_working_df.loc[(self.sub_working_df['caps_reference'] == 1)]
        clean_starts_indices = clean_starts.index.values
        non_clean_start_indices = [index for index in self.sub_working_df.index.values if index not in clean_starts_indices]

        return (clean_starts, clean_starts_indices, non_clean_start_indices)

    def on_stocks(self):
        """Search for 'ON STOCKS' string in matched reference note zones."""

        self.sub_working_df['ref_on_stocks'] = self.sub_working_df.text.apply(ro.on_stocks)
        for index in self.non_clean_start_indices:
            self.sub_working_df.set_value(index, 'ref_on_stocks', 0)

        on_stocks_clean_starts = self.sub_working_df.loc[(self.sub_working_df['ref_on_stocks'] == 1)]
        on_stocks_clean_indices = on_stocks_clean_starts.index.values

        return on_stocks_clean_indices

    def on_bonds(self):
        """Search for 'ON BONDS' string in matched reference note zones."""

        self.sub_working_df['ref_on_bonds'] = self.sub_working_df.text.apply(ro.on_bonds)
        for index in self.non_clean_start_indices:
            self.sub_working_df.set_value(index, 'ref_on_bonds', 0)

        on_bonds_clean_starts = self.sub_working_df.loc[(self.sub_working_df['ref_on_bonds'] == 1)]
        on_bonds_clean_indices = on_bonds_clean_starts.index.values

        return on_bonds_clean_indices

    def update_original(self):
        """Add dummy column denoting Income Statements."""

        self.working_df['ref_on_stocks'] = 0
        for index in self.on_stocks_clean_indices:
            self.working_df.set_value(index, 'ref_on_stocks', 1)

        self.working_df['ref_on_bonds'] = 0
        for index in self.on_bonds_clean_indices:
            self.working_df.set_value(index, 'ref_on_bonds', 1)

        output_dataframe = self.working_df[['file_name', 'manual', 'manual_yr', 'fiche', 'fiche_num',
                                            'zone_num', 'CoName', 'CoNum', 'Hist', 'Dir', 'ref_on_stocks',
                                            'ref_on_bonds', 'text']]

        return output_dataframe

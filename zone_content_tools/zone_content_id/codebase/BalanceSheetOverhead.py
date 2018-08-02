"""Perform operations to find Balance Sheet strings / zones."""

import BalanceSheetOps as bso
import ZoneNeutralOps as zno
import numpy as np
import pandas as pd
import os

pd.options.mode.chained_assignment = None
# pd.set_option('display.max_colwidth', -1)
# pd.set_option('display.max_rows', None)

class balance_sheet_overhead(object):

    """

    Attributes:

    zones_full:
    zones_small:
    working_df:
    sub_working_df:

    clean_starts_data: returned data from id_clean_starts()
        clean_starts:
        clean_starts_indices:
        non_clean_start_indices:

    confident_rows_indices:
    output_dataframe:
    """

    def __init__(self, zones_full, zones_small):

        self.zones_full = zones_full
        self.zones_small = zones_small
        self.working_df = zno.file_to_df(self.zones_small)
        self.sub_working_df = self.test_balance_sheet()

        self.clean_starts_data = self.id_clean_starts()
        self.clean_starts = self.clean_starts_data[0]
        self.clean_starts_indices = self.clean_starts_data[1]
        self.non_clean_start_indices = self.clean_starts_data[2]

        self.numbers_density_id()
        self.trailing_colon_id()

        self.confident_rows_indices = self.final_cut()
        self.output_dataframe = self.update_original()

    def test_balance_sheet(self):
        """Search zone content for 'year(s) ended' string."""

        sub_working_df = self.working_df[['file_name', 'text']]
        sub_working_df['zone_next'] = sub_working_df['text']
        sub_working_df.zone_next = sub_working_df.zone_next.shift(-1)
        sub_working_df = sub_working_df.fillna(value='')

        # sub_working_df['consec_years'] = sub_working_df.apply(zno.test_consec_years, axis=1)
        sub_working_df['caps_bal_she'] = sub_working_df.text.apply(bso.test_caps_balance_sheet)
        sub_working_df['balance_sheet'] = sub_working_df.text.apply(bso.test_balance_sheet)

        return sub_working_df

    def id_clean_starts(self):
        """Identify well-defined Balance Sheet starts."""

        clean_starts = self.sub_working_df.loc[(self.sub_working_df['caps_bal_she'] == 1) |
                                               (self.sub_working_df['balance_sheet'] == 1)]

        clean_starts_indices = clean_starts.index.values
        non_clean_start_indices = [index for index in self.sub_working_df.index.values if index not in clean_starts_indices]

        return (clean_starts, clean_starts_indices, non_clean_start_indices)

    def numbers_density_id(self):
        """Search for table-identifying numbers (by density in zone)."""

        self.sub_working_df['table_numbers'] = self.sub_working_df.apply(bso.trailing_number_content, axis=1)
        for index in self.non_clean_start_indices:
            self.sub_working_df.set_value(index, 'table_numbers', 0)

    def trailing_colon_id(self):
        """Identify Balance Sheet strings with indicative trailing puctuation."""

        self.sub_working_df['trailing_colon'] = self.sub_working_df.text.apply(bso.test_trailing_colon)
        for index in self.non_clean_start_indices:
            self.sub_working_df.set_value(index, 'trailing_colon', 0)

    def final_cut(self):
        """Creat view of intermin dataframe with condifent Balance Sheet rows."""

        clean_starts = self.sub_working_df.loc[self.clean_starts_indices, :]
        confident_rows = clean_starts.loc[(clean_starts['table_numbers'] == 1) |
                                          (clean_starts['trailing_colon'] == 1)]

        confident_rows_indices = confident_rows.index.values
        return confident_rows_indices

    def update_original(self):
        """Add dummy column denoting Balance Sheets."""

        self.working_df['bal_sheet'] = 0
        for index in self.confident_rows_indices:
            self.working_df.set_value(index, 'bal_sheet', 1)

        output_dataframe = self.working_df[['file_name', 'manual', 'manual_yr', 'fiche', 'fiche_num',
                                            'zone_num', 'CoName', 'CoNum', 'Hist', 'Dir', 'bal_sheet',
                                            'text']]

        return output_dataframe

"""Perform operations to find end of company 'objects'."""

import EndSearchOps as eso
import ZoneNeutralOps as zno
import numpy as np
import pandas as pd
import os

pd.options.mode.chained_assignment = None
# pd.set_option('display.max_colwidth', -1)
# pd.set_option('display.max_rows', None)

class end_search_overhead(object):

    """
    Container class to construct testing dataframe looking for ends of company objects.
    Calls methods from similarly-named Ops module. Filters resulting dummy columns
    in data to define ends of company zones with a 1 or 0 score.

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
        self.sub_working_df = self.test_provis_rating()

        self.clean_starts_data = self.id_clean_starts()
        self.clean_starts = self.clean_starts_data[0]
        self.clean_starts_indices = self.clean_starts_data[1]
        self.non_clean_start_indices = self.clean_starts_data[2]

        self.corrected_indices = self.company_search()
        self.output_dataframe = self.update_original()

    def test_provis_rating(self):
        """Search zone content for 'provisional ratings' string."""

        sub_working_df = self.working_df[['file_name', 'text']]
        sub_working_df['zone_next'] = sub_working_df['text']
        sub_working_df['zone_next_next'] = sub_working_df['text']
        sub_working_df['zone_next_next_next'] = sub_working_df['text']
        sub_working_df.zone_next = sub_working_df.zone_next.shift(-1)
        sub_working_df.zone_next_next = sub_working_df.zone_next.shift(-2)
        sub_working_df.zone_next_next_next = sub_working_df.zone_next.shift(-3)
        sub_working_df = sub_working_df.fillna(value='')

        sub_working_df['provis_rtng'] = sub_working_df.text.apply(eso.test_provis_rating)
        return sub_working_df

    def id_clean_starts(self):
        """Identify well-defined 'provisional ratings' zones."""

        clean_starts = self.sub_working_df.loc[(self.sub_working_df['provis_rtng'] == 1)]
        clean_starts_indices = clean_starts.index.values
        non_clean_start_indices = [index for index in self.sub_working_df.index.values if index not in clean_starts_indices]

        return (clean_starts, clean_starts_indices, non_clean_start_indices)

    def company_search(self):
        """Search for company-name-identifying strings (by zone and neighbours)."""

        self.sub_working_df['comp_name'] = self.sub_working_df.apply(eso.company_search, axis=1)
        for index in self.non_clean_start_indices:
            self.sub_working_df.set_value(index, 'comp_name', 0)

        resulting_rows = self.sub_working_df.loc[(self.sub_working_df['comp_name'] != 0)]
        resulting_rows = resulting_rows[~resulting_rows.comp_name.isnull()]
        corrected_indices = []
        for name, row in resulting_rows.iterrows():
            shift_value = row['comp_name'] - 1
            corrected_index = name + shift_value
            corrected_indices.append(int(corrected_index))

        return corrected_indices

    def update_original(self):
        """Add dummy column denoting Income Statements."""

        self.working_df['provis_rtng'] = 0
        for index in self.clean_starts_indices:
            self.working_df.set_value(index, 'provis_rtng', 1)

        self.working_df['comp_name'] = 0
        for index in self.corrected_indices:
            self.working_df.set_value(index, 'comp_name', 1)

        output_dataframe = self.working_df[['file_name', 'manual', 'manual_yr', 'fiche', 'fiche_num',
                                            'zone_num', 'CoName', 'CoNum', 'Hist', 'Dir', 'provis_rtng',
                                            'comp_name', 'text']]

        return output_dataframe

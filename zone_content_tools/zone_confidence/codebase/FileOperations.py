"""Read and combine zone logs into single dataframe."""

import pandas as pd
import numpy as np
import os

class file_operations(object):

    """
    Read in zone character confidence and content files and join them as a single
    file in a Pandas dataframe. Perform simple math to develop confidence data about
    pages and the zones within them. Output .csv file with low conf. zones for inspection.

    Attributes:

    aggregate_zone_df: combined data from input files as a single dataframe with
                       with quality scores and zone content.

    page_confidence_df: dataframe containing page confidence scores.
    trimmed_low_confidence_zones: dataframe containing zones with low confidence
                                  under a variable threshold.
    """

    def __init__(self, file_dict):

        self.file_dict = file_dict
        self.aggregate_zone_df = self.read_combine()
        self.page_confidence_df = self.define_page_confidence()
        self.trimmed_low_confidence_zones = self.show_low_confidence_zones()

    def read_combine(self):
        """loop through files, read file in, and combine file contents into single list object."""

        def define_index(page, zone_index_list, i):
            """define dataframe row_index for each zone."""

            # check if page (i.e. Industrial19200003-0001) is in zone_index_list
            if page in zone_index_list:
                i += 1

                # slice page and build dataframe index using i as the zone number (i.e. 1920-0003-0001-3)
                row_index = page[10:14] + '-' + page[14:] + '-' + str(i)

            else:
                # add page to zone_index_list
                zone_index_list.append(page)

                # slice page and build dataframe index using 1 as the zone number (i.e. 1920-0003-0001-1)
                row_index = page[10:14] + '-' + page[14:] + '-' + str(1)

                # reset i value.
                i = 1

            return (row_index, i)

        # predefine columns titles for aggregate_confidence_df.
        columns_confidence = ['filename', 'zone_index', 'count_zones', 'left', 'top', 'right',
                              'bottom', 'total_characters', 'char_conf_yes', 'char_conf_no', 'conf_ratio']

        # declare empty dataframes to be filled (and later joined).
        aggregate_confidence_dict = {}
        aggregate_content_dict = {}

        # loop through files in earlier-defined file path dictionary and extract data.
        for key, file_list in self.file_dict.items():

            # ID paths in dict. value as temp. objects.
            file_zone_confidence = file_list[0]
            file_zone_text = file_list[1]

            # open file containing zone confidence information
            with open(file_zone_confidence, 'r') as file_in_confidence:

                # set beginning values for i and zone_index_list.
                i = 1
                zone_index_list = []

                # loop through lines in file.
                for line in file_in_confidence:

                    # split line string into comma-sep. items and define page.
                    zone = line.rstrip().split(',')
                    page = zone[0]

                    # trigger define_index function and pass returned index forward.
                    index_data = define_index(page, zone_index_list, i)
                    row_index = index_data[0]
                    i = index_data[1]

                    # perform basic math on confidence scores to summarise zone quality.
                    total_characters = sum([int(value) for value in zone[6:]])
                    char_conf_yes = sum([int(value) for value in zone[6:9]])
                    char_conf_no = sum([int(value) for value in zone[9:]])
                    conf_ratio = round(char_conf_yes / (total_characters + .001), 3)

                    # redefine zone using newly-computed values. Update aggregate_confidence_dict with zone.
                    zone = [zone[0]] + [i] + zone[1:6] + [total_characters] + [char_conf_yes] + [char_conf_no] + [conf_ratio]
                    aggregate_confidence_dict.update({row_index:zone})

                # convert aggregate_confidence_dict to dataframe.
                aggregate_confidence_df = pd.DataFrame.from_dict(aggregate_confidence_dict, orient='index')
                aggregate_confidence_df.columns = columns_confidence

                # # show dataframe.
                # display(aggregate_confidence_df)

            with open(file_zone_text, 'r', encoding = 'ISO-8859-1') as file_in_text:

                # set beginning values for i and zone_index_list.
                i = 1
                zone_index_list = []

                # loop through lines in file.
                for line in file_in_text:

                    # split line string into comma-sep. items and define page.
                    zone = line.rstrip().split(',')
                    page = zone[0][12:]

                    # trigger define_index function and pass returned index forward.
                    index_data = define_index(page, zone_index_list, i)
                    row_index = index_data[0]
                    i = index_data[1]

                    # redefine zone and convert zone list to dataframe row.
                    zone = zone[-1]
                    aggregate_content_dict.update({row_index:zone})

                # convert aggregate_content_dict to dataframe.
                aggregate_content_df = pd.DataFrame.from_dict(aggregate_content_dict, orient='index')
                aggregate_content_df.columns = ['zone_content']

                # # show dataframe.
                # display(aggregate_content_df)

        # join aggregate_confidence_df & aggregate_content_df into single dataframe.
        zone_data_df = aggregate_confidence_df.join(aggregate_content_df)

        # # show dataframe.
        # display(zone_data_df)

        return zone_data_df

    def define_page_confidence(self):
        """Create dataframe for page confidence as an aggregate of zones on-page."""

        page_confidence_df = self.aggregate_zone_df.groupby(['filename']).agg({'count_zones':'count',
                             'total_characters':'sum', 'char_conf_yes':'sum', 'char_conf_no':'sum'})

        page_confidence_df['page_confidence'] = round(page_confidence_df['char_conf_yes'] / (page_confidence_df['total_characters'] + .001), 3)
        return page_confidence_df

    def show_low_confidence_zones(self):
        """Filter aggregate_zone_df to display zones with low confidence."""

        # set confidence boundary (for the time at .90).
        low_confidence_zones = self.aggregate_zone_df[self.aggregate_zone_df.conf_ratio < .90]
        trimmed_low_confidence_zones = low_confidence_zones[['filename', 'count_zones', 'zone_index', 'conf_ratio', 'zone_content']]

        # trim page_confidence_df to only show the page confidence value.
        page_confidence_df_trimmed = self.page_confidence_df[['page_confidence']]

        # combine dataframes to add page confidence column to trimmed_low_confidence_zones.
        trimmed_low_confidence_zones = trimmed_low_confidence_zones.join(page_confidence_df_trimmed, on='filename', how='left')
        trimmed_low_confidence_zones = trimmed_low_confidence_zones[['filename', 'page_confidence', 'count_zones', 'zone_index', 'conf_ratio', 'zone_content']]

        # # show dataframe.
        # display(trimmed_low_confidence_zones)

        # export dataframe as .csv file.
        save_name = 'low_confidence_zones.csv'
        out_path = os.getcwd()[:-8] + save_name
        trimmed_low_confidence_zones.to_csv(out_path, index=False)

        return trimmed_low_confidence_zones

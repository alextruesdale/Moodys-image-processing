"""Operate on pages in manual; extract data from zones and print to examination file."""

from operator import itemgetter
import xmlStaticOperators
import xmlChildSearch
import xmlTableZoneExpander
import os

class xmlTableIdentifier(object):

    """
    Identify two-column pages, search them for table zones and textzones that
    appear to be falsely zoned. Trigger sub-classes to extract data or operate further.

    Attributes:

    year: string value for manual year.
    out_path: incoming out path for saved data.
    zones_dictionary: incoming zone data dictionary object.
    page_data: incoming page data dictionary object.
    line_data: income line data dictionary object.
    table_aggregate_data: counter and modified table data used at for higher level classes.
    """

    def __init__(self, year, data_out_path, manual_zones_dictionary, page_data, line_data):

        self.year = '19' + year
        self.out_path = data_out_path
        self.zones_dictionary = manual_zones_dictionary
        self.page_data = page_data
        self.line_data = line_data
        self.create_manual_directory()
        self.table_aggregate_data = self.identify_tables()
        self.recursive_empty_directory_clean()

    def create_manual_directory(self):
        """Create save directory for page zone data."""

        xmlStaticOperators.clear_destination(self.out_path)
        os.mkdir(self.out_path)

    def recursive_empty_directory_clean(self):
        """Clean out empty directories to avoid saving conflicts."""

        for root, dirnames, filenames in os.walk(self.out_path, topdown = False):
            for dir in dirnames:
                try:
                    os.rmdir(os.path.join(root, dir))
                except:
                    pass

    @staticmethod
    def manual_begin_end(year, page_index):
        """Define beginning and endpoints of manual in terms of areas to search."""

        manual_begin_end_dict = {
            '1920': [[-1, False], [133, True], [1513, False]],
            '1921': [[-1, False], [158, True], [1751, False]],
            '1922': [[-1, False], [193, True], [2077, False]],
            '1923': [[-1, False], [159, True], [2414, False]],
            '1924': [[-1, False], [310, True], [2878, False]],
            '1925': [[-1, False], [225, True], [2405, False]],
            '1926': [[-1, False], [270, True], [2665, False]],
            '1927': [[-1, False], [306, True], [3057, False]],
            '1928': [[-1, False], [348, True], [3425, False]],
            '1929': [[-1, False], [391, True], [3485, False]]
        }

        # Identify nearest neighbour to page ID based on above dictionary;
        # subtract bounds above from page index and find smallest non-zero value.

        difference_list = sorted([[item, page_index - item[0]] for item in
                                  manual_begin_end_dict[year] if page_index - item[0] > 0],
                                  key=itemgetter(1))

        begin_end_value = difference_list[0][0][1]
        return begin_end_value

    def create_page_directory(self, page):
        """Create save directory for page zone data."""

        # slice page path string and reconstruct for output (both dir. and filename).
        output_directory_fiche = page[-9:-5]
        output_directory_fiche_path = os.path.join(self.out_path, output_directory_fiche)
        if not os.path.exists(output_directory_fiche_path):
            os.mkdir(output_directory_fiche_path)

        output_directory_page = page[-4:]
        return (output_directory_fiche_path, output_directory_fiche, output_directory_page)

    def define_column_width(self, page):
        """Define width of columns against which to measure tables."""

        page_columns = len(self.line_data[page][:-1][0].keys())
        page_data = self.page_data[page]
        if page_columns == 1:
            column_width = page_data.page_width
        elif page_columns == 2:
            column_width = page_data.page_width / 2
        elif page_columns == 3:
            column_width = page_data.page_width / 3

        return (page_columns, column_width)

    def define_content_height(self, page):
        """Identify top of page content"""

        # define in-function inputs.
        column_top_dict = {}
        column_bottom_dict = {}
        line_data = self.line_data[page][0]
        top_average = 0
        bottom_average = 0

        # loop through columns on page and define highest and lowest lines.
        for index, column in line_data.items():

            # define list of word objects in each line respectively.
            top_row = column[max(column)]
            bottom_row = column[min(column)]

            # define highest high and lowest low of top and bottom rows.
            column_top = max([word[1] for word in top_row])
            column_bottom = min([word[1] for word in bottom_row])

            # add column values to average top/bottom aggregates.
            top_average += column_top
            bottom_average += column_bottom

            # update top/bottom dicts with top/bottom values for column.
            column_top_dict.update({index: column_top})
            column_bottom_dict.update({index: column_bottom})

        # take averages of the column tops and bottoms to define rough page values.
        top_average = top_average / len(column_top_dict) + .005
        bottom_average = bottom_average / len(column_bottom_dict) - .015
        return (column_top_dict, column_bottom_dict, top_average, bottom_average)

    def identify_tables(self):
        """Identify tableZones from collective zone data; trigger stripping class."""

        # define counters and object(s) to be returned.
        manual_fullwidth_table_count = 0
        manual_fullwidth_ideal_table_count = 0
        table_keys_aggregate = []
        modified_pages = {}

        # loop through all pages in manual and trigger appropriate submodule operations.
        for i, (page, data) in enumerate(self.zones_dictionary.items()):

            # return T or F value for whether this page should be operated upon.
            manual_operate_key = xmlTableIdentifier.manual_begin_end(self.year, i)

            if manual_operate_key:

                # run above-defined functions and link returned objects to new locals.
                output_directory_data = self.create_page_directory(page)
                page_column_data = self.define_column_width(page)
                define_content_height = self.define_content_height(page)
                columns = page_column_data[0]
                column_width = page_column_data[1]
                top_average = define_content_height[2]
                bottom_average = define_content_height[3]

                # determine 2-column pages; if True, trigger further conditions.
                if columns > 1:

                    # loop through zones on page; define zone width and filter on zone type.
                    for zone in data:
                        zone_width = zone[2] - zone[4]
                        if zone[0] == 'tableZone':

                            # check if zone is column-width or a fraction thereof.
                            if column_width - .015 < zone_width < column_width + .03:
                                manual_fullwidth_table_count += 1

                                # define the ElementTree object from the zone object.
                                zone_element = zone[5]

                                # trigger class to ID whether the table structure is clean or not.
                                element_data = xmlChildSearch.xmlChildSearch(output_directory_data,
                                                                             zone_element)

                                if element_data.clean_table:
                                    manual_fullwidth_ideal_table_count += 1
                                    for key in element_data.table_keys:
                                        table_keys_aggregate.append(key)

                        # check if zone is partial-width and that it is within text bounds
                        # defined by self.define_content_height.

                        if (zone_width < column_width - .015 and zone[3] > bottom_average and
                            (zone[1] < top_average or zone[3] < top_average) and
                            (zone[0] == 'tableZone' or zone[0] == 'textZone')):

                            # check if a previous zone on this page has been modified. If yes,
                            # continue with the zones dictionary value from the updated dict.

                            # This will include the expanded zone that has been previously modified
                            # as well as no longer having removed zones to eliminate duplicating work.

                            if page in modified_pages.keys():
                                data = modified_pages[page][1]

                                # if zone has been deleted, skip loop iteration.
                                if zone not in data:
                                    continue

                            # trigger xmlTableZoneExpander class and define output.
                            modified_page = xmlTableZoneExpander.xmlTableZoneExpander(page, self.page_data[page],
                                                                                      columns, output_directory_data,
                                                                                      zone, data, define_content_height)

                            # Mirror and update modified pages dict as similar to original page zone dicitionary.
                            # (will be used to print page PDFs of only pages with modified / updated zones).

                            page_data = self.page_data[page]
                            modified_pages.update({page:[[page_data.page_dimensions[0],
                                                          page_data.page_dimensions[1]],
                                                          modified_page.page_zone_data]})

        return(manual_fullwidth_table_count, manual_fullwidth_ideal_table_count, table_keys_aggregate, modified_pages)

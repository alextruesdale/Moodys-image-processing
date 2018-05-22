"""Further parse tableZones for data."""

import xml.etree.ElementTree as ET
import xmlTableStripper
import xmlStaticOperators
import pandas as pd
import os

class xmlChildSearch(object):

    def __init__(self, output_directory_data, zone_element):

        self.out_path = output_directory_data[0]
        self.out_fiche = output_directory_data[1]
        self.out_page = output_directory_data[2]
        self.zone_element = zone_element
        self.clean_table = self.ideal_table_check()
        self.child_search()
        self.identify_bounds()

        if self.clean_table:
            self.table_keys = self.table_strip()

    def ideal_table_check(self):
        """Discern 'purity' of table from cellZoning."""

        clean_table = False
        cell_clean_values = []
        for cell in self.zone_element.findall('.//cellZone'):
            count_lines = 0
            for child in cell.iter():
                if child.tag == 'ln':
                    count_lines += 1

            if count_lines == 0 or count_lines == 1:
                cell_clean = True
            else:
                cell_clean = False

            cell_clean_values.append(cell_clean)

        if all(cell_clean_values):
            clean_table = True

        return clean_table

    def child_search(self):
        """Create data output from zone_element data."""

        def save_table_data(clean_table, full, out_path, out_fiche, out_page, table_words):
            """Save words in xml tableZones as text files."""

            save_path = xmlStaticOperators.find_unique_id(clean_table, full, out_path, out_fiche,
                                                          out_page, 'word_data', 'txt')

            delimiter = '\n'
            with open(save_path, 'a') as out_file:
                out_file = out_file.write(delimiter.join(table_words))

        table_words = []
        for word in self.zone_element.findall('.//wd'):
            word.text = xmlStaticOperators.none_to_empty(word.text)
            table_words.append(word.text)

        save_table_data(self.clean_table, True, self.out_path, self.out_fiche,
                        self.out_page, table_words)

    def identify_bounds(self):
        """Identify x1, x2, y1, y2 coordinates for table; save as .csv."""

        pixel_coordinates = {}
        twip_coordinates = {}
        root = self.zone_element

        pixel_coordinates['t_pixel'] = float('{:.5f}'.format(((int(root.get('t')) * 400) / 1440)))
        pixel_coordinates['r_pixel'] = float('{:.5f}'.format(((int(root.get('r')) * 400) / 1440)))
        pixel_coordinates['b_pixel'] = float('{:.5f}'.format(((int(root.get('b')) * 400) / 1440)))
        pixel_coordinates['l_pixel'] = float('{:.5f}'.format(((int(root.get('l')) * 400) / 1440)))

        twip_coordinates['t_twip'] = root.get('t')
        twip_coordinates['r_twip'] = root.get('r')
        twip_coordinates['b_twip'] = root.get('b')
        twip_coordinates['l_twip'] = root.get('l')

        pixel_coordinates_series = pd.Series(pixel_coordinates, index = pixel_coordinates.keys())
        twip_coordinates_series = pd.Series(twip_coordinates, index = twip_coordinates.keys())

        xmlStaticOperators.data_to_csv(pixel_coordinates_series, self.clean_table, True, self.out_path,
                                       self.out_fiche, self.out_page, False, True, 'coordinates_pixel')

        xmlStaticOperators.data_to_csv(twip_coordinates_series, self.clean_table, True, self.out_path,
                                       self.out_fiche, self.out_page, False, True, 'coordinates_twip')

    def table_strip(self):
        """Instantiate table stripping class."""

        table_data = xmlTableStripper.xmlTableStripper(self.out_path, self.out_fiche,
                                                       self.out_page, self.zone_element)
        return table_data.table_keys

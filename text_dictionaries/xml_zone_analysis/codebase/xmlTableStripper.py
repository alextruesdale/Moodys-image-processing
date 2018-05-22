"""Strip ideal tables and create .csv charts from them."""

import pandas as pd
import xmlStaticOperators
import xml.etree.ElementTree as ET

class xmlTableStripper(object):

    def __init__(self, out_path, out_fiche, out_page, zone_element):

        self.out_path = out_path
        self.out_fiche = out_fiche
        self.out_page = out_page
        self.zone_element = zone_element
        self.grid_dimensions = self.define_table_structure()
        self.table_dataframe = self.create_pandas_dataframe()
        self.table_cell_dictionary = self.strip_table_data()
        self.table_keys = self.populate_data_frame()

    def define_table_structure(self):
        """Identify table structure via <gridTable> tag contents."""

        count_columns = 0
        count_rows = 0
        grid_table = self.zone_element.find('.//gridTable')
        for dimension in grid_table.iter():
            if dimension.tag == 'gridCol':
                count_columns += 1
            elif dimension.tag == 'gridRow':
                count_rows += 1

        grid_dimensions = [count_columns, count_rows]
        return grid_dimensions

    def create_pandas_dataframe(self):
        """Create DataFrame shell based on ID'd table structure."""

        columns = list(range(0, self.grid_dimensions[0]))
        rows = list(range(0, self.grid_dimensions[1]))
        df_shell = pd.DataFrame(index=rows, columns=columns)

        return df_shell

    def strip_table_data(self):
        """Strip cell data using <gridColumn> and <gridRow> data."""

        table_cell_dictionary = {}
        for i, cell in enumerate(self.zone_element.findall('.//cellZone')):
            cell_data = []
            cell_column = cell.get('gridColFrom')
            cell_row = cell.get('gridRowFrom')
            for child in cell.iter():
                if child.tag == 'wd':
                    child.text = xmlStaticOperators.none_to_empty(child.text)
                    cell_data.append(child.text)

            cell_data = ' '.join(cell_data)
            table_cell_dictionary.update({i:[cell_column, cell_row, cell_data]})

        return table_cell_dictionary

    def populate_data_frame(self):
        """Populate DataFrame cell with stripped data"""

        table_keys = []
        for value in self.table_cell_dictionary.values():
            column = int(value[0])
            row = int(value[1])
            cell_value = value[2]
            self.table_dataframe.at[row, column] = cell_value
            if column == 0:
                table_keys.append(cell_value)

        xmlStaticOperators.data_to_csv(self.table_dataframe, True, True, self.out_path, self.out_fiche,
                                       self.out_page, False, False, 'table_as_csv')
        return table_keys

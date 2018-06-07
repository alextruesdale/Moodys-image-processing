"""Expand table zones of incomplete tables to include fractured textZones in their immediate area."""

from xmlTableAbsorption import xmlTableAbsorption
import xml.etree.ElementTree as ET
import pandas as pd
import xmlStaticOperators

class xmlTableZoneExpander(object):

    def __init__(self, page, page_data, columns, output_directory_data, zone_list, page_zone_data, define_content_height):

        self.page = page
        print(self.page)

        self.columns = columns
        self.page_data = page_data

        self.output_directory_data = output_directory_data
        self.zone_list = zone_list
        self.page_zone_data = page_zone_data
        self.column_top_dict = define_content_height[0]
        self.column_bottom_dict = define_content_height[1]

        self.column_zones = self.identify_zone_column()
        self.column_id = self.column_zones[0]
        self.working_zones = self.column_zones[1]
        self.column_zones_total = self.column_zones[2]
        self.column_width_data = self.exclude_titles()
        self.column_width = self.column_width_data[0]
        self.left_edge = self.column_width_data[1]
        self.right_edge = self.column_width_data[2]

        if not self.pitch_text_zone_list():
            self.column_bounds = self.identify_bounding_neighbours()
            self.top_bound = self.column_bounds[0]
            self.bottom_bound = self.column_bounds[1]
            self.identify_neighbours()
            self.identify_incomplete_text_zones()

            if len(self.working_zones) > 0:
                self.pixel_coordinates = self.zone_absorption()
                self.overwrite_original_table_coordinates()

            if len(self.working_zones) > 1 and not self.same_zone_check():
                self.convert_pixels()
                self.convert_twips()
                table_absorption = xmlTableAbsorption(self.zone_list, self.working_zones,
                                                      self.page_zone_data, self.page_data,
                                                      self.column_zones_total)

                self.page_zone_data = table_absorption.page_zone_data

            else:
                print('single zone:', self.page)

    def identify_zone_column(self):
        """ID which column the table object is in."""

        working_zones = []
        offset_01 = .015
        offset_02 = .005

        if self.columns == 2:
            horizontal_center = self.page_data.center
            if self.zone_list[4] < horizontal_center - offset_01:
                column_id = 1

            elif self.zone_list[2] > horizontal_center + offset_01:
                column_id = 2

            for zone in self.page_zone_data:
                if zone[0] == 'textZone' or zone[0] == 'tableZone':
                    if (column_id == 1 and zone[2] < horizontal_center + offset_01 and
                        zone[4] > self.page_data.page_left - offset_02 or zone is self.zone_list):

                        working_zones.append(zone)

                    elif (column_id == 2 and zone[4] > horizontal_center - offset_01 and
                          zone[2] < self.page_data.page_right + offset_02 or zone is self.zone_list):

                        working_zones.append(zone)

        elif self.columns == 3:
            column_center_01 = self.page_data.third_first
            column_center_02 = self.page_data.third_second

            if self.zone_list[4] < column_center_01 - offset_01:
                column_id = 1

            elif (self.zone_list[2] < column_center_02 + offset_01 and
                  self.zone_list[4] > column_center_01 - offset):

                column_id = 2

            elif self.zone_list[2] > column_center_02 + offset_01:
                column_id = 3

            for zone in self.page_zone_data:
                if zone[0] == 'textZone' or zone[0] == 'tableZone':
                    if (column_id == 1 and zone[2] < column_center_01 + offset_01 and
                        zone[4] > self.page_data.page_right - offset_02 or zone is self.zone_list):

                        working_zones.append(zone)

                    elif (column_id == 2 and zone[2] < column_center_02 + offset_01 and
                          zone[4] > column_center_01 - offset or zone is self.zone_list):

                        working_zones.append(zone)

                    elif (column_id == 3 and zone[4] > column_center_02 - offset_01 and
                          zone[2] < self.page_data.page_right + offset_02 or zone is self.zone_list):

                        working_zones.append(zone)

        column_zones = working_zones
        return (column_id, working_zones, column_zones)

    def exclude_titles(self):
        """Remove table title textZones from working zones."""

        def edge_of_column_members(members, key):
            """Define edge of column members (as opposed to mathematically column edges)."""

            edge_list = []
            if key == 'left':
                dimension_index = 4
            elif key == 'right':
                dimension_index = 2

            for member in members:
                if member[0] != 'tableZone' and abs(member[2] - member[4]) > .13:
                    edge_list.append(member[dimension_index])

            if not edge_list:
                if abs(member[2] - member[4]) > .13:
                    edge_list.append(member[dimension_index])

            if key == 'left':
                edge_list = sorted(edge_list)
            elif key == 'right':
                edge_list = sorted(edge_list, reverse = True)

            edge = edge_list[0]
            return edge

        def define_edge_two_column(column_id, working_zones, page_data):
            """Define column bounds for two column column."""

            if column_id == 1:
                left_edge = page_data.page_left
                right_edge = edge_of_column_members(working_zones, 'right')

            elif column_id == 2:
                left_edge = edge_of_column_members(working_zones, 'left')
                right_edge = page_data.page_right

            return (left_edge, right_edge)

        def define_edge_three_column(column_id, working_zones, page_data):
            """Define column bounds for three column column."""

            if column_id == 1:
                left_edge = page_data.page_left
                right_edge = edge_of_column_members(working_zones, 'right')

            elif column_id == 2:
                left_edge = edge_of_column_members(working_zones, 'left')
                right_edge = edge_of_column_members(working_zones, 'right')

            elif column_id == 3:
                left_edge = edge_of_column_members(working_zones, 'left')
                right_edge = page_data.page_right

            return (left_edge, right_edge)

        if self.columns == 2:
            edges = define_edge_two_column(self.column_id, self.working_zones, self.page_data)
        elif self.columns == 3:
            edges = define_edge_three_column(self.column_id, self.working_zones, self.page_data)

        left_edge = edges[0]
        right_edge = edges[1]
        column_width = abs(right_edge - left_edge)

        working_zones = [zone for zone in self.working_zones if
                         abs(abs(zone[4] - left_edge) - abs(right_edge - zone[2])) > .0075
                         or abs(zone[2] - zone[4]) >= column_width - .004]

        self.working_zones = working_zones
        return (column_width, left_edge, right_edge)

    def pitch_text_zone_list(self):
        """Cancel process if errant text zone."""

        pitch_text_zone_list = False
        if self.zone_list[2] > self.right_edge + .01 or self.zone_list[4] < self.left_edge - .01:
            pitch_text_zone_list = True

        return pitch_text_zone_list

    def identify_bounding_neighbours(self):
        """Find bounding neighbouring zones."""

        table_zone_top = self.zone_list[1]
        table_zone_bottom = self.zone_list[3]

        neighbour_bottom_check_dict = {}
        neighbour_top_check_dict = {}
        for zone in self.working_zones:
            zone_width = abs(zone[2] - zone[4])
            if zone_width >= self.column_width - .005 and zone is not self.zone_list:
                bottom_difference = zone[3] - table_zone_bottom
                if bottom_difference > 0:
                    neighbour_bottom_check_dict.update({bottom_difference: zone})
                top_difference = table_zone_top - zone[1]
                if top_difference > 0:
                    neighbour_top_check_dict.update({top_difference: zone})

        top_bound = self.page_data.page_top
        if neighbour_bottom_check_dict:
            closest_neighbour = neighbour_bottom_check_dict[min(neighbour_bottom_check_dict)]
            zone_height_interim = abs(closest_neighbour[1] - closest_neighbour[3]) / 2
            top_bound = closest_neighbour[3] + zone_height_interim

        bottom_bound = self.page_data.page_bottom - .01
        if neighbour_top_check_dict:
            closest_neighbour = neighbour_top_check_dict[min(neighbour_top_check_dict)]
            zone_height_interim = abs(closest_neighbour[1] - closest_neighbour[3]) / 2
            bottom_bound = closest_neighbour[1] - zone_height_interim

        return(top_bound, bottom_bound)

    def identify_neighbours(self):
        """Find all neighbouring zones."""

        working_zones = [zone for zone in self.working_zones if zone[1] < self.top_bound
                         and zone[3] > self.bottom_bound or zone is self.zone_list]

        self.working_zones = working_zones

    def identify_incomplete_text_zones(self):
        """Identify incomplete neighbouring textZones."""

        def identify_same_zone_table(zone):
            """Identify neighbouring same-zone tables."""

            same_zone_table = False
            if len(zone) == 7:
                if (zone[1] >= self.zone_list[1] and zone[2] >= self.zone_list[2]
                    and zone[3] <= self.zone_list[3] or zone[4] <= self.zone_list[4]):

                    same_zone_table = True

            return same_zone_table

        working_zones = [zone for zone in self.working_zones if
                         abs(zone[2] - zone[4]) <= self.column_width - .005
                         or zone is self.zone_list or identify_same_zone_table(zone)]

        self.working_zones = working_zones

    def zone_absorption(self):
        """Collect neighbouring incomplete textZones along with table object;
           ID max and min coordinates for expanded tableZone."""

        top_list = []
        right_list = []
        bottom_list = []
        left_list = []
        pixel_coordinates = {}

        for zone in self.working_zones:
            top_list.append(zone[1])
            right_list.append(zone[2])
            bottom_list.append(zone[3])
            left_list.append(zone[4])

        offset = .005
        if max(top_list) > self.column_top_dict[self.column_id - 1] + offset:
            pixel_coordinates['t_pixel'] = self.column_top_dict[self.column_id - 1] + offset
        else:
            pixel_coordinates['t_pixel'] = max(top_list)

        if max(right_list) > self.right_edge + offset:
            pixel_coordinates['r_pixel'] = self.right_edge + offset
        else:
            pixel_coordinates['r_pixel'] = max(right_list)

        if min(bottom_list) < self.column_bottom_dict[self.column_id - 1] - 2 * offset:
            pixel_coordinates['b_pixel'] = self.column_bottom_dict[self.column_id - 1] - 2 * offset
        else:
            pixel_coordinates['b_pixel'] = min(bottom_list)

        if min(left_list) < self.left_edge - offset:
            pixel_coordinates['l_pixel'] = self.left_edge - offset
        else:
            pixel_coordinates['l_pixel'] = min(left_list)

        return pixel_coordinates

    def same_zone_check(self):
        """Determine if tableZone already exists on page."""

        same_zone_check = False
        for zone in self.page_zone_data:
            if zone is self.zone_list:
                pass

            elif zone[0] == 'tableZone':
                if (self.zone_list[1] == zone[1] and self.zone_list[2] == zone[2] and
                    self.zone_list[3] == zone[3] and self.zone_list[4] == zone[4]):
                        same_zone_check = True

        return same_zone_check

    def overwrite_original_table_coordinates(self):
        """Replace original table coordinates with new ones."""

        for zone in self.page_zone_data:
            if zone is self.zone_list:
                self.zone_list[1] = self.pixel_coordinates['t_pixel']
                self.zone_list[2] = self.pixel_coordinates['r_pixel']
                self.zone_list[3] = self.pixel_coordinates['b_pixel']
                self.zone_list[4] = self.pixel_coordinates['l_pixel']

                if not self.same_zone_check():
                    zone[0] = 'tableZone'
                    zone[1] = self.pixel_coordinates['t_pixel']
                    zone[2] = self.pixel_coordinates['r_pixel']
                    zone[3] = self.pixel_coordinates['b_pixel']
                    zone[4] = self.pixel_coordinates['l_pixel']
                    zone.append('modifiedZone')

    def convert_pixels(self):
        """Convert tableZone coordinates to output-able pixels."""

        width = self.page_data.page_dimensions[0]
        height = self.page_data.page_dimensions[1]

        pixel_coordinates_out = {}
        pixel_coordinates_out['t_pixel'] = self.pixel_coordinates['t_pixel'] * height
        pixel_coordinates_out['r_pixel'] = self.pixel_coordinates['r_pixel'] * width
        pixel_coordinates_out['b_pixel'] = self.pixel_coordinates['b_pixel'] * height
        pixel_coordinates_out['l_pixel'] = self.pixel_coordinates['l_pixel'] * width

        pixel_coordinates_series = pd.Series(pixel_coordinates_out, index = pixel_coordinates_out.keys())
        xmlStaticOperators.data_to_csv(pixel_coordinates_series, False, False,
                                       self.output_directory_data[0], self.output_directory_data[1],
                                       self.output_directory_data[2], False, True, 'coordinates_pixel')

    def convert_twips(self):
        """Convert tableZone coordinates back to twips."""

        twip_coordinates = {}
        coordinates_twip = []
        for i, bound in enumerate(self.pixel_coordinates.values()):
            if i == 1 or i == 3:
                width = self.page_data.page_dimensions[0]
                twip = round((bound * width * 1440) / 400, 0)
                coordinates_twip.append(twip)
            elif i == 0 or i == 2:
                height = self.page_data.page_dimensions[1]
                twip = round(((1 - bound) * height * 1440) / 400, 0)
                coordinates_twip.append(twip)

        twip_coordinates['t_twip'] = coordinates_twip[0]
        twip_coordinates['r_twip'] = coordinates_twip[1]
        twip_coordinates['b_twip'] = coordinates_twip[2]
        twip_coordinates['l_twip'] = coordinates_twip[3]

        twip_coordinates_series = pd.Series(twip_coordinates, index = twip_coordinates.keys())
        xmlStaticOperators.data_to_csv(twip_coordinates_series, False, False,
                                       self.output_directory_data[0], self.output_directory_data[1],
                                       self.output_directory_data[2], False, True, 'coordinates_twip')

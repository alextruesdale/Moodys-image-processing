"""Dynamic identification of patterns on page based on word positions."""

from operator import itemgetter
import numpy as np

class LineSearch(object):

    def __init__(self, page, data):

        self.page = page
        self.word_data = data[0]

        self.page_top = data[1][0]
        self.page_right = data[1][1]
        self.page_bottom = data[1][2]
        self.page_left = data[1][3]
        self.width_difference = round(abs(self.page_left - self.page_right), 2)

        self.word_dict = self.create_page_word_objects()
        self.lines_list_v = self.vertical_line_search()
        self.lines_list_h = self.rolling_lines_identifier()
        self.consolidate_lines()
        self.remove_intersecting_lines()
        self.remove_intersecting_words()
        self.reindex_zones()
        self.zones_on_page = self.collect_zone_and_words()


    def create_page_word_objects(self):
        """Structure word data in sheet."""

        word_list = sorted([[i, word[0], word[1], word[2], word[3], word[4]] for i, word in
                             enumerate(self.word_data) if (word[2] >= self.page_left and
                             word[4] <= self.page_right and word[1] >= self.page_bottom and
                             word[3] <= self.page_top)], key = itemgetter(4))

        word_dict = {word[0]: [word[1], word[2], word[3], word[4], word[5]] for word in word_list}
        return word_dict

    def vertical_line_search(self):
        """Search page on 1/3 and 2/3 points for continuous right-alligned word groups."""

        def match_list_check(x, match_list):
            """Identify continuous segments and store as sub-lists."""

            new_list_out = []
            new_list_out_list = []
            column_index = 1
            for i, word in enumerate(match_list):
                if i == len(match_list) - 2:
                    if (abs(match_list[i][2] - x) < .0075 and abs(match_list[i+1][2] - x) < .0075
                        and abs(match_list[i-1][2] - x) < .0075):

                        new_list_out.append(match_list[i])

                    else:
                        if len(new_list_out) >= 2:
                            new_list_out_list.append([column_index] + new_list_out)
                            column_index += 1

                        new_list_out = []

                elif i == len(match_list) - 1:
                    if (abs(match_list[i][2] - x) < .0075 and abs(match_list[i-1][2] - x) < .0075
                        and abs(match_list[i-2][2] - x) < .0075):

                        new_list_out.append(match_list[i])
                        new_list_out_list.append([column_index] + new_list_out)
                        column_index += 1
                        new_list_out = []

                    else:
                        if len(new_list_out) >= 2:
                            new_list_out_list.append([column_index] + new_list_out)
                            column_index += 1

                        new_list_out = []

                else:
                    if (abs(match_list[i][2] - x) < .0075 and abs(match_list[i+1][2] - x) < .0075
                        and abs(match_list[i+2][2] - x) < .0075):

                        new_list_out.append(match_list[i])

                    elif (abs(match_list[i][2] - x) < .0075 and abs(match_list[i-1][2] - x) < .0075
                          and abs(match_list[i-2][2] - x) < .0075):

                        new_list_out.append(match_list[i])

                    else:
                        if len(new_list_out) >= 2:
                            new_list_out_list.append([column_index] + new_list_out)
                            column_index += 1

                        new_list_out = []

            return new_list_out_list

        print(self.page, '\n', 'Starting word search...')
        x_third_one = np.linspace(self.page_left + (self.width_difference / 3) - .0055, self.page_left + (self.width_difference / 3) + .0025, 4)
        x_third_two = np.linspace(self.page_left + ((self.width_difference / 3) * 2) - .0055, self.page_left + ((self.width_difference / 3) * 2) + .0025, 4)
        x_list = []
        x_list.extend(x_third_one)
        x_list.extend(x_third_two)
        lines_list = []
        for x in x_list:
            x_component = {}
            match_list = []
            for i, word in self.word_dict.items():
                if (abs(word[2] - x) < .0075 or word[4] < x < word[2]) and len(word[0]) > 0:
                    match_list.append(self.word_dict[i])

            if match_list:
                match_list = sorted(match_list, key=itemgetter(3))
                match_list = match_list_check(x, match_list)

                if match_list:
                    for sub_list in match_list:
                        key = np.mean([word[2] for word in sub_list[1:]])
                        if key in x_component.keys():
                            x_component[key].append([[min([word[3] for word in sub_list[1:]]) - .008,
                                                      max([word[1] for word in sub_list[1:]]) + .008],
                                                      sub_list])

                        else:
                            x_component.update({key: [[[min([word[3] for word in sub_list[1:]]) - .008,
                                                        max([word[1] for word in sub_list[1:]]) + .008],
                                                        sub_list]]})
            else:
                continue

            if x_component:
                lines_list.append(x_component)

        return lines_list

    def rolling_lines_identifier(self):
        """Scan page matrix for contiguous vertical and horizontal segments."""

        lines_list = []
        registered_indeces = []
        lines_dict_component = {}
        sub_list = []
        column_list = list(self.word_dict.items())
        for i, word in enumerate(column_list):
            word_index = column_list[i][0]
            coordinate = column_list[i][1][3]
            offset = .00478

            if i == len(column_list) - 1:
                prev_coordinate = column_list[i-1][1][3]
                if prev_coordinate - offset < coordinate < prev_coordinate + offset:
                    sub_list.append([word_index, coordinate])
                    registered_indeces.append(word_index)

                if len(sub_list) >= 3:
                    sub_list_words = sorted([self.word_dict[item[0]] for item in sub_list], key=itemgetter(3))
                    lines_dict_component.update({np.mean([item[1] for item in sub_list]):
                                                 [[min([word[4] for word in sub_list_words]),
                                                   max([word[2] for word in sub_list_words])],
                                                   sub_list_words]})
                    sub_list = []

            else:
                next_coordinate = column_list[i+1][1][3]
                prev_coordinate = column_list[i-1][1][3]

                if next_coordinate - offset < coordinate < next_coordinate + offset:
                    sub_list.append([word_index, coordinate])
                    registered_indeces.append(word_index)

                else:
                    if prev_coordinate - offset < coordinate < prev_coordinate + offset:
                        sub_list.append([word_index, coordinate])
                        registered_indeces.append(word_index)

                    if len(sub_list) >= 3:
                        sub_list_words = sorted([self.word_dict[item[0]] for item in sub_list], key=itemgetter(3))
                        lines_dict_component.update({np.mean([item[1] for item in sub_list]):
                                                     [[min([word[4] for word in sub_list_words]),
                                                       max([word[2] for word in sub_list_words])],
                                                       sub_list_words]})
                        sub_list = []

        for item in sub_list:
            registered_indeces.remove(item[0])

        lines_list.append(lines_dict_component)
        words_excluded = [word for index, word in self.word_dict.items() if index not in registered_indeces]

        return lines_list

    def consolidate_lines(self):
        """Consolidate line near-neighbours and duplicates."""

        min_max_dict = {
            1: {},
            2: {}
        }

        for line_dict in self.lines_list_v:
            for line_index, value in line_dict.items():
                on_page_index = value[0][1][0]
                min_max = value[0][0]
                if self.page_left + (self.width_difference / 3) - .07 < line_index < self.page_left + (self.width_difference / 3) + .07:
                    line_difference = abs(min_max[0] - min_max[1])
                    if on_page_index in min_max_dict[1].keys():
                        min_max_dict[1][on_page_index].update({line_index: line_difference})
                    else:
                        min_max_dict[1][on_page_index] = {line_index: line_difference}

                elif self.page_left + ((self.width_difference / 3) * 2) - .07 < line_index < self.page_left + ((self.width_difference / 3) * 2) + .07:
                    line_difference = abs(min_max[0] - min_max[1])
                    if on_page_index in min_max_dict[2].keys():
                        min_max_dict[2][on_page_index].update({line_index: line_difference})
                    else:
                        min_max_dict[2][on_page_index] = {line_index: line_difference}

        min_max_list = []
        for column_dict in min_max_dict.values():
            for member_dict in column_dict.values():
                min_max_list.append(max(member_dict, key = member_dict.get))

        dict_out = []
        keys_in = []
        for line_dict in self.lines_list_v:
            if list(line_dict.keys())[0] not in keys_in and list(line_dict.keys())[0] in min_max_list:
                keys_in.append(list(line_dict.keys())[0])
                dict_out.append(line_dict)

        self.lines_list_v = dict_out

    def remove_intersecting_lines(self):
        """Remove horizontal lines in supposed three-column zones."""

        min_max_list = []
        for line_dict in self.lines_list_v:
            for line_index, value in line_dict.items():
                min_max = value[0][0]
                if min_max not in min_max_list:
                    min_max_list.append(min_max)

        remove_list = []
        for line_dict in self.lines_list_h:
            for line_index, value in line_dict.items():
                vertical_cross_count = 0
                for min_max in min_max_list:
                    if min_max[0] < line_index < min_max[1]:
                        vertical_cross_count += 1

                if vertical_cross_count > 1:
                    remove_list.append(line_index)

        self.lines_list_h = [{key : value for (key, value) in self.lines_list_h[0].items() if key not in remove_list}]

    def remove_intersecting_words(self):
        """Remove words from vertical lines that are members of horizontal lines."""

        words_on_lines = []
        indices = []
        for line_dict in self.lines_list_h:
            for line_index, value in line_dict.items():
                indices.append(line_index)
                for word in value[-1]:
                    words_on_lines.append(word)

        def find_vertical_intersections(line_bounds, indices):
            """ID intersections of vertical and horizontal lines."""

            difference_list_bottom = sorted([[index, index - line_bounds[0][0]] for index in
                                              indices if index - line_bounds[0][0] > 0],
                                              key=itemgetter(1), reverse = True)

            difference_list_top = sorted([[index, index - line_bounds[0][1]] for index in
                                           indices if index - line_bounds[0][1] < 0],
                                           key=itemgetter(1))

            bottom_bound = difference_list_bottom[0][0]
            top_bound = difference_list_top[0][0]

        line_dict_out = {}
        for line_dict in self.lines_list_v:
            for line_index, value in line_dict.items():
                # bounds = find_vertical_intersections([value[-1][0]], indices)
                words = [value[-1][1][0]] + [word for word in value[-1][1][1:] if word not in words_on_lines]
                if len(words) > 1:
                    line_bounds = [min([word[3] for word in words[1:]]),
                                   max([word[1] for word in words[1:]])]

                    line_dict_out[line_index] = [[line_bounds, words]]

        self.lines_list_v = [line_dict_out]

    def reindex_zones(self):
        """Redefine line indeces prior to zoning."""

        line_dict_out = {}
        page_index_third_01 = 1
        page_index_third_02 = 1
        for line_dict in self.lines_list_v:
            for line_index, words in line_dict.items():
                if self.page_left + (self.width_difference / 3) - .04 < line_index < self.page_left + (self.width_difference / 3) + .07:
                    words = [[words[0][0], [page_index_third_01, words[0][1][1:]]]]
                    line_dict_out[line_index] = words
                    page_index_third_01 += 1

                elif self.page_left + ((self.width_difference / 3) * 2) - .04 < line_index < self.page_left + ((self.width_difference / 3) * 2) + .07:
                    words = [[words[0][0], [page_index_third_02, words[0][1][1:]]]]
                    line_dict_out[line_index] = words
                    page_index_third_02 += 1

        self.lines_list_v = [line_dict_out]

    def collect_zone_and_words(self):
        """Fine-tuned removal of words on edge-bounds of vertical lines."""

        zones_on_page = {}
        for line_dict in self.lines_list_v:
            for line_index, words in line_dict.items():

                page_index = words[0][1][0]
                line_bounds = words[0][0]

                if page_index in zones_on_page.keys():
                    zones_on_page[page_index].extend(line_bounds)
                else:
                    zones_on_page[page_index] = []
                    zones_on_page[page_index].extend(line_bounds)

        for zone, bounds_list in zones_on_page.items():
            if len(bounds_list) > 3:
                zone_min = min(bounds_list)
                zone_max = max(bounds_list)

                zones_on_page[zone] = [zone_max, self.page_right, zone_min, self.page_left]

        return zones_on_page

"""Construct word map graphs for each sheet in page_data_dictionary."""

class xmlPageData(object):

    def __init__(self, page, data):

        self.page = page
        self.page_dimensions = data[0]
        self.word_data = data[1]

        self.page_bounds = self.define_page_content_bounds()
        self.page_top = self.page_bounds[0][0]
        self.page_right = self.page_bounds[0][1]
        self.page_bottom = self.page_bounds[0][2]
        self.page_left = self.page_bounds[0][3]

        self.top_list = self.page_bounds[1][0]
        self.right_list = self.page_bounds[1][3]
        self.bottom_list = self.page_bounds[1][1]
        self.left_list = self.page_bounds[1][2]

        if self.page_bounds[2]:
            self.page_data = self.page_data_define()

            self.page_width = self.page_data[0]
            self.center = self.page_data[1]
            self.center_range_list = [self.page_data[2], self.page_data[3]]
            self.left_column_start = self.page_data[4]

            self.third_first = self.page_data[5]
            self.third_first_range_list = [self.page_data[6], self.page_data[7]]
            self.third_first_start = self.page_data[8]
            self.third_second = self.page_data[9]
            self.third_second_range_list = [self.page_data[10], self.page_data[11]]
            self.third_second_start = self.page_data[12]

            self.gutter_count_data = self.gutter_word_count()
            self.gutter_count_center = self.gutter_count_data[0]
            self.gutter_count_thirds = self.gutter_count_data[1]

        else:
            self.gutter_count_center = 0
            self.gutter_count_thirds = 0

    def define_page_content_bounds(self):
        """Identify bounds of page content (and exclude outliers)."""

        top_list = sorted([word[1] for word in self.word_data], reverse=True)
        right_list = sorted([word[2] for word in self.word_data], reverse=True)
        bottom_list = sorted([word[3] for word in self.word_data])
        left_list = sorted([word[4] for word in self.word_data])

        list_dict = {
            'top_list' : [1, top_list],
            'bottom_list' : [3, bottom_list],
            'left_list' : [4, left_list],
            'right_list' : [2, right_list]
        }

        list_list = [item[1] for item in list_dict.values()]

        if len(self.word_data) < 65:
            page_bounds_final = [.999, .999, .01, .01]
            operate = False
            return (page_bounds_final, list_list, operate)

        def area_check(bound, list_name, list_object):
            """check for abnormal distances between words."""

            finished = False
            while finished is False:

                border_area = 0
                neighbour_count = 0
                for word in self.word_data:
                    position = word[list_dict[list_name][0]]
                    if bound-.004 < position < bound+.004:
                        if list_name in list(list_dict.keys())[:2]:
                            border_area += abs(word[2]-word[4])
                        elif list_name in list(list_dict.keys())[2:]:
                            border_area += abs(word[1]-word[3])
                        neighbour_count += 1

                if border_area < .02 or (neighbour_count < 3 and border_area < .067):
                    list_object.remove(list_object[0])
                    if len(list_object) > 0:
                        bound = list_object[0]
                    else:
                        bound = .1
                        break
                else:
                    finished = True

            return bound

        bound_list = []
        for key, value in list_dict.items():
            bound = area_check(value[1][0], key, value[1])
            bound_list.append(bound)

        page_bounds = [bound for bound in bound_list]
        page_bounds = [page_bounds[0], page_bounds[3], page_bounds[1], page_bounds[2]]
        word_dict = {i: [word[0], word[1], word[2], word[3], word[4]] for i, word in enumerate(self.word_data)}

        def identify_outliers(input_dict, input_bounds):
            """Search input_dict for words outside of page bounds."""

            temporary_dict = input_dict.copy()
            remove_list = []
            for i, word in temporary_dict.items():
                if ((word[2] < input_bounds[3] and word[4] < input_bounds[3]) or
                    (word[2] > input_bounds[1] and word[4] > input_bounds[1]) or
                    (word[1] > input_bounds[0] and word[3] > input_bounds[0]) or
                    (word[1] < input_bounds[2] and word[3] < input_bounds[2])):

                    remove_list.append(i)

            for i in remove_list:
                del temporary_dict[i]

            page_bounds_new = [
                sorted([word[1] for word in temporary_dict.values()], reverse=True)[0],
                sorted([word[2] for word in temporary_dict.values()], reverse=True)[0],
                sorted([word[3] for word in temporary_dict.values()])[0],
                sorted([word[4] for word in temporary_dict.values()])[0]
            ]

            return page_bounds_new

        page_bounds_01 = identify_outliers(word_dict, page_bounds)
        page_bounds_02 = identify_outliers(word_dict, page_bounds_01)
        page_bounds_final = identify_outliers(word_dict, page_bounds_02)
        operate = True

        return (page_bounds_final, list_list, operate)

    def page_data_define(self):
        """Identify all data necessary for plotting (bounds, center, etc.)."""

        page_width = self.page_right - self.page_left
        range_offset_center = .0030
        range_offset_third = .0012

        center = self.page_right - (page_width / 2)
        center_range_min = center - range_offset_center
        center_range_max = center + range_offset_center

        third_first = self.page_right - ((page_width / 3) * 2)
        third_first_range_min = third_first - range_offset_third
        third_first_range_max = third_first + range_offset_third

        third_second = self.page_right - (page_width / 3)
        third_second_range_min = third_second - range_offset_third
        third_second_range_max = third_second + range_offset_third

        def identify_bound_start(input_list):
            """Circumvent key errors with conditional bound-start assignment."""

            if len(input_list) > 0:
                output = input_list[0]
            elif len(input_list) == 0 and len(self.left_list) > 0:
                output = self.left_list[0]
            else:
                output = 0

            return output

        left_column_start = identify_bound_start(sorted([value for value in self.left_list if value > center - .005]))
        third_one_start = identify_bound_start(sorted([value for value in self.left_list if value > third_first - .005]))
        third_two_start = identify_bound_start(sorted([value for value in self.left_list if value > third_second - .005]))

        return (page_width, center, center_range_min, center_range_max, left_column_start,
                third_first, third_first_range_min, third_first_range_max, third_one_start,
                third_second, third_second_range_min, third_second_range_max, third_two_start)

    def gutter_word_count(self):
        """Test for number words in the center of the sheet."""

        gutter_count_center = 0
        gutter_count_thirds = 0
        for word in self.word_data:

            word_right = word[2]
            word_left = word[4]

            if ((word_left < self.center_range_list[0] < word_right) or
                (word_left < self.center_range_list[1] < word_right)):

                gutter_count_center += 1

            if ((word_left < self.third_first_range_list[0] < word_right) or
                (word_left < self.third_first_range_list[1] < word_right) or
                (word_left < self.third_second_range_list[0] < word_right) or
                (word_left < self.third_second_range_list[1] < word_right)):

                gutter_count_thirds += 1

        return (gutter_count_center, gutter_count_thirds)

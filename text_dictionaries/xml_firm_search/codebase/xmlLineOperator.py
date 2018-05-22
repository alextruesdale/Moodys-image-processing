"""Identify words by a number of criteria. Colour them accordingly for plotting."""

import xmlWordOperators as xmlWO

class xmlLineOperator(object):

    def __init__(self, index, line, page_data, search_key_data, continuation):

        self.page = page_data.page
        self.index = index
        self.line = line[0]
        self.word_list = line[1]

        self.page_left = page_data.page_left
        self.page_right = page_data.page_right
        self.center = page_data.center

        self.left_column_start = page_data.left_column_start
        self.third_first_start = page_data.third_first_start
        self.third_second_start = page_data.third_second_start

        self.search_key_center = search_key_data[0]
        self.search_key_thirds = search_key_data[1]

        if continuation is False and self.search_key_center is True:
            self.line_data = self.line_test_indented_columns('center')

        elif continuation is False and self.search_key_thirds is True:
            self.line_data = self.line_test_indented_columns('thirds')

        elif continuation is True and (self.search_key_center is True or self.search_key_thirds is True):
            self.line_data = self.line_test_continued()

        elif continuation is False and self.search_key_center is False and self.search_key_thirds is False:
            self.line_data = self.line_test_center()

        self.captured_words = self.line_data[0]
        self.company_name_found = self.line_data[1]

    def clean_captured_words(self, captured_words):
        """"""

        string_continuous = ''.join([xmlWO.strip_punctuation(word[0]) for word in captured_words])
        if not xmlWO.check_capital_title(captured_words) or len(captured_words) < 2 or len(string_continuous) < 5:
            captured_words = []

        elif not xmlWO.identify_company_extensions(captured_words):
            if len(captured_words) > 0:
                captured_words = xmlWO.as_of_search(captured_words, string_continuous)
            if len(captured_words) > 0:
                captured_words = xmlWO.capitals_ratio(captured_words, string_continuous)
            if len(captured_words) > 0:
                captured_words = xmlWO.beginning_end_line_filter(captured_words, string_continuous)
            if len(captured_words) > 0:
                captured_words = xmlWO.is_management_bonded(captured_words, string_continuous)

        return captured_words

    def line_test_operator(self, captured_words, company_name_found):
        """"""

        company_name_found = 'Undefined'
        end = False
        for i, word in enumerate(self.word_list[:-1]):
            if i == (len(self.word_list) - 1):
                present_word = self.word_list[i][0]
                next_word = ''
            else:
                present_word = self.word_list[i][0]
                next_word = self.word_list[i+1][0]

            end_position_data = xmlWO.end_position(present_word, next_word)
            if end_position_data[0]:
                end = True
                company_name_found = True

            if end is False or end_position_data[2]:
                captured_words.append(word)
                if end_position_data[2]:
                    break

        captured_words = self.clean_captured_words(captured_words)

        if len(captured_words) == 0:
            company_name_found = False

        return (captured_words, company_name_found)

    def line_test_indented_columns(self, key):
        """Categorise words in line for two column sheets."""

        def line_test_operator_trigger():
            """Compartmentalised function to avoid repetition."""

            captured_words = []
            company_name_found = False
            line_test_data = self.line_test_operator(captured_words, company_name_found)
            return line_test_data

        captured_words = []
        company_name_found = False
        offset_list = [.01, .6]

        word_zero_left = self.word_list[0][4]
        word_zero = self.word_list[0][0]

        if key == 'center':
            word_limit_line = 5
            if self.index == 0:
                column_start = self.page_left
            elif self.index == 1:
                column_start = self.left_column_start
        elif key == 'thirds':
            word_limit_line = 2
            if self.index == 0:
                column_start = self.page_left
            elif self.index == 1:
                column_start = self.third_first_start
            elif self.index == 2:
                column_start = self.third_second_start

        if (column_start + offset_list[0] < word_zero_left < column_start + offset_list[1] and
            len(self.word_list) > word_limit_line and xmlWO.capital_search(word_zero)):

            if xmlWO.identify_company_extensions(self.line_test_operator(captured_words, company_name_found)[0]) is True:
                line_test_data = line_test_operator_trigger()
                captured_words = line_test_data[0]
                company_name_found = line_test_data[1]

            else:
                captured_words = []
                company_name_found = False

                if xmlWO.check_against_popular(xmlWO.strip_punctuation(word_zero), self.word_list, '') is False:
                    line_test_data = line_test_operator_trigger()
                    captured_words = line_test_data[0]
                    company_name_found = line_test_data[1]

        return (captured_words, company_name_found)

    def line_test_continued(self):
        """Search lines that follow an indented line of interest for string endpoints."""

        captured_words = []
        company_name_found = 'Undefined'
        end = False
        for i, word in enumerate(self.word_list[:-1]):
            if i == (len(self.word_list) - 1):
                present_word = self.word_list[i+1][0]
                next_word = ''
            else:
                present_word = self.word_list[i][0]
                next_word = self.word_list[i+1][0]

            end_position_data = xmlWO.end_position(present_word, next_word)
            if end_position_data[0]:
                end = True
                company_name_found = True

            if end is False or end_position_data[2] is True:
                captured_words.append(word)
                break

        captured_words = self.clean_captured_words(captured_words)
        return (captured_words, company_name_found)

    def line_test_center(self):
        """Categorise words in single-column sheets. Look for centered company names."""

        captured_words = []
        company_name_found = False

        line_left = self.word_list[0][4]
        line_right = self.word_list[-1][2]
        distance_left = line_left - self.page_left
        distance_right = self.page_right - line_right
        distance_distance = abs(distance_right - distance_left)

        if distance_distance < .05 and distance_left > .035:
            for word in self.word_list:
                captured_words.append(word)

        captured_words = self.clean_captured_words(captured_words)
        return (captured_words, company_name_found)

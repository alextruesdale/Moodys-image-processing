"""Identify words by a number of criteria. Colour them accordingly for plotting."""

from xmlWordOperators import xmlWordOperators as xmlWO

class xmlLineOperator(object):

    def __init__(self, line, page_plot, page_left, page_right, center,
                 left_column_start, third_first_start, third_second_start, search_key_center,
                 search_key_thirds, continuation):

        self.page_plot = page_plot
        self.line = line[0]
        self.word_list = line[1]

        self.page_left = page_left
        self.page_right = page_right
        self.center = center

        self.left_column_start = left_column_start
        self.third_first_start = third_first_start
        self.third_second_start = third_second_start

        self.search_key_center = search_key_center
        self.search_key_thirds = search_key_thirds

        if continuation == False and self.search_key_center == True:
            self.line_data = self.line_test_indent_two_column('center')

        elif continuation == True and self.search_key_center == True:
            self.line_data = self.line_test_continued('center')

        if continuation == False and self.search_key_thirds == True:
            self.line_data = self.line_test_indent_two_column('thirds')

        elif continuation == True and self.search_key_thirds == True:
            self.line_data = self.line_test_continued('thirds')

        elif continuation == False and self.search_key_center == False:
            self.line_data = self.line_test_center()

        self.captured_words = self.line_data[0]
        self.company_name_found = self.line_data[1]

    def line_test_operator(captured_words, company_name_found):
        """"""

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

            if end == False or end_position_data[2] == True:
                captured_words.append(word)

        if len(captured_words) > 0:
            if len(xmlWO.strip_punctuation(captured_words[-1][0])) > 0:
                if xmlWO.check_against_popular(xmlWO.strip_punctuation(captured_words[-1][0])):
                    # print(captured_words)
                    captured_words = []

            else:
                if xmlWO.check_against_popular(xmlWO.strip_punctuation(captured_words[-2][0])):
                    # print(captured_words)
                    captured_words = []

        if xmlWO.check_capital_title(captured_words) or len(captured_words) < 2:
            captured_words = []

        if len(captured_words) == 0:
            company_name_found = False

        return (captured_words, company_name_found)

    def line_test_indented_columns(self, key):
        """Categorise words in line for two column sheets."""

        captured_words = []
        company_name_found = False
        offset_list = [.012, .025]

        word_zero_left = self.word_list[0][4]
        word_zero = self.word_list[0][0]

        if key == 'center':
            column_start = self.left_column_start
        elif key == 'thirds':
            column_start = self.third_first_start
            column_start = self.third_second_start

        column_start + offset_list[0] < word_zero_left < column_start + offset_list[1] or
        self.page_left + offset_list[0] < word_zero_left < self.page_left + offset_list[1])
        and xmlWO.capital_search(word_zero) and
        xmlWO.check_against_popular(xmlWO.strip_punctuation(word_zero)) == False and
        len(self.word_list) > 5):

        line_test_data = line_test_operator(captured_words, company_name_found)
        captured_words = line_test_data[0]
        company_name_found = line_test_data[1]

        for word in self.word_list:
            colour = 'k'
            if word in captured_words:
                colour = 'm'

            xmlWO(self.page_plot, word, colour)

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

            if end == False or end_position_data[2] == True:
                captured_words.append(word)

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
            capitals_ratio = ((sum([1 for word in self.word_list if
                                    xmlWO.capital_search(xmlWO.strip_punctuation(word[0]))]) + 1) /
                                    (len(self.word_list) + 1))

            if capitals_ratio > .6:
                for word in self.word_list:
                    captured_words.append(word)

        for word in self.word_list:
            colour = 'k'
            if word in captured_words:
                colour = 'm'

            xmlWO(self.page_plot, word, colour)

        return (captured_words, company_name_found)

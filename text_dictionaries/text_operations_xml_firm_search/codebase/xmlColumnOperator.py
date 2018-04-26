"""Loop through lines in column objects and trigger line operator class instances appropriately."""

import xmlLineOperator
import xmlStaticOperators

class xmlColumnOperator(object):

    def __init__(self, index, dictionary, page, year, file_path, page_data, search_key_data):

        self.index = index
        self.dictionary = dictionary
        self.page = page
        self.year = year
        self.file_path = file_path

        self.page_data = page_data
        self.search_key_data = search_key_data
        self.page_break_dictionary_teilweise = self.list_operate()

    def list_operate(self):
        """Plot words on page/figure."""

        def write_from_list(file_path, list_name, delimiter):
            """Write list element to newline-delimited .txt file."""

            with open(file_path, 'a') as temporary_file:
                temporary_file = temporary_file.write(delimiter.join(list_name))

        page_break_dictionary_teilweise = {}
        dictionary_as_list = list(self.dictionary.items())[::-1]
        for i, word_list in enumerate(dictionary_as_list):
            present_line = xmlLineOperator.xmlLineOperator(self.index, dictionary_as_list[i],
                                                           self.page_data, self.search_key_data, False)

            if present_line.company_name_found == 'Undefined' and i < (len(dictionary_as_list) - 1):
                next_line = xmlLineOperator.xmlLineOperator(self.index, dictionary_as_list[i+1],
                                                            self.page_data, self.search_key_data, True)

                for word in next_line.captured_words:
                    present_line.captured_words.append(word)

            if self.index in page_break_dictionary_teilweise.keys() and len(present_line.captured_words) > 0:
                page_break_dictionary_teilweise[self.index].update({max([word[1] for word in present_line.captured_words]): present_line.captured_words})

            elif len(present_line.captured_words) > 0:
                page_break_dictionary_teilweise.update({self.index: {max([word[1] for word in present_line.captured_words]): present_line.captured_words}})

            if len(present_line.captured_words) > 0:
                page = ['\n', self.page, '\n']
                words_to_save = present_line.captured_words[:]
                words_to_save.append('\n')
                write_from_list(self.file_path, page, '')
                write_from_list(self.file_path, [word[0] for word in words_to_save], ' ')

        return page_break_dictionary_teilweise

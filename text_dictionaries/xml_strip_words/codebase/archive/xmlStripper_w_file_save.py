"""Derive relevant data from .xml files."""

from operator import itemgetter
import xml.etree.ElementTree as ET
import re
import os

class xmlStripper(object):

    def __init__(self, file_path, working_file):

        self.working_file = working_file
        self.file_path = file_path
        self.pages = self.split_pages()
        self.root_list = self.xml_to_element()
        self.tags = self.identify_tags()
        self.source_dictionary = self.create_source_dictionary()

        self.collect_words()

    def split_pages(self):
        """Split xml on <page> </page> tags."""

        page_string = re.search(r'\<page.*\>', self.working_file).group(0)
        body = page_string + self.working_file.split(page_string, 1)[1]

        pages = [page + '</page>' for page in body.split('</page>')[:-1]]
        return pages

    def xml_to_element(self):
        """Read xml to Element Tree 'Element'."""

        root_list = []
        for page in self.pages:
            root = ET.fromstring(page)
            root_list.append(root)

        return root_list

    def identify_tags(self):
        """Produce list of tags in document."""

        tags_available = []
        for root in self.root_list:
            for child in root.iter():
                if child.tag not in tags_available:
                    tags_available.append(child.tag)

        return tags_available

    def create_source_dictionary(self):
        """parse xml tree and identify sources; sort them."""

        source_dictionary = {}
        for root in self.root_list:
            for source in root.findall('.//source'):
                width = source.get('sizex')
                height = source.get('sizey')
                source_name = source.get('file').split('/')[-1]

                trimmed = source_name[:-4]
                fiche = trimmed[-9:-5]
                page = trimmed[-4:]

                source_dictionary.update({source_name: [int(fiche), int(page), [width, height]]})

        source_dictionary = sorted(source_dictionary.items(), key=itemgetter(1))
        return source_dictionary

    def collect_words(self):
        """
        Define source documents for each sheet and sheet dimensions.
        Rip information for words from xml Element for each sheet.
        """

        def none_to_empty(word):
            """Reassign NoneType objects to empty strings."""

            if not word:
                word = ''
            else:
                word = word
            return word

        def clear_destination(file_path):
            """Identify if file exists. If so, remove it."""

            if os.path.exists(file_path):
                os.remove(file_path)

        def page_output(save_name, sub_directory, data, reference):
            """Save operation for individual pages."""

            save_path = '../text_output/{}/{}'.format(sub_directory, save_name)
            delimiter = ', '

            if type(data) is dict:
                clear_destination(save_path)
                for key, value in data.items():
                    with open(save_path, 'a') as out_file:
                        out_file = out_file.write(delimiter.join((str(key), str(value[0]),
                                                                  str(value[1]), str(value[2]),
                                                                  str(value[3]), str(value[4]),
                                                                  '\n')))
            elif type(data) is list:
                with open(save_path, 'a') as out_file:
                    out_file = out_file.write(delimiter.join((str(reference), str(data[0]),
                                                              str(data[1]), '\n')))

        i = 1
        for source_data in self.source_dictionary:
            save_name = source_data[0][:-13] + '_data.txt'
            reference_name = source_data[0][:-4] + '.txt'
            sub_directory = 'sheet_directory'
            if i == 1:
                save_path = '../text_output/{}/{}'.format(sub_directory, save_name)
                clear_destination(save_path)

            page_output(save_name, sub_directory, source_data[1][2], reference_name)

            for root in self.root_list:
                word_dictionary = {}
                if root.find('.//source').get('file').split('/')[-1] == source_data[0]:
                    for i, word in enumerate(root.findall('.//wd')):
                        word.text = none_to_empty(word.text)
                        l = word.get('l')
                        r = word.get('r')
                        t = word.get('t')
                        b = word.get('b')

                        word_dictionary.update({i:[word.text,t,r,b,l]})

                    save_name = reference_name
                    sub_directory = 'txt_directory'
                    page_output(save_name, sub_directory, word_dictionary, None)

            i += 1

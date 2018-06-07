"""Derive relevant data from .xml files."""

from operator import itemgetter
import xml.etree.ElementTree as ET
import re

class xmlStripper(object):

    def __init__(self, file_path, working_file):

        self.working_file = working_file
        self.file_path = file_path
        self.pages = self.split_pages()
        self.root_list = self.xml_to_element()
        self.tags = self.identify_tags()
        self.source_dictionary = self.create_source_dictionary()
        self.page_data_data = self.collect_words()
        self.zone_data_dictionary = self.page_data_data[0]
        self.dictionary_length = self.page_data_data[1]

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
                if child.tag not in tags_available and re.match(r'.*Zone', child.tag):
                    tags_available.append(child.tag)

        return tags_available

    def create_source_dictionary(self):
        """parse xml tree and identify sources; sort them."""

        source_dictionary = {}
        for root in self.root_list:
            for source in root.findall('.//source'):
                width = int(source.get('sizex'))
                height = int(source.get('sizey'))
                source_name = source.get('file').split('/')[-1]

                trimmed = source_name[:-4]
                fiche = trimmed[-9:-5]
                page = trimmed[-4:]

                source_dictionary.update({source_name: [int(fiche), int(page), [width, height]]})

        source_dictionary = sorted(source_dictionary.items(), key=itemgetter(1))
        return source_dictionary

    def collect_words(self):
        """
        Define sources for each sheet and sheet dimensions.
        Rip information for words from xml Element for each sheet.
        """

        def none_to_empty(word):
            """Reassign NoneType objects to empty strings."""

            if not word:
                word = ''
            else:
                word = word
            return word

        dictionary_length = len(self.source_dictionary)
        zone_data_dictionary = {}
        for source_data in self.source_dictionary:
            file_name = source_data[0][:-4]
            zone_data_dictionary.update({file_name: []})
            for root in self.root_list:
                if root.find('.//source').get('file').split('/')[-1] == source_data[0]:
                    for tag in self.tags:
                        for zone in root.findall('.//{}'.format(tag)):
                            l = float('{:.5f}'.format(((int(zone.get('l')) * 400) / 1440)/source_data[1][2][0]))
                            r = float('{:.5f}'.format(((int(zone.get('r')) * 400) / 1440)/source_data[1][2][0]))
                            t = float('{:.5f}'.format(1-((int(zone.get('t')) * 400) / 1440)/source_data[1][2][1]))
                            b = float('{:.5f}'.format(1-((int(zone.get('b')) * 400) / 1440)/source_data[1][2][1]))

                            if zone.tag == 'tableZone' or zone.tag == 'textZone':
                                zone_data_dictionary[file_name].append([zone.tag,t,r,b,l,zone])
                            else:
                                zone_data_dictionary[file_name].append([zone.tag,t,r,b,l])

        return (zone_data_dictionary, dictionary_length)

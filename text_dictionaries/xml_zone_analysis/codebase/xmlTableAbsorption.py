"""Absorb neighbouring zones; extract word data; overwrite zones as newly-defined table."""

import xml.etree.ElementTree as ET
import xmlStaticOperators

class xmlTableAbsorption(object):

    def __init__(self, zone_list, working_zones, page_zone_data, page_data, column_zones_total):

        self.zone_list = zone_list
        self.working_zones = working_zones
        self.page_zone_data = page_zone_data
        self.page_data = page_data
        self.column_zones_total = column_zones_total
        self.zone_words = self.extract_words()
        self.remove_zones()
        self.manufacture_wordZones()

    def within_new_zone(self, object_in):
        """Identify if object_in is within new tableZone."""

        within_new_zone = False
        if (object_in[1] <= self.zone_list[1] + .002 and object_in[2] <= self.zone_list[2] + .002 and
            object_in[3] >= self.zone_list[3] - .002 and object_in[4] >= self.zone_list[4] - .002):

            within_new_zone = True

        return within_new_zone

    def extract_words(self):
        """Extract words from all zones in newly absorbed tableZone."""

        zone_words = []
        for zone in self.column_zones_total:
            zone_element = zone[5]
            for word in zone_element.findall('.//wd'):
                word.text = xmlStaticOperators.none_to_empty(word.text)
                l = float('{:.5f}'.format(((int(word.get('l')) * 400) / 1440)/self.page_data.page_dimensions[0]))
                r = float('{:.5f}'.format(((int(word.get('r')) * 400) / 1440)/self.page_data.page_dimensions[0]))
                t = float('{:.5f}'.format(1-((int(word.get('t')) * 400) / 1440)/self.page_data.page_dimensions[1]))
                b = float('{:.5f}'.format(1-((int(word.get('b')) * 400) / 1440)/self.page_data.page_dimensions[1]))
                word_zone = ['wordZone', t, r, b, l, word.text]

                if self.within_new_zone(word_zone):
                    zone_words.append(['wordZone', t, r, b, l, word.text])

        return zone_words

    def remove_zones(self):
        """Remove zones in newly expanded tableZone."""

        self.page_zone_data = [zone for zone in self.page_zone_data if not self.within_new_zone(zone)
                               or zone is self.zone_list]

    def manufacture_wordZones(self):
        """Add words in new tables into wordZones."""

        for word in self.zone_words:
            self.page_zone_data.append(word)

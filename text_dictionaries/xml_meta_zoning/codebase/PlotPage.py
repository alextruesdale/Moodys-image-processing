"""Plot page shell and instantiate word-plotting class."""

import re
import numpy as np
from PlotObjects import PlotObjects
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

class PlotPage(object):

    def __init__(self, line_search_out):

        self.word_data = line_search_out.word_data
        self.zone_data = line_search_out.zones_on_page
        self.lines_list_v = line_search_out.lines_list_v
        self.lines_list_h = line_search_out.lines_list_h

        self.page_top = line_search_out.page_top
        self.page_right = line_search_out.page_right
        self.page_bottom = line_search_out.page_bottom
        self.page_left = line_search_out.page_left
        self.page = line_search_out.page

        self.page_plot = self.plot_page()
        self.plot_lines_v()
        self.plot_lines_h()
        self.plot_zones()
        self.plot_words()

    def plot_page(self):
        """Initialise canvas on which to plot word locations."""

        page_figure = plt.figure(figsize = (8.5, 11), dpi = 150)
        page_plot = page_figure.add_subplot(111)
        page_figure.tight_layout(pad = 5.5)

        page_plot.set_xlim([0, 1.01])
        page_plot.set_ylim([0, 1.01])
        page_plot.set_xticks(np.arange(0.0, 1.1, 0.1))
        page_plot.set_yticks(np.arange(0.0, 1.1, 0.1))

        page_plot.set_title(self.page, fontsize = 13, fontweight = 'bold', y = 1.025)
        page_plot.set_xlabel('sheet width (norm. 0-1)')
        page_plot.set_ylabel('sheet height (norm. 0-1)')
        page_plot.xaxis.set_label_coords(.5, -.05)
        page_plot.yaxis.set_label_coords(-.11, .5)

        page_plot.add_patch(Rectangle((self.page_left, self.page_bottom),
                                      (self.page_right - self.page_left),
                                      (self.page_top - self.page_bottom),
                                      fill = None, edgecolor = 'b', alpha = 1))

        return page_plot

    def plot_lines_v(self):
        """Plot blue lines ID'ing lines of text"""

        for line_dict in self.lines_list_v:
            for line_index, value in line_dict.items():
                for line in value:
                    min_max = value[0][0]
                    min_value = min_max[0]
                    max_value = min_max[1] - .0076

                    self.page_plot.axvline(x = line_index, ymin = min_value, ymax = max_value)

    def plot_lines_h(self):
        """Plot blue lines ID'ing lines of text"""

        for line_dict in self.lines_list_h:
            for line_index, value in line_dict.items():
                for line in value:
                    min_max = value[0]
                    min_value = min_max[0]
                    max_value = min_max[1] - .0076

                    self.page_plot.axhline(y = line_index, xmin = min_value, xmax = max_value)

    def plot_zones(self):
        """Plot three-column zones on sheet."""

        for index, value in self.zone_data.items():
            if len(value) == 4:
                zone = ['', value[0], value[1], value[2], value[3]]
                PlotObjects(self.page_plot, zone, 'm')

    def plot_words(self):
        """Plot word objects on sheet."""

        def define_colour(word):
            """Analyse word content and colour accordingly."""

            def strip_punctuation(word):
                """Strip punctuation from word."""

                word = re.sub(r'[\.\,\:\;\"\'\!\?\(\)\[\]\-\s]', '', word)
                return word

            colour = 'k'
            word = strip_punctuation(word)
            capitals_ratio = ((sum([1 for char in word if char.isupper()]) + .001) /
                              (len([char for char in word]) + .001))

            digits_ratio = ((sum([1 for char in word if char.isdigit()]) + .001) /
                            (len([char for char in word]) + .001))

            if capitals_ratio > .72:
                colour = 'r'

            if digits_ratio > .85:
                colour = 'b'

            if capitals_ratio > .72 and digits_ratio > .85:
                colour = 'g'

            return colour

        for word in self.word_data:
            if (word[2] > self.page_left and word[4] < self.page_right and
                word[1] > self.page_bottom and word[3] < self.page_top):

                colour = define_colour(word[0])
                PlotObjects(self.page_plot, word, colour)

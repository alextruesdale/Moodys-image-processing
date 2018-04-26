"""Plot page shell and instantiate word-plotting class."""

import numpy as np
import xmlPlotWords
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

class xmlPlotPage(object):

    def __init__(self, data, page_line_data, manual_firms):

        self.lines_dict = page_line_data[0]
        self.words_excluded = page_line_data[1]
        self.page_data = data
        if manual_firms:
            self.manual_firms = manual_firms

        self.page_plot = self.plot_page()
        self.company_titles_words = self.page_company_names()
        self.plot_lines()
        self.plot_words()

    def plot_page(self):
        """Initialise canvas on which to plot word locations."""

        page_figure = plt.figure(figsize=(8.5, 11), dpi=150)
        page_plot = page_figure.add_subplot(111)
        page_figure.tight_layout(pad=5.5)

        page_plot.set_xlim([0, 1.01])
        page_plot.set_ylim([0, 1.01])
        page_plot.set_xticks(np.arange(0.0, 1.1, 0.1))
        page_plot.set_yticks(np.arange(0.0, 1.1, 0.1))

        page_plot.set_title(self.page_data.page, fontsize=13, fontweight='bold', y=1.025)
        page_plot.set_xlabel('sheet width (norm. 0-1)')
        page_plot.set_ylabel('sheet height (norm. 0-1)')
        page_plot.xaxis.set_label_coords(.5, -.05)
        page_plot.yaxis.set_label_coords(-.11, .5)

        page_plot.add_patch(Rectangle((self.page_data.page_left, self.page_data.page_bottom),
                                      (self.page_data.page_right - self.page_data.page_left),
                                      (self.page_data.page_top - self.page_data.page_bottom),
                                      fill=None, edgecolor='b', alpha=1))

        return page_plot

    def plot_lines(self):
        """Plot blue lines ID'ing lines of text"""

        for index, line_dict in self.lines_dict.items():
            for line_index in line_dict.keys():
                if len(self.lines_dict) > 1 and len(self.lines_dict) < 3:
                    if index == 0:
                        xmax_value = self.page_data.center - .005
                        xmin_value = 0
                    elif index == 1:
                        xmax_value = 1
                        xmin_value = self.page_data.center - .005

                elif len(self.lines_dict) > 2:
                    if index == 0:
                        xmax_value = self.page_data.third_first - .005
                        xmin_value = 0
                    elif index == 1:
                        xmax_value = self.page_data.third_second - .005
                        xmin_value = self.page_data.third_first - .005
                    elif index == 2:
                        xmax_value = 1
                        xmin_value = self.page_data.third_second - .005

                else:
                    xmin_value = 0
                    xmax_value = 1

                self.page_plot.axhline(y=line_index, xmin=xmin_value, xmax=xmax_value)

    def page_company_names(self):
        """Define list of firm names on page."""

        company_titles_words = []
        if hasattr(self, 'manual_firms'):
            for column in self.manual_firms.values():
                column_dict = dict(column)
                for company_word_list in column_dict.values():
                    for word in company_word_list:
                        company_titles_words.append(word)

        return company_titles_words

    def plot_words(self):
        """Trigger xmlPlotWords class."""

        for word in self.page_data.word_data:
            colour = 'k'
            if (word[2] > self.page_data.page_left and word[4] < self.page_data.page_right and
                word[1] > self.page_data.page_bottom and word[3] < self.page_data.page_top):

                if word in self.company_titles_words:
                    colour = 'm'

                xmlPlotWords.xmlPlotWords(self.page_plot, word, colour)

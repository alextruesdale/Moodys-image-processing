"""Construct manual chart outlining columned sheets."""

from matplotlib import pyplot as plt
import xmlStaticOperators
import xmlSheetGraph
import pandas as pd
import os

class xmlColumnChart(object):

    def __init__(self, section_dictionary, key):

        self.section_dictionary = section_dictionary
        self.key = key

        self.index_list = [index for index in self.section_dictionary.keys()]
        self.word_count_list = [value[1] for value in self.section_dictionary.values()]

        self.word_count_list_out = self.section_continuity()
        self.section_list = self.section_finder()

        self.chart_sheets()

    def section_continuity(self):
        """Document points where manual columns are 1 to 2."""

        word_count = pd.DataFrame(self.word_count_list)
        word_count.columns = ['values']
        word_count['values_binary'] = [1 if value <= 4 else 0 for value in word_count['values']]

        word_count_shift1 = pd.DataFrame(word_count['values_binary'].shift(-1))
        word_count_shift1.columns = ['values']
        word_count_shift2 = pd.DataFrame(word_count['values_binary'].shift(-2))
        word_count_shift2.columns = ['values']
        word_count_shift3 = pd.DataFrame(word_count['values_binary'].shift(-3))
        word_count_shift3.columns = ['values']

        word_count_shift1['values'].fillna(2, inplace=True)
        word_count_shift2['values'].fillna(2, inplace=True)
        word_count_shift3['values'].fillna(2, inplace=True)

        word_count['values_binary1'] = word_count_shift1['values'].astype(int)
        word_count['values_binary2'] = word_count_shift2['values'].astype(int)
        word_count['values_binary3'] = word_count_shift3['values'].astype(int)

        word_count.rename(columns={'values': 'index'}, inplace=True)
        word_count['index'] = word_count.index
        word_count_list_out = word_count.values.tolist()

        return word_count_list_out

    def section_finder(self):
        """Use output from section_continuity to find section boundaries."""

        key = False
        section_list = [[-1, key]]
        continuity = 0
        negative_continuity = 0
        for list_item in self.word_count_list_out:
            if list_item[1] == 1 and (list_item[2] == 1 or list_item[3] == 1):
                continuity += 1
                if continuity > 2:
                    negative_continuity = 0

            elif list_item[1] == 0 and (list_item[2] == 0 or list_item[3] == 0):
                negative_continuity += 1
                if negative_continuity > 2:
                    continuity = 0

            if (negative_continuity > 5 and list_item[1] == 0 and list_item[2] == 1 and
                list_item[3] == 1 and list_item[4] == 1 and key == False):

                key = True
                section_list.append([list_item[0] + 1.5, self.key, key])

            elif (continuity > 5 and list_item[1] == 1 and list_item[2] == 0 and
                  list_item[3] == 0 and list_item[4] == 0 and key == True):

                key = False
                section_list.append([list_item[0] + 1.5, self.key, key])

        return section_list

    def chart_sheets(self):
        """Chart words found in center of page by page."""

        page_figure = plt.figure(figsize=(11, 8.5), dpi=150)
        page_plot = page_figure.add_subplot(111)

        page_plot.set_title('Distribution of Word Count in Sheet Area (by index)',
                            fontsize=13, fontweight='bold', y=1.025)

        page_plot.set_xlabel('Sheet Index')
        page_plot.set_ylabel('Word Count in Gutter')
        page_plot.xaxis.set_label_coords(.5, -.08)
        page_plot.yaxis.set_label_coords(-.08, .5)

        for bound in self.section_list:
            page_plot.axvline(x=bound[0])

        page_plot.scatter(self.index_list, self.word_count_list, color='w', edgecolors='k', alpha=1)

        if self.key == 'center':
            save_name = 'center_word_distribution.pdf'
        elif self.key == 'thirds':
            save_name = 'third_word_distribution.pdf'

        xmlStaticOperators.clear_destination(save_name)
        page_figure.savefig(save_name)

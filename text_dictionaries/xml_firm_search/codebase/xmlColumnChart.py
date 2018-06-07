"""Construct manual chart outlining columned sheets."""

from matplotlib import pyplot as plt
import xmlStaticOperators
import pandas as pd

class xmlColumnChart(object):

    def __init__(self, section_dictionary, key, year):

        self.section_dictionary = section_dictionary
        self.key = key
        self.year = year

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
        line_item_path_df = pd.DataFrame([value[0] for value in self.section_dictionary.values()])

        word_count_shift1['values'].fillna(2, inplace=True)
        word_count_shift2['values'].fillna(2, inplace=True)
        word_count_shift3['values'].fillna(2, inplace=True)

        word_count['values_binary1'] = word_count_shift1['values'].astype(int)
        word_count['values_binary2'] = word_count_shift2['values'].astype(int)
        word_count['values_binary3'] = word_count_shift3['values'].astype(int)

        word_count.rename(columns={'values': 'index'}, inplace=True)
        word_count['index'] = word_count.index
        word_count_merged = word_count.merge(line_item_path_df, left_index=True, right_index=True, how='inner')
        word_count_list_out = word_count_merged.values.tolist()

        return word_count_list_out

    def section_finder(self):
        """Use output from section_continuity to find section boundaries."""

        key = False
        initial_value = False
        section_list = []
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
                list_item[3] == 1 and list_item[4] == 1 and key is False):

                key = True
                section_list.append([list_item[0] + .5, self.key, key, list_item[-1]])

            elif (continuity > 5 and list_item[1] == 1 and list_item[2] == 0 and
                  list_item[3] == 0 and list_item[4] == 0 and key is True):

                key = False
                section_list.append([list_item[0] + .5, self.key, key, list_item[-1]])

        if len(section_list) > 0:
            if section_list[0][2] == True:
                initial_value = False
            elif section_list[0][2] == False:
                initial_value = True

        section_list_out = [[-1, self.key, initial_value]]
        for section in section_list:
            section_list_out.append(section)

        return section_list_out

    def chart_sheets(self):
        """Chart words found in center of page by page."""

        page_figure = plt.figure(figsize=(11, 8.5), dpi=150)
        page_plot = page_figure.add_subplot(111)

        page_plot.set_title('Word Count Distribution ({}) in Sheet Area (by index)'.format(self.key),
                            fontsize=13, fontweight='bold', y=1.025)

        page_plot.set_xlabel('Sheet Index')
        page_plot.set_ylabel('Word Count in Gutter')
        page_plot.xaxis.set_label_coords(.5, -.08)
        page_plot.yaxis.set_label_coords(-.08, .5)

        for bound in self.section_list:
            page_plot.axvline(x=bound[0])

        page_plot.scatter(self.index_list, self.word_count_list, color='w', edgecolors='k', alpha=1)

        if self.key == 'center':
            save_name = '../../text_output/xml_firm_search_output/{}_word_distribution_center.pdf'.format(self.year)
        elif self.key == 'thirds':
            save_name = '../../text_output/xml_firm_search_output/{}_word_distribution_thirds.pdf'.format(self.year)

        xmlStaticOperators.clear_destination(save_name)
        page_figure.savefig(save_name)

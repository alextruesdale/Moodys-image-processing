"""Plot words on sheet."""

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

class xmlPlotWords(object):

    def __init__(self, page_plot, word, colour):

        self.page_plot = page_plot

        self.word_top = word[1]
        self.word_right = word[2]
        self.word_bottom = word[3]
        self.word_left = word[4]

        self.colour = colour
        self.plot_word()

    def plot_word(self):
        """plot word on page_plot object."""

        self.page_plot.add_patch(Rectangle((self.word_left, self.word_bottom),
                                           (self.word_right-self.word_left),
                                           (self.word_top-self.word_bottom),
                                           fill=None, edgecolor=self.colour, alpha=1))

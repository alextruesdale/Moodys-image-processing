"""Plot words on sheet."""

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

class PlotObjects(object):

    def __init__(self, page_plot, object_in, colour):

        self.page_plot = page_plot

        self.object_top = object_in[1]
        self.object_right = object_in[2]
        self.object_bottom = object_in[3]
        self.object_left = object_in[4]

        self.colour = colour
        self.plot_object()

    def plot_object(self):
        """plot word on page_plot object."""

        self.page_plot.add_patch(Rectangle((self.object_left, self.object_bottom),
                                           (self.object_right-self.object_left),
                                           (self.object_top-self.object_bottom),
                                           fill = None, edgecolor = self.colour, alpha = 1))

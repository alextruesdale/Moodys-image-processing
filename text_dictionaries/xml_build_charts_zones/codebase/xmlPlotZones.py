"""Plot zones on sheet."""

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

class xmlPlotZones(object):

    def __init__(self, page_plot, zone, colour, linewidth, linestyle):

        self.page_plot = page_plot

        self.zone_top = zone[1]
        self.zone_right = zone[2]
        self.zone_bottom = zone[3]
        self.zone_left = zone[4]

        self.colour = colour
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.plot_zone()

    def plot_zone(self):
        """plot zone on page_plot object."""

        self.page_plot.add_patch(Rectangle((self.zone_left, self.zone_bottom),
                                           (self.zone_right-self.zone_left),
                                           (self.zone_top-self.zone_bottom),
                                           fill = None, edgecolor=self.colour, alpha = 1,
                                           linewidth = self.linewidth,
                                           linestyle = self.linestyle))

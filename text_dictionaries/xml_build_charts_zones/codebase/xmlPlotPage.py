"""Plot page shell and instantiate word-plotting class."""

import numpy as np
import xmlPlotZones
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

class xmlPlotPage(object):

    def __init__(self, page, data, page_data_dictionary):

        self.page = page
        self.zone_data = data[1]
        self.page_data = page_data_dictionary
        self.page_plot = self.plot_page()
        self.plot_zones()

    def plot_page(self):
        """Initialise canvas on which to plot word locations."""

        page_figure = plt.figure(figsize=(8.5, 11), dpi=150)
        page_plot = page_figure.add_subplot(111)
        page_figure.tight_layout(pad=5.5)

        page_plot.set_xlim([0, 1.01])
        page_plot.set_ylim([0, 1.01])
        page_plot.set_xticks(np.arange(0.0, 1.1, 0.1))
        page_plot.set_yticks(np.arange(0.0, 1.1, 0.1))

        page_plot.set_title(self.page, fontsize=13, fontweight='bold', y=1.025)
        page_plot.set_xlabel('sheet width (norm. 0-1)')
        page_plot.set_ylabel('sheet height (norm. 0-1)')
        page_plot.xaxis.set_label_coords(.5, -.05)
        page_plot.yaxis.set_label_coords(-.11, .5)

        page_plot.add_patch(Rectangle((self.page_data.page_left, self.page_data.page_bottom),
                                      (self.page_data.page_right - self.page_data.page_left),
                                      (self.page_data.page_top - self.page_data.page_bottom),
                                      fill=None, edgecolor='.75', alpha=1,
                                      linewidth = 1.2, linestyle = 'solid'))

        return page_plot

    def plot_zones(self):
        """Trigger xmlPlotzones class."""

        for zone in self.zone_data:
            zone_type = zone[0]

            if zone_type == 'tableZone':
                colour = 'b'
                linewidth = 2.3
                linestyle = 'solid'
            elif zone_type == 'textZone':
                colour = 'm'
                linewidth = 2
                linestyle = 'dotted'
            elif zone_type == 'cellZone':
                colour = 'k'
                linewidth = 1.0
                linestyle = 'dotted'
            elif zone_type == 'wordZone':
                colour = 'g'
                linewidth = 1
                linestyle = 'solid'

            if not (zone[2] < self.page_data.page_left or zone[4] > self.page_data.page_right or
                    zone[1] < self.page_data.page_bottom or zone[3] > self.page_data.page_top):

                xmlPlotZones.xmlPlotZones(self.page_plot, zone, colour, linewidth, linestyle)

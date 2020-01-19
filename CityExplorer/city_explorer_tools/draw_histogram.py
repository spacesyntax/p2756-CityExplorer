import matplotlib.pyplot as plt
import numpy as np
import os

# import project specific settings

from ..log import *
from utility_functions import roundup, getLayerByName

# https://stackoverflow.com/questions/42886076/matplotlib-radar-chart-axis-labels

def drawHistogram(iface, layer, field, use_selection=False): #TODO districts

    # TODO change dynamically based on field
    # colors, chart_legends, map_legends

    colors = field.get_colour_scale()
    ranges = field.get_values_ranges()
    labels = field.get_style_labels()
    column_name = field.ium_column
    x_axis = field.get_x_axis()

    print 'hist_info', colors, ranges, labels, column_name, use_selection

    if use_selection is True:
        values = [f[column_name] for f in layer.selectedFeatures()]
        total = layer.selectedFeatureCount()
        values_grouped = [[y for y in values if min_range < y <= max_range] for (min_range, max_range) in ranges]
        data_dict = {}
        for idx, lbl in enumerate(labels):
            data_dict[labels[idx]] = (100.0 * len(values_grouped[idx])) / float(total)  # calcluate %
    else:
        layer_name = layer.name()
        layer = getLayerByName(layer_name + '_summary_stats')
        if column_name[0:5] == 'nachr':
            layer = getLayerByName(layer_name + '_summary_stats_nach')
        elif column_name[0:4] == 'intr':
            layer = getLayerByName(layer_name + '_summary_stats_int')
        elif column_name in ['vibrancy', 'walkability', 'car_dependence', 'energy_consumption']:
            layer = getLayerByName(layer_name + '_summary_stats_0_1')
        #TODO specify corect for buildings
        data_dict = {f['ranges']: float(f[column_name]) for f in layer.getFeatures()}

    print 'data', data_dict

    fig, ax = plt.subplots()
    ind = np.arange(len(ranges))

    # show the figure, but do not block
    # plt.show(block=False)

    if len(ranges) == 4:
        p0, p1, p2, p3 = plt.bar(ind, [0, 0, 0, 0], align='center')
        p = [p0, p1, p2, p3]
    elif len(ranges) == 16:
        p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15 = plt.bar(ind, [0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0], align='center')
        p = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15]
    else:
        p0, p1, p2, p3, p4, p5 = plt.bar(ind, [0, 0, 0, 0, 0, 0], align='center')
        p = [p0, p1, p2, p3, p4, p5]

    for idx, i in enumerate(p):
        i.set_facecolor(colors[idx])

    ax.set_xticks(ind)
    if len(labels) == 16:
        ax.set_xticklabels(['low', '', '', '','','','','','','','','','','','','high'])
    else:
        ax.set_xticklabels(labels) # ranges

    ax.set_ylim([0, roundup(max(data_dict.values()))]) # [ranges[0][0], ranges[-1][1]]

    ax.set_ylabel('% ')
    ax.set_xlabel(x_axis)
    # ax.set_title('System Monitor')
    # hide top and right ticks
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.tick_bottom()
    ax.yaxis.tick_left()

    # lighten ticks and labels
    ax.tick_params(colors='gray', direction='out')
    for tick in ax.get_xticklabels():
        tick.set_color('gray')
    for tick in ax.get_yticklabels():
        tick.set_color('gray')

    for i, k in zip(p, labels):
        # TODO % or actual value?
        i.set_height(float(data_dict[k]))

    output_path = os.path.dirname(__file__) + '/foo.png'
    plt.savefig(output_path)

    return output_path, data_dict

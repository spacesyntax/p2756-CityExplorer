import matplotlib.pyplot as plt
import numpy as np
import os

# import project specifi settings

from ..log import *

# https://stackoverflow.com/questions/42886076/matplotlib-radar-chart-axis-labels

def drawHistogram(layer, field): #TODO districts

    # TODO change dynamically based on field
    # colors, chart_legends, map_legends

    colors = field.get_colour_scale()
    ranges = field.get_values_ranges()
    labels = field.get_style_lables()
    column_name = field.ium_column

    # TODO add filter based on districts
    data_dict = {}
    for (min_rng, max_rng) in ranges:
        filtered_features = filter(lambda f: min_rng < f[column_name] and f[column_name] <= max_rng, layer.getFeatures())
        data_dict[str(min_rng) + '-' + str(max_rng)] = len(filtered_features)

    # TODO edit always first range or last??
    empty_values = filter(lambda f: f[column_name] is None, layer.getFeatures())
    #data_dict[ranges[0]] = data_dict[ranges[0]] + len(empty_values)

    fig, ax = plt.subplots()
    ind = np.arange(6)

    # show the figure, but do not block
    # plt.show(block=False)

    p0, p1, p2, p3, p4, p5 = plt.bar(ind, [0, 0, 0, 0, 0, 0], align='center')
    p = [p0, p1, p2, p3, p4, p5]

    for idx, i in enumerate(p):
        i.set_facecolor(colors[idx])

    ax.set_xticks(ind)
    # TODO setup ranges dynamically & max & axes names

    ax.set_xticklabels(labels) # ranges
    ax.set_ylim([ranges[0][0], ranges[-1][1]])

    ax.set_ylabel('% buildings')
    ax.set_xlabel('number of land uses')
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

    for i, k in zip(p, ['0', '1', '2-5', '5-10', '10-20', '20-50', '50-100', '>100']):
        i.set_height(50) #data_dict[k])

    output_path = os.path.dirname(__file__) + '/foo.png'
    plt.savefig(output_path)

    return output_path

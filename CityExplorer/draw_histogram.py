import matplotlib.pyplot as plt
import numpy as np
import os

from log import *

# https://stackoverflow.com/questions/42886076/matplotlib-radar-chart-axis-labels


def drawHistogram(factor, districts):

    # input
    # districts
    summary_layer = getLayerByName()
    column = None
    colour_scale = colour_scales[factor]

    ranges = {'-1.00-0': '0', '0-0.2': '0-0.2', '0.2-0.4': '0.2-0.4', '0.4-0.6': '0.4-0.6', '0.6-0.8': '0.6-0.8', '0.8-1': '0.8-1'}
    data = map(lambda f: (ranges[f['ranges']], f[column]) if f[column] else (ranges[f['ranges']], 0), summary_layer.getFeatures())
    data_dict = dict(data)

    fig, ax = plt.subplots()
    ind = np.arange(8)

    # show the figure, but do not block
    # plt.show(block=False)

    p0, p1, p25, p510, p1020, p2050, p50100, p100 = plt.bar(ind, [0, 0, 0, 0, 0, 0, 0, 0], align='center')
    p = [p0, p1, p25, p510, p1020, p2050, p50100, p100]
    colour_scale = colour_scales[factor]

    for idx, i in enumerate(p):
        i.set_facecolor(colour_scale[idx])

    ax.set_xticks(ind)
    ax.set_xticklabels(['0', '1', '2-5', '5-10', '10-20', '20-50', '50-100', '>100'])
    ax.set_ylim([0, 100])
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
        i.set_height(data_dict[k])

    output_path = os.path.dirname(__file__) + '/charts/foo.png'
    plt.savefig(output_path)

    return output_path

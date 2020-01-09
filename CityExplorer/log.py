
# general imports
from PyQt4.QtCore import QObject

# LAND USE ABBREVIATIONS

lu_abbr = {
            'edu': 'education',
            'edu_nursery':	'nurseries',
            'edu_secondary': 'primary & secondary education',
            'edu_higher': 'higher education faculties',

            'hcare': 'healthcare',
            'hcare_primary': 'primary healthcare facilities',
            'hcare_secondary':	'secondary  healthcare facilities',
             #'resi': 'residential',
             # TODO jobs

            'phys': 'physical activity',
            'social': 'cultural facilities',

'act_green': 'parks',
    'jobs' : 'jobs',
'walkability': 'walkability',
'mscale_length': 'vibrancy',
'car_depend': 'car depedence'
}

# INDICES

# tier 1 - districts
# tier 2 - buildings
tier2 = {'liveability': #['edu', 'social', 'act_green', 'mscale_length'],
                        ['vibrancy', 'education', '- nurseries', '- primary & secondary schools', '- higher education', 'parks', 'cultural facilities'],
          # 'sustainability': ['pop_score', 'energy_mean_total'],
          # 'sustainability': ['population coverage', 'energy consumption?'],
          'health':     #['hcare', 'phys', 'pt_stops', 'mixeduse', 'car_depend'],
                        ['sport facilties', 'all healthcare', '- primary healthcare', '- secondary healthcare', 'public transport', 'car dependence', '- jobs', 'walkability'],
          'overall':    #['edu', 'social', 'act_green', 'mscale_length', 'pop_score', 'energy_mean_total', 'hcare', 'phys', 'pt_stops', 'mixeduse', 'car_depend']
                        ['vibrancy', 'education', '- nurseries', '- primary & secondary schools', '- higher education', 'parks', 'cultural facilities',
                         'sport facilties', 'all healthcare', '- primary healthcare', '- secondary healthcare', 'public transport', 'car dependence', '- jobs', 'walkability'],
          }
# tier 3 - streets
streets = ['multi-scale', 'NACh 2km', 'NACh 10km', 'NAIn 2km', 'NAIn 10km', 'count_id_resi']

# COLOURS RANGES

# TODO added light grey & setup transparency change 'color':'#ffffff' with 'color':'0,0,0,0' - ast 0 is transoarency )
colour_scales = {'overall':         ["#D3D3D3", "#fafafa", "#bcbcbc", "#7f7f7f","#424242", "#050505"],
                 'liveability':     ["#D3D3D3", "#ffffff", "#ecbfbf", "#d98080", "#c64040", "#b30000"],
                 'sustainabilty':   ["#f7fcf5", "#caeac3", "#7bc87c", "#2a924a", "#00441b"],
                 'health':          ["#D3D3D3","#f7fbff", "#c8ddf0", "#73b3d8", "#2879b9", "#2879b9", "#08306b"]}


# MODES

default_modes = ['10min walk', '15min public transport', '15min car']
custom_modes = {
        'act_green': ['10min walk', '15min public transport'], # 'parks'
        'mscale_length': ['all modes'], # 'vibrancy'
        'walkability': ['10min walk'], # walkability
        'car_depend': ['car:public transport'], # 'car dependence'
        'jobs': ['30min car', '30min public transport'] #  'jobs'
}
custom_modes_names = {lu_abbr[i]: j for i, j in custom_modes.items()}

# RANGES

default_ranges = [[0, 0], [0, 0.2], [0.2, 0.4], [0.4, 0.6], [0.6, 0.8], [0.8, 1]]
default_choices_range = [[0, 0], [0, 1], [1, 3], [3, 5], [5, 10], [10, 100000000000]]

# overall - between 0 - 1
# min_dist

# STYLE LABELS

default_labels = ['0', '0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1']

# CHART LABELS


# class to get ium properties field

class IUMField(QObject):

    def __init__(self, user_input, mode_input, tier):
        QObject.__init__(self)
        self.user_input = user_input
        self.mode_input = mode_input
        self.tier = tier
        self.ium_column = None
        print self.tier
        if self.tier == 1:
            self.ium_column = self.user_input + '_score'
        elif self.tier == 2 or self.tier == 3:
            # get land use abbreviations
            try:
                self.ium_column = 'sum_count_id' + lu_abbr[self.user_input]
            except KeyError:
                # replace _ with spaces
                self.ium_column = self.user_input.replace(' ', '_')

    def get_modes(self):
        # only in tier 2 & 3
        try:
            return custom_modes[self.ium_column]
        except KeyError:
            return default_modes

    def get_values_ranges(self):
        return default_ranges

    def get_style_lables(self):
        return default_labels

    # function to return color scales
    def get_colour_scale(self):

        return colour_scales['liveability']

    def get_map_legend(self):
        return

    def get_chart_legend(self):
        return




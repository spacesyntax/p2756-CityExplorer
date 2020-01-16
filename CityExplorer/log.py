
# general imports
from PyQt4.QtCore import QObject

# LAND USE ABBREVIATIONS

lu_abbr = {
            'education': 'edu',
            'nurseries': 'edu_nursery',
            'primary & secondary education': 'edu_secondary',
            'higher education faculties': 'edu_higher',

            'healthcare': 'hcare',
            'primary healthcare facilities' :'hcare_primary',
            'secondary healthcare facilities': 'hcare_secondary',

            'sport facilities': 'phys',
            'cultural facilities': 'social',
            'public transport': 'pt_stops',

'parks': 'act_green',
'vibrancy' : 'mscale_length',
'multi-scale accessibility': '', # TODO
'local choice': 'nachr2k',
'global choice': 'nachr10k',
'local integration': 'intr2k',
'global integration': 'intr10k'
}

# INDICES

# tier 1 - districts
# tier 2 - buildings
tier2 = {'liveability': #['edu', 'social', 'act_green', 'mscale_length'],
                        ['education', 'parks', 'cultural facilities', 'vibrancy'],
          # 'sustainability': ['pop_score', 'energy_mean_total'],
          'sustainability': ['population coverage', 'energy consumption?'],
          'health':     #['hcare', 'phys', 'pt_stops', 'mixeduse', 'car_depend'],
                        ['healthcare', 'sport facilities', 'public transport', 'car dependence', 'walkability'],
          'combined':    #['edu', 'social', 'act_green', 'mscale_length', 'pop_score', 'energy_mean_total', 'hcare', 'phys', 'pt_stops', 'mixeduse', 'car_depend']
                        [ 'education', 'parks', 'cultural facilities', 'vibrancy',
                         'healthcare', 'sport facilities', 'public transport', 'car dependence', 'walkability'],
          }

tier3 = {'Access to education': ['all', 'nurseries', 'primary & secondary education', 'higher education faculties'],
         'Access to healthcare': ['all', 'primary healthcare facilities', 'secondary healthcare facilities']
}

# tier 3 - streets
streets = ['Multi-scale accessibility', 'local choice', 'global choice', 'local integration', 'global integration']

# COLOURS RANGES

# TODO added light grey & setup transparency change 'color':'#ffffff' with 'color':'0,0,0,0' - ast 0 is transoarency )
colour_scales = {'combined':         ["#D3D3D3", "#fafafa", "#bcbcbc", "#7f7f7f","#424242", "#050505"],
                 'liveability':     ["#D3D3D3", "#ffffff", "#ecbfbf", "#d98080", "#c64040", "#b30000"],
                 'sustainabilty':   ["#f7fcf5", "#caeac3", "#7bc87c", "#2a924a", "#00441b"],
                 'health':          ["#D3D3D3","#f7fbff", "#c8ddf0", "#73b3d8", "#2879b9", "#2879b9", "#08306b"]}


# MODES

default_modes = ['10min walk', '15min public transport', '15min car']
modes_abbr = {'10min walk': '10_walk',
              '15min public transport': '15_pt',
              '15min car': '10_car',
              '30min car': '30_car',
              '30min public transport': '30_pt'
              }

custom_modes = {
        'Access to parks': ['10min walk', '15min public transport'], # 'parks'
        'Access to public transport': ['10min walk'],
        'Vibrancy': ['all modes'], # 'vibrancy'
        'Walkability': ['all modes'], # walkability
        'Car dependence': ['car:public transport'], # 'car dependence'
        #TODO 'jobs': ['30min car', '30min public transport'] #  'jobs'
}

# RANGES

default_ranges = [[0, 0], [0, 0.2], [0.2, 0.4], [0.4, 0.6], [0.6, 0.8], [0.8, 1]]
default_choices_ranges = [[0, 0], [1, 2], [2, 3], [3, 10000000000]]
default_choices_ranges_big = [[0, 5], [5, 10], [10, 15], [15, 1000]]

# overall - between 0 - 1

# STYLE LABELS

default_labels = ['0', '0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1']
default_choices_labels = ['0', '1-2', '2-3', '>3']
default_choices_labels_big = ['0-5', '5-10', '10-15', '>15']

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
            self.ium_column = self.user_input[:-6] + '_score'
        elif self.tier == 2:
            # get land use abbreviations
            if self.user_input == 'Vibrancy':
                self.ium_column = lu_abbr[self.user_input]
            else:
                try:
                    self.ium_column = 'sum_count_id_' + lu_abbr[self.user_input[10:]] + '_' + modes_abbr[self.mode_input]
                except KeyError:
                    # replace _ with spaces
                    try:
                        self.ium_column = 'sum_count_id_' + lu_abbr[self.user_input] + '_' + modes_abbr[self.mode_input]
                    except KeyError:
                        self.ium_column = self.user_input.replace(' ', '_')
        elif self.tier == 3:
            self.ium_column = lu_abbr[self.user_input]

    def get_values_ranges(self):
        if self.ium_column[0:12] == 'sum_count_id':
            if self.ium_column[0:19] in ('sum_count_id_social', 'sum_count_id_pt_sto', 'sum_count_id_act_gr'):
                return default_choices_ranges_big
            else:
                return default_choices_ranges
        else:
            return default_ranges

    def get_style_labels(self):
        if self.ium_column[0:12] == 'sum_count_id':
            if self.ium_column[0:19] in ('sum_count_id_social', 'sum_count_id_pt_sto', 'sum_count_id_act_gr'):
                return default_choices_labels_big
            else:
                return default_choices_labels
        else:
            return default_labels

    # function to return color scales
    def get_colour_scale(self):

        return colour_scales['liveability']

    def get_total(self):

        return

    def get_x_axis(self):
        if self.ium_column[0:19] == 'sum_count_id_social':
            return 'Number of cultural facilities'
        elif self.ium_column[0:12] == 'sum_count_id':
            return 'Number of' + self.user_input[10:]
        else:
            return self.user_input




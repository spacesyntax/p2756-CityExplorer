
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

'Vibrancy' : 'mscale_length',
'Multi-scale accessibility': '', # TODO
'Local choice': 'nachr2k',
'Global choice': 'nachr10k',
'Local integration': 'intr2k',
'Global integration': 'intr10k'
}

# INDICES

# tier 1 - districts
# tier 2 - buildings
tier2 = {'Liveability': #['edu', 'social', 'act_green', 'mscale_length'],
                        ['education', 'parks', 'cultural facilities', 'Vibrancy'],
          # 'sustainability': ['pop_score', 'energy_mean_total'],
          'Sustainability': ['Energy consumption'],
          'Health':     #['hcare', 'phys', 'pt_stops', 'mixeduse', 'car_depend'],
                        ['healthcare', 'sport facilities', 'public transport', 'Car dependence', 'Walkability'],
          'Combined':    #['edu', 'social', 'act_green', 'mscale_length', 'pop_score', 'energy_mean_total', 'hcare', 'phys', 'pt_stops', 'mixeduse', 'car_depend']
                        [ 'education', 'parks', 'cultural facilities', 'Vibrancy',
                         'healthcare', 'sport facilities', 'public transport', 'Car dependence', 'Walkability', 'Energy consumption'],
          }

tier3 = {'Access to education': ['all', 'nurseries', 'primary & secondary education', 'higher education faculties'],
         'Access to healthcare': ['all', 'primary healthcare facilities', 'secondary healthcare facilities']
}

# tier 3 - streets
streets = ['Multi-scale accessibility', 'Local choice', 'Global choice', 'Local integration', 'Global integration']

# COLOURS RANGES

colour_scales = {

'Liveability':    ["#ffffff", "#efcccc", "#e09999", "#d16666","#c23333","#b30000"],
'Sustainability': ["#f7fcf5","#d4eece","#9dd798","#54b466","#1d8640","#00441b"] ,
'Health':         ["#f7fbff","#d1e2f2","#9ac7e0","#519ccc","#1c6bb0","#08306b"],
'Combined':       ["#fafafa","#c9c9c9","#989898","#676767","#363636","#050505"],

            'education': ["#f7fbff", "#b0d2e8", "#3e8ec4", "#08306b"],

            'nurseries': ["#f7fbff", "#b0d2e8", "#3e8ec4", "#08306b"],
            'primary & secondary education': ["#f7fbff", "#b0d2e8", "#3e8ec4", "#08306b"],
            'higher education faculties': ["#f7fbff", "#b0d2e8", "#3e8ec4", "#08306b"],

            'healthcare': ["#fff5eb","#fdd1ab","#ff7e33","#dc3e00"],
            'primary healthcare facilities': ["#fff5eb","#fdd1ab","#ff7e33","#dc3e00"],
            'secondary healthcare facilities': ["#fff5eb","#fdd1ab","#ff7e33","#dc3e00"],

            'sport facilities': ["#fefeda","#fff063","#e6ff00","#8bfc00"],
            'cultural facilities': ["#edf8fb","#a6bbda","#896bb2","#810f7c"],
            'public transport': ["#08306b","#3e8ec4","#b0d2e8","#f7fbff"],

'parks': ["#f7fcf5","#b2e0ab","#3da75a","#00441b"],
'Vibrancy' : ["#ffffff", "#efcccc", "#e09999", "#d16666","#c23333","#b30000"],
'Multi-scale accessibility': '', # TODO
'Local choice': ["#0000ff","#0050ff","#00b0ff","#00ffff","#00ffb0","#00ff50","#30ff00","#60ff00","#a0ff00","#d0ff00","#ffff00","#ffd000","#ffa000","#ff6000","#ff3000","#ff0000"],
'Global choice': ["#0000ff","#0050ff","#00b0ff","#00ffff","#00ffb0","#00ff50","#30ff00","#60ff00","#a0ff00","#d0ff00","#ffff00","#ffd000","#ffa000","#ff6000","#ff3000","#ff0000"],
'Local integration': ["#0000ff","#0050ff","#00b0ff","#00ffff","#00ffb0","#00ff50","#30ff00","#60ff00","#a0ff00","#d0ff00","#ffff00","#ffd000","#ffa000","#ff6000","#ff3000","#ff0000"],
'Global integration': ["#0000ff","#0050ff","#00b0ff","#00ffff","#00ffb0","#00ff50","#30ff00","#60ff00","#a0ff00","#d0ff00","#ffff00","#ffd000","#ffa000","#ff6000","#ff3000","#ff0000"],
'Energy consumption': ["#ffffff", "#efcccc", "#e09999", "#d16666","#c23333","#b30000"],
'Car dependence': ["#ffffff","#f1eef6","#da9ccc","#d358ac","#d358ac","#3c008c"],
'Walkability': ["#f7fbff","#d1e2f2","#9ac7e0","#519ccc","#1c6bb0","#08306b"]}

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
        'Energy consumption': ['all modes']
}

# RANGES

default_ranges = [[0, 0], [0, 0.2], [0.2, 0.4], [0.4, 0.6], [0.6, 0.8], [0.8, 1]]
default_choices_ranges = [[0, 0], [1, 2], [2, 3], [3, 10000000000]]
ssx_choice_ranges = [[0, 0.333212394316885], [0.333212394316885,0.351122560511418], [0.351122560511418,0.36903272670595],[0.36903272670595,0.388567303322778],[0.388567303322778,0.404853059095015],[0.404853059095015,0.422763225289548],[0.422763225289548,0.440256875991184],[0.440256875991184,0.458167042185717],[0.458167042185717,0.47607720838025],[0.47607720838025,0.493987374574782],[0.493987374574782,0.511897540769315],[0.511897540769315,0.529807706963847],[0.529807706963847,0.547301357665484],[0.547301357665484,0.565211523860016],[0.565211523860016,0.583121690054549],[0.583121690054549,1]]
ssx_int_ranges = [[0.00134057675715326,0.0637574933181945],[0.0637574933181945,0.188591326440277],[0.188591326440277,0.251005432567865],[0.251005432567865,0.313422349128906],[0.313422349128906,0.375839265689947],[0.375839265689947,0.375839265689947],[0.375839265689947,0.438256182250989],[0.438256182250989,0.500670288378577],[0.500670288378577,0.563087204939618],[0.563087204939618,0.625504121500659],[0.625504121500659,0.6879210380617],[0.6879210380617,0.750335144189288],[0.750335144189288,0.812752060750329],[0.812752060750329,0.875168977311371],[0.875168977311371,0.937585893872412],[0.937585893872412,1]]

#TODO ms_qml =

# overall - between 0 - 1

# STYLE LABELS

default_labels = ['0', '0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1']
default_choices_labels = ['0', '1-2', '2-3', '>3']
ssx_choice_labels  = [
    '0-0.333212394316885',
    '0.333212394316885-0.351122560511418'		,
    '0.351122560511418-0.36903272670595'		,
    '0.36903272670595-0.388567303322778'		,
    '0.388567303322778-0.404853059095015'		,
    '0.404853059095015-0.422763225289548'		,
    '0.422763225289548-0.440256875991184'		,
    '0.440256875991184-0.458167042185717'		,
    '0.458167042185717-0.47607720838025'		,
    '0.47607720838025-0.493987374574782'		,
    '0.493987374574782-0.511897540769315'		,
    '0.511897540769315-0.529807706963847'		,
    '0.529807706963847-0.547301357665484'		,
    '0.547301357665484-0.565211523860016'		,
    '0.565211523860016-0.583121690054549'		,
    '0.583121690054549-1'
]
ssx_int_labels= [
'0.00134057675715326-0.0637574933181945'	,
'0.0637574933181945-0.188591326440277'	,
'0.188591326440277-0.251005432567865'	,
'0.251005432567865-0.313422349128906'	,
'0.313422349128906-0.375839265689947'	,
'0.375839265689947-0.375839265689947'	, # TODO - fix
'0.375839265689947-0.438256182250989'	,
'0.438256182250989-0.500670288378577'	,
'0.500670288378577-0.563087204939618'	,
'0.563087204939618-0.625504121500659'	,
'0.625504121500659-0.6879210380617'	,
'0.6879210380617-0.750335144189288'	,
'0.750335144189288-0.812752060750329'	,
'0.812752060750329-0.875168977311371'	,
'0.875168977311371-0.937585893872412'	,
'0.937585893872412-1'
]


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
            self.ium_column = self.user_input[:-6].lower() + '_score'
        elif self.tier == 2:
            # get land use abbreviations
            try:
                self.ium_column = 'sum_count_id_' + lu_abbr[self.user_input[10:]] + '_' + modes_abbr[self.mode_input]
            except KeyError:
                # replace _ with spaces
                try:
                    self.ium_column = 'sum_count_id_' + lu_abbr[self.user_input] + '_' + modes_abbr[self.mode_input]
                except KeyError:
                    self.ium_column = (self.user_input.replace(' ', '_')).lower()
        elif self.tier == 3:
            self.ium_column = lu_abbr[self.user_input]

    def get_values_ranges(self):
        if self.ium_column[0:12] == 'sum_count_id':
            return default_choices_ranges
        else:
            if self.tier == 3:
                if self.ium_column[0:5] == 'nachr':
                    return  ssx_choice_ranges
                elif self.ium_column[0:4] == 'intr':
                    return ssx_int_ranges
                else:
                    return # TODO MS_SCALE
            else:
                return default_ranges

    def get_style_labels(self):
        if self.ium_column[0:12] == 'sum_count_id':
            return default_choices_labels
        else:
            if self.tier == 3:
                if self.ium_column[0:5] == 'nachr':
                    return ssx_choice_labels
                elif self.ium_column[0:4] == 'intr':
                    return ssx_int_labels
                else:
                    return # TODO MS_SCALE
            else:
                return default_labels

    # function to return color scales
    def get_colour_scale(self):
        if self.tier == 1:
            return colour_scales[self.user_input[:-6]]
        elif self.tier == 2:
            try:
                return colour_scales[self.user_input[10:]]
            except KeyError:
                return colour_scales[self.user_input]
        elif self.tier == 3:
            return colour_scales[self.user_input]

    def get_x_axis(self):
        if self.ium_column[0:19] == 'sum_count_id_social':
            return 'Number of cultural facilities'
        elif self.ium_column[0:12] == 'sum_count_id':
            return 'Number of' + self.user_input[10:]
        else:
            return self.user_input




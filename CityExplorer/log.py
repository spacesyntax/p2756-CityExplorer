
# KPIs

kpis = {'overall':[],
        'liveability': ['vibrancy', 'schools', '- nurseries', '- primary and secondary schools', '- higher education', 'parks', 'cultural facilities'],
        # 'sustainability': ['population coverage', 'energy consumption?'],
        'health': ['sport facilties', 'all healthcare', '- primary healthcare', '- secondary healthcare', 'public transport', 'car dependence', 'walkability']
        }

tier1 = ['final_score', 'liveability_score','sustain_sc', 'health_score']

tier2 = {
'liveability' : ['edu' , 'social', 'act_green', 'mscale_length'],
# 'sustainability': ['pop_score', 'energy_mean_total'],
'health': ['hcare', 'phys', 'pt_stops', 'mixeduse', 'car_depend'],
'overall': ['edu' , 'social', 'act_green', 'mscale_length', 'pop_score', 'energy_mean_total', 'hcare', 'phys', 'pt_stops', 'mixeduse', 'car_depend']
}

tier3 = {
'edu': [ 'edu_nursery', 'edu_secondary', 'edu_higher'],
'hcare': ['hcare_primary', 'hcare_secondary'],
'car_depend': ['jobs']
}

streets = ['multi-scale', 'NACh 2km', 'NACh 10km', 'NAIn 2km', 'NAIn 10km', 'count_id_resi']

# LAND USE ABBREVIATIONS

lu_abbr = {
            'edu': 'educational',
            'edu_nursery':	'nurseries',
            'edu_secondary': 'primary & secondary education',
            'edu_higher': 'higher education faculties',

            'hcare': 'healthcare',
            'hcare_primary': 'primary healthcare facilities',
            'hcare_secondary':	'secondary  healthcare facilities',
             #'resi': 'residential',

            'phys': 'physical activity',
            'social': 'cultural facilities'
}

# COLOURS RANGES

# TODO added light grey
# TODO setup transparency change 'color':'#ffffff' with 'color':'0,0,0,0' - ast 0 is transoarency )

colour_scales = {'overall':         ["#D3D3D3", "#fafafa", "#bcbcbc", "#7f7f7f","#424242", "#050505"],
                 'liveability':     ["#D3D3D3", "#ffffff", "#ecbfbf", "#d98080", "#c64040", "#b30000"],
                 'sustainabilty':   ["#f7fcf5", "#caeac3", "#7bc87c", "#2a924a", "#00441b"],
                 'health':          ["#D3D3D3","#f7fbff", "#c8ddf0", "#73b3d8", "#2879b9", "#2879b9", "#08306b"]}

# MODES

default_modes = [ '10min walk', '15min public transport', '15min car']

modes = {
    'edu': default_modes ,
        'edu_nursery': default_modes,
        'edu_secondary': default_modes,
        'edu_higher': default_modes,
    'social': default_modes,
    'act_green': ['10min walk', '15min public transport'],
    'mscale_length': ['all modes'],
    # TODO add sustainability
    'hcare' : default_modes,
        'hcare_primary': default_modes,
        'hcare_secondary': default_modes,
    'phys': default_modes,
    'pt_stops': default_modes,
    'mixeduse': ['10min walk'],
    'car_depend': ['car:public transport'],
        'jobs': ['30min car', '30min public transport']
}

# RANGES

ranges = [
    [0, 0],
    [0, 0.2],
    [0.2, 0.4],
    [0.4, 0.6],
    [0.6, 0.8],
    [0.8, 1]
]

# MAP LABELS

labels = ['0', '0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1']

# CHART LABELS

# TODO: create a function to get the column name
def get_column(user_input, tier):
    if tier == 1:
        return user_input + '_score'
    elif tier == 2:
        # get land use abbreviations
        try:
            return 'sum_count_id' + lu_abbr[user_input]
        except KeyError:
            # replace _ with spaces
            return



# TODO - change
# include 3, 4 together

kpis = { 'overall':[],
        'liveability': ['vibrancy', 'schools', '- nurseries', '- primary and secondary schools', '- higher education', 'parks', 'cultural facilities'],
        #TODO add sustainability
        # 'sustainability': ['population coverage', 'energy consumption?'],
        'health': ['sport facilties','all healthcare', '- primary healthcare', '- secondary healthcare', 'public transport', 'car dependence', 'walkability'  ]
        }

## colour ranges
# TODO added light grey
# TODO setup transparency change 'color':'#ffffff' with 'color':'0,0,0,0' - ast 0 is transoarency )

colour_scales = {'overall': ["#D3D3D3", "#fafafa", "#bcbcbc", "#7f7f7f","#424242", "#050505"],
                 'liveability': ["#D3D3D3", "#ffffff", "#ecbfbf", "#d98080", "#c64040", "#b30000"],
                 'sustainabilty': ["#f7fcf5", "#caeac3", "#7bc87c", "#2a924a", "#00441b"],
                 'health': ["#D3D3D3","#f7fbff", "#c8ddf0", "#73b3d8", "#2879b9", "#2879b9", "#08306b"]}

## sytem of column names

## tier 1 - index_name (e.g. overall, livability, ...) + '_score'
## tier 2 -  _10_walk
tier1 = ['final_score', 'liveability_score','sustain_sc', 'health_score']

tier2 = {
'liveability' : ['edu' , 'social', 'act_green', 'mscale_length'],
# TODO add sustainability
# 'sustainability': ['pop_score', 'energy_mean_total'],
'health': ['hcare', 'phys', 'pt_stops', 'mixeduse', 'car_depend'],
'overall': ['edu' , 'social', 'act_green', 'mscale_length', 'pop_score', 'energy_mean_total', 'hcare', 'phys', 'pt_stops', 'mixeduse', 'car_depend']
}

tier3 = {
'edu': [ 'edu_nursery', 'edu_secondary', 'edu_higher'],
'hcare': ['hcare_primary', 'hcare_secondary'],
'car_depend': ['jobs']
}

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
streets = ['multi-scale', 'NACh 2km', 'NACh 10km', 'NAIn 2km', 'NAIn 10km', 'count_id_resi']

ranges = [
    [0,0],
    [0, 0.2],
    [0.2, 0.4],
    [0.4, 0.6],
    [0.6, 0.8],
    [0.8, 1]
]
labels = ['0', '0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1']

# ms, nach, in, count_id_resi

# TODO: excel table (old column name - new column name)
# TODO: copy of the ex IUM - change the columns names
#       ALTER TABLE .... RENAME COLUMN x TO y;


# TODO: create a function to get the column name
# def get_column(user_input, tier):
#   if tier == 1:
#       return user_input + '_score'


# TODO: populate drop downs

# TODO: create main visualisation function (see CityZen explorer line 298 in cityzen_explorer_dockwidget.py)
# def update_visualisation_map():
#   # 1. get user input
#   # 2. get colours
# ...
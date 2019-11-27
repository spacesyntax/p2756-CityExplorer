
# TODO - change
# include 3, 4 together

kpi = { 'overall':[],
            'liveability': ['vibrancy', 'schools', '- nurseries', '- primary and secondary schools', '- higher education', 'parks', 'cultural facilities'],
            'sustainabilty': ['population coverage', 'energy consumption?'],
<<<<<<< HEAD
            'health': [ 'sport facilties','all healthcare', '- primary healthcare', '- secondary healthcare', 'public transport', 'car dependence', 'walkability'  ],

=======
            'health': [ 'sport facilties','all healthcare', '- primary healthcare', '- secondary healthcare', 'public transport', 'car dependence', 'walkability'  ]
>>>>>>> cec471e6db30cad356219908a8a95dcce6eda935
        }

## colour ranges
colour_scales = {'overall': ["#fafafa", "#bcbcbc", "#7f7f7f","#424242", "#050505"],
                 'liveability': ["#ffffff", "#ecbfbf", "#d98080", "#c64040", "#b30000"],
                 'sustainabilty': ["#f7fcf5", "#caeac3", "#7bc87c", "#2a924a", "#00441b"],
                 'health': ["#f7fbff", "#c8ddf0", "#73b3d8", "#2879b9", "#2879b9", "#08306b"]}

## sytem of column names

## tier 1 - index_name (e.g. overall, livability, ...) + '_score'
## tier 2 -  _10_walk
tier1 = ['final_score', 'liveability_score','sustain_sc', 'health_score']

tier2 = {
'liveability' : ['edu' , 'social', 'act_green', 'mscale_length'],
'sustainability': ['pop_score', 'energy_mean_total'],
'health': ['hcare', 'phys', 'pt_stops', 'mixeduse', 'car_depend']
}

tier3 = {
'edu': [ 'edu_nursery', 'edu_secondary', 'edu_higher'],
'hcare': ['hcare_primary', 'hcare_secondary'],
'car_depend': ['jobs']
}

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
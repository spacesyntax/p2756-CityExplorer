
# TODO - change
# include 3, 4 together

kpi = { 'overall':[],
            'liveability': ['vibrancy', 'all schools', '- nurseries', '- primary and secondary schools', '- higher education', 'parks', 'cultural facilities'],
            'sustainabilty': ['population coverage', 'energy consumption?'],
            'health': [ 'sport facilties','all healthcare', '- primary healthcare', '- secondary healthcare', 'public transport'. 'car dependence', 'walkability'  ],

        }

## colour ranges
colour_scales = {'overall': ["#fafafa", "#bcbcbc", "#7f7f7f","#424242", "#050505"],
                 'liveability': ["#ffffff", "#ecbfbf", "#d98080", "#c64040", "#b30000"],
                 'sustainabilty': ["#f7fcf5", "#caeac3", "#7bc87c", "#2a924a", "#00441b"],
                 'health': ["#f7fbff", "#c8ddf0", "#73b3d8", "#2879b9", "#2879b9", "#08306b"]}

## sytem of column names

## tier 1 - index_name (e.g. overall, livability, ...) + '_score'
## tier 2 -  _10_walk
tier1 = {'final_score', 'liveability_score','sustain_sc', 'health_score'}

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

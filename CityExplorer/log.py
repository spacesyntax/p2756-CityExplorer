
# TODO - change
# include 3, 4 together

landuses = { 'overall':[],
            'social opportunities': ['unplanned interaction', 'bakery', 'super market', 'cafe', 'restaurant', 'shopping mall', 'convenience store', 'goods store',
                                     'library', 'cultural centre', 'gallery', 'museum', 'cinema/theatre', 'concert hall', 'social', 'place of worship',
                                     'community sports club', 'sports general', 'sports centre', 'gym', 'sports club', 'park'],
            'physical activity': ['walkability', 'community sports club', 'sports general', 'sports centre', 'gym', 'sports club', 'park'],
            'transport': [ 'bus', 'rail', 'metro'],
            'healthcare facilities': ['hospital', 'mental health centre', 'emergency', 'special care', 'rehabilitation centre','dentist', 'hearing centre', 'general practitioner' ]
        }

## colour ranges
colour_scales = {'social opportunities': ["#D3D3D3", "#ffffcc", "#c1e7bc", "#81ceba", "#41b6c4", "#3391bc", "#2966ac", "#253494"],
                'physical activity':["#D3D3D3", "#ffffcc", "#d7efaa", "#a9dc8e", "#78c679", "#48af60","#208f4a", "#006837"],
                'transport': ["#D3D3D3", "#f1eef6", "#e0c8e2",  "#da9acb",  "#df65b0", "#de348a", "#c61266", "#980043"],
                'healthcare facilities': ["#D3D3D3", "#ffffd4", "#ffe6a5", "#fec46c", "#fe9929", "#e67217","#c4500a", "#993404"],
                'ssx':["#0000ff", "#00ffff", "#00ff50", "#ffff00", "#ffa000","#ff0000"]}

## sytem of column names

## tier 1 - index_name (e.g. overall, livability, ...) + '_score'
## tier 2 -  _10_walk
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

land_use_queries = {
'Liveability index' :           "lu_group IN ('edu', 'act_parks') ",
'Access to education':    "lu_group = 'edu'",
'nurseries':	"lu_subgroup	=	'edu_nursery'",
'primary & secondary education':	"lu_subgroup 	=	'edu_secondary'",
'higher education faculties':	"lu_subgroup 	=	'edu_higher'",
'Access to parks':      "lu_group =	'act_parks'",
'Access to cultural facilities': "lu_group =	'social'",
'Health index':                "lu_group IN 	('phys', 'hcare', 'pt_stop')",
'Access to sport facilities': "lu_group =	'phys'",
'Access to healthcare':  "lu_group =	'hcare'",
'primary healthcare facilities': "lu_subgroup =	'hcare_primary'",
'secondary healthcare facilities': "lu_subgroup =	'hcare_secondary'",
'Access to public transport': "lu_group =	'pt_stop'",
'Car dependence': "lu_group IN 	('agri', 'edu', 'hcare', 'indu' , 'office' , 'phys', 'public' , 'retail' , 'tour' , 'comm')",
'Walkability': "lu_group IN 	('comm', 'edu' , 'hcare', 'office' , 'phys' , 'resi', 'retail' , 'social' ) "
}

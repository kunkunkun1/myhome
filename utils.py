a = {
		'iType': '龟丞相',
		'iHp': 397,
		'iMp': 244,
		'iAtt_all': 125,
		'iDef_All': 176,
		'iDex_All': 63,
		'iMagDef_all': 125,
		'life': 9609,
		'yuanxiao': 0,
		'lianshou': 0,
		'left_qlxl': 7,
		'iGrade': 29,
		'iCor_all': 42,
		'iMag_all': 73,
		'iStr_all': 49,
		'iRes_all': 69,
		'iSpe_all': 78,
		'iPoint': 0,
		'grow': 1.049,
		'ruyidan': 0,
		'iBaobao': 0,
		'att': 797,
		'def': 1308,
		'hp': 4782,
		'mp': 1821,
		'spe': 810,
		'dod': 881,
		'qianjinlu': 0,
		'lx': 0,
		'pet_icon': 'https://cbg-xyq.res.netease.com/images/pets/small/102064.gif',
		'genius': 0,
		'genius_skill': {},
		'skill_list': [{
			'icon': 'https://cbg-xyq.res.netease.com/images/pet_child_skill/0313.gif',
			'skill_type': '313',
			'level': 1
		}, {
			'icon': 'https://cbg-xyq.res.netease.com/images/pet_child_skill/0430.gif',
			'skill_type': '430',
			'level': 1
		}, {
			'icon': 'https://cbg-xyq.res.netease.com/images/pet_child_skill/0332.gif',
			'skill_type': '332',
			'level': 1
		}, {
			'icon': 'https://cbg-xyq.res.netease.com/images/pet_child_skill/0328.gif',
			'skill_type': '328',
			'level': 1
		}, {
			'icon': 'https://cbg-xyq.res.netease.com/images/pet_child_skill/0426.gif',
			'skill_type': '426',
			'level': 1
		}],
		'all_skill': '313|430|332|328|426',
		'all_skills': ['313', '430', '332', '328', '426'],
		'equip_list': [None, None, None],
		'neidan': []
	}

if __name__ == '__main__':
    for key,value in a.items():
        if isinstance(value,str):
            s = "{key} = models.CharField(verbose_name='',max_length={length},null=True,blank=True)".format(key=key,length=len(value*2))
        elif isinstance(value,int):
            s = "{key} = models.IntegerField(verbose_name='',null=True,blank=True)".format(key=key)
        print(s)

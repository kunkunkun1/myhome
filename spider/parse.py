
from spider import setting

class Parse:
    def __init__(self, json_data):
        self.json_data = json_data
        self.ResUrl = 'https://cbg-xyq.res.netease.com'

    def _get_role_icon(self, icon):
        if icon > 200:
            kindid = ((icon - 200 - 1) % 12 + 1) + 200
        else:
            kindid = ((icon - 1) % 12 + 1)
        return kindid

    def _get_role_fly_status(self, i3FlyLv, iZhuanZhi):
        fly_status = ""
        if i3FlyLv and i3FlyLv > 0:
            fly_status = "化圣" + setting.CHINESE_NUM_CONFIG[i3FlyLv]
        else:
            if iZhuanZhi >= 0:
                fly_status = setting.ROLE_ZHUAN_ZHI_CONFIG[iZhuanZhi]
        return fly_status

    def _get_role_changesch(self, changesch_data):
        if changesch_data:
            changesch = ','.join([setting.SchoolNameInfo[i]
                                  for i in changesch_data])
        else:
            changesch = "无"
        return changesch

    def _get_role_proKept(self, _prokept, iGrade):

        def parse_single_prop_kept(prop, grade):
            # _this = this;
            attr_list = []
            for key in prop:
                if setting.PROP_KEPT_KEYS[key] and prop[key] >= (grade * 2 + 10):
                    attr_list.append({
                        'key': key,
                        'value': prop[key],
                        'name': setting.PROP_KEPT_KEYS[key]
                    })
            if len(attr_list) < 1:
                return None
            if len(attr_list) < 2:
                return attr_list[0]['name']
            attr_list.sort(key=lambda x: x['value'] or -setting.PROP_KEPT_KEYS_ORDER.index(x['key']))

            return attr_list[0]['name'][0:1] + attr_list[1]['name'][0:1]

        res = []
        if _prokept:
            for i in range(len(_prokept)):
                s = parse_single_prop_kept(_prokept[str(i)], iGrade)
                s and res.append(s)
        propKept = ','.join(res) if len(res) > 0 else '无'
        return propKept

    def _get_role_community_info(self, commu_name, commu_gid):
        if commu_name and commu_gid:
            community_info = str(commu_name) + ":" + str(commu_gid)
        else:
            community_info = "无"
        return community_info

    def parse_role(self):
        '''
        解析角色
        :return:角色字典
        '''
        json_data = self.json_data
        role = {}
        role['iGrade'] = json_data['iGrade']
        role['cName'] = json_data['cName']

        # 角色
        kindid = self._get_role_icon(json_data['iIcon'])
        role['roleKindName'] = setting.RoleKindNameInfo[kindid]
        # 人气
        role['iPride'] = json_data['iPride']
        # 帮派
        role['cOrg'] = json_data['cOrg']
        # 帮贡
        role['iOrgOffer'] = json_data['iOrgOffer']
        # 门派
        role['iSchool'] = setting.SchoolNameInfo[json_data['iSchool']]
        # 门贡
        role['iSchOffer'] = json_data['iSchOffer']
        # 气血
        role['iHp_Max'] = json_data['iHp_Max']
        # 体质
        role['iCor_All'] = json_data['iCor_All']
        # 魔法
        role['iMp_Max'] = json_data['iMp_Max']
        # 魔力
        role['iMag_All'] = json_data['iMag_All']
        # 命中
        role['iAtt_All'] = json_data['iAtt_All']
        # 力量
        role['iStr_All'] = json_data['iStr_All']
        # 伤害
        role['iDamage_All'] = json_data['iDamage_All']
        # 耐力
        role['iRes_All'] = json_data['iRes_All']
        # 防御
        role['iDef_All'] = json_data['iDef_All']
        # 敏捷
        role['iSpe_All'] = json_data['iSpe_All']
        # 速度
        role['iDex_All'] = json_data['iDex_All']
        # 潜力
        role['iPoint'] = json_data['iPoint']
        # 法伤
        role['iTotalMagDam_all'] = json_data['iTotalMagDam_all']
        # 法防
        role['iTotalMagDef_all'] = json_data['iTotalMagDef_all']
        # 获得经验
        role['iUpExp'] = json_data['iUpExp']
        # 已用潜能果数量
        role['iNutsNum'] = json_data['iNutsNum']
        # 新版乾元丹数量
        role['TA_iAllNewPoint'] = json_data['TA_iAllNewPoint']
        # 总经验
        role['sum_exp'] = json_data['sum_exp']
        # 月饼粽子食用量
        role['addPoint'] = json_data['addPoint']
        # 原始种族
        role['ori_race'] = json_data['ori_race']
        # 已获得机缘属性
        role['jiyuan'] = json_data['jiyuan']
        # 飞升/渡劫/化圣
        fly_status = self._get_role_fly_status(json_data['i3FlyLv'],
                                               json_data['iZhuanZhi'])
        role['fly_status'] = fly_status
        # 历史门派
        changesch = self._get_role_changesch(json_data['changesch'])
        role['changesch'] = changesch

        # 属性保存方案
        propKept = self._get_role_proKept(json_data['propKept'], json_data['iGrade'])
        role['propKept'] = propKept
        # 攻击修炼
        role['iExptSki1'] = json_data['iExptSki1']
        # 防御修炼
        role['iExptSki2'] = json_data['iExptSki2']
        # 法术修炼
        role['iExptSki3'] = json_data['iExptSki3']
        # 抗法修炼
        role['iExptSki4'] = json_data['iExptSki4']
        # 猎术修炼
        role['iExptSki5'] = json_data['iExptSki5']
        # 育兽术
        role['yu_shou_shu'] = json_data["all_skills"].get("221", 0)
        # 攻击控制力
        role['iBeastSki1'] = json_data['iBeastSki1']
        # 防御控制力
        role['iBeastSki2'] = json_data['iBeastSki2']
        # 法术控制力
        role['iBeastSki3'] = json_data['iBeastSki3']
        # 抗法控制力
        role['iBeastSki4'] = json_data['iBeastSki4']
        # 房屋
        role['fangwu'] = setting.fangwu_info[json_data['rent_level']]
        # 牧场
        role['muchang'] = setting.muchang_info[json_data['farm_level']]
        # 庭院
        role['tingyuan'] = setting.tingyuan_info[json_data['outdoor_level']]
        # 社区
        community_info = self._get_role_community_info(json_data["commu_name"], json_data["commu_gid"])
        role['shequ'] = community_info
        # 比武积分
        role['HeroScore'] = json_data['HeroScore']
        # 剑会积分
        role['sword_score'] = json_data['sword_score']
        # 三界功绩
        role['datang_feat'] = json_data['datang_feat']

        return role

    def _make_img_name(self, img_name):
        img_id = int(img_name)
        addon = ""
        if img_id < 10:
            addon = "000"
        elif img_id >= 10 and img_id < 100:
            addon = "00"
        elif img_id >= 100 and img_id < 1000:
            addon = "0"

        return addon + str(img_name)

    def _get_skill_icon(self, typeid):
        return self.ResUrl + "/images/role_skills/" + self._make_img_name(typeid) + ".gif"

    def parse_skill(self):
        '''
        解析角色技能
        :return: 角色技能字典
        '''
        json_data = self.json_data
        all_skills = {}
        life_skill = []
        school_skill = []
        ju_qing_skill = []

        raw_skill_info = json_data["all_skills"]
        for _skill in raw_skill_info:
            info = {
                "skill_id": _skill,
                "skill_grade": raw_skill_info[_skill],
                "skill_pos": 0
            }
            info["skill_icon"] = self._get_skill_icon(_skill)

            if setting.skill["life_skill"].get(_skill):
                info["skill_name"] = setting.skill["life_skill"][_skill]
                life_skill.append(info)
            elif setting.skill["school_skill"].get(_skill):
                info["skill_name"] = setting.skill["school_skill"][_skill]["name"]
                info["skill_pos"] = setting.skill["school_skill"][_skill]["pos"]
                school_skill.append(info)
            elif setting.skill["ju_qing_skill"].get(_skill):
                info["skill_name"] = setting.skill["ju_qing_skill"][_skill]
                ju_qing_skill.append(info)

        all_skills['life_skill'] = life_skill
        all_skills['school_skill'] = school_skill
        all_skills['ju_qing_skill'] = ju_qing_skill
        return all_skills

    def _get_equip_info(self, typeid):
        info = setting.equip_info.get(int(typeid))
        result = {
            "name": "",
            "desc": ""
        }
        if info:
            result["name"] = info["name"]
            result["desc"] = info["desc"]

        return result

    def _get_lock_types(self, equip):
        locks = []
        if equip.get("iLock"):
            locks.append(equip["iLock"])
        if equip.get("iLockNew"):
            locks.append(equip["iLockNew"])

        return locks

    def _parse_equip_info(self, AllEquip):
        result = {}

        ResUrl = self.ResUrl

        all_equips = AllEquip

        get_equip_small_icon = lambda itype: ResUrl + "/images/equip/small/" + str(itype) + ".gif"

        get_equip_big_icon = lambda itype: ResUrl + "/images/big/" + str(itype) + ".gif"

        using_equips = []
        not_using_equips = []
        for equip in all_equips:
            equip_info = self._get_equip_info(all_equips[equip]["iType"])
            info = {
                "pos": int(equip),
                "type": all_equips[equip]["iType"],
                "name": equip_info["name"],
                "desc": all_equips[equip]["cDesc"],
                "lock_type": self._get_lock_types(all_equips[equip]),
                "static_desc": equip_info["desc"].replace(r'#R', '<br />').replace(r'#r', '<br />'),
                "small_icon": get_equip_small_icon(all_equips[equip]["iType"]),
                "big_icon": get_equip_big_icon(all_equips[equip]["iType"])
            }

            pos = int(equip)
            if (pos >= 1 and pos <= 6) or (pos in [187, 188, 189, 190]):
                using_equips.append(info)
            else:
                not_using_equips.append(info)

        result["using_equips"] = using_equips
        result["not_using_equips"] = not_using_equips
        return result

    def _get_fabao_info(self, typeid):
        info = setting.fabao_info.get(int(typeid))
        result = {
            "name": "",
            "desc": ""
        }
        if info:
            result["name"] = info["name"]
            result["desc"] = info["desc"]

        return result

    def _parse_fabao_info(self, fabao):
        result = {}
        ResUrl = self.ResUrl
        all_fabao = fabao
        get_fabao_icon = lambda itype: ResUrl + "/images/fabao_new2/" + str(itype) + ".png"

        using_fabao = []

        nousing_fabao = []
        for pos in all_fabao:
            fabao_info = self._get_fabao_info(all_fabao[pos]["iType"])

            info = {
                "pos": int(pos),
                "type": all_fabao[pos]["iType"],
                "name": fabao_info["name"],
                "desc": all_fabao[pos]["cDesc"],
                "icon": get_fabao_icon(all_fabao[pos]["iType"]),
                "static_desc": fabao_info["desc"]
            }
            if info.get('desc'):
                info['desc'] = info['desc'][1:] if info['desc'].startswith('0') else info['desc']

            if int(pos) >= 1 and int(pos) <= 4:
                using_fabao.append(info)
            else:
                nousing_fabao.append(info)

        nousing_fabao.sort(key=lambda x: x['pos'])
        result["using_fabao"] = using_fabao
        result["nousing_fabao"] = nousing_fabao
        return result

    def parse_tool(self):
        '''
        解析道具/法宝
        :return: 返回道具法宝字典
        '''
        tools = {}
        equip_result = self._parse_equip_info(self.json_data["AllEquip"])
        fabao_result = self._parse_fabao_info(self.json_data["fabao"])
        tools['equip_result'] = equip_result
        tools['fabao_result'] = fabao_result
        return tools

    def _safe_attr(self, attr_value, default_value=None):
        if not attr_value:
            return default_value if default_value != None else "未知"
        return attr_value

    def _parse_pet_info(self, info, pet):
        ResUrl = self.ResUrl

        get_pet_icon = lambda itype: ResUrl + "/images/pets/small/" + str(itype) + ".gif"

        max_equip_num = 3

        get_pet_skill_icon = lambda skill_id: ResUrl + "/images/pet_child_skill/" + self._make_img_name(
            skill_id) + ".gif"

        get_pet_equip_icon = lambda typeid: ResUrl + "/images/equip/small/" + str(typeid) + ".gif"

        get_pet_shipin_icon = lambda typeid: ResUrl + "/images/pet_shipin/small/" + str(typeid) + ".png"

        get_child_icon = lambda child_id: ResUrl + "/images/child_icon/" + self._make_img_name(child_id) + ".gif"

        get_child_skill_icon = lambda skill_id: ResUrl + "/images/pet_child_skill/" + self._make_img_name(
            skill_id) + ".gif"

        get_pet_name = lambda itype: setting.pet_info.get(itype)

        get_child_name = lambda itype: setting.child_info.get(itype)

        get_ending_name = lambda itype: setting.ending_info.get(itype)

        get_neidan_icon = lambda neidan_id: ResUrl + "/images/neidan/" + str(neidan_id) + '.jpg'

        info['pet_icon'] = get_pet_icon(pet['iType'])

        info["genius"] = pet["iGenius"]
        if info["genius"] != 0:
            info["genius_skill"] = {
                "icon": get_pet_skill_icon(pet["iGenius"]),
                "skill_type": pet["iGenius"]
            }
        else:
            info["genius_skill"] = {}

        info["skill_list"] = []
        all_skills = pet["all_skills"]
        if all_skills:
            all_skill_str = []
            for typeid in all_skills:
                all_skill_str.append(str(typeid))
                if (int(typeid) == info["genius"]):
                    continue
                info["skill_list"].append({
                    "icon": get_pet_skill_icon(typeid),
                    "skill_type": typeid,
                    "level": all_skills[typeid]})

            info['all_skill'] = '|'.join(all_skill_str)
        else:
            info['all_skill'] = ''

        info['all_skills'] = info['all_skill'].split('|')

        info["equip_list"] = []
        for i in range(max_equip_num):
            item = pet.get("summon_equip" + str((i + 1)))
            if item:
                equip_name_info = self._get_equip_info(item["iType"])
                info["equip_list"].append({
                    "name": equip_name_info["name"],
                    "icon": get_pet_equip_icon(item["iType"]),
                    "type": item["iType"],
                    "desc": item["cDesc"],
                    "lock_type": self._get_lock_types(item),
                    "static_desc": equip_name_info["desc"].replace(r'#R', '<br />').replace(r'#r', '<br />')
                })
            else:
                info["equip_list"].append(None)

        info["neidan"] = []
        if pet["summon_core"]:
            for p in pet["summon_core"]:
                p_core = pet["summon_core"][p]
                info["neidan"].append({
                    "name": self._safe_attr(setting.PetNeidanInfo[int(p)]),
                    "icon": get_neidan_icon(p),
                    "level": p_core[0],
                    'itype': p
                })

    def parse_bb(self):
        '''
        解析宝宝
        :return: 返回宝宝字典
        '''
        allSummon = self.json_data['AllSummon']
        pet_list = []

        if not allSummon: return
        for pet in allSummon:
            info = {}
            info["iTypeid"] = pet["iType"]
            # 类型
            info["iType"] = setting.pet_info[pet["iType"]]
            # 气血
            info["iHp"] = pet["iHp"]
            # 魔法
            info["iMp"] = pet["iMp"]
            # 攻击
            info["iAtt_all"] = pet["iAtt_all"]
            # 防御
            info["iDef_All"] = pet["iDef_All"]
            # 速度
            info["iDex_All"] = pet["iDex_All"]
            # 灵力
            info["iMagDef_all"] = pet["iMagDef_all"]
            # 寿命
            info["life"] = pet["life"]
            # 已用元宵
            info["yuanxiao"] = pet["yuanxiao"]
            # 已用炼兽珍经
            info["lianshou"] = pet["lianshou"]
            # 已用清灵仙露
            info["left_qlxl"] = pet["left_qlxl"]
            # 等级
            info["iGrade"] = pet["iGrade"]
            # 体质
            info["iCor_all"] = pet["iCor_all"]
            # 法力
            info["iMag_all"] = pet["iMag_all"]
            # 力量
            info["iStr_all"] = pet["iStr_all"]
            # 耐力
            info["iRes_all"] = pet["iRes_all"]
            # 敏捷
            info["iSpe_all"] = pet["iSpe_all"]
            # 潜能
            info["iPoint"] = pet["iPoint"]
            # 成长
            info["grow"] = pet["grow"] / 1000
            # 已用如意的
            info["ruyidan"] = pet["ruyidan"]
            # 是否宝宝
            info["iBaobao"] = pet["iBaobao"]
            # 攻击资质
            info["att"] = pet["att"]
            # 防御资质
            info["def"] = pet["def"]
            # 体力资质
            info["hp"] = pet["hp"]
            # 法力资质
            info["mp"] = pet["mp"]
            # 速度资质
            info["spe"] = pet["spe"]
            # 躲闪资质
            info["dod"] = pet["dod"]
            # 已用千金露
            info["qianjinlu"] = pet["qianjinlu"]
            # 灵性
            info["lx"] = pet["jinjie"]['lx']

            # 技能
            self._parse_pet_info(info, pet)

            pet_list.append(info)

        return pet_list

    def _parse_rider_info(self, raw_info):
        ResUrl = self.ResUrl
        rider_name_info = setting.rider_info

        get_rider_icon = lambda itype: ResUrl + "/images/riders/" + str(itype) + ".gif"

        get_skill_icon = lambda typeid: ResUrl + "/images/rider_skill/" + self._make_img_name(typeid) + ".gif"

        all_rider = raw_info.get("AllRider") or {}

        result = []
        for rider in all_rider:
            rider_info = raw_info["AllRider"][rider]
            info = {
                "type": rider_info["iType"],
                "grade": rider_info["iGrade"],
                "exgrow": rider_info["exgrow"] / 10000,
                "icon": get_rider_icon(rider_info["iType"]),
                "type_name": self._safe_attr(rider_name_info[str(rider_info["iType"])]),
                "mattrib": rider_info["mattrib"] if rider_info.get("mattrib") else "未选择",
            }
            info["all_skills"] = []
            all_skills = rider_info["all_skills"]
            for typeid in all_skills:
                info["all_skills"].append({
                    "type": typeid,
                    "icon": get_skill_icon(typeid),
                    "grade": all_skills[typeid]
                })

            result.append(info)

        return result

    def parse_rider_info(self):
        '''
        解析坐骑
        :return: 返回坐骑字典
        '''
        return self._parse_rider_info(self.json_data)

    def _parse_xiangrui_info(self, raw_info):
        ResUrl = self.ResUrl

        all_xiangrui_info = setting.xiangrui_info

        all_skills = setting.xiangrui_skill

        nosale_xiangrui = setting.nosale_xiangrui

        get_xiangrui_icon = lambda itype: ResUrl + "/images/xiangrui/" + str(itype) + ".gif"

        get_skill_icon = lambda: ResUrl + "/images/xiangrui_skills/1.gif"

        all_xiangrui = raw_info.get("HugeHorse")
        if not all_xiangrui:
            return

        result = []
        for pos in all_xiangrui:
            xiangrui_info = all_xiangrui[pos]
            itype = xiangrui_info["iType"]
            info = {
                "type": itype,
                "name": xiangrui_info['cName'] or self._safe_attr(all_xiangrui_info[itype]),
                "icon": get_xiangrui_icon(itype),
                "skill_name": all_skills.get(xiangrui_info['iSkill'], '无'),
                "order": xiangrui_info["order"]
            }
            if xiangrui_info["iSkillLevel"]:
                info["skill_level"] = str(xiangrui_info["iSkillLevel"]) + "级"
            else:
                info["skill_level"] = ""

            result.append(info)

        # result.sort(key=lambda x :x['order'])
        return result

    def parse_xiangrui_info(self):
        '''
        解析祥瑞
        :return:返回祥瑞字典
        '''
        return self._parse_xiangrui_info(self.json_data)

    def _parse_clothes_info(self, raw_info):
        ResUrl = self.ResUrl
        all_clothes_info = setting.clothes_info
        get_clothes_icon = lambda itype: ResUrl + "/images/clothes/" + str(itype) + "0000.gif"

        def get_cloth_name_desc(itype):
            if all_clothes_info.get(itype):
                return all_clothes_info[itype]
            else:
                return {
                    "name": "",
                    "desc": ""
                }

        all_clothes = raw_info["ExAvt"]
        if not all_clothes:
            return

        result = []
        for pos in all_clothes:
            clothes_info = all_clothes[pos]
            clothe_name = clothes_info.get('cName') or self._safe_attr(all_clothes_info[clothes_info["iType"]])
            info = {
                "type": clothes_info["iType"],
                "name": clothe_name,
                "icon": get_clothes_icon(clothes_info["iType"]),
                "order": clothes_info["order"],
                "static_desc": ""
            }
            result.append(info)

        return result

    def parse_clothes_info(self):
        '''解析锦衣'''
        return self._parse_clothes_info(self.json_data)

    def start_parse(self):
        '''开始解析所有字段'''
        result = {}
        result['role_info'] = self.parse_role()
        result['skill_info'] = self.parse_skill()
        result['tool_info'] = self.parse_tool()
        result['pet_info'] = self.parse_bb()
        result['rider_info'] = self.parse_rider_info()
        result['xiangrui_info'] = self.parse_xiangrui_info()
        result['clothes_info'] = self.parse_clothes_info()

        return result

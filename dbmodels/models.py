from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


from dbmodels.manager import ShowImgManager, RightNavManager, MenuManager, TransactionManager


class UserInfo(AbstractUser):
    '''用户信息表'''
    REQUIRED_FIELDS = ['nikename','email','sex']
    sex_choices = ((1,'男'),
                   (2,'女'),)

    nikename = models.CharField(max_length=64,unique=True)
    # pwd = models.CharField(max_length=64)
    # nickname = models.CharField(max_length=16)
    sex = models.IntegerField(choices=sex_choices,null=True,blank=True)
    # email = models.EmailField()
    header_img = models.ImageField(null=True,blank=True)


    def get_absolute_url(self):
        return '1'

class Friends(models.Model):
    '''好友表'''
    user = models.OneToOneField('UserInfo',primary_key=True,on_delete=models.CASCADE)
    friend = models.ForeignKey('self',on_delete=models.CASCADE)


class Transaction(models.Model):
    '''交易帖子'''
    objects = TransactionManager()
    stat_choices = ((0, '售出'), (1, '上架'),)

    team = models.CharField(max_length=64)
    img = models.ImageField(upload_to='indeximg',null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    stat = models.IntegerField(choices=stat_choices,default=1)

    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE)



    class Meta:
        verbose_name_plural = '交易帖子'
        verbose_name = '交易帖子'

    def __str__(self):
        return '%s' % (self.team,)



class Reply(models.Model):
    '''回复表'''
    count = models.IntegerField()
    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction',on_delete=models.CASCADE)

class Collection(models.Model):
    '''收藏表'''
    count = models.IntegerField()
    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction',on_delete=models.CASCADE)

class Watch(models.Model):
    '''查看表'''
    count = models.IntegerField()
    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction',on_delete=models.CASCADE)

class ShowImg(models.Model):
    objects = ShowImgManager()

    stat_choices = ((0,'下架'),(1,'上架'),)
    img_type_choices = ((0,'轮播'),(1,'最热'),(2,'最新'))

    img_type = models.IntegerField(choices=img_type_choices,default=3)
    stat = models.IntegerField(choices=stat_choices,default=1)
    top = models.BooleanField(default=False)
    transcation = models.OneToOneField('Transaction',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '首页图片'
        verbose_name = '首页图片'

    def __str__(self):
        return '%s:%s' % (self.get_img_type_display(),self.transcation.team)

class RightNav(models.Model):
    objects = RightNavManager()
    stat_choices = ((0, '下架'), (1, '上架'),)

    title = models.CharField(max_length=10)
    stat = models.IntegerField(choices=stat_choices, default=1)
    icon = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        verbose_name_plural = '右侧导航'
        verbose_name = '右侧导航'

    def __str__(self):
        return '%s:%s' % (self.title,self.get_stat_display())

class Menu(models.Model):
    objects = MenuManager()
    stat_choices = ((0, '下架'), (1, '上架'),)

    title = models.CharField(max_length=10)
    url = models.CharField(max_length=100,null=True,blank=True)
    parent_menu = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='child')
    stat = models.IntegerField(choices=stat_choices, default=1)

    class Meta:
        verbose_name_plural = '菜单'
        verbose_name = '菜单'

    def __str__(self):
        return '%s:%s' % (self.title,self.get_stat_display())





class RoleBase(models.Model):
    eid = models.CharField(max_length=64)
    equip_name = models.CharField(max_length=16)

    transaction = models.ForeignKey(to='Transaction',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('eid', 'equip_name',)

class Role(models.Model):
    role_base = models.OneToOneField('RoleBase',on_delete=models.CASCADE)

    iGrade = models.IntegerField(verbose_name='等级', null=True, blank=True)
    cName = models.CharField(verbose_name='名称', max_length=10, null=True, blank=True)
    roleKindName = models.CharField(verbose_name='角色', max_length=6, null=True, blank=True)
    iPride = models.IntegerField(verbose_name='人气', null=True, blank=True)
    cOrg = models.CharField(verbose_name='帮派', max_length=10, null=True, blank=True)
    iOrgOffer = models.IntegerField(verbose_name='帮贡', null=True, blank=True)
    iSchool = models.CharField(verbose_name='门派', max_length=4, null=True, blank=True)
    iSchOffer = models.IntegerField(verbose_name='门贡', null=True, blank=True)
    iHp_Max = models.IntegerField(verbose_name='气血', null=True, blank=True)
    iCor_All = models.IntegerField(verbose_name='体质', null=True, blank=True)
    iMp_Max = models.IntegerField(verbose_name='魔法', null=True, blank=True)
    iMag_All = models.IntegerField(verbose_name='魔力', null=True, blank=True)
    iAtt_All = models.IntegerField(verbose_name='命中', null=True, blank=True)
    iStr_All = models.IntegerField(verbose_name='力量', null=True, blank=True)
    iDamage_All = models.IntegerField(verbose_name='伤害', null=True, blank=True)
    iRes_All = models.IntegerField(verbose_name='耐力', null=True, blank=True)
    iDef_All = models.IntegerField(verbose_name='防御', null=True, blank=True)
    iSpe_All = models.IntegerField(verbose_name='敏捷', null=True, blank=True)
    iDex_All = models.IntegerField(verbose_name='速度', null=True, blank=True)
    iPoint = models.IntegerField(verbose_name='潜力', null=True, blank=True)
    iTotalMagDam_all = models.IntegerField(verbose_name='法伤', null=True, blank=True)
    iTotalMagDef_all = models.IntegerField(verbose_name='法防', null=True, blank=True)
    iUpExp = models.IntegerField(verbose_name='获得经验', null=True, blank=True)
    iNutsNum = models.IntegerField(verbose_name='已用潜能果数量', null=True, blank=True)
    TA_iAllNewPoint = models.IntegerField(verbose_name='新版乾元丹数量', null=True, blank=True)
    sum_exp = models.IntegerField(verbose_name='总经验', null=True, blank=True)
    addPoint = models.IntegerField(verbose_name='月饼粽子食用量', null=True, blank=True)
    ori_race = models.IntegerField(verbose_name='原始种族', null=True, blank=True)
    jiyuan = models.IntegerField(verbose_name='已获得机缘属性', null=True, blank=True)
    fly_status = models.CharField(verbose_name='飞升/渡劫/化圣', max_length=6, null=True, blank=True)
    changesch = models.CharField(verbose_name='历史门派', max_length=12, null=True, blank=True)
    propKept = models.CharField(verbose_name='属性保存方案', max_length=10, null=True, blank=True)

class Practice(models.Model):
    role_base = models.OneToOneField('RoleBase', on_delete=models.CASCADE)

    iExptSki1 = models.IntegerField(verbose_name='攻击修炼', null=True, blank=True)
    iExptSki2 = models.IntegerField(verbose_name='防御修炼', null=True, blank=True)
    iExptSki3 = models.IntegerField(verbose_name='法术修炼', null=True, blank=True)
    iExptSki4 = models.IntegerField(verbose_name='抗法修炼', null=True, blank=True)
    iExptSki5 = models.IntegerField(verbose_name='猎术修炼', null=True, blank=True)
    yu_shou_shu = models.IntegerField(verbose_name='育兽术', null=True, blank=True)
    iBeastSki1 = models.IntegerField(verbose_name='攻击控制力', null=True, blank=True)
    iBeastSki2 = models.IntegerField(verbose_name='防御控制力', null=True, blank=True)
    iBeastSki3 = models.IntegerField(verbose_name='法术控制力', null=True, blank=True)
    iBeastSki4 = models.IntegerField(verbose_name='抗法控制力', null=True, blank=True)

class Home(models.Model):
    role_base = models.OneToOneField('RoleBase', on_delete=models.CASCADE)
    fangwu = models.CharField(verbose_name='房屋', max_length=4, null=True, blank=True)
    muchang = models.CharField(verbose_name='牧场', max_length=2, null=True, blank=True)
    tingyuan = models.CharField(verbose_name='庭院', max_length=4, null=True, blank=True)
    shequ = models.CharField(verbose_name='社区', max_length=2, null=True, blank=True)

class Score(models.Model):
    role_base = models.OneToOneField('RoleBase', on_delete=models.CASCADE)
    HeroScore = models.IntegerField(verbose_name='比武积分', null=True, blank=True)
    sword_score = models.IntegerField(verbose_name='剑会积分', null=True, blank=True)
    datang_feat = models.IntegerField(verbose_name='三界功绩', null=True, blank=True)

class Skill(models.Model):
    role_base = models.ForeignKey('RoleBase',on_delete=models.CASCADE)

    skill_type_choices = ((1,'师门技能'),(2,'生活技能'),(3,'剧情技能'),)
    skill_type = models.IntegerField(choices=skill_type_choices)

    from spider.setting import skill
    school_skill_choices = [(int(i),j['name']) for i,j in skill['school_skill'].items()]
    school_skill = models.IntegerField(choices=school_skill_choices,null=True, blank=True)

    life_skill_choices = [(int(i),j) for i,j in skill['life_skill'].items()]
    life_skill = models.IntegerField(choices=life_skill_choices,null=True, blank=True)

    ju_qing_skill_choices = [(int(i),j) for i,j in skill['ju_qing_skill'].items()]
    ju_qing_skill = models.IntegerField(choices=ju_qing_skill_choices,null=True, blank=True)

    skill_grade = models.IntegerField(null=True, blank=True)

from spider.setting import equip_info
equip_choices = [(int(i),j['name']) for i,j in equip_info.items()]
class Tool(models.Model):
    role_base = models.ForeignKey('RoleBase',on_delete=models.CASCADE)

    tool_type_choices = ((0,'装备灵饰'),(1,'装备'),(2,'未装备'),(3,'法宝'),(4,'未装备法宝'))
    tool_type = models.IntegerField(choices=tool_type_choices)

    lingshi = models.IntegerField(choices=equip_choices,null=True, blank=True)
    equip = models.IntegerField(choices=equip_choices,null=True, blank=True)
    no_equip = models.IntegerField(choices=equip_choices,null=True, blank=True)

    from spider.setting import fabao_info
    fabao_choices = [(int(i),j['name']) for i,j in fabao_info.items()]
    fabao = models.IntegerField(choices=fabao_choices,null=True, blank=True)
    no_fabao = models.IntegerField(choices=fabao_choices,null=True, blank=True)

    desc = models.TextField(null=True, blank=True)

class Pet(models.Model):
    role_base = models.ForeignKey('RoleBase',on_delete=models.CASCADE)

    from spider.setting import pet_info
    iType_choices = [(int(i),j) for i,j in pet_info.items()]
    iType = models.IntegerField(verbose_name='类型',choices=iType_choices,null=True,blank=True)

    iHp = models.IntegerField(verbose_name='气血',null=True,blank=True)
    iMp = models.IntegerField(verbose_name='魔法',null=True,blank=True)
    iAtt_all = models.IntegerField(verbose_name='攻击',null=True,blank=True)
    iDef_All = models.IntegerField(verbose_name='防御',null=True,blank=True)
    iDex_All = models.IntegerField(verbose_name='速度',null=True,blank=True)
    iMagDef_all = models.IntegerField(verbose_name='灵力',null=True,blank=True)
    life = models.IntegerField(verbose_name='寿命',null=True,blank=True)
    yuanxiao = models.IntegerField(verbose_name='已用元宵',null=True,blank=True)
    lianshou = models.IntegerField(verbose_name='已用炼兽珍经',null=True,blank=True)
    left_qlxl = models.IntegerField(verbose_name='已用清灵仙露',null=True,blank=True)
    iGrade = models.IntegerField(verbose_name='等级',null=True,blank=True)
    iCor_all = models.IntegerField(verbose_name='体质',null=True,blank=True)
    iMag_all = models.IntegerField(verbose_name='法力',null=True,blank=True)
    iStr_all = models.IntegerField(verbose_name='力量',null=True,blank=True)
    iRes_all = models.IntegerField(verbose_name='耐力',null=True,blank=True)
    iSpe_all = models.IntegerField(verbose_name='敏捷',null=True,blank=True)
    iPoint = models.IntegerField(verbose_name='潜能',null=True,blank=True)
    ruyidan = models.IntegerField(verbose_name='已用如意丹',null=True,blank=True)
    iBaobao = models.IntegerField(verbose_name='是否宝宝',null=True,blank=True)
    att = models.IntegerField(verbose_name='攻击资质',null=True,blank=True)
    def_zz = models.IntegerField(verbose_name='防御资质',null=True,blank=True)
    hp = models.IntegerField(verbose_name='体力资质',null=True,blank=True)
    mp = models.IntegerField(verbose_name='法力资质',null=True,blank=True)
    spe = models.IntegerField(verbose_name='速度资质',null=True,blank=True)
    dod = models.IntegerField(verbose_name='躲闪资质',null=True,blank=True)
    qianjinlu = models.IntegerField(verbose_name='已用千金露',null=True,blank=True)
    lx = models.IntegerField(verbose_name='灵性',null=True,blank=True)
    petSkills = models.CharField(verbose_name='所有技能',null=True,blank=True,max_length=64)

class PetSkill(models.Model):
    role_base = models.ForeignKey('Pet',on_delete=models.CASCADE)

    skill_type_choices = ((1,'认证技能'),(2,'技能'),)
    skill_type = models.IntegerField(choices=skill_type_choices)

    from spider.setting import PetSkillInfo
    pet_skill_choices = [(int(i),j) for i,j in PetSkillInfo.items()]
    pet_skill = models.IntegerField(choices=pet_skill_choices,null=True, blank=True)
    genius_skill = models.IntegerField(choices=pet_skill_choices,null=True, blank=True)

class PetEquip(models.Model):
    role_base = models.ForeignKey('Pet',on_delete=models.CASCADE)

    pet_equip = models.IntegerField(choices=equip_choices,null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

class PetNeiDan(models.Model):
    role_base = models.ForeignKey('Pet',on_delete=models.CASCADE)

    from spider.setting import PetNeidanInfo
    pet_neidan_choices = [(int(i),j) for i,j in PetNeidanInfo.items()]
    pet_neidan = models.IntegerField(choices=pet_neidan_choices,null=True, blank=True)

    level = models.IntegerField(null=True, blank=True)

class Rider(models.Model):
    role_base = models.ForeignKey('RoleBase',on_delete=models.CASCADE)

    from spider.setting import rider_info
    rider_choices = [(int(i),j) for i,j in rider_info.items()]
    rider = models.IntegerField(choices=rider_choices,null=True, blank=True)

    grade = models.IntegerField(verbose_name='等级',null=True, blank=True)
    exgrow = models.FloatField(verbose_name='成长',null=True, blank=True)
    mattrib = models.CharField(verbose_name='属性',null=True, blank=True,max_length=16)

class RiderSkill(models.Model):
    role_base = models.ForeignKey('Rider',on_delete=models.CASCADE)

    itype = models.IntegerField(verbose_name='类型', null=True, blank=True)
    grade = models.IntegerField(verbose_name='等级', null=True, blank=True)

class XiangRui(models.Model):
    role_base = models.ForeignKey('RoleBase',on_delete=models.CASCADE)

    from spider.setting import xiangrui_info
    xiangrui_choices = [(int(i),j) for i,j in xiangrui_info.items()]
    xiangrui = models.IntegerField(choices=xiangrui_choices,null=True, blank=True)

    skill = models.CharField(verbose_name='技能',null=True, blank=True,max_length=16)

class clothes(models.Model):
    role_base = models.ForeignKey('RoleBase',on_delete=models.CASCADE)

    name = models.CharField(verbose_name='名字',null=True, blank=True,max_length=16)


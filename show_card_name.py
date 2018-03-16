# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:24:44 2018

@author: luo xi yang
"""

class Show_Card_Name():
    def __init__(self,name_english,num):
        self.name_english=name_english
        self.num=num
        self.change={'AoMiJiaShou079':'奥米加兽079',
                     'AoMiJiaShou179':'奥米加兽179',
                     'CaiJueShou202':'裁决兽202',
                     'GangDanShou239':'钢弹兽239',
                     'GangHuShou451':'钢虎兽451',
                     'FengHuangShou538':'凤凰兽538',
                     'JiuJiMoShou320':'究极魔兽320',
                     'ChaoBiDuoShou090':'超比多兽090',
                     'AErFaShou002':'阿尔法兽002',
                     'DanDanShou232':'蛋蛋兽232',
                     'DuoLuZhanLongShou237':'多路战龙兽237',
                     'JuLongShou230':'巨龙兽230',
                     'JuJingShou256':'巨鲸兽256',
                     'GaoLiShou037':'高力兽037',
                     'XZhanDouBaoLongShou014':'战斗暴龙兽X014',
                     'XJiXieBaoLongShou234':'机械暴龙兽X234',
                     'DuoLuJiaShou046':'多路加兽046',
                     'QingLongShou010':'青龙兽010',
                     'BaiHuShou021':'白虎兽021',
                     'ZhongZiShou008':'种子兽008',
                     'GuJiaShou228':'古加兽228',
                     'HuoShanShou045':'火山兽045',
                     'DaGuJiaShou087':'大古加兽087',
                     'GangTieHaiLongShou197':'钢铁海龙兽X197',
                     'JiuJiChangJingShou238':'究极长颈兽238',
                     'JiXieZhuangJiaShou093':'机械装甲兽093',
                     'BaoLongShou052':'暴龙兽052',
                     'SangShiBaoLongShou323':'丧尸暴龙兽323',
                     'MieShiLongShou108':'灭世龙兽108',
                     'QianNianShou006':'千年兽006',
                     'WuShiShou428':'武士兽428',
                     'ShengShuShou556':'圣树兽556',
                     'ShuWaShou165':'树蛙兽165',
                     'AnDuoLuLongShou450':'暗多路龙兽450',
                     'JiuJiVLongShou217':'究极V龙兽217',
                     'DiGeShou030':'迪哥兽030',
                     'AiJingLingShou358':'爱精灵兽358',
                     'GuDaiHongCaiShou390':'古代虹彩兽390',
                     'DiLuShou257':'迪路兽257' ,
                     'TianShiShou066':'天使兽066',
                     'BingWuShiShou848':'冰巫师兽848'
                     }
        
    def Turn_English_To_Chinese(self):
        #print('r')
        EnglishName=self.name_english
        length=len(EnglishName)
        name=[]
        for k in range(length):
            for n,v in self.change.items():
                #print(EnglishName[k])
                if EnglishName[k]==n:
                    bb=v
                    name.append(bb)
                else:
                    pass
        #print(name)
        """求不匹配的个数；只保存已经匹配的"""
        count1,name1=0,[]
        for i in range(len(name)):
            name1.append(name[i])
        #print('count1')
        count1=self.num-len(name1)
        print(count1)
        return name1,str(count1)
        

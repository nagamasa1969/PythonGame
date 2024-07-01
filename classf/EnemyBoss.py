from pygame.locals import *
import pygame

class EnemyBoss():
    imgEnemy = ""
    emy_name = ""
    emy_lifemax = ""
    emy_life = ""
    emy_atk = ""
    emy_def = ""
    emy_acy = ""
    emy_eva = ""
    emy_exp = ""
    emy_x = ""
    emy_y = ""
    emy_blink = ""
    dmg_eff = ""
    emy_step = ""
    
    def __init__(self, filename, enemyFlg, EMY_NAME, typ, lev):
        if enemyFlg: #通常的の場合
            #制御情報の初期化
            self.imgEnemy = pygame.image.load(filename + "/image/enemy"+str(typ)+".png")
            self.emy_name = EMY_NAME[typ] + "LV" + str(lev)
            self.emy_lifemax = 60*(typ+1) + lev*10
            self.emy_life = self.emy_lifemax
            self.emy_atk = 20*(typ+3) + lev*10
            self.emy_def = 10*(typ+2) + lev*10
            self.emy_acy = int(self.emy_def/2) + 10*(typ)
            self.emy_eva = int(self.emy_atk/7)
            self.emy_exp = int(self.emy_lifemax/2)
            self.emy_x = int(440 - self.imgEnemy.get_width()/2)
            self.emy_y = 560 - self.imgEnemy.get_height()
            self.emy_blink = 0
            self.dmg_eff = 0
            self.emy_step = 0
        else: #ボスの場合
            imgBoss = pygame.image.load(filename+ "/image/floor_"+str(lev)+"_img.png")
            self.emy_lifemax = EMY_NAME[int(lev/10)-1] + "LV" + str(lev)
            self.emy_lifemax = 300 * lev
            self.emy_life = self.emy_lifemax 
            self.emy_atk = 25 * lev + 100
            self.emy_def = 10 * lev + 50
            self.emy_acy = 10 * lev + 20
            self.emy_eva = 8 * lev + 20
            self.emy_exp = self.emy_lifemax  * 2
            self.emy_x = int(440 - imgBoss.get_width()/2)
            self.emy_y = 560 - imgBoss.get_height()
            self.emy_blink = 0
            self.dmg_eff = 0
            self.emy_step = 0
import pygame
import sys
import random
import psycopg2
from pygame.locals import *
import os
from classf import MapC
from classf import Drawing
from classf import PlayerSet
from classf import CommandData

# 画像の読み込み
filename = os.path.expanduser('~/Desktop/One2')
imgTitle = pygame.image.load(filename + "/image/title.png")
imgExplanation = pygame.image.load(filename + "/image/setumei.png")
imgWall = pygame.image.load(filename + "/image/wall.png")
imgWall2 = pygame.image.load(filename + "/image/wall2.png")
imgDark = pygame.image.load(filename + "/image/dark.png")
imgPara = pygame.image.load(filename + "/image/para.png")
imgBtlBG = pygame.image.load(filename + "/image/btlbg.png")
imgEnemy = pygame.image.load(filename + "/image/enemy0.png")
imgItem = [
    pygame.image.load(filename + "/image/potion.png"),
    pygame.image.load(filename + "/image/blaze_gem.png"),
    pygame.image.load(filename + "/image/spoiled.png"),
    pygame.image.load(filename + "/image/apple.png"),
    pygame.image.load(filename + "/image/meat.png")
]
imgFloor = [
    pygame.image.load(filename + "/image/floor.png"),
    pygame.image.load(filename + "/image/tbox.png"),
    pygame.image.load(filename + "/image/cocoon.png"),
    pygame.image.load(filename + "/image/stairs.png"),
    pygame.image.load(filename + "/image/tbox.png")
]

imgPlayer1 = [
    pygame.image.load(filename + "/image/chara1_0.png"),
    pygame.image.load(filename + "/image/chara1_1.png"),
    pygame.image.load(filename + "/image/chara1_2.png"),
    pygame.image.load(filename + "/image/chara1_3.png"),
    pygame.image.load(filename + "/image/chara1_4.png"),
    pygame.image.load(filename + "/image/chara1_5.png"),
    pygame.image.load(filename + "/image/chara1_6.png"),
    pygame.image.load(filename + "/image/chara1_7.png"),
    pygame.image.load(filename + "/image/chara1_8.png")
]
imgEffect = [
    pygame.image.load(filename + "/image/effect_b.png"),
    pygame.image.load(filename + "/image/allow.png"),
    pygame.image.load(filename + "/image/tue_effect.png")
]
imgBoss = pygame.image.load(filename + "/image/floor_10_img.png")
imgBossField = [
    pygame.image.load(filename + "/image/floor_10.png"),
    pygame.image.load(filename + "/image/floor_20.png"),
    pygame.image.load(filename + "/image/floor_30.png")
]

#DB接続文字列（自宅内の読み込み）
#dsn = "dbname=postgres user=postgres host=192.168.3.7 password=naga1969 port=5432"  #外部PC接続用
dsn = "dbname=game host=localhost user=nagamasa password=naga19691"                  #自分のPC接続用
conn = 1  #１のままの場合DB接続失敗なのでコネクション終了処理を飛ばす
cur = 1   #１のままの場合DB接続失敗なのでコネクション終了処理を飛ばす
try:
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute("select id from test where name = 'MAX';")
    (fl_max,) = cur.fetchone()
except psycopg2.Error as e:
    if conn != 1:
        conn.rollback()
    fl_max = 0
finally:
    if cur != 1:   
        cur.close()
    if conn != 1:
        conn.close()
    
# 変数の宣言
speed = 1         #スピード

#プレイヤー情報初期化
pl_lifemax_s = 250
pl_life_s = pl_lifemax_s
pl_mpmax_s = 100
pl_mp_s = pl_mpmax_s
pl_atk_s = 70
pl_def_s = 50
pl_acy_s = 50
pl_eva_s = 30
pl_p_s = 0
pl_exp_s = 0
max_SP_s = 300
SP_s = max_SP_s
skill_s = 0
pl_lv_s = 1
potion_s = 0
blazegem_s = 0
def_ca_s = 0
def_c_s = 0
skill_c_s = True

#各表示情報
COMMAND = ["[A]ttack", "[P]otion", "[B]laze gem", "[R]un"]
COMMAND1 = ["[A]ttack", "[P]otion", "[B]laze gem", "[K]Skill", "[R]un"]

TRE_NAME = ["Potion", "Blaze gem", "SP spiled", "SP +50", "SP +150",]
EMY_NAME = [
    "Green slim", "Red slime", "Axe beast", "Ogre", "Sword man",
    "Death hornet", "Signal slime", "Devil plant", "Twin killer", "Hell",
    "Snow Man", "Fire Spear", "Fire Sword", "Nemesis", "Adventurer",
    "Human Cat", "Wolf", "Trident", "Ice Girl", "Strongest"
    ]

BOSS_NAME = ["Red Dragon", "Prince", "Deamon"]
SKILL_NAME = ["[1]Back","[2]Shower Arrow MP -30", "[3]Defence Charge MP-20"]

def Save_data(): #セーブする
    global pl_lv, pl_exp, max_exp, potion, blazegem, pl_lifemax, pl_life, def_ca, def_c
    global pl_atk, pl_def, pl_acy, pl_eva, SP, max_SP, skill, pl_mp, pl_mpmax, skill_c
    global floor, pl_p, boss, idx, pl_x, pl_y, dsn
    
    skill_cint = 0
    boss_int = 0
    
    # skill_cフラグを数値に変える
    if(skill_c):
        skill_cint = 1
    else:
        skill_cint = 0
        
    # bossフラグを数値に変える
    if(boss):
        boss_int = 1
    else:
        boss_int = 0
    
    sData = [pl_lv, pl_exp, max_exp, potion, blazegem, pl_lifemax, pl_life, def_ca, def_c,
             pl_atk, pl_def, pl_acy, pl_eva, SP, max_SP, skill, pl_mp, pl_mpmax, skill_cint, floor, pl_p,
             boss_int, CmDt.idx, pl_x, pl_y]
    try:
        conn = 1    #１のままの場合接続に失敗
        cur = 1     #１のままの場合接続に失敗
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()

        cur.execute("DELETE FROM status WHERE id = %s;", "1")
        cur.execute("DELETE FROM map_info WHERE id = %s;", "1")
        conn.commit()
    
        # カウンタ変数
        i = 0
        for dName in sData:
            cur.execute("INSERT INTO status(id, status_name, state, stateid) VALUES(1, 'TEST', %s, %s);", (str(dName), str(i)))
            i += 1
        
        param = 0
        for y in range(DUNGEON_H):
            for x in range(DUNGEON_W):
                param = dungeon[y][x]
                cur.execute("INSERT INTO map_info(id, map_x, map_y, value) VALUES(1, %s, %s, %s);", (str(x), str(y), str(param)))
    
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        if conn != 1:
            conn.rollback()
    finally:
        if cur != 1:   
            cur.close()
        if conn != 1:
            conn.close()

def Load_data(): #ロードする
    global pl_lv, pl_exp, max_exp, potion, blazegem, pl_lifemax, pl_life, def_ca, def_c
    global pl_atk, pl_def, pl_acy, pl_eva, SP, max_SP, skill, pl_mp, pl_mpmax, skill_c
    global floor, pl_p, boss, idx, pl_x, pl_y, dsn
    #データをDBからロードする
    try:
        conn = 1  #１のままの場合DB接続失敗なのでコネクション終了処理を飛ばす
        cur = 1   #１のままの場合DB接続失敗なのでコネクション終了処理を飛ばす
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        cur.execute("select state from status where id = 1 order by stateid;")
        lData= cur.fetchall()
        pl_lv = lData[0][0]
        pl_exp = lData[1][0]
        max_exp = lData[2][0]
        potion = lData[3][0]
        blazegem = lData[4][0]
        pl_lifemax = lData[5][0]
        pl_life = lData[6][0]
        def_ca = lData[7][0]
        def_c = lData[8][0]
        pl_atk = lData[9][0]
        pl_def = lData[10][0]
        pl_acy = lData[11][0]
        pl_eva = lData[12][0]
        SP = lData[13][0]
        max_SP = lData[14][0]
        skill = lData[15][0]
        pl_mp = lData[16][0]
        pl_mpmax = lData[17][0]
        if(lData[18][0] == 0):
            skill_c = False
        else:
            skill_c = True
        floor = lData[19][0]
        pl_p = lData[20][0]
        if(lData[21][0] == 0):
            boss = False
        else:
            boss = True
        CmDt.idx = lData[22][0]
        pl_x = lData[23][0]
        pl_y = lData[24][0]
    
        cur.execute("select * from map_info where id = 1;")
        lDatamap= cur.fetchall()
        for lDatamapValue in lDatamap:
            dungeon[lDatamapValue[2]][lDatamapValue[1]] = lDatamapValue[3]
        cur.close()
    except psycopg2.Error as e:
        if conn != 1:
            conn.rollback()
    finally:
        if cur != 1:   
            cur.close()
        if conn != 1:
            conn.close()

def main():# メイン処理
    global speed, floor, fl_max, welcome, dsn

    pygame.init()
    pygame.display.set_caption("one hour Dungeon Next")
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    #フォント設定s
    font = pygame.font.Font(filename + "/Freesansbold.ttf" , 30)
    fontS = pygame.font.Font(filename + "/Freesansbold.ttf", 20)
    FONT_1 = pygame.font.Font(filename+ "/Freesansbold.ttf", 13)
    se = [ # 効果音とジングル
        pygame.mixer.Sound(filename + "/sound/ohd_se_attack.ogg"),
        pygame.mixer.Sound(filename + "/sound/eff_fireball.ogg"),
        pygame.mixer.Sound(filename + "/sound/se_field_potion.ogg"),
        pygame.mixer.Sound(filename + "/sound/0020.ogg"),
        pygame.mixer.Sound(filename + "/sound/0066levup.ogg"),
        pygame.mixer.Sound(filename + "/sound/0059.ogg"),
        pygame.mixer.Sound(filename + "/sound/miss.ogg"),
        pygame.mixer.Sound(filename + "/sound/eff_magicstart.ogg"),
        pygame.mixer.Sound(filename + "/sound/eff_lightning1.ogg"),
        pygame.mixer.Sound(filename + "/sound/dmg_wind_g.ogg"),
        pygame.mixer.Sound(filename + "/sound/def_up.ogg")
    ]
    point_se = pygame.mixer.Sound(filename + "/sound/point_use.ogg")
    
    #プレイヤークラスの初期化
    plSt = PlayerSet.PlayerSet(pl_lifemax_s, pl_mpmax_s, pl_atk_s,
                pl_def_s, pl_acy_s, pl_eva_s, pl_p_s,
                pl_exp_s, max_SP_s, skill_s, pl_lv_s,
                potion_s, blazegem_s, def_ca_s, def_c_s,
                skill_c_s)
    
    #制御クラスの初期化
    cmDt = CommandData.CommandData(screen, clock, font, fontS, FONT_1,
                                   se, point_se, TRE_NAME, COMMAND,
                                   COMMAND1, SKILL_NAME, EMY_NAME, BOSS_NAME)
    
    #ダンジョンクラスの初期化
    mapCt = MapC.MapC()

    #描画クラスの初期化
    drawCt = Drawing.Drawing(imgTitle, imgExplanation, imgWall,
                        imgWall2, imgDark, imgPara, imgBtlBG,
                        imgEnemy, imgItem, imgFloor, imgPlayer1,
                        imgEffect, imgBoss, imgBossField)
    
    #ゲーム終了まで無限ループさせる
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    speed = speed + 1
                    if speed == 4:
                        speed = 1

        cmDt.tmr = cmDt.tmr + 1 #タイマーを１上昇
        key = pygame.key.get_pressed()
        cmDt.gameControl(filename, drawCt, plSt, mapCt, key)
        drawCt.draw_text(screen, "[S]peed"+str(speed), 740, 40, fontS, drawCt.WHITE)
        plSt.player_exp()
        pygame.display.update()
        clock.tick(6+2*speed)

if __name__ == '__main__':
    main()

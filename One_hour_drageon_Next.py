import pygame
import sys
import random
import psycopg2
from pygame.locals import *
import janome
import os


#色の定義
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
CYAN  = (  0,255,255)
PINK  = (255, 64,255)
BLINK = [(224,255,255), (192,224,255), (128,224,255), (64, 192,255), (128,224,255), (192,240,255)]

# 画像の読み込み
#filename = os.path.abspath(__file__).replace("/One_hour_drageon_Next.py", "")
#filename = os.getcwd()
#filename = "/Users/owner/Desktop/One2"
filename = os.path.expanduser('~/Desktop/One2')
#print(filename)
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
#dsn = "dbname=postgres user=postgres host=192.168.3.7 password=naga1969 port=5432"
dsn = "dbname=game host=localhost user=nagamasa password=scram-sha-256"
try:
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
 
    cur.execute("select id from test where name = 'MAX';")
    (fl_max,) = cur.fetchone()
except psycopg2.Error as e:
    conn.rollback()
    fl_max = 0
finally:
    cur.close()
    conn.close()

# 変数の宣言
speed = 1
idx = 0
tmr = 0
floor = 0
welcome = 0
startInfo = 0

pl_x = 0
pl_y = 0
pl_d = 0
pl_a = 0
pl_lifemax = 0
pl_life = 0
pl_mpmax = 0
pl_mp = 0
pl_atk = 0
pl_def = 0
pl_acy = 0
pl_eva = 0
pl_exp = 0
pl_lv = 1
pl_p = 0
max_exp = 0
SP = 0
max_SP = 0
skill = 0
skill_c = True
def_ca = 0
def_c = 0

potion = 0
blazegem = 0
treasure = 0

emy_name = ""
emy_lifemax = 0
emy_life = 0
emy_atk = 0
emy_def = 0
emy_acy = 0
emy_eva = 0
emy_x = 0
emy_y = 0
emy_step = 0
emy_blink = 0
emy_exp = 0


boss_name = ""
boss_lifemax = 0
boss_life = 0
boss_atk = 0
boss_def = 0
boss_acy = 0
boss_eva = 0
boss_x = 0
boss_y = 0
boss = False
boss_blink = 0
boss_step = 0
boss = True

dmg_eff = 0
btl_cmd = 0
skill_cmd = 0
map_flg = False

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

MAZE_W = 15
MAZE_H = 9
maze = []
for y in range(MAZE_H):
    maze.append([0]*MAZE_W)

DUNGEON_W = MAZE_W*3
DUNGEON_H = MAZE_H*3
dungeon = []
for y in range(DUNGEON_H):
    dungeon.append([0]*DUNGEON_W)
    
def make_dungeon():#　ダンジョンの自動生成
    global floor
    XP = [ 0, 1, 0,-1]
    YP = [-1, 0, 1, 0]
    # 周りの壁
    for x in range(MAZE_W):
        maze[0][x] = 1
        maze[MAZE_H-1][x] = 1
    for y in range(1, MAZE_H-1):
        maze[y][0] = 1
        maze[y][MAZE_W-1] = 1
    # 中を何もない状態に
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            maze[y][x] = 0
    # 柱
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            maze[y][x] = 1
    # 柱から上下左右に壁を作る
    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            d = random.randint(0, 3)
            if x > 2:# 二番目からは左に壁を作らない
                d = random.randint(0, 2)
            maze[y+YP[d]][x+XP[d]] = 1
            
    #　迷路からダンジョンを作る
    #全体を壁にする
    for y in range(DUNGEON_H):
        for x in range(DUNGEON_W):
            dungeon[y][x] = 9
    # 部屋と通路の配置
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            dx = x*3+1
            dy = y*3+1
            if maze[y][x] == 0:
                if random.randint(0, 99) < 20:# 部屋を作る
                    for ry in range(-1, 2):
                        for rx in range(-1, 2):
                            dungeon[dy+ry][dx+rx] = 0
                else: # 通路を作る
                    dungeon[dy][dx] = 0
                    if maze[y-1][x] == 0: dungeon[dy-1][dx] = 0
                    if maze[y+1][x] == 0: dungeon[dy+1][dx] = 0
                    if maze[y][x-1] == 0: dungeon[dy][dx-1] = 0
                    if maze[y][x+1] == 0: dungeon[dy][dx+1] = 0
                        
def boss_dungeon(): # ボスダンジョンの生成
    global floor
    #周りの壁
    for y in range(DUNGEON_H):
        for x in range(DUNGEON_W):
            dungeon[y][x] = 9
    # 中をなにも無い状態に
    for y in range(2, DUNGEON_H-2):
        for x in range(2, DUNGEON_W-2):
            dungeon[y][x] = 0
    # マップの生成
    for y in range(2, 7):
        for x in range(2, 19):
            dungeon[y][x] = 9
    for y in range(2, 7):
        for x in range(24, 43):
            dungeon[y][x] = 9
    for y in range(7, 9):
        for x in range(21):
            dungeon[y][x] = 9
    for y in range(7, 9):
        for x in range(22, 43):
            dungeon[y][x] = 9
    for y in range(18, 20):
        for x in range(21):
            dungeon[y][x] = 9
    for y in range(18, 20):
        for x in range(22, 43):
            dungeon[y][x] = 9
    for y in range(20, 25):
        for x in range(19):
            dungeon[y][x] = 9
    for y in range(20, 25):
        for x in range(24, 43):
            dungeon[y][x] = 9
            
def put_boss_event(): # ボスのフロアにイベントの配置をする
    global pl_x, pl_y, pl_d, pl_a
    #　階段の配置
    y = 4
    x = 21
    dungeon[y][x] = 3
        
    #　繭の配置
    for i in range(15):
        x = random.randint(2, 42)
        y = random.randint(9, 17)
        dungeon[y][x] = 2
    
    # 宝箱の配置
    for i in range(3):
        x = random.randint(2, 42)
        y = random.randint(9, 17)
        dungeon[y][x] = 1
    for y in range(2,3):
        for x in range(19, 24):
            dungeon[y][x] = 4

    # ボスの配置
    boss_y = 8
    boss_x = 21
    dungeon[boss_y][boss_x] = 5
            
    # プレイヤーの配置
    pl_x = 21
    pl_y = 22
    pl_d = 1
    pl_a = 2


def draw_dungeon(bg, fnt, FONT_1):# ダンジョンを描画する
    global floor
    bg.fill(BLACK)
    for y in range(-4, 6):
        for x in range(-5, 6):
            X = (x+5)*80
            Y = (y+4)*80
            dx = pl_x + x
            dy = pl_y + y
            if 0 <= dx and dx < DUNGEON_W and 0 <= dy and dy < DUNGEON_H:
                if dungeon[dy][dx] <= 4:
                    bg.blit(imgFloor[dungeon[dy][dx]], [X, Y])
                if dungeon[dy][dx] == 9:
                    bg.blit(imgWall, [X, Y-40])
                    if dy >= 1 and dungeon[dy-1][dx] == 9:
                        bg.blit(imgWall2, [X, Y-80])
                if dungeon[dy][dx] == 5:
                    bg.blit(imgBossField[int(floor/10)-1], [X, Y])
            if x == 0 and y == 0: #主人公のキャラ表示
                bg.blit(imgPlayer1[pl_a], [X-6, Y-20])
    bg.blit(imgDark, [0, 0]) # 四隅が暗闇の画像を重ねる
    draw_para(bg, fnt, FONT_1) # 主人公の能力を表示
         
def put_event(): # 床にイベントを配置する
    global pl_x, pl_y, pl_d, pl_a
    #　階段の配置
    while True:
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)
        if (dungeon[y][x]) == 0:
           for ry in range(-1, 2): # 階段の周囲を床にする
               for rx in range(-1, 2):
                   dungeon[y+ry][x+rx] = 0
           dungeon[y][x] = 3
           break
    #　繭の配置
    for i in range(35):
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)
        if (dungeon[y][x] == 0):
            dungeon[y][x] = 2
    # 宝箱の配置
    for i in range(10):
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)
        if (dungeon[y][x] == 0 and dungeon[y-1][x] != 3 and dungeon[y+1][x] != 3 and dungeon[y][x+1] != 3 and dungeon[y][x-1] != 3 and dungeon[y-1][x-1] != 3 and dungeon[y+1][x-1] != 3 and dungeon[y+1][x+1] != 3 and dungeon[y-1][x+1] != 3):
            for ry in range(-1, 2): # 宝箱の周囲を床にする
               for rx in range(-1, 2):
                    dungeon[y+ry][x+rx] = 0
            dungeon[y][x] = 1
            
    # プレイヤーの初期配置
    while True:
        pl_x = random.randint(3, DUNGEON_W-4)
        pl_y = random.randint(3, DUNGEON_H-4)
        if(dungeon[pl_y][pl_x] == 0):
            break
    pl_d = 1
    pl_a = 2

def player_exp():# 経験値の管理
    global pl_lv, max_exp, skill

    i = pl_lv - 1
    exp_list = [
                100,200,300,400,650,900,1300,1800,2600,3200,
                4000,5000,6000,7000,8000,9000,10000,11000,12000,13000,
                15000,17000,19000,21000,23000,25000,27000,29000,31000,33000,
                36000,39000,42000,45000,48000,51000,54000,57000,60000,63000,
                68000,73000,78000,83000,88000,93000,98000,103000,108000,113000,
                123000,133000,143000,153000,163000,173000,183000,193000,203000,213000,
                None
                ]
    if i >= 60:
        max_exp *= 1.2
    else:
        max_exp = exp_list[i]
        
    if pl_lv == 5:
        skill = skill + 1
    if pl_lv == 15:
        skill = skill + 1
    
def move_player(key): # 主人公の移動
    global idx, tmr, pl_x, pl_y, pl_d, pl_a, pl_life, SP, max_SP, potion, blazegem, treasure, screen
    global pl_atk, pl_def, pl_acy, pl_eva, pl_p, pl_mp, pl_mpmax, map_flg
    
    point_se = pygame.mixer.Sound(filename + "/sound/point_use.ogg")
    if dungeon[pl_y][pl_x] == 1: # 宝箱に載った
        dungeon[pl_y][pl_x] = 0
        treasure = random.choice([0,0,0,1,1,1,1,1,1,2])
        if treasure == 0:
            potion = potion + 1
        if treasure == 1:
            blazegem = blazegem + 1
        if treasure == 2:
            SP = int(SP/2)
        idx = 3
        tmr = 0
        return
    if dungeon[pl_y][pl_x] == 2: # 繭に載った
        dungeon[pl_y][pl_x] = 0
        r = random.randint(0, 99)
        if r < 25: # 食料
            treasure = random.choice([3,3,3,4])
            if treasure == 3:
                SP = SP + 50
            if SP >= max_SP:
                SP = max_SP
            if treasure == 4:
                SP = SP + 150
            if SP >= max_SP:
                SP = max_SP
            idx = 3
            tmr = 0
        else: # 敵の出現
            idx = 10
            tmr = 0
        return
    if dungeon[pl_y][pl_x] == 3: # 階段に載った
        idx = 2
        tmr = 0
        return
    if dungeon[pl_y][pl_x] == 4: # ボス戦後の宝箱に載った
        dungeon[pl_y][pl_x] = 0
        treasure = random.choice([0,1])
        if treasure == 0:
            potion = potion + 1
        if treasure == 1:
            blazegem = blazegem + 1
        idx = 3
        tmr = 0
        return

    if dungeon[pl_y][pl_x] == 5: # ボスとの戦闘
        dungeon[pl_y][pl_x] = 0
        idx = 24
        tmr = 0
        return
    # 方向キーで上下左右に移動
    x = pl_x
    y = pl_y
    if key[K_UP] == 1:
        pl_d = 0
        if dungeon[pl_y-1][pl_x] != 9:
            pl_y = pl_y - 1
    if key[K_DOWN] == 1:
        pl_d = 1
        if dungeon[pl_y+1][pl_x] != 9:
            pl_y = pl_y + 1
    if key[K_LEFT] == 1:
        pl_d = 2
        if dungeon[pl_y][pl_x-1] != 9:
            pl_x = pl_x - 1
    if key[K_RIGHT] == 1:
        pl_d = 3
        if dungeon[pl_y][pl_x+1] != 9:
            pl_x = pl_x + 1
    pl_a = pl_d*2
    if pl_x != x or pl_y != y: #移動したら食料の量と体力とMPを計算
        pl_a = pl_a + tmr%2 # 移動したら足踏みのアニメーション
        if SP > 0:
            SP = SP - 1
            if pl_life < pl_lifemax:
                pl_life = pl_life + 1
            if pl_mp < pl_mpmax:
                pl_mp = pl_mp + 1
        else:
            pl_life = pl_life - 5
            if pl_life <= 0:
                pl_life = 0
                pygame.mixer.music.stop()
                idx = 9
                tmr = 0
            if pl_mp < pl_mpmax:
                pl_mp = pl_mp + 1   
    # [P]ボタンで回復
    if key[K_p] == 1:
        treasure = 0
        if potion > 0:
            idx = 4
            tmr = 0

    # [B]ボタンでブレイズジェム使用する
    if key[K_b] == 1:
        trasure = 1
        if blazegem > 0:
            idx = 5
            tmr = 0
            
    # [A]ボタンでポイント使用してATKをアップする
    if key[K_a] == 1:
        if pl_p > 0:
            pl_atk = pl_atk + 1
            pl_p = pl_p - 1
            point_se.play()
            
    # [D]ボタンでポイント使用してDEFをアップする
    if key[K_d] == 1:
        if pl_p > 0:
            pl_def = pl_def + 1
            pl_p = pl_p - 1
            point_se.play()
    # [C]ボタンでポイント使用してACYをアップする
    if key[K_c] == 1:
        if pl_p > 0:
            pl_acy = pl_acy + 1
            pl_p = pl_p - 1
            point_se.play()
            
    # [E]ボタンでポイント使用してATKをアップする
    if key[K_e] == 1:
        if pl_p > 0:
            pl_eva = pl_eva + 1
            pl_p = pl_p - 1
            point_se.play()
    
    # [M]ボタンでマップ表示の切り替え
    if key[K_m] == 1:
        if map_flg == True:
            map_flg = False
        else:
            map_flg = True
            
    # [q]ボタンで大画面表示
    if key[K_q] == 1:
        screen = pygame.display.set_mode(
        (880, 680),
        pygame.FULLSCREEN
        )
        
    # [w]ボタンで通常表示
    if key[K_w] == 1:
        screen = pygame.display.set_mode((880, 720))
    
    # [V]ボタンでセーブ
    if key[K_v] == 1:
        Save_data()
        idx = 27
            
def draw_text(bg, txt, x,  y, fnt, col): # 影付き文字の表示
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur,[x+1, y+2])
    sur = fnt.render(txt, True, col) 
    bg.blit(sur, [x, y])

def draw_para(bg, fnt, FONT_1): #主人公の能力表示
    X = 30 
    Y = 600
    bg.blit(imgPara, [X, Y])
    col = WHITE
    if pl_life < int(pl_lifemax/5) and tmr%2 == 0: col = RED
    draw_text(bg, "{}/{}".format(pl_life, pl_lifemax), X+83, Y+4, FONT_1, col)
    draw_text(bg, str(pl_atk),X+190, Y+6, FONT_1, WHITE)
    draw_text(bg, str(pl_def),X+190, Y+25, FONT_1, WHITE)
    draw_text(bg, str(pl_acy),X+35, Y+62, FONT_1, WHITE)
    draw_text(bg, str(pl_eva),X+100, Y+62, FONT_1, WHITE)
    draw_text(bg, str(pl_lv),X+27, Y+48, FONT_1, WHITE)
    draw_text(bg, "{}/{}".format(pl_exp, max_exp), X+175, Y+62, FONT_1, WHITE)
    draw_text(bg, "{}/{}".format(pl_mp, pl_mpmax), X+83, Y+19, FONT_1, WHITE)
    col = WHITE
    if SP == 0 and tmr%2 == 0: col = RED
    draw_text(bg, "{}/{}".format(SP, max_SP), X+83, Y+35, FONT_1, col)
    draw_text(bg, str(potion), X+266, Y+6, FONT_1, WHITE)
    draw_text(bg, str(blazegem), X+266, Y+25, FONT_1, WHITE)

def init_battle(): # 戦闘に入る準備をする
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_x, emy_y, emy_exp, emy_atk, emy_def, emy_acy, emy_eva
    typ = random.randint(0, floor)
    if floor >= 20:
        typ = random.randint(0, 19)
    lev = random.randint(int(floor/2)+1, floor)
    imgEnemy = pygame.image.load(filename + "/image/enemy"+str(typ)+".png")
    emy_name = EMY_NAME[typ] + "LV" + str(lev)
    emy_lifemax = 60*(typ+1) + lev*10
    emy_life = emy_lifemax
    emy_atk = 20*(typ+3) + lev*10
    emy_def = 10*(typ+2) + lev*10
    emy_acy = int(emy_def/2) + 10*(typ)
    emy_eva = int(emy_atk/7)
    emy_exp = int(emy_lifemax/2)
    emy_x = int(440-imgEnemy.get_width()/2)
    emy_y = 560-imgEnemy.get_height()

def draw_bar(bg, x, y, w, h, val, ma):# 敵の体力を表示するバー
    pygame.draw.rect(bg, WHITE, [x-2, y-2, w+4, h+4])
    pygame.draw.rect(bg, BLACK, [x, y, w, h])
    if val > 0:
        pygame.draw.rect(bg, (0, 128, 255), [x, y, int(w*val/ma), h])

def draw_battle(bg, fnt, FONT_1): # 戦闘画面の描画
    global emy_blink, dmg_eff
    bx = 0
    by = 0
    if dmg_eff > 0:
        dmg_eff = dmg_eff - 1
        bx = random.randint(-20, 20)
        by = random.randint(-10, 10)
    bg.blit(imgBtlBG, [bx, by])
    if emy_life > 0 and emy_blink%2 == 0:
        bg.blit(imgEnemy, [emy_x, emy_y+emy_step])
    draw_bar(bg, 340, 580, 200, 10, emy_life, emy_lifemax)
    if emy_blink > 0:
        emy_blink = emy_blink - 1
    for i in range(10): # 戦闘メッセージの表示
        draw_text(bg, message[i], 600, 100+i*50, fnt, WHITE)
    draw_para(bg, fnt, FONT_1) # 主人公の能力を表示

def init_boss_battle(): # ボスの戦闘に入る準備をする
    global imgBoss, boss_name, boss_lifemax, boss_life, boss_x, boss_y, boss_exp, boss_atk, boss_def, boss_acy, boss_eva, floor
    lev = floor
    imgBoss = pygame.image.load(filename+ "/image/floor_"+str(floor)+"_img.png")
    boss_name = BOSS_NAME[int(floor/10)-1] + "LV" + str(lev)
    boss_lifemax = 300*floor
    boss_life = boss_lifemax
    boss_atk = 25*floor + 100
    boss_def = 10*floor + 50
    boss_acy = 10*floor + 20
    boss_eva = 8*floor + 20
    boss_exp = boss_lifemax * 2
    boss_x = int(440-imgBoss.get_width()/2)
    boss_y = 560-imgBoss.get_height()

def draw_boss_battle(bg, fnt, FONT_1): # ボスの戦闘画面の描画
    global boss_blink, dmg_eff
    boss_bx = 0
    boss_by = 0
    if dmg_eff > 0:
        dmg_eff = dmg_eff - 1
        boss_bx = random.randint(-20, 20)
        boss_by = random.randint(-10, 10)
    bg.blit(imgBtlBG, [boss_bx, boss_by])
    if boss_life > 0 and boss_blink%2 == 0:
        bg.blit(imgBoss, [boss_x, boss_y+boss_step])
    draw_bar(bg, 340, 580, 200, 10, boss_life, boss_lifemax)
    if boss_blink > 0:
        boss_blink = boss_blink - 1
    for i in range(10): # 戦闘メッセージの表示
        draw_text(bg, message[i], 600, 100+i*50, fnt, WHITE)
    draw_para(bg, fnt, FONT_1) # 主人公の能力を表示
    
def battle_command(bg, fnt, key): # コマンドの入力と表示
    global btl_cmd, skill, skill_cmd, skill_c, pl_lv
    ent = False
    if key[K_a] and skill_c == True: # Aキー
        btl_cmd = 0
        ent = True
    if key[K_p] and skill_c == True: # Pキー
        btl_cmd = 1
        ent = True
    if key[K_b] and skill_c == True: # Bキー
        btl_cmd = 2
        ent = True
    if skill >= 1:
        if key[K_k] and skill_c == True:# Kキー
            skill_c = False
    if key[K_r] and skill_c == True: # Rキー
        if skill == 0:
            btl_cmd = 3
            ent = True
        else:
            btl_cmd = 4
            ent = True
    if key[K_1]and skill_c == False:# 1キー
        skill_cmd = 0
        ent = True
    if key[K_2]and skill_c == False:# 2キー
        skill_cmd = 1
        ent = True
    if pl_lv >= 15:
        if key[K_3] and skill_c == False:# 3キー
            skill_cmd = 2
            ent = True
    if key[K_UP]: # ↑キー
        if btl_cmd > 0 and skill_c == True:
            btl_cmd -= 1
        if skill_cmd > 0 and skill_c == False:
            skill_cmd -= 1       
    if key[K_DOWN]: # ↓キー
        if skill == 0 and btl_cmd < 3:
            btl_cmd += 1
        if skill >= 1 and btl_cmd < 4 and skill_c == True:
            btl_cmd += 1
        if pl_lv <= 5 and skill_c == False:
            if skill_cmd < 1:
                skill_cmd += 1
        if pl_lv >= 15 and skill_c == False:
            if skill_cmd < 2:
                skill_cmd += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
            
    if skill <= 1:
        for i in range(4):
            c = WHITE
            if btl_cmd == i: c = BLINK[tmr%6]
            draw_text(bg, COMMAND[i], 20, 360+i*60, fnt, c)
    if skill >= 1:
        if skill_c == True:
            for i in range(5):
                c = WHITE
                if btl_cmd == i: c = BLINK[tmr%6]
                draw_text(bg, COMMAND1[i], 20, 320+i*60, fnt, c)
        if skill_c == False and pl_lv <= 14:
            for i in range(2):
                c = WHITE
                if skill_cmd == i: c = BLINK[tmr%6]
                draw_text(bg, SKILL_NAME[i], 20, 360+i*60, fnt, c)
        if skill_c == False and pl_lv >= 15:
            for i in range(3):
                c = WHITE
                if skill_cmd == i: c = BLINK[tmr%6]
                draw_text(bg, SKILL_NAME[i], 20, 360+i*60, fnt, c)
    return ent
    #return skill_c

# 戦闘メッセージの表示処理
message = [""]*(10)
def init_message():
    for i in range(10):
        message[i] = ""

def set_message(msg):
    for i in range(10):
        if message[i] == "":
            message[i] = msg
            return
    for i in range(9):
        message[i] = message[i+1]
    message[9] = msg

def Map_info(bg):
    global pl_y, pl_x, pl_a
    pygame.draw.rect(bg,BLACK,Rect(90,100,700,400))
    for y in range(0, 27):
        for x in range(0, 45):
            my = (y * 15) + 1
            mx = (x * 15) + 1
            if dungeon[y][x] == dungeon[pl_y][pl_x]:
                bg.blit(pygame.transform.scale(imgPlayer1[pl_a], [50, 50]), [64 + (pl_x * 15 + 1), 65 + (pl_y * 15 + 1)])
            for rmy in range(-8, 8):
                for rmx in range(-8, 8):
                    if dungeon[y][x] != 9:
                        pygame.draw.rect(bg,WHITE,Rect(90 + mx + rmx,100 + my + rmy,1,1))

def Save_data():
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
             boss_int, idx, pl_x, pl_y]
    #dsn = "dbname=game host=localhost user=nagamasa password=scram-sha-256 port=5432"
    #dsn = "dbname=game host=60.120.72.111 user=nagamasa password=scram-sha-256 port=5432"
    try:
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
    except:
        conn.rollback()
    finally:
        conn.close()

def Load_data():
    global pl_lv, pl_exp, max_exp, potion, blazegem, pl_lifemax, pl_life, def_ca, def_c
    global pl_atk, pl_def, pl_acy, pl_eva, SP, max_SP, skill, pl_mp, pl_mpmax, skill_c
    global floor, pl_p, boss, idx, pl_x, pl_y, dsn
    try:
        #dsn = "dbname=game host=localhost user=nagamasa password=scram-sha-256"
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
        idx = lData[22][0]
        pl_x = lData[23][0]
        pl_y = lData[24][0]
    
        cur.execute("select * from map_info where id = 1;")
        lDatamap= cur.fetchall()
        for lDatamapValue in lDatamap:
            dungeon[lDatamapValue[2]][lDatamapValue[1]] = lDatamapValue[3]
        cur.close()
    except:
        conn.rollback()
    finally:
        conn.close()
    #cur.execute("select id from test where name = 'MAX';")
    #(floor,) = cur.fetchone()

def main():# メイン処理
    global speed, idx, tmr, floor, fl_max, welcome
    global pl_a, pl_lv, pl_exp, max_exp, potion, blazegem, pl_lifemax, pl_life, def_ca, def_c
    global pl_atk, pl_def, pl_acy, pl_eva, SP, max_SP, skill, pl_mp, pl_mpmax, skill_c
    global emy_life, emy_step, emy_blink, dmg_eff, emy_exp, emy_atk, pl_x, pl_y
    global emy_def, emy_acy, emy_eva, boss_step, boss_blink, pl_p, boss
    global boss_life, boss_exp, boss_atk, boss_def, boss_acy, boss_eva, map_flg, dsn
    dmg = 0
    lif_p = 0
    atk_p = 0

    pygame.init()
    pygame.display.set_caption("one hour Dungeon Next")
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font(filename + "/Freesansbold.ttf" , 30)
    fontS = pygame.font.Font(filename + "/Freesansbold.ttf", 20)
    FONT_1 = pygame.font.Font(filename+ "/Freesansbold.ttf", 13)
    #font = pygame.font.Sysfont("Arial", 40)
    #fontS = pygame.font.Sysfont("Arial", 30)
    #FONT_1 = pygame.font.Sysfont("Arial", 23)
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

        tmr = tmr + 1
        key = pygame.key.get_pressed()

        if idx == 0: # タイトル画面
            if tmr == 1:
                pygame.mixer.music.load(filename + "/sound/0071.ogg")
                pygame.mixer.music.play(-1)
            screen.fill(BLACK)
            screen.blit(imgTitle, [40, 60])
            if fl_max >= 0:
                draw_text(screen, "You reached floor {}.".format(fl_max), 300, 460, font, CYAN)
            draw_text(screen, "Press space key", 320, 560, font, BLINK[tmr%6]) 
            #pygame.draw.rect(screen,WHITE,Rect(200,450,450,200))
            if key[K_SPACE] == 1:
                pygame.draw.rect(screen,BLACK,Rect(300,450,400,200))
                startInfo = 0
                idx = 26

        elif idx == 1: # プレイヤーの移動
            move_player(key)
            draw_dungeon(screen, fontS, FONT_1)
            draw_text(screen, "floor {} ({},{})".format(floor, pl_x, pl_y), 60, 40, fontS, WHITE)
            draw_text(screen, "[P] = potion use", 330, 600, FONT_1, WHITE)
            draw_text(screen, "[B] = Blaze gem use", 330, 620, FONT_1, WHITE)
            draw_text(screen, "[M] = Map View", 330, 640, FONT_1, WHITE)
            draw_text(screen, "[A] ATK+1 [D] DEF+1 [C] ACY+1 [E] EVA+1", 30, 560, FONT_1, WHITE)
            draw_text(screen, "[Q] WideScreen [W] DefaultScreen [V]Save", 30, 580, FONT_1, WHITE)
            draw_text(screen,"Point : " + str(pl_p), 30, 540, FONT_1, WHITE)
            if map_flg:
                Map_info(screen)
            if welcome > 0:
                welcome = welcome - 1
                draw_text(screen,"Welcome to floor {}.".format(floor), 300, 180, font, CYAN)

        elif idx == 2: # 画面の切替
            draw_dungeon(screen, fontS, FONT_1)
            if 1 <= tmr and tmr <= 5:
                h = 80*tmr
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
            if tmr == 5:
                floor = floor + 1
                if floor > fl_max:
                    fl_max = floor
                    try:
                        #dsn = "dbname=game host=localhost user=nagamasa password=scram-sha-256"
                        #dsn = "dbname=game user=nagamasa password=scram-sha-256 port=5432"
                        conn = psycopg2.connect(dsn)
                        cur = conn.cursor()
                        cur.execute("UPDATE test SET id = %s", (fl_max,))
                        conn.commit()
                        cur.execute("select id from test where name = 'MAX';")
                        (fl_max,) = cur.fetchone()
                        cur.close()
                    except:
                        conn.rollback()
                    finally:
                        conn.close()
                welcome = 15
            if tmr == 6:
                if floor == 10 or floor == 20 or floor == 30:
                    boss_dungeon()
                    put_boss_event()
                else:
                    make_dungeon()
                    put_event()
            if 7 <= tmr and tmr <= 10:
                h = 80*(10-tmr)
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
            if tmr == 11:
                if floor == 11:
                    pygame.mixer.music.load(filename + "/sound/0021.ogg")
                    pygame.mixer.music.play(-1)
                if floor == 21:
                    pygame.mixer.music.load(filename + "/sound/0070.ogg")
                    pygame.mixer.music.play(-1)
            if tmr == 12:
                idx = 1

        elif idx == 3: # アイテム入手もしくはトラップ
            draw_dungeon(screen, fontS, FONT_1)
            screen.blit(imgItem[treasure], [320, 220])
            draw_text(screen, TRE_NAME[treasure], 380, 240, font, WHITE)
            if tmr == 10:
                idx = 1
                
        elif idx == 4: # フィールドアイテム使用(ポーション)
            draw_dungeon(screen, fontS, FONT_1)
            screen.blit(imgItem[0], [320, 220])
            draw_text(screen, TRE_NAME[0], 380, 240, font, WHITE)
            if tmr == 1:
                set_message("Potion!")
                pygame.mixer.Sound(filename + "/sound/se_field_potion.ogg").play()
            if tmr == 5:
                pl_life = pl_life + 1000
                if pl_life >= pl_lifemax:
                    pl_life = pl_lifemax
                potion = potion - 1
            if tmr == 10:
                idx = 1
                
        elif idx == 5: # フィールドアイテム使用(ブレイズジェム)
            draw_dungeon(screen, fontS, FONT_1)
            screen.blit(imgItem[1], [320, 220])
            draw_text(screen, TRE_NAME[1], 380, 240, font, WHITE)
            img_rz = pygame.transform.rotozoom(imgEffect[1], 30*tmr, (12-tmr)/8)
            X = int(440-img_rz.get_width()/2)
            Y = int(360-img_rz.get_height()/2)
            screen.blit(img_rz, [X, Y])
            if tmr == 1:
                set_message("Blaze gem!")
                pygame.mixer.Sound(filename + "/sound/eff_fireball.ogg").play()
            if tmr == 6:
                blazegem = blazegem - 1
            if tmr == 11:
                if dungeon[pl_y-1][pl_x] == 2:
                    dungeon[pl_y-1][pl_x] = 0
            if tmr == 12:
                if dungeon[pl_y+1][pl_x] == 2:
                    dungeon[pl_y+1][pl_x] = 0
            if tmr == 13:
                if dungeon[pl_y][pl_x-1] == 2:
                    dungeon[pl_y][pl_x-1] = 0
            if tmr == 14:
                if dungeon[pl_y][pl_x+1] == 2:
                    dungeon[pl_y][pl_x+1] = 0
            if tmr == 15:
                if dungeon[pl_y-1][pl_x+1] == 2:
                    dungeon[pl_y-1][pl_x+1] = 0
            if tmr == 16:
                if dungeon[pl_y-1][pl_x-1] == 2:
                    dungeon[pl_y-1][pl_x-1] = 0
            if tmr == 17:
                if dungeon[pl_y+1][pl_x-1] == 2:
                    dungeon[pl_y+1][pl_x-1] = 0
            if tmr == 18:
                if dungeon[pl_y+1][pl_x+1] == 2:
                    dungeon[pl_y+1][pl_x+1] = 0
            if tmr == 20:
                idx = 1

        elif idx == 9: # ゲームオーバー
            if tmr <= 30:
                PL_TURN = [2, 4, 0, 6]
                pl_a = PL_TURN[tmr%4]
                if tmr == 30: pl_a = 8 # 倒れた絵
                draw_dungeon(screen, fontS, FONT_1)
            elif tmr == 31:
                se[3].play()
                draw_text(screen, "You died.", 360, 240, font, RED)
                draw_text(screen, "Game over.", 360, 380, font, RED)
            elif tmr == 120:
                idx = 0
                tmr = 0

        elif idx == 10: # 戦闘開始
            if tmr == 1:
                pygame.mixer.music.load(filename+ "/sound/0154.ogg")
                pygame.mixer.music.play(-1)
                init_battle()
                init_message()
            elif tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(imgBtlBG, [bx, by])
                draw_text(screen, "Encounter!", 350, 200, font, WHITE)
            elif tmr <= 16:
                draw_battle(screen, fontS, FONT_1)
                draw_text(screen, emy_name+" apper!", 300, 200,font, WHITE)
            else:
                tmr == 17
            if tmr == 17:
                if pl_eva >= emy_eva:
                    idx = 11
                    tmr = 0
                else:
                    idx = 13
                    tmr = 0

        elif idx == 11: # プレイヤーのターン(入力待ち)
            if boss == False:
                draw_battle(screen, fontS, FONT_1)
            if boss == True:
                draw_boss_battle(screen, fontS, FONT_1)
            if tmr == 1:set_message("You turn.")
            if skill == 0:
                if battle_command(screen, font, key) == True:
                    if btl_cmd == 0:
                        idx = 12
                        tmr = 0
                    if btl_cmd == 1 and potion > 0:
                        idx = 20
                        tmr = 0
                    if btl_cmd == 2 and blazegem > 0:
                        idx = 21
                        tmr = 0
                    if btl_cmd == 3:
                        idx = 14
                        tmr = 0
            if skill >= 1:
                if skill_c == True:
                    if battle_command(screen, font, key) == True:
                        if btl_cmd == 0:
                            idx = 12
                            tmr = 0
                        if btl_cmd == 1 and potion > 0:
                            idx = 20
                            tmr = 0
                        if btl_cmd == 2 and blazegem > 0:
                            idx = 21
                            tmr = 0
                        if btl_cmd == 3:
                            idx = 18
                            tmr = 0
                        if btl_cmd == 4:
                            idx = 14
                            tmr = 0
                if skill_c == False:
                    if battle_command(screen, font, key) == True:
                        if skill_cmd == 0:
                            skill_c = True
                        if skill_cmd == 1:
                            idx = 19
                            tmr = 0
                        if pl_lv >= 15:
                            if skill_cmd == 2:
                                idx = 23
                                tmr = 0
                            
        elif idx == 12: # プレイヤーの攻撃
            if boss == False:
                draw_battle(screen, fontS, FONT_1)
            if boss == True:
                draw_boss_battle(screen, fontS, FONT_1)
            if tmr == 1:
                set_message("You attack!")
                if boss == False:
                    pl_hit = 70 + pl_acy - emy_eva
                if boss == True:
                    pl_hit = 70 + pl_acy - boss_eva
                if pl_hit >= 100:
                    pl_hit = 99
                if pl_hit < 0:
                    pl_hit = 0
                hit = random.randint(1, 100)
                if boss == False:
                    if hit <= pl_hit:
                        dmg = pl_atk - emy_def + int(pl_atk/random.randint(10,13))
                        if dmg <= 0:
                            dmg = 0
                    else:
                        se[6].play()
                        dmg = 0
                        tmr = 6
                if boss == True:
                    if hit <= pl_hit:
                        dmg = pl_atk - boss_def + int(pl_atk/random.randint(10,13))
                        if dmg <= 0:
                            dmg = 0
                    else:
                        se[6].play()
                        dmg = 0
                        tmr = 6                
            if tmr == 2:
                se[9].play()
                img_3 = imgEffect[2]
                X = 440-int(img_3.get_width()/2)
                Y = 300-int(img_3.get_height()/2)
                screen.blit(img_3, [X, Y])
            if tmr == 3:
                img_3 = imgEffect[2]
                X = 520-int(img_3.get_width()/2)
                Y = 460-int(img_3.get_height()/2)
                screen.blit(img_3, [X, Y])
            if tmr == 4:
                se[9].play()
                img_3 = imgEffect[2]
                X = 440-int(img_3.get_width()/2)
                Y = 530-int(img_3.get_height()/2)
                screen.blit(img_3, [X, Y])
                
            if tmr == 5:
                if boss == False:
                    emy_blink = 5
                if boss == True:
                    boss_blink = 5
                set_message(str(dmg)+"pts of damege!")
                tmr = 11
            if tmr ==6:
                set_message("miss")
                tmr = 16
            if tmr == 11:
                if boss == False:
                    emy_life = emy_life - dmg
                    if emy_life <= 0:
                        emy_life = 0
                        idx = 16
                        tmr = 0
                if boss == True:
                    boss_life = boss_life -dmg
                    if boss_life <= 0:
                        boss_life = 0
                        idx = 16
                        tmr = 0
            if tmr == 16:
                idx = 13
                tmr = 0

        elif idx == 13: # 敵のターン
            if boss == False:
                draw_battle(screen, fontS, FONT_1)
            if boss == True:
                draw_boss_battle(screen, fontS, FONT_1)
            if tmr == 2:
                set_message("Enemy turn.")
            if tmr == 5:
                if boss == False:
                    set_message(emy_name + " attack!")
                    emy_step = 30
                    emy_hit = 70 + emy_acy - pl_eva
                    if emy_hit >= 100:
                        emy_hit = 99
                    e_hit = random.randint(1, 100)
                    if e_hit <= emy_hit:
                        se[0].play()
                    else:
                        se[6].play()
                        dmg = 0
                        tmr = 12
                if boss == True:
                    set_message(boss_name + " attack!")
                    boss_step = 30
                    emy_hit = 70 + boss_acy - pl_eva
                    if emy_hit >= 100:
                        emy_hit = 99
                    e_hit = random.randint(1, 100)
                    if e_hit <= emy_hit:
                        se[0].play()
                    else:
                        se[6].play()
                        dmg = 0
                        tmr = 12
            if tmr == 9:
                if boss == False:
                    dmg = emy_atk - pl_def + int(emy_atk/random.randint(10,13))
                    if dmg <= 0:
                        dmg = 0
                    set_message(str(dmg)+"pts of damege!")
                    dmg_eff = 5
                    emy_step = 0
                if boss == True:
                    dmg = boss_atk - pl_def + int(emy_atk/random.randint(10,13))
                    if dmg <= 0:
                        dmg = 0
                    set_message(str(dmg)+"pts of damege!")
                    dmg_eff = 5
                    boss_step = 0
                tmr = 15
            if tmr == 12:
                set_message("miss")
                tmr = 20
                emy_step = 0
            if tmr == 15:
                pl_life = pl_life - dmg
                if pl_life <= 0:
                    pl_life = 0
                    idx = 15
                    tmr = 0
            if tmr == 20:
                skill_c = True
                idx = 11
                tmr = 0

        elif idx == 14: # 逃げられる？
            if boss == False:
                draw_battle(screen, fontS, FONT_1)
            if boss == True:
                draw_boss_battle(screen, fontS, FONT_1)
            if tmr == 1: set_message("...")
            if tmr == 2: set_message(".....")
            if tmr == 1: set_message(".......")
            if tmr == 1: set_message(".........")
            if tmr == 5:
                if boss == False:
                    if random.randint(0, 99) < 60:
                        idx = 22
                    else:
                        set_message("You faild to flee")
                if boss == True:
                    set_message("You faild to flee")
                    idx = 11
                    tmr = 0
            if tmr == 10:
                idx = 13
                tmr = 0

        elif idx == 15: # 敗北
            if boss == False:
                draw_battle(screen, fontS, FONT_1)
            if boss == True:
                draw_boss_battle(screen, fontS, FONT_1)
            if tmr == 1:
                pygame.mixer.music.stop()
                set_message("You lose.")
                if def_ca == 1:
                    pl_def = pl_def - def_c
                    def_c = 0
                    def_ca = 0
            if tmr == 11:
                idx = 9
                tmr = 29
                
        elif idx == 16: # 勝利
            if boss == False:
                draw_battle(screen, fontS, FONT_1)
            if boss == True:
                draw_boss_battle(screen, fontS, FONT_1)
            if tmr == 1:
                if def_ca == 1:
                    pl_def = pl_def - def_c
                    def_c = 0
                    def_ca = 0
                if boss == False:
                    set_message("You win! "+str(emy_exp)+" exp get")
                    pl_exp = pl_exp + emy_exp
                if boss == True:
                    set_message("You win! "+str(boss_exp)+" exp get")
                    pl_exp = pl_exp + boss_exp
                pygame.mixer.music.stop()
                se[5].play()
                
            if tmr == 28:
                idx = 22
                if pl_exp >= max_exp:
                    pl_lv = pl_lv + 1
                    idx = 17
                    tmr = 0

        elif idx == 17: # レベルアップ
            if boss == False:
                draw_battle(screen, fontS, FONT_1)
            if boss == True:
                draw_boss_battle(screen, fontS, FONT_1)
            if tmr == 1:
                set_message("Level up")
                se[4].play()
                lif_p = random.randint(10, 20)
                mp_p = random.randint(5, 10)
                atk_p = random.randint(2, 5)
                SP_p = random.randint(5, 10)
                def_p = random.randint(4, 8)
                acy_p = random.randint(2, 5)
                eva_p = random.randint(2, 5)
                pl_p = pl_p + 5
            if tmr == 8:
                set_message("HP + "+str(lif_p))
                pl_lifemax = pl_lifemax + lif_p
                pl_life = pl_life + 15
                if pl_life >= pl_lifemax:
                    pl_life = pl_lifemax
            if tmr == 10:
                set_message("MP + "+str(mp_p))
                pl_mpmax = pl_mpmax + mp_p
                pl_mp = pl_mp + 15
                if pl_mp >= pl_mpmax:
                    pl_mp = pl_mpmax
            if tmr == 12:
                set_message("ATK + "+str(atk_p))
                pl_atk = pl_atk + atk_p
            if tmr == 14:
                set_message("SP + "+str(SP_p))
                max_SP = max_SP + SP_p
                SP = SP + int(max_SP/2)
                if SP >= max_SP:
                    SP = max_SP
            if tmr == 16:
                set_message("DEF + "+str(def_p))
                pl_def = pl_def + def_p
            if tmr == 18:
                set_message("ACY + "+str(acy_p))
                pl_acy = pl_acy + acy_p
            if tmr == 20:
                set_message("EVA + "+str(eva_p))
                pl_eva = pl_eva + eva_p
            if tmr == 20:
                set_message("Player Point + 5")
            if tmr == 20:
                if pl_lv == 5:
                    set_message("Skill Shower Allow get")
                if pl_lv == 15:
                    set_message("Skill Defence Charge get")
            if tmr == 35:
                if pl_exp >= max_exp:
                    pl_lv = pl_lv + 1
                    idx = 17
                    tmr = 0
            if tmr == 50:
                skill_c = True
                idx = 22
                
        elif idx == 18: # スキル画面に変更
            draw_battle(screen, fontS, FONT_1)
            if tmr == 1:
                skill_c = False
            if tmr == 2:
                idx = 11
                tmr = 2
                
        elif idx == 19: # プレイヤーのスキル(Shower Arrow)
            if boss == False:
                draw_battle(screen, fontS, FONT_1)
            if boss == True:
                draw_boss_battle(screen, fontS, FONT_1)
            mp_p = 30
            if tmr == 1:
                if pl_mp < 30:
                    set_message("MP Not Enough")
                    idx = 11
                    tmr = 1
                if pl_mp >= 30:
                    tmr = 2
                    set_message("You skill Shower Arrow!!")
            if 2 <= tmr and tmr <= 6:
                img_rz = pygame.transform.rotozoom(imgEffect[1], 400*tmr, (10-tmr)/8)
                X = 440-int(img_rz.get_width()/2)
                Y = 360-int(img_rz.get_height()/2)
                screen.blit(img_rz, [X, Y])
                se[7].play()
            if tmr == 7:
                se[8].play()
                if boss == False:
                    emy_blink = 5
                    dmg = pl_atk + pl_acy * 2 + pl_lv * 5 + int(pl_acy/random.randint(10,13)) - emy_def
                if boss == True:
                    boss_blink = 5
                    dmg = pl_atk + pl_acy * 2 + pl_lv * 5 + int(pl_acy/random.randint(10,13)) - boss_def
                set_message(str(dmg)+"pts of damege!")
            if tmr == 11:
                pl_mp = pl_mp - mp_p
                if boss == False:
                    emy_life = emy_life - dmg
                    if emy_life <= 0:
                        emy_life = 0
                        idx = 16
                        tmr = 0
                if boss == True:
                    boss_life = boss_life - dmg
                    if boss_life <= 0:
                        boss_life = 0
                        idx = 16
                        tmr = 0
            if tmr == 16:
                idx = 13
                tmr = 0


        elif idx == 20: # Potion
            if boss == False:
                draw_battle(screen, fontS, FONT_1)
            if boss == True:
                draw_boss_battle(screen, fontS, FONT_1)
            if tmr == 1:
                set_message("Potion!")
                se[2].play()
            if tmr == 6:
                pl_life = pl_life + 1000
                if pl_life >= pl_lifemax:
                    pl_life = pl_lifemax
                potion = potion - 1
            if tmr == 11:
                idx = 13
                tmr = 0

        elif idx == 21: # Blaze gem
            if boss == False:
                draw_battle(screen, fontS, FONT_1)
            if boss == True:
                draw_boss_battle(screen, fontS, FONT_1)
            img_rz = pygame.transform.rotozoom(imgEffect[0], 30*tmr, (12-tmr)/8)
            X = int(440-img_rz.get_width()/2)
            Y = int(360-img_rz.get_height()/2)
            screen.blit(img_rz, [X, Y])
            if tmr == 1:
                set_message("Blaze gem")
                se[1].play()
            if tmr == 6:
                blazegem = blazegem - 1
            if tmr == 11:
                if boss == False:
                    dmg = 1000
                if boss == True:
                    dmg = 500
                idx = 12
                tmr = 4
                
        elif idx == 22: # 戦闘終了
            if floor <= 10:
                pygame.mixer.music.load(filename + "/sound/0022.ogg")
                pygame.mixer.music.play(-1)
            if floor >= 11 and floor <= 20:
                pygame.mixer.music.load(filename + "/sound/0021.ogg")
                pygame.mixer.music.play(-1)
            if floor >= 21:
                pygame.mixer.music.load(filename + "/sound/0070.ogg")
                pygame.mixer.music.play(-1)
            if def_ca == 1:
                    pl_def = pl_def - def_c
                    def_c = 0
                    def_ca = 0
            skill_c = True
            boss = False
            idx = 1

        elif idx == 23: # プレイヤースキル(Deffense Charge)
            if boss == False:
                draw_battle(screen, fontS, FONT_1)
            if boss == True:
                draw_boss_battle(screen, fontS, FONT_1)
            mp_p = 20
            if tmr == 1:
                if pl_mp < 20:
                    set_message("MP Not Enough")
                    idx = 11
                    tmr = 1
            if tmr == 2:
                if def_ca >= 1:
                    set_message("Deffense Charge Not Use")
                    idx = 11
                    tmr = 1
                else:
                    def_c = pl_eva + pl_lv
                    pl_def = pl_def + def_c
                    se[10].play()
            if tmr == 5:
                def_ca = def_ca + 1
                pl_mp = pl_mp - mp_p
                idx = 13
                tmr = 0

        elif idx == 24: # ボスの戦闘
            if tmr == 1:
                boss = True
                pygame.mixer.music.load(filename + "/sound/0008.ogg")
                pygame.mixer.music.play(-1)
                init_boss_battle()
                init_message()
            elif tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(imgBtlBG, [bx, by])
                draw_text(screen, "Encounter!", 350, 200, font, WHITE)
            elif tmr <= 16:
                draw_boss_battle(screen, fontS, FONT_1)
                draw_text(screen, boss_name+" apper!", 300, 200,font, WHITE)
            else:
                tmr == 17
            if tmr == 17:
                if pl_eva >= boss_eva:
                    idx = 11
                    tmr = 0
                else:
                    idx = 13
                    tmr = 0
                    
        elif idx == 25: # 説明
            screen.fill(WHITE)
            screen.blit(imgExplanation, [10, 0])
            draw_text(screen, "Press Return key", 320, 590, font, BLINK[tmr%6])
            if key[K_RETURN] == 1:
                make_dungeon()
                put_event()
                floor = 1
                welcome = 15
                pl_lifemax = 250
                pl_life = pl_lifemax
                pl_mpmax = 100
                pl_mp = pl_mpmax
                pl_atk = 70
                pl_def = 50
                pl_acy = 50
                pl_eva = 30
                pl_p = 0
                pl_exp = 0
                max_SP = 300
                SP = max_SP
                skill = 0
                pl_lv = 1
                potion = 0
                blazegem = 0
                skill_c = True
                boss = False
                def_ca = 0
                def_c = 0
                idx = 1
                pygame.mixer.music.load(filename + "/sound/0022.ogg")
                pygame.mixer.music.play(-1)
            
        elif idx == 26:
            #キーボタンが上の時、NewGame下の時、Continue
            if key[K_UP] == 1:
                startInfo = 0
            if key[K_DOWN] == 1:
                startInfo = 1

            if startInfo == 0:
                a = BLINK[tmr%6]
                b = WHITE
            else:
                a = WHITE
                b = BLINK[tmr%6]

            if key[K_RETURN] == 1:
                if startInfo == 0:
                    idx = 25
                elif startInfo == 1:
                    idx = 28
            draw_text(screen, "New Game", 375, 500, font, a)
            draw_text(screen, "Continue", 375, 590, font, b)
        elif idx == 27:
            #セーブ成功時
            draw_text(screen, "SaveOK", 380, 240, font, WHITE)
            idx = 1
        elif idx == 28:
            #Load_data()
            if floor <= 10:
                pygame.mixer.music.load(filename + "/sound/0022.ogg")
            if floor >= 11 and floor <= 20:
                pygame.mixer.music.load(filename + "/sound/0021.ogg")
            if floor >= 21:
                pygame.mixer.music.load(filename + "/sound/0070.ogg")
            pygame.mixer.music.play(-1)
            idx = 1
        draw_text(screen, "[S]peed"+str(speed), 740, 40, fontS, WHITE)
        player_exp()
        pygame.display.update()
        clock.tick(6+2*speed)

if __name__ == '__main__':
    main()

from pygame.locals import *
import pygame
import random
from .EnemyBoss import *
import sys
import os

class CommandData():
    tmr = 0         #処理タイミング
    idx = 0         #状態
    map_flg = False #マップフラグ
    treasure = 0    #宝箱
    enemyboss = ""  #敵情報
    skill_cmd = 0   #スキル情報
    btl_cmd = 0     #バトル情報
    dmg_eff = 0     #ダメージエフェクト
    screen = ""     #画面描画
    clock = ""      #クロック
    font = ""       #フォント
    fontS = ""      #フォント2
    FONT_1 = ""     #フォント3
    se = []         #SE
    point_se = ""   #ポイント用SE
    fl_max = 0      #最大フロア数
    floor = 0       #現在フロア
    TRE_NAME = []   #宝物名
    startinfo = 0   #スタート情報
    COMMAND = []    #戦闘コマンド
    COMMAND1 = []   #戦闘コマンド(スキル追加後)
    SKILL_NAME = [] #スキル名
    boss = False    #ボスフラグ
    welcome = 0     #初期表示
    EMY_NAME = []   #敵の名称
    BOSSNAME = []   #ボスの名称
    dmg = 0         #ダメージ
    DB = ""         #DB情報
    lif_p = 0
    mp_p = 0
    atk_p = 0
    SP_p = 0
    def_p = 0
    acy_p = 0
    eva_p = 0
    filename = os.path.expanduser('~/Desktop/PythonGame')
    
    def __init__(self, screen, clock, font, fontS, FONT_1, se, point_se, TRE_NAME, COMMAND, COMMAND1, SKILL_NAME, EMY_NAME, BOSSNAME, DB, enemyboss):
        #制御情報の初期化
        self.tmr = 0
        self.idx = 0
        self.map_flg = False
        self.treasure = 0
        self.skill_cmd = 0
        self.btl_cmd = 0
        self.dmg_eff = 0
        self.screen = screen
        self.clock = clock
        self.font = font
        self.fontS = fontS
        self.FONT_1 = FONT_1
        self.se = se
        self.point_se = point_se
        self.fl_max = 0
        self.floor = 0
        self.TRE_NAME = TRE_NAME
        self.startinfo = 0
        self.COMMAND = COMMAND
        self.COMMAND1 = COMMAND1
        self.SKILL_NAME = SKILL_NAME
        self.boss = False
        self.welcome = 0
        self.EMY_NAME = EMY_NAME
        self.BOSSNAME = BOSSNAME
        self.dmg= 0
        self.DB = DB
        self.enemyboss = enemyboss
    
    def move_player(self, key, pl, maps): # 主人公の移動
    
        if maps.dungeon[pl.pl_y][pl.pl_x] == 1: # 宝箱に載った
            maps.dungeon[pl.pl_y][pl.pl_x] = 0
            self.treasure = random.choice([0,0,0,1,1,1,1,1,1,2])
            if self.treasure == 0:
                pl.potion = pl.potion + 1
            if self.treasure == 1:
                pl.blazegem = pl.blazegem + 1
            if self.treasure == 2:
                pl.SP = int(pl.SP/2)
            self.idx = 3 # アイテム入手もしくはトラップ
            self.tmr = 0
            return
        if maps.dungeon[pl.pl_y][pl.pl_x] == 2: # 繭に載った
            maps.dungeon[pl.pl_y][pl.pl_x] = 0
            r = random.randint(0, 99)
            if r < 25: # 食料
                self.treasure = random.choice([3,3,3,4])
                if self.treasure == 3:
                    pl.SP = pl.SP + 50
                if pl.SP >= pl.max_SP:
                    pl.SP = pl.max_SP
                if self.treasure == 4:
                    pl.SP = pl.SP + 150
                if pl.SP >= pl.max_SP:
                    pl.SP = pl.max_SP
                self.idx = 3 # アイテム入手もしくはトラップ
                self.tmr = 0
            else: # 敵の出現
                self.idx = 10 # 戦闘開始
                self.tmr = 0
            return
        if maps.dungeon[pl.pl_y][pl.pl_x] == 3: # 階段に載った
            self.idx = 2 #画面移動へ
            self.tmr = 0
            return
        if maps.dungeon[pl.pl_y][pl.pl_x] == 4: # ボス戦後の宝箱に載った
            maps.dungeon[pl.pl_y][pl.pl_x] = 0
            self.treasure = random.choice([0,1])
            if self.treasure == 0:
                pl.potion = pl.potion + 1
            if self.treasure == 1:
                pl.blazegem = pl.blazegem + 1
            self.idx = 3 # アイテム入手もしくはトラップ
            self.tmr = 0
            return

        if maps.dungeon[pl.pl_y][pl.pl_x] == 5: # ボスとの戦闘
            maps.dungeon[pl.pl_y][pl.pl_x] = 0
            self.idx = 24 # ボスの戦闘
            self.tmr = 0
            return
        # 方向キーで上下左右に移動
        x = pl.pl_x
        y = pl.pl_y
        if key[K_UP] == 1: #上移動
            pl.pl_d = 0
            if maps.dungeon[pl.pl_y - 1][pl.pl_x] != 9:
                pl.pl_y = pl.pl_y - 1
        if key[K_DOWN] == 1: #下移動
            pl.pl_d = 1
            if maps.dungeon[pl.pl_y + 1][pl.pl_x] != 9:
                pl.pl_y = pl.pl_y + 1
        if key[K_LEFT] == 1: #左移動
            pl.pl_d = 2
            if maps.dungeon[pl.pl_y][pl.pl_x - 1] != 9:
                pl.pl_x = pl.pl_x - 1
        if key[K_RIGHT] == 1: #右移動
            pl.pl_d = 3
            if maps.dungeon[pl.pl_y][pl.pl_x + 1] != 9:
                pl.pl_x = pl.pl_x + 1
        pl.pl_a = pl.pl_d * 2
        if pl.pl_x != x or pl.pl_y != y: #移動したら食料の量と体力とMPを計算
            pl.pl_a = pl.pl_a + self.tmr % 2 # 移動したら足踏みのアニメーション
        
            #SPの管理SP、SPがなくなるとライフが１ずつ減少する
            if pl.SP > 0:
                pl.SP = pl.SP - 1
                if pl.pl_life < pl.pl_lifemax:
                    pl.pl_life = pl.pl_life + 1
                if pl.pl_mp < pl.pl_mpmax:
                    pl.pl_mp = pl.pl_mp + 1
            else:
                pl.pl_life = pl.pl_life - 5
                if pl.pl_life <= 0:
                    pl.pl_life = 0
                    pygame.mixer.music.stop()
                    self.self.idx = 9 # ゲームオーバー
                    self.self.tmr = 0
                if pl.pl_mp < pl.pl_mpmax:
                    pl.pl_mp = pl.pl_mp + 1
                
        # [P]ボタンで回復
        if key[K_p] == 1:
            self.treasure = 0
            if pl.potion > 0:
                self.idx = 4 # フィールドアイテム使用(ポーション)
                self.tmr = 0

        # [B]ボタンでブレイズジェム使用する
        if key[K_b] == 1:
            self.trasure = 1
            if pl.blazegem > 0:
                self.idx = 5 # フィールドアイテム使用(ブレイズジェム)
                self.tmr = 0
            
        # [A]ボタンでポイント使用してATKをアップする
        if key[K_a] == 1:
            if pl.pl_p > 0:
                pl.pl_atk = pl.pl_atk + 1
                pl.pl_p = pl.pl_p - 1
                self.point_se.play()
            
        # [D]ボタンでポイント使用してDEFをアップする
        if key[K_d] == 1:
            if pl.pl_p > 0:
                pl.pl_def = pl.pl_def + 1
                pl.pl_p = pl.pl_p - 1
                self.point_se.play()
    
        # [C]ボタンでポイント使用してACYをアップする
        if key[K_c] == 1:
            if pl.pl_p > 0:
                pl.pl_acy = pl.pl_acy + 1
                pl.pl_p = pl.pl_p - 1
                self.point_se.play()
            
        # [E]ボタンでポイント使用してATKをアップする
        if key[K_e] == 1:
            if pl.pl_p > 0:
                pl.pl_eva = pl.pl_eva + 1
                pl.pl_p = pl.pl_p - 1
                self.point_se.play()
    
        # [M]ボタンでマップ表示の切り替え
        if key[K_m] == 1:
            if self.map_flg == True:
                self.map_flg = False
            else:
                self.map_flg = True
            
        # [q]ボタンで大画面表示
        if key[K_q] == 1:
            self.screen = pygame.display.set_mode(
            (880, 680),
            pygame.FULLSCREEN
            )
        
        # [w]ボタンで通常表示
        if key[K_w] == 1:
            self.screen = pygame.display.set_mode((880, 720))
    
        # [V]ボタンでセーブ
        if key[K_v] == 1:
            if self.DB != "":
                self.DB.Save_data(pl, self.floor, self.idx, self.boss, maps)
                self.idx = 27 #セーブ

    def init_battle(self): # 戦闘に入る準備をする
        typ = random.randint(0, self.floor)
        if self.floor >= 20:
            typ = random.randint(0, 19)
        lev = random.randint(int(self.floor/2)+1, self.floor)
        #敵フラグ(True:敵 False:ボス)
        enemyFlg = True
        #敵情報作成
        self.enemyboss.updateEnemyBoss(enemyFlg, self.EMY_NAME, typ, lev)
    
    def init_boss_battle(self): # ボスの戦闘に入る準備をする
        lev = self.floor
        #敵フラグ(True:敵 False:ボス)
        enemyFlg = False
        typ = 0
        #ボス情報作成
        self.enemyboss.updateEnemyBoss(enemyFlg, self.BOSSNAME, typ, lev)
        
    def battle_command(self, bg, fnt, key, draw, pl): # コマンドの入力と表示
        ent = False
        if key[K_a] and pl.skill_c == True: # Aキー
            self.btl_cmd = 0
            ent = True
        if key[K_p] and pl.skill_c == True: # Pキー
            self.btl_cmd = 1
            ent = True
        if key[K_b] and pl.skill_c == True: # Bキー
            self.btl_cmd = 2
            ent = True
        if pl.skill >= 1:
            if key[K_k] and pl.skill_c == True:# Kキー
                pl.skill_c = False
        if key[K_r] and pl.skill_c == True: # Rキー
            if pl.skill == 0:
                self.btl_cmd = 3
                ent = True
            else:
                self.btl_cmd = 4
                ent = True
        if key[K_1]and pl.skill_c == False:# 1キー
            self.skill_cmd = 0
            ent = True
        if key[K_2]and pl.skill_c == False:# 2キー
            self.skill_cmd = 1
            ent = True
        if pl.pl_lv >= 15:
            if key[K_3] and pl.skill_c == False:# 3キー
                self.skill_cmd = 2
                ent = True
        if key[K_UP]: # ↑キー
            if self.btl_cmd > 0 and pl.skill_c == True:
                self.btl_cmd -= 1
            if self.skill_cmd > 0 and pl.skill_c == False:
                self.skill_cmd -= 1       
        if key[K_DOWN]: # ↓キー
            if pl.skill == 0 and self.btl_cmd < 3:
                self.btl_cmd += 1
            if pl.skill >= 1 and self.btl_cmd < 4 and pl.skill_c == True:
                self.btl_cmd += 1
            if pl.pl_lv <= 5 and pl.skill_c == False:
                if self.skill_cmd < 1:
                    self.skill_cmd += 1
            if pl.pl_lv >= 15 and pl.skill_c == False:
                if self.skill_cmd < 2:
                    self.skill_cmd += 1
        if key[K_SPACE] or key[K_RETURN]: #スペースまたはリターンキー
            ent = True
            
        if pl.skill <= 1: #スキル状態確認
            for i in range(4):
                c = draw.WHITE
                if self.btl_cmd == i: c = draw.BLINK[self.tmr%6]
                draw.draw_text(bg, self.COMMAND[i], 20, 360+i*60, fnt, c)
        if pl.skill >= 1:
            if pl.skill_c == True:
                for i in range(5):
                    c = draw.WHITE
                    if self.btl_cmd == i: c = draw.BLINK[self.tmr%6]
                    draw.draw_text(bg, self.COMMAND1[i], 20, 320+i*60, fnt, c)
            if pl.skill_c == False and pl.pl_lv <= 14:
                for i in range(2):
                    c = draw.WHITE
                    if self.skill_cmd == i: c = draw.BLINK[self.tmr%6]
                    draw.draw_text(bg, self.SKILL_NAME[i], 20, 360+i*60, fnt, c)
            if pl.skill_c == False and pl.pl_lv >= 15:
                for i in range(3):
                    c = draw.WHITE
                    if self.skill_cmd == i: c = draw.BLINK[self.tmr%6]
                    draw.draw_text(bg, self.SKILL_NAME[i], 20, 360+i*60, fnt, c)
        return ent
        
    def gameControl(self, draw, pl, maps, key): #ゲーム全体の制御
        if self.idx == 0: # タイトル画面
            if self.tmr == 1:
                pygame.mixer.music.load(self.filename + "/sound/0071.ogg")
                pygame.mixer.music.play(-1)
            self.screen.fill(draw.BLACK)
            self.screen.blit(draw.imgTitle, [40, 60])
            
            #過去履歴がある場合、最大フロア数を表示
            if self.fl_max == 0:
                if self.DB != "":
                    self.fl_max = self.DB.floor
            if self.fl_max > 0:
                draw.draw_text(self.screen, "You reached floor {}.".format(self.fl_max), 300, 460, self.font, draw.CYAN)
            draw.draw_text(self.screen, "Press space key", 320, 560, self.font, draw.BLINK[self.tmr%6]) 
            
            #スペースキー押下でNewGameContinueをそれぞれ表示
            if key[K_SPACE] == 1:
                pygame.draw.rect(self.screen, draw.BLACK, Rect(300,450,400,200))
                self.startInfo = 0
                self.idx = 26

        elif self.idx == 1: # プレイヤーの移動
            self.move_player(key, pl, maps)
            #表示の変更
            draw.draw_dungeon(self.screen, self.fontS, self.FONT_1, maps, pl.pl_x, pl.pl_y, pl.pl_a, self.floor, pl, self.tmr)
            draw.draw_text(self.screen, "floor {} ({},{})".format(self.floor, pl.pl_x, pl.pl_y), 60, 40, self.fontS, draw.WHITE)
            draw.draw_text(self.screen, "[P] = potion use", 330, 600, self.FONT_1, draw.WHITE)
            draw.draw_text(self.screen, "[B] = Blaze gem use", 330, 620, self.FONT_1, draw.WHITE)
            draw.draw_text(self.screen, "[M] = Map View", 330, 640, self.FONT_1, draw.WHITE)
            draw.draw_text(self.screen, "[A] ATK+1 [D] DEF+1 [C] ACY+1 [E] EVA+1", 30, 560, self.FONT_1, draw.WHITE)
            draw.draw_text(self.screen, "[Q] WideScreen [W] DefaultScreen [V]Save", 30, 580, self.FONT_1, draw.WHITE)
            draw.draw_text(self.screen,"Point : " + str(pl.pl_p), 30, 540, self.FONT_1, draw.WHITE)
            if self.map_flg:
                draw.Map_info(self.screen, pl , maps)
            if self.welcome > 0:
                self.welcome = self.welcome - 1
                draw.draw_text(self.screen,"Welcome to floor {}.".format(self.floor), 300, 180, self.font, draw.CYAN)

        elif self.idx == 2: # 画面の切替
            draw.draw_dungeon(self.screen, self.fontS, self.FONT_1, maps, pl.pl_x, pl.pl_y, pl.pl_a, self.floor, pl, self.tmr)
            
            #タイマーの時間により処理を変更する
            if 1 <= self.tmr and self.tmr <= 5:
                h = 80 * self.tmr
                pygame.draw.rect(self.screen, draw.BLACK, [0, 0, 880, h])
                pygame.draw.rect(self.screen, draw.BLACK, [0, 720 - h, 880, h])
            if self.tmr == 5: #フロアの制御
                self.floor = self.floor + 1
                if self.floor > self.fl_max:
                    self.fl_max = self.floor
                    if self.DB != "":
                        self.DB.UpdateflMax(self.fl_max)
                self.welcome = 15
            if self.tmr == 6: #ボスダンジョンへ移動か、通常ダンジョンかを制御する
                if self.floor == 10 or self.floor == 20 or self.floor == 30:
                    maps.boss_dungeon()
                    maps.put_boss_event(pl)
                else:
                    maps.make_dungeon()
                    maps.put_event(pl)
            if 7 <= self.tmr and self.tmr <= 10: #画面表示の変更
                h = 80*(10 - self.tmr)
                pygame.draw.rect(self.screen, draw.BLACK, [0, 0, 880, h])
                pygame.draw.rect(self.screen, draw.BLACK, [0, 720-h, 880, h])
            if self.tmr == 11: #ダンジョンの階数によりBGMを変更する
                if self.floor == 11:
                    pygame.mixer.music.load(self.filename + "/sound/0021.ogg")
                    pygame.mixer.music.play(-1)
                if self.floor == 21:
                    pygame.mixer.music.load(self.filename + "/sound/0070.ogg")
                    pygame.mixer.music.play(-1)
            if self.tmr == 12:
                self.idx = 1

        elif self.idx == 3: # アイテム入手もしくはトラップ
            draw.draw_dungeon(self.screen, self.fontS, self.FONT_1, maps, pl.pl_x, pl.pl_y, pl.pl_a, self.floor, pl, self.tmr)
            self.screen.blit(draw.imgItem[self.treasure], [320, 220])
            draw.draw_text(self.screen, self.TRE_NAME[self.treasure], 380, 240, self.font, draw.WHITE)
            if self.tmr == 10:
                self.idx = 1
                
        elif self.idx == 4: # フィールドアイテム使用(ポーション)
            draw.draw_dungeon(self.screen, self.fontS, self.FONT_1, maps, pl.pl_x, pl.pl_y, pl.pl_a, self.floor, pl, self.tmr)
            self.screen.blit(draw.imgItem[0], [320, 220])
            draw.draw_text(self.screen, self.TRE_NAME[0], 380, 240, self.font, draw.WHITE)
            if self.tmr == 1:
                draw.set_message("Potion!")
                pygame.mixer.Sound(self.filename + "/sound/se_field_potion.ogg").play()
            if self.tmr == 5:
                pl.pl_life = pl.pl_life + 1000
                if pl.pl_life >= pl.pl_lifemax:
                    pl.pl_life = pl.pl_lifemax
                pl.potion = pl.potion - 1
            if self.tmr == 10:
                self.idx = 1
                
        elif self.idx == 5: # フィールドアイテム使用(ブレイズジェム)
            draw.draw_dungeon(self.screen, self.fontS, self.FONT_1, maps, pl.pl_x, pl.pl_y, pl.pl_a, self.floor, pl, self.tmr)
            self.screen.blit(draw.imgItem[1], [320, 220])
            draw.draw_text(self.screen, self.TRE_NAME[1], 380, 240, self.font, draw.WHITE)
            img_rz = pygame.transform.rotozoom(draw.imgEffect[0], 30 * self.tmr, (12- self.tmr ) / 8)
            X = int(440 - img_rz.get_width()/2)
            Y = int(360 - img_rz.get_height()/2)
            self.screen.blit(img_rz, [X, Y])
            

            #周りの繭を焼き払う
            if self.tmr == 1:
                draw.set_message("Blaze gem!")
                pygame.mixer.Sound(self.filename + "/sound/eff_fireball.ogg").play()
            if self.tmr == 6:
                pl.blazegem = pl.blazegem - 1
            if self.tmr == 11: #下方向の処理
                if maps.dungeon[pl.pl_y-1][pl.pl_x] == 2:
                    maps.dungeon[pl.pl_y-1][pl.pl_x] = 0
            if self.tmr == 12: #上方向の処理
                if maps.dungeon[pl.pl_y+1][pl.pl_x] == 2:
                    maps.dungeon[pl.pl_y+1][pl.pl_x] = 0
            if self.tmr == 13: #左方向の処理
                if maps.dungeon[pl.pl_y][pl.pl_x-1] == 2:
                    maps.dungeon[pl.pl_y][pl.pl_x-1] = 0
            if self.tmr == 14: #右方向の処理
                if maps.dungeon[pl.pl_y][pl.pl_x+1] == 2:
                    maps.dungeon[pl.pl_y][pl.pl_x+1] = 0
            if self.tmr == 15: #右下向の処理
                if maps.dungeon[pl.pl_y-1][pl.pl_x+1] == 2:
                    maps.dungeon[pl.pl_y-1][pl.pl_x+1] = 0
            if self.tmr == 16: #左下方向の処理
                if maps.dungeon[pl.pl_y-1][pl.pl_x-1] == 2:
                    maps.dungeon[pl.pl_y-1][pl.pl_x-1] = 0
            if self.tmr == 17: #左上方向の処理
                if maps.dungeon[pl.pl_y+1][pl.pl_x-1] == 2:
                    maps.dungeon[pl.pl_y+1][pl.pl_x-1] = 0
            if self.tmr == 18: #右上方向の処理
                if maps.dungeon[pl.pl_y+1][pl.pl_x+1] == 2:
                    maps.dungeon[pl.pl_y+1][pl.pl_x+1] = 0
            if self.tmr == 20:
                self.idx = 1

        elif self.idx == 9: # ゲームオーバー
            if self.tmr <= 30: #倒れるエフェクト
                PL_TURN = [2, 4, 0, 6]
                pl.pl_a = PL_TURN[self.tmr % 4]
                if self.tmr == 30: pl.pl_a = 8 # 倒れた絵
                draw.draw_dungeon(self.screen, self.fontS, self.FONT_1, maps, pl.pl_x, pl.pl_y, pl.pl_a, self.floor, pl, self.tmr)
            elif self.tmr == 31: #倒れた後の表示
                self.se[3].play()
                draw.draw_text(self.screen, "You died.", 360, 240, self.font, draw.RED)
                draw.draw_text(self.screen, "Game over.", 360, 380, self.font, draw.RED)
            elif self.tmr == 120: #初期化処理
                self.idx = 0
                self.tmr = 0

        elif self.idx == 10: # 戦闘開始
            if self.tmr == 1:
                pygame.mixer.music.load(self.filename + "/sound/0154.ogg")
                pygame.mixer.music.play(-1)
                self.init_battle()
                draw.init_message()
            elif self.tmr <= 4:
                bx = (4 - self.tmr) * 220
                by = 0
                self.screen.blit(draw.imgBtlBG, [bx, by])
                draw.draw_text(self.screen, "Encounter!", 350, 200, self.font, draw.WHITE)
            elif self.tmr <= 16:
                draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
                draw.draw_text(self.screen, self.enemyboss.emy_name + " apper!", 300, 200,self.font, draw.WHITE)
            else:
                self.tmr == 17
            if self.tmr == 17:
                if pl.pl_eva >= self.enemyboss.emy_eva:
                    self.idx = 11 # プレイヤーのターン(入力待ち)
                    self.tmr = 0
                else:
                    self.idx = 13 # 敵のターン
                    self.tmr = 0

        elif self.idx == 11: # プレイヤーのターン(入力待ち)
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            if self.tmr == 1:draw.set_message("You turn.")
            if pl.skill == 0:
                if self.battle_command(self.screen, self.font, key, draw, pl) == True:
                    if self.btl_cmd == 0:
                        self.idx = 12 #プレイヤーの攻撃へ
                        self.tmr = 0
                    if self.btl_cmd == 1 and pl.potion > 0:
                        self.idx = 20 # Potion
                        self.tmr = 0
                    if self.btl_cmd == 2 and pl.blazegem > 0:
                        self.idx = 21 # Blaze gem
                        self.tmr = 0
                    if self.btl_cmd == 3:
                        self.idx = 14 # 逃げられる？
                        self.tmr = 0
            if pl.skill >= 1:
                if pl.skill_c == True:
                    if self.battle_command(self.screen, self.font, key, draw, pl) == True:
                        if self.btl_cmd == 0:
                            self.idx = 12 #プレイヤーの攻撃へ
                            self.tmr = 0
                        if self.btl_cmd == 1 and pl.potion > 0:
                            self.idx = 20 # Potion
                            self.tmr = 0
                        if self.btl_cmd == 2 and pl.blazegem > 0:
                            self.idx = 21 # Blaze gem
                            self.tmr = 0
                        if self.btl_cmd == 3:
                            self.idx = 18 # スキル画面に変更
                            self.tmr = 0
                        if self.btl_cmd == 4:
                            self.idx = 14 # 逃げられる？
                            self.tmr = 0
                if pl.skill_c == False:
                    if self.battle_command(self.screen, self.font, key, draw, pl) == True:
                        if self.skill_cmd == 0:
                            pl.skill_c = True
                        if self.skill_cmd == 1:
                            self.idx = 19 # プレイヤーのスキル(Shower Arrow)
                            self.tmr = 0
                        if pl.pl_lv >= 15:
                            if self.skill_cmd == 2:
                                self.idx = 23 # プレイヤースキル(Deffense Charge)
                                self.tmr = 0
                            
        elif self.idx == 12: # プレイヤーの攻撃
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            if self.tmr == 1:
                draw.set_message("You attack!")
                pl_hit = 70 + pl.pl_acy - self.enemyboss.emy_eva
                if pl_hit >= 100:
                    pl_hit = 99
                if pl_hit < 0:
                    pl_hit = 0
                hit = random.randint(1, 100)
                if hit <= pl_hit:
                    self.dmg= pl.pl_atk - self.enemyboss.emy_def + int(pl.pl_atk/random.randint(10,13))
                    if self.dmg<= 0:
                        self.dmg= 0
                else:
                    self.se[6].play()
                    self.dmg= 0
                    self.tmr = 6
                                       
            if self.tmr == 2:
                self.se[9].play()
                img_3 = draw.imgEffect[2]
                X = 440-int(img_3.get_width()/2)
                Y = 300-int(img_3.get_height()/2)
                self.screen.blit(img_3, [X, Y])
                
            if self.tmr == 3:
                img_3 = draw.imgEffect[2]
                X = 520-int(img_3.get_width()/2)
                Y = 460-int(img_3.get_height()/2)
                self.screen.blit(img_3, [X, Y])

            if self.tmr == 4:
                self.se[9].play()
                img_3 = draw.imgEffect[2]
                X = 440-int(img_3.get_width()/2)
                Y = 530-int(img_3.get_height()/2)
                self.screen.blit(img_3, [X, Y])
                
            if self.tmr == 5:
                self.enemyboss.emy_blink = 5
                draw.set_message(str(self.dmg)+"pts of damege!")
                self.tmr = 11
            if self.tmr == 6:
                draw.set_message("miss")
                self.tmr = 16
            if self.tmr == 11:
                self.enemyboss.emy_life = self.enemyboss.emy_life - self.dmg
                if self.enemyboss.emy_life <= 0:
                    self.enemyboss.emy_life = 0
                    self.idx = 16 # 勝利
                    self.tmr = 0
            if self.tmr == 16:
                self.idx = 13 # 敵のターン
                self.tmr = 0

        elif self.idx == 13: # 敵のターン
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            if self.tmr == 2:
                draw.set_message("Enemy turn.")
            if self.tmr == 5: #回避判定
                draw.set_message(self.enemyboss.emy_name + " attack!")
                self.enemyboss.emy_step = 30
                emy_hit = 70 + self.enemyboss.emy_acy - pl.pl_eva
                #回避計算
                if emy_hit >= 100:
                    emy_hit = 99
                e_hit = random.randint(1, 100)
                if e_hit <= emy_hit:
                    self.se[0].play()
                else:
                    self.se[6].play()
                    self.dmg= 0
                    self.tmr = 12
            if self.tmr == 9: #ダメージ計算
                self.dmg= self.enemyboss.emy_atk - pl.pl_def + int(self.enemyboss.emy_atk/random.randint(10,13))
                if self.dmg <= 0:
                    self.dmg= 0
                draw.set_message(str(self.dmg)+"pts of damege!")
                self.enemyboss.dmg_eff = 5
                self.enemyboss.emy_step = 0
                self.tmr = 15
            if self.tmr == 12:
                draw.set_message("miss")
                self.tmr = 20
                self.enemyboss.emy_step = 0
            if self.tmr == 15:
                pl.pl_life = pl.pl_life - self.dmg
                if pl.pl_life <= 0:
                    pl.pl_life = 0
                    self.idx = 15 # 敗北
                    self.tmr = 0
            if self.tmr == 20:
                skill_c = True
                self.idx = 11 # プレイヤーのターン(入力待ち)
                self.tmr = 0

        elif self.idx == 14: # 逃げられる？
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            if self.tmr == 1: draw.set_message("...")
            if self.tmr == 2: draw.set_message(".....")
            if self.tmr == 1: draw.set_message(".......")
            if self.tmr == 1: draw.set_message(".........")
            if self.tmr == 5:
                if self.boss == False: #ボス以外は逃げれるか計算する
                    if random.randint(0, 99) < 60:
                        self.idx = 22 # 戦闘終了
                    else:
                        draw.set_message("You faild to flee")
                if self.boss == True: #ボスの時は逃げれない
                    draw.set_message("You faild to flee")
                    self.idx = 11 # プレイヤーのターン(入力待ち)
                    self.tmr = 0
            if self.tmr == 10:
                self.idx = 13 # 敵のターン
                self.tmr = 0

        elif self.idx == 15: # 敗北
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            if self.tmr == 1:
                pygame.mixer.music.stop()
                draw.set_message("You lose.")
                if pl.def_ca == 1: #ステータスを戻す処理
                    pl.pl_def = pl.pl_def - pl.def_c
                    pl.def_c = 0
                    pl.def_ca = 0
            if self.tmr == 11:
                self.idx = 9 # ゲームオーバー
                self.tmr = 29
                
        elif self.idx == 16: # 勝利
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            if self.tmr == 1: #各種ステータスを戻す処理
                if pl.def_ca == 1:
                    pl.pl_def = pl.pl_def - pl.def_c
                    pl.def_c = 0
                    pl.def_ca = 0
                draw.set_message("You win! "+str(self.enemyboss.emy_exp)+" exp get")
                pl.pl_exp = pl.pl_exp + self.enemyboss.emy_exp
                pygame.mixer.music.stop()
                self.se[5].play()
                
            if self.tmr == 28: # レベルアップ判定
                self.idx = 22 # 戦闘終了
                if pl.pl_exp >= pl.max_exp:
                    pl.pl_lv = pl.pl_lv + 1
                    self.idx = 17 # レベルアップ
                    self.tmr = 0

        elif self.idx == 17: # レベルアップ
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            if self.tmr == 1:
                draw.set_message("Level up")
                self.se[4].play()
                #レベルアップ時の各種ステータスのアップポイント
                self.lif_p = random.randint(10, 20)
                self.mp_p = random.randint(5, 10)
                self.atk_p = random.randint(2, 5)
                self.SP_p = random.randint(5, 10)
                self.def_p = random.randint(4, 8)
                self.acy_p = random.randint(2, 5)
                self.eva_p = random.randint(2, 5)
                pl.pl_p = pl.pl_p + 5
            if self.tmr == 8: #HPステータスアップ表示
                draw.set_message("HP + "+str(self.lif_p))
                pl.pl_lifemax = pl.pl_lifemax + self.lif_p
                pl.pl_life = pl.pl_life + 15
                if pl.pl_life >= pl.pl_lifemax:
                    pl.pl_life = pl.pl_lifemax
            if self.tmr == 10: #MPステータスアップ表示
                draw.set_message("MP + "+str(self.mp_p))
                pl.pl_mpmax = pl.pl_mpmax + self.mp_p
                pl.pl_mp = pl.pl_mp + 15
                if pl.pl_mp >= pl.pl_mpmax:
                    pl.pl_mp = pl.pl_mpmax
            if self.tmr == 12: #ATKステータスアップ表示
                draw.set_message("ATK + "+str(self.atk_p))
                pl.pl_atk = pl.pl_atk + self.atk_p
            if self.tmr == 14: #SPステータスアップ表示
                draw.set_message("SP + "+str(self.SP_p))
                pl.max_SP = pl.max_SP + self.SP_p
                pl.SP = pl.SP + int(pl.max_SP / 2)
                if pl.SP >= pl.max_SP:
                    pl.SP = pl.max_SP
            if self.tmr == 16: #DEFステータスアップ表示
                draw.set_message("DEF + "+str(self.def_p))
                pl.pl_def = pl.pl_def + self.def_p
            if self.tmr == 18: #ACYステータスアップ表示
                draw.set_message("ACY + "+str(self.acy_p))
                pl.pl_acy = pl.pl_acy + self.acy_p
            if self.tmr == 20: #EVAステータスアップ表示
                draw.set_message("EVA + "+str(self.eva_p))
                pl.pl_eva = pl.pl_eva + self.eva_p
            if self.tmr == 20: #プレイヤーポイント取得表示
                draw.set_message("Player Point + 5")
            if self.tmr == 20: #スキル取得表示
                if pl.pl_lv == 5:
                    draw.set_message("Skill Shower Allow get")
                if pl.pl_lv == 15:
                    draw.set_message("Skill Defence Charge get")
            if self.tmr == 35: #レベルアップ（連続の場合）
                if pl.pl_exp >= pl.max_exp:
                    pl.pl_lv = pl.pl_lv + 1
                    self.idx = 17 # レベルアップ
                    self.tmr = 0
            if self.tmr == 50: #スキルフラグ
                pl.skill_c = True
                self.idx = 22 # 戦闘終了
                
        elif self.idx == 18: # スキル画面に変更
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            if self.tmr == 1:
                skill_c = False
            if self.tmr == 2:
                self.idx = 11 # プレイヤーのターン(入力待ち)
                self.tmr = 2
                
        elif self.idx == 19: # プレイヤーのスキル(Shower Arrow)
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            mp_p = 30
            if self.tmr == 1:
                if pl.pl_mp < 30:
                    draw.set_message("MP Not Enough")
                    self.idx = 11 # プレイヤーのターン(入力待ち)
                    self.tmr = 1
                if pl.pl_mp >= 30:
                    self.tmr = 2
                    draw.set_message("You skill Shower Arrow!!")
            if 2 <= self.tmr and self.tmr <= 6:
                img_rz = pygame.transform.rotozoom(draw.imgEffect[1], 400 * self.tmr, (10 - self.tmr) / 8)
                X = 440-int(img_rz.get_width()/2)
                Y = 360-int(img_rz.get_height()/2)
                self.screen.blit(img_rz, [X, Y])
                self.se[7].play()
            if self.tmr == 7:
                #ダメージ計算
                self.se[8].play()
                self.enemyboss.emy_blink = 5
                self.dmg= pl.pl_atk + pl.pl_acy * 2 + pl.pl_lv * 5 + int(pl.pl_acy/random.randint(10,13)) - self.enemyboss.emy_def
                draw.set_message(str(self.dmg)+"pts of damege!")
            if self.tmr == 11:
                #MPとダメージ反映
                pl.pl_mp = pl.pl_mp - mp_p
                self.enemyboss.emy_life = self.enemyboss.emy_life - self.dmg
                if self.enemyboss.emy_life <= 0:
                    self.enemyboss.emy_life = 0
                    self.idx = 16 # 勝利
                    self.tmr = 0
            if self.tmr == 16:
                self.idx = 13 # 敵のターン
                self.tmr = 0


        elif self.idx == 20: # Potion
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            if self.tmr == 1:
                draw.set_message("Potion!")
                self.se[2].play()
            if self.tmr == 6:
                pl.pl_life = pl.pl_life + 1000
                if pl.pl_life >= pl.pl_lifemax:
                    pl.pl_life = pl.pl_lifemax
                pl.potion = pl.potion - 1
            if self.tmr == 11:
                self.idx = 13 # 敵のターン
                self.tmr = 0

        elif self.idx == 21: # Blaze gem
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            img_rz = pygame.transform.rotozoom(draw.imgEffect[0], 30*  self.tmr, (12 - self.tmr) / 8)
            X = int(440-img_rz.get_width()/2)
            Y = int(360-img_rz.get_height()/2)
            self.screen.blit(img_rz, [X, Y])
            if self.tmr == 1:
                draw.set_message("Blaze gem")
                self.se[1].play()
            if self.tmr == 6:
                pl.blazegem = pl.blazegem - 1
            if self.tmr == 11:
                if self.boss == False:
                    self.dmg= 1000
                if self.boss == True:
                    self.dmg= 500
                self.idx = 12 #プレイヤーの攻撃へ
                self.tmr = 4
                
        elif self.idx == 22: # 戦闘終了
            if self.floor <= 10:
                pygame.mixer.music.load(self.filename + "/sound/0022.ogg")
                pygame.mixer.music.play(-1)
            if self.floor >= 11 and self.floor <= 20:
                pygame.mixer.music.load(self.filename + "/sound/0021.ogg")
                pygame.mixer.music.play(-1)
            if self.floor >= 21:
                pygame.mixer.music.load(self.filename + "/sound/0070.ogg")
                pygame.mixer.music.play(-1)
            if pl.def_ca == 1:
                    pl.pl_def = pl.pl_def - pl.def_c
                    pl.def_c = 0
                    pl.def_ca = 0
            pl.skill_c = True
            self.boss = False
            self.idx = 1

        elif self.idx == 23: # プレイヤースキル(Deffense Charge)
            draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
            mp_p = 20
            if self.tmr == 1:
                if pl.pl_mp < 20:
                    draw.set_message("MP Not Enough")
                    self.idx = 11 # プレイヤーのターン(入力待ち)
                    self.tmr = 1
            if self.tmr == 2:
                if pl.def_ca >= 1:
                    draw.set_message("Deffense Charge Not Use")
                    self.idx = 11 # プレイヤーのターン(入力待ち)
                    self.tmr = 1
                else:
                    pl.def_c = pl.pl_eva + pl.pl_lv
                    pl.pl_def = pl.pl_def + pl.def_c
                    self.se[10].play()
            if self.tmr == 5:
                pl.def_ca = pl.def_ca + 1
                pl.pl_mp = pl.pl_mp - mp_p
                self.idx = 13 # 敵のターン
                self.tmr = 0

        elif self.idx == 24: # ボスの戦闘
            if self.tmr == 1:
                self.boss = True
                pygame.mixer.music.load(self.filename + "/sound/0008.ogg")
                pygame.mixer.music.play(-1)
                self.init_boss_battle()
                draw.init_message()
            elif self.tmr <= 4:
                bx = (4 - self.tmr)*220
                by = 0
                self.screen.blit(draw.imgBtlBG, [bx, by])
                draw.draw_text(self.screen, "Encounter!", 350, 200, self.font, draw.WHITE)
            elif self.tmr <= 16:
                draw.draw_battle(self.screen, self.fontS, self.FONT_1, self.enemyboss, pl, self.tmr)
                draw.draw_text(self.screen, self.enemyboss.emy_name+" apper!", 300, 200, self.font, draw.WHITE)
            else:
                self.tmr == 17
            if self.tmr == 17:
                if pl.pl_eva >= self.enemyboss.emy_eva:
                    self.idx = 11 # プレイヤーのターン(入力待ち)
                    self.tmr = 0
                else:
                    self.idx = 13 # 敵のターン
                    self.tmr = 0
                    
        elif self.idx == 25: # 説明
            self.screen.fill(draw.WHITE)
            self.screen.blit(draw.imgExplanation, [10, 0])
            draw.draw_text(self.screen, "Press Return key", 320, 590, self.font, draw.BLINK[self.tmr % 6])
            if key[K_RETURN] == 1:
                maps.make_dungeon()
                maps.put_event(pl)
                self.floor = 1
                self.welcome = 15
                pl.resetPlayer()
                self.boss = False
                self.idx = 1 #プレイヤー移動へ
                pygame.mixer.music.load(self.filename + "/sound/0022.ogg")
                pygame.mixer.music.play(-1)
            
        elif self.idx == 26: #スタート画面（初めてか続きからを表示と制御）
            #キーボタンが上の時、NewGame下の時、Continue
            if key[K_UP] == 1:
                self.startInfo = 0
            if key[K_DOWN] == 1:
                self.startInfo = 1

            if self.startInfo == 0:
                newgame = draw.BLINK[self.tmr % 6]
                load = draw.WHITE
            else:
                newgame = draw.WHITE
                load = draw.BLINK[self.tmr % 6]

            if key[K_RETURN] == 1:
                if self.startInfo == 0:
                    self.idx = 25 #説明画面へ
                elif self.startInfo == 1:
                    self.idx = 28 #ロード処理へ
            draw.draw_text(self.screen, "New Game", 375, 500, self.font, newgame)
            draw.draw_text(self.screen, "Continue", 375, 590, self.font, load)

        elif self.idx == 27: #セーブ
            #セーブ成功時
            draw.draw_text(self.screen, "SaveOK", 380, 240, self.font, draw.WHITE)
            self.idx = 1 #プレイヤー移動へ

        elif self.idx == 28: #ロード（Continue押下時)
            if self.DB != "":
                self.DB.Load_data(pl, maps)
                #セーブデータがない場合は動作させない
                if  pl.pl_atk == 0:
                    self.idx = 26 #スタート画面へ
                    return
                else:
                    self.floor = self.DB.floor
                    self.boss = self.DB.boss
                    self.idx = self.DB.idx
                if self.floor <= 10:
                    pygame.mixer.music.load(self.filename + "/sound/0022.ogg")
                if self.floor >= 11 and self.floor <= 20:
                    pygame.mixer.music.load(self.filename + "/sound/0021.ogg")
                if self.floor >= 21:
                    pygame.mixer.music.load(self.filename + "/sound/0070.ogg")
                pygame.mixer.music.play(-1)


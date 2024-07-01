import pygame
from pygame.locals import *
import random

class Drawing():
    #色の定義
    WHITE = (255,255,255)
    BLACK = (  0,  0,  0)
    RED   = (255,  0,  0)
    CYAN  = (  0,255,255)
    PINK  = (255, 64,255)
    BLINK = [(224,255,255), (192,224,255), (128,224,255), (64, 192,255), (128,224,255), (192,240,255)]
    imgTitle = ""
    imgExplanation = ""
    imgWall = ""
    imgWall2 = ""
    imgDark = ""
    imgPara = ""
    imgBtlBG = ""
    imgEnemy = ""
    imgItem = []
    imgFloor = []
    imgPlayer1 = []
    imgEffect = []
    imgBoss = ""
    imgBossField = []
    
    # 戦闘メッセージの表示処理
    message = [""]*(10)
    
    def __init__(self, imgTitle, imgExplanation, imgWall,
                 imgWall2, imgDark, imgPara, imgBtlBG,
                 imgEnemy, imgItem, imgFloor, imgPlayer1,
                 imgEffect, imgBoss, imgBossField): #初期化処理
        self.imgTitle = imgTitle
        self.imgExplanation = imgExplanation
        self.imgWall = imgWall
        self.imgWall2 = imgWall2
        self.imgDark = imgDark
        self.imgPara = imgPara
        self.imgBtlBG = imgBtlBG
        self.imgEnemy = imgEnemy
        self.imgItem = imgItem
        self.imgFloor = imgFloor
        self.imgPlayer1 = imgPlayer1
        self.imgEffect = imgEffect
        self.imgBoss = imgBoss
        self.imgBossField = imgBossField
        
    def draw_dungeon(self, bg, fnt, FONT_1, mapC, pl_x, pl_y, pl_a, floor, pl):# ダンジョンを描画する
        bg.fill(self.BLACK)
        for y in range(-4, 6):
            for x in range(-5, 6):
                X = (x+5)*80
                Y = (y+4)*80
                dx = pl_x + x
                dy = pl_y + y
                if 0 <= dx and dx < mapC.DUNGEON_W and 0 <= dy and dy < mapC.DUNGEON_H:
                    if mapC.dungeon[dy][dx] <= 4:
                        bg.blit(self.imgFloor[mapC.dungeon[dy][dx]], [X, Y])
                    if mapC.dungeon[dy][dx] == 9:
                        bg.blit(self.imgWall, [X, Y-40])
                        if dy >= 1 and mapC.dungeon[dy-1][dx] == 9:
                            bg.blit(self.imgWall2, [X, Y-80])
                    if mapC.dungeon[dy][dx] == 5:
                        bg.blit(self.imgBossField[int(floor/10)-1], [X, Y])
                if x == 0 and y == 0: #主人公のキャラ表示
                    bg.blit(self.imgPlayer1[pl_a], [X-6, Y-20])
        bg.blit(self.imgDark, [0, 0]) # 四隅が暗闇の画像を重ねる
        self.draw_para(bg, fnt, FONT_1, pl) # 主人公の能力を表示
    
    def draw_para(self, bg, fnt, FONT_1, pl): #主人公の能力表示
        X = 30 
        Y = 600
        bg.blit(self.imgPara, [X, Y])
        col = self.WHITE
        if pl.pl_life < int(pl.pl_lifemax/5) and self.tmr % 2 == 0:
            col = self.RED
        self.draw_text(bg, "{}/{}".format(pl.pl_life, pl.pl_lifemax), X+83, Y+4, FONT_1, col)
        self.draw_text(bg, str(pl.pl_atk),X+190, Y+6, FONT_1, self.WHITE)
        self.draw_text(bg, str(pl.pl_def),X+190, Y+25, FONT_1, self.WHITE)
        self.draw_text(bg, str(pl.pl_acy),X+35, Y+62, FONT_1, self.WHITE)
        self.draw_text(bg, str(pl.pl_eva),X+100, Y+62, FONT_1, self.WHITE)
        self.draw_text(bg, str(pl.pl_lv),X+27, Y+48, FONT_1, self.WHITE)
        self.draw_text(bg, "{}/{}".format(pl.pl_exp, pl.max_exp), X+175, Y+62, FONT_1, self.WHITE)
        self.draw_text(bg, "{}/{}".format(pl.pl_mp, pl.pl_mpmax), X+83, Y+19, FONT_1, self.WHITE)
        col = self.WHITE
        if pl.SP == 0 and tmr%2 == 0:
            col = self.RED
        self.draw_text(bg, "{}/{}".format(pl.SP, pl.max_SP), X+83, Y+35, FONT_1, col)
        self.draw_text(bg, str(pl.potion), X+266, Y+6, FONT_1, self.WHITE)
        self.draw_text(bg, str(pl.blazegem), X+266, Y+25, FONT_1, self.WHITE)
        
    def draw_text(self, bg, txt, x,  y, fnt, col): # 影付き文字の表示
        sur = fnt.render(txt, True, self.BLACK)
        bg.blit(sur,[x+1, y+2])
        sur = fnt.render(txt, True, col) 
        bg.blit(sur, [x, y])
    
    def Map_info(self, bg, pl, maps): #マップの描画
        pygame.draw.rect(bg, self.BLACK, Rect(90,100,700,400))
        for y in range(0, 27):
            for x in range(0, 45):
                my = (y * 15) + 1
                mx = (x * 15) + 1
                if maps.dungeon[y][x] == maps.dungeon[pl.pl_y][pl.pl_x]:
                    bg.blit(pygame.transform.scale(self.imgPlayer1[pl.pl_a], [50, 50]), [64 + (pl.pl_x * 15 + 1), 65 + (pl.pl_y * 15 + 1)])
                for rmy in range(-8, 8):
                    for rmx in range(-8, 8):
                        if maps.dungeon[y][x] != 9:
                            pygame.draw.rect(bg,self.WHITE,Rect(90 + mx + rmx,100 + my + rmy,1,1))
    
    def draw_bar(self, bg, x, y, w, h, val, ma):# 敵の体力を表示するバー
        pygame.draw.rect(bg, self.WHITE, [x-2, y-2, w+4, h+4])
        pygame.draw.rect(bg, self.BLACK, [x, y, w, h])
        if val > 0:
            pygame.draw.rect(bg, (0, 128, 255), [x, y, int(w*val/ma), h])
    
    def draw_battle(self, bg, fnt, FONT_1, enemy, pl): # 戦闘画面の描画
        bx = 0
        by = 0
        if enemy.dmg_eff > 0:
            enemy.dmg_eff = enemy.dmg_eff - 1
            bx = random.randint(-20, 20)
            by = random.randint(-10, 10)
        bg.blit(self.imgBtlBG, [bx, by])
        if enemy.emy_life > 0 and enemy.emy_blink % 2 == 0:
            bg.blit(self.imgEnemy, [enemy.emy_x, enemy.emy_y + enemy.emy_step])
        self.draw_bar(bg, 340, 580, 200, 10, enemy.emy_life, enemy.emy_lifemax)
        if enemy.emy_blink > 0:
            enemy.emy_blink = enemy.emy_blink - 1
        for i in range(10): # 戦闘メッセージの表示
            self.draw_text(bg, self.message[i], 600, 100+i*50, fnt, self.WHITE)
        self.draw_para(bg, fnt, FONT_1, pl) # 主人公の能力を表示
    
    def init_message(self):
        for i in range(10):
            self.message[i] = ""

    def set_message(self, msg):
        for i in range(10):
            if self.message[i] == "":
                self.message[i] = msg
                return
        for i in range(9):
            self.message[i] = self.message[i+1]
        self.message[9] = msg
        
    def draw_boss_battle(self, bg, fnt, FONT_1, enemy, pl): # ボスの戦闘画面の描画
        boss_bx = 0
        boss_by = 0
        if enemy.dmg_eff > 0:
            enemy.dmg_eff = enemy.dmg_eff - 1
            boss_bx = random.randint(-20, 20)
            boss_by = random.randint(-10, 10)
        bg.blit(self.imgBtlBG, [boss_bx, boss_by])
        if enemy.boss_life > 0 and enemy.boss_blink%2 == 0:
            bg.blit(self.imgBoss, [enemy.boss_x, enemy.boss_y + enemy.boss_step])
        self.draw_bar(bg, 340, 580, 200, 10, enemy.boss_life, enemy.boss_lifemax)
        if enemy.boss_blink > 0:
            enemy.boss_blink = enemy.boss_blink - 1
        for i in range(10): # 戦闘メッセージの表示
            self.draw_text(bg, self.message[i], 600, 100+i*50, fnt, self.WHITE)
        self.draw_para(bg, fnt, FONT_1, pl) # 主人公の能力を表示
            


import random

class MapC():
    MAZE_W = 15
    MAZE_H = 9
    DUNGEON_W = MAZE_W*3
    DUNGEON_H = MAZE_H*3
    maze = []
    dungeon = []

    def __init__(self): #初期化処理
        for y in range(self.MAZE_H):
            self.maze.append([0]*self.MAZE_W)
        for y in range(self.DUNGEON_H):
            self.dungeon.append([0]*self.DUNGEON_W)

    def make_dungeon(self):# ダンジョンの自動生成
        XP = [ 0, 1, 0,-1]
        YP = [-1, 0, 1, 0]
        # 周りの壁
        for x in range(self.MAZE_W):
            self.maze[0][x] = 1
            self.maze[self.MAZE_H-1][x] = 1
        for y in range(1, self.MAZE_H-1):
            self.maze[y][0] = 1
            self.maze[y][self.MAZE_W-1] = 1
        # 中を何もない状態に
        for y in range(1, self.MAZE_H-1):
            for x in range(1, self.MAZE_W-1):
                self.maze[y][x] = 0
        # 柱
        for y in range(2, self.MAZE_H-2, 2):
            for x in range(2, self.MAZE_W-2, 2):
                self.maze[y][x] = 1
        # 柱から上下左右に壁を作る
        for y in range(2, self.MAZE_H-2, 2):
            for x in range(2, self.MAZE_W-2, 2):
                d = random.randint(0, 3)
                if x > 2:# 二番目からは左に壁を作らない
                    d = random.randint(0, 2)
                self.maze[y+YP[d]][x+XP[d]] = 1
            
        #迷路からダンジョンを作る
        #全体を壁にする
        for y in range(self.DUNGEON_H):
            for x in range(self.DUNGEON_W):
                self.dungeon[y][x] = 9
        # 部屋と通路の配置
        for y in range(1, self.MAZE_H-1):
            for x in range(1, self.MAZE_W-1):
                dx = x*3+1
                dy = y*3+1
                if self.maze[y][x] == 0:
                    if random.randint(0, 99) < 20:# 部屋を作る
                        for ry in range(-1, 2):
                            for rx in range(-1, 2):
                                self.dungeon[dy+ry][dx+rx] = 0
                    else: # 通路を作る
                        self.dungeon[dy][dx] = 0
                        if self.maze[y-1][x] == 0: self.dungeon[dy-1][dx] = 0
                        if self.maze[y+1][x] == 0: self.dungeon[dy+1][dx] = 0
                        if self.maze[y][x-1] == 0: self.dungeon[dy][dx-1] = 0
                        if self.maze[y][x+1] == 0: self.dungeon[dy][dx+1] = 0

    def boss_dungeon(self): # ボスダンジョンの生成
        #周りの壁
        for y in range(self.DUNGEON_H):
            for x in range(self.DUNGEON_W):
                self.dungeon[y][x] = 9
        # 中をなにも無い状態に
        for y in range(2, self.DUNGEON_H-2):
            for x in range(2, self.DUNGEON_W-2):
                self.dungeon[y][x] = 0
        # マップの生成
        for y in range(2, 7):
            for x in range(2, 19):
                self.dungeon[y][x] = 9
        for y in range(2, 7):
            for x in range(24, 43):
                self.dungeon[y][x] = 9
        for y in range(7, 9):
            for x in range(21):
                self.dungeon[y][x] = 9
        for y in range(7, 9):
            for x in range(22, 43):
                self.dungeon[y][x] = 9
        for y in range(18, 20):
           for x in range(21):
                self.dungeon[y][x] = 9
        for y in range(18, 20):
            for x in range(22, 43):
                self.dungeon[y][x] = 9
        for y in range(20, 25):
            for x in range(19):
                self.dungeon[y][x] = 9
        for y in range(20, 25):
            for x in range(24, 43):
                self.dungeon[y][x] = 9

    def put_boss_event(self, pl): # ボスのフロアにイベントの配置をする
        #　階段の配置
        y = 4
        x = 21
        self.dungeon[y][x] = 3
                
            #　繭の配置
        for i in range(15):
            x = random.randint(2, 42)
            y = random.randint(9, 17)
            self.dungeon[y][x] = 2
    
        # 宝箱の配置
        for i in range(3):
            x = random.randint(2, 42)
            y = random.randint(9, 17)
            self.dungeon[y][x] = 1
        for y in range(2,3):
            for x in range(19, 24):
                self.dungeon[y][x] = 4
                
        # ボスの配置
        boss_y = 8
        boss_x = 21
        self.dungeon[boss_y][boss_x] = 5
        
        # プレイヤーの配置
        pl.pl_x = 21
        pl.pl_y = 22
        pl.pl_d = 1
        pl.pl_a = 2
            
    def put_event(self, pl): # 床にイベントを配置する  
        #　階段の配置
        while True:
            x = random.randint(3, self.DUNGEON_W-4)
            y = random.randint(3, self.DUNGEON_H-4)
            if (self.dungeon[y][x]) == 0:
               for ry in range(-1, 2): # 階段の周囲を床にする
                   for rx in range(-1, 2):
                       self.dungeon[y+ry][x+rx] = 0
               self.dungeon[y][x] = 3
               break
       
        #　繭の配置
        for i in range(35):
            x = random.randint(3, self.DUNGEON_W-4)
            y = random.randint(3, self.DUNGEON_H-4)
            if (self.dungeon[y][x] == 0):
                self.dungeon[y][x] = 2
            
        # 宝箱の配置
        for i in range(10):
            x = random.randint(3, self.DUNGEON_W-4)
            y = random.randint(3, self.DUNGEON_H-4)
            if (self.dungeon[y][x] == 0 and
                self.dungeon[y-1][x] != 3 and
                self.dungeon[y+1][x] != 3 and
                self.dungeon[y][x+1] != 3 and
                self.dungeon[y][x-1] != 3 and
                self.dungeon[y-1][x-1] != 3 and
                self.dungeon[y+1][x-1] != 3 and
                self.dungeon[y+1][x+1] != 3 and
                self.dungeon[y-1][x+1] != 3):
                for ry in range(-1, 2): # 宝箱の周囲を床にする
                   for rx in range(-1, 2):
                        self.dungeon[y+ry][x+rx] = 0
                self.dungeon[y][x] = 1
            
        # プレイヤーの初期配置
        while True:
            pl.pl_x = random.randint(3, self.DUNGEON_W-4)
            pl.pl_y = random.randint(3, self.DUNGEON_H-4)
            if(self.dungeon[pl.pl_y][pl.pl_x] == 0):
                break
        pl.pl_d = 1
        pl.pl_a = 2

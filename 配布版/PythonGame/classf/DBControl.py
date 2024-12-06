
import psycopg2

class DBcontrol():
    dsn = ""                  #接続文字列
    floor = 0
    boss = False
    idx = 0
    def __init__(self, dsn):
        #制御情報の初期化
        self.dsn = dsn
        self.floor = 0
        self.boss = False
        self.idx = 0

    def floorMax(self):
        conn = 1  #１のままの場合DB接続失敗なのでコネクション終了処理を飛ばす
        cur = 1   #１のままの場合DB接続失敗なのでコネクション終了処理を飛ばす
        fl_max = 0
        try:
            conn = psycopg2.connect(self.dsn)
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
        return fl_max
    
    def UpdateflMax(self, fl_max):
        conn = 1    #１のままの場合接続失敗
        cur = 1     #１のままの場合接続失敗
        try:
            conn = psycopg2.connect(self.dsn)
            cur = conn.cursor()
            cur.execute("UPDATE test SET id = %s", (fl_max,))
            conn.commit()
            cur.execute("select id from test where name = 'MAX';")
            (fl_max,) = cur.fetchone()
            cur.close()
        except:
            if conn != 1:
                conn.rollback()
        finally:
            if conn != 1:
                conn.close()
            if cur != 1:
                cur.close()

    def Save_data(self, pl, floor, idx, boss, maps): #セーブする

        skill_cint = 0
        boss_int = 0
    
        # skill_cフラグを数値に変える
        if(pl.skill_c):
            skill_cint = 1
        else:
            skill_cint = 0
        
        # bossフラグを数値に変える
        if(boss):
            boss_int = 1
        else:
            boss_int = 0
    
        sData = [pl.pl_lv, pl.pl_exp, pl.max_exp, pl.potion, pl.blazegem, pl.pl_lifemax, pl.pl_life, pl.def_ca, pl.def_c,
                 pl.pl_atk, pl.pl_def, pl.pl_acy, pl.pl_eva, pl.SP, pl.max_SP, pl.skill, pl.pl_mp, pl.pl_mpmax, skill_cint, floor, pl.pl_p,
                 boss_int, idx, pl.pl_x, pl.pl_y]
        try:
            conn = 1    #１のままの場合接続に失敗
            cur = 1     #１のままの場合接続に失敗
            conn = psycopg2.connect(self.dsn)
            cur = conn.cursor()

            # 前回情報の削除
            cur.execute("DELETE FROM status WHERE id = %s;", "1")
            cur.execute("DELETE FROM map_info WHERE id = %s;", "1")
            conn.commit()
    
            # カウンタ変数
            i = 0
            # 今回データ（プレイヤー情報）
            for dName in sData:
                cur.execute("INSERT INTO status(id, status_name, state, stateid) VALUES(1, 'TEST', %s, %s);", (str(dName), str(i)))
                i += 1
      
            # 床情報
            param = 0
            # 今回データ（ダンジョン情報）
            for y in range(maps.DUNGEON_H):
                for x in range(maps.DUNGEON_W):
                    param = maps.dungeon[y][x]
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

    def Load_data(self, pl, maps): #ロードする
        #データをDBからロードする
        try:
            conn = 1  #１のままの場合DB接続失敗なのでコネクション終了処理を飛ばす
            cur = 1   #１のままの場合DB接続失敗なのでコネクション終了処理を飛ばす
            conn = psycopg2.connect(self.dsn)
            cur = conn.cursor()
            # 情報読込
            cur.execute("select state from status where id = 1 order by stateid;")
            lData= cur.fetchall()
            
            #プレイヤー情報セット
            pl.pl_lv = lData[0][0]
            pl.pl_exp = lData[1][0]
            pl.max_exp = lData[2][0]
            pl.potion = lData[3][0]
            pl.blazegem = lData[4][0]
            pl.pl_lifemax = lData[5][0]
            pl.pl_life = lData[6][0]
            pl.def_ca = lData[7][0]
            pl.def_c = lData[8][0]
            pl.pl_atk = lData[9][0]
            pl.pl_def = lData[10][0]
            pl.pl_acy = lData[11][0]
            pl.pl_eva = lData[12][0]
            pl.SP = lData[13][0]
            pl.max_SP = lData[14][0]
            pl.skill = lData[15][0]
            pl.pl_mp = lData[16][0]
            pl.pl_mpmax = lData[17][0]
            if(lData[18][0] == 0):
                pl.skill_c = False
            else:
                pl.skill_c = True
            self.floor = lData[19][0]
            pl.pl_p = lData[20][0]
            if(lData[21][0] == 0):
                self.boss = False
            else:
                self.boss = True
            self.idx = lData[22][0]
            pl.pl_x = lData[23][0]
            pl.pl_y = lData[24][0]
            
            #マップ情報セット
            cur.execute("select * from map_info where id = 1;")
            lDatamap= cur.fetchall()
            for lDatamapValue in lDatamap:
                maps.dungeon[lDatamapValue[2]][lDatamapValue[1]] = lDatamapValue[3]
            cur.close()
        except psycopg2.Error as e:
            if conn != 1:
                conn.rollback()
        finally:
            if cur != 1:   
                cur.close()
            if conn != 1:
                conn.close()
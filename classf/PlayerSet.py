class PlayerSet():
    #プレイヤーステータス
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
    pl_x = 0
    pl_y = 0
    pl_d = 0
    pl_a = 0
    
    #アイテム
    potion = 0
    blazegem = 0
    
    #プレイヤーステータス(リセット用)
    rs_pl_lifemax = 0
    rs_pl_life = 0
    rs_pl_mpmax = 0
    rs_pl_mp = 0
    rs_pl_atk = 0
    rs_pl_def = 0
    rs_pl_acy = 0
    rs_pl_eva = 0
    rs_pl_exp = 0
    rs_pl_lv = 1
    rs_pl_p = 0
    rs_max_exp = 0
    rs_SP = 0
    rs_max_SP = 0
    rs_skill = 0
    rs_skill_c = True
    rs_def_ca = 0
    rs_def_c = 0
    rs_pl_x = 0
    rs_pl_y = 0
    rs_pl_d = 0
    rs_pl_a = 0

    #アイテム
    rs_potion = 0
    rs_blazegem = 0

    
    def __init__(self, pl_lifemax_s, pl_mpmax_s, pl_atk_s,
                pl_def_s, pl_acy_s, pl_eva_s, pl_p_s,
                pl_exp_s, max_SP_s, skill_s, pl_lv_s,
                potion_s, blazegem_s, def_ca_s, def_c_s,
                skill_c_s): #初期化処理
        #プレイヤーステータス
        self.pl_lifemax = pl_lifemax_s
        self.pl_life = pl_lifemax_s
        self.pl_mpmax = pl_mpmax_s
        self.pl_mp = pl_mpmax_s
        self.pl_atk = pl_atk_s
        self.pl_def = pl_def_s
        self.pl_acy = pl_acy_s
        self.pl_eva = pl_eva_s
        self.pl_exp = pl_exp_s
        self.pl_lv = pl_lv_s
        self.pl_p = pl_p_s
        self.max_exp = 0
        self.SP = max_SP_s
        self.max_SP = max_SP_s
        self.skill = skill_s
        self.skill_c = skill_c_s
        self.def_ca = def_ca_s
        self.def_c = def_c_s
        self.pl_x = 0
        self.pl_y = 0
        self.pl_d = 0
        self.pl_a = 0

        #アイテム
        self.potion = potion_s
        self.blazegem = blazegem_s
        
        #リセット用の保持
        #プレイヤーステータス
        self.rs_pl_lifemax = pl_lifemax_s
        self.rs_pl_life = pl_lifemax_s
        self.rs_pl_mpmax = pl_mpmax_s
        self.rs_pl_mp = pl_mpmax_s
        self.rs_pl_atk = pl_atk_s
        self.rs_pl_def = pl_def_s
        self.rs_pl_acy = pl_acy_s
        self.rs_pl_eva = pl_eva_s
        self.rs_pl_exp = pl_exp_s
        self.rs_pl_lv = pl_lv_s
        self.rs_pl_p = pl_p_s
        self.rs_max_exp = 0
        self.rs_SP = max_SP_s
        self.rs_max_SP = max_SP_s
        self.rs_skill = skill_s
        self.rs_skill_c = skill_c_s
        self.rs_def_ca = def_ca_s
        self.rs_def_c = def_c_s
        self.rs_pl_x = 0
        self.rs_pl_y = 0
        self.rs_pl_d = 0
        self.rs_pl_a = 0
        #アイテム
        self.rs_potion = potion_s
        self.rs_blazegem = blazegem_s
        
    def player_exp(self):# 経験値の管理
        i = self.pl_lv - 1
        #経験値リストレベル60まで
        exp_list = [
                    100,200,300,400,650,900,1300,1800,2600,3200,
                    4000,5000,6000,7000,8000,9000,10000,11000,12000,13000,
                    15000,17000,19000,21000,23000,25000,27000,29000,31000,33000,
                    36000,39000,42000,45000,48000,51000,54000,57000,60000,63000,
                    68000,73000,78000,83000,88000,93000,98000,103000,108000,113000,
                    123000,133000,143000,153000,163000,173000,183000,193000,203000,213000
                    ]
        #レベル60以上は倍数で管理
        if i >= 60:
            self.max_exp *= 1.2
        else:
            self.max_exp = exp_list[i]
    
        #レベル5以上と15レベル以上は新スキル獲得
        if self.pl_lv == 5:
            self.skill = self.skill + 1
        if self.pl_lv == 15:
            self.skill = self.skill + 1
    
    def resetPlayer(self): #プレイヤー情報リセット
        #プレイヤーステータス
        self.pl_lifemax = self.rs_pl_lifemax
        self.pl_life = self.rs_pl_life
        self.pl_mpmax = self.rs_pl_mpmax 
        self.pl_mp = self.rs_pl_mp
        self.pl_atk = self.rs_pl_atk
        self.pl_def = self.rs_pl_def 
        self.pl_acy = self.rs_pl_acy
        self.pl_eva = self.rs_pl_eva
        self.pl_exp = self.rs_pl_exp
        self.pl_lv = self.rs_pl_lv
        self.pl_p = self.rs_pl_p 
        self.max_exp = 0
        self.SP = self.rs_SP
        self.max_SP = self.rs_max_SP
        self.skill = self.rs_skill 
        self.skill_c = self.rs_skill_c
        self.def_ca = self.rs_def_ca
        self.def_c = self.rs_def_c
        self.rs_pl_x = 0
        self.rs_pl_y = 0
        self.rs_pl_d = 0
        self.rs_pl_a = 0

        #アイテム
        self.potion = self.rs_potion 
        self.blazegem = self.rs_blazegem
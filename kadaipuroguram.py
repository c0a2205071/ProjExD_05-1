import sys
import time
import random

import pygame as pg

# 色の数値の設定
white = (255,255,255)
black = (0,0,0)
green = (0,150,0)
red = (255,0,0)
blue = (0,0,255)
light_blue = (147,251,253)
width = 1600 # ディスプレイの横の長さ
height = 900 # ディスプレイの縦の長さ
goalheight = 150 # ゴールの範囲

def check_bound(area: pg.Rect, obj: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj.left < area.left or area.right < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < area.top or area.bottom < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

def check_bound_hockey(scr_rect: pg.Rect, obj_rect: pg.Rect):
    """
    ホッケーの動く範囲を指定
    """
    yoko, tate = True, True
    if obj_rect.center <  scr_rect.center:
        if obj_rect.left < scr_rect.left or scr_rect.centerx < obj_rect.right:
            yoko = False
    if obj_rect.center >  scr_rect.center:
        if obj_rect.left < scr_rect.centerx or scr_rect.right < obj_rect.right:
            yoko = False
    if obj_rect.top < scr_rect.top or scr_rect.bottom < obj_rect.bottom:
        tate = False
    return yoko, tate
class playerlect: # パドルに関するクラス
    # 1パターン目の押下キーと移動量の辞書
    _alfa = {
        pg.K_w: (0, -2),
        pg.K_s: (0, +2),
        pg.K_a: (-2, 0),
        pg.K_d: (+2, 0),
    }
    # 2パターン目の押下キーと移動量の辞書
    _delta = {
        pg.K_UP: (0, -2),
        pg.K_DOWN: (0, +2),
        pg.K_LEFT: (-2, 0),
        pg.K_RIGHT: (+2, 0),
    }
    

    def __init__(self, xy: tuple[int,int], zw: tuple[int,int]): 
        self._img1 = pg.transform.rotozoom(pg.image.load(f"ex05/redpad.png"),0, 2.0)
        self._img2 = pg.transform.rotozoom(pg.image.load(f"ex05/bluepad.png"),0, 2.0)
        self._rct1 = self._img1.get_rect()
        self._rct2 = self._img2.get_rect()
        self._rct1.center = xy
        self._rct2.center = zw
        

    def update(self,key_lst: list[bool], screen: pg.Surface):
        for k,mv in __class__._delta.items():
            if key_lst[k]:
                self._rct1.move_ip(mv)
        if check_bound_hockey(screen.get_rect(), self._rct1) != (True, True):
            for k, mv in __class__._delta.items():
                if key_lst[k]:
                    self._rct1.move_ip(-mv[0], -mv[1])
        
        for k,mv in __class__._alfa.items():
            if key_lst[k]:
                self._rct2.move_ip(mv)
        if check_bound_hockey(screen.get_rect(), self._rct2) != (True, True):
            for k, mv in __class__._alfa.items():
                if key_lst[k]:
                    self._rct2.move_ip(-mv[0], -mv[1])

        screen.blit(self._img1,self._rct1)
        screen.blit(self._img2,self._rct2)

class ball: # ディスクに関するクラス
    _dires = [-1, +1]
    def __init__(self):
        self._img = pg.image.load(f"ex05/disc.png")
        self._rct = self._img.get_rect()
        self._rct.center = width/2,height/2
        self._vx, self._vy = random.choice(ball._dires), random.choice(ball._dires)
        
    def update(self,screen: pg.Surface, pl: playerlect):

        yoko,tate = check_bound(screen.get_rect(), self._rct)
        if not yoko:
            self._vx *= -1
        if not tate:
            self._vy *= -1

        if pl._rct1.colliderect(self._rct):
            self._vx *= random.choice(ball._dires)
            self._vy *= random.choice(ball._dires)
        
        if pl._rct2.colliderect(self._rct):
            self._vx *= random.choice(ball._dires)
            self._vy *= random.choice(ball._dires)

        self._rct.move_ip(self._vx, self._vy)
        screen.blit(self._img,self._rct)
        
    def check_goal_in(self, scr_rect: pg.Rect, goalheight):
        """
        玉がゴールに入ったか否か、ゴールに入ったとしたらどちらのゴールかを判定する.
        引数：クラス自身で定義した変数
        引数：画面SurfaceのRect
        引数：ゴールの高さ
        戻り値：それぞれのゴールの衝突判定 左ゴール判定left: True or False / 右ゴール判定right: True or False
        """
        goal_in_left = False
        goal_in_right = False
        if (self._rct.left <= scr_rect.left) and (self._rct.top <= scr_rect.centery + goalheight) and (self._rct.bottom >= scr_rect.centery - goalheight):
            goal_in_left = True
        if (self._rct.right >= scr_rect.right) and (self._rct.top <= scr_rect.centery + goalheight) and (self._rct.bottom >= scr_rect.centery - goalheight):
            goal_in_right = True
        return goal_in_left, goal_in_right


def main():
    pg.display.set_caption("Air-hockey")
    screen = pg.display.set_mode((1600,900))
    pl1 = playerlect((width-300,height/2),(300,height/2))
    disc = ball()
    clock = pg.time.Clock()
    fonto = pg.font.Font(None, 80)
    fonto2 = pg.font.Font(None, 80)
    fonto3 = pg.font.Font(None, 80)
    score1 = 0
    score2 = 0
    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        screen.fill((0,0,0))
        
        # ディスプレイの周りに表示する線に関するプログラム
        pg.draw.line(screen, blue,(0,0), (screen.get_width()/2 - 5,0) ,20)
        pg.draw.line(screen, blue,(0,screen.get_height()), (screen.get_width()/2 - 5,screen.get_height()) ,20)
        pg.draw.line(screen, red, (screen.get_width()/2+5,0), (screen.get_width() ,0) ,20)
        pg.draw.line(screen, red, (screen.get_width()/2 + 5,screen.get_height()) , (screen.get_width(),screen.get_height()) ,20)
        pg.draw.line(screen,white,(width/2,0),(width/2,height),5)
        pg.draw.line(screen, blue, (0,0), (0,screen.get_height()/2-goalheight) ,5)
        pg.draw.line(screen, blue, (0,screen.get_height()/2 + goalheight), (0,screen.get_height()) ,5)
        pg.draw.line(screen, red, (screen.get_width(),0), (screen.get_width(),screen.get_height()/2-goalheight) ,5)
        pg.draw.line(screen, red, (screen.get_width(),screen.get_height()/2 + goalheight), (screen.get_width(),screen.get_height()) ,5)

        # ゴール判定 左ゴールに入った場合、g_leftがTrueに,右ゴールに入った場合、g_rightがTrueにそれぞれなる
        g_left, g_right = disc.check_goal_in(screen.get_rect(), goalheight)
        if g_left == True:
            score2 += 1  # 得点機能
            disc = ball()
        if g_right == True:
            score1 += 1
            disc = ball()
        if score1 == 5 or score2 == 5:
            txt2 = fonto3.render("Game Set!", True, (255, 0, 0)) 
            screen.blit(txt2, [700, 200]) 
            pg.display.update()
            time.sleep(1) 
            break

        key_lst = pg.key.get_pressed()
        
        pl1.update(key_lst,screen)  # 得点の表示
        txt = fonto.render(str(int(score1)), True, (255, 255, 255))
        screen.blit(txt, [400, 200])
        txt2 = fonto2.render(str(int(score2)), True, (255, 255, 255))  
        screen.blit(txt2, [1200, 200])  
        disc.update(screen, pl1)
        pg.display.update()
        clock.tick(1000)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
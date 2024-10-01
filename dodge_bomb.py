import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 移動量の定義
DELTA = {
    pg.K_UP: (0, -5),    # 上矢印で上に移動
    pg.K_DOWN: (0, 5),   # 下矢印で下に移動
    pg.K_LEFT: (-5, 0),  # 左矢印で左に移動
    pg.K_RIGHT: (5, 0)   # 右矢印で右に移動
}
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 横方向速度と縦方向速度
    vx, vy = 5, 5

    # 爆弾のSurfaceを作成
    bomb_radius = 10  # 半径
    bomb_color = (255, 0, 0)  # 赤色
    bb_img = pg.Surface((bomb_radius * 2, bomb_radius * 2), pg.SRCALPHA)  # 透明背景のSurface
    pg.draw.circle(bb_img, bomb_color, (bomb_radius, bomb_radius), bomb_radius)
    clock = pg.time.Clock()

    # 爆弾の初期位置をランダムに作成
    bb_rct = bb_img.get_rect()
    bb_rct.x = random.randint(0, WIDTH - bb_rct.width)
    bb_rct.y = random.randint(0, HEIGHT - bb_rct.height)

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)

        # 爆弾の位置を更新
        bb_rct.move_ip(vx, vy)

        # 爆弾を画面に描画
        screen.blit(bb_img, bb_rct)
        
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

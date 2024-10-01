import os
import sys
import pygame as pg
import random
import time

# ウィンドウの幅と高さを定義
WIDTH, HEIGHT = 1100, 650

# スクリプトの実行ファイルのディレクトリに移動
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 移動量の定義
DELTA = {
    pg.K_UP: (0, -5),    
    pg.K_DOWN: (0, 5),   
    pg.K_LEFT: (-5, 0),  
    pg.K_RIGHT: (5, 0)   
}

# 加速度リストと爆弾のサイズリストを作成
saccs = [a for a in range(1, 11)]
bb_imgs = [pg.Surface((20 * r, 20 * r), pg.SRCALPHA) for r in range(1, 11)]
for r in range(1, 11):
    pg.draw.circle(bb_imgs[r-1], (255, 0, 0), (10 * r, 10 * r), 10 * r)

def game_over_screen(screen: pg.Surface, kk_img: pg.Surface):
    screen.fill((0, 0, 0))
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    font = pg.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(kk_img, (WIDTH // 2 - kk_img.get_width() // 2, HEIGHT // 2 + 50))

    pg.display.update()
    time.sleep(5)

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj_rct.left < 0 or obj_rct.right > WIDTH:
        yoko = False
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:
        tate = False
    return yoko, tate

def get_bomb_properties(tmr: int) -> tuple[pg.Surface, float]:
    """
    タイマーに応じて爆弾のSurfaceと加速度を返す関数。
    
    Args:
        tmr (int): タイマーの値
        
    Returns:
        tuple[pg.Surface, float]: 爆弾のSurfaceと加速度
    """
    index = min(tmr // 500, 9)  # タイマーに基づくインデックスを計算
    return bb_imgs[index], saccs[index]

def get_movement_and_image(key_lst, kk_img: pg.Surface) -> pg.Surface:
    """
    こうかとんの移動方向に基づいて画像を回転または反転する。
    
    Args:
        key_lst: 現在押されているキーのリスト
        kk_img: こうかとんの画像Surface
    
    Returns:
        pg.Surface: 移動方向に応じて回転・反転された画像
    """
    # 移動量の初期化
    sum_mv = [0, 0]  # [x, y]

    # 各方向のキーをチェックし、移動量を計算
    for key in DELTA.keys():
        if key_lst[key]:
            sum_mv[0] += DELTA[key][0]
            sum_mv[1] += DELTA[key][1]

    # 移動量に基づいて角度を計算して画像を回転・反転
    if sum_mv != [0, 0]:  # 移動がある場合
        angle = 0
        rotated_image = kk_img

        # 右移動
        if sum_mv == [5, 0]:
            rotated_image = pg.transform.flip(kk_img, True, False)  # 右向き反転
            angle = 0
        # 右上
        elif sum_mv == [5, -5]:
            rotated_image = pg.transform.flip(kk_img, True, False)
            angle = 45
        # 右下
        elif sum_mv == [5, 5]:
            rotated_image = pg.transform.flip(kk_img, True, False)
            angle = -45
        # 左移動
        elif sum_mv == [-5, 0]:
            angle = 0
        # 左上
        elif sum_mv == [-5, -5]:
            angle = -45  # 左上は反時計回り
        # 左下
        elif sum_mv == [-5, 5]:
            angle = 45  # 左下は時計回り
        # 上移動
        elif sum_mv == [0, -5]:
            angle = -90
        # 下移動
        elif sum_mv == [0, 5]:
            angle = 90

        # 画像を回転（角度に応じて適切な回転を行う）
        rotated_image = pg.transform.rotozoom(rotated_image, angle, 1)
        return rotated_image

    return kk_img  # 移動がない場合はそのままの画像を返す





def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # 背景画像とこうかとんの画像を読み込む
    bg_img = pg.image.load(os.path.join("fig", "pg_bg.jpg"))
    kk_img = pg.transform.rotozoom(pg.image.load(os.path.join("fig", "3.png")), 0, 0.9)

    # こうかとんの初期位置
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200  

    # 爆弾の初期位置
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.x = random.randint(0, WIDTH - bb_rct.width)
    bb_rct.y = random.randint(0, HEIGHT - bb_rct.height)

    vx, vy = 5, 5  # 爆弾の速度
    clock = pg.time.Clock()

    tmr = 0  # タイマー

    frame_count = 0
    frame_limit = 100  # 100フレームごとに出力

    while True:
        # イベント処理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return  

        frame_count += 1
        # 出力回数を制限
        if frame_count % frame_limit == 0:
            print("Pythonなんて大っ嫌い二度と見なくない\n")
            
        screen.blit(bg_img, [0, 0])

        # キーの押下状態を取得
        key_lst = pg.key.get_pressed()
        
        # こうかとんの画像を更新（移動方向に基づいて回転）
        rotated_kk_img = get_movement_and_image(key_lst, kk_img)
        
        # 移動量を取得
        sum_mv = [0, 0]
        for key in DELTA.keys():
            if key_lst[key]:
                sum_mv[0] += DELTA[key][0]
                sum_mv[1] += DELTA[key][1]

        # こうかとんの移動
        kk_rct.move_ip(sum_mv)

        # 画面外チェック
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # 回転した画像を描画
        screen.blit(rotated_kk_img, kk_rct)

        # タイマーに基づいて爆弾のプロパティを取得
        bb_img, acc = get_bomb_properties(tmr)
        avx = vx * acc

        # 爆弾の移動
        bb_rct.move_ip(avx, vy)

        # 爆弾が画面外に出たら方向転換
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1  
        if not tate:
            vy *= -1  

        # 爆弾を描画
        screen.blit(bb_img, bb_rct)

        pg.display.update()

        clock.tick(50)

        tmr += 1  # タイマーを1増加

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            print("衝突！")
            game_over_screen(screen, kk_img)
            return  
 


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

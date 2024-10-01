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
    pg.K_UP: (0, -5),    # 上矢印で上に移動
    pg.K_DOWN: (0, 5),   # 下矢印で下に移動
    pg.K_LEFT: (-5, 0),  # 左矢印で左に移動
    pg.K_RIGHT: (5, 0)   # 右矢印で右に移動
}

def game_over_screen(screen: pg.Surface, kk_img: pg.Surface):
    """
    ゲームオーバー画面を表示する関数。
    Args:
        screen (pg.Surface): ゲーム画面
        kk_img (pg.Surface): 泣いているこうかとんの画像
    """
    # 画面をブラックアウト
    screen.fill((0, 0, 0))
    
    # 半透明の黒いオーバーレイを描画
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)  # 半透明度の設定
    screen.blit(overlay, (0, 0))
    
    # "Game Over" テキストを表示
    font = pg.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))  # 赤色のテキスト
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    # 泣いているこうかとんの画像を表示
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(kk_img, (WIDTH // 2 - kk_img.get_width() // 2, HEIGHT // 2 + 50))

    # 画面を更新して5秒間停止
    pg.display.update()
    time.sleep(5)

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    画面内か外かをチェックする関数。
    Args:
        obj_rct (pg.Rect): 矩形オブジェクト（こうかとん or 爆弾）
    Returns:
        tuple[bool, bool]: 横方向・縦方向の真理値タプル（True: 画面内 / False: 画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or obj_rct.right > WIDTH:
        yoko = False
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:
        tate = False
    return yoko, tate

def main():
    # ゲームのウィンドウのタイトルを設定
    pg.display.set_caption("逃げろ！こうかとん")
    
    # ゲーム画面を作成
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # 背景画像とこうかとんの画像を読み込み
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    
    # こうかとんの矩形（位置とサイズ）を取得
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200  # 初期位置を設定

    # 爆弾のSurfaceを作成
    bomb_radius = 10  # 半径
    bomb_color = (255, 0, 0)  # 赤色
    bb_img = pg.Surface((bomb_radius * 2, bomb_radius * 2), pg.SRCALPHA)  # 透明背景のSurface
    pg.draw.circle(bb_img, bomb_color, (bomb_radius, bomb_radius), bomb_radius)

    # 爆弾の初期位置をランダムに作成
    bb_rct = bb_img.get_rect()
    bb_rct.x = random.randint(0, WIDTH - bb_rct.width)
    bb_rct.y = random.randint(0, HEIGHT - bb_rct.height)

    # 横方向速度と縦方向速度
    vx, vy = 5, 5
    
    # フレームレート管理用の時計
    clock = pg.time.Clock()

    tmr = 0  # タイマー変数

    # ゲームループ
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # ウィンドウが閉じられた場合
                return  # メイン関数を終了

        # 背景を描画
        screen.blit(bg_img, [0, 0])

        # 押下中のキーを取得
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 移動量の初期化

        # 各方向のキーが押されているかをチェックし、移動量を更新
        for key in DELTA.keys():
            if key_lst[key]:
                sum_mv[0] += DELTA[key][0]
                sum_mv[1] += DELTA[key][1]
        
        # こうかとんを移動
        kk_rct.move_ip(sum_mv)

        # こうかとんの画面内チェック
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 画面外なら移動をキャンセル

        # こうかとんを画面に描画
        screen.blit(kk_img, kk_rct)

        # 爆弾の位置を更新
        bb_rct.move_ip(vx, vy)

        # 爆弾の画面内チェック
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1  # 横方向の速度を反転
        if not tate:
            vy *= -1  # 縦方向の速度を反転

        # 爆弾を画面に描画
        screen.blit(bb_img, bb_rct)
        
        # 画面を更新
        pg.display.update()
        
        # フレームレートを50fpsに設定
        clock.tick(50)
        
        tmr += 1  # タイマー更新

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            print("衝突！")  # 衝突した場合のメッセージ
            game_over_screen(screen, kk_img)
            return  # メイン関数を終了

if __name__ == "__main__":
    pg.init()  # Pygameの初期化
    main()  # メイン関数を実行
    pg.quit()  # Pygameを終了
    sys.exit()  # プログラムを終了

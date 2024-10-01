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

# 加速度リストと爆弾のサイズリストを作成
saccs = [a for a in range(1, 11)]  # 1から10までの加速度リスト
bb_imgs = [pg.Surface((20 * r, 20 * r), pg.SRCALPHA) for r in range(1, 11)]  # 爆弾のSurfaceを生成
for r in range(1, 11):
    pg.draw.circle(bb_imgs[r-1], (255, 0, 0), (10 * r, 10 * r), 10 * r)  # 各爆弾を赤い円で描画

def game_over_screen(screen: pg.Surface, kk_img: pg.Surface):
    # ゲームオーバー画面を表示する関数
    screen.fill((0, 0, 0))  # 画面を黒で塗りつぶす
    overlay = pg.Surface((WIDTH, HEIGHT))  # 半透明のオーバーレイを作成
    overlay.set_alpha(128)  # 半透明度の設定
    screen.blit(overlay, (0, 0))  # オーバーレイを画面に描画
    
    # "Game Over" テキストを表示
    font = pg.font.Font(None, 74)  # フォントの設定
    text = font.render("Game Over", True, (255, 0, 0))  # 赤色のテキストを描画
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # テキストの位置を計算
    screen.blit(text, text_rect)  # テキストを画面に描画

    # 泣いているこうかとんの画像を表示
    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(kk_img, (WIDTH // 2 - kk_img.get_width() // 2, HEIGHT // 2 + 50))

    pg.display.update()  # 画面を更新
    time.sleep(5)  # 5秒間停止

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    # 画面内か外かをチェックする関数
    yoko, tate = True, True  # 初期値は画面内とする
    if obj_rct.left < 0 or obj_rct.right > WIDTH:  # 左右の境界をチェック
        yoko = False  # 画面外
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:  # 上下の境界をチェック
        tate = False  # 画面外
    return yoko, tate  # 横方向・縦方向の真理値タプルを返す

def get_bomb_properties(tmr: int) -> tuple[pg.Surface, float]:
    # タイマーに応じて爆弾のSurfaceと加速度を返す関数
    index = min(tmr // 500, 9)  # タイマーに基づくインデックスを計算
    return bb_imgs[index], saccs[index]  # 爆弾のSurfaceと加速度を返す

def main():
    pg.display.set_caption("逃げろ！こうかとん")  # ウィンドウのタイトルを設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ゲーム画面を作成

    # 背景画像とこうかとんの画像を読み込み
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # こうかとんの画像をリサイズ

    # こうかとんの矩形（位置とサイズ）を取得
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200  # 初期位置を設定

    # 爆弾の初期位置をランダムに作成
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.x = random.randint(0, WIDTH - bb_rct.width)
    bb_rct.y = random.randint(0, HEIGHT - bb_rct.height)

    vx, vy = 5, 5  # 爆弾の初期速度
    clock = pg.time.Clock()  # フレームレート管理用の時計

    tmr = 0  # タイマー変数

    # ゲームループ
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # ウィンドウが閉じられた場合
                return  # メイン関数を終了

        screen.blit(bg_img, [0, 0])  # 背景を描画

        key_lst = pg.key.get_pressed()  # 押下中のキーを取得
        sum_mv = [0, 0]  # 移動量の初期化

        # 各方向のキーが押されているかをチェックし、移動量を更新
        for key in DELTA.keys():
            if key_lst[key]:
                sum_mv[0] += DELTA[key][0]
                sum_mv[1] += DELTA[key][1]

        # 衝突判定
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が衝突したかをチェック
            print("衝突！")  # 衝突した場合のメッセージ
            game_over_screen(screen, kk_img)  # ゲームオーバー画面を表示
            return  # メイン関数を終了
        
        # こうかとんを移動
        kk_rct.move_ip(sum_mv)

        # こうかとんの画面内チェック
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 画面外なら移動をキャンセル

        screen.blit(kk_img, kk_rct)  # こうかとんを画面に描画

        # タイマーに基づいて爆弾のプロパティを取得
        bb_img, acc = get_bomb_properties(tmr)
        avx = vx * acc  # 爆弾の加速度を考慮して速度を計算

        bb_rct.move_ip(avx, vy)  # 爆弾を移動

        # 爆弾の画面内チェック
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1  # 横方向の速度を反転
        if not tate:
            vy *= -1  # 縦方向の速度を反転

        screen.blit(bb_img, bb_rct)  # 爆弾を画面に描画
        
        pg.display.update()  # 画面を更新
        
        clock.tick(50)  # フレームレートを50fpsに設定
        
        tmr += 1  # タイマー更新

        

if __name__ == "__main__":
    pg.init()  # Pygameの初期化
    main()  # メイン関数を実行
    pg.quit()  # Pygameを終了
    sys.exit()  # プログラムを終了

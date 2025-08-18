from rich import print as rprint

import pyxel
import time
from src.settings import *
from src.DataClass import *


class Scene:
    """
    全てのシーンの基底クラス。
    フォントの読み込みなど、共通の初期化処理をここで行う。
    """

    def __init__(self, app):
        self.app = app
        # 各種フォントを読み込んでインスタンス変数に格納
        self.mm8 = pyxel.Font(r"../assets/fonts/misaki_mincho.bdf")  # 8px
        self.mg1_8 = pyxel.Font(r"../assets/fonts/misaki_gothic.bdf")  # 8px
        self.mg2_8 = pyxel.Font(
            r"../assets/fonts/misaki_gothic_2nd.bdf")  # 8px
        self.umplus10 = pyxel.Font(r"../assets/fonts/umplus_j10r.bdf")  # 10px
        self.umplus12 = pyxel.Font(r"../assets/fonts/umplus_j12r.bdf")  # 12px
        self.unifont_jp = pyxel.Font(r"../assets/fonts/unifont_jp.bdf")  # 16px

    def update(self):
        """
        シーンの状態を更新する。
        このメソッドは毎フレーム呼び出される。
        """
        pass

    def draw(self):
        """
        シーンを描画する。
        このメソッドは update の後に毎フレーム呼び出される。
        """
        pyxel.cls(0)


class TitleScene(Scene):
    """
    タイトル画面のシーン。
    ゲームの開始を待機する。
    """

    def __init__(self, app):
        super().__init__(app)

    def update(self):
        """
        タイトル画面の更新処理。
        スペースキーが押されたら、ゲームシーンに遷移する。
        """
        super().update()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.app.current_scene = self.app.scene["game"]

    def draw(self):
        """
        タイトル画面の描画処理。
        ゲームタイトルと開始メッセージを表示する。
        """
        super().draw()
        title_text = TITLE
        w = self.unifont_jp.text_width(title_text)
        h = 16
        pyxel.text((pyxel.width - w) // 2, 10,
                   "Devil card game", 8, self.unifont_jp)
        w = self.umplus10.text_width("Start")
        h = 10
        pyxel.text((pyxel.width - w) // 2, 30, "Start", 8, self.umplus10)
        pyxel.rectb(((pyxel.width - w) // 2)-2, 30, w+4, h+2, 8)


class GameScene(Scene):
    """
    ゲームプレイ中のメインシーン。
    カード選択、戦闘、ターン進行など、ゲームのコアロジックを管理する。
    """

    def __init__(self, app):
        """
        ゲームシーンの初期化。
        プレイヤー、カード、ゲームデータなどのオブジェクトを生成する。
        """
        super().__init__(app)
        self.master_cards = MASTER_CARDS  # ゲームに登場する全カードのリスト

        self.is_standby = False  # TODO: 現在未使用。将来的にターン開始時の準備フェーズなどで使用する可能性あり

        # プレイヤーオブジェクトの生成と初期化
        self.player1 = Player("Alice", 15, [], self.master_cards, [])
        self.player2 = Player("Bob", 15, [], self.master_cards, [])

        # 各プレイヤーに初期手札として5枚のカードをランダムに配る
        i = 0
        while i < 5:
            num1 = pyxel.rndi(0, len(self.master_cards)-1)
            num2 = pyxel.rndi(0, len(self.master_cards)-1)
            self.player1.hand.append(self.master_cards[num1])
            self.player2.hand.append(self.master_cards[num2])
            i += 1

        # ゲーム全体の進行状況を管理するオブジェクト
        self.game = GameData(players=[self.player1, self.player2])

        # プレイヤーが選択したカードを保持する変数
        self.selected_card1 = None
        self.selected_card2 = None

        # 戦闘演出のための状態変数
        self.battle_wait = False  # 戦闘開始前の待機状態フラグ
        self.battle_start_frame = 0  # 戦闘演出を開始したフレーム数

    def update(self):
        """
        ゲームシーンの更新処理。
        プレイヤーの入力、カード選択、戦闘処理の呼び出しなどを行う。
        """
        super().update()

        # --- プレイヤー1のカード選択フェーズ ---
        # プレイヤー1がまだカードを選択していない場合、キー入力(1-5)を受け付ける
        if not self.selected_card1:
            if pyxel.btnp(pyxel.KEY_1):
                self.selected_card1 = self.game.players[0].hand[0]
            elif pyxel.btnp(pyxel.KEY_2):
                self.selected_card1 = self.game.players[0].hand[1]
            elif pyxel.btnp(pyxel.KEY_3):
                self.selected_card1 = self.game.players[0].hand[2]
            elif pyxel.btnp(pyxel.KEY_4):
                self.selected_card1 = self.game.players[0].hand[3]
            elif pyxel.btnp(pyxel.KEY_5):
                self.selected_card1 = self.game.players[0].hand[4]

        # --- プレイヤー2(AI)のカード選択フェーズ ---
        # プレイヤー1がカードを選択済みで、かつプレイヤー2がまだ選択していない場合
        # プレイヤー2は手札からランダムにカードを選択する (現在のAIロジック)
        if self.selected_card1 and not self.selected_card2:
            self.selected_card2 = self.game.players[1].hand[
                pyxel.rndi(0, len(self.game.players[1].hand)-1)]

        # --- 戦闘開始待機フェーズ ---
        # 両プレイヤーのカードが選択され、まだ戦闘待機状態でない場合
        if self.selected_card1 and self.selected_card2 and not self.battle_wait:
            self.battle_wait = True  # 待機状態に移行
            self.battle_start_frame = pyxel.frame_count  # 待機開始フレームを記録

        # --- 戦闘実行フェーズ ---
        # 戦闘待機状態の場合、一定時間(90フレーム)が経過したら戦闘処理を実行する
        if self.battle_wait:
            if pyxel.frame_count - self.battle_start_frame > 90:  # 90フレーム = 3秒 (FPS=30の場合)
                self._battle()  # 戦闘処理の呼び出し

                # 戦闘後のリセット処理
                self.battle_wait = False
                self.selected_card1 = None
                self.selected_card2 = None
                self.is_standby = False  # TODO: is_standby の役割を明確にする必要あり

    def draw(self):
        """
        ゲームシーンの描画処理。
        プレイヤー情報、選択されたカード、現在のターン数などを画面に表示する。
        """
        super().draw()
        # 現在のターン数を表示
        pyxel.text(10, 10, f"Turn: {self.game.turn}", 3, self.umplus10)

        # 各プレイヤーのHUD(Head-Up Display)を描画
        self._draw_player_hud(self.game.players[0], x=10, y=20)
        self._draw_player_hud(self.game.players[1], x=128, y=20)

        # 選択されたカードの情報を描画
        self._draw_card_info(self.selected_card1, x=8)
        self._draw_card_info(self.selected_card2, x=128)

        # 両方のカードが選択されたら "Battle!" の文字を表示
        if self.selected_card1 and self.selected_card2:
            pyxel.text(80, 150, "Battle!", 8, self.mg2_8)

    def _draw_card_info(self, card, x, color=10):
        """
        単一のカード情報を受け取り、指定されたx座標にその詳細を描画する。

        Args:
            card (Card): 描画対象のカードオブジェクト。Noneの場合は何も描画しない。
            x (int): 描画を開始するX座標。
            color (int, optional): 描画に使用するpyxelのカラーコード。デフォルトは10。
        """
        # カードが選択されていない(None)場合は、何もせずに処理を終了
        if not card:
            return

        # カードの各情報を描画
        # カード名
        pyxel.text(x, 100, f"{card.name}", color, self.mg2_8)

        # 爵位 (リスト内の各爵位を描画)
        for i, title_char in enumerate(card.title):
            pyxel.text(x + i * 40, 110, f"{title_char}", color, self.mg2_8)

        # ステータス (攻撃力, 防御力, スピード)
        pyxel.text(x, 120, f"ATK: {card.attack}", color, self.mg2_8)
        pyxel.text(x, 130, f"DEF: {card.defense}", color, self.mg2_8)
        pyxel.text(x, 140, f"SPD: {card.speed}", color, self.mg2_8)

    def _draw_player_hud(self, player, x, y, color=3):
        """
        指定されたプレイヤーのHUD（名前、ライフ、手札）を指定座標に描画する。

        Args:
            player (Player): 描画対象のプレイヤーオブジェクト。
            x (int): 描画を開始するX座標。
            y (int): 描画を開始するY座標。
            color (int, optional): 描画に使用するpyxelのカラーコード。デフォルトは3。
        """
        # ライフを描画
        life_y = y
        pyxel.text(x, life_y, f"Life: {player.life}", color, self.umplus10)

        # プレイヤー名を描画
        player_name_y = y + 10
        pyxel.text(x, player_name_y, player.name, color, self.umplus10)

        # 手札のリストを描画
        hand_start_y = y + 24  # 手札表示の開始Y座標
        line_height = 10       # 手札1枚ごとの行の高さ

        for i, card in enumerate(player.hand):
            # 手札の番号とカード名を表示
            display_text = f"{i+1}:{card.name}"
            draw_y = hand_start_y + i * line_height
            pyxel.text(x, draw_y, display_text, color, self.mg2_8)

    def _battle(self):
        """
        戦闘処理を実行する。
        ダメージ計算を行い、各プレイヤーのライフを更新し、ターンを進める。
        """
        # TODO: 現在のロジックではスピードの速さに関わらず、同時にダメージ計算が行われている。
        #       ルール(rule4.md)に基づき、スピードが速い方の効果から先に解決するロジックへの修正が必要。
        #       例えば、効果の発動とダメージ計算を分離するなどの設計変更が考えられる。

        # ダメージ計算式: 基本ダメージ = 自分の攻撃力 - 相手の防御力 (マイナスなら0)
        basedamage1 = self.selected_card1.attack - self.selected_card2.defense
        basedamage2 = self.selected_card2.attack - self.selected_card1.defense

        # 最終ダメージ計算式: 最終ダメージ = 基本ダメージ * (1 + 魂の数 * 0.1)
        # 小数点以下は切り捨て
        finaldamage1 = int(max(0, basedamage1 * (1 + self.player1.soul_point * 0.1)))
        finaldamage2 = int(max(0, basedamage2 * (1 + self.player2.soul_point * 0.1)))

        # 各プレイヤーのライフから最終ダメージを引く
        self.game.players[1].life -= finaldamage1
        self.game.players[0].life -= finaldamage2

        # TODO: 戦闘後のカード処理。手札から選択したカードを墓地に送る、
        #       山札からカードを1枚引く、などの処理をここに追加する必要がある。

        # ターン数を1進める
        self.game.turn += 1


class ResultScene(Scene):
    """
    リザルト画面のシーン。
    ゲームの勝敗結果を表示する。
    (現在、未実装)
    """

    def __init__(self, app):
        super().__init__(app)

    def update(self):
        """
        リザルト画面の更新処理。
        (現在、未実装)
        """
        super().update()

    def draw(self):
        """
        リザルト画面の描画処理。
        (現在、未実装)
        """
        super().draw()

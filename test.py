from rich import print as rprint
import pyxel
from dataclasses import dataclass, field
from typing import List
import random


@dataclass
class Card:
    """カードのデータを保持"""
    id: int                 # カードの種類を識別する番号
    name: str               # カードの名前
    title: List[str]        # 爵位
    attack: int             # 攻撃力
    defense: int            # 防御力
    speed: int              # スピード

    def __post_init__(self):
        self.description = f"{self.name}({','.join(self.title)}) Attack:{self.attack} Defense:{self.defense} Speed:{self.speed}"


@dataclass
class Player:
    """プレイヤーのデータを保持"""
    id: int                # プレイヤーID
    name: str               # プレイヤーの名前
    hand: List[Card] = field(default_factory=list)      # プレイヤーの手札
    graveyard: List[Card] = field(default_factory=list)  # 使用済みのカード
    hp: int = 15            # HP
    soul: int = 0           # 魂
    selected_card: Card | None = None   # 選択中のカード
    contract_zone: List[Card] = field(default_factory=list)     # 契約ゾーン


# カードデータ
MASTER_CARDS = [
    Card(1, "バエル", ["king"], 1, 5, 72),
    Card(2, "アガレス", ["Duke"], 2, 4, 71),
    Card(3, "ウェサゴ", ["Prince"], 3, 3, 70),
    Card(4, "ガミジン", ["Marquess"], 4, 2, 69),
    Card(5, "マルバス", ["President"], 5, 1, 68),
    Card(6, "ウァレフォル", ["Duke"], 1, 1, 67),
    Card(7, "アモン", ["Marquess"], 2, 2, 66),
    Card(8, "バルバトス", ["Duke"], 3, 3, 65),
    Card(9, "パイモン", ["king"], 4, 4, 64),
    Card(10, "ブエル", ["President"], 5, 5, 63),
]


# ゲームロジック
class App:
    """ゲームのメインクラス"""

    def __init__(self):
        """ゲームの初期化"""
        pyxel.init(256, 256, title="Goetic Gambit Test", fps=30)

        pyxel.mouse(True)

        self.scenes = dict()
        self.scenes["title"] = TitleScene(self)
        self.scenes["game"] = GameScene(self)
        self.scenes["result"] = ResultScene(self)

        self.current_scene = self.scenes["title"]

        pyxel.run(self.updata, self.draw)

    def updata(self):
        self.current_scene.update()

    def draw(self):
        pyxel.cls(0)
        self.current_scene.draw()
# シーン


class Scene:
    """シーンの基底クラス"""

    def __init__(self, app):
        self.app = app
        self.mg2_8 = pyxel.Font(r"./assets/fonts/misaki_gothic_2nd.bdf")

    def update(self):
        pass

    def draw(self):
        pass


class TitleScene(Scene):
    """タイトルシーン"""

    def __init__(self, app):
        super().__init__(app)

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.app.current_scene = self.app.scenes["game"]

    def draw(self):
        pyxel.cls(1)
        pyxel.text(2, 2, "Title", 7)
        pyxel.text(2, 12, "Press Space to Start", 7)


class GameScene(Scene):
    """ゲームシーン"""

    def __init__(self, app):
        super().__init__(app)
        self.cards = MASTER_CARDS
        self.phases = [
            "start",    # ターン開始
            "select",   # カード選択
            "effect",   # 効果解決
            "battle",   # 戦闘
            "contract",  # 契約解決
            "end",      # ターン終了
        ]
        self.setup()

    def setup(self):
        """ゲームを初期化"""
        self.winner = None
        self.current_phase = self.phases[0]
        self.turn = 0
        self.players = [
            Player(0, "Player1"),
            Player(1, "Player2"),
        ]
        for player in self.players:
            for _ in range(4):
                self._draw_card(player)

    def _draw_card(self, player: Player):
        """プレイヤーが山札からカードを1枚引く"""
        card = random.choice(self.cards)
        player.hand.append(card)

    def update(self):
        if self.current_phase == "start":
            """ターン開始"""
            rprint(f"Turn: {self.turn}")
            rprint(f"Current Phase: {self.current_phase}")
            print(f"p1 hp: {self.players[0].hp}")
            print(f"p2 hp: {self.players[1].hp}")
            self.turn += 1
            for player in self.players:
                self._draw_card(player)

            self.current_phase = self.phases[1]

        elif self.current_phase == "select":
            """カード選択"""
            rprint(self.players[0].hand)
            hand_size = len(self.players[0].hand)
            for i in range(hand_size):
                if pyxel.btnp(pyxel.KEY_1 + i):
                    self.players[0].selected_card = self.players[0].hand.pop(i)

                    self.players[1].selected_card = self.players[1].hand.pop(
                        random.randint(0, len(self.players[1].hand) - 1))

                    self.current_phase = self.phases[2]
                    break

        elif self.current_phase == "effect":
            """効果解決"""
            # print(f"Current Phase: {self.current_phase}")
            rprint(self.players[0].selected_card)
            rprint(self.players[1].selected_card)

            # TODO: 惑星バフ、契約の利益

            self.current_phase = self.phases[3]

        elif self.current_phase == "battle":
            """戦闘"""
            # print(f"Current Phase: {self.current_phase}")

            self.p1_speed = self.players[0].selected_card.speed
            self.p2_speed = self.players[1].selected_card.speed

            p1_base_damage = self.players[1].selected_card.attack - \
                self.players[0].selected_card.defense
            p2_base_damage = self.players[0].selected_card.attack - \
                self.players[1].selected_card.defense

            p1_base_damage = int(max(0, p1_base_damage))
            p2_base_damage = int(max(0, p2_base_damage))

            self.players[0].hp -= p1_base_damage
            self.players[1].hp -= p2_base_damage

            self.current_phase = self.phases[4]

        elif self.current_phase == "contract":
            """契約解決"""
            print(f"Current Phase: {self.current_phase}")
            self.current_phase = self.phases[5]

        elif self.current_phase == "end":
            """ターン終了"""
            print(f"Current Phase: {self.current_phase}")
            if self.players[0].hp <= 0 and self.players[1].hp <= 0:
                if self.p1_speed > self.p2_speed:
                    self.winner = "Player1"
                elif self.p1_speed < self.p2_speed:
                    self.winner = "Player2"
                self.app.current_scene = self.app.scenes["result"]
            elif self.players[0].hp <= 0:
                self.winner = "Player2"
                self.app.current_scene = self.app.scenes["result"]
            elif self.players[1].hp <= 0:
                self.winner = "Player1"
                self.app.current_scene = self.app.scenes["result"]
            else:
                self.current_phase = self.phases[0]

    def draw(self):
        pyxel.cls(2)
        if self.current_phase == "start":
            pass
        elif self.current_phase == "select":
            pyxel.text(2, 2, "Please select a card (1-5).", 7)
            pyxel.text(2, 12, f"P1 HP:{self.players[0].hp}", 7)
            pyxel.text(2, 22, f"P2 HP:{self.players[1].hp}", 7)
            for i in range(len(self.players[0].hand)):
                pyxel.text(2, 32 + i * 10,
                           f"{i + 1}: {self.players[0].hand[i].description}", 7, self.mg2_8)
        elif self.current_phase == "effect":
            pass
        elif self.current_phase == "battle":
            pass
        elif self.current_phase == "contract":
            pass
        elif self.current_phase == "end":
            pass


class ResultScene(Scene):
    """リザルトシーン"""

    def __init__(self, app):
        super().__init__(app)

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.app.current_scene = self.app.scenes["game"]
            self.app.current_scene.setup()

    def draw(self):
        pyxel.cls(3)
        pyxel.text(2, 2, "Result", 7)
        pyxel.text(2, 12, f"Winner: {self.app.scenes['game'].winner}", 7)


if __name__ == "__main__":
    App()

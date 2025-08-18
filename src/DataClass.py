from src.settings import *
from dataclasses import dataclass, field
from typing import List


@dataclass
class Card:
    id: int                 # カードの種類を識別する番号
    name: str               # カードの名前
    title: List[str]        # 爵位
    attack: int             # 攻撃力
    defense: int            # 防御力
    speed: int              # スピード
    # TODO: 契約(利益、代償、穢れた魂の増加量)


@dataclass
class Player:
    name: str               # プレイヤーの名前
    life: int = 15          # プレイヤーの体力
    hand: List[Card] = field(default_factory=list)      # プレイヤーの手札
    deck: List[Card] = field(default_factory=list)      # プレイヤーのデッキ
    graveyard: List[Card] = field(default_factory=list)  # 使用済みのカード
    field_card: Card = None
    soul_point: int = 0


@dataclass
class GameData:
    turn: int = 1
    players: List[Player] = field(
        default_factory=lambda: [
            Player(name="Player 1"),
            Player(name="Player 2"),
        ]
    )
    log: List[str] = field(default_factory=list)


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


DEBUG_CARDS = [
    Card(0, "Daemon", ["Debug"], 0, 0, 0),
    Card(99, "デーモンコア", ["Debug"], 99, 99, 99),
]

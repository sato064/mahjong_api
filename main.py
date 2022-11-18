from fastapi import FastAPI
#計算
from mahjong.hand_calculating.hand import HandCalculator
#麻雀牌
from mahjong.tile import TilesConverter
#役, オプションルール
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
#鳴き
from mahjong.meld import Meld
#風(場&自)
from mahjong.constants import EAST, SOUTH, WEST, NORTH
import json
from typing import Dict

app = FastAPI()
calculator = HandCalculator()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
def read_item(item: Dict):
    s_hand = item["s_hand"]
    p_hand = item["p_hand"]
    m_hand = item["m_hand"]
    h_hand = item["h_hand"]
    win = item["win"]
    tsumo = item["tsumo"]
    doras = item["doras"]
    SELF_WIND = item["self_wind"]
    FIELD_WIND = item["field_wind"]
    reach = item["reach"]

    print(m_hand)
    print(p_hand)
    print(s_hand)
    # 役牌処理
    honors = []
    for k in h_hand:
        if k == "t":
            honors.append("1")
        if k == "n":
            honors.append("2")
        if k == "l":
            honors.append("3")
        if k == "e":
            honors.append("4")
        if k == "w":
            honors.append("5")
        if k == "g":
            honors.append("6")
        if k == "r":
            honors.append("7")
    # 手牌処理
    tiles = TilesConverter.string_to_136_array(man=m_hand, pin=p_hand, sou=s_hand, honors=honors)
    # 上がり牌処理
    if win[0] == "s":
        win_tile = TilesConverter.string_to_136_array(sou=win[1])[0]
    elif win[0] == "p":
        win_tile = TilesConverter.string_to_136_array(pin=win[1])[0]
    elif win[0] == "m":
        win_tile = TilesConverter.string_to_136_array(man=win[1])[0]
    elif win[0] in 'tnlewgr':
        if k == "t":
            win_tile = TilesConverter.string_to_136_array(honors='1')[0]
        if k == "n":
            win_tile = TilesConverter.string_to_136_array(honors='2')[0]
        if k == "l":
            win_tile = TilesConverter.string_to_136_array(honors='3')[0]
        if k == "e":
            win_tile = TilesConverter.string_to_136_array(honors='4')[0]
        if k == "w":
            win_tile = TilesConverter.string_to_136_array(honors='5')[0]
        if k == "g":
            win_tile = TilesConverter.string_to_136_array(honors='6')[0]
        if k == "r":
            win_tile = TilesConverter.string_to_136_array(honors='7')[0]
    # Todo:鳴き処理
    melds = None
    # ドラ処理
    dora_indicators = []
    for c, i in enumerate(doras):
        if i == "s":
            print(doras[c+1])
            dora_indicators.append(TilesConverter.string_to_136_array(sou=str(doras[c+1]))[0])
        elif i == "p":
            dora_indicators.append(TilesConverter.string_to_136_array(pin=str(doras[c+1]))[0])
        elif i == "m":
            dora_indicators.append(TilesConverter.string_to_136_array(man=str(doras[c+1]))[0])
        elif i in '123456789':
            continue
        elif i in 'tnelwgr':
            if k == "t":
                win_tile = TilesConverter.string_to_136_array(honors='1')[0]
            if k == "n":
                win_tile = TilesConverter.string_to_136_array(honors='2')[0]
            if k == "l":
                win_tile = TilesConverter.string_to_136_array(honors='3')[0]
            if k == "e":
                win_tile = TilesConverter.string_to_136_array(honors='4')[0]
            if k == "w":
                win_tile = TilesConverter.string_to_136_array(honors='5')[0]
            if k == "g":
                win_tile = TilesConverter.string_to_136_array(honors='6')[0]
            if k == "r":
                win_tile = TilesConverter.string_to_136_array(honors='7')[0]
    # ツモ処理
    if tsumo == 0:
        is_tsumoed = False
    if tsumo == 1:
        is_tsumoed = True
    # リーチ処理
    if reach == 0:
        is_reach = False
    if reach == 1:
        is_reach = True
    # 風の変換
    if SELF_WIND == "EAST":
        player_wind = EAST
    elif SELF_WIND == "WEST":
        player_wind = WEST
    elif SELF_WIND == "SOUTH":
        player_wind = SOUTH
    elif SELF_WIND == "NORTH":
        player_wind = NORTH

    if FIELD_WIND == "EAST":
        round_wind = EAST
    elif FIELD_WIND == "WEST":
        round_wind = WEST
    elif FIELD_WIND == "SOUTH":
        round_wind = SOUTH
    elif FIELD_WIND == "NORTH":
        round_wind = NORTH
    
    config = HandConfig(is_tsumo = is_tsumoed, is_riichi=is_reach, player_wind=player_wind, round_wind=round_wind)
    result = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)
    print(result)
    d = {'oya_point' : result.cost['main'], 'co_point' : result.cost['additional'] , 'yaku' : result.yaku}
    return d
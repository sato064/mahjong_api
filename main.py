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
    win = item["win"]
    tsumo = item["tsumo"]
    print(m_hand)
    print(p_hand)
    print(s_hand)
    tiles = TilesConverter.string_to_136_array(man=m_hand, pin=p_hand, sou=s_hand)
    if(win[0] == "s"):
        win_tile = TilesConverter.string_to_136_array(sou=win[1])[0]
    if(win[0] == "p"):
        win_tile = TilesConverter.string_to_136_array(pin=win[1])[0]
    if(win[0] == "m"):
        print(win[1])
        win_tile = TilesConverter.string_to_136_array(man=win[1])[0]    
    melds = None
    dora_indicators = None
    if tsumo == 0:
        is_tsumoed = False
    if tsumo == 1:
        is_tsumoed = True
    config = HandConfig(is_tsumo = is_tsumoed)
    result = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)
    print(result)
    d = {'point' : result.cost['main'], 'yaku' : result.yaku}
    return d
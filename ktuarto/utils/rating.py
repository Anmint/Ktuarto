# coding: UTF-8

import os
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
        }
basicAuth = HTTPBasicAuth(os.getenv('BASIC_USER'), os.getenv('BASIC_PASSWORD'))

def calcEloRating (PlayerAName, PlayerBName, winNumberPlayerA, winNumberPlayerB, K=32):
    """calcEloRating (eloPlayerA, eloPlayerB, winNumberPlayerA, winNumberPlayerBw K=32)

    ELOレーティングを計算します。PlayerAとPlayerBについて同時に算出します。

    Args:
        eloPlayerA: PlayerAの試合前ELOレーティングです。
        eloPlayerB: PlayerBの試合前ELOレーティングです。
        winNumberPlayerA: PlayerAの勝利数です。引き分けの場合0.5勝としてください。
        winNumberPlayerB: PlayerBの勝利数です。引き分けの場合0.5勝としてください。
        K: ELOレーティング収束速度を決定する定数です。

    Returns:
        (calcedEloPlayerA, calcedEloPlayerB): 各プレイヤーの試合後ELOレーティングをタプルで返します。
    """

    initElo(PlayerAName)
    initElo(PlayerBName)
    eloPlayerA = getElo(PlayerAName)
    eloPlayerB = getElo(PlayerBName)

    # winRateAtoBはAの予測勝率、winRateBtoAはBの予測勝率
    winRateAtoB = 1/(pow(10,(float(eloPlayerB) - float(eloPlayerA))/400) + 1)
    winRateBtoA = 1 - winRateAtoB
    gameNumber = winNumberPlayerA + winNumberPlayerB #全試合数
    # ELO更新
    newEloPlayerA = int(round(eloPlayerA + K * (winNumberPlayerA - gameNumber * winRateAtoB)))
    newEloPlayerB = int(round(eloPlayerB + K * (winNumberPlayerB - gameNumber * winRateBtoA)))

    updateElo(PlayerAName, newEloPlayerA)
    updateElo(PlayerBName, newEloPlayerB)
    
    return (newEloPlayerA,newEloPlayerB)

def initElo(name):
    requests.post(
            "http://quarto.unigiri.net:3001/api/v1/ais",
            headers = headers,
            data = json.dumps({'name': name}),
            auth = basicAuth
            )

def getElo(name):
    response = requests.get(
            f'http://quarto.unigiri.net:3001/api/v1/ais/{name}',
            headers = headers,
            auth = basicAuth
            )
    return response.json()['ai']['elo']

def updateElo(name, elo):
    requests.put(
            f"http://quarto.unigiri.net:3001/api/v1/ais/{name}",
            headers = headers,
            data = json.dumps({'elo': elo}),
            auth = basicAuth
            )

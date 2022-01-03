# coding: UTF-8

import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv

load_dotenv()

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

    client = getFirestoreClient()
    eloPlayerA = getElo(client, PlayerAName)
    eloPlayerB = getElo(client, PlayerBName)

    # winRateAtoBはAの予測勝率、winRateBtoAはBの予測勝率
    winRateAtoB = 1/(pow(10,(float(eloPlayerB) - float(eloPlayerA))/400) + 1)
    winRateBtoA = 1 - winRateAtoB
    gameNumber = winNumberPlayerA + winNumberPlayerB #全試合数
    # ELO更新
    newEloPlayerA = int(round(eloPlayerA + K * (winNumberPlayerA - gameNumber * winRateAtoB)))
    newEloPlayerB = int(round(eloPlayerB + K * (winNumberPlayerB - gameNumber * winRateBtoA)))

    updateElo(client, PlayerAName, newEloPlayerA)
    updateElo(client, PlayerBName, newEloPlayerB)
    
    return (newEloPlayerA,newEloPlayerB)

def getFirestoreClient():
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
      'projectId': 'quartobattlestation'
    })
    return firestore.client()

def getElo(client, name):
    AI_data = client.collection(u'AIs').document(name).get()
    if AI_data.exists:
        return AI_data.to_dict()['ELO']
    else:
        return 1200

def updateElo(client, name, newELO):
    client.collection(u'AIs').document(name).set({'ELO': newELO})

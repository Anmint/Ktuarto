# coding: UTF-8

def calcEloRating (PlayerAName, PlayerBName, winNumberPlayerA, winNumberPlayerB, firebaseClient, K=32):
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

    eloPlayerA = firebaseClient.get_elo(PlayerAName)
    eloPlayerB = firebaseClient.get_elo(PlayerBName)

    # winRateAtoBはAの予測勝率、winRateBtoAはBの予測勝率
    winRateAtoB = 1/(pow(10,(float(eloPlayerB) - float(eloPlayerA))/400) + 1)
    winRateBtoA = 1 - winRateAtoB
    gameNumber = winNumberPlayerA + winNumberPlayerB #全試合数
    # ELO更新
    newEloPlayerA = int(round(eloPlayerA + K * (winNumberPlayerA - gameNumber * winRateAtoB)))
    newEloPlayerB = int(round(eloPlayerB + K * (winNumberPlayerB - gameNumber * winRateBtoA)))

    firebaseClient.update_elo(PlayerAName, newEloPlayerA)
    firebaseClient.update_elo(PlayerBName, newEloPlayerB)
    
    return (newEloPlayerA,newEloPlayerB)

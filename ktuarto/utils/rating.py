# coding: UTF-8
def calcEloRating (eloPlayerA, eloPlayerB, winNumberPlayerA, winNumberPlayerB, K=32):
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
    # winRateAtoBはAの予測勝率、winRateBtoAはBの予測勝率
    winRateAtoB = 1/(pow(10,(float(eloPlayerB) - float(eloPlayerA))/400) + 1)
    winRateBtoA = 1 - winRateAtoB
    gameNumber = winNumberPlayerA + winNumberPlayerB #全試合数
    # ELO更新
    newEloPlayerA = int(round(eloPlayerA + K * (winNumberPlayerA - gameNumber * winRateAtoB)))
    newEloPlayerB = int(round(eloPlayerB + K * (winNumberPlayerB - gameNumber * winRateBtoA)))
    
    return (newEloPlayerA,newEloPlayerB)
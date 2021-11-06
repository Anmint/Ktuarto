# coding: UTF-8
import unittest
import rating

class TestEloRating(unittest.TestCase):
    def testcalcEloRating(self):
        # 初期値対等で1勝したばあいはK/2だけ増減
        self.assertEqual(rating.calcEloRating(1500,1500,1,0),(1516,1484))
        # Wikipediaの例
        self.assertEqual(rating.calcEloRating(1500,1700,1,0),(1524,1676))
        # 複数回勝った場合
        elo1 = 1500
        elo2 = 1500
        for i in range(10):
            elo1, elo2 = rating.calcEloRating(elo1,elo2, 0, 1)
        self.assertEqual((elo1, elo2), (1390, 1610))

if __name__ == '__main__':
    unittest.main()
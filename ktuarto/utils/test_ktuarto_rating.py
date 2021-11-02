# coding: UTF-8
import unittest
import rating

class TestEloRating(unittest.TestCase):
    def testcalcEloRating(self):
        # 初期値対等で1勝したばあいはK/2だけ増減
        self.assertEqual(rating.calcEloRating(1500,1500,1,0),(1516,1484))
        # Wikipediaの例
        self.assertEqual(rating.calcEloRating(1500,1700,1,0),(1524,1676))

if __name__ == '__main__':
    unittest.main()
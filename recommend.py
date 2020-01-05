from MatrixFactorisation.GoodBooks import GoodBooks
from surprise import SVD
from surprise import NormalPredictor
from MatrixFactorisation.Evaluator import Evaluator

import random
import numpy as np

class RecommendationSystem(object):
    """ Base class for the recommendation system. """
    def __init__(self, get_db):
        self.get_db = get_db;

class RandomRecommender(RecommendationSystem):

    def get(self):
        # FIXME: Could just select 10 from books with SQL, instead of everything.
        conn = self.get_db()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        conn.commit()

        # randomize, then return the last ten.
        random.shuffle(books)
        return books[:10]

class SVDRecommender(RecommendationSystem):

    def __init__(self, get_db):
        # Call the superclass, setting the get_db function.
        super().__init__(get_db)
        np.random.seed(0)
        random.seed(0)

    def LoadGoodBooksData(self):
        """ Load the GoodBooks Data from the CSV file. """
        # FIXME: This should load from the sqlite database.
        gb = GoodBooks()
        data = gb.loadGoodBooksLatestSmall()
        rankings = gb.getPopularityRanks()
        return (gb, data, rankings)

    def get(self):
        (gb, evaluationData, rankings) = self.LoadGoodBooksData()
        evaluator = Evaluator(evaluationData, rankings)
        evaluator.AddAlgorithm(SVD(), "SVD")
        evaluator.Evaluate(False)

        book_ids = evaluator.SampleTopNRecs(gb, testSubject = 15)

        conn = self.get_db()
        cur  = conn.cursor()
        # convert each book_id to a string, then join them with ', ' as a seperator.
        SQL_book_ids = ', '.join([str(x) for x in book_ids])
        cur.execute("SELECT * FROM books WHERE book_id IN ({})".format(
            SQL_book_ids))
        books = cur.fetchall()
        conn.commit()

        return books




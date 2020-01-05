# -*- coding: utf-8 -*-

from GoodBooks import GoodBooks
from surprise import SVD, SVDpp
from surprise import NormalPredictor
from Evaluator import Evaluator

import random
import numpy as np

def LoadGoodBooksData():
    gb = GoodBooks()
    data = gb.loadGoodBooksLatestSmall()
    rankings = gb.getPopularityRanks()
    return (gb, data, rankings)

np.random.seed(0)
random.seed(0)

# Links to the GoodBooks.py class -- loads in our dataset
(gb, evaluationData, rankings) = LoadGoodBooksData()

# Constructs an evaluator 
evaluator = Evaluator(evaluationData, rankings)

# SVD
SVD = SVD()
evaluator.AddAlgorithm(SVD, "SVD")

# Fight!
evaluator.Evaluate(False)
evaluator.SampleTopNRecs(gb, testSubject = 15)

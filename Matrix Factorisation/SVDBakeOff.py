# -*- coding: utf-8 -*-


from GoodBooks import GoodBooks
from surprise import SVD, SVDpp
from surprise import NormalPredictor
from Evaluator import Evaluator

import random
import numpy as np

def LoadGoodBooksData():
    gb = GoodBooks()
    print("Loading books ratings...")
    data = gb.loadGoodBooksLatestSmall()
    print("\nComputing book popularity ranks so we can measure novelty later...")
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

# SVD++
SVDPlusPlus = SVDpp()
evaluator.AddAlgorithm(SVDPlusPlus, "SVD++")

# Random recommendation generator for comparison purposes
Random = NormalPredictor()
evaluator.AddAlgorithm(Random, "Random")

# Fight!
evaluator.Evaluate(False)

evaluator.SampleTopNRecs(gb, testSubject = 15)

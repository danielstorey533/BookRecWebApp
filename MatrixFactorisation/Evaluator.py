from .EvaluationData import EvaluationData
from .EvaluatedAlgorithm import EvaluatedAlgorithm

class Evaluator:
    
    algorithms = []
    
    def __init__(self, dataset, rankings):
        ed = EvaluationData(dataset, rankings)
        self.dataset = ed
        
    def AddAlgorithm(self, algorithm, name):
        alg = EvaluatedAlgorithm(algorithm, name)
        self.algorithms.append(alg)
        
    def Evaluate(self, doTopN):
        results = {}
        for algorithm in self.algorithms:
            results[algorithm.GetName()] = algorithm.Evaluate(self.dataset, doTopN)

    def SampleTopNRecs(self, ml, testSubject=85, k=10):
        
        for algo in self.algorithms:
            trainSet = self.dataset.GetFullTrainSet()
            algo.GetAlgorithm().fit(trainSet)
            
            testSet = self.dataset.GetAntiTestSetForUser(testSubject)
        
            predictions = algo.GetAlgorithm().test(testSet)
            
            recommendations = []
            
            for user_id, book_id, actualRating, estimatedRating, _ in predictions:
                intBookID = int(book_id)
                recommendations.append((intBookID, estimatedRating))
            
            recommendations.sort(key=lambda x: x[1], reverse=True)
            
            r = []
            for ratings in recommendations[:10]:
                # Only return the BOOK ID.
                r.append(ratings[0])
            return 

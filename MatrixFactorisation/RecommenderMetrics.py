import itertools

from surprise import accuracy
from collections import defaultdict

class RecommenderMetrics:

    def MAE(predictions):
        return accuracy.mae(predictions, verbose=False)

    def RMSE(predictions):
        return accuracy.rmse(predictions, verbose=False)

    def GetTopN(predictions, n=10, minimumRating=4.0):
        topN = defaultdict(list)


        for user_id, book_id, actualRating, estimatedRating, _ in predictions:
            if (estimatedRating >= minimumRating):
                topN[int(user_id)].append((int(book_id), estimatedRating))

        for user_id, ratings in topN.items():
            ratings.sort(key=lambda x: x[1], reverse=True)
            topN[int(user_id)] = ratings[:n]

        return topN

    def HitRate(topNPredicted, leftOutPredictions):
        hits = 0
        total = 0

        # For each left-out rating
        for leftOut in leftOutPredictions:
            user_id = leftOut[0]
            leftOutBookID = leftOut[1]
            # Is it in the predicted top 10 for this user?
            hit = False
            for book_id, predictedRating in topNPredicted[int(user_id)]:
                if (int(leftOutBookID) == int(book_id)):
                    hit = True
                    break
            if (hit) :
                hits += 1

            total += 1

        # Compute overall precision
        return hits/total

    def CumulativeHitRate(topNPredicted, leftOutPredictions, ratingCutoff=0):
        hits = 0
        total = 0

        # For each left-out rating
        for user_id, leftOutBookID, actualRating, estimatedRating, _ in leftOutPredictions:
            # Only look at ability to recommend things the users actually liked...
            if (actualRating >= ratingCutoff):
                # Is it in the predicted top 10 for this user?
                hit = False
                for book_id, predictedRating in topNPredicted[int(user_id)]:
                    if (int(leftOutBookID) == book_id):
                        hit = True
                        break
                if (hit) :
                    hits += 1

                total += 1

        # Compute overall precision
        return hits/total

    def RatingHitRate(topNPredicted, leftOutPredictions):
        hits = defaultdict(float)
        total = defaultdict(float)

        # For each left-out rating
        for user_id, leftOutBookID, actualRating, estimatedRating, _ in leftOutPredictions:
            # Is it in the predicted top N for this user?
            hit = False
            for book_id, predictedRating in topNPredicted[int(user_id)]:
                if (int(leftOutBookID) == book_id):
                    hit = True
                    break
            if (hit) :
                hits[actualRating] += 1

            total[actualRating] += 1

        # Compute overall precision
        for rating in sorted(hits.keys()):
            print (rating, hits[rating] / total[rating])

    def AverageReciprocalHitRank(topNPredicted, leftOutPredictions):
        summation = 0
        total = 0
        # For each left-out rating
        for user_id, leftOutBookID, actualRating, estimatedRating, _ in leftOutPredictions:
            # Is it in the predicted top N for this user?
            hitRank = 0
            rank = 0
            for book_id, predictedRating in topNPredicted[int(user_id)]:
                rank = rank + 1
                if (int(leftOutBookID) == book_id):
                    hitRank = rank
                    break
            if (hitRank > 0) :
                summation += 1.0 / hitRank

            total += 1

        return summation / total

    # What percentage of users have at least one "good" recommendation
    def UserCoverage(topNPredicted, numUsers, ratingThreshold=0):
        hits = 0
        for user_id in topNPredicted.keys():
            hit = False
            for book_id, predictedRating in topNPredicted[user_id]:
                if (predictedRating >= ratingThreshold):
                    hit = True
                    break
            if (hit):
                hits += 1

        return hits / numUsers

    def Diversity(topNPredicted, simsAlgo):
        n = 0
        total = 0
        simsMatrix = simsAlgo.compute_similarities()
        for user_id in topNPredicted.keys():
            pairs = itertools.combinations(topNPredicted[user_id], 2)
            for pair in pairs:
                book1 = pair[0][0]
                book2 = pair[1][0]
                innerID1 = simsAlgo.trainset.to_inner_iid(str(book1))
                innerID2 = simsAlgo.trainset.to_inner_iid(str(book2))
                similarity = simsMatrix[innerID1][innerID2]
                total += similarity
                n += 1

        S = total / n
        return (1-S)

    def Novelty(topNPredicted, rankings):
        n = 0
        total = 0
        for user_id in topNPredicted.keys():
            for rating in topNPredicted[user_id]:
                book_id = rating[0]
                rank = rankings[book_id]
                total += rank
                n += 1
        return total / n

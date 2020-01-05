import os
import csv
import sys
import re

from surprise import Dataset
from surprise import Reader

from collections import defaultdict
import numpy as np

class GoodBooks:

    book_id_to_name = {}
    name_to_book_id = {}
    ratingsPath = 'MatrixFactorisation/dataset/ratings.csv'
    booksPath = 'MatrixFactorisation/dataset/books.csv'
    
    def loadGoodBooksLatestSmall(self):

        # Look for files relative to the directory we are running from
        # os.chdir(os.path.dirname(sys.argv[0]))

        ratingsDataset = 0
        self.book_id_to_name = {}
        self.name_to_book_id = {}

        reader = Reader(line_format='user item rating', sep=',', skip_lines=1)

        ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader=reader)

        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
                bookReader = csv.reader(csvfile)
                next(bookReader)  #Skip header line
                for row in bookReader:
                    book_id = int(row[0])
                    bookName = row[10]
                    self.book_id_to_name[book_id] = bookName
                    self.name_to_book_id[bookName] = book_id

        return ratingsDataset

    def getUserRatings(self, user):
        userRatings = []
        hitUser = False
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                user_id = int(row[0])
                if (user == user_id):
                    book_id = int(row[1])
                    rating = float(row[2])
                    userRatings.append((book_id, rating))
                    hitUser = True
                if (hitUser and (user != user_id)):
                    break

        return userRatings

    def getPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                book_id = int(row[1])
                ratings[book_id] += 1
        rank = 1
        for book_id, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[book_id] = rank
            rank += 1
        return rankings
    
    def getGenres(self):
        genres = defaultdict(list)
        genreIDs = {}
        maxGenreID = 0
        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile)
            next(bookReader)  #Skip header line
            for row in bookReader:
                book_id = int(row[0])
                genreList = row[2].split('|')
                genreIDList = []
                for genre in genreList:
                    if genre in genreIDs:
                        genreID = genreIDs[genre]
                    else:
                        genreID = maxGenreID
                        genreIDs[genre] = genreID
                        maxGenreID += 1
                    genreIDList.append(genreID)
                genres[book_id] = genreIDList
        # Convert integer-encoded genre lists to bitfields that we can treat as vectors
        for (book_id, genreIDList) in genres.items():
            bitfield = [0] * maxGenreID
            for genreID in genreIDList:
                bitfield[genreID] = 1
            genres[book_id] = bitfield            
        
        return genres
    
    def getYears(self):
        p = re.compile(r"(?:\((\d{4})\))?\s*$")
        years = defaultdict(int)
        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile)
            next(bookReader)
            for row in bookReader:
                book_id = int(row[0])
                title = row[1]
                m = p.search(title)
                year = m.group(1)
                if year:
                    years[book_id] = int(year)
        return years
    
    
    
    def getBookName(self, book_id):
        if book_id in self.book_id_to_name:
            return self.book_id_to_name[book_id]
        else:
            return ""
        
    def getbook_id(self, bookName):
        if bookName in self.name_to_book_id:
            return self.name_to_book_id[bookName]
        else:
            return 0

import sys
import re

class Table(object):

	def __init__(self):
		self.teams = {}

	def __str__(self):
		return str(self.teams)

	def addTeam(self, team):
		self.teams[team.name] = team

	def getTeam(self, teamname):
		return self.teams[teamname]

	""" Returns all the teams on the table in decending table position
	"""
	def getTeams(self):
		return sorted(self.teams.values(), key=lambda team: team.getCurrentPoints(), reverse=True)



class Game(object):

	def __init__(self, attributes):
		self.attributes = {}
		self.ordered_keys = attributes
		for attr in attributes:
			self.attributes[attr] = None

	def setAttr(self, attr, value):
		self.attributes[attr] = value

	def getAttr(self, attr):
		return self.attributes[attr]

	def toCSVRow(self):
		row = ""
		for key in self.ordered_keys:
			row += str(self.attributes[key]) + ","
		# remove last comma
		if len(row) > 0:
			row = row[:-1] + "\n"
		return row

	def getOppositeResult(self, result):
		if result == "win":
			return "loss"
		elif result == "loss":
			return "win"
		else: # draw
			return result

        def setNaiveBet(self, prediction, chance, thresh):
                # bets depeding on what has highest chance to win
                chanceType = self.attributes[prediction]
                if chanceType == "H" and chance >= thresh:
                        return "Make bet on home team!"
                elif chanceType == "A" and chance >= thresh:
                        return "Make bet on away team!"
                elif chanceType == "D" and chance >= thresh:
                        return "Make bet on a draw!"
                else: # if under threshold dont bet
                        return "Don't make bet!"

                        
        def setBet(self, prediction, chance, thresh, winH, winA, winD):
                # bets depending on weighted value between chance to win and betting ratio
                chanceType = self.attributes[prediction]
                if chanceType == "H":
                        weight = (1 - (1 / float(self.attributes[winH])) + float(self.attributes[chance])) / 2
                elif chanceType == "A":
                        weight = (1 - (1 / float(self.attributes[winA])) + float(self.attributes[chance])) / 2
                else:
                        weight = (1 - (1 / float(self.attributes[winD])) + float(self.attributes[chance])) / 2
                
                if weight >= thresh and chanceType == "H":
                        return "Make bet on home team!"
                elif weight >= thresh and chanceType == "A":
                        return "Make bet on away team!"
                elif weight >= thresh and chanceType == "D":
                        return "Make bet on a draw!"
                else: # if under threshold dont bet
                        return "Don't make bet!"

	def __str__(self):
		strGame = ""
		for key in self.ordered_keys:
			strGame += key + ":" + str(self.attributes[key]) + ", "
		# remove last comma
		if len(strGame) > 0:
			strGame = strGame[:-2]
		return strGame

class Team(object):

	def __init__(self, name):
		self.results = []
		self.name = name
		self.shots = [] # total shots
		self.targetShots = [] # shots on target

	

class Constants(object):

	# csv headings
	inst = "inst"
	actual = "actual"
	predicted = "predicted"
	probability = "probability"
	oddsH = "oddsH"
	oddsD = "oddsD"
	oddsA = "oddsA"

	perGame = "PG"

	# classes
	homeWin = "H"
	draw = "D"
	awayWin = "A"

	# the features of the dataset
	features = [inst, actual, predicted, probability, oddsH, oddsD, oddsA]

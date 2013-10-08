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

	def getTeamPosition(self, team):
		position = 0
		# variable used to determine position when teams have same points
		lastTotal = -1
		for t in self.getTeams():
			teamTotal = t.getCurrentPoints()
			if lastTotal != teamTotal:
				position += 1
			if t.name == team: return position
			# updated the lastTotal and position
			lastTotal = teamTotal


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

        def setNaiveBet(self, chanceH, chanceA, chanceD, bet, thresh):
                # bets depeding on what has highest chance to win
                home = self.attributes[chanceH]
                away = self.attributes[chanceA]
                draw = self.attributes[chanceD]
                if home >= thresh and home > away and home > draw:
                        self.attributes[bet] = "Make bet on home team!"
                elif away >= thresh and away > home and away > draw:
                        self.attributes[bet] = "Make bet on away team!"
                elif draw >= thresh and draw > home and draw > away:
                        self.attributes[bet] = "Make bet on a draw!"
                else: # if under threshold dont bet
                        self.attributes[bet] = "Don't make bet!"

        def setBet(self, chanceH, chanceA, chanceD, bet, thresh, winH, winA, winD):
                # bets depending on weighted value between chance to win and betting ratio
                weightH = (1 - (1 / self.attributes[winH]) + self.attributes[chanceH]) / 2
                weightA = (1 - (1 / self.attributes[winA]) + self.attributes[chanceA]) / 2
                weightD = (1 - (1 / self.attributes[winD]) + self.attributes[chanceD]) / 2
                if weightH >= thresh and weightH > weightA and weightH > weightD:
                        self.attributes[bet] = "Make bet on home team!"
                elif weightA >= thresh and weightA > weightH and weightA > weightD:
                        self.attributes[bet] = "Make bet on away team!"
                elif weightD >= thresh and weightD > weightH and weightD > weightA:
                        self.attributes[bet] = "Make bet on a draw!"
                else: # if under threshold dont bet
                        self.attributes[bet] = "Don't make bet!"

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

	def addPoints(self, points):
		self.results.append(points)

	def addShots(self, total, onTarget):
		self.shots.append(total)
		self.targetShots.append(onTarget)

	""" returns shots per game for the team
	"""
	def getShotsPerGame(self):
		if len(self.shots) == 0:
			return 0.0
		total = 0.0
		for s in self.shots: total += s
		return total/len(self.shots)

	""" returns shots on target per game for the team
	"""
	def getShotsOnTargetPerGame(self):
		if len(self.targetShots) == 0:
			return 0.0
		total = 0.0
		for s in self.targetShots: total += s
		return total/len(self.targetShots)


	""" returns the teams total points
	"""
	def getCurrentPoints(self):
		tally = 0
		for r in self.results: tally += r
		return tally

	""" returns the teams current form
	"""
	def getCurrentForm(self, gameRange):
		rounds = len(self.results)
		# return average if no games played yet
		if rounds == 0:
			return Constants.average_form

		# adjust the range of games considered if nessessary
		adjustedRange = gameRange
		if rounds < gameRange:
			adjustedRange = rounds

		# calculate form points total
		formPoints = 0
		for i in range(-adjustedRange, 0):
			if self.results[i] == 3: # win
				formPoints += 2
			elif self.results[i] == 1: # draw
				formPoints += 1


		# determine form
		formBand = (adjustedRange + 1) * 2 / 3;
		if formPoints >= formBand * 2:
			return Constants.good_form
		elif formPoints >= formBand:
			return Constants.average_form
		else:
			return Constants.poor_form

class Constants(object):
	# form
	good_form = "good"
	average_form = "average"
	poor_form = "poor"

	# csv headings
	date = "Date"
	hometeam = "HomeTeam"
	awayteam = "AwayTeam"
	homeForm = "FormH"
	awayForm = "FormA"
	homePosition = "PositionH"
	awayPosition = "PositionA"
	result = "FTR"
	homeShots = "HS"
	awayShots = "AS"
	homeTargetShots = "HST"
	awayTargetShots = "AST"
	oddsH = "B365H"
	oddsD = "B365D"
	oddsA = "B365A"

	perGame = "PG"

	# classes
	homeWin = "H"
	draw = "D"
	awayWin = "A"

	# the features of the dataset
	features = [date, hometeam, awayteam,
	homeForm, awayForm, homePosition, awayPosition,
	homeShots + perGame, awayShots + perGame,
	homeTargetShots + perGame, awayTargetShots + perGame,
	oddsH, oddsD, oddsA,
	result]

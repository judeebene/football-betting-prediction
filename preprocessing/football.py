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
		# return average if no games played yet
		if len(self.results) == 0: 
			return Constants.average_form

		# adjust the range of games considered if nessessary
		adjustedRange = gameRange
		if len(self.results) < gameRange:
			adjustedRange = len(self.results)

		# calculate form points total
		formPoints = 0
		for i in range(-adjustedRange, -1):
			if self.results[i] == 3: # win
				formPoints += 2
			elif self.results[i] == 1: # draw
				formPoints += 1

		# determine form
		if formPoints <=  adjustedRange / 3:
			return Constants.poor_form
		elif formPoints <= adjustedRange / 3 * 2:
			return Constants.average_form
		else:
			return Constants.good_form

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

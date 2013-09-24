import sys
import re

class Ladder(object):
	
	def __init__(self):
		self.teams = {}

	def __str__(self):
		return str(self.teams)

	def addTeam(self, team):
		self.teams[team] = Team(team)

	def getTeamPosition(self, team):
		position = 0
		teamPoints = 0
		if len(self.teams[team].results) > 0 :
			teamPoints = self.teams[team].results[-1]
		for key, oppTeam in self.teams.iteritems() :
			if key == team: continue
			if oppTeam.results[-1] > teamPoints :
				position += 1
		return position

	def getTeamForm(self, team, gameRange):
		return self.teams[team].getCurrentForm(gameRange)

	def setResults(self, teamPointPairs):
		for team, points in teamPointPairs:
			if team not in self.teams:
				self.addTeam(team)
			self.teams[team].addPoints(points)

class Game(object):

	def __init__(self, features):
		self.attributes = {}
		for attr in attributes:
			self.attributes.append([attr, None])

	def setAttr(self, attr, value):
		for i, a in enumerate(attributes):
			if a == attr:
				self.attributes[i][1] = value

	def getAttr(self, attr):
		for i, a in enumerate(attributes):
			if a == attr:
				return self.attributes[i][1]

	def toCSVRow(self):
		row = ""
		for attr in self.attributes:
			row += str(attr[1])
			if attr != self.attributes[-1] : row += ","
		row += "\n"
		return row

	def getOppositeResult(self, result):
		if result == "win":
			return "loss"
		elif result == "loss":
			return "win"
		else: # draw
			return result

	def __str__(self):
		return str(self.attributes)

class Team(object):

	def __init__(self, name):
		self.results = []
		self.name = name

	def addPoints(self, points):		
		self.results.append(points)


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
	poor_form = "form"

	# classes
	home_win = "H"
	draw = "D"
	away_win = "A"

	def __init__(self):
		# the features of the dataset
		self.features = []
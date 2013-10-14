import re
import sys
import csv
import football
from football import Constants

# global settings
formRange = 3

class FeatureGen(object):

	def __init__(self, path):
		self.path = path
		self.games = []
		self.features = Constants.features
		self.columns = []
		self.table = football.Table()
		# set up everything
		self.setup()


	def setup(self):
		teamnames = []
		homeIndex = 0
		# set up features and table
		with open(self.path, 'rb') as statCsv:
			reader = csv.reader(statCsv)
			for row in reader:
				# if we are on the first line these are the features
				if reader.line_num == 1:
					self.columns = row
					homeIndex = self.columns.index(Constants.hometeam)
				else:
					teamnames.append(row[homeIndex])

		# ensure no duplicates in teamname list
		teamnames = set(teamnames)
		for teamname in teamnames:
			team = football.Team(teamname)
			self.table.addTeam(team)

	def printFeatures(self):
		fLine = ""
		for feature in self.features : fLine += feature + ","
		sys.stdout.write(fLine[:-1] + "\n")

	def generate(self):
		# open the csv
		with open(self.path, 'rb') as statCsv:
			reader = csv.reader(statCsv)
			# print feature row
			self.printFeatures()
			for row in reader:
				# skip the heading row
				if (reader.line_num == 1) : continue
				# create a new game and a game to hold data from csv row
				game = football.Game(self.features)
				rowGame = football.Game(self.columns)
				# populate the row variable with inital values from the row
				for i in range(0, len(self.columns)) : rowGame.setAttr(self.columns[i], row[i])
				# set up the teams and teamnames
				homeTeam = rowGame.getAttr(Constants.hometeam)
				awayTeam = rowGame.getAttr(Constants.awayteam)
				home = self.table.getTeam(homeTeam)
				away = self.table.getTeam(awayTeam)
				# set the date field
				self.setDate(game, rowGame)
				# set the game teams
				self.setTeamnames(game, home, away)
				# set the form fields
				self.setForm(game, home, away)
				# set the table position fields
				self.setTablePosition(game, home, away)
				# set the shots and shots on target per game
				self.setShots(game, rowGame, home, away)
				# set the game odds
				self.setOdds(game, rowGame)
				# set the goal difference
				self.setGoalDifference(game, rowGame, home, away)
				# add the game to the list
				self.games.append(game)
				# update teams based on result
				self.setResult(game, rowGame, home, away)
				# print the game
				sys.stdout.write(game.toCSVRow())

	def setDate(self, game, rowGame):
		game.setAttr(Constants.date, rowGame.getAttr(Constants.date))

	def setTeamnames(self, game, home, away):
		game.setAttr(Constants.hometeam, home.name)
		game.setAttr(Constants.awayteam, away.name)

	def setForm(self, game, home, away):
		hForm = home.getCurrentForm(formRange)
		aForm = away.getCurrentForm(formRange)
		game.setAttr(Constants.homeForm, hForm)
		game.setAttr(Constants.awayForm, aForm)

	def setTablePosition(self, game, home, away):
		hPos = self.table.getTeamPosition(home.name)
		aPos = self.table.getTeamPosition(away.name)
		game.setAttr(Constants.homePosition, hPos)
		game.setAttr(Constants.awayPosition, aPos)

	def setOdds(self, game, rowGame):
		game.setAttr(Constants.oddsH, rowGame.getAttr(Constants.oddsH))	
		game.setAttr(Constants.oddsD, rowGame.getAttr(Constants.oddsD))	
		game.setAttr(Constants.oddsA, rowGame.getAttr(Constants.oddsA))	

	def setShots(self, game, rowGame, home, away):
		# add the current shot per game stats to the game object
		hShots = home.getShotsPerGame()
		aShots = away.getShotsPerGame()
		hTShots = home.getShotsOnTargetPerGame()
		aTShots = away.getShotsOnTargetPerGame()
		game.setAttr(Constants.homeShots + Constants.perGame, round(hShots, 2))
		game.setAttr(Constants.awayShots + Constants.perGame, round(aShots, 2))
		game.setAttr(Constants.homeTargetShots + Constants.perGame, round(hTShots, 2))
		game.setAttr(Constants.awayTargetShots + Constants.perGame, round(aTShots, 2))
		# update shots based on game stats
		# print type(rowGame.getAttr(Constants.awayTargetShots))
		home.addShots(float(rowGame.getAttr(Constants.homeShots)), 
			float(rowGame.getAttr(Constants.homeTargetShots)))
		away.addShots(float(rowGame.getAttr(Constants.awayShots)), 
			float(rowGame.getAttr(Constants.awayTargetShots)))

	def setGoalDifference(self, game, rowGame, home, away):
		hDiff = home.getGoalDiff()
		aDiff = away.getGoalDiff()
		game.setAttr(Constants.homeGoalDiff, hDiff)
		game.setAttr(Constants.awayGoalDiff, aDiff)
		# update the goal difference
		hGoals = int(rowGame.getAttr(Constants.homeGoals))
		aGoals = int(rowGame.getAttr(Constants.awayGoals))
		home.addGoals(hGoals, aGoals)
		away.addGoals(aGoals, hGoals)

	def setResult(self, game, rowGame, home, away):
		# get the result
		result = rowGame.getAttr(Constants.result)
		# set the result
		game.setAttr(Constants.result, result)
		# update team points
		if result == Constants.homeWin:
			home.addPoints(3)
			away.addPoints(0)
		elif result == Constants.awayWin:
			home.addPoints(0)
			away.addPoints(3)
		else: # draw
			home.addPoints(1)
			away.addPoints(1)


def main():
	if sys.argv == None or len(sys.argv) != 2:		
		sys.stderr.write("Invalid number of arguments\n")
		sys.exit(2)

	# get the csv path
	path = sys.argv[1]
	f = FeatureGen(path)
	# run the feature generator
	f.generate()

	sys.exit(0)

if __name__ == '__main__':
    main()
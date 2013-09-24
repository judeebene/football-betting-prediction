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
		self.features = []
		self.table = football.Table()
		# set up everything
		self.setup()


	def setup(self):
		teamnames = []
		homeIndex = 0
		# set up features and table
		with open(self.path, 'r') as statCsv:
			reader = csv.reader(statCsv)
			for row in reader:
				# if we are on the first line these are the features
				if reader.line_num == 1:
					self.features = row
					homeIndex = self.features.index(Constants.hometeam)
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
		with open(self.path, 'r') as statCsv:
			reader = csv.reader(statCsv)
			# print feature row
			self.printFeatures()
			for row in reader:
				if (reader.line_num == 1) : continue
				# create a new game
				game = football.Game(self.features)
				# set inital values
				for i in range(0, len(self.features)-1) : game.setAttr(self.features[i], row[i])
				# get the home and away teamnames
				home = game.getAttr(Constants.hometeam)
				away = game.getAttr(Constants.awayteam)
				# set the form fields
				hForm = self.table.getTeam(home).getCurrentForm(formRange)
				aForm = self.table.getTeam(away).getCurrentForm(formRange)
				game.setAttr(Constants.homeForm, hForm)
				game.setAttr(Constants.awayForm, aForm)
				# set the table position fields
				hPos = self.table.getTeamPosition(home)
				aPos = self.table.getTeamPosition(away)
				game.setAttr(Constants.homePosition, hPos)
				game.setAttr(Constants.awayPosition, aPos)
				# add the game to the list
				self.games.append(game)
				# update teams based on result
				result = game.getAttr(Constants.result)
				if result == Constants.homeWin:
					self.table.getTeam(home).addPoints(3)
					self.table.getTeam(away).addPoints(0)
				elif result == Constants.awayWin:
					self.table.getTeam(home).addPoints(0)
					self.table.getTeam(away).addPoints(3)
				else: # draw
					self.table.getTeam(home).addPoints(1)
					self.table.getTeam(away).addPoints(1)
				# print the game
				sys.stdout.write(game.toCSVRow())





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
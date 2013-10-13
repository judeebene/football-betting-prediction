import re
import sys
import csv
import betting
from betting import Constants

# global settings
formRange = 3

class FeatureGen(object):

        def __init__(self, path):
                self.path = path
                self.games = []
                self.features = Constants.features
                self.columns = []
                self.table = betting.Table()
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
                                        homeIndex = self.columns.index(Constants.inst)
                                else:
                                        teamnames.append(row[homeIndex])

                # ensure no duplicates in teamname list
                teamnames = set(teamnames)
                for teamname in teamnames:
                        team = betting.Team(teamname)
                        self.table.addTeam(team)

        def printFeatures(self):
                fLine = ""
		sys.stdout.write("bet,")
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
                                game = betting.Game(self.features)
                                rowGame = betting.Game(self.columns)
                                # populate the row variable with inital values from the row
                                for i in range(0, len(self.columns)) : rowGame.setAttr(self.columns[i], row[i])
                                # set the fields
                                buildStr = self.setCols(game, rowGame)
                                # add the game to the list
                                self.games.append(game)
                                # print the game
                                sys.stdout.write(buildStr + "," + game.toCSVRow())

        def setCols(self, game, rowGame):
                game.setAttr(Constants.inst, rowGame.getAttr(Constants.inst))
                game.setAttr(Constants.actual, rowGame.getAttr(Constants.actual))
                game.setAttr(Constants.predicted, rowGame.getAttr(Constants.predicted))
                game.setAttr(Constants.probability, rowGame.getAttr(Constants.probability))
                game.setAttr(Constants.oddsH, rowGame.getAttr(Constants.oddsH))
                game.setAttr(Constants.oddsD, rowGame.getAttr(Constants.oddsD))
                game.setAttr(Constants.oddsA, rowGame.getAttr(Constants.oddsA))
		return game.setBet(Constants.predicted, Constants.probability, 0.4, Constants.oddsH, Constants.oddsA, Constants.oddsD)
                #game.setAttr(Constants.result, rowGame.getAttr(Constants.result))


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

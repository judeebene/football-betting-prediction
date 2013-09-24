import sys
import os
import unittest
import football

# test names are in the following format: test_<class>_<method>_<expected>

class FootballTestSuite(unittest.TestCase):

	# Team unit tests

    def test_team_constructor_shouldCreateTeam(self):
    	# set up
    	teamname = "Arsenal"
    	# exercise
    	team = football.Team(teamname)
    	# verify
        assert team.name is teamname
        assert len(team.results) is 0

    def test_team_addPoints_shouldAdd3Points(self):
    	# set up
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	# exercise
    	team.addPoints(3)
    	# verify
        assert len(team.results) is 1
        assert team.results[0] is 3

    def test_team_getCurrentForm_shouldGetGoodForm(self):
    	# set up
    	goodform = football.Constants.good_form
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	# simulate three wins
    	team.addPoints(3)
    	team.addPoints(3)
    	team.addPoints(3)
    	# exercise
    	form = team.getCurrentForm(3)
    	# verify
    	assert form is goodform

    def test_team_getCurrentForm_shouldGetAverageForm(self):
    	# set up
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	# simulate two wins and one loss
    	team.addPoints(0)
    	team.addPoints(3)
    	team.addPoints(3)
    	# exercise
    	form = team.getCurrentForm(3)
    	# verify
    	assert form is football.Constants.average_form

    def test_team_getCurrentForm_shouldGetPoorForm(self):
    	# set up
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	# simulate two losses and one draw
    	team.addPoints(0)
    	team.addPoints(0)
    	team.addPoints(1)
    	# exercise
    	form = team.getCurrentForm(3)
    	# verify
    	assert form is football.Constants.poor_form

	# Game unit tests

    def test_game_constructor_shouldCreateGame(self):
    	# set up
    	attrs = ["home team", "away team", "result"]
    	# exerise
    	g = football.Game(attrs)
    	# verify
    	assert len(g.attributes) is 3

    def test_game_setgetAttr_shouldSetAndGetAttributes(self):
    	# set up
    	teamname = "Arsenal"
    	attrs = ["home team", "away team", "result"]
    	g = football.Game(attrs)
    	# exerise
    	g.setAttr("home team", teamname)
    	team = g.getAttr("home team")
    	# verify
    	assert team is teamname

    def test_game_toCSVRow_shouldReturnValidCsvRow(self):
    	# set up
    	home = "Arsenal"
    	away = "Man U"
    	result = "H"
    	attrs = ["home team", "away team", "result"]
    	expected = "{0},{1},{2}\n".format(home, away, result)
    	g = football.Game(attrs)
    	# set the attributes
    	g.setAttr("home team", home)
    	g.setAttr("away team", away)
    	g.setAttr("result", result)
    	# excercise
    	row  = g.toCSVRow()
    	# verify
    	assert row == expected




def main():
    unittest.main()

if __name__ == '__main__':
    main()
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

    def test_team_getCurrentPoints_shouldGetPoints(self):
    	# set up
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	# exercise
    	team.addPoints(3)
    	team.addPoints(1)
    	# verify
        assert team.getCurrentPoints() is 4


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

    # Table unit tests

    def test_table_constructor_shouldCreateTable(self):
    	# exercise
    	t = football.Table()
    	# verify
    	assert len(t.teams) is 0

    def test_table_addTeam_shouldAddTeam(self):
    	# setup
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	t = football.Table()
    	# exercise
    	t.addTeam(team)
    	# verify
    	assert len(t.teams) is 1
    	assert t.teams[teamname] is not None

    def test_table_getTeam_shouldGetTeam(self):
    	# setup
    	teamname = "Arsenal"
    	t = football.Table()
    	t.addTeam(football.Team(teamname))
    	# exercise
    	team = t.getTeam(teamname)
    	# verify
    	assert team is not None
    	assert team.name is teamname

    def test_table_getTeams_shouldGetTeamsInOrder(self):
    	# setup teams
    	arsenal = football.Team("Arsenal")
    	arsenal.addPoints(3)
    	manu = football.Team("Manchester United")
    	manu.addPoints(1)
    	# setup table
    	t = football.Table()
    	t.addTeam(arsenal)
    	t.addTeam(manu)
    	# exercise
    	teams = t.getTeams()
    	# verify
    	assert len(teams) is 2
    	assert teams[0].name == arsenal.name
    	assert teams[1].name == manu.name

    def test_table_getTeamPosition_shouldReturn2ndPosition(self):
    	# setup teams
    	arsenal = football.Team("Arsenal")
    	arsenal.addPoints(3)
    	manu = football.Team("Manchester United")
    	manu.addPoints(1)
    	stoke = football.Team("Stoke")
    	stoke.addPoints(0)
    	# setup table
    	t = football.Table()
    	t.addTeam(arsenal)
    	t.addTeam(manu)
    	t.addTeam(stoke)
    	# exercise
    	pos = t.getTeamPosition(manu.name)
    	# verify
    	assert pos is 2

    def test_table_getTeamPosition_shouldReturnTied1stPosition(self):
    	# setup teams
    	arsenal = football.Team("Arsenal")
    	arsenal.addPoints(3)
    	manu = football.Team("Manchester United")
    	manu.addPoints(3)
    	stoke = football.Team("Stoke")
    	stoke.addPoints(0)
    	# setup table
    	t = football.Table()
    	t.addTeam(arsenal)
    	t.addTeam(manu)
    	t.addTeam(stoke)
    	# exercise
    	m = t.getTeamPosition(manu.name)
    	a = t.getTeamPosition(arsenal.name)
    	s = t.getTeamPosition(stoke.name)
    	# verify
    	assert m is 1 and a is 1 and s is 2




def main():
    unittest.main()

if __name__ == '__main__':
    main()
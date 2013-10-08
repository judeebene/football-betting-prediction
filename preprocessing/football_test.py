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
        self.assertEqual(team.name, teamname)
        self.assertEqual(len(team.results), 0)

    def test_team_addPoints_shouldAdd3Points(self):
    	# set up
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	# exercise
    	team.addPoints(3)
    	# verify
        self.assertEqual(len(team.results), 1)
        self.assertEqual(team.results[0], 3)

    def test_team_getCurrentPoints_shouldGetPoints(self):
    	# set up
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	# exercise
    	team.addPoints(3)
    	team.addPoints(1)
    	# verify
        self.assertEqual(team.getCurrentPoints(), 4)


    def test_team_getCurrentForm_shouldGetGoodForm(self):
    	# set up
    	goodform = football.Constants.good_form
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	# simulate three wins
    	team.addPoints(3)
    	# exercise
    	form = team.getCurrentForm(3)
    	# verify
    	self.assertEqual(form, goodform)

    def test_team_getCurrentForm_shouldGetAverageForm(self):
    	# set up
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	# simulate two wins and one loss
    	team.addPoints(0)
    	team.addPoints(1)
    	team.addPoints(3)
    	# exercise
    	form = team.getCurrentForm(3)
    	# verify
    	self.assertEqual(form, football.Constants.average_form)

    def test_team_getCurrentForm_shouldGetAverageFormAfterSingleGame(self):
    	# set up
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	# simulate two wins and one loss
    	team.addPoints(1)
    	# exercise
    	form = team.getCurrentForm(3)
    	# verify
    	self.assertEqual(form, football.Constants.average_form)

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
    	self.assertEqual(form, football.Constants.poor_form)

    def test_team_getShotsPerGame_shouldGetAverageShots(self):
    	# set up
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	team.addShots(6, 3)
    	team.addShots(6, 3)
    	# exercise
    	shots = team.getShotsPerGame()
    	# verify
    	self.assertEqual(shots, 6)

    def test_team_getShotsOnTargetPerGame_shouldGetAverageShots(self):
    	# set up
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	team.addShots(6, 3)
    	team.addShots(6, 2)
    	# exercise
    	shots = team.getShotsOnTargetPerGame()
    	# verify
    	self.assertEqual(shots, 2.5)

	# Game unit tests

    def test_game_constructor_shouldCreateGame(self):
    	# set up
    	attrs = ["home team", "away team", "result"]
    	# exerise
    	g = football.Game(attrs)
    	# verify
    	self.assertEqual(len(g.attributes), 3)

    def test_game_setgetAttr_shouldSetAndGetAttributes(self):
    	# set up
    	teamname = "Arsenal"
    	attrs = ["home team", "away team", "result"]
    	g = football.Game(attrs)
    	# exerise
    	g.setAttr("home team", teamname)
    	team = g.getAttr("home team")
    	# verify
    	self.assertEqual(team, teamname)

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
    	self.assertEqual(row, expected)

    # Table unit tests

    def test_table_constructor_shouldCreateTable(self):
    	# exercise
    	t = football.Table()
    	# verify
    	self.assertEqual(len(t.teams), 0)

    def test_table_addTeam_shouldAddTeam(self):
    	# setup
    	teamname = "Arsenal"
    	team = football.Team(teamname)
    	t = football.Table()
    	# exercise
    	t.addTeam(team)
    	# verify
    	self.assertEqual(len(t.teams), 1)
    	self.assertNotEqual(t.teams[teamname], None)

    def test_table_getTeam_shouldGetTeam(self):
    	# setup
    	teamname = "Arsenal"
    	t = football.Table()
    	t.addTeam(football.Team(teamname))
    	# exercise
    	team = t.getTeam(teamname)
    	# verify
    	self.assertNotEqual(team, None)
    	self.assertEqual(team.name, teamname)

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
    	self.assertEqual(len(teams), 2)
    	self.assertEqual(teams[0].name, arsenal.name)
    	self.assertEqual(teams[1].name, manu.name)

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
    	self.assertEqual(pos, 2)

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
    	self.assertEqual(m, 1)
    	self.assertEqual(a, 1)
    	self.assertEqual(s, 2)

    def test_betting_makeBet_shouldMakeNaiveBetHome(self):
    	# set up
    	home = "Arsenal"
    	away = "Man U"
    	result = "H"
        chanceH = 0.5
        chanceA = 0.4
        chanceD = 0.1
        bet = "Make bet on home team!"
        thresh = 0.4
    	attrs = ["home team", "away team", "result", "chanceH", "chanceA", "chanceD", "bet"]
    	expected = "{0},{1},{2},{3},{4},{5},{6}\n".format(home, away, result, chanceH, chanceA, chanceD, bet)
    	g = football.Game(attrs)
    	# set the attributes
    	g.setAttr("home team", home)
    	g.setAttr("away team", away)
    	g.setAttr("result", result)
    	g.setAttr("chanceH", chanceH)
    	g.setAttr("chanceA", chanceA)
    	g.setAttr("chanceD", chanceD)
    	g.setNaiveBet("chanceH", "chanceA", "chanceD", "bet", thresh)
    	# excercise
    	row  = g.toCSVRow()
    	# verify
    	self.assertEqual(row, expected)

    def test_betting_makeBet_shouldMakeNaiveBetAway(self):
    	# set up
    	home = "Arsenal"
    	away = "Man U"
    	result = "H"
        chanceH = 0.35
        chanceA = 0.4
        chanceD = 0.25
        bet = "Make bet on away team!"
        thresh = 0.4
    	attrs = ["home team", "away team", "result", "chanceH", "chanceA", "chanceD", "bet"]
    	expected = "{0},{1},{2},{3},{4},{5},{6}\n".format(home, away, result, chanceH, chanceA, chanceD, bet)
    	g = football.Game(attrs)
    	# set the attributes
    	g.setAttr("home team", home)
    	g.setAttr("away team", away)
    	g.setAttr("result", result)
    	g.setAttr("chanceH", chanceH)
    	g.setAttr("chanceA", chanceA)
    	g.setAttr("chanceD", chanceD)
    	g.setNaiveBet("chanceH", "chanceA", "chanceD", "bet", thresh)
    	# excercise
    	row  = g.toCSVRow()
    	# verify
    	self.assertEqual(row, expected)

    def test_betting_makeBet_shouldMakeNaiveBetDraw(self):
    	# set up
    	home = "Arsenal"
    	away = "Man U"
    	result = "H"
        chanceH = 0.3
        chanceA = 0.1
        chanceD = 0.6
        bet = "Make bet on a draw!"
        thresh = 0.4
    	attrs = ["home team", "away team", "result", "chanceH", "chanceA", "chanceD", "bet"]
    	expected = "{0},{1},{2},{3},{4},{5},{6}\n".format(home, away, result, chanceH, chanceA, chanceD, bet)
    	g = football.Game(attrs)
    	# set the attributes
    	g.setAttr("home team", home)
    	g.setAttr("away team", away)
    	g.setAttr("result", result)
    	g.setAttr("chanceH", chanceH)
    	g.setAttr("chanceA", chanceA)
    	g.setAttr("chanceD", chanceD)
    	g.setNaiveBet("chanceH", "chanceA", "chanceD", "bet", thresh)
    	# excercise
    	row  = g.toCSVRow()
    	# verify
    	self.assertEqual(row, expected)

    def test_betting_makeBet_shouldNotMakeNaiveBet(self):
    	# set up
    	home = "Arsenal"
    	away = "Man U"
    	result = "H"
        chanceH = 0.3
        chanceA = 0.35
        chanceD = 0.35
        bet = "Don't make bet!"
        thresh = 0.4
    	attrs = ["home team", "away team", "result", "chanceH", "chanceA", "chanceD", "bet"]
    	expected = "{0},{1},{2},{3},{4},{5},{6}\n".format(home, away, result, chanceH, chanceA, chanceD, bet)
    	g = football.Game(attrs)
    	# set the attributes
    	g.setAttr("home team", home)
    	g.setAttr("away team", away)
    	g.setAttr("result", result)
    	g.setAttr("chanceH", chanceH)
    	g.setAttr("chanceA", chanceA)
    	g.setAttr("chanceD", chanceD)
    	g.setNaiveBet("chanceH", "chanceA", "chanceD", "bet", thresh)
    	# excercise
    	row  = g.toCSVRow()
    	# verify
    	self.assertEqual(row, expected)

    def test_betting_makeBet_shouldMakeBetHome(self):
       # set up
    	home = "Arsenal"
    	away = "Man U"
    	result = "H"
        chanceH = 0.6
        chanceA = 0.2
        chanceD = 0.2
        ratioH = 2.0
        ratioA = 5.0
        ratioD = 5.0
        bet = "Make bet on home team!"
        thresh = 0.4
    	attrs = ["home team", "away team", "result", "chanceH", "chanceA", "chanceD", "home ratio", "away ratio", "draw ratio", "bet"]
    	expected = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(home, away, result, chanceH, chanceA, chanceD, ratioH, ratioA, ratioD, bet)
    	g = football.Game(attrs)
    	# set the attributes
    	g.setAttr("home team", home)
    	g.setAttr("away team", away)
    	g.setAttr("result", result)
    	g.setAttr("chanceH", chanceH)
    	g.setAttr("chanceA", chanceA)
    	g.setAttr("chanceD", chanceD)
    	g.setAttr("home ratio", ratioH)
    	g.setAttr("away ratio", ratioA)
    	g.setAttr("draw ratio", ratioD)
    	g.setBet("chanceH", "chanceA", "chanceD", "bet", thresh, "home ratio", "away ratio", "draw ratio")
    	# excercise
    	row  = g.toCSVRow()
    	# verify
    	self.assertEqual(row, expected)

    def test_betting_makeBet_shouldMakeBetAway(self):
       # set up
    	home = "Arsenal"
    	away = "Man U"
    	result = "H"
        chanceH = 0.4
        chanceA = 0.4
        chanceD = 0.2
        ratioH = 2.0
        ratioA = 2.4
        ratioD = 2.0
        bet = "Make bet on away team!"
        thresh = 0.1
    	attrs = ["home team", "away team", "result", "chanceH", "chanceA", "chanceD", "home ratio", "away ratio", "draw ratio", "bet"]
    	expected = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(home, away, result, chanceH, chanceA, chanceD, ratioH, ratioA, ratioD, bet)
    	g = football.Game(attrs)
    	# set the attributes
    	g.setAttr("home team", home)
    	g.setAttr("away team", away)
    	g.setAttr("result", result)
    	g.setAttr("chanceH", chanceH)
    	g.setAttr("chanceA", chanceA)
    	g.setAttr("chanceD", chanceD)
    	g.setAttr("home ratio", ratioH)
    	g.setAttr("away ratio", ratioA)
    	g.setAttr("draw ratio", ratioD)
    	g.setBet("chanceH", "chanceA", "chanceD", "bet", thresh, "home ratio", "away ratio", "draw ratio")
    	# excercise
    	row  = g.toCSVRow()
    	# verify
    	self.assertEqual(row, expected)

    def test_betting_makeBet_shouldMakeBetDraw(self):
       # set up
    	home = "Arsenal"
    	away = "Man U"
    	result = "H"
        chanceH = 0.25
        chanceA = 0.4
        chanceD = 0.35
        ratioH = 2.0
        ratioA = 2.4
        ratioD = 6.0
        bet = "Make bet on a draw!"
        thresh = 0.1
    	attrs = ["home team", "away team", "result", "chanceH", "chanceA", "chanceD", "home ratio", "away ratio", "draw ratio", "bet"]
    	expected = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(home, away, result, chanceH, chanceA, chanceD, ratioH, ratioA, ratioD, bet)
    	g = football.Game(attrs)
    	# set the attributes
    	g.setAttr("home team", home)
    	g.setAttr("away team", away)
    	g.setAttr("result", result)
    	g.setAttr("chanceH", chanceH)
    	g.setAttr("chanceA", chanceA)
    	g.setAttr("chanceD", chanceD)
    	g.setAttr("home ratio", ratioH)
    	g.setAttr("away ratio", ratioA)
    	g.setAttr("draw ratio", ratioD)
    	g.setBet("chanceH", "chanceA", "chanceD", "bet", thresh, "home ratio", "away ratio", "draw ratio")
    	# excercise
    	row  = g.toCSVRow()
    	# verify
    	self.assertEqual(row, expected)

    def test_betting_makeBet_shouldNotMakeBet(self):
       # set up
    	home = "Arsenal"
    	away = "Man U"
    	result = "H"
        chanceH = 0.5
        chanceA = 0.25
        chanceD = 0.35
        ratioH = 2.0
        ratioA = 4.0
        ratioD = 1.5
        bet = "Don't make bet!"
        thresh = 0.4
    	attrs = ["home team", "away team", "result", "chanceH", "chanceA", "chanceD", "home ratio", "away ratio", "draw ratio", "bet"]
    	expected = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(home, away, result, chanceH, chanceA, chanceD, ratioH, ratioA, ratioD, bet)
    	g = football.Game(attrs)
    	# set the attributes
    	g.setAttr("home team", home)
    	g.setAttr("away team", away)
    	g.setAttr("result", result)
    	g.setAttr("chanceH", chanceH)
    	g.setAttr("chanceA", chanceA)
    	g.setAttr("chanceD", chanceD)
    	g.setAttr("home ratio", ratioH)
    	g.setAttr("away ratio", ratioA)
    	g.setAttr("draw ratio", ratioD)
    	g.setBet("chanceH", "chanceA", "chanceD", "bet", thresh, "home ratio", "away ratio", "draw ratio")
    	# excercise
    	row  = g.toCSVRow()
    	# verify
    	self.assertEqual(row, expected)


def main():
    unittest.main()

if __name__ == '__main__':
    main()

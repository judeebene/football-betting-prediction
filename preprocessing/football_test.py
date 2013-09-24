import sys
import os
import unittest
import football

# test names are in the following format: test_<class>_<method>_<expected>

class FootballTestSuite(unittest.TestCase):

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
    	self.assertEqual(form, goodform)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
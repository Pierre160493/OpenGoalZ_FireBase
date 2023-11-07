import unittest
import json
from icecream import ic
from classes.stats import clsStats



########################################################################
############ Tests on class Stats
class TestStats(unittest.TestCase):

  stats = clsStats()
  stats0 = clsStats(GoalKeeping=0, Defending=0, Passing=0, PlayMaking=0, Winging=0, Scoring=0, SetPiecing=0)
  stats100 = clsStats(GoalKeeping=100, Defending=100, Passing=100, PlayMaking=100, Winging=100, Scoring=100, SetPiecing=100)

  statsPerfectGoalKeeper = clsStats(GoalKeeping=30.0, Defending=10.0, Passing=20.0, PlayMaking=10.0, Winging=10.0, Scoring=10.0, SetPiecing=20.0)
  statsPerfectDefender   = clsStats(GoalKeeping=10.0, Defending=30.0, Passing=20.0, PlayMaking=20.0, Winging=10.0, Scoring=10.0, SetPiecing=10.0)
  statsPerfectBackWinger = clsStats(GoalKeeping=10.0, Defending=30.0, Passing=20.0, PlayMaking=10.0, Winging=20.0, Scoring=10.0, SetPiecing=10.0)
  statsPerfectMidFielder = clsStats(GoalKeeping=10.0, Defending=15.0, Passing=20.0, PlayMaking=30.0, Winging=10.0, Scoring=15.0, SetPiecing=10.0)
  statsPerfectWinger     = clsStats(GoalKeeping=10.0, Defending=10.0, Passing=20.0, PlayMaking=20.0, Winging=30.0, Scoring=10.0, SetPiecing=10.0)
  statsPerfectScorer     = clsStats(GoalKeeping=10.0, Defending=10.0, Passing=20.0, PlayMaking=20.0, Winging=10.0, Scoring=30.0, SetPiecing=10.0)

########################################################################
############ Tests Methods
###### Tests on average calculation of players
  def test_AvgCalculation_Player100_Error_Seeker(self):
    with self.assertRaises(Exception) as context:
      self.stats.AvgScore(Position= "Seeker")
    self.assertTrue("[Seeker] doesn't exist in the list ['GoalKeeper', 'Defender', 'BackWinger', 'MidFielder', 'Winger', 'Scorer']" in str(context.exception))
  def test_AvgCalculation_Player100_Error_Goalkeeper(self):
    with self.assertRaises(Exception) as context:
      self.stats.AvgScore(Position= "Goalkeeper")
    self.assertTrue("[Goalkeeper] doesn't exist in the list ['GoalKeeper', 'Defender', 'BackWinger', 'MidFielder', 'Winger', 'Scorer']" in str(context.exception))

  def test_AvgCalculation_Player100_All(self):
    self.assertEqual(self.stats100.AvgScore(Position= "All"), 100)
  def test_AvgCalculation_Player100_None(self):
    self.assertEqual(self.stats100.AvgScore(), 100)
  def test_AvgCalculation_Player100_GoalKeeper(self):
    self.assertEqual(self.stats100.AvgScore(Position= "GoalKeeper"), 100)
  def test_AvgCalculation_Player100_Defender(self):
    self.assertEqual(self.stats100.AvgScore(Position= "Defender"), 100)
  def test_AvgCalculation_Player100_BackWinger(self):
    self.assertEqual(self.stats100.AvgScore(Position= "BackWinger"), 100)
  def test_AvgCalculation_Player100_MidFielder(self):
    self.assertEqual(self.stats100.AvgScore(Position= "MidFielder"), 100)
  def test_AvgCalculation_Player100_Winger(self):
    self.assertEqual(self.stats100.AvgScore(Position= "Winger"), 100)
  def test_AvgCalculation_Player100_Scorer(self):
    self.assertEqual(self.stats100.AvgScore(Position= "Scorer"), 100)

###### Tests that for each player average calculation, the sum of weights equals 1
  def test_AvgCalculation_Weight_GoalKeeper(self):
    self.assertEqual(sum(self.stats.tabCalculatePlayerAvg["GoalKeeper"].values()), 1)
  def test_AvgCalculation_Weight_Defender(self):
    self.assertEqual(sum(self.stats.tabCalculatePlayerAvg["Defender"].values()), 1)
  def test_AvgCalculation_Weight_BackWinger(self):
    self.assertEqual(sum(self.stats.tabCalculatePlayerAvg["BackWinger"].values()), 1)
  def test_AvgCalculation_Weight_MidFielder(self):
    self.assertEqual(sum(self.stats.tabCalculatePlayerAvg["MidFielder"].values()), 1)
  def test_AvgCalculation_Weight_Winger(self):
    self.assertEqual(sum(self.stats.tabCalculatePlayerAvg["Winger"].values()),1)
  def test_AvgCalculation_Weight_Scorer(self):
    self.assertEqual(sum(self.stats.tabCalculatePlayerAvg["Scorer"].values()),1)

###### Tests on best position calculation
  def test_AvgCalculation_BestPosition_GoalKeeper_Error(self):
    with self.assertRaises(Exception) as context:
      self.stats.AvgScore(Position= "GoalKeeper", returnPos= True)
    self.assertTrue("When returning best position of a player, Position must be None or [ALL], Position was: [GoalKeeper]" in str(context.exception))

  def test_AvgCalculation_BestPosition_GoalKeeper(self):
    self.assertEqual(self.statsPerfectGoalKeeper.AvgScore(Position= "All", returnPos= True), "GoalKeeper")
  def test_AvgCalculation_BestPosition_GoalKeeper2(self):
    self.assertEqual(self.statsPerfectGoalKeeper.AvgScore(returnPos= True), "GoalKeeper")

###### Tests on stats generation
  def test_GenerateStats_PerfectGoalKeeper(self):
    # ic(clsStats.generatePlayerStats(Position= "GoalKeeper", isPerfect= True).toJSON())
    self.assertEqual(clsStats.generatePlayerStats(Position= "GoalKeeper", isPerfect= True).toJSON(), self.statsPerfectGoalKeeper.toJSON())
  def test_GenerateStats_PerfectDefender(self):
    self.assertEqual(clsStats.generatePlayerStats(Position= "Defender", isPerfect= True).toJSON(), self.statsPerfectDefender.toJSON())
  def test_GenerateStats_PerfectBackWinger(self):
    self.assertEqual(clsStats.generatePlayerStats(Position= "BackWinger", isPerfect= True).toJSON(), self.statsPerfectBackWinger.toJSON())
  def test_GenerateStats_PerfectMidFielder(self):
    self.assertEqual(clsStats.generatePlayerStats(Position= "MidFielder", isPerfect= True).toJSON(), self.statsPerfectMidFielder.toJSON())
  def test_GenerateStats_PerfectWinger(self):
    self.assertEqual(clsStats.generatePlayerStats(Position= "Winger", isPerfect= True).toJSON(), self.statsPerfectWinger.toJSON())
  def test_GenerateStats_PerfectStriker(self):
    self.assertEqual(clsStats.generatePlayerStats(Position= "Scorer", isPerfect= True).toJSON(), self.statsPerfectScorer.toJSON())

###### Tests on strings
  def test_str(self):
    self.assertEqual(str(self.stats100), "GoalKeeping=100, Defending=100, Passing=100, PlayMaking=100, Winging=100, Scoring=100, SetPiecing=100")

  def test_JSON(self):
    output = {
      "Defending": 100,
      "GoalKeeping": 100,
      "Passing": 100,
      "PlayMaking": 100,
      "Scoring": 100,
      "SetPiecing": 100,
      "Winging": 100}
    self.assertEqual(self.stats100.toJSON(), json.dumps(output, default=lambda o: o.__dict__, sort_keys=True, indent=4))
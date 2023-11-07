import unittest
import json
from icecream import ic
from classes.player import clsPlayer



########################################################################
############ Tests on class Stats
class TestPlayer(unittest.TestCase):

  lisFirstLastNamesSingle = [{"FirstName": "Zinedine", "LastName": "Zidane"}]

  lisFirstLastNamesTwo = [
    {"FirstName": "Zinedine", "LastName": "Zidane"},
    {"FirstName": "Zinedine", "LastName": "Zidane"}]

  output = {"FirstName": "Zinedine", "LastName": "Zidane"}

########################################################################
############ Tests Methods
###### Tests on player name generation
  def test_generatePlayerName_Single(self):
    self.assertEqual(clsPlayer.generatePlayerName(lisFirstLastNames= self.lisFirstLastNamesSingle), self.output)
  def test_generatePlayerName_Two(self):
    self.assertEqual(clsPlayer.generatePlayerName(lisFirstLastNames= self.lisFirstLastNamesTwo), self.output)
  def test_generatePlayerName_With_Inputs(self):
    self.assertEqual(clsPlayer.generatePlayerName(lisFirstLastNames= None, FirstName= "Zinedine", LastName= "Zidane"), self.output)
  def test_generatePlayerName_With_None(self):
    with self.assertRaises(Exception) as context:
      clsPlayer.generatePlayerName(lisFirstLastNames= None)
    self.assertTrue("ERROR: When the input list containing the names is None, we need an input FirstName and LastName" in str(context.exception))
  def test_generatePlayerName_With_Empty_List(self):
    with self.assertRaises(Exception) as context:
      clsPlayer.generatePlayerName(lisFirstLastNames= [])
    self.assertTrue("ERROR: When the input list containing the names is None, we need an input FirstName and LastName" in str(context.exception))

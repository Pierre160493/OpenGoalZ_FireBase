import math
import json
import random

from datetime import datetime, timedelta
from icecream import ic

############ Need it to import correctly the following packages otherwise we get an: ModuleNotFoundError: No module named 'test' (https://github.com/firebase/firebase-functions-python/issues/92)
import sys
from pathlib import Path
sys.path.insert(0, Path(__file__).parent.as_posix())

from stats import clsStats
############

########################################################################
########################################################################
############ Class for player
class clsPlayer:
### Players
### | FirstName: String
### | LastName: String
### | DateBirth: Date
### | Country: String
### | Salary: Double
### | Club
### | | Name: String
### | | Id: Reference
### | | DateStart: Date
### | Stats: clsStats
### ------------------
########################################################################
########################################################################
###### Table of available positions
  lisPositions = ["GoalKeeper", "Defender", "BackWinger", "MidFielder", "Winger", "Scorer"]

########################################################################
########################################################################
###### Fetch all the FirstNames and LastNames in the FireStore collection of documents
  @staticmethod
  def getDataBaseFirstAndLastNames(fstDocs): #Get all the First and Last Names in the database (from FireStore Document fstDocs) 
    lisDbFirstLastNames = []
    for doc in fstDocs: #Loop through each document of the collection
      if doc.exists:
        data = doc.to_dict() #Get data in dict
        NamePlayer = {"FirstName": None, "LastName": None}
        for key in NamePlayer: #Loop through the two elements of key pair
          if key in data: #Check if the key exists in the data
            NamePlayer[key] = data[key] #If it exists, add the value to the key pair
      lisDbFirstLastNames.append(NamePlayer) #Append the player to the list
    return lisDbFirstLastNames

########################################################################
########################################################################
###### Generate new player
  @staticmethod
  def createPlayers(lisPositions, Country, fstDocs, ClubId=None, ClubName=None, Age=None, isYoung= False):
###### Initial Checks
### Position checks
    for i in range(len(lisPositions)-1): #Loop through each input positions
      if lisPositions[i] is None: #If the position is not given
        lisPositions[i] = random.choice(list(clsPlayer.lisPositions)) #Generate a random position if position input is None
      elif lisPositions[i] not in clsPlayer.lisPositions: #We check that it's a legitimate position
        raise Exception(f"ERROR: Position [{lisPositions[i]}] doesn't exists in the list of possible positions") #Error if the position is unknown
### Age checks
    if isYoung:
      age_min = 15
      age_max = 17
    else:
      age_min = 17 #Minimum age
      age_max = 35 #Maximum age
    if Age is None:
      Age = random.randint(age_min, age_max)
    elif Age < age_min or Age > age_max:
      raise Exception(f"ERROR: Age [{Age}] is not between minimum age: {age_min} and maximum age: {age_max}")
###### Calculations
### Get the collection of documents containing First and Last Names from database
    lisFirstLastNames = clsPlayer.getDataBaseFirstAndLastNames(fstDocs= fstDocs)
### Creation of the players
    lisPlayers = []
    for i in range(len(lisPositions)-1):
      NamePlayer = clsPlayer.generatePlayerName(lisFirstLastNames)
### Age and birth date calculation
      DateBirth = datetime.now() - timedelta(days= int(Age * 112)) # (1 game season = 16 real life weeks = 112 real life days)
      Experience = random.randint(0, 20) + Age #Generate random experience value and add age influence
### Stats calculation
      Stats = clsStats.generatePlayerStats(lisPositions[i]) #Generate stats
### Other stats
      Form = 70
      Stamina = 70
      Loyalty = 150
### Salary calculation
      Salary = Stats.Salary(BaseSalary= math.floor(500 + 100 * Age)) #Calculate Salary with base value, age and stats influence
###### Store data
      Player = clsPlayer(FirstName= NamePlayer["FirstName"], LastName= NamePlayer["LastName"], DateBirth= DateBirth, Experience= Experience,
        Country= Country, ClubId= ClubId, ClubName= ClubName, Stats= Stats, Form= Form, Stamina= Stamina, Loyalty= Loyalty, Salary= Salary,)
      lisPlayers.append(Player)

    return lisPlayers


########################################################################
########################################################################
###### Player name generation from the list in the database (can force values with optional parameters)
  @staticmethod
  def generatePlayerName(lisFirstLastNames= None, FirstName= None, LastName= None):
    if (lisFirstLastNames is None or lisFirstLastNames == []) and (FirstName is None or LastName is None):
      raise Exception("ERROR: When the input list containing the names is None, we need an input FirstName and LastName")
    NamePlayer = {"FirstName": FirstName, "LastName": LastName}
    RandNumber = {"FirstName": None, "LastName": None} #This will enable to generate perfect players if FirstName matches LastName
    for key in NamePlayer.keys():
      while NamePlayer[key] is None:
        RandNumber[key] = random.randint(0, len(lisFirstLastNames) - 1)
        NamePlayer[key] = lisFirstLastNames[RandNumber[key]][key] #Store the value
    return NamePlayer


########################################################################
########################################################################
###### Init method
  def __init__(self,
               FirstName = None, LastName = None, DateBirth = None, Experience = None, Country = None,
               ClubId = None, ClubName = None, ClubArrival = datetime.now,
               Stats = None, Form = None, Stamina = None, Loyalty = None, Salary = None):
    self.FirstName = FirstName
    self.LastName = LastName
    self.DateBirth = DateBirth
    self.Country = Country
    self.ClubId = ClubId
    self.ClubName = ClubName
    self.ClubArrival = ClubArrival
    self.Stats = Stats
    self.Form = Form
    self.Stamina = Stamina
    self.Loyalty = Loyalty
    self.Experience = Experience
    self.Salary = Salary
    
    
    if self.FirstName is None:
      raise Exception("ERROR: LastName is mandatory when generating player element (Class Player)")
    if self.LastName is None:
      raise Exception("ERROR: LastName is mandatory when generating player element (Class Player)")
    if self.DateBirth is None:
      pass


#  def __str__(self):
#    return f"{self.FirstName} {self.LastName} {self.DateBirth} {self.Country} {self.ClubId} {self.ClubArrival} {self.Salary} {self.Form} {self.Stamina} {self.Experience}"

  def to_dict(self):
    return {
      "FirstName": self.FirstName,
      "LastName": self.LastName,
      "DateBirth": self.DateBirth,
      "Country": self.Country,
      "ClubId": self.ClubId,
      "ClubName": self.ClubName,
      # "ClubArrival": self.ClubArrival,
      "Stats": self.Stats.to_dict(),
      "Form": self.Form,
      "Stamina": self.Stamina,
      "Loyalty": self.Loyalty,
      "Experience": self.Experience,
      "Salary": self.Salary      
    }

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

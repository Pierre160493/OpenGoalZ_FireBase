
import sys
from pathlib import Path
from firebase_admin import initialize_app

sys.path.insert(0, Path(__file__).parent.as_posix()) #Need it to import correctly the following packages otherwise we get an: ModuleNotFoundError: No module named 'test' (https://github.com/firebase/firebase-functions-python/issues/92)

# # from OpenGoalZ_Functions.foo import * # Tests default functions
# from OpenGoalZ_Functions.add_to_name_generator import add_to_name_generator # Add name in the tables used for generating random player names
# http://127.0.0.1:5001/openhattrick/us-central1/add_to_name_generator/?Country=France&FirstName=Pierre&LastName=Granger&Position=CB
from OpenGoalZ_Functions.create_club import *
# http://127.0.0.1:5001/openhattrick/us-central1/createClub/?Country=France


initialize_app()

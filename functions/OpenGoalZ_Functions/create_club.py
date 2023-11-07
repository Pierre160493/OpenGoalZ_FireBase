import random
import google.cloud.firestore

from firebase_functions import https_fn
from firebase_admin import firestore
from icecream import ic

############ Need it to import correctly the following packages otherwise we get an: ModuleNotFoundError: No module named 'test' (https://github.com/firebase/firebase-functions-python/issues/92)
import sys
from pathlib import Path
sys.path.insert(0, Path(__file__).parent.as_posix())

from classes.player import clsPlayer
############

############################################################################################################
############################################################################################################
############ Create Club
@https_fn.on_request()
def createClub(req: https_fn.Request) -> https_fn.Response:
    """Club creation
    Mandatory: Country
    Optional: NameClub

    http://127.0.0.1:5001/openhattrick/us-central1/createClub/?Country=France&NameClub=FC%20Bordeaux
    https://createclub-hqe5g73yoq-uc.a.run.app/?Country=France
    """

    firestore_client: google.cloud.firestore.Client = firestore.client()

###### Country
    Country = req.args.get("Country")
    if Country is None:
        return https_fn.Response("Oups... Country parameter is mandatory, we found nothing", status=400)
    elif Country not in ["France", "Test"]:
        return https_fn.Response(f"Oups... Country [{Country}] doesn't exist yet", status=400)
    strDocument1 = Country

###### Name
    NameClub = req.args.get("NameClub")
    if NameClub is None:
        FieldCity = "Name"
        strCollection1 = "NameGenerator"
        strCollection2 = "Cities"
        doc_ref = firestore_client.collection(strCollection1).document(strDocument1).collection(strCollection2)
        docs = doc_ref.get()
        n_docs = len([doc for doc in docs])
        # return https_fn.Response(f"Oups... n_docs [{n_docs}] doesn't exist yet", status=400)
        while NameClub is None:
            random_index = random.randint(0, n_docs - 1)
            # Query and retrieve the random document
            # rand_doc = doc_ref.limit(1).offset(random_index).get()
            rand_doc = docs[random_index]
            
            if rand_doc.exists:
                data = rand_doc.to_dict()
                if FieldCity in data: # Field exists in the document
                    NameClub = data[FieldCity]

        NameClub = random.choice(["FC", "FC", "AS", "Union", "Entente"]) + f" {NameClub}" #Club Name with random generation
    
###### Stadium
    NameStadium = req.args.get("NameStadium")
    if NameStadium is None:
        NameStadium = random.choice(["Stade de la Mairie", "Stade de l'école", "Stade de la République", "Stade de la Liberté", "Stade Régional", "Stade Départemental", "Champ de patate de Mr.Jean"])

    DateCreation = firestore.SERVER_TIMESTAMP #Creation Date and Time of the club

    # Push the new Club into Cloud Firestore using the Firebase Admin SDK.
    _, doc_ref = firestore_client.collection("Clubs").add(
        {
            "Country": Country,
            "Name": NameClub,
            "isBot": True,
            "TeamSpirit": 60,
            "TeamConfidence": 60,
            "Money": 250000,
            "Stadium": {
                "Name": NameStadium,
                "Seats": {
                    "Uncovered": 1000,
                    "Covered": 500,
                    "VIP": 50
                }
            },
            "Fans": {
                "Mood": 60,
                "Number": 100
            },
            "DateCreation": DateCreation
        }
    )
    IdClub = doc_ref.id #Id of the new created club

    #return https_fn.Response(f"Successfully created [{NameClub}] with id {doc_ref.id}.")

###### Create Players
    strCollection1 = "NameGenerator" #First Collection where we will search for some data
    strCollection2 = "Players" #Second document where we will search for some data
    doc_ref = firestore_client.collection(strCollection1).document(strDocument1).collection(strCollection2) #NameGenerator/France/Players
    docs = doc_ref.get() # Get the documents of the following path: NameGenerator/France/Players/
    #docs = firestore_client.collection(strCollection1).document(strDocument1).collection(strCollection2).get() # Get the documents of the following path: NameGenerator/France/Players/
    lisPositions= ["GoalKeeper"]*2+["Defender"]*4+["BackWinger"]*4+["MidFielder"]*4+["Winger"]*4+["Scorer"]*4
    lisPlayers = clsPlayer.createPlayers(Country= Country, lisPositions= lisPositions, fstDocs= docs) #List of all players

    for player in lisPlayers:
        # _, doc_ref = firestore_client.collection("Players").add(player)
        # _, doc_ref = firestore_client.collection("Players").add(vars(player))
        ic(player.to_dict())
        _, doc_ref = firestore_client.collection("Players").add(player.to_dict())
        # _, doc_ref = firestore_client.collection("Players").add({})

        # _, doc_ref = firestore_client.collection("Players").document(doc_ref.id).collection("History").add(
        #     {
        #         "Event": "Player generated at club creation",
        #         "Date": DateCreation,
        #         "Club": {
        #             "Id": IdClub,
        #             "Name": NameClub
        #         }
        #     }
        # )

    return https_fn.Response(f"Successfully created [{NameClub}] with id {IdClub}.")


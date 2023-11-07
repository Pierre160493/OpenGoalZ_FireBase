import google.cloud.firestore
from firebase_functions import https_fn
from firebase_admin import firestore
from icecream import ic

############################################################################################################
############################################################################################################
############ Add First Name and Last Name for generating player name
@https_fn.on_request()
def add_to_name_generator(req: https_fn.Request) -> https_fn.Response:
    """Add first names and last names in the player_name_generator collection
    Mandatory: Type of add (Players, ...); Country
    Optional: FirstName; LastName; Position
    http://localhost:5001/openhattrick/us-central1/add_to_player_name_generator/?Country=France&FirstName=Pierre&LastName=Granger&Position=CB
    """

    #FieldTypeOfAdd="TypeOfAdd"
    FieldCountry="Country"
    FieldFirstName="FirstName"
    FieldLastName="LastName"
    FieldPosition="Position"

    strDocument1 = "Players"
    #if strDocument is None:
    #    return https_fn.Response(f"Oups... {FieldTypeOfAdd} parameter is mandatory, we found nothing as input ==> Must be Players", status=400)

    strCountry = req.args.get(FieldCountry)
    if strCountry is None:
        return https_fn.Response(f"Oups... {FieldCountry} parameter is mandatory, we found nothing as input", status=400)

    FirstName = req.args.get(FieldFirstName)
    LastName = req.args.get(FieldLastName)
    if FirstName is None and LastName is None:
        return https_fn.Response(f"You must at least specify a {FieldFirstName} or a {FieldLastName} ==> Found none for both !", status=400)

    db: google.cloud.firestore.Client = firestore.client()
    strCollection1 = "NameGenerator"
    strCollection2 = strCountry
    strPath = f"[{strCollection1}/{strDocument1}/{strCollection2}]" #Path of the document we want to create

    #try:
    #    doc_ref = db.collection(strCollection1).document(strDocument1).collection(strCollection2)
    #    doc = doc_ref.get()
    #    if not doc.exists:
    #        return https_fn.Response(f"The path: {strPath} is unknown", status=400)
    #except Exception as e:
    #    print(f"An error occurred: {e}")
    #    return https_fn.Response(f"Error when opening the path: {strPath} ==> {e}", status=400)

    strAdd = None
    if FirstName is not None: # Push the new FirstName in the db
        strAdd = {
            FieldFirstName: FirstName,
        }

    if LastName is not None: # Push the new LastName in the db
        strAdd.update({FieldLastName: LastName})

        Position = req.args.get(FieldPosition)
        if Position is not None:
            strAdd .update({FieldPosition: Position})

    _, doc_ref = db.collection(strCollection1).document(strDocument1).collection(strCollection2).add(strAdd)


    # Send back a message that we've successfully written the message
    return https_fn.Response(f"Successfully added new document [{strAdd}] in the path {strPath}")

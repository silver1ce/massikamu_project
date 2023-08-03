import pymongo
import certifi
import datetime
# Connect to MongoDB

connection = pymongo.MongoClient("mongodb+srv://temp:massikamu@cluster0.qn6cv7r.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db = connection["MassiKamu"]
expense_collection = db["expenses"]

def yhdista_mongoon():
    try:
        CONNECTION_STRING="mongodb+srv://temp:massikamu@cluster0.qn6cv7r.mongodb.net/?retryWrites=true&w=majority"
        connection = pymongo.MongoClient(CONNECTION_STRING)
        print("yhteys ok")
        return connection["MassiKamu"]

    except Exception:
        print("Ei voida yhdistää Mongoon")

def tallenna_tiedot(nimi:str, summa:float, paivamaara:datetime):
    expense_collection.insert_one(
        {
            "nimi": nimi,
            "summa":summa,
            "paivamaara": paivamaara
        }
    )

#yritys tehdä poistamisominaisuus, ei toimi vielä. Täytyy tarkastaa, miten sieltä poistettiinkaan
def poista_tiedot(nimi:str, summa:float):
    expense_collection.remove(
        {
            "nimi": nimi,
            "summa":summa

        }

    )

def nayta_tiedot():
    tiedot = []
    for rivi in expense_collection.find():
        tiedot.append(
            rivi["nimi"] + 
            ": " +
            str(rivi["summa"])+ 
            ", " +
            (rivi ["paivamaara"]).strftime("%d.%m.%Y %H:%M")

        )
    
    return tiedot

db = yhdista_mongoon()

import pymongo

## Step 1
## --------------------------------------------------------------------
client = pymongo.MongoClient("mongodb+srv://amysaad98:8876873333@gradebook.gisyiki.mongodb.net/?retryWrites=true&w=majority&appName=gradebook")

database = client["<yourDatabaseName>"]
collection = database["ton"]

## Step 2 & 3
## ---------------------------------------------------------------------

bridgerton_family_data = {
    "child1": {"name": "Anthony", "year": 1784},
    "child2": {"name": "Benedict", "year": 1786},
    "child3": {"name": "Colin", "year": 1791},
    "child4": {"name": "Daphne", "year": 1792},
    "child5": {"name": "Eloise", "year": 1796},
    "child6": {"name": "Francesca", "year": 1797},
    "child7": {"name": "Gregory", "year": 1801},
    "child8": {"name": "Hyacinth", "year": 1803}
}

featherington_family_data = {
    "child1": {"name": "Marina", "year": 1794},
    "child2": {"name": "Prudence", "year": 1794},
    "child3": {"name": "Philippa", "year": 1795},
    "child4": {"name": "Penelope", "year": 1796}
}

bridgerton_collection = database["bridgertonFamily"]
featherington_collection = database["featheringtonFamily"]

def create_document(collection, family_data):
    collection.insert_many([{"name": name, "year": data["year"]} for name, data in family_data.items()])

create_document(bridgerton_collection, bridgerton_family_data)
create_document(featherington_collection, featherington_family_data)

## Step 4
## ---------------------------------------------------------------------
new_values = {"$set": {"family_name": "Bridgerton"}}
query = {"name": "Anthony"} 
bridgerton_collection.update_one(query,new_values)
new_values = {"$set": {"family_name": "Featherington"}}
query = {"name": "Penelope"} 
featherington_collection.update_one(query,new_values)

## Step 6
## ----------------------------------------------------------------------
for doc in bridgerton_collection.find():
    row = doc.items()
    for each in row:
        print(each)
print()

## Step 7
## ----------------------------------------------------------------------
x = bridgerton_collection.count_documents({"family_name":"Bridgerton"})
print(x)

## Step 8
## ----------------------------------------------------------------------
query = {"family_name": "Featherington"}
projection = {"_id":0, "child4.name": 1, "child4.year":1}
person = featherington_collection.find(query,projection)
for each in person:
    print(each)

## Step 6
## ----------------------------------------------------------------------
new_bridgerton_doc = {
    "family_name": "Bridgerton",
    "children": [
        {"name": "Anthony", "year": 1784},
        {"name": "Benedict", "year": 1786},
        {"name": "Colin", "year": 1791},
        {"name": "Daphne", "year": 1792},
        {"name": "Eloise", "year": 1796},
        {"name": "Francesca", "year": 1797},
        {"name": "Gregory", "year": 1801},
        {"name": "Hyacinth", "year": 1803}
    ]
}

## Bonus
## ----------------------------------------------------------------------
eligible_people = []

for doc in collection.find():
    for member, details in doc.items():
        if isinstance(details, dict):
            age = calculate_age(details["year"])
            if age >= 18:
                first_name = details["name"]
                last_name = doc["family_name"]
                eligible_people.append({"first_name": first_name, "last_name": last_name, "age": age})

print("Eligible people:")
for person in eligible_people:
    print("First Name:", person["first_name"])
    print("Last Name:", person["last_name"])
    print("Age:", person["age"])
    print()

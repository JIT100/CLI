import json
from settings import DATABASE

filename=DATABASE
def read_database(filename):
    database = {}
    person={}
    address={}
    try:
        with open(filename,'r',encoding='utf-8') as file:
            data = json.load(file)
        person=data['person']
        address=data['address']
    except IOError:
        print('\nFile not found, will create a new one.')
        person={}
        address={}
        database['person']=person
        database['address']=address
        with open(filename, 'w+') as file:
            json.dump(database, file, indent=4)

    except json.decoder.JSONDecodeError:
        person={}
        address={}
    database["person"]=person
    database["address"]=address
    return database

def write_database(filename,data):
    database={}
    try:
        with open(filename,'w+',encoding='utf-8') as file:
            json.dump(data, file,indent=4)
    except IOError:
        print('\nFile not found, will create a new one.')
        person={}
        address={}
        database['person']=person
        database['address']=address
        with open(filename, 'w+') as file:
            json.dump(database, file, indent=4)

    except json.decoder.JSONDecodeError:
        person={}
        address={}

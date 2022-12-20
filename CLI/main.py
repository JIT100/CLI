from models import Address,Person,id_must_be_unique_integer,ValidationError
from data import read_database,write_database
import fire
from collections import Counter
from settings import DATABASE
from pprint import pprint


filename=DATABASE
database=read_database(filename)
person_dict=database["person"]
address_dict=database["address"]


def name_uniqueness(firstname,lastname):
    fullname=firstname+lastname
    fullname=fullname.lower()
    for i in person_dict:
        person=person_dict[i]
        first_name=person["firstname"]
        last_name=person["lastname"]
        person_fullname=first_name+last_name
        person_fullname=person_fullname.lower()
        if fullname == person_fullname:
            return False
    return True

def address_uniqueness(line1,line2,country,postcode,id=None):
    fulladdress=line1+line2+country+postcode
    for i in address_dict:
        each_address=address_dict[i]
        line1=each_address["line1"]
        line2=each_address["line2"]
        country=each_address["country"]
        postcode=each_address["postcode"]
        full_each_address=line1+line2+country+postcode
        if fulladdress.lower() == full_each_address.lower():
            return False
    return True
    
def address_validator(address):
    if address:
        duplicate=[i for i,v in Counter(address).items() if v>1]
        if len(duplicate) > 0:
            return {"issue":1,"message":"\nA person can't have same address twice. Kindly Change your addresses."}
        else:
            for id in address:
                current_address=id
                if not str(current_address) in address_dict.keys():
                    return {"issue":2,"message":f"\nAddress doesn't have any object with the {current_address} id."}



class Person_updater(object):

    def person_view(self,id=None):

        """Check the details of all the persons or a specific person details from the database."""  

        if id:
            try:
                person=person_dict[str(id)]
                view_preson=Person.parse_obj(person).dict()
                print(f'\nThe details of the person with ID of {id} are as followed:')
                return view_preson
            except ValidationError as e:
                return e
            except:
                return f'\nThere is no person exist with the ID of {id} in the Database. Please Provide different ID.'
        else:
            for i in person_dict:
                try:
                    person=person_dict[i]
                    persons=Person.parse_obj(person).dict()
                except ValidationError as e:
                    return e
            print('\nThe details of all person database are as followed...\n')
            pprint(person_dict,sort_dicts=False)


    def person_add(self,firstname,lastname,dob,nickname=None,address=None):

        """Add a new person on the database, by providing all required details of the person."""  

        person=person_dict
        key=id_must_be_unique_integer("person")
        uniquename=name_uniqueness(firstname,lastname)
        all_address=[]
        check_address=isinstance(address, list)
        if not check_address:
            return f'\nAddress parameter has to be a valid list containing integer. Kindly provide list value instead of string or integer.'
        if address:
            address_unvalid=address_validator(address)
            if address_unvalid:
                if address_unvalid["issue"]==1:
                    return address_unvalid['message']
                elif address_unvalid["issue"]==2:
                    return address_unvalid['message']
            else:
                for id in address:
                    current_address=id
                    all_address.append(address_dict[str(current_address)])
        if uniquename:
            try:
                if nickname==None and address==None:
                    person[key]=Person(firstname=firstname,lastname=lastname,dob=dob).dict()
                elif nickname==None:
                    person[key]=Person(firstname=firstname,lastname=lastname,dob=dob,address=all_address).dict()
                elif address==None:
                    person[key]=Person(firstname=firstname,lastname=lastname,dob=dob,nickname=nickname).dict()
                else:
                    person[key]=Person(firstname=firstname,lastname=lastname,dob=dob,nickname=nickname,address=all_address).dict()
                data=person
                database['person']=data
                write_database(filename,database)
                print('\nA new user has been created. The details are as followed...')
                return person[key]
            except ValidationError as e:
                return e
        else:
            return f'\nSomeone with {firstname} {lastname} name already exist in database, Kindly Choose another name.'
        

    def person_edit(self,id,firstname=None,lastname=None,dob=None,nickname=None,address=None):

        """Edit the details of already existing person in the database by providing correct ID & other details."""  

        person=person_dict
        user_id=str(id)
        all_address=[]
        if user_id in person:
            user=person[user_id]
            rawdata={"address":address,"firstname":firstname,"lastname":lastname,"dob":dob,"nickname":nickname}
            updated_field=[]
            check_address=isinstance(address, list)
            if not check_address:
                return f'\nAddress parameter has to be a valid list containing integer. Kindly provide list value instead of string or integer.'
            try:
                for item in rawdata:
                    if rawdata[item]:
                        if item=='address':
                            address_unvalid=address_validator(rawdata[item])
                            if address_unvalid:
                                if address_unvalid["issue"]==1:
                                    return address_unvalid['message']
                                elif address_unvalid["issue"]==2:
                                    return address_unvalid['message']
                            else:
                                for id in rawdata[item]:
                                    all_address.append(address_dict[str(id)])
                            user[item]=all_address
                        else:
                            user[item]=rawdata[item]
                            updated_field.append(item)
                view_preson=Person.parse_obj(user).dict()
                for field in updated_field:
                    print(f'\n{field} has been updated for the user with id of {user_id}.')
                person[user_id]=user
                database['person']=person
                write_database(filename,database)
                print('\nThe updated details are as Followed:')
                return view_preson
            except ValidationError as e:
                return e
        else:
            return f"\nThe user with {id} id doesn't exist, Kindly provide correct ID."


    def person_delete(self,id):

        """Delete a person's details from Database by providing correct ID of that person."""  

        person=person_dict
        user_id=str(id)
        deleted_item=person.pop(user_id,None)
        if deleted_item:
            print(f"\nThe User with ID of {user_id} has been deleted from person Database.")
            print('\nDeleted details are as Followed:')
            view_preson=Person.parse_obj(deleted_item).dict()
            database['person']=person
            write_database(filename,database)
            return view_preson
        else:
            return f"\nThe User with ID of {user_id} doesn't exist in person Database. Kindly check the ID provided."
            

    def search(self,firstname,lastname):

        """Search through database for a specific person by their first name & last name."""  

        persons=person_dict
        fullname=firstname.capitalize()+lastname.capitalize()
        print(f"\nSearching for the person in the database with the name of {firstname} {lastname}.....")
        for i in persons:
            user=persons[i]
            first_name=user['firstname']
            last_name=user['lastname']
            user_fullname=first_name+last_name
            if fullname==user_fullname:
                user_id=user['id']
                print(f"\nSearch has been finished. Person found.")
                view_detail=self.person_view(user_id)
                return view_detail
        return f"\nThere are no person named with {firstname} {lastname} in the Database. Kindly try again with different name."



class Address_updater(object):
    def address_view(self,id=None):

        """Check all addresses or only one address by ID."""

        if id:
            try:
                address=address_dict[str(id)]
                view_address=Address.parse_obj(address).dict()
                print(f'\nThe details of the address with ID of {id} are as followed:')
                return view_address
            except ValidationError as e:
                return e
            except:
                return f'\nThere is no address exist with the ID of {id} in the Database. Please Provide different ID.'
        else:
            for i in address_dict:
                address=address_dict[i]
                try:
                    addresses=Address.parse_obj(address).dict()
                except ValidationError as e:
                    return e
            print('\nThe details of all person database are as followed...\n')
            pprint(address_dict,sort_dicts=False)
    
    def address_add(self,line1:str,line2: str=None,country: str=None,postcode:str=None):

        """Add a new address to the Database."""

        line1_type=str(type(line1))
        if line1_type == "<class 'tuple'>":
            line1=' '.join(line1)       
        line2_type=str(type(line2))
        if line2_type == "<class 'tuple'>":
            line2=' '.join(line2)
        if postcode:      
            postcode=str(postcode)
        address=address_dict
        fulladdress=line1,line2,country,postcode
        unique_address=address_uniqueness(line1,line2,country,postcode)
        try:
            if unique_address:
                key=id_must_be_unique_integer("address")
                if line1:
                    address[key]=Address(line1=line1,line2=line2,country=country,postcode=str(postcode)).dict()
                data=address
                print('\nA new address has been created. The details are as followed...')
                database['address']=data
                write_database(filename,database)
                return address[key]
            else:
                return f"\nThis address: {fulladdress} already exists in the database, Kindly enter different address."
        except ValidationError as e:
            return e

    
    def address_edit(self,id,line1=None,line2=None,country=None,postcode=None):

        """Edit a existing address by providing correct details & ID."""    

        line1_type=str(type(line1))
        if line1_type == "<class 'tuple'>":
            line1=' '.join(line1)       
        line2_type=str(type(line2))
        if line2_type == "<class 'tuple'>":
            line2=' '.join(line2)
        if postcode: 
            postcode=str(postcode)
        address=address_dict
        all_address=address_dict
        address_id=str(id)
        new_address={}
        if address_id in all_address:
            address=all_address[address_id]
            new_address=address.copy()
            rawdata={"line1":line1,"line2":line2,"country":country,"postcode":postcode}
            try:               
                for item in rawdata:
                    if rawdata[item]:
                        new_address[item]=rawdata[item]
                unique_address=address_uniqueness(**new_address)
                if unique_address:
                    view_address=Address.parse_obj(new_address).dict()
                    all_address[address_id]=new_address
                    database["address"]=all_address
                    print(f'\nAddress with the ID of {address_id} has been updated...')
                    write_database(filename,database)
                    print('\nThe updated details are as Followed.')
                    return view_address
                else:
                    return f"\nProvided Address already exists in the database, Kindly enter different address."
            except ValidationError as e:
                return e
        else:
            return f"\nThe address with {address_id} id doesn't exist, Kindly provide correct ID."

    def address_delete(self,id):

        """Delete a existing address by ID.""" 

        address=address_dict
        address_id=str(id)
        deleted_item=address.pop(address_id,None)
        if deleted_item:
            print(f"\nThe address with ID of {address_id} has been deleted from address Database.")
            print('\nDeleted details are as Followed:')
            view_address=Address.parse_obj(deleted_item).dict()
            database['address']=address
            write_database(filename,database)
            return view_address
        else:
            return f"\nThe address with ID of {address_id} doesn't exist in address Database. Kindly check the ID provided."
                    



class updater(Address_updater,Person_updater):
    pass

if __name__ == '__main__':
    fire.Fire(updater)
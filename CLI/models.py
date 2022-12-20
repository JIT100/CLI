from pydantic import BaseModel,ValidationError, validator,Field
from typing import List, Optional
from datetime import datetime,date
import pycountry_convert as pc
import re
from data import read_database
from settings import DATABASE


filename=DATABASE
database=read_database(filename)

def id_must_be_unique_integer(model):
    database=read_database(filename)
    if model=="person":
        person_data=database["person"]
        if person_data.keys():
            all_keys=[int(i) for i in person_data.keys() ]
            max_keys=max(all_keys)
            new_key=max_keys+1
            return str(new_key)
        return '1'
    elif model=="address":
        address_data=database["address"]
        if address_data.keys():
            all_keys=[int(i) for i in address_data.keys() ]
            max_keys=max(all_keys)
            new_key=max_keys+1
            return str(new_key)
        return '1'

class Address(BaseModel):
    """Schema for Address"""

    id: int =Field(default=id_must_be_unique_integer("address"))
    line1:str
    line2:Optional[str]
    country:Optional[str]
    postcode:Optional[str]

    @validator('postcode')
    def postcode_cannot_contain_special_character(cls, v):
        if v:
            if not (bool(re.match('^[a-zA-Z0-9]*$',v))==True):
                raise ValueError('Postcode must not contain special character. Only string & integers are allowed.')
        return v

    @validator('line2')
    def cannot_contain_numbers(cls, v):
        if v:
            if any(char.isdigit() for char in v):
                raise ValueError('Address Line 2 must not contain a digit.')
        return v

    @validator('country')
    def country_must_be_in_europe(cls, v):
        if v:
            try:
                country_alpha2 = pc.country_name_to_country_alpha2(v,cn_name_format="upper")
                country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
                country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
                if country_continent_name !='Europe':
                    raise ValueError('Country must be based on Europe continent')
            except Exception as e:
                raise ValueError(str(e))
        country=v.capitalize()
        return country

    @validator('line1')
    def line1_cannot_be_empty(cls, v):
        if not (len(v)>=1):
            raise ValueError('Address line 1 must not be empty.')
        return v

    @validator('id')
    def id_must_be_unique(cls, v):
        person_data=database['address']
        all_keys=person_data.keys()
        if v in all_keys:
            raise ValueError("ID with {} already exists, Kindly Use Unique Id. Or Don't pass ID manually.".format(v))
        return v

class Person(BaseModel):
    """Schema for Person"""
    
    id: int =Field(default=id_must_be_unique_integer("person"))
    firstname:str
    lastname:str
    dob:str
    nickname: Optional[str]
    address:Optional[List[Address]]

    @validator('firstname','lastname','nickname')
    def name_cannot_contain_numbers(cls, v):
        if v:
            if any(char.isdigit() for char in v):
                raise ValueError('Names must not contain a digit.')
        return v

    @validator('firstname','lastname','address')
    def name_cannot_be_empty(cls, v):
        if not (len(v)>=1):
            raise ValueError('field must not be empty.')
        return v

    @validator('firstname','lastname')
    def name_captalize(cls, v):
        name=v
        name=name.capitalize()
        return name

    @validator('id')
    def id_must_be_unique(cls, v):
        person_data=database['person']
        all_keys=person_data.keys()
        if v in all_keys:
            raise ValueError("ID with {} already exists, Kindly Use Unique Id. Or Don't pass ID manually.".format(v))
        return v

    @validator('dob')
    def date_format(cls, v):
        format = "%d.%m.%Y"
        try:
            format = datetime.strptime(v, format)
        except:
            raise ValueError ("Kindly use correct date & correct date format. E.G: '25.01.2000'")
        return v

    @validator('address')
    def covert_address_string(cls, v):
        address=v
        str_address=[]
        for i in address:
            str_address.append(str(i))
        return v
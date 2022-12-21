# README #
This README document will provide you all the details about how to setup this Python FIRE CLI based basic application & it's command usage.

This application uses json base human readable file as a database to store it's data. You can customize the name of the database through the **settings.py** or use the default name which is **database.json**.
# INTRODUCTION #

Purpose of this application is to create 2 table containing person & address details & have *CRUD* functionality on top of them.  

Followings are the basic constraints of the 2 tables.
### Person Table: ###

|field|Constraints|
|----|-----|
|ID|Unique, can be text or numeric|
|First Name|Required, cannot contain numbers|
|Last Name|Required, cannot contain numbers|
|Date of Birth|Required|
|Nickname|Cannot contain numbers|

### Address Table: ###

|field|Constraints|
|----|-----|
|ID|Unique, can be text or numeric|
|Line 1|Required|
|Line 2|cannot contain numbers|
|Country|Must be a valid country in Europe|
|Postcode|No special symbols/characters|

#### Other Constraints ####

* The user should not be able to add a Person with the same First and Last Name as an existing Person.
* The user should not be able to add a duplicate Address (with all the same fields) to an existing Person.
* Two different People may have the same Address.
* All data should be persisted (saved) to a file in a human readable format,eg json, XML or YAML etc.


# How To Setup #

* Clone the Repo on a specified folder.
* install Python 3.8
* install git
* install pip3
* install virtualenv
* install virtualenvwrapper
* Create virtual enviroment using virtualenvwrapper ( Follow this documentation to know how to create one: https://virtualenvwrapper.readthedocs.io/en/latest/ ) & activate the Virtual enviroment.
* make virtual enviroment using virtualenvwrapper or By using Python's vnv module.
* Install all the dependencies mentioned in the requirements.txt in that virtual enviroment by running `pip install -r requirements.txt` on the terminal.
* switch to the *main.py* file directory under CLI folder using `cd` command & run `pyinstaller --console --onefile main.py` on the terminal. It'll create a .exe file of the main.py. E.G: **main.exe**
* open a windows command prompt aka cmd & change path to the newly created *dist* folder containing **main.exe**.
* After switching to the correct directory, run `main.exe` in the cmd terminal to check all the commands available. 

# COMMAND USAGE #

We can either use the fullname of the argument like `-firstname` or we can use the shorter version of the arugument which is `-f` , Generally the first character of the argument. Incase there are 2 argument with same first letter use the fullname of the argument.

For more information about a command use **--help** flag after a command. Example: `main.exe person_add --help` . It'll show you all required datatype, required field & optional field for that command.

### Person Add ###

Add a new person on the database, by providing all required details of the person.

* Command: **person_add**
* Syntax: *`main.exe person_add -firstname  -lastname -dob -nickname:optional -address:optional`*
* Example: `main.exe person_add -firstname="Alex" -lastname="Sanchez" -dob="26.07.2005" -address=[1]`

    Ps: *Pass Integer value as address ID inside the list syntax of python for the address field. Inorder to pass a address, You need to create a address first using address_add command , otherwise don't pass address arugement for that person.*

### Person View ###

Check the details of all the persons or a specific person details from the database.

* Command: **person_view**
* Syntax: *`main.exe person_view -id:optional`*
To Check all person details on the database, use below example.
* Example: `main.exe person_view`
To Check a particular person details, Kindly pass the person ID as argument.
* Example: `main.exe person_view -i=1` or `main.exe person_view 1`

### Person Edit ###

 Edit the details of already existing person in the database by providing correct ID & other details.

* Command: **person_edit**
* Syntax: *`main.exe person_edit -id -firstname:optional  -lastname:optional -dob:optional -nickname:optional -address:optional`*
* Example: `main.exe person_edit -i=1 -f="Alexis" -a=[2,3]`

### Person Delete ###

Delete a person's details from Database by providing correct ID of that person.

* Command: **person_delete**
* Syntax: *`main.exe person_delete -id`*
* Example: `main.exe person_delete -i=1`


### Search ###

 Search through database for a specific person by their first name & last name.

* Command: **search**
* Syntax: *`main.exe search -firstname -lastname`*
* Example: `main.exe search -f="alex" -l="sanchez"`

### Address Add ###

Add a new address on the database, by providing all required details of the address.

* Command: **address_add**
* Syntax: *`main.exe address_add -line1  -line2:optional -country:optional -postcode:optional`*
* Example: `main.exe address_add -line1="Via di Santa Melania 60" -line2="Rifiano" -c="Italy" -p="39010"`

### Address Edit ###

 Edit the details of already existing address in the database by providing correct ID & other details.

* Command: **address_edit**
* Syntax: *`main.exe address_edit -id -line1:optional  -line2:optional -country:optional -postcode:optional`*
* Example: `main.exe address_edit -i=1 -line2="london" -p="22314HY"`

### Address Delete ###

Delete a address details from Database by providing correct ID of that address.

* Command: **address_delete**
* Syntax: *`main.exe address_delete -id`*
* Example: `main.exe address_delete -i=1`

### Address View ###

Check the details of all the addresses or a specific address details from the database.

* Command: **address_view**
* Syntax: *`main.exe address_view -id:optional`*
To Check all addresses details on the database, use below example.
* Example: `main.exe address_view`
To Check a particular address details, Kindly pass the address ID as argument.
* Example: `main.exe address_view -i=1` or `main.exe address_view 1`






# OpenClassrooms - Project 12 : EPIC Events - CRM

## Installation

### Python
Install [Python 3.9+](https://www.python.org/downloads/).

### PostgreSQL
Install [PostgreSQL 12+](https://www.postgresql.org/download/).

### Source code
Download the sources or clone this repository : ```git clone https://github.com/YaShuHee/openclassrooms_project_12```.

## Project setup
### Virtual environment
* Go to the project root : ```cd openclassrooms_project_12```.
* Create a virtual environment :
    - on Windows : ```py -3 -m venv env```,
    - on Linux/macOS : ```python -m venv env```.
* Activate the virtual environment :
    - on windows (from [PowerShell](https://docs.microsoft.com/fr-fr/powershell/)): ```. .\env\Scripts\activate```,
    - on Linux/macOS : ```. ./env/bin/activate```.
* Install the project dependencies in the virtual environment : ```pip install -r requirements.txt```.
* You can now activate the virtual environment you just created each time you need to run the app.
When you have finished using it, you can run ```deactivate``` to exit the virtual environment.

### Database creation
* [Create a database](https://www.tutorialspoint.com/postgresql/postgresql_create_database.htm) for the application.
* You will need the database name, the username and password you just set up for the next step.

### Settings
* This python project uses [python-decouple](https://pypi.org/project/python-decouple/) to prevent from sharing accidentally sensitive information (as secret keys), and to manage environments specificities (production VS developpment) in a simple file, no matter what OS you use.
* Create a file named '.env' at the root of the project ('openclassrooms_project_12/').
* Fill the file with all the variables mentioned next. You can modify the values. They don't need quote marks.
```
SECRET_KEY=g3n3r@T3_@_n3w_k3y
DEBUG=True
DB_NAME=previously_created_db_name
DB_USER=previously_created_db_username
DB_PASSWORD=previously_created_password
DB_HOST=localhost
DB_PORT=5432
```

### Application first run
* Run ```python ./manage.py makemigrations```
* Run ```python ./manage.py migrate```
* If you want to prepopulate the database with users, run ```python ./manage.py loaddata crm_user.json```.
* Run ```python ./manage.py runserver```.

## Test the application
### Get a username and a password
#### Solution 1 : Use the prepopulated users
* Their password is 'uns4f3pass'. To get their username (it is their email) and group, check into the 'crm/fixtures/crm_user.json' file. 

#### Solution 2 : Create your own super user
* Run ```python ./manage.py createsuperuser``` to create a super user.

### Test the admin interface
* Log into [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

### Test the API
#### Endpoints :
List of the endpoints :
 * clients list : [http://127.0.0.1:8000/api/v1/client/](http://127.0.0.1:8000/api/v1/client/)
 * detail for the client with pk=1 : [http://127.0.0.1:8000/api/v1/client/1/](http://127.0.0.1:8000/api/v1/client/1/)
 * contracts list : [http://127.0.0.1:8000/api/v1/contract/](http://127.0.0.1:8000/api/v1/contract/)
 * detail for the contracts with pk=1 : [http://127.0.0.1:8000/api/v1/contract/1/](http://127.0.0.1:8000/api/v1/contract/1/)
 * contract status list : [http://127.0.0.1:8000/api/v1/contract_status/](http://127.0.0.1:8000/api/v1/contract_status/)
 * detail for the contract status with pk=1 : [http://127.0.0.1:8000/api/v1/contract_status/1/](http://127.0.0.1:8000/api/v1/contract_status/1/)
 * events list : [http://127.0.0.1:8000/api/v1/event/](http://127.0.0.1:8000/api/v1/event/)
 * detail for the events with pk=1 : [http://127.0.0.1:8000/api/v1/event/1/](http://127.0.0.1:8000/api/v1/event/1/)
 * users list : [http://127.0.0.1:8000/api/v1/user/](http://127.0.0.1:8000/api/v1/user/)

#### Solution 1 : from the DRF web interface
* Log into [http://127.0.0.1:8000/admin/login/](http://127.0.0.1:8000/admin/login/).
* You can now check the endpoints.
* Log out [http://127.0.0.1:8000/admin/logout/](http://127.0.0.1:8000/admin/logout/).

#### Solution 2 : using Postman
* Send a POST request to [http://127.0.0.1:8000/admin/login/](http://127.0.0.1:8000/admin/login/) with 'Body' as a 'form-data' with two keys :
    - username,
    - password.
* Get the value of 'csrftoken' in the answer 'Cookies'. From now, pass it to the 'Headers' of every request you send to the API, using the key 'X-CSRFToken'.
* You can now send requests to the endpoints.
    - List endpoints (without the primary key in URL) accept GET and POST requests.
    - Detail endpoints (with the primary key in URL) accept GET, PUT and DELETE requests.
    - Only super user can use DELETE requests.
* To log out, just send a POST request to [http://127.0.0.1:8000/admin/logout/](http://127.0.0.1:8000/admin/logout/).

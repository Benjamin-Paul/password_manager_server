## Presentation

This repository contains the code for a simple password manager server written in Python.

The sevrer, at its core, is a Flask API contained in [the app package](/app/).

Through API endpoints implemented as Flask routes in the [routes module of the app package](/app/routes.py), it allows for user registration (/register), user login (/login), encrypted password storage (/add), vaulted password retrieval (/get), vaulted password modification (/change) and vaulted password deletion (/delete). 

It is designed to work off the shelf with a Postgresql database. Since it uses SQLALchemy, however, only a few changes to [the database subpackage](/app/database/) should suffice to make it work with other types of databases.

The postgres database must be created indpendently. Once a databse exists, its connection details must be entered in [the database.ini file](/app/database/database.ini.example). You can then run [the config.py script](/config.py) to automatically create the required tables in your database. The link between the server and the database is then handled through Flask-SQLAlchemy models defined in [the models module of the app package](/app/models.py).

The server implements JWT for user authentication. Sessions are maintained for one hour after the token has been issued. See [the auth subpackage](/app/auth/) for details. Tokens are signed and verified with a secret key stored in [the project .env file](/.env.example).


## Getting strated 

Install the project's requirements :

```bash
pip install -r requirements.txt
```

Enter your postgres database details in [the database.ini file](/app/database/database.ini.example). For example :

```
[postgresql]
database = postgres
user = johndoe
host = mysuperdatabase.com
password = correct_horse_battery_staple
port = 5433
```

Run the config.py script to create the tables in the database :

```bash
python3 conifg.py
```

Rename the .env.example file to .env and add a long, random JWT signing key to it. For example (obvioulsy don't use this key) :

```
JWT_KEY="0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a"
```

Run the config.py script to create the tables in the database :

```bash
python3 conifg.py
```


## About security

This server is designed to be as secure as possible : as such, it never stores users master passwords in any form. Instead, it uses a zero-proof knowledge algorithm to authentify clients. The password are then stored in an encrypted form that can only be decrypted on the client itself, since the server doesn't know anything about master passwords.

For more, check the corresponding client implementation. 






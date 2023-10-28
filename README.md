*This is an educational project, and users should assume full responsibility for any issues that may arise during real-life use.*


# Presentation

This repository contains the code for a simple password manager server written in Python.

The sevrer, at its core, is a Flask API contained in the [app](/app/) package.

Through API endpoints implemented as Flask routes in the [routes](/app/routes.py) module of the app package, it allows for user registration (/register), user login (/login), encrypted password storage (/add), vaulted password retrieval (/get), vaulted password modification (/change) and vaulted password deletion (/delete). 

It is designed to work off the shelf with a Postgresql database. Since it uses SQLALchemy, however, only a few changes to the [database](/app/database/) subpackage should suffice to make it work with other types of databases.

The postgres database must be created indpendently. Once a databse exists, its connection details must be entered in the [database.ini](/app/database/database.ini.example) file. You can then run the [config.py](/config.py) script to automatically create the required tables in your database. The link between the server and the database is then handled through Flask-SQLAlchemy models defined in the [models](/app/models.py) module of the app package.

The server implements JWT for user authentication. Sessions are maintained for one hour after the token has been issued. See the [auth](/app/auth/) subpackage for details. Tokens are signed and verified with a secret key stored in the project [.env](/.env.example) file.


# Getting strated 

Install the project's requirements :

```bash
pip install -r requirements.txt
```

Enter your postgres database details in the [database.ini file](/app/database/database.ini.example). This file should look like this :

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

Rename the [.env example file](/.env.example). to .env and add a long, random JWT signing key to it. The file should look like this (obvioulsy don't use this key) :

```
JWT_KEY="0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a"
```

Execute [run.py](/run.py) to launch the server :

```bash
python3 run.py
```


# About security

This server is designed to be as secure as possible : as such, it never stores users master passwords in any form. Instead, it uses a zero-proof knowledge algorithm to authentify clients. The passwords are then stored as encrypted strings that can only be decrypted on the client itself, since the server doesn't know anything about master passwords.

For more, check the corresponding client implementation. 







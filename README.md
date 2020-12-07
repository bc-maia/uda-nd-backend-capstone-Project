# Udacity Capstone Project

### This Capstone project finishes the full stack nanodegree course.

As rubrics: the following steps were implemented to fulfill all requirements as listed bellow:

* Data Modeling
* API Architecture and Testing
* Third-Party Authentication
* Deployment
* Code Quality & Documentation

The tech-stack this project makes use of are:
* python
* python unittest
* flask
* auth0.com
* heroku.com
* postman

___

## Steps for testing

## User and passes
* For this project were created two testing accounts with their proper roles
    * dungeon master (admin role):
        * dungeonmaster@dungeon-monsters.io
    * basic user (player role):
        * player@dungeon-monsters.io

Both users have the same testing password: **L0gin123-**
___
## Login URLs for heroku and localhost

[heroku](https://uda-cafe.us.auth0.com/authorize?audience=https://dungeon-monster.herokuapp.com&response_type=token&client_id=xSDVoDPZBduRjHFLyaBXkyN0S8llJ1az&redirect_uri=https://dungeon-monster.herokuapp.com)

[localhost](https://uda-cafe.us.auth0.com/authorize?audience=https://dungeon-monster.herokuapp.com&response_type=token&client_id=xSDVoDPZBduRjHFLyaBXkyN0S8llJ1az&redirect_uri=http://localhost:5000)


### After these two steps above, select one of the URLs above and one user to generate a token

* When the URL loads, a Auth0 login screen will appear, so put the user/pass.
* When the page finishes loading the request, the page will be redirect to the root of the running API. (heroku or local)

The jwt token is contained in the response URL as **access_token**.

A quick hand to get the token is open the browser console on developer tools (F12), and run the following JavaScript command
```JavaScript
window.location.hash.substr(1).split('&')[0].split('=')[1];
```
___

## Database Setup

When cloning this repository, the database must be configured so this API can persist it's data using PostgreSQL database. For this project, any install will work from bare metal to dockerized database. Once created, you should update the **./setup.sh** file, changing the postgre connection URL unless a database is created using same username/password/database_name.

After database created, run this command to create the database tables:
```terminal
python manage.py db upgrade
```
___

## Client Setup ([Postman](https://www.getpostman.com/))
* First, get the postman collection in this repo and import on postman client. [how to](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/)

* Then, create a postman environment for our collection variables: [how to](https://learning.postman.com/docs/sending-requests/managing-environments/#creating-environments)
    * bearer
    * host
    * port (only for localhost testing, remote heroku uses SSL, which's by default 443, so it's not required)

* using the previous step to accquire the *bearer token*, add it to the postman environment variable **bearer**, this variable will be used by the authorization tab.

* the host and port will vary deppending on the environment used for testing, these two will be used for constructing the request URL:
    * For *local* testing:
        * http://localhost
        * 5000
    * For *heroku* testing
        * https://dungeon-monster.herokuapp.com
        * 443

___

## Done

```
  ___________________
< Now, Make-A-Request! >
  -------------------
         \   ^__^
          \  (oo)\_______
             (__)\       )\/\
                 ||---WW||
                 ||     ||

```


## API Routes Map

The complete route specification and required payloads are on this postman file:
**./postman/Udacity_capstone_dungeon_monster.postman_collection.json**

```
GET /monsters
```
* Lists all available monsters

```
GET /monsters/1
```
* Description of a specific monster with details
```
POST /monsters
```
* Create a new monster
```
PATCH /monsters/3
```
* Update a monster data by ID
```
DELETE /monsters/3
```
* Remove a monster by ID
```
GET /dungeons
```
* Lists all available dungeons
```
GET /dungeons/1
```
* Description of a specific dungeon with details
```
POST /dungeons
```
* Create a new dungeon
```
PATCH /dungeons/2
```
* Update a dungeon data by ID
```
DELETE /dungeons/2
```
* Remove a dungeon by ID
```
GET /dungeons/1/monsters
```
* Lists all monsters from a dungeon
```
POST /dungeons/1/monsters
```
* Add a monster to a dungeon
```
DELETE /dungeons/1/monsters
```
* Remove a monster from a dungeon

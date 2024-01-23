# SHIRITORI WEB APPLICATION
#### Video Demo:  https://youtu.be/YMM2M9SN2ho

#### Description:
This is a web application for the traditional japanese word chaining game, Shiritori. This web application utilized Flask with python as it's backend along with Javascript, HTML and CSS. Some functions and templates for the pset9, Finance are used in this project. There are a couple of folders and files utilized and I will explain them below.

# Features
# flask_session
This contains the flask session produced during the development of the web application.

# static
This directory contain the stylesheet for the website and the javascript used for the website.

### styles.css
This css file contains some of the css used for the website, some other css are used are from boostrap and not in this file.

### play.js
This is a javascript file for the template, "play.html". This javascript utilize AJAX to communicate information to the python script for further processing and this also contains multiple functions for the score system to work and also dynamically changes the UI and some part of the webpage with innerHTML and styles.

# templates
This directory contains all the html templates as well as the layout html for the entire web application.

### apology.html
This html shows the apology message to the user in the case of user missuse of the web application.

### history.html
This html shows the history of a user's score and the time upon a completion of a game.

### index.html
This html shows the index of the web application, which is a big play button for the user to start a game.

### layout.html
This html is the layout of the entire web application, it utilizes flask to achieve the purpose of serving as a layout html.

### login.html
This html is the login page of the web application, it utilizes a database and a python script to authenticate it's users.

### play.html
This html is the bread and butter of the web application, as it is where the user play the game. There is a input field for the user to insert some words and new words will be generate upon the submission of the user.

### ps.html
This html allows the user to change their password.

### register.html
This html is the registration page of the web application, it allow users to register a new account into the database.

### rules.html
This html shows the rules of the game, Shiritori.
#### Referenced source: https://en.wikipedia.org/wiki/Shiritori

### scores.html
This html shows the top 5 score of every players and their respective username from descending order.

### settings.html
This html shows the settings available for the users to change, which contains two links.
1. ps.html -> Change password
2. un.html -> Change username

### un.html
This html allows the user to change their username.

# app.py
This python file contains the main part of the web application's routing, it handles all the routes and return values of the entire web application.

# helpers.py
This python helper file defines functions and libraries that app.py uses and handles return values for app.py to function.

# JMdict_e.xml
This is an xml file that contains japanese word that the game uses, it serves as a dictionary that verifies word validity and their definitions.

# requirements.txt
This is a text file that shows the requirements used for the web application.

# stack.py
This python file keeps track of a user's input to prevent the same input.

# users.db
This database file contains all the user's login information and their scores with respective time for the web application.

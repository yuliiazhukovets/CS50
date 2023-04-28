CS 50. Final Project
Zhukovets Yuliia
College&Squash
Documentation

Folders
All necessary files are in the directory Project. Inside this directory there is directory Static that contains a stylesheet and a picture for the main page and directory Templates that contains all HTML files. Inside the directory Project, there is file application.py, which contains source code for the project, it also references file helpers.py. Inside the directory Project is also database squash.db, that contains all the necessary information to populate web pages.

Compiling
To compile the code, one will need to cd in the directory Project and type “flask run”. There are no other necessary actions to perform.

Manual
When the webpage opens, a user will see a navigation bar with two buttons “Register” and “Log In”.
If a user visits the website for the first time, they will have to register, by pressing the following button. There they have to input their email address (which will be used for logging in later), their first name, last name, password and confirmation password, that should match. User should then press the register button.
If a user has previously registered, they should click the “Login” button. Where they will have to put their email address and password, that they used upon registration.
After logging in/registering a user will see a home page with a brief introduction and a navigation bar on top with buttons: Search, Favorites, About, Map and Log Out.

Search
On the search page there is an input field, where a user can start typing the name of some team and by pressing the search button or enter will be redirected to the results webpage, where they will be able to see the information about the teams from the search action.
On the results page they will see a table. The first column contains a favorites button. A user can press this button and the team on the same row will be added to their favorites, which they can later view in the Favorites tab. They also see the name of the team, its gender, rank and type. On each row there is an information button, which the user can press and see a personalized page of a particular team.
On a personalized page of each team a user is able to see a name of the team, gender, type and its coach. They are also able to visit the website of this team by pressing  “Link to the website of this team”. Below users are also able to see the table with the ranks of this team over the past 4 seasons.
On the search page, the user will see the table with all US college squash teams, which has the same functionalities as the table on the results webpage. In addition to the table, there are 3 buttons above it.
Order By ->  Rank
By pressing this button, the user will see the search webpage, but with teams ordered by ranks in the ascending order.
Order By -> Alphabetically(default)
By pressing this button the user will be redirected to the initial search page.
Filter by Gender -> Men
By pressing this button the user will be redirected to the search webpage, but now they will be able to see only men teams.
Filter by Gender -> Women
By pressing this button the user will be redirected to the search webpage, but now they will be able to see only women teams.
Filter by Type -> Club
By pressing this button the user will be redirected to the search webpage, but now they will be able to see only club teams.
Filter by Type -> Varsity
By pressing this button the user will be redirected to the search webpage, but now they will be able to see only varsity teams.

Favorites
By pressing the Favorites button on the navigation bar, users will be redirected to the webpage where they will be able to see all the teams they have previously saved. In the same way as on results and search webpages, they will see a table with a name, gender, type and rank of the team. As well as a button Info that will take them to a personalized web page of the following team.

About
By pressing the About button on the navigation bar, users will be redirected to the webpage where they will be able to read a brief introduction and why I decided to make this website.

Map
By pressing the Map button on the navigation bar, a user will be redirected to the webpage where they can see google map with several markers of the universities that have squash teams. They can move the map (zoom in/out). By pressing a marker a user will be able to see a name of the university, its address and type of the squash team.

Log Out
Finally, once a user is done using the website, they can log out. However, it is not necessary to log out, they can just close the tab and the session will end automatically.

Link to the video presentation
https://youtu.be/8N-QckpkQaU
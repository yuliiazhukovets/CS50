CS 50. Final Project
Zhukovets Yuliia
College&Squash
Design

Squash Database
Because my project greatly relies on the SQL queries, I have created a database that stores all the necessary data.
In table teams, I store the name, gender, type and rank for season 2019-2020 for each of the teams.
In table teams, I store the names of the coaches for each of the teams.
In table links, I store links to the official websites of each team.
In table, all_ranks I store information about the ranks of each team in the past 4 seasons.
Each team has its unique id and all tables could be INNER JOINED on it. I decided to store all this information separately, to avoid a lot of columns in one table,
In table users, I store email, hashed passwords (for security reasons), first and last names and their unique ids.
In table favorites, I store the user's id and ids of all the team that the user saved during the sessions.
Where these tables can be joined on the users’ id.

Layout
In my layout.html I set up the general layout for the all HTML pages. If a user is not logged in, they will see only Login and Register buttons on the navigation bar. If a user is Logged in, they will see Search, About, Favorites and Map tabs. On the bottom, I have a footer with the hyperlink that provides access to the website from where I got most of the information.

Register
At first I implemented a register function, which is very similar to the one I implemented in Finance. Through request.form get python code gets name, email and password of a user and updates the database with these details, provided there are no users with the same email addresses. In the HTML code, I have a form that gets submitted with the post request. I decided to position input fields in the center for visual purposes, as well as potistion first and last name fields on one line and passwords fields on the same line too.

LogIn
For login,  through request.form get python code gets email and password from the HTML page and checks against the data in the squash.db. In the HTML page,  I used a form that sends a post request when the user presses the LogIn button.

Search
For search functions I have used if statements to differentiate between actions necessary for POST and GET requests. If it is a POST request, that is a user submits a form on the webpage. Python code gets the name of the team and then runs an SQL query to find all the teams that are similar  to the input that the user has provided in the input field. To run SQL query I decided to use %”user’s input”% to allow for all the possible search results. However, if the user's input is incomprehensible, code will return an error template asking to provide a valid name of the team. After running a SQL query and finding matching teams, the program outputs a results template which contains information of all the teams that matched the search condition.
To personalize a user's experience I run an SQL query to get a name of the current user and output “Welcome, [name]” on most of the webpages.
On search and results HTMLS users will see a table that has information about the team, as well as two buttons on each row. To dynamically populate the table, I used JINJA code in my HTMLs, by looping through the data passed with render_template. On each row there are favorites and info buttons, that both use forms to send POST requests to application.py when the user clicks on either of them (for this I used onclick/onchange parameter and submit). When implementing the code I ran into an issue of nesting forms. For both of the forms I needed the same information. However, I had to close first form before running second. That is why I decided to use the “hidden input” tag for the name and gender of the team in both forms. For each button I had to create a seperate form, because the submit function uses document.getElementById and all ids are supposed to be unique. In order to create unique ids, I looped through the list of dictionaries (the data put through render_template) and added keys favorites_id and team_page_id and populated it with the unique ids for each form. By doing this, I got my code to submit a particular form for a particular team and get accurate information.
I used the same approach for favorites.HTML, but there I only have info form.
Secondly, if it is a GET request, my program runs a SQL query to get information about all teams and passes it to the HTML code through render_template. Later on the HTML page I loop through this data to populate the table..
On my search page there are also 3 buttons that allow a user to filter table entries by gender or type, or to order tables entered by rank or alphabetically. To implement these features, I created 6 separate routes and functions. Where all of the have if functions for POST or GET request, where POST request of identical to the one in search and the only difference in GET request is that they use different ORDER BYs or column where the input for women_men/varsity_club is only Men/Women/Varsity/Club.
I wish I could have found a more sophisticated and efficient way to implement Order by and Filter by functionalities. But because there are different routes and all of them use POST and GET requests, this was the only solution I found.
I tried separating table entries into several pages (by having 20 entries on each page), but, unfortunately, I could not figure out the code for it.

/ and About
These two routes only return HTML template with brief introduction and an image. I add special CSS parameters for the image, so that it is adopted to the mobile phone screens as well.

Favorites
Favorites function also takes two requests: GET and POST.
If a POST request gets submitted (that is user presses Favorites button on search or results webpage) program gets name and gender of the team and then runs SQL query to get its id. In order to avoid programs adding the same team to favorites all the team, I run an error-check. Where I look up this id in the favorites table and if there is no such id (that is a returned list is null), I proceed to add this team’s id to the favorites table, making sure it corresponds to the id of the current user. After that the user gets redirected back to the search page.
I tried implementing an alert JS function that would pop up every time a user saves a particular team. Unfortunately, I could not do it, because I did not figure out how to pass information from Python to JS.
If a GET request gets submitted (that is the user just opens a Favorites tab), the program runs a SQL query on the favorites table to get ids of all teams that the current user has saved. Because there might be several teams that the user has saved, I decided to create an empty list, to which I append information about each saved team. In the loop I also generate unique ids for the info form (for the reasons explained above). Then the program renders a template favorites, which is a page very similar to the search, except that there is no favorites button and Order by, Filter by buttons. Essentially it is the table where users can see brief descriptions for each team and then click the info button to find out more information. I decided not to implement Order by and Filter by functionalities on the favorites page, because there should not be that many teams saved and adding these buttons would mean adding 6 more routes and functions.

Team Info
This function only takes GET requests (that is when the user presses the info button on either search, results or favorites page). Because there are 137 teams, I decided to create one template that will take information about a particular team from the database and populate the HTML page. Therefore, in my code for the team_info function, it gets the name and gender of the team and then runs 4 SQL queries on tables: teams, links, ranks and coaches,  to get all the necessary information. Then it renders a template through which I pass all the information above and in that way the page gets populated with the personalized information of each team. On the HTML page, a user is able to see the name of the team, its gender, type and coach. There is also a hyperlink that will lead to the official website of this team. Below is also a table with the ranks over the past 4 seasons.
I wish I provided more information on the personalized web pages(like picture,  the roster, played matches etc), but because there are 137 teams I would have to manually input all these information. That is why I decided to opt in putting just a link to the official website, by clicking which a user can see more information.

Map(index.html)
Finally, I implemented a map function which only renders a template of index.html, because all information is static. On the map user is able to see marks for some universities that have squash teams,
I decided to put only several markers on the map, because otherwise I would have to manually look up coordinates and addresses of each university.
Ultimately, in my index html I run JS code, where I input coordinates of each university, then create a marker, content for the information window, create information window and add EvenListener that opens the information window when a marker is clicked. On the top I initialize my map to open focused on the center of the USA.
Because there were not as many universities, I decided to write all of these functions separately, instead of creating lists and looping through them.

Alerts
On each webpage, I have added alerts that users can close after reading them, to provide a more user friendly experience.

CSS file
In my style sheet I altered parameters for most of the tags: implementing the same font for all texts, aligning objects and setting up the color scheme.

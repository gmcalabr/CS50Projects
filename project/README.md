# Personal Family Tree Website
#### Video Demo: https://youtu.be/JbN_xCHbPmk
#### Description: Family Tree recording and viewing website

## Hello World, Hello CS50

My project is a simple family tree recording website. I began with the CS50 Finance site structure but changed so much from there.

This is a passion project that stems from my genealogical research as of late. Ancestry.com is the premier research platform but I believe it lacks in printable, single-page layouts. Nearly all information about each person is hidden in the tree view and only shown by navigating into each person's information page. Comparing birth locations, occupations, immigration dates, etc between people requires a lot of navigation and cannot be viewed simultaneously. As someone who is looking for a printable family tree that could even be hung on the wall, I created a basic tree layout tool for my own use with this project.

## Basic User Flow

Upon first visit to the site, a user is asked to create a username and password to login. Once registered they are directed to add their own personal information first. After form submission, the user is guided to the index page. The site UX is essentially two web pages, one for information entry/editing, and this index family tree view. This tree view centers on the user and their data, but more relatives can be generated easily through the interface.

After the user lands on the family tree index page, all other additional family members can be added directly to the user's 'root' by clicking the “Add a Mom” or “Add a Dad” buttons at the bottom of the object. These buttons will open a familiar data entry form page. Submitting this form leads the user back to the index page and whatever relative was added will show in the standard family tree format.

The index page is designed to hold 7 people, or 3 generations at a time. However, the three itself can be infinitely expansive. This navigation forward up the branches is handled by a ‘Focus on {name}‘ button located in each person's tree object. The page redraw the 3 generations of tree data without without reloading the page. A simple ‘recenter tree’ button appears at the top of the page which is essentially a convenient refresh button.

One additional button is included in each person object: an edit button. As expected this button brings the user back to the familiar data entry page, but the form will be pre-filled with all existing information for easy editing. Form submission brings the user back to their newly edited tree (index).

## Back End

As stated, this website starts with the CS50 Finance structure. Programming is standing on the shoulders of giants. The basic Finance layout, login, logout, and registration pages are largely intact. The app.py is mostly fresh, including all new routes and new libraries in order to support the very different functionality. The styles.css page was heavily updated to visually enhance the site.

The database structure is different than Finance. The user.db is largely similar but there are now 3 db files. People.db lists all persons and their information in the website using an auto-generated sequential person id number and are also linked to users.db via a userid number. Lineage.db tracks the structure of each family tree using three id numbers. The id, mother, and father are all id's matching the id numbers appearing in people.db.

Data entry and editing is handled in three highly similar html pages. /newperson, /firstperson, and /editperson appear mostly the same but with some differences based on the specific flow of the site. The /firstperson is very straightforward. /newperson adds relationship data to handle all lineage.db interaction. The newperson.html autofills this data based on the navigation clicks made by the user /editperson is the same as /firstperson but prefills all existing data so the user may edit, remove, or add to that data.

### index.html

This is the most complicated part of this website. The page’s job is merely to draw 7 boxes full of database information so the actual html content is very short, however the script is built to iterate through a loop to fill this content in 7 placeholders.

There are essentially two main functions and several supporting functions with the script. The generatePyramid(people) draws 3 classes (rows) of content based on the generations being shown in this tree (or pyramid) structure. These classes are the user, their parents, and their grand parents. Each person must have their information pulled from the database and shown to screen. The first class must additionally be able to identify who the user (or other first ‘generation’) and their parents. The second generation must identify the 3rd generation. The third generation is simpler.

The second critical function in index.html is the generateTable(person). This function is called within the generatePyramid() function, and uses the already iterated people.forEach((person))selection. This function generates a table of data that goes into each person object (currently a subset of all information gathered), as well as the 4 navigation buttons tagged to each person. These buttons were by far the most difficult part of this project. There are 3 very different functions, auto-generated if-on demand, all inside the same form, iterated over 7 people in the display. Avoiding form submission conflicts, hiding and showing buttons dependent on the person’s position and whether or not family members existed in the database, etc. took significant work.

One of those buttons is very critical function for navigation. The button labeled “Focus on {person.name}” button triggers a series of smaller functions. Most critically, this function clears the table, selects a new first person (top of the table), and redraws the page content. This is done without refreshing the page for speed and smooth UX. So long as there are relatives in the tree, the user may continue to move down any particular branch of the tree as far as they like.

### app.py

Of course, the app.py file is the backbone of this website. I don’t wish to belabor all functions here, but I want to point out two things. First, the general layout of the three most similar routes, and the simplicity of the /index route.

The three most similar routes, (/firstperson, /newperson, /editperson), essentially just create and gather a form in their GET and POST methods. I highlight here the safety measures implemented. Since the people.db file includes all people from all users’ families, there needs to be a sort of firewall between them. Separate databases for each user’s data is infeasable as the userbase grows so instead I ran code that checks the user’s session data and compares that against the information they’re attempting to query. In the GET method, any person being edited has their userid checked against the userid from the session data prior to load, and an error is returned to the user letting them know this is an invalid request. In case the user gets smart and merely tries to edit someone else’s data, the POST method makes this same check again before allowing an edit.

There’s one more route of interest. The /index route is formed of essentially 3 lines. These lines gather information from the database into the variable people and then pass that variable into the index.html page. Since virtually all code is client-side, this pushes the computing load to the client and leads to the great flexibility used in the js code in the html page. All of the error-checking, security protection, and database management occurs server-side while all of the UX occurs client-side.

## Final Thoughts and Future Improvements

There are three specific things that could change this website in the future.

Most obviously, the three .html files used for data entry could be combined to simplify the structure. However, small differences in how data is collected and verified make that difficult. This was not worth the complication at this early stage; being online is more important to a new website than being perfect.

Second, the index.html file could have the script section pushed to a script file. I chose not to for time. However this code is only used in this page and there is no copypasta with any other pages.

Third, I used 3 separate db files. This was at first what I believed I needed before I got to work on the actual index.html script structure. It turned out to not be fully necessary. Still, I think that it enables far more dynamic UX in the future, so it was kept.

I hope you have enjoyed using my family database creation website.



# Huertapp
A web-app to plan a vegetable garden.

#### Video Demo on [Youtube](https://youtu.be/yz1h42X94P0)
#### Live version at [Heroku](https://myhuerta-app.herokuapp.com/) - With bugs 

### Description:
Huertapp is a web-app using python, flask, sqlite3 and jquery mostly.

The main idea is an app that helps the user browse through vegetables, select some and with those selected then plan and design the garden.

Due to the time frame only some of the ideas where fully implemented in this first step, some remained partially implemented and are marked as "beta".

### Files

#### proyect/application.py
 Contains the mayority of the python code use by Huertapp.

 Handles the interacction with the database, rendering the html's of each corresponding page with the content requested of the db and also receives the data from the html and user selections and input to save it on the db.

  The user on first entering, not having selected any vegetables selects some and those are added to de db and then removed from the catalog from which it was choosen. The catalog on render checks the current user's selected vegetables so as to not show them. In the landing page / or index.html if the user has any vegetables they are shown, and also the user is allowed to removed the selected vegetables. Also there is a datepicker, whose date once selected is saved to the database and is loaded on render if already selected previously. The date can also be updated any times and it changes on the db.

  There are to routes/functions in "beta": my_plot and my_garden, the implementation on both is not ready yet.

  My_plot checks the user's current vegetables and displays in a select grid of 3x3 those vegetables. On change of any of them searches for compatible plants and adds them to the select.

  Yet to implement is saving any possible combination of choices by the user on the grid and also that only the contiguous selects to the one changed display the compatibilites.

  My_garden shows a container and pictures from the user's vegetables, the user can drag and drop the images inside the container and organize them, but a save of the selection is yet to be implemented. As well as some further work in the user experience of the drag and drop.

 This file also manages user sessions, including user, password and change of password.

#### proyect/helpers.py
  Contains two helper functions provided by CS50 Finance PSET.

#### proyect/huertapp.db
  The sqlite3 database of the app.

  It has 4 tables.
- Users: Which keeps track of user id, username and pass
- Plants: Where all of the info from the vegetables is, most of the info here was obtained from [https://data.world/sharon/vegetables-herbs-and-edible-flowers] an open source csv.
- users_plants: A many to many table that takes the user id and each of the user's selected vegetables and also (if provided) the sow_date for the vegetable.
- compatible_plants: A many to many table in the making, only 10/90 vegetables where added so far. This table joins the id from one vegetable with each of the compatible plants a column in the plants table, the info in the plants table is a string and in the table compatible_plants are all id's.

#### proyect/static/styles.css
  The stylesheet for the web-app

 #### proyect/templates/apology.html
 A file provided by CS50 Finance PSET that conects to an API to make apology memes for errors, modified to match the style of Huertapp.

 #### proyect/templates/index.html
 The landing page on register and login.
 Checks if the user has selected any vegetables, if not renders a page offering to choose some, and redirects them to vegetable_catalog to add some vegetables.
 If the user has any vegetables for each vegetable creates a bootstrap collapsable with several options from retrieved information from the database. The options are selectable by icons from fontawesom library. There also is a datepicker, the selected date is saved in the table users_plants and then displayed on the datepicker on every load of index.html. Lastly there is a remove button which deletes the vegetable from the users_plants table for the current user.

 #### proyect/templates/vegetables_catalog.html
 The catalog of all non-selected vegetables, using boostrap cards.
 On render selected from the database recieves all non-selected vegetables to be displayed, each has an ADD button, onclick the vegetable is added to users_plants for the current user id. On the bottom of the page there is a READY! button to take the user to My Vegetables once has finished browsing and adding. The nav-bar link My Vegetables also can be used to get there.

 #### proyect/templates/my_garden.html  BETA
 One of the two functionalities still in beta that will be further developed at a later time is My Garden.

 This is a drag and drop where you have a container and the pictures of each of the user selected's vegetables which you can drag and drop into the container and re-arrenge there.

 In the future the user will be able to edit the size of the container on scale to their planed plot and the pictures will resize according to the scale.

 Also a table will be created to save the user's preferences and planning.

 #### proyect/templates/my_plot.html  BETA
 Similarly as with my_garden, my plot is still in beta.

 There is a grid with nine selects in a 3x3 disposition. On each select we have the current user's vegetables, and after selecting one the other selects options will update acording to the table compatible_plants offering compatible plants for the latest vegetable selected.

 There are a lot of corner cases and functionalities inside this idea that are not yet solved, so i will continue to work on this!

 #### proyect/templates/register.html
The register screen, checks if the user already exists and if the password and the confirmation are the same, then it logs in the user, developed for CS50 Finance and adapted to match Huertapp style.

 #### proyect/templates/login.html
 Login screen, checks if the username and password matches and logs the user in, developed for CS50 Finance and adapted to match Huertapp style.

 #### proyect/templates/pass.html
 A page to change the password, developed for CS50 Finance and adapted to match Huertapp style.

 #### proyect/templates/layout.html
The layout for the scripts, links, imports, navbar, main body and footer.

### I am Martina Quintas, from Buenos Aires, Argentina and THIS was Huertapp!

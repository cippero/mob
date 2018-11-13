[Check out the app!](https://mobtracker.herokuapp.com/)
# Mob

## Proposal
*Mob* is an MVT app that lets users post goals and share advice on achieving those goals. The app sends incoming replies to IBM’s Watson AI to analyze against the posted goal and determine the relevance. I then use the response from Watson to style the posted advice so that more relevant posts are color-coded and easily identifiable. 

## Description
I chose to build this application on Django since this powerful framework facilitates building modular apps that can easily be incorporated into a larger Django application. In addition, it includes useful tools like built-in CSRF to protect the user’s session from getting maliciously hijacked while submitting forms, and an ORM to easily and securely communicate with databases while preventing SQL injections. The Model layer of this application consists of PostgreSQL and the Template layer uses jQuery and the Jinja2 templating engine to render the UI and incorporate dynamic data from the Model layer.

A typical interaction with the app will usually consist of the following steps:
* The user registers or logs in through the Register/Login Template forms, where Django’s built-in CSRF protects the user’s session from being maliciously hijacked.
* The user will post a goal.
* The goal’s title is run through a Regular Expression to sanitize and use as the RESTful endpoint for the particular goal.
* The goal is posted to the database and the user is redirected to the goal’s dynamically generated Template.
* If another user replies to the posted goal, their message is sent to the Watson AI to analyze in relation the goal and given a relevancy score, which color-codes the reply.
* The message is posted to the database and rendered on the page in the color-coded relevancy score.
* The replier’s username is added to the list of contributors.
* Users can browse or search through posted goals or view all the contributions a user has made by going to their profile. 

## Technologies and Tools

Python, jQuery, Django, PostgreSQL, Materialize.

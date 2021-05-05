# flask-authentication
Flask app giving access to registered users to a secret page containing a Flask cheatsheet PDF.

The goal of this app was to implement authentication with Flask on a full-stack website.

For a website, having users is important as it allows more interaction between the application and potential clients. 
Having real humans contributing to the web site adds more content and flavour to the site.

But in order to have users, we need to associate data to user accounts and this requires the implementation of a registration system,
that allows the users to register, then sign in and out from the site.

This means that the users will give us some information about them (email, name, password) so that we can confirm their identity as a user of our site.
This is the main idea behind authentication ! We don't want to give full access to all the pages and routes of our site to everyone. Some routes and 
pages and therefore content will be restricted to users only.

The project implements this, by allowing users to download a Flask programming cheatsheet. But this PDF file will only be available once they have registered
and that they are logged in.



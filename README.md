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

Registering new users

To register new user, we need to extract the information inputed into the the register form and use it to create a new user on the database.
This is done thanks to the Python module "request". Once the data (name, email and password) is extracted we insert a new entry in the database
and render afterwards the secret page containing the PDF file. The form used for the register page is a simple and classic HTML form element

![image](https://user-images.githubusercontent.com/55893421/117393353-f064ef80-aec1-11eb-8362-2db203a1337d.png)


Hashing the passwords

A key aspect sometimes neglected by companies is the ability to protect the user data. It is very risky to store our user's passwords as plain text. A hacker breaking
into our database would have almost immediate access to all the user's accounts on our site. A good strategy against such sort events is to employ hashing for 
our passwords. Hashing involves the use of a hashing function which will take the plain text password and generate a scrambled reprensentation of the password
thanks to a set algorithm (in our case, pbkdf2:sha256). To increase the encryption of our passwords, we use a salt of 8 characters. A "salt" is simply a set of random
unique characters that are added to the hashed password. In this project, we use the Werkzeug helper function generate_password_hash(). 
This function takes three parameters: the first one is the password of the user that we must hash, the second is the method of hashing, the third is the number of 
characters for our salt.

![image](https://user-images.githubusercontent.com/55893421/117394535-55214980-aec4-11eb-9907-94a553dc1ad9.png)


More info on the Werkzeug helper function generate_password_hash() can be found here: https://werkzeug.palletsprojects.com/en/1.0.x/utils/#module-werkzeug.security






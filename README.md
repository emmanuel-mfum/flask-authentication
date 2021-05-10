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


Authenticating Users with Flask-Login

The next step is now to make sure the "/secrets" route is no longer accessible unless one is authenticated (aka logged in)
This is done via a function decorator "@login_required" from the flask_login module.
We apply this decorator to the route "/secrets" and "/download".

![image](https://user-images.githubusercontent.com/55893421/117725202-cefe4f00-b1b2-11eb-9ae7-9dfb6b468327.png)

![image](https://user-images.githubusercontent.com/55893421/117725252-e2111f00-b1b2-11eb-9f27-88d13334061c.png)

Once we got our "sensitive" routes secured, we must implement the login route.
This is done configuring our application by first creating an instance of the LoginManager class.
![image](https://user-images.githubusercontent.com/55893421/117725814-b3477880-b1b3-11eb-9ead-1ae1af5faf3e.png)

Once the actual application object has been created, we can configure it for login with:
![image](https://user-images.githubusercontent.com/55893421/117725848-bb9fb380-b1b3-11eb-99a6-fa632e8a0747.png)

Flask-Login uses sessions for authentication. This means we must set the secret key on our application, otherwise Flask will give us an error message.

After configuring our app, we need to create a user loader function. The purpose of such function is to reload the user from its user id
![image](https://user-images.githubusercontent.com/55893421/117726634-d7578980-b1b4-11eb-95cc-2f4ec9929f64.png)

Afterwards, we need to implement a UserMixin, which is basically a class with properties and functions inherent to all user sessions. 
We can import this class from the flask_login module and we pass it as a parameter in our User class (therefore making our User class inherit 
all those methods and properties from UserMixin). The Mixin is much simpler way of implementing methods for the user authentication as we 
provide inheritance of the class to our User class.

![image](https://user-images.githubusercontent.com/55893421/117727064-88f6ba80-b1b5-11eb-8fff-0e0125da5c8a.png)

Now, we can start implementing our login route.

First, we check to see if our user is authenticated upon reaching the login page. If he/she is, then he/she is redirected to the secret page.
However, if the user just logged in by entering his/her credentials, then we extract those from a form. Using the email entered, we try to find 
the user inside our database.

If the user is not found (no corresponding email is found in the database), we will flash a message accordingly telling so the user.
Else if the user is found, we need to check if his password is correct , otherwise we flash a message on the screen telling the user about it.
If the user is found on the database via its email and the password entered is correct, then we log in the user by passing our user obhect found
in the database into the function login_user() which starts the user session. That method comes from the flask_login module.


![image](https://user-images.githubusercontent.com/55893421/117733982-7d5cc100-b1c0-11eb-9dec-ac800146b73b.png)


Flask Flash Messages

Sometimes, we want to inform the user that something went wrong (password or email) with their log in attempt. In that case, it is a good idea
to use Flask Flash messages. They are messages that get sent to the template to be rendered just once. And they disappear when the page is reloaded.
To do that, we just need to put some Jinja code relating to Flask Flash templates in our "login.html" file:

![image](https://user-images.githubusercontent.com/55893421/117734461-84d09a00-b1c1-11eb-8148-7116bb817ff0.png)

Then in our Flask server we can call the function flash when we need to flash message on the login route. See photo above with the login route.
The method takes an argument which is the message we want to flash.


Passing Authentication Status to Templates

When a user is logged in, the home page should not show the login/register buttons. The navigation bar should not show Register or Login either.
We can therefore, check if our user is authenticated directly in the html file where our navigation bar appears. With a set of if/else statement and
conditional rendering with Jinja we can decide which list item should not be displayed:

![image](https://user-images.githubusercontent.com/55893421/117735285-286e7a00-b1c3-11eb-870f-c54c23aa2a06.png)






[DevMo](http://gonebal.pythonanywhere.com/)

# Introduction

DevMo is like [BevMo](https://www.bevmo.com/), but Dev stands for Developer.
If you have used Dribble or Behance before, it will be very familiar to you.

![preview](_screenshots/preview2.gif?raw=true "Title")

You can check it out by clicking on the [following link](http://gonebal.pythonanywhere.com/).

The Main idea is Instagram for Tech People. You have that Instagram feed, but
instead of cute and nice selfies, you get useful posts with projects, code, new
updates on any programming language or framework.

There are a lot of categories you can choose: Web Development, UI/UX Design,
JavaScript, Python, Django etc.

You are free to post your own projects and developments! Spend your time Wisely!

### Main features

Okay, so I have my directory templates with 6 HTML pages. Layout, Index(Main Feed),
Register/Login together in register.HTML, Newpost(Create New Post), Publication,
Profile.

CSS files and JS files to those pages are located in static directory.

My project is Ready-to-Upload-and-Use Website. And I will keep work on it in
the future to make it even better!

I used Django to build this project and it has 4 models. For front-end I used
CSS with JavaScript. JavaScript helped me a lot with fetch method, animation
and just in general.

The Website has features like Creating new publication, Search through existing
publication by name in Title or in the description, Categories Filter, Add to
favorites, Like post, Subscribe to other users.

The Website is mobile-responsive through Media queries(@media).

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/GonEbal/devmo2.git
    $ cd devmo2
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver

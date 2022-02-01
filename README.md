# Ridehare Backend
An open-source backend for an app helping students find rides on campus.

## Installation

This project uses the Django Rest Framework. 
Clone the project with

```
git clone https://github.com/cuappdev/rideshare-backend.git
```
After cloning the project, `cd` into the new directory and install dependencies with

```
$ python3 -m pip install virtualenv venv
$ . venv/bin/activate
(venv) $ python3 -m pip install -r requirements.txt
```

You can run the project with

```
(venv) $ python3 manage.py runserver
```
You can update the database schema with
```
(venv) $ python3 manage.py makemigrations
(venv) $ python3 manage.py migrate
```

## Environment Variables

It's recommended to use direnv. The required environment variables for this API are listed in envrc.template.

To use direnv with this repository, run the following and set the variables appropriately.
```
cp envrc.template .envrc
```
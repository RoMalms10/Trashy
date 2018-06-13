# Trashy
Trash Can Locator

## Description
Trashy is a responsive web app that shows the nearest 20 trash cans near the user by grabbing their geolocation. The initial data set was from DataSF data set and the rest are user submitted. If a user wants to submit a trash can location, they must sign in using the `login` button on the top right.

## Environment

* __OS:__ Ubuntu 14.04 LTS
* __language:__ Python 3.4.3
* __web server:__ nginx/1.4.6
* __application server:__ Flask 0.12.2
* __web server gateway:__ gunicorn (version 19.7.1)
* __database:__ SQLite3 3.8.2

## Configuration Files

The `/config/` directory contains configuration files for `nginx` and the
Upstart scripts.  The nginx configuration file is for the configuration file in
the path: `/etc/nginx/sites-available/default`.  The enabled site is a sym link
to that configuration file.  The upstart script should be saved in the path:
`/etc/init/[FILE_NAME.conf]`.  To begin this service, execute:

```
$ sudo start trashy.conf
```
This script's main task is to execute the following `gunicorn` command:

```
$ exec gunicorn --workers 4 --bind unix:/home/ubuntu/Trashy/trash.sock -m 007 wsgi
```

The `gunicorn` command starts an instance of a Flask Application.

---

## Setup

This project comes with various setup scripts to support automation, especially
during maintanence or to scale the entire project.  The following files are the
setupfiles along with a brief explanation:

* **`dev/setup.sql`:** Drops test and dev databases, and then reinitializes
the database.

  * Usage: `$ cat dev/setup_db.sql | mysql -uroot -p`
  
## Author
* Robert Malmstein, [RoMalms10](https://github.com/RoMalms10) | [@RobertMalmstein](https://twitter.com/RobertMalmstein)

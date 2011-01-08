Base Track
===================

Base Track is a task tracker based on `django_odesk.task`.

Before Start
------------

To start with project you need to have:

 - Python (tested on version 2.6)
 - git
 - virtualenv

Linux/Unix is not required, but recommended.

Run dev instance
----------------

To run and test basetrack on your own host, you need to do following:

 1. Obtain project code, for example clone this repo:
 `git clone git://github.com:j2a/basetrack-sprint.git` and go into it
 `cd basetrack-sprint`.

 2. Run `python ./boostrap.py` in terminal.

 3. You need to create oDesk API access keys for your dev instance at
 <http://www.odesk.com/services/api/apply> with callback url
 http://localhost:8000/odesk-auth/callback/

 5. Place your keys to `local_settings.py`.

 6. Define oDesk company and teamroom for tasks and fill this setting in local
 config.

 7. Be sure users you want to be staff/superuser is listed in local settings as
 odesk admins/superusers.

 7. Make syncdb: `ve/bin/python manage.py syncdb --noinput`.

 8. Load default data: `ve/bin/python manage.py loaddata fixtures/*`

 9. Run dev server `ve/bin/python manage.py runserver` and go to
 <http://localhost:8000>.

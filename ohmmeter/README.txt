
Requirements
------------

OhmMeter requires such Debian/Ubuntu packages:

 * PyGTK (python-gtk2)
 * WebKit (python-webkit)
 * python-odesk (should be installed via pip)


How to setup
------------

Prepare oDesk API keys:

 1. Go to oDesk API center: http://www.odesk.com/services/api/apply
 2. Give the name for app: say, yyurevich-ohmmeter
 3. Select project type: web
 4. Set-up callback url as: https://odesk-auth-proxy.appspot.com/<yourapp-name>/callback
    e.g. for our app yyurevich-ohmmeter it would be
    https://odesk-auth-proxy.appspot.com/yyurevich-ohmmeter/callback.
 5. Write some description :)
 6. Set API usage as "101-500" per day.
 7. Flag checkbox that you agreed with oDesk API terms of use
 8. Click apply
 9. You should see your new key with available "Key" and "Secret".

Obtain token:

 1. Copy creds.ini.def to creds.ini
 2. Fill in the values for public and secret keys from step #9 of "Prepare oDesk API keys"
 3. Run obtain_token.py
 4. Sign in into odesk and allow access to your account for your app from step #2 of "Prepare oDesk API keys"
 5. If all is going smooth, token should appear in creds.ini.

Run the "climeter.py" and you'll see how many hours you worked today :)

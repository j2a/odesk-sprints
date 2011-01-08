odesk-timelog-rework
--------------------

The target for sprint: make features I want to use with oDesk time logger.

**Ohmmeter**. Time meter done right.

Time meter should show the time worked right now,
not few hours ago (as godesk->meter shows now) and
it should show in human readable format (e.g. hours and minutes).

**odesk-auth-proxy**. Authentication proxy for desktop apps.

While playing around ohmmeter I found that oDesk API is not ready
for desktop apps. So I wrote small auth proxy powered by Google
App Engine and hosted it at http://odesk-auth-proxy.appspot.com

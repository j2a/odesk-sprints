# -*- coding: utf-8 -*-
import datetime
import odesk
from tipfy import RequestHandler, Response

from apps.odesk_auth_proxy.models import OdeskApplication


class IndexHandler(RequestHandler):
    def get(self):
        return Response('oDesk API auth proxy for desktop apps')


class SubmitKeysHandler(RequestHandler):
    def get(self, app):
        stored_app = OdeskApplication.get_by_key_name(app)
        if not stored_app:
            r = Response(
                'There is no app %s registered in oDesk Auth Proxy' % app)
            r.status_code = 404
            return r
        client = odesk.Client(stored_app.public_key, stored_app.secret_key)
        return Response(client.auth.auth_url())


    def post(self, app):
        public = self.request.form.get('public')
        secret = self.request.form.get('secret')
        if not public and not secret:
            r = Response('Bad request: both public and secret is required')
            r.status_code = 400
            return r
        stored_app = OdeskApplication.get_by_key_name(app)
        if not stored_app:
            stored_app = OdeskApplication(key_name=app)
            stored_app.created = datetime.datetime.utcnow()
        stored_app.public_key = public
        stored_app.secret_key = secret
        stored_app.updated = datetime.datetime.utcnow()

        stored_app.put()
        return Response('Ok')


class AuthCallbackHandler(RequestHandler):
    def get(self, app):
        frob = self.request.args.get('frob')
        if not frob:
            r = Response("Missed required param frob")
            r.status_code = 400
            return r

        stored_app = OdeskApplication.get_by_key_name(app)
        if not stored_app:
            r = Response(
                'There is no app %s registered in oDesk Auth Proxy' % app)
            r.status_code = 404
            return r
        client = odesk.Client(stored_app.public_key, stored_app.secret_key)
        auth_token, user = client.auth.get_token(frob)
        return Response(auth_token)

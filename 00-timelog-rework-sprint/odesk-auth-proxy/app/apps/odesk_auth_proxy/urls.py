# -*- coding: utf-8 -*-
from tipfy import Rule


def get_rules(app):
    rules = [
        Rule('/', endpoint='odesk-index',
             handler='apps.odesk_auth_proxy.handlers.IndexHandler'),
        Rule('/a/<string:app>', endpoint='odesk-submit-keys',
             handler='apps.odesk_auth_proxy.handlers.SubmitKeysHandler'),
        Rule('/a/<string:app>/callback', endpoint='odesk-callback',
             handler='apps.odesk_auth_proxy.handlers.AuthCallbackHandler')
    ]

    return rules

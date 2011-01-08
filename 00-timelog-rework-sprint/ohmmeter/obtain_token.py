#!/usr/bin/env

import odesk
import gtk
import webkit
import re
import ConfigParser

token_uri_pattern = re.compile(
    r'https://odesk-auth-proxy.appspot.com/a/.\w+/callback\?frob=.+')

class WebBrowserWindow(gtk.Window):
    def __init__(self, *args, **kwargs):
        gtk.Window.__init__(self, *args, **kwargs)
        self.browser = webkit.WebView()
        self.add(self.browser)
        self.connect('destroy', _cb_destroy)



def main(public, secret):
    client = odesk.Client(public, secret)
    auth_url = client.auth.auth_url()
    window = WebBrowserWindow()
    window.show_all()
    window.browser.open(auth_url)
    window.browser.connect('load-finished', _cb_load_finished, window)
    gtk.main()

def _cb_destroy(window):
    window.destroy()
    gtk.main_quit()

def _cb_load_finished(view, frame, window):
    uri = frame.get_uri()
    if token_uri_pattern.match(uri):
        token = str(frame.get_data_source().get_data())
        cfg = ConfigParser.ConfigParser()
        cfg.read(['creds.ini'])
        cfg.set('odesk-auth', 'token', token)
        cfg.write(open('creds.ini', 'w'))
        window.destroy()
        gtk.main_quit()

if __name__ == '__main__':
    import ConfigParser
    cfg = ConfigParser.ConfigParser()
    cfg.read(['creds.ini'])
    main(
        cfg.get('odesk-auth', 'public-key'),
        cfg.get('odesk-auth', 'secret-key'))

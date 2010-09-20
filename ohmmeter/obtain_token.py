#!/usr/bin/env

import odesk
import gtk
import webkit

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
    gtk.main()

def _cb_destroy(window):
    window.destroy()
    gtk.main_quit()

if __name__ == '__main__':
    import ConfigParser
    cfg = ConfigParser.ConfigParser()
    cfg.read(['creds.ini'])
    main(
        cfg.get('odesk-auth', 'public-key'),
        cfg.get('odesk-auth', 'secret-key'))
